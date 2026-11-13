"""Behavioral checks on isolated, entirely synthetic repositories and sources."""

import collections
import hashlib
import importlib.util
import json
import pathlib
import sqlite3
import subprocess
import sys
import tempfile
import unicodedata
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


class TestOriginalBytesIdentityAndExcerpt(unittest.TestCase):
    """Regressions for supplied bytes, record identity and match-bound excerpts."""

    NEWLINES = {
        "lf": b"alpha\nneedle\nomega\n",
        "crlf": b"alpha\r\nneedle\r\nomega\r\n",
        "cr": b"alpha\rneedle\romega\r",
    }

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

        git("init", "-q")
        git("config", "user.email", "test@example.invalid")
        git("config", "user.name", "Synthetic Test")
        git("config", "core.autocrlf", "false")
        (cls.repo / ".gitattributes").write_text("* -text\n")
        for name, raw in cls.NEWLINES.items():
            (cls.repo / (name + ".txt")).write_bytes(raw)
        git("add", ".")
        git("commit", "-qm", "synthetic newline fixtures")
        cls.ref = git("rev-parse", "HEAD")
        spec = importlib.util.spec_from_file_location("search_module_spans", SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.limit = cls.module.EXCERPT_CHARS
        cls.counter = 0

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @staticmethod
    def entry(path, **metadata):
        return {
            "local_path": str(path),
            "source_id": "synthetic-source",
            "source_version": "v1",
            "title": "same-title.txt",
            "source_kind": "original",
            **metadata,
        }

    def build(self, entries):
        type(self).counter += 1
        manifest = self.root / f"sources-{self.counter}.json"
        manifest.write_text(json.dumps(entries), encoding="utf-8")
        output = self.root / f"index-{self.counter}"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "build",
                "--repo",
                str(self.repo),
                "--ref",
                self.ref,
                "--corpus",
                str(manifest),
                "--out",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        return result, output

    def source(self, text):
        type(self).counter += 1
        path = self.root / f"source-{self.counter}.txt"
        path.write_bytes(text.encode("utf-8"))
        return path

    def hit(self, text, query, *options):
        result, output = self.build([self.entry(self.source(text))])
        self.assertEqual(result.returncode, 0, result.stderr)
        found = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "search",
                str(output / "search.sqlite3"),
                query,
                "--scope",
                "corpus",
                "--include-private",
                *options,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(found.returncode, 0, found.stderr)
        results = json.loads(found.stdout)["results"]
        self.assertEqual(len(results), 1)
        self.assertLessEqual(len(results[0]["excerpt"]), self.limit)
        return results[0]

    @staticmethod
    def shown(hit):
        start, end = hit["match_span_in_excerpt"]
        return hit["excerpt"][start:end]

    def rows(self, output):
        db = sqlite3.connect((output / "search.sqlite3").resolve().as_uri() + "?mode=ro", uri=True)
        try:
            return db.execute(
                "select id, sha256, representation, start_line, read_state, original, scope, path"
                " from docs order by start_line, representation"
            ).fetchall()
        finally:
            db.close()

    def test_local_import_keeps_supplied_bytes_and_hash(self):
        for name, raw in self.NEWLINES.items():
            with self.subTest(newline=name):
                result, output = self.build([self.entry(self.repo / (name + ".txt"))])
                self.assertEqual(result.returncode, 0, result.stderr)
                rows = self.rows(output)
                corpus = next(r for r in rows if r[6] == "corpus")
                tracked = next(r for r in rows if r[6] == "main" and r[7] == name + ".txt")
                expected = hashlib.sha256(raw).hexdigest()
                self.assertEqual(corpus[5].encode("utf-8"), raw)
                self.assertEqual(corpus[1], expected)
                self.assertEqual(tracked[1], expected)
                manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
                listed = [d["sha256"] for d in manifest["documents"] if d["scope"] == "corpus"]
                self.assertEqual(listed, [expected])

    def test_other_newlines_keep_line_anchor_and_original_characters(self):
        for name, raw in self.NEWLINES.items():
            with self.subTest(newline=name):
                text = raw.decode("utf-8")
                hit = self.hit(text, "needle")
                self.assertEqual(hit["line"], 2)
                self.assertEqual(hit["anchor_kind"], "matching_line")
                self.assertEqual(hit["excerpt"], text.rstrip("\r\n"))
                self.assertEqual(self.shown(hit), "needle")
                self.assertFalse(hit["excerpt_clipped"])

    def test_same_bytes_at_two_positions_are_two_records(self):
        source = self.source("needle repeated\n")
        result, output = self.build(
            [
                self.entry(source, start_line=line, representation="extracted_utf8")
                for line in (10, 100)
            ]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [r for r in self.rows(output) if r[6] == "corpus"]
        self.assertEqual(len({r[0] for r in rows}), 2)
        self.assertEqual([r[3] for r in rows], [10, 100])
        self.assertEqual(len({r[1] for r in rows}), 1)
        self.assertEqual({r[4] for r in rows}, {"MACHINE_INDEXED_NOT_SEMANTICALLY_READ"})
        scope = json.loads(result.stdout)["scopes"]["corpus"]
        self.assertEqual(scope["indexed_documents"], 2)
        self.assertEqual(scope["tokens"], 4)
        self.assertEqual(scope["unique_content_tokens"], 2)

    def test_same_bytes_in_two_representations_are_two_records(self):
        source = self.source("needle repeated\n")
        result, output = self.build(
            [
                self.entry(source, start_line=10, representation=name)
                for name in ("raw_utf8", "extracted_utf8")
            ]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [r for r in self.rows(output) if r[6] == "corpus"]
        self.assertEqual(len({r[0] for r in rows}), 2)
        self.assertEqual(sorted(r[2] for r in rows), ["extracted_utf8", "raw_utf8"])
        self.assertEqual({r[3] for r in rows}, {10})
        self.assertEqual(len({r[1] for r in rows}), 1)
        scope = json.loads(result.stdout)["scopes"]["corpus"]
        self.assertEqual(scope["tokens"], 4)
        self.assertEqual(scope["unique_content_tokens"], 2)

    def test_identical_record_and_unusable_start_line_are_rejected_with_reason(self):
        source = self.source("needle repeated\n")
        for entries, reason in [
            ([self.entry(source, start_line=10), self.entry(source, start_line="10")], "Duplicate"),
            ([self.entry(source, start_line="tenth")], "start_line is not a whole number"),
            ([self.entry(source, start_line=10.5)], "start_line is not a whole number"),
        ]:
            with self.subTest(reason=reason):
                result, _ = self.build(entries)
                self.assertEqual(result.returncode, 2)
                self.assertIn(reason, result.stderr)
                self.assertNotIn("UNIQUE constraint", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_undecodable_local_source_is_still_rejected_without_traceback(self):
        source = self.root / "not-utf8.txt"
        source.write_bytes(b"needle \xff\xfe\r\n")
        result, _ = self.build([self.entry(source)])
        self.assertEqual(result.returncode, 2)
        self.assertIn("corpus-search:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def search(self, output, query, *options):
        found = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "search",
                str(output / "search.sqlite3"),
                query,
                "--limit",
                "1000",
                *options,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(found.returncode, 0, found.stderr)
        return json.loads(found.stdout)["results"]

    def test_declared_visibility_survives_build_manifest_and_search(self):
        label = "PRIVATE_HANDOFF / nicht \u00f6ffentlich"
        entries = [
            self.entry(self.source("needle eins\n"), title="a.txt", visibility="private"),
            self.entry(self.source("needle zwei\n"), title="b.txt", visibility=label),
            self.entry(self.source("needle drei\n"), title="c.txt"),
        ]
        result, output = self.build(entries)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {"a.txt": "private", "b.txt": label, "c.txt": None}
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        listed = {
            d["path"]: d["visibility"] for d in manifest["documents"] if d["scope"] == "corpus"
        }
        self.assertEqual(listed, expected)
        hits = self.search(output, "needle", "--include-private")
        shown = {h["path"]: h["visibility"] for h in hits if h["scope"] == "corpus"}
        self.assertEqual(shown, expected)
        tracked = [h for h in self.search(output, "alpha") if h["scope"] == "main"]
        self.assertTrue(tracked)
        self.assertEqual({h["visibility"] for h in tracked}, {None})

    def test_unknown_corpus_field_fails_closed_and_names_only_the_field(self):
        source = self.source("needle\n")
        entry = self.entry(source, title="streng-vertraulicher-titel.txt", visiblity="geheimwert")
        result, _ = self.build([self.entry(self.source("needle\n"), title="ok.txt"), entry])
        self.assertEqual(result.returncode, 2)
        self.assertIn("visiblity", result.stderr)
        self.assertIn("entry 2", result.stderr)
        for protected in ("geheimwert", "streng-vertraulicher-titel", str(source)):
            self.assertNotIn(protected, result.stderr + result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_default_search_does_not_disclose_nonpublic_corpus_or_its_match_counts(self):
        entries = [
            self.entry(
                self.source("needle private-content-470\n"),
                title=f"private-title-{number}.txt",
                source_id=f"private-id-{number}",
                provenance_url=f"https://example.invalid/private-{number}",
                **({"visibility": label} if label is not None else {}),
            )
            for number, label in enumerate(
                (
                    "privat",
                    "private",
                    "PRIVATE_HANDOFF / nicht öffentlich",
                    "reduced",
                    "unknown",
                    None,
                )
            )
        ]
        result, output = self.build(entries)
        self.assertEqual(result.returncode, 0, result.stderr)
        for mode in ("literal", "tokens", "expanded"):
            with self.subTest(mode=mode):
                found = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "search",
                        str(output / "search.sqlite3"),
                        "needle",
                        "--mode",
                        mode,
                        "--limit",
                        "1",
                        "--scope",
                        "corpus",
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(found.returncode, 0, found.stderr)
                response = json.loads(found.stdout)
                self.assertEqual(response["results"], [])
                self.assertEqual(response["total_matching_documents_by_scope"], {})
                self.assertEqual(response["returned_documents"], 0)
                self.assertFalse(response["truncated"])
                for secret in ("private-content-470", "private-title", "private-id", "/private-"):
                    self.assertNotIn(secret, found.stdout + found.stderr)

    def test_only_explicit_public_corpus_is_shown_without_private_opt_in(self):
        entries = [
            self.entry(
                self.source("needle public\n"), title=f"public-{number}.txt", visibility=label
            )
            for number, label in enumerate(("public", "öffentlich", " PUBLIC "))
        ]
        entries.append(
            self.entry(self.source("needle private\n"), title="hidden.txt", visibility="privat")
        )
        result, output = self.build(entries)
        self.assertEqual(result.returncode, 0, result.stderr)
        hits = [h for h in self.search(output, "needle") if h["scope"] == "corpus"]
        self.assertEqual(
            {h["path"] for h in hits}, {"public-0.txt", "public-1.txt", "public-2.txt"}
        )
        self.assertEqual({h["visibility"] for h in hits}, {"public", "öffentlich", " PUBLIC "})

    def test_visibility_that_is_not_text_is_rejected(self):
        for value in (True, "", "   ", ["private"]):
            with self.subTest(value=value):
                result, _ = self.build([self.entry(self.source("needle\n"), visibility=value)])
                self.assertEqual(result.returncode, 2)
                self.assertIn("visibility", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_same_record_with_contradicting_visibility_is_not_merged(self):
        source = self.source("needle\n")
        result, _ = self.build(
            [self.entry(source, visibility="private"), self.entry(source, visibility="public")]
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Duplicate", result.stderr)

    def test_search_reads_an_index_built_before_the_visibility_column(self):
        result, output = self.build([self.entry(self.source("needle alt\n"))])
        self.assertEqual(result.returncode, 0, result.stderr)
        db = sqlite3.connect(output / "search.sqlite3")
        try:
            db.execute("alter table docs drop column visibility")
            db.commit()
        finally:
            db.close()
        default_hits = [h for h in self.search(output, "needle") if h["scope"] == "corpus"]
        self.assertEqual(default_hits, [])
        hits = [
            h for h in self.search(output, "needle", "--include-private") if h["scope"] == "corpus"
        ]
        self.assertEqual([h["visibility"] for h in hits], [None])

    def test_short_context_is_unchanged(self):
        hit = self.hit("before\nneedle: important context\nafter\nlater\nunseen\n", "needle")
        self.assertEqual(hit["line"], 2)
        self.assertEqual(hit["excerpt"], "before\nneedle: important context\nafter\nlater")
        self.assertEqual(hit["excerpt_match"], "complete")
        self.assertEqual(hit["match_span_in_excerpt"], [7, 13])
        self.assertFalse(hit["excerpt_clipped"])

    def test_long_preceding_line_does_not_displace_match(self):
        hit = self.hit("x" * 1900 + "\nneedle: important context\nafter\n", "needle")
        self.assertEqual(hit["line"], 2)
        self.assertEqual(hit["anchor_kind"], "matching_line")
        self.assertEqual(self.shown(hit), "needle")
        self.assertIn("needle: important context\nafter", hit["excerpt"])
        self.assertEqual(hit["excerpt_match"], "complete")
        self.assertTrue(hit["excerpt_clipped"])

    def test_late_match_on_long_line_stays_visible_in_every_mode(self):
        late = "x" * 1900 + " needle: important context\n"
        combined = "x" * 1900 + " Gru\u0308neisen Stra\u00dfe\n"
        for text, query, mode, original in [
            (late, "needle", "literal", "needle"),
            (late, "needle", "tokens", "needle"),
            (late, "needle", "expanded", "needle"),
            (combined, "Gr\u00fcneisen", "expanded", "Gru\u0308neisen"),
            (combined, "gr\u00fcneisen", "tokens", "Gru\u0308neisen"),
        ]:
            with self.subTest(query=query, mode=mode):
                hit = self.hit(text, query, "--mode", mode)
                self.assertEqual(hit["line"], 1)
                self.assertEqual(hit["anchor_kind"], "matching_line")
                self.assertEqual(self.shown(hit), original)
                self.assertEqual(hit["excerpt_match"], "complete")
                self.assertTrue(hit["excerpt_clipped"])

    def test_folded_queries_show_original_spelling_and_position(self):
        pad = "\u00e4\u00df " * 700
        for text, query, original in [
            (pad + "Stra\u00dfe am Ende\n", "strasse", "Stra\u00dfe"),
            (pad + "STRASSE am Ende\n", "stra\u00dfe", "STRASSE"),
            (pad + "Stra\u00dfe am Ende\n", "sse a", "\u00dfe a"),
            (pad + "Gru\u0308neisen am Ende\n", "GR\u00dcNEISEN", "Gru\u0308neisen"),
            (pad + "Gr\u00fcneisen am Ende\n", "gru\u0308neisen", "Gr\u00fcneisen"),
        ]:
            with self.subTest(query=query):
                hit = self.hit(text, query)
                self.assertEqual(hit["line"], 1)
                self.assertEqual(self.shown(hit), original)
                end = hit["match_span_in_excerpt"][1]
                self.assertTrue(hit["excerpt"].endswith("m Ende"))
                self.assertIn(hit["excerpt"][end:], (" am Ende", "m Ende"))
                self.assertEqual(hit["excerpt_match"], "complete")

    def test_token_span_follows_token_rule_not_substring(self):
        hit = self.hit("master " * 400 + "Mast 2 und 2 position\n", "Mast", "--mode", "tokens")
        start, end = hit["match_span_in_excerpt"]
        self.assertEqual(hit["excerpt"][start:end], "Mast")
        self.assertEqual(hit["excerpt"][start - 1 : end + 2], " Mast 2")
        doubled = self.hit("master " * 400 + "Mast 2 und 2 position\n", "2 2", "--mode", "tokens")
        self.assertEqual(self.shown(doubled), "2 und 2")
        self.assertEqual(doubled["matched_tokens"], ["2", "2"])

    def test_match_longer_than_excerpt_is_marked_partial(self):
        spread = "lead " * 50 + "alpha " + "x" * 3000 + " omega tail\n"
        phrase = "y" * 2000
        for text, query, mode, opening in [
            (spread, "omega alpha", "tokens", "alpha "),
            ("lead " * 50 + phrase + " tail\n", phrase, "literal", "y"),
        ]:
            with self.subTest(mode=mode):
                hit = self.hit(text, query, "--mode", mode)
                self.assertEqual(hit["anchor_kind"], "matching_line")
                self.assertEqual(hit["excerpt_match"], "partial_match_exceeds_excerpt")
                self.assertEqual(hit["match_span_in_excerpt"], [0, self.limit])
                self.assertEqual(len(hit["excerpt"]), self.limit)
                self.assertTrue(hit["excerpt"].startswith(opening))
                self.assertTrue(hit["excerpt_clipped"])

    def test_scattered_tokens_keep_document_anchor(self):
        result, output = self.build(
            [self.entry(self.source("alpha\nfiller\nfiller\nfiller\nomega\n"), start_line=40)]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        found = json.loads(
            subprocess.check_output(
                [
                    sys.executable,
                    str(SCRIPT),
                    "search",
                    str(output / "search.sqlite3"),
                    "alpha omega",
                    "--mode",
                    "tokens",
                    "--scope",
                    "corpus",
                    "--include-private",
                ]
            )
        )["results"][0]
        self.assertEqual(found["anchor_kind"], "document_level_tokens_or_multiline")
        self.assertEqual(found["line"], 40)
        self.assertEqual(found["excerpt_match"], "not_located_document_level")
        self.assertIsNone(found["match_span_in_excerpt"])
        self.assertEqual(found["excerpt"], "alpha\nfiller\nfiller")

    def test_clipped_edges_keep_base_letter_and_combining_mark_together(self):
        pair = "u\u0308"
        hit = self.hit(pair * 1500 + " needle " + pair * 1500 + "\n", "needle")
        self.assertEqual(self.shown(hit), "needle")
        self.assertTrue(hit["excerpt_clipped"])
        self.assertFalse(unicodedata.combining(hit["excerpt"][0]))
        self.assertTrue(unicodedata.combining(hit["excerpt"][-1]))

    def test_span_mapping_checks_itself_against_the_original(self):
        span = self.module.original_span
        norm = self.module.norm
        for text, needle, original in [
            ("x\u1100\u1161\u11a8y", "\uac01", "\u1100\u1161\u11a8"),
            ("l\u0304\u0323 Stra\u00dfe", "sse", "\u00dfe"),
            ("\u0130stanbul \u00dcber", "\u00fcber", "\u00dcber"),
        ]:
            with self.subTest(text=text):
                folded = norm(text)
                position = folded.find(norm(needle))
                self.assertGreaterEqual(position, 0)
                first, last = span(text, position, position + len(norm(needle)), norm)
                self.assertEqual(text[first:last], original)
                self.assertIn(norm(needle), norm(text[first:last]))

    def test_token_excerpt_contains_every_wanted_token(self):
        text = "x" * 1900 + " zweites Gru\u0308neisen-Ma\u00df dann erstes Wort\n"
        hit = self.hit(text, "erstes zweites", "--mode", "tokens")
        present = collections.Counter(self.module.tokens(self.shown(hit)))
        self.assertGreaterEqual(present["erstes"], 1)
        self.assertGreaterEqual(present["zweites"], 1)
        self.assertEqual(self.shown(hit), "zweites Gru\u0308neisen-Ma\u00df dann erstes")


if __name__ == "__main__":
    unittest.main()
