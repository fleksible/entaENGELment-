# VOIDMAP Metadata Update Policy

Status: Draft governance policy  
Scope: `VOIDMAP.yml` metadata discipline only  
Related: #180

## Purpose

`VOIDMAP.yml` is the source of truth for tracked gaps in the repository. Its
`metadata.last_updated` field should reflect meaningful changes to the VOID
registry, not every incidental formatting or generated-document change.

This policy defines when `metadata.last_updated` must change, when it should
not change, and how generated artifacts such as `docs/voids_backlog.md` relate
to the source file.

## Source and Generated Artifacts

- `VOIDMAP.yml` is the canonical source.
- `metadata.generated_doc` may point to a generated Markdown view, currently
  `docs/voids_backlog.md`.
- Generated documents are derived artifacts. Regenerating them does not, by
  itself, change the semantic state of `VOIDMAP.yml`.

## Required `last_updated` Changes

Update `metadata.last_updated` when any semantic state in `VOIDMAP.yml` changes.
This includes:

- adding or removing a VOID entry;
- changing a VOID `status`, including `OPEN`, `IN_PROGRESS`, `SUSPENDED`, or
  `CLOSED`;
- changing `priority`, `owner`, `target_date`, `domain`, `symptom`,
  `closing_path`, `evidence`, `created`, `closed`, or `notes` in a way that
  changes the meaning of the entry;
- changing top-level metadata that affects generated artifacts or canonical
  interpretation, such as `metadata.generated_doc`;
- changing the allowed status vocabulary or template semantics in the file
  header in a way that affects how future VOIDs should be interpreted.

## Non-Required `last_updated` Changes

Do not update `metadata.last_updated` for changes that do not alter the
semantic state of the VOID registry, such as:

- whitespace-only edits;
- line wrapping or formatting-only edits;
- comment-only edits that do not change the allowed vocabulary or template
  semantics;
- regenerating `docs/voids_backlog.md` from an unchanged `VOIDMAP.yml`;
- changing generated artifacts that merely reflect an already-current
  `VOIDMAP.yml` state.

## Generated Backlog Rule

When `VOIDMAP.yml` changes semantically, regenerate the backlog view with:

```bash
python3 tools/voids_backlog_gen.py
```

or check it with:

```bash
python3 tools/voids_backlog_gen.py --check
```

The generated file should reflect the source state. It must not become a second
source of truth.

## Review Guidance

Reviewers should treat a changed `metadata.last_updated` field as evidence that
semantic VOIDMAP state changed. If the date changes without a semantic change,
request clarification or revert the metadata change.

Conversely, if a semantic VOIDMAP change occurs without updating
`metadata.last_updated`, request that the metadata be updated in the same PR.

## Non-Goals

This policy does not:

- define release readiness;
- create or close VOIDs;
- change `VOIDMAP.yml` directly;
- wire backlog generation into `make verify` or CI;
- alter GOLD/ANNEX/IMMUTABLE path rules.
