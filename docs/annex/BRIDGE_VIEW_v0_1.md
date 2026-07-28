# BRIDGE_VIEW v0.1

Status: **DRAFT — read-only projection, no authority**

`BRIDGE_VIEW_v0.1` is a human-readable projection of an existing
`BridgeTranslation`. It does not create bridge records, retag claims, emit
events, read files, access the network, execute runtime actions, authorize a
promotion, or change any status.

## Fields

| Field | Existing source |
|---|---|
| `source` | `translation.material.material_id` |
| `target` | `translation.relation.claim_id` |
| `relation` | `translation.relation.relation_type` |
| `register` | `translation.context.source_register` |
| `status` | matching material/relation status |
| `known_loss` | `translation.context.known_loss` |
| `review_pointer` | `translation.context.m5_review_pointer` |
| `promotion_eligibility` | structural display only |
| `rollback` | `translation.context.rollback` |
| `receipt` | explicit repo-relative pointer supplied by the caller |

`ELIGIBLE_FOR_HUMAN_REVIEW` means only that the existing translation has a
promotion-capable relation, reviewed material trust, and the required M5
pointer. It does not mean approved, authorized, promoted, canonical, or true.

## Fail-closed invariants

- No view is emitted when `known_loss` is absent or malformed. A failed
  projection is never represented as complete.
- Source and target IDs must be canonical kebab-case IDs.
- Relations and registers must be members of their existing closed
  vocabularies; no relation is guessed or silently downgraded.
- Myth, metaphor, psychology, and UI cannot produce promotion eligibility.
- Physical and biological projections require the documented review pointer.
  A missing pointer is an error, not a downgrade.
- Material and relation status must agree.
- Receipt and review pointers must be explicit repo-relative paths. Receipt
  targets are limited to supported text files under `receipts/`.
- The projection never adds authority. Promotion remains a separate human
  decision behind existing governance gates.

Existence of the VOID-027 receipt target is checked by
`tools/verify_pointers.py` through its `VOIDMAP.yml` evidence entry. The pure
projection validates pointer shape only so it keeps the no-file-access
boundary.

## Rollback

Revert the introducing commit. Remove the corresponding `VOIDMAP.yml` evidence
pointer in the same revert. Preserve the Git history and receipt as historical
evidence of the withdrawn projection.
