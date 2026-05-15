#!/usr/bin/env python3
"""EntaENGELment Frame Lint v0.1.1.

Checks operative_frame declarations for claims/receipts using
policies/frame_taxonomy_v0_1_1.yml.

v0.1.1 scope:
- tag-based frame requirement only for INFERENZ / HYPOTHESE
- alias normalization (e.g. MET -> MYTH_ARCHETYPE)
- declaration validation with item-level short-circuit
- allowed/forbidden canonical claim tag checks
- optional trigger-term INFO/WARN when item.text is available
- CUSTOM fail/warn field checks

This tool intentionally does not infer frame requirements from prose body,
context-boundary crossing, or release/evidence roles. See
VOID-FRAME-CONTENT-PARSE-001.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as e:  # pragma: no cover
    raise SystemExit("PyYAML is needed. Install with: pip install pyyaml") from e

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY = REPO_ROOT / "policies" / "frame_taxonomy_v0_1_1.yml"
TriggerIndex = dict[str, list[tuple[str, str]]]


@dataclass
class Finding:
    severity: str
    rule_id: str
    reason_code: str
    message: str
    claim_id: str | None = None
    receipt_id: str | None = None
    frame_id: str | None = None
    canonical_frame_id: str | None = None


@dataclass
class LintResult:
    claim_id: str | None = None
    receipt_id: str | None = None
    frame_id: str | None = None
    canonical_frame_id: str | None = None
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, rule_id: str, reason_code: str, message: str) -> None:
        self.findings.append(
            Finding(
                severity=severity,
                rule_id=rule_id,
                reason_code=reason_code,
                message=message,
                claim_id=self.claim_id,
                receipt_id=self.receipt_id,
                frame_id=self.frame_id,
                canonical_frame_id=self.canonical_frame_id,
            )
        )

    def fail(self, rule_id: str, reason_code: str, message: str) -> None:
        self.add("FAIL", rule_id, reason_code, message)

    def warn(self, rule_id: str, reason_code: str, message: str) -> None:
        self.add("WARN", rule_id, reason_code, message)

    def info(self, rule_id: str, reason_code: str, message: str) -> None:
        self.add("INFO", rule_id, reason_code, message)

    @property
    def failed(self) -> bool:
        return any(f.severity == "FAIL" for f in self.findings)


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def canonical_tag_map(taxonomy: dict[str, Any]) -> dict[str, str]:
    config = taxonomy.get("normalization", {}).get("claim_tag_normalization", {})
    tags = config.get("canonical_tags", {})
    mapping: dict[str, str] = {}
    for canonical, data in tags.items():
        mapping[str(canonical).upper()] = str(canonical)
        for alias in data.get("aliases", []) or []:
            mapping[str(alias).upper()] = str(canonical)
    return mapping


def normalize_claim_tag(tag: str | None, taxonomy: dict[str, Any]) -> str | None:
    if tag is None:
        return None
    return canonical_tag_map(taxonomy).get(str(tag).upper(), str(tag))


def resolve_alias(frame_id: str | None, taxonomy: dict[str, Any]) -> str | None:
    if frame_id is None:
        return None
    aliases = (
        taxonomy.get("normalization", {}).get("alias_resolution", {}).get("aliases", {})
    )
    return aliases.get(frame_id, frame_id)


def required_tags(taxonomy: dict[str, Any]) -> set[str]:
    policy = taxonomy.get("implementation_contract", {}).get(
        "requires_frame_policy", {}
    )
    return {str(tag) for tag in policy.get("required_canonical_tags", []) or []}


def build_trigger_index(taxonomy: dict[str, Any]) -> TriggerIndex:
    """Invert frames[*].trigger_terms once per run.

    The returned mapping is lower-case trigger term -> [(frame_id, original_term)].
    This keeps lint_item deterministic while avoiding repeated O(frames * terms)
    scans for every claim in repository-wide runs.
    """
    index: TriggerIndex = {}
    for frame_id, frame_spec in (taxonomy.get("frames", {}) or {}).items():
        for term in frame_spec.get("trigger_terms", []) or []:
            normalized = str(term).lower()
            index.setdefault(normalized, []).append((str(frame_id), str(term)))
    return index


def _item_get(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in item:
            return item[key]
    return None


def check_custom_required_fields(
    frame: dict[str, Any], taxonomy: dict[str, Any], result: LintResult
) -> bool:
    policy = taxonomy.get("custom_frame_policy", {})
    ok = True
    for field_name in policy.get("fail_required_fields", []) or []:
        if not frame.get(field_name):
            result.fail(
                "LINT_FRAME_DECL_01",
                "RC_G6_FRAME_CUSTOM_001",
                f"CUSTOM frame missing field: {field_name}",
            )
            ok = False
    for field_name in policy.get("warn_required_fields", []) or []:
        if not frame.get(field_name):
            result.warn(
                "LINT_FRAME_CONTENT_01",
                "RC_G6_FRAME_CUSTOM_WARN_001",
                f"CUSTOM frame missing recommended field: {field_name}",
            )
    return ok


def check_allowed_claim_tag(
    tag: str | None, frame_spec: dict[str, Any], result: LintResult
) -> None:
    if tag is None:
        return
    perms = frame_spec.get("epistemic_permissions", {})
    allowed = set(perms.get("allowed_claim_tags", []) or [])
    forbidden = set(perms.get("forbidden_claim_tags", []) or [])
    # Forbidden tags are handled by check_forbidden_claim_tag so the result is not duplicated.
    if tag in forbidden:
        return
    if allowed and tag not in allowed:
        result.fail(
            "LINT_FRAME_CONTENT_01",
            "RC_G4_FRAME_CONTENT_001",
            f"Claim tag {tag!r} is not allowed for frame {result.canonical_frame_id!r}",
        )


def check_forbidden_claim_tag(
    tag: str | None, frame_spec: dict[str, Any], result: LintResult
) -> None:
    if tag is None:
        return
    perms = frame_spec.get("epistemic_permissions", {})
    forbidden = set(perms.get("forbidden_claim_tags", []) or [])
    if tag in forbidden:
        reason_code = "RC_G4_FRAME_CONTENT_001"
        if result.canonical_frame_id == "MYTH_ARCHETYPE" and tag == "FAKT":
            reason_code = "RC_G8_MYTH_EVIDENCE_001"
        result.fail(
            "LINT_FRAME_CONTENT_01",
            reason_code,
            f"Claim tag {tag!r} is forbidden for frame {result.canonical_frame_id!r}",
        )


def check_counterfactual_warn(
    tag: str | None, frame: dict[str, Any], result: LintResult
) -> None:
    if tag == "HYPOTHESE" and not frame.get("counterfactual_frame"):
        result.warn(
            "LINT_FRAME_CONTENT_01",
            "RC_G4_FRAME_WARN_001",
            "HYPOTHESE frame declaration should include counterfactual_frame",
        )


def check_trigger_terms(
    item: dict[str, Any],
    taxonomy: dict[str, Any],
    result: LintResult,
    trigger_index: TriggerIndex,
) -> None:
    text = str(item.get("text") or "")
    if not text:
        return
    text_lower = text.lower()
    active_frame = result.canonical_frame_id
    frame = item.get("operative_frame") or {}
    counterfactual_frame = resolve_alias(frame.get("counterfactual_frame"), taxonomy)

    for normalized_term, frame_matches in trigger_index.items():
        if normalized_term not in text_lower:
            continue
        for frame_id, original_term in frame_matches:
            if frame_id == active_frame:
                continue
            if counterfactual_frame == frame_id:
                result.info(
                    "LINT_FRAME_CONTENT_01",
                    "RC_G4_FRAME_TRIGGER_INFO_001",
                    f"Trigger term {original_term!r} suggests frame {frame_id!r}; "
                    "counterfactual_frame declares it",
                )
            else:
                result.warn(
                    "LINT_FRAME_CONTENT_01",
                    "RC_G4_FRAME_TRIGGER_WARN_001",
                    f"Trigger term {original_term!r} suggests frame {frame_id!r}; "
                    f"active frame is {active_frame!r}",
                )
            return


def lint_item(
    item: dict[str, Any],
    taxonomy: dict[str, Any],
    trigger_index: TriggerIndex | None = None,
) -> LintResult:
    if trigger_index is None:
        trigger_index = build_trigger_index(taxonomy)

    claim_id = _item_get(item, "claim_id", "id")
    receipt_id = _item_get(item, "receipt_id")
    result = LintResult(claim_id=claim_id, receipt_id=receipt_id)

    tag = normalize_claim_tag(_item_get(item, "claim_tag", "tag"), taxonomy)
    frame = item.get("operative_frame")
    frame_required = tag in required_tags(taxonomy)
    decl_ok = True

    if frame_required and not frame:
        result.fail(
            "LINT_FRAME_DECL_01",
            "RC_G6_FRAME_001",
            f"Claim tag {tag!r} needs operative_frame",
        )
        decl_ok = False

    if frame:
        original_frame_id = frame.get("frame_id")
        canonical_frame_id = resolve_alias(original_frame_id, taxonomy)
        result.frame_id = original_frame_id
        result.canonical_frame_id = canonical_frame_id

        if canonical_frame_id != original_frame_id:
            result.info(
                "FRAME_ALIAS_NORMALIZED",
                "RC_G6_FRAME_ALIAS_001",
                f"Frame alias {original_frame_id!r} normalized to {canonical_frame_id!r}",
            )

        frames = taxonomy.get("frames", {}) or {}
        if canonical_frame_id not in frames and canonical_frame_id != "CUSTOM":
            result.fail(
                "LINT_FRAME_DECL_01",
                "RC_G6_FRAME_002",
                f"Unknown frame_id: {original_frame_id!r}",
            )
            decl_ok = False

        if canonical_frame_id == "CUSTOM":
            decl_ok = check_custom_required_fields(frame, taxonomy, result) and decl_ok

    if not decl_ok:
        return result

    if frame:
        frames = taxonomy.get("frames", {}) or {}
        frame_spec = frames.get(result.canonical_frame_id, frames.get("CUSTOM", {}))
        check_allowed_claim_tag(tag, frame_spec, result)
        check_forbidden_claim_tag(tag, frame_spec, result)
        check_counterfactual_warn(tag, frame, result)
        if item.get("text"):
            check_trigger_terms(item, taxonomy, result, trigger_index)

    return result


def extract_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("claims"), list):
            receipt_id = data.get("receipt_id") or data.get("id")
            items = []
            for claim in data["claims"]:
                if isinstance(claim, dict):
                    item = dict(claim)
                    item.setdefault("receipt_id", receipt_id)
                    if "operative_frame" not in item and "operative_frame" in data:
                        item["operative_frame"] = data["operative_frame"]
                    items.append(item)
            return items
        return [data]
    return []


def lint_path(
    path: Path, taxonomy: dict[str, Any], trigger_index: TriggerIndex
) -> list[LintResult]:
    data = load_yaml(path)
    return [lint_item(item, taxonomy, trigger_index) for item in extract_items(data)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint operative_frame declarations")
    parser.add_argument("paths", nargs="+", help="YAML claim/receipt files to lint")
    parser.add_argument(
        "--taxonomy", default=str(DEFAULT_TAXONOMY), help="Frame taxonomy YAML"
    )
    args = parser.parse_args()

    taxonomy = load_yaml(Path(args.taxonomy))
    trigger_index = build_trigger_index(taxonomy)
    results: list[LintResult] = []
    for raw_path in args.paths:
        results.extend(lint_path(Path(raw_path), taxonomy, trigger_index))

    has_fail = False
    for result in results:
        for finding in result.findings:
            print(
                f"{finding.severity} {finding.rule_id} {finding.reason_code} "
                f"claim={finding.claim_id} receipt={finding.receipt_id} "
                f"frame={finding.frame_id}->{finding.canonical_frame_id}: {finding.message}"
            )
            has_fail = has_fail or finding.severity == "FAIL"

    if not results:
        print("FRAME LINT: no lintable items")
    elif has_fail:
        print("FRAME LINT: FAIL")
    else:
        print("FRAME LINT: PASS")
    return 1 if has_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
