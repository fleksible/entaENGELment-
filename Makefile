PY ?= python3
OUT ?= out
RECEIPT ?= receipts/arc_sample.json
SNAPSHOT_INPUTS ?= "seeds/*.yaml" "audit/*.yaml"
STATUS ?= PASS
H ?= 0.84
DMI ?= 4.7
PHI ?= 0.72
REFRACTORY ?= 120
JS_VERIFY_CMD ?= pnpm turbo run typecheck lint build

.PHONY: help install install-dev install-hooks test test-unit test-integration test-ethics coverage lint format type-check clean gate-test port-lint frame-lint voids-backlog voids-backlog-check voidmap-ui-drift-check pipeline-essentials workflow-posture-check verify verify-core verify-governance verify-js verify-all verify-pointers claim-lint verify-json status status-verify snapshot all deepjump benchmark-replay intake

help:
	@echo "entaENGELment Framework - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install         Install package"
	@echo "  make install-dev     Install package with dev dependencies"
	@echo "  make install-hooks   Install pre-commit guard hooks"
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
	@echo "  make frame-lint      Run Frame Operator lint v0.1.1 (scope TBD; set FRAME_LINT_PATHS)"
	@echo ""
	@echo "Gate Policy:"
	@echo "  make gate-test       Test gate toggle functionality"
	@echo ""
	@echo "DeepJump Protocol v1.2:"
	@echo "  make verify          Phase 1: Core verify (ports, tests, pointers, claims)"
	@echo "  make verify-core     Same core membrane as make verify, without status/snapshot"
	@echo "  make verify-governance Check workflow posture and VOID backlog drift"
	@echo "  make verify-js       Check JS/TS workspace with frozen pnpm lockfile + Turbo"
	@echo "  make verify-all      Run core + governance + JS/TS verifier layers"
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
	@echo "Benchmark:"
	@echo "  make benchmark-replay Run deterministic benchmark replay"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove build artifacts and cache"
	@echo ""
	@echo "Docs:"
	@echo "  make voids-backlog       Regenerate docs/voids_backlog.md from VOIDMAP.yml"
	@echo "  make voids-backlog-check Verify docs/voids_backlog.md is in sync (exit 1 on drift)"
	@echo "  make voidmap-ui-drift-check Verify ui-app VOIDMAP mirror matches VOIDMAP.yml"
	@echo "  make pipeline-essentials  Report pipeline essentials and next expansion options"
	@echo "  make workflow-posture-check Verify workflows declare permissions + concurrency (exit 1 on drift)"
	@echo ""
	@echo "Intake (Calm Intake Layer):"
	@echo "  make intake FILE=<path> TITLE=\"<title>\" SOURCE=\"<source>\""
	@echo "                       Capture a document into docs/intake/raw/ (no canonisation)"

# === Setup ===
install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

# === Hooks ===
install-hooks:
	git config core.hooksPath .githooks
	@echo "Pre-commit hooks installed."

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

port-lint:
	@echo "🔍 Running Port-Matrix linter (K0..K4)..."
	@python3 tools/port_lint.py

# Frame Operator Lint (v0.1.1) — see tools/frame_lint.py and
# policies/frame_taxonomy_v0_1_1.yml.
#
# NOTE: input scope is not yet fixed. The tool expects YAML paths as positional
# arguments (claim/receipt files with `operative_frame`). Until a canonical
# scope is agreed (e.g. ark/p4/receipts/*.yaml, receipts/*.json), this target
# is NOT wired into `verify`. Override FRAME_LINT_PATHS to run it locally,
# e.g.: `make frame-lint FRAME_LINT_PATHS="ark/p4/receipts/*.yaml"`.
FRAME_LINT_PATHS ?=
frame-lint:
	@echo "🔍 Running Frame Operator linter (v0.1.1)..."
	@if [ -z "$(FRAME_LINT_PATHS)" ]; then \
		echo "frame-lint: no FRAME_LINT_PATHS set; scope to be defined."; \
		echo "Usage: make frame-lint FRAME_LINT_PATHS=\"path/to/file.yaml ...\""; \
		python3 tools/frame_lint.py --help >/dev/null 2>&1 || true; \
	else \
		python3 tools/frame_lint.py $(FRAME_LINT_PATHS); \
	fi

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
# Keep `verify` as the stable core membrane. Governance and JS/TS checks are
# explicit layered gates so dependency PRs cannot be treated as covered by a
# Python-only run, while small local edits stay ergonomically verifiable.
verify: verify-core
	@echo ""
	@echo "=== VERIFY COMPLETE ==="
	@echo "✅ Core verify membrane passed"
	@echo ""
	@echo "Next layered gates when relevant:"
	@echo "  make verify-governance  # workflow posture + VOID backlog drift"
	@echo "  make verify-js          # ui-app / packages / pnpm workspace"
	@echo ""

verify-core: port-lint test verify-pointers claim-lint
	@echo "✅ Core: ports, tests, pointers, and claims checked"

verify-governance: workflow-posture-check voids-backlog-check voidmap-ui-drift-check
	@echo "✅ Governance membrane checked"

verify-js:
	@echo "=== JS/TS WORKSPACE VERIFY ==="
	@command -v pnpm >/dev/null 2>&1 || { \
		echo "pnpm not found. Run 'corepack enable' so packageManager can provide pnpm."; \
		exit 2; \
	}
	@pnpm install --frozen-lockfile
	@$(JS_VERIFY_CMD)
	@echo "✅ JS/TS workspace verified with frozen lockfile"

verify-all: verify verify-governance verify-js
	@echo "✅ All verifier layers passed"

verify-pointers:
	@echo "=== VERIFY POINTERS ==="
	@$(PY) tools/verify_pointers.py --strict

claim-lint:
	@echo "=== CLAIM LINT ==="
	@$(PY) tools/claim_lint.py --scope index,spec,receipts,tools

# Docs generator: regenerate docs/voids_backlog.md from VOIDMAP.yml.
# Not wired into `verify` — opt-in. Use `voids-backlog-check` for drift detection.
voids-backlog:
	@$(PY) tools/voids_backlog_gen.py

voids-backlog-check:
	@$(PY) tools/voids_backlog_gen.py --check

# Drift check: ensure ui-app/lib/voidmap-parser.ts mirrors VOIDMAP.yml statuses.
voidmap-ui-drift-check:
	@$(PY) tools/voidmap_ui_drift_check.py

pipeline-essentials:
	@$(PY) tools/pipeline_essentials.py

# CI/CD posture drift check: verify workflows declare permissions + concurrency.
workflow-posture-check:
	@$(PY) tools/workflow_posture_check.py

# Calm Intake Layer: capture a document into docs/intake/raw/ (no canonisation).
# Thin wrapper around tools/intake_add.py. See docs/intake/README.md.
intake:
	@if [ -z "$(FILE)" ] || [ -z "$(TITLE)" ] || [ -z "$(SOURCE)" ]; then \
		echo "Usage: make intake FILE=<path> TITLE=\"<title>\" SOURCE=\"<source>\""; \
		exit 2; \
	fi
	@$(PY) tools/intake_add.py --file "$(FILE)" --title "$(TITLE)" --source "$(SOURCE)"

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

# === Benchmark ===
benchmark-replay:
	@echo "=== Benchmark Replay: Phasor Determinism ==="
	python3 tests/benchmark/test_phasor_replay.py
	@echo "=== Benchmark Replay: Receipt Lint ==="
	python3 tools/receipt_lint.py receipts/arc_sample.json
	@echo "=== Benchmark PASS ==="

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
