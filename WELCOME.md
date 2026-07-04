# Welcome to entaENGELment

entaENGELment is an experimental consent-first, audit-first and anti-capture framework for human-guided, verifiable and mythopoetic systems.

It is not a finished product, not a production security system, and not empirical proof of its symbolic models.

It is also not intended to become a surveillance engine, semantic profiling tool, hidden personalization loop, or enterprise lock-in architecture.

This repository is a research and governance framework in active formation. This welcome file is a gentle orientation; authoritative rules remain in `README.md`, `CLAUDE.md`, policies, tests, schemas and CI gates.

---

## Core layers

1. **Governance**  
   Consent, boundaries, review gates, claim-status discipline and anti-overclaim rules.

2. **Verification**  
   Repeatable checks such as `make verify`, pointer validation, claim linting, tests, receipts and ledger-integrity checks where implemented.

3. **Gläserne Agora & Receipt-Ledger**  
   A user-sovereign claim space. The system must not define meaning for the user. Claims should be added with visible status, origin, membrane context and revision/fork paths. Where implemented, the Receipt-Ledger is append-only and tamper-evident rather than silently overwritable.

4. **Essence Architecture**  
   Public symbolic and image-generation grammar: schemas, prompt modules, visual operators, policy gates and tests. This layer may be open and auditable without receiving private user data.

5. **Commons & Anti-Capture**  
   The project supports open development while resisting extractive capture: surveillance, profiling, hidden personalization, private-user-data extraction and lock-in.

6. **Exploration**  
   A symbolic and conceptual research space for resonance, membranes, voids, tesser3TAKT, Grimm Narration 2.0 and multi-agent coordination.

---

## Start here

For a fast technical check:

```bash
git clone https://github.com/fleksible/entaENGELment-.git
cd entaENGELment-
make install-dev
make verify
```

For the optional UI / lab interface:

```bash
corepack enable
pnpm install --frozen-lockfile
pnpm --filter entaengelment-ui dev
```

Then open:

```text
http://localhost:3000
```

---

## What matters most

> No claim without status.  
> No handover without receipt.  
> No merge without verification.  
> No resonance without boundary.  
> No GitHub without privacy reduction.  
> No open architecture without anti-capture guard.

Important terms:

- **User-Claim** means the claim belongs to the user, not to the system.
- **Gläserne Agora** is the user-facing claim space where meanings may be added, forked, revised or withdrawn without silently overwriting prior claims.
- **Receipt-Ledger** stores claim events without treating any single entry as the final definition.
- **verifyLedger** is the intended integrity check for hash-chain, structure and references where the ledger implementation exists.
- **materialPointers** may show which active lab materials shaped a claim, without turning those materials into authority or evidence by default.
- **VOIDMAP** tracks open gaps, risks and unresolved system questions.
- **DeepJump** describes the verify -> status -> snapshot workflow.
- **Receipts** document evidence, state transitions or claim events, depending on module context.
- **Guards G0-G6** define consent, focus, boundary and merge discipline.
- **ANNEX vs GOLD** separates changeable work zones from protected canonical material.

---

## GitHub Use Policy

GitHub is used as a public development, documentation and witness layer. It may contain public code, documentation, schemas, tests, visual grammar modules, prompt-compiler logic and reduced integrity anchors.

GitHub must not become a semantic generator of private user data.

Allowed in GitHub:

- public source code
- public schemas
- public tests
- public governance documents
- public essence/image architecture
- prompt-compiler logic without private user data
- reduced hash or snapshot manifests
- documentation and audit notes

Not allowed in GitHub by default:

- private raw User-Claims
- private user images
- personal symbolic profiles
- embeddings of private content
- inferred psychological profiles
- private ledger exports
- hidden personalization loops
- generated prompt seeds derived from private user data

Core rule:

> GitHub may witness integrity, but must not become a semantic generator of private user data.

See also: [`GITHUB_USE_POLICY.md`](GITHUB_USE_POLICY.md) and [`PRIVACY_BOUNDARY.md`](PRIVACY_BOUNDARY.md).

---

## Anti-Capture Position

Commercial use and extractive capture are not identical. The project is primarily concerned with capture, surveillance, profiling, hidden personalization, semantic extraction and lock-in.

entaENGELment should not be used to support extractive personalization, behavioral manipulation, semantic profiling, enterprise lock-in or the conversion of private meaning into commercial advantage.

This is a governance position. Legal enforceability depends on the actual project license, contribution rules, hosted-service terms and separate policy documents.

Current license review is required before claiming that anti-capture obligations are legally enforceable.

See also: [`ANTI_CAPTURE_POLICY.md`](ANTI_CAPTURE_POLICY.md) and [`LICENSE_REVIEW.md`](LICENSE_REVIEW.md).

---

## What this project is not

entaENGELment is not:

- a finished product,
- a general-purpose framework,
- a production security system,
- an empirical proof of its symbolic models,
- a claim that metaphor equals evidence,
- a startup funnel,
- a surveillance engine,
- a private-user-data extraction pipeline,
- a semantic profiling tool,
- an enterprise lock-in architecture,
- or a system for turning user meaning into hidden personalization loops.

Symbolic language is allowed here, but it must not replace verification.

---

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
- `GITHUB_USE_POLICY.md`
- `ANTI_CAPTURE_POLICY.md`
- `PRIVACY_BOUNDARY.md`
- `LICENSE_REVIEW.md`

If you are reviewing the claim-space architecture, look for:

- the Gläserne Agora UI
- the Receipt-Ledger implementation
- ledger-integrity checks such as `verifyLedger`
- Governance Cockpit / Ledger Integrity Block
- JSONL export/import logic

If a path does not exist yet, open a small PR or VOID instead of inventing structure silently.

If you are exploring the conceptual layer, start with:

- `REPOSITORY_ESSENZ_ANALYSE.md`
- `docs/`
- `index/`
- `spec/`

---

## Contribution style

Small, focused pull requests are preferred.

Good PRs usually do one thing:

- fix a typo,
- add a test,
- clarify a claim,
- improve privacy boundaries,
- improve anti-overclaim wording,
- update one dependency,
- close one VOID with evidence,
- improve one documented workflow,
- strengthen GitHub witness-only separation,
- improve UI accessibility,
- improve schema validation,
- or improve import/export safety.

PRs must not:

- upload private User-Claims to GitHub,
- add telemetry for private claims,
- create hidden personalization from private ledger data,
- remove claim-status visibility,
- mutate old receipts,
- weaken ledger-integrity checks without explicit review,
- turn analogy into evidence,
- or turn GitHub into a user-data feedback loop.

When unsure, choose the smaller change.
