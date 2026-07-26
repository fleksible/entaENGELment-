"""
src/core/action_gate.py

Nicht-ausführende Action-Gate-Schnittstelle für den Evidence Routing Kernel v0.1.

Zweck (siehe docs/annex/ACTION_GATE_v0_1.md):
Aus einer extern gefundenen Handlungsanweisung (z.B. eine Install-Zeile aus einer
README, einem Makefile oder einer requirements-Datei) erzeugt dieses Modul
ausschließlich ein strukturiertes, nicht ausführbares ``ActionProposal``-Manifest.

Harte Grenzen dieses Moduls:
- Es führt **nichts** aus: keine Shell, kein Subprozess, kein Netzwerk, keine
  Installation, kein Dateisystemeffekt.
- ``proposed_command`` bleibt ein reiner String und wird niemals in ausführbare
  Tokens zerlegt oder interpretiert.
- Unbekannte Registry/Herkunft und nicht überprüfbare Version führen fail-closed
  zu ``HOLD`` (kein stiller Durchlass).
- Externes Material ist untrusted; das Manifest ist ein Vorschlag, keine
  Autorität. Jede reale Nebenwirkung ist ``HUMAN_ONLY``.

Das Modul importiert bewusst keine ausführenden oder netzwerkfähigen Bibliotheken
(``subprocess``, ``os.system``, ``socket``, ``urllib`` …). ``tests/ethics``
prüft diese Grenze strukturell.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import InitVar, asdict, dataclass
from enum import Enum
from types import MappingProxyType

from .evidence_routing import (
    GUARD_HOLD,
    GUARD_PROPOSE,
    TRUST_REVIEWED,
    TRUST_TRUSTED,
    VISIBILITY_PRIVATE,
    VISIBILITY_PUBLIC,
    VISIBILITY_REDUCED,
    MaterialRef,
    normalize_trust,
)

# ---------------------------------------------------------------------------
# Schema- und Vokabular-Konstanten
# ---------------------------------------------------------------------------

ACTION_GATE_SCHEMA_VERSION = "action_gate.v0.1"

# Gate-Zustand: bewusst nur PROPOSE/HOLD. Der Action-Gate v0.1 emittiert keinen
# Zustand, der Ausführung erlaubt. HOLD ist der fail-closed Standard.
ACTION_GATE_STATES = frozenset({GUARD_PROPOSE, GUARD_HOLD})

_KNOWN_VISIBILITIES = frozenset({VISIBILITY_PRIVATE, VISIBILITY_REDUCED, VISIBILITY_PUBLIC})

# Trust-Level, die eine Materialquelle nicht als untrusted markieren.
_NON_UNTRUSTED_TRUST = frozenset({TRUST_TRUSTED, TRUST_REVIEWED})

# Kleine, fail-closed Allowlist bekannter Paket-Registries/Herkünfte, gekeyt nach
# Ökosystem. Bekanntheit heißt ausdrücklich nicht "vertrauenswürdig zur
# Ausführung" — sie unterscheidet nur eine zum Ökosystem passende Registry von
# unbekannter oder falsch zugeordneter Herkunft. Eine Registry, die nicht zum
# angegebenen Ökosystem gehört (z.B. npm + pypi.org), sowie ein unbekanntes
# Ökosystem führen fail-closed zu HOLD.
# MappingProxyType macht die Default-Allowlist read-only: kein Consumer kann sie
# prozessweit erweitern (`DEFAULT_KNOWN_REGISTRIES['npm'] = ...` schlägt fehl) und
# so das Gate für andere still aufweiten. Die Werte sind bereits frozensets.
DEFAULT_KNOWN_REGISTRIES: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "pypi": frozenset({"pypi", "pypi.org"}),
        "npm": frozenset({"npm", "registry.npmjs.org"}),
        "cargo": frozenset({"cargo", "crates.io"}),
        "rubygems": frozenset({"rubygems", "rubygems.org"}),
        "go": frozenset({"go", "pkg.go.dev"}),
        "maven": frozenset({"maven", "maven-central", "maven central"}),
    }
)

# Maximale Länge einer Versionsangabe. Längere Eingaben sind für diese kleine,
# rein lokale Schnittstelle nicht nötig und fallen deterministisch auf HOLD.
_MAX_VERSION_LENGTH = 128

# npm: striktes SemVer 2.0.0 ohne ``v``-/``=``-Normalisierung. Numerische
# Prerelease-Komponenten mit führender Null werden nach dem Match separat
# abgewiesen.
_NPM_SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9][0-9]*)\."
    r"(?P<minor>0|[1-9][0-9]*)\."
    r"(?P<patch>0|[1-9][0-9]*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$",
    re.ASCII,
)

# PyPI: konservativer kanonischer PEP-440-Public-Identifier. Das Gate verlangt
# mindestens Major.Minor.Patch und akzeptiert bewusst keine lokalen ``+label``-
# Versionen für die öffentliche PyPI-Registry.
_PYPI_CANONICAL_VERSION_RE = re.compile(
    r"^(?:[1-9][0-9]*!)?"
    r"(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){2,}"
    r"(?:(?:a|b|rc)(?:0|[1-9][0-9]*))?"
    r"(?:\.post(?:0|[1-9][0-9]*))?"
    r"(?:\.dev(?:0|[1-9][0-9]*))?$",
    re.ASCII,
)

# Verifikationsstatus, der eine überprüfte Quelle bezeugt.
VERIFICATION_VERIFIED = "verified"

# Sichtbarkeits-Restriktivität (kleiner = privater). Ein Proposal darf niemals
# öffentlicher sein als seine Materialquelle.
_VISIBILITY_ORDER = {VISIBILITY_PRIVATE: 0, VISIBILITY_REDUCED: 1, VISIBILITY_PUBLIC: 2}

# Skalare Felder des Manifests, die echte Strings sein müssen.
_SCALAR_STRING_FIELDS = (
    "action_id",
    "schema_version",
    "source_material_ref",
    "proposed_command",
    "ecosystem",
    "package_or_resource",
    "requested_version",
    "registry_or_origin",
    "reversibility",
    "verification_status",
    "guard_state",
    "responsibility_class",
    "visibility",
)


class ResponsibilityClass(str, Enum):
    """Verantwortungsklasse der vorgeschlagenen Aktion (nicht des Gates selbst).

    Die Berechnung des Manifests ist immer COMPUTATIONAL. Diese Klasse beschreibt
    die *vorgeschlagene Handlung*:

    - COMPUTATIONAL: deterministisch, ohne externe Nebenwirkung, vollständig
      überprüft. Nur diese Klasse darf ohne menschliche Freigabe weitergereicht
      werden.
    - IN_BETWEEN: effektfrei, aber unaufgelöst (unbekannte Registry, nicht
      gepinnte Version, unverifizierte oder untrusted Quelle). Nur Review-Kandidat.
    - HUMAN_ONLY: reale externe Nebenwirkung (Netzwerk, Dateisystem, Prozess,
      Installation) oder Irreversibilität. Erfordert eine explizite, widerrufbare
      menschliche Entscheidung; darf niemals durch einen Agenten substituiert
      werden.
    """

    COMPUTATIONAL = "COMPUTATIONAL"
    IN_BETWEEN = "IN_BETWEEN"
    HUMAN_ONLY = "HUMAN_ONLY"


class ActionReasonCode(str, Enum):
    """Geschlossenes Reason-Code-Vokabular des Action-Gate (keine dynamischen Codes).

    Bewusst getrennt vom ``ReasonCode`` des Claim-Kernels: Action-Gate und
    Claim-Transition sind verschiedene Übergangssysteme und dürfen ihre
    Vokabulare nicht vermischen.
    """

    ACTION_PROPOSAL_ONLY = "ACTION_PROPOSAL_ONLY"
    NO_EXECUTION = "NO_EXECUTION"
    SHELL_FRAGMENT_INERT = "SHELL_FRAGMENT_INERT"
    REGISTRY_KNOWN = "REGISTRY_KNOWN"
    REGISTRY_UNKNOWN = "REGISTRY_UNKNOWN"
    VERSION_PINNED = "VERSION_PINNED"
    VERSION_UNVERIFIABLE = "VERSION_UNVERIFIABLE"
    SOURCE_VERIFIED = "SOURCE_VERIFIED"
    SOURCE_UNVERIFIED = "SOURCE_UNVERIFIED"
    NETWORK_REQUIRED = "NETWORK_REQUIRED"
    FILESYSTEM_EFFECT = "FILESYSTEM_EFFECT"
    PROCESS_EFFECT = "PROCESS_EFFECT"
    IRREVERSIBLE_EFFECT = "IRREVERSIBLE_EFFECT"
    UNTRUSTED_SOURCE_MATERIAL = "UNTRUSTED_SOURCE_MATERIAL"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"


_KNOWN_ACTION_REASON_CODES = frozenset(code.value for code in ActionReasonCode)
_KNOWN_RESPONSIBILITY_CLASSES = frozenset(rc.value for rc in ResponsibilityClass)

# Reason-Codes, die im Builder immer ``hold()`` auslösen. Der interne
# Kohärenzcheck bindet sie exakt an HOLD + menschliche Freigabe.
_HOLD_IMPLYING_REASON_CODES = frozenset(
    {
        ActionReasonCode.REGISTRY_UNKNOWN.value,
        ActionReasonCode.VERSION_UNVERIFIABLE.value,
        ActionReasonCode.SOURCE_UNVERIFIED.value,
        ActionReasonCode.NETWORK_REQUIRED.value,
        ActionReasonCode.FILESYSTEM_EFFECT.value,
        ActionReasonCode.PROCESS_EFFECT.value,
        ActionReasonCode.IRREVERSIBLE_EFFECT.value,
        ActionReasonCode.UNTRUSTED_SOURCE_MATERIAL.value,
    }
)

# Ein über JSON rekonstruiertes Manifest darf die vom Gate berechneten Felder
# nicht selbst wählen. Nur ``build_action_proposal`` besitzt dieses
# prozesslokale, nicht serialisierbare Konstruktionstoken. Es ist keine
# Authentisierung oder Sandbox-Grenze gegen bösartigen Code im selben Prozess.
_ACTION_PROPOSAL_BUILDER_TOKEN = object()


class ActionGateError(ValueError):
    """Fail-closed Fehler des Action-Gate mit kontrollierten Reason-Codes."""

    def __init__(self, message: str, reason_codes: Sequence[ActionReasonCode] = ()) -> None:
        super().__init__(message)
        self.reason_codes: tuple[ActionReasonCode, ...] = tuple(reason_codes)


# ---------------------------------------------------------------------------
# Manifest-Modell
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ActionProposal:
    """Nicht ausführbares Manifest einer extern gefundenen Handlungsanweisung.

    Alle Felder sind serialisierbar. ``proposed_command`` ist reiner Text und wird
    niemals ausgeführt oder geparst. ``guard_state`` ist immer PROPOSE oder HOLD;
    ein ausführender Zustand existiert in v0.1 nicht.
    """

    action_id: str
    schema_version: str
    source_material_ref: str
    proposed_command: str
    ecosystem: str
    package_or_resource: str
    requested_version: str
    registry_or_origin: str
    network_required: bool
    filesystem_effects: tuple[str, ...]
    process_effects: tuple[str, ...]
    reversibility: str
    verification_status: str
    guard_state: str
    responsibility_class: str
    human_approval_required: bool
    reason_codes: tuple[str, ...]
    visibility: str
    _builder_token: InitVar[object | None] = None

    def __post_init__(self, _builder_token: object | None) -> None:
        """Builder-sealed Manifestfelder und ihre Kohärenz erzwingen.

        ``ActionProposal`` ist öffentlich lesbar, aber nicht öffentlich
        konstruierbar: Ein deserialisiertes Mapping darf ``guard_state``,
        ``responsibility_class`` und Reason-Codes nicht selbst setzen. Es muss
        mit Materialquelle und Registry-Policy erneut durch
        :func:`build_action_proposal` laufen.
        """
        if _builder_token is not _ACTION_PROPOSAL_BUILDER_TOKEN:
            raise ActionGateError(
                "ActionProposal is builder-only; re-evaluate data with build_action_proposal"
            )

        # Skalare Textfelder müssen echte Strings sein — sonst könnte ein direkt
        # konstruiertes Manifest z.B. ``proposed_command=['curl', 'x']`` tragen
        # und die Invariante "Befehl ist inerter Text" verletzen.
        for field_name in _SCALAR_STRING_FIELDS:
            if type(getattr(self, field_name)) is not str:
                raise ActionGateError(f"{field_name} must be a string")

        # Kollektionen fail-closed normalisieren: ein blindes ``tuple()`` würde
        # einen bloßen String in Zeichen zerlegen und Nicht-String-Einträge
        # (z.B. ``[123]``) durchreichen. Beides wird abgewiesen.
        for field_name in ("filesystem_effects", "process_effects", "reason_codes"):
            value = getattr(self, field_name)
            if type(value) not in (list, tuple):
                raise ActionGateError(
                    f"{field_name} must be a sequence of strings, not {type(value).__name__}"
                )
            if not all(type(item) is str for item in value):
                raise ActionGateError(f"{field_name} must contain only strings")
            object.__setattr__(self, field_name, tuple(value))

        if self.schema_version != ACTION_GATE_SCHEMA_VERSION:
            raise ActionGateError(f"unknown schema_version: {self.schema_version!r}")
        if self.guard_state not in ACTION_GATE_STATES:
            raise ActionGateError(f"invalid guard_state: {self.guard_state!r}")
        if self.responsibility_class not in _KNOWN_RESPONSIBILITY_CLASSES:
            raise ActionGateError(f"invalid responsibility_class: {self.responsibility_class!r}")
        if self.visibility not in _KNOWN_VISIBILITIES:
            raise ActionGateError(f"invalid visibility: {self.visibility!r}")
        if (
            type(self.network_required) is not bool
            or type(self.human_approval_required) is not bool
        ):
            raise ActionGateError("network_required and human_approval_required must be bool")
        unknown_codes = [c for c in self.reason_codes if c not in _KNOWN_ACTION_REASON_CODES]
        if unknown_codes:
            raise ActionGateError(f"unknown reason codes: {unknown_codes}")
        if len(self.reason_codes) != len(set(self.reason_codes)):
            raise ActionGateError("reason_codes must not contain duplicates")

        codes = set(self.reason_codes)
        required_baseline = {
            ActionReasonCode.ACTION_PROPOSAL_ONLY.value,
            ActionReasonCode.NO_EXECUTION.value,
            ActionReasonCode.SHELL_FRAGMENT_INERT.value,
        }
        if not required_baseline <= codes:
            raise ActionGateError("proposal is missing mandatory inert baseline reason codes")

        def expect_code(code: ActionReasonCode, expected: bool) -> None:
            if (code.value in codes) != expected:
                raise ActionGateError(f"{code.value} inconsistent with descriptive manifest fields")

        # Genau eine Registry-Entscheidung muss aus der vom Builder verwendeten
        # Allowlist stammen. Die Policy selbst wird nicht serialisiert; deshalb
        # sind rohe Manifeste nicht rekonstruierbar und der Konstruktor ist oben
        # versiegelt.
        has_registry_known = ActionReasonCode.REGISTRY_KNOWN.value in codes
        has_registry_unknown = ActionReasonCode.REGISTRY_UNKNOWN.value in codes
        if has_registry_known == has_registry_unknown:
            raise ActionGateError("proposal must carry exactly one registry decision")

        pinned = _is_pinned_version(self.requested_version, self.ecosystem)
        expect_code(ActionReasonCode.VERSION_PINNED, pinned)
        expect_code(ActionReasonCode.VERSION_UNVERIFIABLE, not pinned)

        verified = self.verification_status.strip().lower() == VERIFICATION_VERIFIED
        expect_code(ActionReasonCode.SOURCE_VERIFIED, verified)
        expect_code(ActionReasonCode.SOURCE_UNVERIFIED, not verified)

        filesystem_effect = bool(self.filesystem_effects)
        process_effect = bool(self.process_effects)
        irreversible = self.reversibility.strip().lower() != "reversible"
        expect_code(ActionReasonCode.NETWORK_REQUIRED, self.network_required)
        expect_code(ActionReasonCode.FILESYSTEM_EFFECT, filesystem_effect)
        expect_code(ActionReasonCode.PROCESS_EFFECT, process_effect)
        expect_code(ActionReasonCode.IRREVERSIBLE_EFFECT, irreversible)

        expected_hold = bool(codes & _HOLD_IMPLYING_REASON_CODES)
        expected_guard = GUARD_HOLD if expected_hold else GUARD_PROPOSE
        if self.guard_state != expected_guard:
            raise ActionGateError("guard_state inconsistent with computed reason codes")

        expect_code(ActionReasonCode.HUMAN_APPROVAL_REQUIRED, expected_hold)
        if self.human_approval_required != expected_hold:
            raise ActionGateError("human_approval_required inconsistent with guard_state")

        if self.network_required or filesystem_effect or process_effect or irreversible:
            expected_responsibility = ResponsibilityClass.HUMAN_ONLY.value
        elif expected_hold:
            expected_responsibility = ResponsibilityClass.IN_BETWEEN.value
        else:
            expected_responsibility = ResponsibilityClass.COMPUTATIONAL.value
        if self.responsibility_class != expected_responsibility:
            raise ActionGateError("responsibility_class inconsistent with effects and guard_state")

    def to_manifest(self) -> dict[str, object]:
        """Kanonische, serialisierbare (JSON-native) Manifest-Darstellung.

        Die intern unveränderlichen Tupel werden defensiv als frische Listen
        ausgegeben: Ein Aufrufer kann das Manifest mutieren, ohne den frozen
        Proposal oder dessen ``manifest_digest`` zu verändern.
        """
        data = asdict(self)
        data["filesystem_effects"] = list(self.filesystem_effects)
        data["process_effects"] = list(self.process_effects)
        data["reason_codes"] = list(self.reason_codes)
        return data

    def manifest_digest(self) -> str:
        """Deterministischer Integritätsverweis über das kanonisierte Manifest.

        Der Digest bezeugt Integrität, nicht Wahrheit oder Autorisierung.
        """
        serialized = json.dumps(
            self.to_manifest(),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Deterministische lokale Checks (COMPUTATIONAL)
# ---------------------------------------------------------------------------


def _is_pinned_version(value: str, ecosystem: str) -> bool:
    """Eine konservative, ökosystemspezifische Exact-Version prüfen.

    v0.1 validiert nur die beiden tatsächlich implementierten Grammatiken:

    - ``npm``: striktes SemVer 2.0.0;
    - ``pypi``: kanonischer PEP-440-Public-Identifier mit mindestens drei
      Release-Komponenten.

    Für weitere bekannte Registries fehlt ein lokaler Exact-Version-Parser.
    Sie bleiben deshalb fail-closed ``VERSION_UNVERIFIABLE`` statt durch einen
    unsicheren gemeinsamen Näherungscheck als gepinnt zu gelten.
    """
    if type(value) is not str or type(ecosystem) is not str:
        return False
    if value != value.strip() or not value or len(value) > _MAX_VERSION_LENGTH:
        return False

    normalized_ecosystem = ecosystem.strip().lower()
    if normalized_ecosystem == "npm":
        match = _NPM_SEMVER_RE.fullmatch(value)
        if match is None:
            return False
        prerelease = match.group("prerelease")
        if prerelease is None:
            return True
        return all(
            not (identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"))
            for identifier in prerelease.split(".")
        )

    if normalized_ecosystem == "pypi":
        return _PYPI_CANONICAL_VERSION_RE.fullmatch(value) is not None

    return False


def _normalize_effects(effects: Sequence[str] | None) -> list[str]:
    """Effektliste auf nicht-leere, aussagekräftige String-Einträge reduzieren."""
    if effects is None:
        return []
    if type(effects) not in (list, tuple):
        raise ActionGateError(
            "effects must be a list or tuple of strings",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )
    normalized: list[str] = []
    for item in effects:
        if type(item) is not str:
            raise ActionGateError(
                "each effect entry must be a string",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
        token = item.strip()
        if token and token.lower() not in {"none", "no", "false"}:
            normalized.append(token)
    return normalized


def _registry_is_known(
    ecosystem: str,
    registry_or_origin: str,
    known_registries: Mapping[str, frozenset[str]],
) -> bool:
    """Eine Registry-Zuordnung kontrolliert und fail-closed auswerten."""
    # Nur eingebaute, seiteneffektfreie Container akzeptieren. Eine beliebige
    # Mapping-Implementierung könnte bereits in ``get`` Aufrufercode ausführen
    # und damit das Reinheitsversprechen des Gates brechen.
    if known_registries is DEFAULT_KNOWN_REGISTRIES:
        policy_items = tuple(DEFAULT_KNOWN_REGISTRIES.items())
    elif type(known_registries) is dict:
        try:
            policy_items = tuple(known_registries.items())
        except RuntimeError as exc:
            raise ActionGateError(
                "known_registries changed while being read",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            ) from exc
    else:
        raise ActionGateError(
            "known_registries must be the default policy or a built-in dict",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )

    normalized_policy: dict[str, frozenset[str]] = {}
    for policy_ecosystem, registries in policy_items:
        if (
            type(policy_ecosystem) is not str
            or not policy_ecosystem
            or policy_ecosystem != policy_ecosystem.strip()
        ):
            raise ActionGateError(
                "registry policy keys must be non-empty strings without edge whitespace",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
        if type(registries) not in (set, frozenset, list, tuple):
            raise ActionGateError(
                "registry allowlist entries must be string collections",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
        if not all(type(item) is str and item and item == item.strip() for item in registries):
            raise ActionGateError(
                "registry allowlist entries must contain canonical non-empty strings",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
        normalized_ecosystem = policy_ecosystem.lower()
        if normalized_ecosystem in normalized_policy:
            raise ActionGateError(
                "registry policy contains duplicate normalized ecosystem keys",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
        normalized_policy[normalized_ecosystem] = frozenset(item.lower() for item in registries)

    return registry_or_origin.lower() in normalized_policy.get(ecosystem.lower(), frozenset())


def _resolve_visibility(requested: str | None, source_visibility: object) -> str:
    """Proposal-Sichtbarkeit fail-closed bestimmen, ohne Eskalation über die Quelle.

    - ``requested is None`` → das Proposal erbt die Sichtbarkeit der Quelle.
    - sonst → das Restriktivere (privater) von Wunsch und Quelle.

    Eine unbekannte Quell-Sichtbarkeit wird fail-closed als ``private`` behandelt.
    """
    if type(source_visibility) is str and source_visibility in _KNOWN_VISIBILITIES:
        source = source_visibility
    else:
        source = VISIBILITY_PRIVATE

    if requested is None:
        return source
    if type(requested) is not str or requested not in _KNOWN_VISIBILITIES:
        raise ActionGateError(
            f"unknown visibility class: {requested!r}",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )
    # Kleinere Ordnungszahl = privater = restriktiver.
    if _VISIBILITY_ORDER[requested] <= _VISIBILITY_ORDER[source]:
        return requested
    return source


def build_action_proposal(
    *,
    action_id: str,
    source_material: MaterialRef,
    proposed_command: str,
    ecosystem: str,
    package_or_resource: str,
    requested_version: str,
    registry_or_origin: str,
    network_required: bool,
    filesystem_effects: Sequence[str] | None = None,
    process_effects: Sequence[str] | None = None,
    reversibility: str = "unknown",
    verification_status: str = "unverified",
    known_registries: Mapping[str, frozenset[str]] = DEFAULT_KNOWN_REGISTRIES,
    visibility: str | None = None,
) -> ActionProposal:
    """Ein nicht ausführbares ``ActionProposal`` aus einer Handlungsanweisung bauen.

    Diese Funktion ist rein und deterministisch. Sie führt ``proposed_command``
    niemals aus, öffnet keine Netzwerkverbindung und schreibt nichts. Sie berechnet
    ausschließlich ein Manifest samt fail-closed Gate-Zustand.

    Fail-closed Regeln:
    - unbekannte oder nicht zum Ökosystem passende Registry/Herkunft → ``HOLD``
      (``REGISTRY_UNKNOWN``);
    - nicht überprüfbare/ungepinnte Version → ``HOLD`` (``VERSION_UNVERIFIABLE``);
    - unverifizierte Quelle → ``HOLD`` (``SOURCE_UNVERIFIED``);
    - Netzwerk/Dateisystem/Prozess-Effekt oder Irreversibilität → ``HOLD``;
    - untrusted Materialquelle → ``HOLD`` (``UNTRUSTED_SOURCE_MATERIAL``).

    ``visibility`` wird niemals über die Sichtbarkeit der Materialquelle
    hinaus eskaliert: bei ``None`` erbt das Proposal die Quell-Sichtbarkeit,
    sonst wird auf das Restriktivere von Wunsch und Quelle geklemmt. So kann
    kein privater ``proposed_command`` über ein ``reduced``/``public``-Label
    diffundieren.
    """
    if type(source_material) is not MaterialRef:
        raise ActionGateError(
            "source_material must be a MaterialRef",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )
    for name, value in (
        ("action_id", action_id),
        ("proposed_command", proposed_command),
        ("ecosystem", ecosystem),
        ("package_or_resource", package_or_resource),
        ("requested_version", requested_version),
        ("registry_or_origin", registry_or_origin),
        ("reversibility", reversibility),
        ("verification_status", verification_status),
    ):
        if type(value) is not str:
            raise ActionGateError(
                f"{name} must be a string",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
    for name, value in (
        ("action_id", action_id),
        ("source_material.material_id", source_material.material_id),
        ("proposed_command", proposed_command),
        ("package_or_resource", package_or_resource),
    ):
        if type(value) is not str or not value.strip():
            raise ActionGateError(
                f"{name} must be a non-empty string",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
    for name, value in (
        ("action_id", action_id),
        ("source_material.material_id", source_material.material_id),
        ("ecosystem", ecosystem),
        ("package_or_resource", package_or_resource),
        ("registry_or_origin", registry_or_origin),
        ("reversibility", reversibility),
        ("verification_status", verification_status),
    ):
        if value != value.strip():
            raise ActionGateError(
                f"{name} must not contain leading or trailing whitespace",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
    if type(network_required) is not bool:
        raise ActionGateError(
            "network_required must be a bool",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )

    visibility = _resolve_visibility(visibility, source_material.visibility)
    fs_effects = _normalize_effects(filesystem_effects)
    proc_effects = _normalize_effects(process_effects)
    source_trust = normalize_trust(
        source_material.trust if type(source_material.trust) is str else None
    )

    # Reason-Codes werden in fester Reihenfolge angehängt → deterministisch.
    reasons: list[ActionReasonCode] = [
        ActionReasonCode.ACTION_PROPOSAL_ONLY,
        ActionReasonCode.NO_EXECUTION,
        ActionReasonCode.SHELL_FRAGMENT_INERT,
    ]
    guard_state = GUARD_PROPOSE  # optimistisch; jede Verletzung senkt auf HOLD.

    def hold(code: ActionReasonCode) -> None:
        nonlocal guard_state
        guard_state = GUARD_HOLD
        if code not in reasons:
            reasons.append(code)

    # Registry-/Herkunfts-Allowlist (fail-closed), gekeyt nach Ökosystem: eine
    # Registry muss zum angegebenen Ökosystem passen. Unbekanntes Ökosystem oder
    # falsch zugeordnete Registry (z.B. npm + pypi.org) → HOLD.
    if _registry_is_known(ecosystem, registry_or_origin, known_registries):
        reasons.append(ActionReasonCode.REGISTRY_KNOWN)
    else:
        hold(ActionReasonCode.REGISTRY_UNKNOWN)

    # Versions-Pin-Prüfung.
    if _is_pinned_version(requested_version, ecosystem):
        reasons.append(ActionReasonCode.VERSION_PINNED)
    else:
        hold(ActionReasonCode.VERSION_UNVERIFIABLE)

    # Quellen-Verifikation.
    if verification_status.strip().lower() == VERIFICATION_VERIFIED:
        reasons.append(ActionReasonCode.SOURCE_VERIFIED)
    else:
        hold(ActionReasonCode.SOURCE_UNVERIFIED)

    # Reale Nebenwirkungen (jede davon macht die Aktion HUMAN_ONLY).
    has_side_effect = False
    if network_required:
        hold(ActionReasonCode.NETWORK_REQUIRED)
        has_side_effect = True
    if fs_effects:
        hold(ActionReasonCode.FILESYSTEM_EFFECT)
        has_side_effect = True
    if proc_effects:
        hold(ActionReasonCode.PROCESS_EFFECT)
        has_side_effect = True
    # Nicht nachweisbar reversibel (inkl. ``unknown``) zählt fail-closed als
    # menschliche Grenze — die Spec ordnet Irreversibilität HUMAN_ONLY zu.
    irreversible = reversibility.strip().lower() != "reversible"
    if irreversible:
        hold(ActionReasonCode.IRREVERSIBLE_EFFECT)

    # Untrusted Materialquelle.
    if source_trust not in _NON_UNTRUSTED_TRUST:
        hold(ActionReasonCode.UNTRUSTED_SOURCE_MATERIAL)

    # Verantwortungsklasse der vorgeschlagenen Handlung ableiten. Reale
    # Nebenwirkung oder Irreversibilität erzwingt HUMAN_ONLY.
    if has_side_effect or irreversible:
        responsibility = ResponsibilityClass.HUMAN_ONLY
    elif guard_state == GUARD_HOLD:
        responsibility = ResponsibilityClass.IN_BETWEEN
    else:
        responsibility = ResponsibilityClass.COMPUTATIONAL

    # Menschliche Freigabe ist erforderlich, sobald etwas nicht fail-open
    # durchläuft: reale Nebenwirkung, Irreversibilität oder ein HOLD-Zustand.
    human_required = has_side_effect or irreversible or guard_state == GUARD_HOLD
    if human_required:
        reasons.append(ActionReasonCode.HUMAN_APPROVAL_REQUIRED)

    return ActionProposal(
        action_id=action_id,
        schema_version=ACTION_GATE_SCHEMA_VERSION,
        source_material_ref=source_material.material_id,
        proposed_command=proposed_command,
        ecosystem=ecosystem,
        package_or_resource=package_or_resource,
        requested_version=requested_version,
        registry_or_origin=registry_or_origin,
        network_required=network_required,
        filesystem_effects=tuple(fs_effects),
        process_effects=tuple(proc_effects),
        reversibility=reversibility,
        verification_status=verification_status,
        guard_state=guard_state,
        responsibility_class=responsibility.value,
        human_approval_required=human_required,
        reason_codes=tuple(code.value for code in reasons),
        visibility=visibility,
        _builder_token=_ACTION_PROPOSAL_BUILDER_TOKEN,
    )
