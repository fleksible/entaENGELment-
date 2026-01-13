import tempfile
from pathlib import Path

from tools.port_lint import extract_markers, lint_file


def _tmp_file(text: str, suffix: str) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8")
    f.write(text)
    f.flush()
    f.close()
    return Path(f.name)


def test_extract_markers_basic():
    text = "K0::NEBEL ... K1::FADEN ... K2::PORT? ... K3::LEAK ... K4::PASS"
    assert extract_markers(text) == ["K0::NEBEL", "K1::FADEN", "K2::PORT?", "K3::LEAK", "K4::PASS"]


def test_no_markers_is_ok():
    p = _tmp_file("This doc has no markers.", ".md")
    errs = lint_file(p)
    assert errs == []


def test_marker_backwards_is_error():
    p = _tmp_file("Here: K3::LEAK then later K1::FADEN (backwards)", ".md")
    errs = lint_file(p)
    assert any(code == "K_MARKER_ORDER" for code, _ in errs)


def test_gaps_are_allowed():
    p = _tmp_file("We only mention K2::PORT? and K4::PASS", ".md")
    errs = lint_file(p)
    assert errs == []


def test_receipt_flood_guard_triggers_only_for_receiptish_files():
    # JSON with many tags and receipt keyword should trigger
    tags = " ".join(["FACT"] * 60)
    p = _tmp_file(f'{{"kind":"receipt","tags":"{tags}"}}', ".json")
    errs = lint_file(p)
    assert any(code == "RECEIPT_FLOOD" for code, _ in errs)


def test_receipt_flood_guard_does_not_trigger_without_receipt_hint():
    tags = " ".join(["FACT"] * 60)
    p = _tmp_file(f'{{"kind":"note","tags":"{tags}"}}', ".json")
    errs = lint_file(p)
    assert errs == []
