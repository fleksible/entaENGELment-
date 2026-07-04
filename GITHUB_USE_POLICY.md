# GitHub Use Policy

GitHub is a public development, documentation and witness layer for entaENGELment.

It may hold the public essence architecture of the project. It must not become a semantic generator of private user data.

---

## Claim status

This document is a governance policy draft. It is not legal advice and does not replace the repository license, contribution rules or hosted-service terms.

---

## Core rule

> GitHub may witness integrity, but must not become a semantic generator of private user data.

In project language:

> GitHub may hold the public Lyra. It must not record the private heartbeat.

---

## Allowed by default

GitHub may contain:

- public source code
- public documentation
- public schemas
- public tests
- public governance documents
- public essence/image architecture
- prompt-compiler logic without private user data
- visual grammar modules
- reduced hash or snapshot manifests
- public audit notes
- policy hashes and reduced integrity anchors

---

## Not allowed by default

GitHub must not receive by default:

- private raw User-Claims
- private user images
- private generated outputs
- personal symbolic profiles
- embeddings of private content
- inferred psychological profiles
- private ledger exports
- hidden personalization loops
- generated prompt seeds derived from private user data
- private material labels that reveal sensitive user context

Private material may only be published after explicit, informed and reversible user action where technically possible.

---

## Witness-only anchor payload

A GitHub anchor payload should be reduced and non-reconstructive.

Allowed fields include:

```json
{
  "schemaVersion": "receipt-anchor.v0.1",
  "snapshotRootHash": "sha256:...",
  "entryCount": 0,
  "createdAt": "2026-01-01T00:00:00.000Z",
  "previousSnapshotHash": "sha256:...",
  "policyHash": "sha256:...",
  "visibility": "public-anchor"
}
```

The anchor proves only that a reduced ledger state was witnessed. It does not prove the truth of claims.

---

## Forbidden feedback loop

The following loop is forbidden by default:

```text
private User-Claims
  -> GitHub/public snapshot
  -> generated inspirational environment
  -> new user prompts/claims
```

This would turn GitHub into a zipper between private meaning and generated environment. That is not the intended architecture.

Correct flow:

```text
private User-Claims
  -> local Receipt-Ledger
  -> verifyLedger / integrity check
  -> reduced public anchor
  -> GitHub witness
```

No automatic return path from GitHub witness data into personalization is allowed.

---

## Essence architecture

GitHub may host the public essence architecture for image generation and symbolic interfaces:

- public symbol modules
- public prompt schemas
- public visual operators
- public negative prompts
- public anti-overclaim rules
- public tests and validation

User input activates this architecture only at runtime. Private activation data must not be written back to GitHub by default.

---

## Review checklist

Before any GitHub sync, export or anchor feature is merged, reviewers should ask:

1. Does the payload contain raw private claims?
2. Does it contain private images or generated outputs?
3. Does it contain embeddings or profiles?
4. Can the payload reconstruct private user meaning?
5. Is the visibility explicitly `public-anchor`, `public`, `internal` or `private`?
6. Does the UI explain what will be exported?
7. Is public export opt-in rather than default?
8. Is the payload reduced to integrity metadata where possible?

If any answer is unclear, stop and add a VOID, test or policy note before merging.
