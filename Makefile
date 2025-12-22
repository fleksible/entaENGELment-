PY ?= python3
OUT ?= out
RECEIPT ?= receipts/arc_sample.json
SNAPSHOT_INPUTS ?= "seeds/*.yaml" "audit/*.yaml"
STATUS ?= PASS
H ?= 0.84
DMI ?= 4.7
PHI ?= 0.72
REFRACTORY ?= 120

.PHONY: verify-json status status-verify snapshot clean all

all: verify-json status-verify snapshot

verify-json:
	@mkdir -p $(OUT)
	@$(PY) tests/verify_deep_jump.py --receipt $(RECEIPT) --json > $(OUT)/verify.json

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

snapshot:
	@mkdir -p $(OUT)
	@$(PY) tools/snapshot_guard.py $(OUT)/snapshot_manifest.json $(SNAPSHOT_INPUTS) --strict

clean:
	rm -rf $(OUT)
