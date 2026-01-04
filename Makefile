PY ?= python3
OUT ?= out
RECEIPT ?= receipts/arc_sample.json
SNAPSHOT_INPUTS ?= "seeds/*.yaml" "audit/*.yaml"
STATUS ?= PASS
H ?= 0.84
DMI ?= 4.7
PHI ?= 0.72
REFRACTORY ?= 120

.PHONY: help install install-dev test test-unit test-integration test-ethics coverage lint format type-check clean gate-test verify verify-pointers claim-lint verify-json status status-verify snapshot all deepjump

help:
	@echo "entaENGELment Framework - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install         Install package"
	@echo "  make install-dev     Install package with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests"
	@echo "  make test-unit       Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-ethics     Run ethics/fail-safe tests only"
	@echo "  make coverage        Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            Run linting (ruff)"
	@echo "  make format          Format code (black)"
	@echo "  make type-check      Run type checking (mypy)"
	@echo ""
	@echo "Gate Policy:"
	@echo "  make gate-test       Test gate toggle functionality"
	@echo ""
	@echo "DeepJump Protocol v1.2:"
	@echo "  make verify          Phase 1: Verify pointers, claims, and tests"
	@echo "  make verify-pointers Check for dead pointers in index/modules"
	@echo "  make claim-lint      Detect untagged claims in core artefacts"
	@echo "  make status          Phase 2: Emit HMAC status (use status_emit.py for receipts)"
	@echo "  make snapshot        Phase 3: Generate snapshot manifest"
	@echo "  make all             Full DeepJump flow (verify + test + snapshot)"
	@echo "  make deepjump        Alias for 'make all'"
	@echo ""
	@echo "Legacy DeepJump:"
	@echo "  make verify-json     Verify JSON receipts"
	@echo "  make status-verify   Emit and verify status"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove build artifacts and cache"

# === Setup ===
install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

# === Testing ===
test:
	pytest -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-ethics:
	pytest tests/ethics/ -v

coverage:
	pytest --cov --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

# === Code Quality ===
lint:
	ruff check src/ tools/ tests/

format:
	black src/ tools/ tests/

type-check:
	mypy src/ tools/

# === Gate Policy ===
gate-test:
	@echo "Testing gate with valid context (should open):"
	python tools/mzm/gate_toggle.py 0.9 true true 1.0 true
	@echo ""
	@echo "Testing gate with low phi (should close):"
	python tools/mzm/gate_toggle.py 0.5 true true 1.0 true
	@echo ""
	@echo "Testing gate without consent (should close):"
	python tools/mzm/gate_toggle.py 0.9 false true 1.0 true

# === DeepJump Protocol v1.2 ===

# Phase 1: VERIFY (vor jedem Arbeitsschritt)
verify: verify-pointers claim-lint
	@echo ""
	@echo "=== VERIFY COMPLETE ==="
	@echo "✅ Pointers checked"
	@echo "✅ Claims linted"
	@echo ""

verify-pointers:
	@echo "=== VERIFY POINTERS ==="
	@$(PY) tools/verify_pointers.py --strict

claim-lint:
	@echo "=== CLAIM LINT ==="
	@$(PY) tools/claim_lint.py --scope index,spec,receipts,tools

# Phase 2: STATUS (HMAC Receipt)
status:
	@mkdir -p $(OUT)
	@$(PY) tools/status_emit.py \
		--outdir $(OUT) \
		--status $(STATUS) \
		--H $(H) \
		--dmi $(DMI) \
		--phi $(PHI) \
		--refractory $(REFRACTORY)

status-verify: status
	@$(PY) tools/status_verify.py $(OUT)/status/deepjump_status.json

# Phase 3: SNAPSHOT (strict)
snapshot:
	@echo "=== SNAPSHOT ==="
	@mkdir -p $(OUT)
	@$(PY) tools/snapshot_guard.py $(OUT)/snapshot_manifest.json $(SNAPSHOT_INPUTS) --strict

# Full DeepJump flow
all: verify test snapshot
	@echo ""
	@echo "✅ All DeepJump checks passed. Ready to commit."

deepjump: all

# Legacy: Verify JSON receipts
verify-json:
	@mkdir -p $(OUT)
	@$(PY) tests/verify_deep_jump.py --receipt $(RECEIPT) --json > $(OUT)/verify.json

# === Cleanup ===
clean:
	rm -rf $(OUT)
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
