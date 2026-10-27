"""Behavioral checks on isolated, entirely synthetic repositories and sources."""

import importlib.util
import json
import pathlib
import sqlite3
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "tools" / "corpus_search.py"


class TestCorpusSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = pathlib.Path(cls.temp.name)
        cls.repo = cls.root / "repo"
        cls.repo.mkdir()

        def git(*args):
            return (
                subprocess.check_output(
                    ["git", "-C", str(cls.repo), *args], stderr=subprocess.DEVNULL
                )
                .decode()
                .strip()
            )

        cls.git = staticmethod(git)
        git("init", "-q")
        git("config", "user.email", "test@example.invalid")
        git("config", "user.name", "Synthetic Test")
        git("remote", "add", "origin", "https://github.com/synthetic/search-fixture.git")
        (cls.repo / "original.md").write_text("Grüneisen\n2👁2\nzN\nStatus: HOLD\n")
        (cls.repo / "copy.md").write_bytes((cls.repo / "original.md").read_bytes())
        (cls.repo / "variant.md").write_text("Grueneisen\n2|1|2\nzñ\n")
        (cls.repo / "single-number.md").write_text("Only 2\n")
        (cls.repo / "mast.md").write_text("master marker\nMast position\n")
        (cls.repo / "uv.lock").write_text("technical repeat repeat repeat")
        (cls.repo / "binary.dat").write_bytes(b"\x00\xff")
        git("add", ".")
        git("commit", "-qm", "synthetic base")
        cls.base = git("rev-parse", "HEAD")
        (cls.repo / "proposal.md").write_text("SIMULATION_PROXY new candidate\nStatus: HOLD\n")
        git("add", ".")
        git("commit", "-qm", "synthetic proposal")
        cls.head = git("rev-parse", "HEAD")
        cls.aliases = cls.root / "aliases.json"
        cls.aliases.write_text(
            json.dumps(
                {
                    "groups": [
                        {
                            "key": "g",
                            "spellings": ["Grüneisen", "Grueneisen"],
                            "related": ["SIMULATION_PROXY"],
                            "guard": "Different registers",
                        }
                    ]
                }
            )
        )
        cls.out = cls.root / "output"
        cls.stats = json.loads(
            subprocess.check_output(
                [
                    "python3",
                    str(SCRIPT),
                    "build",
                    "--repo",
                    str(cls.repo),
                    "--ref",
                    cls.base,
                    "--overlay",
                    "pr-test=" + cls.head,
                    "--aliases",
                    str(cls.aliases),
                    "--out",
                    str(cls.out),
                ]
            )
        )

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def query(self, q, *args):
        return json.loads(
            subprocess.check_output(
                ["python3", str(SCRIPT), "search", str(self.out / "search.sqlite3"), q, *args]
            )
        )

    def build_at(self, destination, *args):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "build",
                "--repo",
                str(self.repo),
                "--ref",
                self.base,
                "--out",
                str(destination),
                *args,
            ],
            capture_output=True,
            text=True,
        )

    def test_literal_preserves_diacritics(self):
        r = self.query("Gru\u0308neisen")
        self.assertEqual(r["total_matching_documents_by_scope"], {"main": 2})

    def test_variants_require_explicit_expansion(self):
        r = self.query("Grüneisen", "--mode", "expanded")
        self.assertEqual(r["total_matching_documents_by_scope"], {"main": 3})
        self.assertNotIn("pr-test", r["total_matching_documents_by_scope"])

    def test_related_terms_are_labelled_and_opt_in(self):
        r = self.query("Grüneisen", "--mode", "expanded", "--related")
        self.assertIn("pr-test", r["total_matching_documents_by_scope"])
        self.assertIn(["SIMULATION_PROXY", "related_not_equivalent"], r["expanded_terms"])

    def test_symbols_are_not_silently_equated(self):
        self.assertEqual(self.query("2👁2")["total_matching_documents_by_scope"], {"main": 2})
        self.assertEqual(self.query("2|1|2")["total_matching_documents_by_scope"], {"main": 1})
        self.assertEqual(self.query("zñ")["total_matching_documents_by_scope"], {"main": 1})

    def test_token_mode_rejects_symbol_loss(self):
        r = subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "search",
                str(self.out / "search.sqlite3"),
                "2👁2",
                "--mode",
                "tokens",
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("discard query symbols", r.stderr)

    def test_token_multiplicity_is_preserved(self):
        r = self.query("2 2", "--mode", "tokens")
        self.assertNotIn("single-number.md", [x["path"] for x in r["results"]])
        self.assertEqual(r["results"][0]["matched_variants"], [])
        self.assertEqual(r["results"][0]["matched_tokens"], ["2", "2"])

    def test_nested_status_retains_line_scope(self):
        spec = importlib.util.spec_from_file_location("search_module", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(
            module.declared_status("record:\n  status: OPEN\n"),
            [{"line": 2, "declaration": "status: OPEN"}],
        )
        self.assertEqual(len(module.declared_status("  status: OPEN\n" * 22)), 22)

    def test_token_line_anchor_is_not_substring(self):
        r = self.query("Mast", "--mode", "tokens")
        self.assertEqual(r["results"][0]["line"], 2)
        self.assertIn("Mast position", r["results"][0]["excerpt"])

    def test_provenance_uses_actual_repository(self):
        r = self.query("SIMULATION_PROXY")
        self.assertTrue(
            r["results"][0]["provenance_url"].startswith(
                "https://github.com/synthetic/search-fixture/blob/"
            )
        )

    def test_pr_is_changed_files_only(self):
        self.assertEqual(self.stats["scopes"]["pr-test"]["indexed_documents"], 1)
        self.assertEqual(self.query("SIMULATION_PROXY", "--scope", "main")["results"], [])

    def test_dedup_and_lock_exclusions(self):
        self.assertLess(
            self.stats["scopes"]["main"]["unique_content_tokens"],
            self.stats["scopes"]["main"]["tokens"],
        )
        self.assertEqual(self.stats["excluded"]["dependency_lock_or_generated_requirements"], 1)

    def test_status_not_promoted(self):
        r = self.query("2👁2")
        self.assertIn("HOLD", str(r["results"][0]["declared_status"]))
        self.assertEqual(r["results"][0]["read_state"], "MACHINE_INDEXED_NOT_SEMANTICALLY_READ")

    def test_ref_and_source_are_pinned(self):
        r = self.query("SIMULATION_PROXY")
        self.assertEqual(r["results"][0]["ref"], self.head)
        self.assertEqual(r["results"][0]["path"], "proposal.md")

    def test_truncation_is_explicit_and_does_not_change_total(self):
        r = self.query("Grüneisen", "--limit", "1")
        self.assertEqual(len(r["results"]), 1)
        self.assertEqual(r["total_matching_documents_by_scope"], {"main": 2})
        self.assertTrue(r["truncated"])

    def test_related_query_does_not_expand_back_to_canonical_spelling(self):
        r = self.query("SIMULATION_PROXY", "--mode", "expanded")
        self.assertEqual(r["total_matching_documents_by_scope"], {"pr-test": 1})

    def test_existing_output_and_source_tree_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            out = pathlib.Path(temp)
            sentinel = out / "manifest.json"
            sentinel.write_text("retain this")
            self.assertNotEqual(self.build_at(out).returncode, 0)
            self.assertEqual(sentinel.read_text(), "retain this")
        self.assertNotEqual(self.build_at(self.repo / "forbidden-output").returncode, 0)
        self.assertFalse((self.repo / "forbidden-output").exists())

    def test_invalid_queries_do_not_silently_become_broad_matches(self):
        for query, options in [
            ("", []),
            (" ", []),
            ("Mast", ["--limit", "-1"]),
            ("👁", ["--mode", "tokens"]),
        ]:
            with self.subTest(query=query, options=options):
                r = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "search",
                        str(self.out / "search.sqlite3"),
                        query,
                        *options,
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(r.returncode, 0)

    def test_corpus_sources_with_same_title_keep_distinct_identities(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            original = root / "text.txt"
            original.write_text("unresolved original")
            sources = root / "sources.json"
            sources.write_text(
                json.dumps(
                    [
                        {
                            "local_path": str(original),
                            "source_id": source_id,
                            "source_version": None,
                            "title": "same-title.txt",
                            "source_kind": "original",
                        }
                        for source_id in ["synthetic-source-1", "synthetic-source-2"]
                    ]
                )
            )
            output = root / "search"
            result = self.build_at(output, "--corpus", str(sources))
            self.assertEqual(result.returncode, 0, result.stderr)
            db = sqlite3.connect(
                (output / "search.sqlite3").resolve().as_uri() + "?mode=ro", uri=True
            )
            try:
                self.assertEqual(
                    db.execute("select count(*) from docs where scope='corpus'").fetchone()[0], 2
                )
                self.assertEqual(
                    db.execute(
                        "select count(distinct family) from docs where scope='corpus'"
                    ).fetchone()[0],
                    1,
                )
                self.assertEqual(
                    db.execute("select distinct family from docs where scope='corpus'").fetchone()[
                        0
                    ],
                    "UNKNOWN",
                )
            finally:
                db.close()

    def test_generated_index_control_is_excluded_before_opening(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            sources = root / "sources.json"
            sources.write_text(
                json.dumps(
                    [
                        {
                            "local_path": str(root / "does-not-exist"),
                            "title": "control.txt",
                            "source_kind": "generated_index",
                        }
                    ]
                )
            )
            result = self.build_at(root / "search", "--corpus", str(sources))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout)["excluded"]["generated_index_control_not_evidence"], 1
            )

    def test_rename_deletion_and_large_file_are_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            repo = root / "repo"
            subprocess.run(["git", "clone", "-q", str(self.repo), str(repo)], check=True)

            def git(*args):
                return subprocess.check_output(["git", "-C", str(repo), *args]).decode().strip()

            git("config", "user.email", "test@example.invalid")
            git("config", "user.name", "Synthetic Test")
            git("checkout", "-q", "--detach", self.base)
            git("mv", "original.md", "renamed.md")
            (repo / "large.txt").write_bytes(b"x" * (4 * 1024 * 1024 + 1))
            git("add", ".")
            git("commit", "-qm", "synthetic rename and oversized text")
            head = git("rev-parse", "HEAD")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "build",
                    "--repo",
                    str(repo),
                    "--ref",
                    self.base,
                    "--overlay",
                    "proposal=" + head,
                    "--out",
                    str(root / "search"),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((root / "search" / "manifest.json").read_text())
            overlay = next(s for s in manifest["scope"] if s["scope"] == "proposal")
            self.assertIn("original.md", overlay["deleted_paths"])
            self.assertIn(
                "renamed.md", [d["path"] for d in manifest["documents"] if d["scope"] == "proposal"]
            )
            self.assertIn(
                {"scope": "proposal", "ref": head, "path": "large.txt", "reason": "size_limit"},
                manifest["exclusions"],
            )


if __name__ == "__main__":
    unittest.main()
