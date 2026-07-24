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
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from enum import Enum

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
DEFAULT_KNOWN_REGISTRIES: Mapping[str, frozenset[str]] = {
    "pypi": frozenset({"pypi", "pypi.org"}),
    "npm": frozenset({"npm", "registry.npmjs.org"}),
    "cargo": frozenset({"cargo", "crates.io"}),
    "rubygems": frozenset({"rubygems", "rubygems.org"}),
    "go": frozenset({"go", "pkg.go.dev"}),
    "maven": frozenset({"maven", "maven-central", "maven central"}),
}

# Versionsangaben, die keine überprüfbare, gepinnte Version darstellen.
_UNPINNED_VERSION_TOKENS = frozenset({"", "latest", "*", "any", "x", "unknown", "none"})

# Eine gepinnte Version muss mindestens Major.Minor.Patch auflösen. Kürzere
# Angaben (``1``, ``1.2``) werden von npm & Co. als X-Range interpretiert und
# gelten hier fail-closed als nicht gepinnt.
_MIN_PINNED_VERSION_COMPONENTS = 3

# Verifikationsstatus, der eine überprüfte Quelle bezeugt.
VERIFICATION_VERIFIED = "verified"


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

    def __post_init__(self) -> None:
        """Strukturelle Gültigkeit erzwingen — egal über welchen Konstruktionspfad.

        ``ActionProposal`` ist Teil der öffentlichen Core-API. Wird ein Manifest
        direkt (statt über :func:`build_action_proposal`) erzeugt, deserialisiert
        oder gecacht, darf es die geschlossenen Vokabulare und Enum-Grenzen nicht
        verletzen. Kollektionen werden defensiv zu Tupeln normalisiert.

        Diese Prüfung sichert **strukturelle** Konsistenz, nicht die vollständige
        Neuberechnung der Gate-Entscheidung: :func:`build_action_proposal` bleibt
        die alleinige Autorität für die abgeleiteten Felder.
        """
        # Kollektionen fail-closed normalisieren: ein blindes ``tuple()`` würde
        # einen bloßen String in Zeichen zerlegen und Nicht-String-Einträge
        # (z.B. ``[123]``) durchreichen. Beides wird abgewiesen.
        for field_name in ("filesystem_effects", "process_effects", "reason_codes"):
            value = getattr(self, field_name)
            if isinstance(value, str) or not isinstance(value, (list, tuple)):
                raise ActionGateError(
                    f"{field_name} must be a sequence of strings, not {type(value).__name__}"
                )
            if not all(isinstance(item, str) for item in value):
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
        if not isinstance(self.network_required, bool) or not isinstance(
            self.human_approval_required, bool
        ):
            raise ActionGateError("network_required and human_approval_required must be bool")
        unknown_codes = [c for c in self.reason_codes if c not in _KNOWN_ACTION_REASON_CODES]
        if unknown_codes:
            raise ActionGateError(f"unknown reason codes: {unknown_codes}")
        # Kohärenz: das HUMAN_APPROVAL_REQUIRED-Signal muss zum Flag passen.
        has_human_code = ActionReasonCode.HUMAN_APPROVAL_REQUIRED.value in self.reason_codes
        if has_human_code != self.human_approval_required:
            raise ActionGateError("human_approval_required flag inconsistent with reason codes")

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


def _is_pinned_version(value: str) -> bool:
    """True nur für eine konkret gepinnte, überprüfbare Version.

    Leere, offene oder Range-artige Angaben (``latest``, ``*``, ``^1``, ``>=2`` …)
    gelten fail-closed als nicht überprüfbar.
    """
    if not isinstance(value, str):
        return False
    token = value.strip().lower()
    if token in _UNPINNED_VERSION_TOKENS:
        return False
    # Range-/Wildcard-Operatoren markieren keine feste Version.
    if any(op in token for op in ("^", "~", ">", "<", "*", "=", " - ", "||", ",")):
        return False
    parts = token.split(".")
    # Eingebettete Wildcard- oder leere Komponenten (``1.x``, ``1.2.x``, ``x``)
    # sind nicht gepinnt, obwohl sie eine Ziffer enthalten.
    if any(part in ("x", "") for part in parts):
        return False
    # Teilweise Versionen (``1``, ``1.2``) sind X-Ranges, keine feste Version.
    if len(parts) < _MIN_PINNED_VERSION_COMPONENTS:
        return False
    # Mindestens ein Ziffernanteil ist für eine konkrete Version zu erwarten.
    return any(ch.isdigit() for ch in token)


def _normalize_effects(effects: Sequence[str] | None) -> list[str]:
    """Effektliste auf nicht-leere, aussagekräftige String-Einträge reduzieren."""
    if effects is None:
        return []
    if isinstance(effects, str):
        raise ActionGateError(
            "effects must be a sequence of strings, not a bare string",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )
    normalized: list[str] = []
    for item in effects:
        if not isinstance(item, str):
            raise ActionGateError(
                "each effect entry must be a string",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
        token = item.strip()
        if token and token.lower() not in {"none", "no", "false"}:
            normalized.append(token)
    return normalized


def _validate_visibility(visibility: str) -> str:
    if visibility not in _KNOWN_VISIBILITIES:
        raise ActionGateError(
            f"unknown visibility class: {visibility!r}",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )
    return visibility


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
    visibility: str = VISIBILITY_REDUCED,
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
    """
    if not isinstance(source_material, MaterialRef):
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
        if not isinstance(value, str):
            raise ActionGateError(
                f"{name} must be a string",
                [ActionReasonCode.ACTION_PROPOSAL_ONLY],
            )
    if not isinstance(network_required, bool):
        raise ActionGateError(
            "network_required must be a bool",
            [ActionReasonCode.ACTION_PROPOSAL_ONLY],
        )

    visibility = _validate_visibility(visibility)
    fs_effects = _normalize_effects(filesystem_effects)
    proc_effects = _normalize_effects(process_effects)
    source_trust = normalize_trust(source_material.trust)

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
    ecosystem_registries = known_registries.get(ecosystem.strip().lower(), frozenset())
    if registry_or_origin.strip().lower() in {r.lower() for r in ecosystem_registries}:
        reasons.append(ActionReasonCode.REGISTRY_KNOWN)
    else:
        hold(ActionReasonCode.REGISTRY_UNKNOWN)

    # Versions-Pin-Prüfung.
    if _is_pinned_version(requested_version):
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
    )
