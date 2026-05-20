# Save-State Cards

Status: lightweight templates and verifier only.

This folder stores small JSON templates for re-entry and inner-gate work. They are intentionally separate from immutable receipts and from `data/receipts/`.

## Verify

```bash
python3 tools/verify_cards.py cards/templates
```

Expected signal:

```text
VERIFY CARDS: PASS (6 cards)
```

## Card types

- `ack_triade`
- `nectar_attune`
- `rubedo_stop`
- `synthosia_scope`
- `reentry_vector`
- `ruecknahme_exit`

## Rücknahme invariant

For `ruecknahme_exit`, `fields.no_trace` must be `true`. This means the release state is successful without post-exit telemetry or persistent binding.

## Boundary

Cards are working artifacts. They are not evidence receipts, not clinical records, and not implementation approval for Synthosia/XR.
