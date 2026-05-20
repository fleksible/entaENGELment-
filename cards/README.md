# Save-State Cards

Status: lightweight templates and verifier only.

This folder stores small JSON templates for re-entry and inner-gate work. They are intentionally separate from immutable receipts and from `data/receipts/`.

## Verify

```bash
python3 tools/verify_cards.py cards/templates
```

Expected signal:

```text
VERIFY CARDS: PASS (5 cards)
```

## Boundary

Cards are working artifacts. They are not evidence receipts, not clinical records, and not implementation approval for Synthosia/XR.
