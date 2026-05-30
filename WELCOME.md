# Welcome to entaENGELment

entaENGELment is an experimental consent-first framework for auditable, human-guided multi-agent workflows.

It combines three layers:

1. **Governance**
   Clear boundaries, consent checks, evidence trails, and review gates.

2. **Verification**
   Repeatable commands such as `make verify`, pointer validation, claim linting, tests, and receipts.

3. **Exploration**
   A symbolic and conceptual research space for resonance, membranes, voids, and multi-agent coordination.

This repository is not production-ready software. It is a research and governance framework in active formation.

This guide is intentionally lightweight. Authoritative rules remain in `README.md`, `CLAUDE.md`, policies, tests, and CI gates.

## Start here

For a fast technical check:

```bash
git clone https://github.com/fleksible/entaENGELment-.git
cd entaENGELment-
make install-dev
make verify
```

For the optional UI:

```bash
cd ui-app
npm ci
npm run dev
```

Then open:

```text
http://localhost:3000
```

## What matters most

The project follows a simple rule:

> No claim without status.
> No merge without verification.
> No resonance without boundary.

Important terms:

- **VOIDMAP** tracks open gaps, risks, and unresolved system questions.
- **DeepJump** describes the verify -> status -> snapshot workflow.
- **Receipts** document evidence and state transitions.
- **Guards G0-G6** define consent, focus, boundary, and merge discipline.
- **ANNEX vs GOLD** separates changeable work zones from protected canonical material.

## What this project is not

entaENGELment is not:

- a finished product,
- a general-purpose framework,
- a production security system,
- an empirical proof of its symbolic models,
- or a claim that metaphor equals evidence.

Symbolic language is allowed here, but it must not replace verification.

## Recommended paths

If you are a developer, start with:

- `README.md`
- `Makefile`
- `tests/`
- `tools/`

If you are reviewing governance, start with:

- `CLAUDE.md`
- `policies/`
- `VOIDMAP.yml`
- `docs/guards/`

If you are exploring the conceptual layer, start with:

- `REPOSITORY_ESSENZ_ANALYSE.md`
- `docs/`
- `index/`
- `spec/`

## Contribution style

Small, focused pull requests are preferred.

Good PRs usually do one thing:

- fix a typo,
- add a test,
- clarify a claim,
- update one dependency,
- close one VOID with evidence,
- or improve one documented workflow.

When unsure, choose the smaller change.
