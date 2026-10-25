"""Privates Korpus als DataLad-Dataset (tools/corpus_datalad.py, tools/corpus_code/*)."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

from tools import corpus_datalad as cd
from tools.corpus_code import extract_text as ex
from tools.corpus_code import inventory as inv

DOCX_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
    "<w:p><w:r><w:t>Skaleninvarianz</w:t></w:r><w:r><w:tab/><w:t>Form</w:t></w:r></w:p>"
    "<w:p><w:r><w:t>Zeile</w:t><w:br/><w:t>zwei</w:t></w:r></w:p>"
    "</w:body></w:document>"
)


def _write_docx(path: Path, xml: str | bytes = DOCX_XML) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("word/document.xml", xml)


def _write_pdf(path: Path, text: str) -> None:
    """Minimales einseitiges PDF (Helvetica) für pdftotext."""
    stream = f"BT /F1 18 Tf 20 80 Td ({text}) Tj ET".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    path.write_bytes(bytes(out))


@pytest.fixture()
def inbox(tmp_path: Path) -> Path:
    box = tmp_path / "inbox" / "export"
    (box / "sub").mkdir(parents=True)
    (box / "save_state.md").write_text("# Save State\n", encoding="utf-8")
    (box / "sub" / "kopie.md").write_text("# Save State\n", encoding="utf-8")
    (box / "notiz.txt").write_bytes(b"\xef\xbb\xbfGrimm 1812\n")
    _write_docx(box / "analyse.docx")
    (box / "bild.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (box / ".DS_Store").write_bytes(b"x")
    with zipfile.ZipFile(box / "paket.zip", "w") as archive:
        archive.writestr("a/save_state.md", "# Save State\n")
        archive.writestr("../evil.txt", "x")
    return tmp_path / "inbox"


# --- extract_text ----------------------------------------------------------------------


def test_extract_text_outputs_and_log(inbox: Path, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ex.shutil, "which", lambda name: None)  # ohne pdftotext
    _write_pdf(inbox / "export" / "radar.pdf", "Resonanz")
    out = tmp_path / "text"
    log = ex.run(inbox, out)
    by_path = {e["path"]: e for e in log["entries"]}
    assert (out / "export/save_state.md.txt").read_text(encoding="utf-8") == "# Save State\n"
    assert (out / "export/notiz.txt.txt").read_text(encoding="utf-8") == "Grimm 1812\n"
    assert (out / "export/analyse.docx.txt").read_text(encoding="utf-8") == (
        "Skaleninvarianz\tForm\nZeile\nzwei\n"
    )
    assert by_path["export/radar.pdf"]["status"] == "skipped"
    assert by_path["export/paket.zip"]["status"] == "skipped"
    assert by_path["export/bild.png"]["status"] == "skipped"
    assert "export/.DS_Store" not in by_path
    assert log["pdftotext"] == "missing"
    assert log["counts"] == {"ok": 4, "skipped": 3}
    first = (out / ex.LOG_NAME).read_bytes()
    ex.run(inbox, out)
    assert (out / ex.LOG_NAME).read_bytes() == first  # deterministisch für datalad rerun


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="pdftotext not installed")
def test_extract_pdf_with_pdftotext(tmp_path: Path) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    _write_pdf(box / "radar.pdf", "Resonanz und Komplementaritaet")
    log = ex.run(box, tmp_path / "text")
    assert log["entries"][0]["status"] == "ok"
    assert "Resonanz und Komplementaritaet" in (tmp_path / "text/radar.pdf.txt").read_text()


def test_extract_reports_missing_annex_content_and_stale_outputs(tmp_path: Path) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    (box / "weg.md").symlink_to(tmp_path / "nicht-da")  # annex-Datei ohne lokalen Inhalt
    out = tmp_path / "text"
    out.mkdir()
    (out / "alt.md.txt").write_text("alt", encoding="utf-8")
    log = ex.run(box, out)
    assert log["entries"] == [
        {"path": "weg.md", "status": "missing", "detail": "Inhalt nicht lokal (git annex get)"}
    ]
    assert log["stale_outputs"] == ["alt.md.txt"]
    assert (out / "alt.md.txt").exists()  # nie löschen, nur melden


def test_docx_size_guard_yields_error(tmp_path: Path, monkeypatch) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    _write_docx(box / "gross.docx")
    monkeypatch.setattr(ex, "MAX_DOCX_XML_BYTES", 10)
    entry = ex.run(box, tmp_path / "text")["entries"][0]
    assert entry["status"] == "error"
    assert "zu groß" in entry["detail"]


def test_broken_docx_yields_error_not_exception(tmp_path: Path) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    (box / "kaputt.docx").write_bytes(b"kein zip")
    assert ex.run(box, tmp_path / "text")["entries"][0]["status"] == "error"


def test_output_path_collision_is_a_file_error(tmp_path: Path) -> None:
    box = tmp_path / "inbox"
    (box / "note.md.txt").mkdir(parents=True)
    (box / "note.md").write_text("a", encoding="utf-8")
    (box / "note.md.txt" / "other.md").write_text("b", encoding="utf-8")
    entries = ex.run(box, tmp_path / "text")["entries"]
    assert [(e["path"], e["status"]) for e in entries] == [
        ("note.md", "ok"),
        ("note.md.txt/other.md", "error"),
    ]
    assert entries[1]["detail"].startswith("Ausgabe note.md.txt/other.md.txt")


def test_pdf_timeout_is_a_file_error(tmp_path: Path, monkeypatch) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    (box / "lang.pdf").write_bytes(b"%PDF-1.4\n")
    (box / "danach.md").write_text("weiter", encoding="utf-8")

    def timeout(path: Path) -> str:
        raise subprocess.TimeoutExpired(["pdftotext"], ex.PDF_TIMEOUT_S)

    monkeypatch.setattr(ex.shutil, "which", lambda _name: "/usr/bin/pdftotext")
    monkeypatch.setattr(ex, "pdftotext_version", lambda: "test")
    monkeypatch.setattr(ex, "extract_pdf", timeout)
    log = ex.run(box, tmp_path / "text")
    assert log["counts"] == {"error": 1, "ok": 1}
    assert "TimeoutExpired" in log["entries"][1]["detail"]


# --- inventory -------------------------------------------------------------------------


def test_inventory_duplicates_archives_and_anchor(inbox: Path, tmp_path: Path) -> None:
    out = tmp_path / "inv"
    data = inv.run(inbox, out)
    summary = data["summary"]
    assert summary["files"] == 6
    assert summary["duplicate_groups"] == 1
    assert data["duplicates"][0]["locations"] == ["export/save_state.md", "export/sub/kopie.md"]
    members = data["archives"][0]["members"]
    assert [m["member"] for m in members] == ["../evil.txt", "a/save_state.md"]
    assert not (tmp_path / "evil.txt").exists()  # Archive werden nie entpackt
    cross = data["duplicates_including_archive_members"][0]
    assert "export/paket.zip!a/save_state.md" in cross["locations"]
    anchor = json.loads((out / "public_anchor.json").read_text(encoding="utf-8"))
    hashes = sorted(f["sha256"] for f in data["files"])
    assert anchor["snapshotRootHash"] == hashlib.sha256("\n".join(hashes).encode()).hexdigest()
    assert anchor["entryCount"] == 6 and anchor["distinctContentCount"] == 5
    anchor_text = (out / "public_anchor.json").read_text(encoding="utf-8")
    assert "save_state" not in anchor_text and "export" not in anchor_text
    assert "Duplikatgruppen: 1" in (out / "SUMMARY.md").read_text(encoding="utf-8")


def test_inventory_member_size_guard_and_missing(inbox: Path, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(inv, "MAX_MEMBER_BYTES", 1)
    (inbox / "export" / "weg.md").symlink_to(tmp_path / "nicht-da")
    data = inv.run(inbox, tmp_path / "inv")
    statuses = {m["member"]: m.get("status") for m in data["archives"][0]["members"]}
    assert statuses["a/save_state.md"] == "skipped: zu groß"
    assert data["missing_content"] == ["export/weg.md"]


def test_inventory_skips_encrypted_zip_members(inbox: Path, tmp_path: Path) -> None:
    path = inbox / "export" / "geheim.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("m.txt", "geheim")
    raw = bytearray(path.read_bytes())
    raw[raw.find(b"PK\x03\x04") + 6] |= 0x1  # Verschlüsselungsbit im lokalen Header
    raw[raw.find(b"PK\x01\x02") + 8] |= 0x1  # und im zentralen Verzeichnis
    path.write_bytes(bytes(raw))
    data = inv.run(inbox, tmp_path / "inv")
    archive_entry = next(a for a in data["archives"] if a["path"] == "export/geheim.zip")
    assert archive_entry["members"] == [
        {"member": "m.txt", "size": 6, "status": "skipped: verschlüsselt"}
    ]
    assert data["summary"]["files"] == 7


def test_inventory_is_deterministic(inbox: Path, tmp_path: Path) -> None:
    out = tmp_path / "inv"
    inv.run(inbox, out)
    first = {p.name: p.read_bytes() for p in out.iterdir()}
    inv.run(inbox, out)
    assert {p.name: p.read_bytes() for p in out.iterdir()} == first


# --- corpus_datalad --------------------------------------------------------------------


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_init_refuses_targets_inside_git_worktree(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    assert cd.inside_git_worktree(tmp_path / "out" / "korpus") == tmp_path.resolve()
    with pytest.raises(cd.CorpusError, match="außerhalb jedes"):
        cd.cmd_init(tmp_path / "out" / "korpus")


def test_init_refuses_non_empty_directory(tmp_path: Path) -> None:
    (tmp_path / "korpus").mkdir()
    (tmp_path / "korpus" / "x").write_text("x", encoding="utf-8")
    with pytest.raises(cd.CorpusError, match="nicht leer"):
        cd.cmd_init(tmp_path / "korpus")


def test_missing_tools_are_reported(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(cd, "inside_git_worktree", lambda path: None)
    monkeypatch.setattr(cd.shutil, "which", lambda name: None)
    with pytest.raises(cd.CorpusError, match="Nicht installiert: datalad, git-annex"):
        cd.cmd_init(tmp_path / "korpus")


def test_commands_require_a_dataset(tmp_path: Path) -> None:
    with pytest.raises(cd.CorpusError, match="kein DataLad-Dataset"):
        cd.cmd_extract(tmp_path)


def _fake_dataset(tmp_path: Path) -> Path:
    ds = tmp_path / "korpus"
    (ds / ".datalad").mkdir(parents=True)
    (ds / cd.IMPORTS_OUT).mkdir(parents=True)
    return ds


def test_import_copies_records_and_skips_symlinks(tmp_path: Path, monkeypatch) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr(cd, "_run", lambda cmd, cwd=None: calls.append(cmd) or "")
    ds = _fake_dataset(tmp_path)
    src = tmp_path / "export"
    (src / "sub").mkdir(parents=True)
    (src / "a.md").write_text("a", encoding="utf-8")
    (src / "sub" / "b.pdf").write_bytes(b"%PDF")
    (src / "link.md").symlink_to(src / "a.md")
    record = cd.cmd_import(ds, src, "Drive Export 2026-10-25")
    assert record["slug"] == "drive-export-2026-10-25"
    assert [f["path"] for f in record["files"]] == ["a.md", "sub/b.pdf"]
    assert record["skipped"] == [{"path": "link.md", "reason": "Symlink nicht übernommen"}]
    assert (ds / "inbox/drive-export-2026-10-25/sub/b.pdf").read_bytes() == b"%PDF"
    saved = json.loads((ds / cd.IMPORTS_OUT / "drive-export-2026-10-25.json").read_text())
    assert saved["files"][0]["sha256"] == hashlib.sha256(b"a").hexdigest()
    assert calls[-1][:2] == ["datalad", "save"]
    with pytest.raises(cd.CorpusError, match="existiert bereits"):
        cd.cmd_import(ds, src, "Drive Export 2026-10-25")
    with pytest.raises(cd.CorpusError, match="enthalten"):
        cd.cmd_import(ds, tmp_path, "zu weit")


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_import_keeps_git_control_files_inert(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(cd, "_run", lambda cmd, cwd=None: "")
    ds = _fake_dataset(tmp_path)
    subprocess.run(["git", "init", "-q", str(ds)], check=True)
    (ds / ".gitattributes").write_text(cd.GITATTRIBUTES, encoding="utf-8")
    src = tmp_path / "export"
    (src / ".git").mkdir(parents=True)
    (src / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (src / ".gitattributes").write_text("* annex.largefiles=nothing\n", encoding="utf-8")
    (src / "a.md").write_text("Original\n", encoding="utf-8")
    record = cd.cmd_import(ds, src, "Beispiel")
    assert [(f["path"], f.get("stored_as")) for f in record["files"]] == [
        (".git/HEAD", ".git~import/HEAD"),
        (".gitattributes", ".gitattributes~import"),
        ("a.md", None),
    ]
    box = ds / "inbox" / "beispiel"
    assert not (box / ".gitattributes").exists() and not (box / ".git").exists()
    assert (box / ".gitattributes~import").read_text() == "* annex.largefiles=nothing\n"
    attr = subprocess.run(
        ["git", "check-attr", "annex.largefiles", "--", "inbox/beispiel/a.md"],
        cwd=ds,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert attr == "inbox/beispiel/a.md: annex.largefiles: unspecified"


def test_import_rejects_colliding_storage_paths(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(cd, "_run", lambda cmd, cwd=None: "")
    ds = _fake_dataset(tmp_path)
    src = tmp_path / "export"
    src.mkdir()
    (src / ".gitignore").write_text("*\n", encoding="utf-8")
    (src / ".gitignore~import").write_text("x\n", encoding="utf-8")
    with pytest.raises(cd.CorpusError, match="Ablagepfad doppelt"):
        cd.cmd_import(ds, src, "Kollision")
    assert not (ds / "inbox" / "kollision").exists()


def test_import_into_clone_without_imports_dir(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(cd, "_run", lambda cmd, cwd=None: "")
    ds = tmp_path / "klon"
    (ds / ".datalad").mkdir(parents=True)  # Klon: leerer imports/-Ordner fehlt
    src = tmp_path / "export"
    src.mkdir()
    (src / "a.md").write_text("a", encoding="utf-8")
    cd.cmd_import(ds, src, "Im Klon")
    assert (ds / cd.IMPORTS_OUT / "im-klon.json").is_file()


def test_sources_for_reentry_bind_hashes(tmp_path: Path) -> None:
    ds = _fake_dataset(tmp_path)
    files = [
        {"path": "export/save_state.md", "size": 1, "sha256": "a" * 64},
        {"path": "export/sub/save_state.md", "size": 1, "sha256": "a" * 64},
        {"path": "export/radar.pdf", "size": 1, "sha256": "b" * 64},
    ]
    (ds / cd.INVENTORY_OUT / "inventory.json").write_text(json.dumps({"files": files}))
    entries = cd.sources_for_reentry(ds, "*.md")
    assert [e["id"] for e in entries] == ["save-state-aaaaaaaa", "save-state-aaaaaaaa-2"]
    assert entries[0] == {
        "id": "save-state-aaaaaaaa",
        "path": str(ds.resolve() / "inbox/export/save_state.md"),
        "role": "input",
        "sha256": "a" * 64,
    }
    assert len(cd.sources_for_reentry(ds)) == 3


@pytest.mark.skipif(
    shutil.which("datalad") is None or shutil.which("git-annex") is None,
    reason="datalad/git-annex not installed",
)
def test_end_to_end_with_datalad(inbox: Path, tmp_path: Path) -> None:
    ds = cd.cmd_init(tmp_path / "korpus")
    cd.cmd_import(ds, inbox / "export", "Synthetischer Export")
    assert cd.cmd_extract(ds)["counts"]["ok"] == 4
    assert cd.cmd_inventory(ds)["summary"]["duplicate_groups"] == 1
    log = subprocess.run(
        ["git", "log", "--format=%s"], cwd=ds, capture_output=True, text=True, check=True
    ).stdout
    assert "[DATALAD RUNCMD] extract" in log and "[DATALAD RUNCMD] inventory" in log
    assert (ds / "inbox/synthetischer-export/save_state.md").is_symlink()  # Inhalt im annex
    assert not (ds / "code/extract_text.py").is_symlink()  # Code in git


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_only_dataset_root_readme_is_kept_in_git(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitattributes").write_text(cd.GITATTRIBUTES, encoding="utf-8")
    out = subprocess.run(
        ["git", "check-attr", "annex.largefiles", "--", "README.md", "inbox/x/README.md"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert out == [
        "README.md: annex.largefiles: nothing",
        "inbox/x/README.md: annex.largefiles: unspecified",  # Original bleibt im annex
    ]


@pytest.mark.parametrize("encoding", ["utf-8", "utf-16"])
@pytest.mark.parametrize("decl", ["<!DOCTYPE d [<!ENTITY a 'x'>]>", "<!ENTITY a 'x'>"])
def test_docx_with_dtd_or_entities_is_rejected(tmp_path: Path, decl: str, encoding: str) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    xml = DOCX_XML.replace("UTF-8", encoding.upper()).replace("Form", "&a;")
    _write_docx(
        box / "bomb.docx", xml.replace("<w:document", decl + "<w:document", 1).encode(encoding)
    )
    entry = ex.run(box, tmp_path / "text")["entries"][0]
    assert entry["status"] == "error"
    assert not (tmp_path / "text/bomb.docx.txt").exists()


def test_utf16_docx_without_dtd_is_extracted(tmp_path: Path) -> None:
    box = tmp_path / "inbox"
    box.mkdir()
    _write_docx(box / "u16.docx", DOCX_XML.replace("UTF-8", "UTF-16").encode("utf-16"))
    assert ex.run(box, tmp_path / "text")["entries"][0]["status"] == "ok"
    assert "Skaleninvarianz\tForm" in (tmp_path / "text/u16.docx.txt").read_text()
