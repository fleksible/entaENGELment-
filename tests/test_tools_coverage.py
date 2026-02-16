"""Import-based tests for tools/ modules to ensure coverage.

Existing tests call tools via subprocess which coverage cannot track.
These tests import and exercise core functions directly.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from unittest import mock

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"

# Ensure tools/ is importable
if str(TOOLS_DIR.parent) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR.parent))


# ===========================================================================
# tools/claim_lint.py
# ===========================================================================


class TestClaimLintImport:
    """Cover claim_lint.py via direct import."""

    def _import(self):
        from tools import claim_lint

        return claim_lint

    def test_valid_tags_constant(self):
        cl = self._import()
        assert "[FACT]" in cl.VALID_TAGS
        assert "[HYP]" in cl.VALID_TAGS
        assert "[MET]" in cl.VALID_TAGS
        assert "[TODO]" in cl.VALID_TAGS
        assert "[RISK]" in cl.VALID_TAGS

    def test_has_claim_tag_positive(self):
        cl = self._import()
        assert cl.has_claim_tag("This is a [FACT] statement")
        assert cl.has_claim_tag("[HYP] hypothesis here")

    def test_has_claim_tag_negative(self):
        cl = self._import()
        assert not cl.has_claim_tag("No tags in this line")
        assert not cl.has_claim_tag("Just some text")

    def test_is_python_code_line(self):
        cl = self._import()
        assert cl._is_python_code_line("if something:")
        assert cl._is_python_code_line("return value")
        assert cl._is_python_code_line("x = 42")
        assert cl._is_python_code_line("print('hello')")
        assert cl._is_python_code_line("# a comment")
        assert cl._is_python_code_line('"""docstring"""')
        assert not cl._is_python_code_line("This must be tagged")

    def test_should_skip(self):
        cl = self._import()
        assert cl.should_skip("foo/__pycache__/bar.pyc")
        assert cl.should_skip("path/.git/config")
        assert not cl.should_skip("tools/claim_lint.py")

    def test_get_repo_root(self):
        cl = self._import()
        root = cl.get_repo_root()
        assert root.exists()
        assert (root / "tools" / "claim_lint.py").exists()

    def test_find_claims_in_file_with_tag(self, tmp_path):
        cl = self._import()
        f = tmp_path / "test.yaml"
        f.write_text("[FACT] This must work\n")
        results = cl.find_claims_in_file(f, tmp_path)
        assert len(results) == 0  # tagged, so not reported

    def test_find_claims_in_file_without_tag(self, tmp_path):
        cl = self._import()
        f = tmp_path / "test.yaml"
        f.write_text("This must work\n")
        results = cl.find_claims_in_file(f, tmp_path)
        assert len(results) == 1
        assert results[0].claim_word == "must"

    def test_find_claims_noqa_suppression(self, tmp_path):
        cl = self._import()
        f = tmp_path / "test.yaml"
        f.write_text("verify_report: out/verify.json  # noqa: claim-lint\n")
        results = cl.find_claims_in_file(f, tmp_path)
        assert len(results) == 0

    def test_find_claims_python_code_skip(self, tmp_path):
        cl = self._import()
        f = tmp_path / "test.py"
        f.write_text("passed = reason is None\nif passed:\n    return passed\n")
        results = cl.find_claims_in_file(f, tmp_path)
        assert len(results) == 0

    def test_scan_directory_empty(self, tmp_path):
        cl = self._import()
        results = cl.scan_directory(tmp_path, tmp_path)
        assert results == []

    def test_scan_directory_missing(self, tmp_path):
        cl = self._import()
        results = cl.scan_directory(tmp_path / "nonexistent", tmp_path)
        assert results == []

    def test_scan_directory_with_claims(self, tmp_path):
        cl = self._import()
        f = tmp_path / "test.yaml"
        f.write_text("This must be done\n")
        results = cl.scan_directory(tmp_path, tmp_path)
        assert len(results) == 1

    def test_run_claim_lint_clean(self, tmp_path):
        cl = self._import()
        d = tmp_path / "scope"
        d.mkdir()
        (d / "clean.yaml").write_text("[FACT] All tagged properly\n")
        success = cl.run_claim_lint(tmp_path, ["scope"], strict=True)
        assert success is True

    def test_run_claim_lint_strict_fail(self, tmp_path):
        cl = self._import()
        d = tmp_path / "scope"
        d.mkdir()
        (d / "bad.yaml").write_text("This must fail\n")
        success = cl.run_claim_lint(tmp_path, ["scope"], strict=True)
        assert success is False

    def test_run_claim_lint_warn(self, tmp_path):
        cl = self._import()
        d = tmp_path / "scope"
        d.mkdir()
        (d / "bad.yaml").write_text("This must warn\n")
        success = cl.run_claim_lint(tmp_path, ["scope"], strict=False)
        assert success is True  # warns but doesn't fail


# ===========================================================================
# tools/verify_pointers.py
# ===========================================================================


class TestVerifyPointersImport:
    """Cover verify_pointers.py via direct import."""

    def _import(self):
        from tools import verify_pointers

        return verify_pointers

    def test_get_repo_root(self):
        vp = self._import()
        root = vp.get_repo_root()
        assert root.exists()

    def test_is_optional_context(self):
        vp = self._import()
        assert vp.is_optional_context("(optional) path/to/file")
        assert vp.is_optional_context("[OPT] path/to/file")
        assert not vp.is_optional_context("path/to/required")

    def test_is_core_path(self):
        vp = self._import()
        assert vp.is_core_path("tools/status_emit.py")
        assert vp.is_core_path("tests/verify_deep_jump.py")

    def test_extract_paths_from_yaml(self):
        vp = self._import()
        root = vp.get_repo_root()
        yaml_path = root / "index" / "modules" / "MOD_6_RECEIPTS_CORE.yaml"
        if yaml_path.exists():
            results = vp.extract_paths_from_yaml(yaml_path, root)
            assert len(results) > 0

    def test_verify_pointers_runs(self):
        vp = self._import()
        root = vp.get_repo_root()
        success = vp.verify_pointers(root, strict=False)
        assert success is True


# ===========================================================================
# tools/snapshot_guard.py
# ===========================================================================


class TestSnapshotGuardImport:
    """Cover snapshot_guard.py via direct import."""

    def _import(self):
        from tools import snapshot_guard

        return snapshot_guard

    def test_get_repo_root(self):
        sg = self._import()
        root = sg.get_repo_root()
        assert os.path.isdir(root)

    def test_hash_file(self, tmp_path):
        sg = self._import()
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h = sg.hash_file(str(f))
        expected = hashlib.sha256(b"hello world").hexdigest()
        assert h == expected

    def test_is_within_root(self):
        sg = self._import()
        root = sg.get_repo_root()
        assert sg.is_within_root(os.path.join(root, "tools", "snapshot_guard.py"), root)
        assert not sg.is_within_root("/etc/passwd", root)

    def test_build_file_list(self):
        sg = self._import()
        root = sg.get_repo_root()
        files = sg.build_file_list(root, ["seeds/*.yaml"])
        assert isinstance(files, list)

    def test_create_manifest(self, tmp_path):
        sg = self._import()
        f = tmp_path / "test.txt"
        f.write_text("manifest test")
        manifest = sg.create_manifest(str(tmp_path), [str(f)])
        assert isinstance(manifest, dict)
        assert len(manifest) == 1


# ===========================================================================
# tools/status_emit.py
# ===========================================================================


class TestStatusEmitImport:
    """Cover status_emit.py via direct import."""

    def _import(self):
        from tools import status_emit

        return status_emit

    def test_valid_tags_constant(self):
        se = self._import()
        assert "[FACT]" in se.VALID_TAGS

    def test_canonical_json(self):
        se = self._import()
        payload = {"b": 2, "a": 1}
        result = se.canonical_json(payload)
        parsed = json.loads(result)
        keys = list(parsed.keys())
        assert keys == ["a", "b"]  # sorted

    def test_sign_payload(self):
        se = self._import()
        payload = {"test": "data"}
        sig = se.sign_payload(payload, "test_secret")
        assert isinstance(sig, str)
        assert len(sig) == 64  # HMAC-SHA256 hex

    def test_compute_state_fingerprint(self):
        se = self._import()
        payload = {"status": "PASS", "metrics": {"H": 0.85}}
        fp = se.compute_state_fingerprint(payload)
        assert isinstance(fp, str)
        assert len(fp) > 0

    def test_get_secret_from_env(self):
        se = self._import()
        with mock.patch.dict(os.environ, {"ENTA_HMAC_SECRET": "testsecret"}):
            secret = se.get_secret()
            assert secret == "testsecret"

    def test_get_secret_fallback(self):
        se = self._import()
        env = {
            k: v for k, v in os.environ.items() if k not in ("ENTA_HMAC_SECRET", "CI_SECRET", "CI")
        }
        with mock.patch.dict(os.environ, env, clear=True):
            secret = se.get_secret()
            assert secret == ""

    def test_get_secret_raises_in_ci(self):
        se = self._import()
        env = {k: v for k, v in os.environ.items() if k not in ("ENTA_HMAC_SECRET", "CI_SECRET")}
        env["CI"] = "true"
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(OSError, match="ENTA_HMAC_SECRET is not set"):
                se.get_secret()


# ===========================================================================
# tools/status_verify.py
# ===========================================================================


class TestStatusVerifyImport:
    """Cover status_verify.py via direct import."""

    def _import(self):
        from tools import status_verify

        return status_verify

    def test_verify_payload_valid(self):
        from tools import status_emit, status_verify

        payload = {"status": "PASS", "metrics": {"H": 0.85}}
        secret = "test_secret_key"
        sig = status_emit.sign_payload(payload, secret)
        signed = copy.deepcopy(payload)
        signed["signatures"] = {"hmac": sig}
        ok, msg = status_verify.verify_payload(signed, secret)
        assert ok is True

    def test_verify_payload_invalid(self):
        sv = self._import()
        payload = {"status": "PASS", "signatures": {"hmac": "bad_signature"}}
        ok, msg = sv.verify_payload(payload, "secret")
        assert ok is False

    def test_verify_payload_missing_sig(self):
        sv = self._import()
        payload = {"status": "PASS"}
        ok, msg = sv.verify_payload(payload, "secret")
        assert ok is False


# ===========================================================================
# tools/metatron_check.py
# ===========================================================================


class TestMetatronCheckImport:
    """Cover metatron_check.py via direct import."""

    def _import(self):
        from tools import metatron_check

        return metatron_check

    def test_check_text_with_fokus(self):
        mc = self._import()
        ok, checks = mc.check_text("FOKUS: Test coverage\nSome work done")
        assert ok is True

    def test_check_text_without_fokus(self):
        mc = self._import()
        ok, checks = mc.check_text("No focus marker here")
        assert ok is False

    def test_check_text_with_switch(self):
        mc = self._import()
        text = "FOKUS: Original task\nFOKUS-SWITCH: Original -> New\nFrage: Switch?"
        ok, checks = mc.check_text(text)
        assert ok is True

    def test_has_question_after_switch(self):
        mc = self._import()
        text = "FOKUS-SWITCH: A -> B\nFrage: Should we switch?"
        assert mc.has_question_after_switch(text) is True

    def test_no_question_after_switch(self):
        mc = self._import()
        text = "FOKUS-SWITCH: A -> B\nNo question here"
        assert mc.has_question_after_switch(text) is False


# ===========================================================================
# tools/receipt_lint.py
# ===========================================================================


class TestReceiptLintImport:
    """Cover receipt_lint.py via direct import."""

    def _import(self):
        from tools import receipt_lint

        return receipt_lint

    def test_is_legacy_manifest_colon(self):
        rl = self._import()
        assert rl.is_legacy_manifest_colon("file.json:path") is True
        assert rl.is_legacy_manifest_colon("file.json#/path") is False

    def test_find_evidence_refs_string(self):
        rl = self._import()
        refs = list(rl.find_evidence_refs({"evidence_ref": "data.json#/key"}))
        assert len(refs) == 1
        assert refs[0] == "data.json#/key"

    def test_find_evidence_refs_nested(self):
        rl = self._import()
        obj = {"items": [{"evidence_ref": "a.json#/x"}, {"evidence_ref": "b.json#/y"}]}
        refs = list(rl.find_evidence_refs(obj))
        assert len(refs) == 2

    def test_lint_file_valid(self):
        rl = self._import()
        sample = REPO_ROOT / "receipts" / "arc_sample.json"
        if sample.exists():
            errors = rl.lint_file(sample, strict=False)
            assert errors == []

    def test_iter_yaml_files(self, tmp_path):
        rl = self._import()
        (tmp_path / "a.yaml").write_text("key: value\n")
        (tmp_path / "b.json").write_text("{}\n")
        yaml_files = list(rl.iter_yaml_files(tmp_path))
        assert len(yaml_files) == 1
