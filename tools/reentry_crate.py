#!/usr/bin/env python3
"""tesser3TAKT Save State als RO-Crate 1.2 (Re-Entry-Paket).

[MODEL] Ein Save State ist ein Ordner mit ``ro-crate-metadata.json`` (RO-Crate 1.2,
JSON-LD/schema.org), einer lesbaren Wiedereinstiegs-Kurzfassung ``REENTRY.md``, dem
normalisierten Zustand ``savestate.json``, einer ``reentry_vector``-Karte (Format von
``tools/verify_cards.py``) und den kopierten Quellen unter ``payload/``. ``SEAL.json``
hält SHA-256 je Datei plus HMAC-Signatur (``ENTA_HMAC_SECRET``) oder ``UNSIGNED``.

[MODEL] Felder wie ``authority``, ``promotion_status``, ``known_losses``,
``next_allowed_action``, ``frozen_state`` und ``floating_problem`` übernehmen das
bestehende Save-State-/Receipt-Vokabular des Projekts.

[RISK] Save States tragen oft private Bedeutung. Standardziel ist ``out/reentry/``
(gitignored). Ein Ziel, das git committen könnte, verlangt ``--publish``
(PRIVACY_BOUNDARY.md: GitHub erhält private Bedeutung nicht per Default).

[RISK] UNSIGNED-Siegel sichern nur Integrität (Hash-Abgleich), keine Herkunft.

Usage:
    python tools/reentry_crate.py save --manifest savestate.yaml [--out out/reentry]
    python tools/reentry_crate.py verify --crate out/reentry/<id> [--require-signed]
    python tools/reentry_crate.py brief --crate out/reentry/<id>
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from tools.status_emit import compute_state_fingerprint, sign_payload
    from tools.verify_cards import validate_card
except ModuleNotFoundError:  # Standalone-Aufruf ohne editable Install
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from tools.status_emit import compute_state_fingerprint, sign_payload
    from tools.verify_cards import validate_card

SCHEMA_VERSION = "tesser3takt-savestate.v0.1"
TOOL_VERSION = "0.1.0"
RO_CRATE_CONTEXT = "https://w3id.org/ro/crate/1.2/context"
RO_CRATE_PROFILE = "https://w3id.org/ro/crate/1.2"

METADATA_FILE = "ro-crate-metadata.json"
SEAL_FILE = "SEAL.json"
BRIEF_FILE = "REENTRY.md"
STATE_FILE = "savestate.json"
CARD_FILE = "payload/cards/reentry_vector.json"
DEFAULT_OUT = Path("out") / "reentry"

# Claim-Arten: Projekt-Tags (claim_lint/EPISTEMIC_HYGIENE) plus Save-State-/Receipt-Vokabular.
CLAIM_TAGS = frozenset(
    {
        "FACT",
        "HYP",
        "MET",
        "TODO",
        "RISK",
        "MODEL",
        "HYPOTHESIS",
        "METAPHOR",
        "FAKT",
        "BEOBACHTUNG",
        "REKONSTRUKTION",
        "INFERENZ",
        "MODELL",
        "HYPOTHESE",
        "METAPHER",
        "GUARD",
        "VOID",
        "CLAIM",
        "POESIE",
        "SPEC",
        "KORPUSBEFUND",
        "EXTRAPOLATION",
    }
)
STATUSES = frozenset({"DERIVED", "REVIEW-PENDING", "HOLD", "UNRESOLVED", "VERIFIED", "RETRACTED"})
PROMOTION_STATUSES = frozenset({"NO_CANON_PROMOTION", "REVIEW_REQUESTED"})
SOURCE_ROLES = frozenset({"input", "context", "output"})
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
PRIVATE_LICENSE_ID = "#private-by-default"
MANIFEST_KEYS = frozenset(
    {
        "id",
        "title",
        "summary",
        "focus",
        "authority",
        "promotion_status",
        "current_status",
        "floating_problem",
        "next_allowed_action",
        "agent",
        "license",
        "frozen_state",
        "open_points",
        "negative_findings",
        "known_losses",
        "notes",
        "sources",
        "claims",
        "next_actions",
        "lineage",
    }
)


class ManifestError(ValueError):
    """Manifest ist unvollständig oder widersprüchlich."""


@dataclass
class VerifyResult:
    verdict: str
    authenticity: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "authenticity": self.authenticity,
            "errors": self.errors,
            "warnings": self.warnings,
        }


# --- Hilfsfunktionen -----------------------------------------------------------------


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60].strip("-") or "savestate"


def _git(args: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def git_info(cwd: Path) -> dict[str, Any]:
    commit = _git(["rev-parse", "HEAD"], cwd) or "unknown"
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], cwd) or "unknown"
    status = _git(["status", "--porcelain"], cwd)
    return {"commit": commit, "branch": branch, "dirty": bool(status)}


def committable_by_git(path: Path) -> bool:
    """True, wenn ``path`` in einem git-Arbeitsbaum liegt und nicht ignoriert wird."""
    probe = path
    while not probe.exists():
        probe = probe.parent
    top = _git(["rev-parse", "--show-toplevel"], probe if probe.is_dir() else probe.parent)
    if top is None:
        return False
    result = subprocess.run(
        ["git", "check-ignore", "-q", str(path.resolve())],
        cwd=top,
        capture_output=True,
        check=False,
    )
    return result.returncode == 1


def _str_list(data: dict[str, Any], key: str, errors: list[str]) -> list[str]:
    value = data.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        errors.append(f"{key}: Liste nicht-leerer Strings erwartet")
        return []
    return [v.strip() for v in value]


def _opt_str(data: dict[str, Any], key: str, errors: list[str]) -> str:
    value = data.get(key, "")
    if value is None:
        return ""
    if not isinstance(value, str):
        errors.append(f"{key}: String erwartet")
        return ""
    return value.strip()


# --- Manifest ------------------------------------------------------------------------


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ManifestError(f"Manifest nicht lesbar: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError("Manifest muss ein Mapping sein")
    return data


def normalize_manifest(data: dict[str, Any]) -> dict[str, Any]:
    """Prüft das Manifest und gibt eine normalisierte Kopie zurück (fail-closed)."""
    errors: list[str] = []
    out: dict[str, Any] = {}

    unknown = sorted(set(data) - MANIFEST_KEYS)
    if unknown:
        errors.append(f"unbekannte Felder: {', '.join(unknown)}")

    for key in ("title", "summary", "focus"):
        value = _opt_str(data, key, errors)
        if not value:
            errors.append(f"{key}: Pflichtfeld fehlt")
        out[key] = value

    state_id = _opt_str(data, "id", errors) or ""
    if state_id and not ID_RE.match(state_id):
        errors.append(f"id: nur [A-Za-z0-9_.-] erlaubt, erhalten {state_id!r}")
    out["id"] = state_id

    authority = _opt_str(data, "authority", errors) or "REVIEW-PENDING"
    if authority not in STATUSES:
        errors.append(f"authority: {authority!r} nicht in {sorted(STATUSES)}")
    out["authority"] = authority

    promotion = _opt_str(data, "promotion_status", errors) or "NO_CANON_PROMOTION"
    if promotion not in PROMOTION_STATUSES:
        errors.append(f"promotion_status: {promotion!r} nicht in {sorted(PROMOTION_STATUSES)}")
    out["promotion_status"] = promotion

    for key in ("current_status", "floating_problem", "next_allowed_action", "agent"):
        out[key] = _opt_str(data, key, errors)
    out["license"] = _opt_str(data, "license", errors) or "private"

    for key in ("frozen_state", "open_points", "negative_findings", "known_losses", "notes"):
        out[key] = _str_list(data, key, errors)

    sources: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(data.get("sources") or []):
        where = f"sources[{index}]"
        if not isinstance(raw, dict):
            errors.append(f"{where}: Mapping erwartet")
            continue
        src_id = str(raw.get("id", "")).strip()
        if not ID_RE.match(src_id):
            errors.append(f"{where}.id: fehlt oder ungültig")
        elif src_id in seen:
            errors.append(f"{where}.id: doppelt ({src_id})")
        seen.add(src_id)
        has_path, has_uri = bool(raw.get("path")), bool(raw.get("uri"))
        if has_path == has_uri:
            errors.append(f"{where}: genau eines von path/uri angeben")
        role = str(raw.get("role", "input"))
        if role not in SOURCE_ROLES:
            errors.append(f"{where}.role: {role!r} nicht in {sorted(SOURCE_ROLES)}")
        sha = str(raw.get("sha256", "")).lower()
        if sha and not re.fullmatch(r"[0-9a-f]{64}", sha):
            errors.append(f"{where}.sha256: 64 Hex-Zeichen erwartet")
        sources.append(
            {
                "id": src_id,
                "path": str(raw.get("path", "")),
                "uri": str(raw.get("uri", "")),
                "role": role,
                "title": str(raw.get("title", "")),
                "sha256": sha,
            }
        )
    out["sources"] = sources

    claims: list[dict[str, Any]] = []
    for index, raw in enumerate(data.get("claims") or []):
        where = f"claims[{index}]"
        if not isinstance(raw, dict) or not str(raw.get("text", "")).strip():
            errors.append(f"{where}: Mapping mit text erwartet")
            continue
        tag = str(raw.get("tag", "")).strip().strip("[]").upper()
        if tag not in CLAIM_TAGS:
            errors.append(f"{where}.tag: {tag!r} nicht im Vokabular")
        status = str(raw.get("status", "") or "").strip().upper()
        if status and status not in STATUSES:
            errors.append(f"{where}.status: {status!r} nicht in {sorted(STATUSES)}")
        refs = raw.get("sources") or []
        if not isinstance(refs, list):
            errors.append(f"{where}.sources: Liste erwartet")
            refs = []
        for ref in refs:
            if ref not in seen:
                errors.append(f"{where}.sources: unbekannte Quelle {ref!r}")
        claims.append(
            {
                "text": str(raw["text"]).strip(),
                "tag": tag,
                "status": status,
                "sources": [str(r) for r in refs],
            }
        )
    out["claims"] = claims

    actions: list[dict[str, Any]] = []
    for index, raw in enumerate(data.get("next_actions") or []):
        if isinstance(raw, str):
            raw = {"id": f"N{index + 1}", "title": raw}
        if not isinstance(raw, dict) or not str(raw.get("title", "")).strip():
            errors.append(f"next_actions[{index}]: title fehlt")
            continue
        paths = raw.get("paths") or []
        actions.append(
            {
                "id": str(raw.get("id") or f"N{index + 1}"),
                "title": str(raw["title"]).strip(),
                "paths": [str(p) for p in paths] if isinstance(paths, list) else [],
            }
        )
    out["next_actions"] = actions

    lineage = data.get("lineage") or {}
    if lineage:
        nodes = lineage.get("nodes") if isinstance(lineage, dict) else None
        edges = lineage.get("edges") if isinstance(lineage, dict) else None
        if not isinstance(nodes, list) or not isinstance(edges, list):
            errors.append("lineage: nodes und edges als Listen erwartet")
            lineage = {}
        else:
            node_ids = {str(n.get("id")) for n in nodes if isinstance(n, dict)}
            for edge in edges:
                if (
                    not isinstance(edge, dict)
                    or not {
                        str(edge.get("source")),
                        str(edge.get("target")),
                    }
                    <= node_ids
                ):
                    errors.append(f"lineage: Kante verweist auf unbekannten Knoten: {edge}")
    out["lineage"] = lineage

    if errors:
        raise ManifestError("; ".join(errors))
    return out


def claim_audit(claims: list[dict[str, Any]]) -> dict[str, Any]:
    by_tag: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for claim in claims:
        by_tag[claim["tag"]] = by_tag.get(claim["tag"], 0) + 1
        status = claim["status"] or "UNSET"
        by_status[status] = by_status.get(status, 0) + 1
    return {
        "total": len(claims),
        "by_tag": dict(sorted(by_tag.items())),
        "by_status": dict(sorted(by_status.items())),
    }


# --- Save ----------------------------------------------------------------------------


def _payload_target(src: Path, repo_root: Path | None, prefix: str) -> str:
    resolved = src.resolve()
    if repo_root is not None:
        try:
            return f"{prefix}/{resolved.relative_to(repo_root).as_posix()}"
        except ValueError:
            pass
    return f"{prefix}/external/{resolved.name}"


def _iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        p
        for p in path.rglob("*")
        if p.is_file() and not any(part.startswith(".") for part in p.relative_to(path).parts)
    )


def _md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render_brief(state: dict[str, Any], crate_rel: str) -> str:
    git = state["git"]
    dirty = " (dirty)" if git["dirty"] else ""
    lines = [
        f"# Re-Entry: {state['title']}",
        "",
        f"> Save State `{state['id']}` · erstellt {state['created_at']} · "
        f"Commit `{git['commit'][:12]}`{dirty} · Branch `{git['branch']}`",
        f"> Authority: **{state['authority']}** · Promotion: **{state['promotion_status']}** "
        f"· FOKUS: {state['focus']}",
        "",
        "**Vor dem Weiterarbeiten:** "
        f"`python3 tools/reentry_crate.py verify --crate {crate_rel}` muss PASS melden. "
        "Rückführung in dauerhaften Zustand nur mit explizitem OK (Re-Entry-Schwelle).",
        "",
        "## Stand",
        "",
    ]
    if state["current_status"]:
        lines += [f"**Status:** {state['current_status']}", ""]
    lines += [state["summary"], ""]

    def bullets(title: str, items: list[str]) -> None:
        if items:
            lines.extend([f"## {title}", ""])
            lines.extend(f"- {item}" for item in items)
            lines.append("")

    bullets("Eingefroren (frozen state)", state["frozen_state"])
    if state["floating_problem"]:
        lines += ["## Schwebendes Problem", "", state["floating_problem"], ""]

    if state["claims"]:
        audit = state["claim_audit"]
        tags = " · ".join(f"{k} {v}" for k, v in audit["by_tag"].items())
        lines += [
            "## Aussagen",
            "",
            f"Claim-Audit: {audit['total']} Aussagen — {tags}",
            "",
            "| # | Tag | Status | Aussage | Quellen |",
            "|---|-----|--------|---------|---------|",
        ]
        for number, claim in enumerate(state["claims"], start=1):
            lines.append(
                f"| {number} | {claim['tag']} | {claim['status'] or '–'} | "
                f"{_md_cell(claim['text'])} | {', '.join(claim['sources']) or '–'} |"
            )
        lines.append("")

    bullets("Offene Stellen (UNRESOLVED)", state["open_points"])
    bullets("Negativbefunde", state["negative_findings"])
    bullets("Bekannte Verluste", state["known_losses"])

    if state["next_actions"] or state["next_allowed_action"]:
        lines += ["## Nächste Schritte", ""]
        for action in state["next_actions"]:
            paths = f" (`{'`, `'.join(action['paths'])}`)" if action["paths"] else ""
            lines.append(f"- **{action['id']}** {action['title']}{paths}")
        if state["next_allowed_action"]:
            lines += ["", f"**Nächste erlaubte Aktion:** {state['next_allowed_action']}"]
        lines.append("")

    if state["sources"]:
        lines += [
            "## Quellen",
            "",
            "| ID | Rolle | Ort | SHA-256 |",
            "|----|-------|-----|---------|",
        ]
        for src in state["sources"]:
            where = src.get("payload") or src["uri"]
            sha = src["sha256"][:16] + "…" if src["sha256"] else "–"
            lines.append(f"| {src['id']} | {src['role']} | `{_md_cell(where)}` | `{sha}` |")
        lines.append("")

    lineage = state.get("lineage") or {}
    if lineage:
        lines += ["## Lineage", ""]
        for node in lineage["nodes"]:
            lines.append(
                f"- `{node.get('id')}` {node.get('label', '')} ({node.get('status', '–')})"
            )
        for edge in lineage["edges"]:
            lines.append(f"- `{edge['source']}` —{edge.get('relation', '')}→ `{edge['target']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _file_entity(crate: Path, rel: str, name: str) -> dict[str, Any]:
    path = crate / rel
    fmt = mimetypes.guess_type(path.name)[0]
    if path.suffix in {".md", ".markdown"}:
        fmt = "text/markdown"
    elif path.suffix in {".yaml", ".yml"}:
        fmt = "application/yaml"
    entity: dict[str, Any] = {
        "@id": rel,
        "@type": "File",
        "name": name,
        "contentSize": str(path.stat().st_size),
        "sha256": sha256_file(path),
    }
    if fmt:
        entity["encodingFormat"] = fmt
    return entity


def build_metadata(crate: Path, state: dict[str, Any]) -> dict[str, Any]:
    files: list[dict[str, Any]] = [
        _file_entity(crate, BRIEF_FILE, "Re-Entry-Kurzfassung"),
        _file_entity(crate, STATE_FILE, "Normalisierter Save State"),
        _file_entity(crate, CARD_FILE, "reentry_vector-Karte"),
    ]
    remote: list[dict[str, Any]] = []
    for src in state["sources"]:
        if src.get("payload"):
            files.append(_file_entity(crate, src["payload"], src["title"] or src["id"]))
        else:
            entity: dict[str, Any] = {
                "@id": src["uri"],
                "@type": "CreativeWork",
                "name": src["title"] or src["id"],
                "identifier": src["id"],
            }
            if src["sha256"]:
                entity["sha256"] = src["sha256"]
            remote.append(entity)
    for note in state["notes_payload"]:
        files.append(_file_entity(crate, note, "Notiz"))

    if state["license"] == "private":
        license_entity: dict[str, Any] = {
            "@id": PRIVATE_LICENSE_ID,
            "@type": "CreativeWork",
            "name": "Privat per Default",
            "description": "Nicht zur Weitergabe; siehe PRIVACY_BOUNDARY.md im Repository.",
        }
    else:
        is_uri = re.match(r"^https?://", state["license"]) is not None
        license_entity = {
            "@id": state["license"] if is_uri else f"#license-{_slugify(state['license'])}",
            "@type": "CreativeWork",
            "name": state["license"],
            "description": "Im Manifest angegebene Lizenz.",
        }

    claims = [
        {
            "@id": f"#claim-{number}",
            "@type": "Claim",
            "text": claim["text"],
            "keywords": claim["tag"],
            "creativeWorkStatus": claim["status"] or "UNSET",
            **(
                {"isBasedOn": [{"@id": _source_ref(state, ref)} for ref in claim["sources"]]}
                if claim["sources"]
                else {}
            ),
        }
        for number, claim in enumerate(state["claims"], start=1)
    ]

    tool = {
        "@id": "#reentry-crate-tool",
        "@type": "SoftwareApplication",
        "name": "tools/reentry_crate.py",
        "version": f"{TOOL_VERSION}+{state['git']['commit'][:12]}",
    }
    action: dict[str, Any] = {
        "@id": "#save-action",
        "@type": "CreateAction",
        "name": "tesser3TAKT Save State",
        "instrument": {"@id": tool["@id"]},
        "object": [{"@id": _source_ref(state, s["id"])} for s in state["sources"]],
        "result": [{"@id": BRIEF_FILE}, {"@id": STATE_FILE}, {"@id": CARD_FILE}],
        "endTime": state["created_at"],
        "actionStatus": {"@id": "http://schema.org/CompletedActionStatus"},
    }
    graph_extra: list[dict[str, Any]] = []
    if state["agent"]:
        action["agent"] = {"@id": "#agent"}
        graph_extra.append({"@id": "#agent", "@type": "Person", "name": state["agent"]})

    root: dict[str, Any] = {
        "@id": "./",
        "@type": "Dataset",
        "name": state["title"],
        "description": state["summary"],
        "datePublished": state["created_at"],
        "license": {"@id": license_entity["@id"]},
        "keywords": ["tesser3TAKT", "save-state", "re-entry", state["focus"]],
        "creativeWorkStatus": state["authority"],
        "hasPart": [{"@id": f["@id"]} for f in files],
        "mentions": [{"@id": c["@id"]} for c in claims],
    }
    if remote:
        root["isBasedOn"] = [{"@id": r["@id"]} for r in remote]

    descriptor = {
        "@id": METADATA_FILE,
        "@type": "CreativeWork",
        "conformsTo": {"@id": RO_CRATE_PROFILE},
        "about": {"@id": "./"},
    }
    graph = [descriptor, root, *files, *remote, *claims, action, tool, license_entity]
    return {"@context": RO_CRATE_CONTEXT, "@graph": graph + graph_extra}


def _source_ref(state: dict[str, Any], source_id: str) -> str:
    for src in state["sources"]:
        if src["id"] == source_id:
            return str(src.get("payload") or src["uri"])
    raise KeyError(source_id)


def resolve_secret() -> str:
    return os.environ.get("ENTA_HMAC_SECRET") or os.environ.get("CI_SECRET") or ""


def seal_crate(crate: Path, crate_id: str, commit: str, secret: str, now: str) -> dict[str, Any]:
    files = {
        p.relative_to(crate).as_posix(): sha256_file(p)
        for p in sorted(crate.rglob("*"))
        if p.is_file() and p.name != SEAL_FILE
    }
    seal: dict[str, Any] = {
        "seal_version": "1.0",
        "crate_id": crate_id,
        "sealed_at": now,
        "commit": commit,
        "hash_alg": "sha256",
        "canonicalization": "json_c14n_v1",
        "files": files,
    }
    seal["state_fingerprint"] = "0x" + compute_state_fingerprint(seal)
    if secret:
        seal["hmac_signature"] = "0x" + sign_payload(seal, secret)
    else:
        seal["hmac_signature"] = "UNSIGNED"
        seal["warning"] = "No ENTA_HMAC_SECRET set. Seal covers integrity only, not origin."
    (crate / SEAL_FILE).write_text(json.dumps(seal, indent=2) + "\n", encoding="utf-8")
    return seal


def save_state(
    manifest: dict[str, Any],
    out_root: Path,
    *,
    base: Path,
    secret: str,
    publish: bool = False,
    now: str | None = None,
) -> Path:
    """Erzeugt und versiegelt ein Re-Entry-Paket; gibt den Crate-Pfad zurück."""
    state = normalize_manifest(manifest)
    created_at = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    state["id"] = state["id"] or f"{created_at[:10]}_{_slugify(state['title'])}"
    crate: Path = (out_root / state["id"]).resolve()

    if crate.exists():
        raise ManifestError(f"{crate} existiert bereits; Save States werden nie überschrieben")
    if committable_by_git(crate) and not publish:
        raise ManifestError(
            f"{crate} wäre von git committbar. Save States sind privat per Default "
            "(PRIVACY_BOUNDARY.md). Ziel unter out/ wählen oder bewusst --publish setzen."
        )

    repo_top = _git(["rev-parse", "--show-toplevel"], base)
    repo_root = Path(repo_top).resolve() if repo_top else None

    copies: list[tuple[Path, str]] = []
    for src in state["sources"]:
        if not src["path"]:
            continue
        path = (base / src["path"]).resolve()
        if not path.is_file():
            raise ManifestError(f"Quelle {src['id']}: Datei nicht gefunden ({src['path']})")
        src["payload"] = _payload_target(path, repo_root, "payload")
        copies.append((path, src["payload"]))
    notes_payload: list[str] = []
    for note in state["notes"]:
        note_path = (base / note).resolve()
        if not note_path.exists():
            raise ManifestError(f"Notiz nicht gefunden: {note}")
        for file in _iter_files(note_path):
            root = note_path if note_path.is_dir() else note_path.parent
            target = f"payload/notes/{note_path.name if note_path.is_dir() else ''}"
            target = f"{target.rstrip('/')}/{file.relative_to(root).as_posix()}"
            notes_payload.append(target)
            copies.append((file, target))
    targets = [t for _, t in copies]
    if len(targets) != len(set(targets)):
        raise ManifestError("Zwei Quellen landen am selben Payload-Pfad; Dateinamen prüfen")

    crate.mkdir(parents=True)
    for source, target in copies:
        destination = crate / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    for src in state["sources"]:
        if src.get("payload"):
            src["sha256"] = sha256_file(crate / src["payload"])

    state.update(
        {
            "schema": SCHEMA_VERSION,
            "created_at": created_at,
            "git": git_info(base),
            "tool_version": TOOL_VERSION,
            "notes_payload": notes_payload,
            "claim_audit": claim_audit(state["claims"]),
            "input_hashes": {s["id"]: s["sha256"] for s in state["sources"] if s["sha256"]},
        }
    )
    card = {
        "card_type": "reentry_vector",
        "timestamp": created_at,
        "fields": {
            "status": state["current_status"] or state["authority"],
            "current_hold": state["floating_problem"]
            or (state["open_points"][0] if state["open_points"] else "–"),
            "next_action": state["next_allowed_action"]
            or (state["next_actions"][0]["title"] if state["next_actions"] else "–"),
            "source_doc": BRIEF_FILE,
        },
    }
    (crate / CARD_FILE).parent.mkdir(parents=True, exist_ok=True)
    (crate / CARD_FILE).write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    (crate / STATE_FILE).write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    crate_rel = os.path.relpath(crate, base)
    (crate / BRIEF_FILE).write_text(render_brief(state, crate_rel), encoding="utf-8")
    metadata = build_metadata(crate, state)
    (crate / METADATA_FILE).write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    seal_crate(crate, state["id"], state["git"]["commit"], secret, created_at)
    return crate


# --- Verify --------------------------------------------------------------------------


def _check_metadata(crate: Path, errors: list[str]) -> None:
    try:
        metadata = json.loads((crate / METADATA_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{METADATA_FILE}: nicht lesbar ({exc})")
        return
    if metadata.get("@context") != RO_CRATE_CONTEXT:
        errors.append(f"{METADATA_FILE}: @context ist nicht {RO_CRATE_CONTEXT}")
    graph = {e.get("@id"): e for e in metadata.get("@graph", []) if isinstance(e, dict)}
    descriptor = graph.get(METADATA_FILE, {})
    if descriptor.get("@type") != "CreativeWork" or descriptor.get("about") != {"@id": "./"}:
        errors.append("Metadata Descriptor fehlt oder zeigt nicht auf ./")
    if descriptor.get("conformsTo") != {"@id": RO_CRATE_PROFILE}:
        errors.append(f"Metadata Descriptor: conformsTo ist nicht {RO_CRATE_PROFILE}")
    root = graph.get("./", {})
    if root.get("@type") != "Dataset":
        errors.append("Root Data Entity ./ fehlt oder ist kein Dataset")
    for key in ("name", "description", "datePublished", "license"):
        if not root.get(key):
            errors.append(f"Root Data Entity: {key} fehlt")
    parts = {p.get("@id") for p in root.get("hasPart", []) if isinstance(p, dict)}
    for entity_id, entity in graph.items():
        if entity.get("@type") != "File":
            continue
        if entity_id not in parts:
            errors.append(f"{entity_id}: File nicht über hasPart erreichbar")
        path = crate / str(entity_id)
        if not path.is_file():
            errors.append(f"{entity_id}: im Crate nicht vorhanden")
            continue
        if entity.get("sha256") != sha256_file(path):
            errors.append(f"{entity_id}: SHA-256 weicht von Metadaten ab")
        if entity.get("contentSize") != str(path.stat().st_size):
            errors.append(f"{entity_id}: contentSize weicht ab")


def verify_crate(crate: Path, *, secret: str = "", require_signed: bool = False) -> VerifyResult:
    result = VerifyResult(verdict="HOLD", authenticity="UNKNOWN")
    if not crate.is_dir():
        result.errors.append(f"{crate}: kein Verzeichnis")
        return result
    _check_metadata(crate, result.errors)

    try:
        state = json.loads((crate / STATE_FILE).read_text(encoding="utf-8"))
        if state.get("schema") != SCHEMA_VERSION:
            result.errors.append(f"{STATE_FILE}: schema ist nicht {SCHEMA_VERSION}")
    except (OSError, json.JSONDecodeError) as exc:
        result.errors.append(f"{STATE_FILE}: nicht lesbar ({exc})")
    if (crate / CARD_FILE).is_file():
        result.errors.extend(validate_card(crate / CARD_FILE))
    else:
        result.errors.append(f"{CARD_FILE}: fehlt")

    try:
        seal = json.loads((crate / SEAL_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result.errors.append(f"{SEAL_FILE}: nicht lesbar ({exc})")
        return result
    sealed_files = seal.get("files") or {}
    present = {
        p.relative_to(crate).as_posix()
        for p in crate.rglob("*")
        if p.is_file() and p.name != SEAL_FILE
    }
    for rel in sorted(present - set(sealed_files)):
        result.errors.append(f"{rel}: nicht im Siegel (nachträglich hinzugefügt)")
    for rel in sorted(set(sealed_files) - present):
        result.errors.append(f"{rel}: im Siegel, aber fehlt")
    for rel in sorted(present & set(sealed_files)):
        if sha256_file(crate / rel) != sealed_files[rel]:
            result.errors.append(f"{rel}: SHA-256 weicht vom Siegel ab")

    signature = seal.get("hmac_signature", "")
    unsigned = {k: v for k, v in seal.items() if k not in ("hmac_signature", "warning")}
    fingerprint = {k: v for k, v in unsigned.items() if k != "state_fingerprint"}
    if unsigned.get("state_fingerprint") != "0x" + compute_state_fingerprint(fingerprint):
        result.errors.append(f"{SEAL_FILE}: state_fingerprint passt nicht zum Inhalt")
    if signature == "UNSIGNED":
        result.authenticity = "UNSIGNED"
        result.warnings.append("Siegel UNSIGNED: Integrität geprüft, Herkunft nicht.")
        if require_signed:
            result.errors.append("Signatur verlangt, Siegel ist UNSIGNED")
    elif not secret:
        result.authenticity = "SIGNED_UNCHECKED"
        result.warnings.append("Signiert, aber kein ENTA_HMAC_SECRET zum Prüfen gesetzt.")
        if require_signed:
            result.errors.append("Signatur verlangt, aber ohne Secret nicht prüfbar")
    elif hmac.compare_digest(str(signature), "0x" + sign_payload(unsigned, secret)):
        result.authenticity = "SIGNED_VALID"
    else:
        result.authenticity = "SIGNED_INVALID"
        result.errors.append(f"{SEAL_FILE}: HMAC-Signatur ungültig")

    result.verdict = "HOLD" if result.errors else "PASS"
    return result


# --- CLI -----------------------------------------------------------------------------


def _print_result(result: VerifyResult, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
        return
    print(f"REENTRY VERIFY: {result.verdict} (authenticity: {result.authenticity})")
    for error in result.errors:
        print(f"  [HOLD] {error}")
    for warning in result.warnings:
        print(f"  [WARN] {warning}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="tesser3TAKT Save State als RO-Crate 1.2")
    sub = parser.add_subparsers(dest="command", required=True)

    p_save = sub.add_parser("save", help="Save State aus Manifest erzeugen und versiegeln")
    p_save.add_argument("--manifest", required=True, type=Path)
    p_save.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p_save.add_argument("--base", type=Path, default=Path.cwd(), help="Basis relativer Pfade")
    p_save.add_argument(
        "--publish",
        action="store_true",
        help="Ziel darf git-committbar sein (nur nach Privacy-Prüfung)",
    )

    for name, text in (("verify", "Integrität/Signatur prüfen"), ("brief", "REENTRY.md")):
        p = sub.add_parser(name, help=text)
        p.add_argument("--crate", required=True, type=Path)
        p.add_argument("--require-signed", action="store_true")
        p.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    secret = resolve_secret()

    if args.command == "save":
        if os.environ.get("CI") and not secret:
            print("[ERROR] Unsigned save states are not permitted in CI.", file=sys.stderr)
            return 2
        try:
            crate = save_state(
                load_manifest(args.manifest),
                args.out,
                base=args.base.resolve(),
                secret=secret,
                publish=args.publish,
            )
        except ManifestError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 2
        result = verify_crate(crate, secret=secret)
        print(f"[SAVE] {crate}")
        _print_result(result, as_json=False)
        return 0 if result.verdict == "PASS" else 1

    result = verify_crate(args.crate, secret=secret, require_signed=args.require_signed)
    if args.command == "verify" or result.verdict != "PASS":
        _print_result(result, args.json)
        return 0 if result.verdict == "PASS" else 1
    print((args.crate / BRIEF_FILE).read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
