#!/usr/bin/env python3
"""[FACT] Lesender, quellgebundener Stichwortindex mit Python-Standardbibliothek.

[RISK] Lokal hinzugefügte Korpora und Suchindizes können private Originaltexte
enthalten. Nur explizit ausgewählte öffentliche Artefakte veröffentlichen.
Vertrag: docs/annex/CORPUS_SEARCH_v0_1.md.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import pathlib
import re
import sqlite3
import subprocess
import unicodedata
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

TOKEN_RE = re.compile(
    r"\d+\s*[×x]\s*\d+(?:\s*\+\s*\d+\s*[×x]\s*[nN])?|[^\W_]+(?:[_'’\-][^\W_]+)*", re.UNICODE
)
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".rst",
    ".json",
    ".jsonl",
    ".yml",
    ".yaml",
    ".toml",
    ".py",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".css",
    ".html",
    ".htm",
    ".csv",
    ".tsv",
    ".sh",
    ".svg",
    ".xml",
    ".ini",
    ".cfg",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".sql",
    ".uplugin",
    ".patch",
    ".cron",
}
LOCK_NAMES = {
    "uv.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "requirements-dev.txt",
    "poetry.lock",
}
SOURCE_SUFFIXES = {
    ".py",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".css",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".sql",
}
MAX_BYTES = 4 * 1024 * 1024


def norm(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def tokens(text: str) -> list[str]:
    return [norm(m.group()) for m in TOKEN_RE.finditer(unicodedata.normalize("NFC", text))]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: pathlib.Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def resolve(repo: pathlib.Path, ref: str) -> str:
    return (
        git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()
    )


def role_for(path: str) -> str:
    p = pathlib.PurePosixPath(path)
    if path.startswith(("docs/intake/raw/", "INBOX/")):
        return "imported_snapshot"
    if path.startswith(("docs/audit/", "OUT/")):
        return "generated_review"
    if p.suffix.lower() in SOURCE_SUFFIXES:
        return "code"
    if p.suffix.lower() in {".md", ".rst", ".txt", ".html", ".htm"}:
        return "document"
    return "configuration"


def declared_status(text: str) -> list[dict[str, object]]:
    pattern = re.compile(
        r"^\s*(?:\*\*)?(?:Status|Authority|Anbindung|Promotion-Effect)(?:\*\*)?\s*:(?:\*\*)?[^\n]{0,220}",
        re.I,
    )
    return [
        {"line": i, "declaration": line.strip()}
        for i, line in enumerate(text.splitlines(), 1)
        if pattern.match(line)
    ]


def object_files(
    repo: pathlib.Path, ref: str, selected: set[str] | None = None
) -> Iterator[tuple[str, str | None, str | None]]:
    entries = []
    for item in git(repo, "ls-tree", "-r", "-z", "-l", ref).split(b"\0"):
        if not item:
            continue
        info, name = item.split(b"\t", 1)
        mode, kind, oid, tree_size = info.decode().split()
        path = name.decode("utf-8")
        if selected is None or path in selected:
            entries.append((mode, kind, oid, path, tree_size))
    process = subprocess.Popen(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    writer, reader = process.stdin, process.stdout
    if writer is None or reader is None:
        raise RuntimeError("Git batch pipes are unavailable.")
    try:
        for mode, kind, oid, path, raw_size in entries:
            if mode != "100644" and mode != "100755":
                yield path, None, "symlink_or_nonregular"
                continue
            if pathlib.PurePosixPath(path).name in LOCK_NAMES:
                yield path, None, "dependency_lock_or_generated_requirements"
                continue
            p = pathlib.PurePosixPath(path)
            if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in {
                "Makefile",
                "Dockerfile",
                "LICENSE",
                "NOTICE",
                "CODEOWNERS",
                ".gitignore",
                "pre-commit",
            }:
                yield path, None, "unsupported_extension"
                continue
            if kind != "blob":
                yield path, None, "non_blob"
                continue
            if int(raw_size) > MAX_BYTES:
                yield path, None, "size_limit"
                continue
            writer.write((oid + "\n").encode())
            writer.flush()
            header = reader.readline().split()
            size = int(header[2])
            content = reader.read(size)
            reader.read(1)
            if b"\0" in content:
                yield path, None, "binary"
            else:
                try:
                    yield path, content.decode("utf-8"), None
                except UnicodeDecodeError:
                    yield path, None, "non_utf8"
    finally:
        writer.close()
        process.wait()


def create_db(path: pathlib.Path) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.executescript("""
    CREATE TABLE docs(id TEXT PRIMARY KEY, scope TEXT, ref TEXT, path TEXT,
      sha256 TEXT, source_id TEXT, family TEXT, role TEXT, representation TEXT,
      start_line INTEGER, read_state TEXT, status TEXT, provenance_url TEXT,
      original TEXT, normalized TEXT, token_count INTEGER);
    CREATE TABLE terms(scope TEXT, role TEXT, term TEXT, occurrences INTEGER,
      documents INTEGER, unique_content_occurrences INTEGER);
    CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
    CREATE INDEX docs_scope ON docs(scope);
    CREATE INDEX terms_key ON terms(scope,term);
    """)
    return db


def build(args: argparse.Namespace) -> None:
    out = pathlib.Path(args.out).resolve()
    repo = pathlib.Path(args.repo).resolve()
    if out == repo or repo in out.parents:
        raise ValueError("Output must be outside the source repository.")
    if out.exists() and any(out.iterdir()):
        raise ValueError("Output directory must be new or empty; existing files are preserved.")
    out.mkdir(parents=True, exist_ok=True)
    if (out / "search.sqlite3").exists():
        raise ValueError("Use a new output directory; existing index is preserved.")
    base = resolve(repo, args.ref)
    try:
        remote = git(repo, "config", "--get", "remote.origin.url").decode().strip()
    except subprocess.CalledProcessError:
        remote = ""
    identity = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:)([^/\s]+)/([^/\s]+?)(?:\.git)?", remote
    )
    repository_url = ("https://github.com/" + identity[1] + "/" + identity[2]) if identity else None
    aliases = json.loads(pathlib.Path(args.aliases).read_text()) if args.aliases else {"groups": []}
    manifest: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_sha": base,
        "repository_url": repository_url,
        "repository_full_name": (identity[1] + "/" + identity[2]) if identity else None,
        "scope": [],
        "exclusions": [],
        "documents": [],
        "token_rule": TOKEN_RE.pattern,
        "normalization": "NFC + casefold; original retained",
        "interpretation": "lexical tokens, not linguistic word segmentation or evidence weight",
        "overlay_rule": "full changed files versus merge-base, not additive PR word counts",
        "validation": "NOT_ASSESSED; indexing is not semantic reading",
    }
    db = create_db(out / "search.sqlite3")
    counts: collections.defaultdict[tuple[str, str], collections.Counter[str]] = (
        collections.defaultdict(collections.Counter)
    )
    df: collections.defaultdict[tuple[str, str], collections.Counter[str]] = (
        collections.defaultdict(collections.Counter)
    )
    unique: collections.defaultdict[tuple[str, str], collections.Counter[str]] = (
        collections.defaultdict(collections.Counter)
    )
    seen_hash: collections.defaultdict[tuple[str, str], set[str]] = collections.defaultdict(set)
    scope_docs: collections.Counter[str] = collections.Counter()
    scope_tokens: collections.Counter[str] = collections.Counter()
    scope_unique: collections.Counter[str] = collections.Counter()
    seen_scope: collections.defaultdict[str, set[str]] = collections.defaultdict(set)

    def add(scope, ref, path, text, metadata=None):
        m = metadata or {}
        digest = sha(text.encode())
        role = m.get("source_kind") or role_for(path)
        family = m.get("source_family") or "UNKNOWN"
        all_tokens = tokens(text)
        key = (scope, role)
        counts[key].update(all_tokens)
        df[key].update(set(all_tokens))
        if digest not in seen_hash[key]:
            unique[key].update(all_tokens)
            seen_hash[key].add(digest)
        scope_docs[scope] += 1
        scope_tokens[scope] += len(all_tokens)
        if digest not in seen_scope[scope]:
            scope_unique[scope] += len(all_tokens)
            seen_scope[scope].add(digest)
        record = {
            "id": sha(
                (
                    scope
                    + "\0"
                    + str(ref)
                    + "\0"
                    + str(m.get("source_id") or path)
                    + "\0"
                    + path
                    + "\0"
                    + digest
                ).encode()
            )[:24],
            "scope": scope,
            "ref": ref,
            "path": path,
            "sha256": digest,
            "source_id": m.get("source_id") or path,
            "family": family,
            "role": role,
            "representation": m.get("representation") or "tracked_raw_utf8",
            "start_line": m.get("start_line") or 1,
            "read_state": m.get("read_state") or "MACHINE_INDEXED_NOT_SEMANTICALLY_READ",
            "status": m.get("claim_status") or declared_status(text) or ["UNKNOWN"],
            "provenance_url": m.get("provenance_url")
            or (
                repository_url + "/blob/" + ref + "/" + quote(path, safe="/")
                if scope != "corpus" and repository_url
                else None
            ),
            "token_count": len(all_tokens),
        }
        # Never infer canonical status, tested behavior, or independence from role/path.
        db.execute(
            "INSERT INTO docs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                record["id"],
                scope,
                ref,
                path,
                digest,
                record["source_id"],
                family,
                role,
                record["representation"],
                record["start_line"],
                record["read_state"],
                json.dumps(record["status"], ensure_ascii=False),
                record["provenance_url"],
                text,
                norm(text),
                len(all_tokens),
            ),
        )
        manifest["documents"].append(record)

    snapshots: list[tuple[str, str, set[str] | None]] = [("main", base, None)]
    for overlay in args.overlay:
        name, ref = overlay.split("=", 1)
        if name in {"main", "corpus"} or any(x[0] == name for x in snapshots):
            raise ValueError("Overlay names must be distinct from main/corpus and each other.")
        head = resolve(repo, ref)
        ancestor = git(repo, "merge-base", base, head).decode().strip()
        changed = set(
            git(
                repo,
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "--no-renames",
                "--name-only",
                "-z",
                "--diff-filter=ACMT",
                ancestor,
                head,
            )
            .decode()
            .split("\0")
        ) - {""}
        deleted = (
            git(
                repo,
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "--no-renames",
                "--name-only",
                "-z",
                "--diff-filter=D",
                ancestor,
                head,
            )
            .decode()
            .split("\0")
        )
        manifest["scope"].append(
            {
                "scope": name,
                "ref": head,
                "merge_base": ancestor,
                "deleted_paths": [x for x in deleted if x],
                "semantics": "proposal; full changed files",
            }
        )
        snapshots.append((name, head, changed))
    manifest["scope"].insert(0, {"scope": "main", "ref": base, "semantics": "tracked snapshot"})
    for scope, ref, selected in snapshots:
        for path, text, error in object_files(repo, ref, selected):
            if error:
                manifest["exclusions"].append(
                    {"scope": scope, "ref": ref, "path": path, "reason": error}
                )
            else:
                add(scope, ref, path, text)

    if args.corpus:
        for item in json.loads(pathlib.Path(args.corpus).read_text()):
            if item.get("source_kind") == "generated_index":
                manifest["exclusions"].append(
                    {
                        "scope": "corpus",
                        "path": item["title"],
                        "reason": "generated_index_control_not_evidence",
                    }
                )
                continue
            p = pathlib.Path(item["local_path"])
            text = p.read_text(encoding="utf-8")
            add("corpus", item.get("source_version"), item["title"], text, item)
        manifest["scope"].append(
            {
                "scope": "corpus",
                "semantics": "selected supplied text representations; bounded coverage",
            }
        )

    with (out / "word-frequency.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["scope", "role", "token", "occurrences", "documents", "unique_content_occurrences"]
        )
        for key in sorted(counts):
            for term, n in counts[key].most_common():
                row = (key[0], key[1], term, n, df[key][term], unique[key][term])
                writer.writerow(row)
                db.execute("INSERT INTO terms VALUES (?,?,?,?,?,?)", row)
    stats = {
        "scopes": {
            s: {
                "indexed_documents": scope_docs[s],
                "tokens": scope_tokens[s],
                "unique_content_tokens": scope_unique[s],
            }
            for s in sorted(scope_docs)
        },
        "segments": [
            {"scope": k[0], "role": k[1], "tokens": sum(v.values()), "unique_tokens": len(v)}
            for k, v in sorted(counts.items())
        ],
        "excluded": dict(collections.Counter(x["reason"] for x in manifest["exclusions"])),
    }
    for name, value in [("manifest", manifest), ("statistics", stats), ("aliases", aliases)]:
        (out / (name + ".json")).write_text(
            json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        db.execute("INSERT INTO meta VALUES (?,?)", (name, json.dumps(value, ensure_ascii=False)))
    db.commit()
    db.close()
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def search(args: argparse.Namespace) -> None:
    path = pathlib.Path(args.database).resolve()
    # SQLite URI read-only protects the index from accidental query writes.
    db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    aliases = json.loads(db.execute("SELECT value FROM meta WHERE key='aliases'").fetchone()[0])
    q = norm(args.query)
    variants = [(args.query, "original")]
    groups = []
    for group in aliases.get("groups", []):
        if q in [norm(x) for x in [group["key"]] + group["spellings"] + group["related"]]:
            groups.append(group)
    if args.mode == "expanded":
        for group in groups:
            # A related term must not silently expand to all the group's spellings.
            if q == norm(group["key"]) or q in [norm(x) for x in group["spellings"]]:
                variants.extend((v, "spelling_variant") for v in group["spellings"])
            if args.related:
                variants.extend(
                    (v, "related_not_equivalent") for v in group["related"] + group["spellings"]
                )
    variants = list({norm(v): (v, rel) for v, rel in reversed(variants)}.values())
    matches = []
    totals: collections.Counter[str] = collections.Counter()
    wanted = collections.Counter(tokens(args.query))
    for row in db.execute("SELECT * FROM docs ORDER BY scope,role,path"):
        if args.scope and row["scope"] not in args.scope:
            continue
        if args.mode == "tokens":
            present = collections.Counter(tokens(row["original"]))
            found = (
                [args.query] if wanted and all(present[t] >= n for t, n in wanted.items()) else []
            )
        else:
            found = [v for v, _ in variants if norm(v) in row["normalized"]]
        if not found:
            continue
        lines = row["original"].splitlines()
        if args.mode == "tokens":
            hit_lines = [
                i
                for i, line in enumerate(lines)
                if all(collections.Counter(tokens(line))[t] >= n for t, n in wanted.items())
            ]
        else:
            hit_lines = [
                i for i, line in enumerate(lines) if any(norm(v) in norm(line) for v in found)
            ]
        if not hit_lines:
            # Multiline phrase or token matches get an explicit document anchor.
            i = 0
        else:
            i = hit_lines[0]
        totals[row["scope"]] += 1
        record = {
            k: row[k]
            for k in (
                "scope",
                "ref",
                "path",
                "source_id",
                "family",
                "role",
                "representation",
                "read_state",
                "provenance_url",
            )
        }
        record.update(
            {
                "declared_status": json.loads(row["status"]),
                "status_scope": "verbatim source declarations; nested records are not whole-document status",
                "matched_variants": found if args.mode != "tokens" else [],
                "matched_tokens": list(wanted.elements()) if args.mode == "tokens" else [],
                "line": row["start_line"] + i,
                "excerpt": "\n".join(lines[max(0, i - 1) : i + 3])[:1800],
                "anchor_kind": (
                    "matching_line" if hit_lines else "document_level_tokens_or_multiline"
                ),
            }
        )
        matches.append(record)
    output = {
        "query": args.query,
        "mode": args.mode,
        "expanded_terms": variants,
        "related_expansion": args.related,
        "total_matching_documents_by_scope": totals,
        "returned_documents": min(len(matches), args.limit),
        "truncated": len(matches) > args.limit,
        "limits": "bounded indexed corpus; lexical match does not establish meaning, truth, chronology or independent evidence",
        "groups": [
            {"key": g["key"], "guard": g["guard"], "suggested_related_terms": g["related"]}
            for g in groups
        ],
        "results": matches[: args.limit],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("build")
    p.add_argument("--repo", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--overlay", action="append", default=[])
    p.add_argument("--corpus")
    p.add_argument("--aliases")
    p.add_argument("--out", required=True)
    p.set_defaults(func=build)
    p = sub.add_parser("search")
    p.add_argument("database")
    p.add_argument("query")
    p.add_argument("--mode", choices=["literal", "expanded", "tokens"], default="literal")
    p.add_argument("--related", action="store_true")
    p.add_argument("--scope", action="append")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=search)
    args = parser.parse_args()
    if getattr(args, "query", None) is not None and not args.query.strip():
        parser.error("Query must contain non-whitespace text.")
    if getattr(args, "limit", 1) < 1:
        parser.error("--limit must be positive.")
    if getattr(args, "related", False) and args.mode != "expanded":
        parser.error("--related requires --mode expanded")
    if getattr(args, "mode", None) == "tokens":
        remainder = TOKEN_RE.sub("", unicodedata.normalize("NFC", args.query))
        if remainder.strip():
            parser.error("Token mode would discard query symbols. Use literal or expanded mode.")
    try:
        args.func(args)
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as error:
        parser.exit(2, f"corpus-search: {error}\n")


if __name__ == "__main__":
    main()
