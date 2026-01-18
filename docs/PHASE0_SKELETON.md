# EntaENGELment — Phase 0 Skeleton (P0)

Enthält:
- Deterministic Ledger/Receipts (event/deterministic split)
- JSON Schema für Receipts
- Tensor Mapping Skeleton + Validator
- Ethics/Privacy Templates
- Pytest-Suite (grün)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pytest -q
```

## Struktur
- `ledger/` deterministische Receipts
- `mapping/` TENSOR_MAPPING + Validator
- `docs/` Ethics/Privacy/Architecture
- `tests/` Tests
