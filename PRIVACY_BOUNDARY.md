# Privacy Boundary

This document defines the privacy boundary for entaENGELment, especially around User-Claims, the Gläserne Agora, Receipt-Ledgers, material pointers, GitHub anchors and essence architecture.

It is a governance and implementation guide, not legal advice.

---

## Core principle

Private meaning must not be silently converted into system fuel.

User-Claims, private images, personal symbolic profiles and embeddings belong behind a privacy boundary unless the user explicitly chooses otherwise.

---

## Data classes

### Private by default

- raw User-Claims
- private user images
- personal symbolic profiles
- private material labels
- private generated outputs
- embeddings of private content
- local Receipt-Ledger exports
- inferred psychological or behavioral profiles

### Internal / lab use

- local test ledgers
- local JSONL snapshots
- local material pointers
- local integrity-check reports
- local tamper-drill outputs

### Public by explicit action

- public documentation
- public code
- public schemas
- public tests
- public essence architecture
- public claim examples that contain no private data
- reduced public anchors

### Public-anchor only

- `ledgerRootHash` or `snapshotRootHash`
- `entryCount`
- `schemaVersion`
- `createdAt`
- `previousSnapshotHash`
- `policyHash`
- `visibility: public-anchor`

---

## GitHub boundary

GitHub must not receive private user meaning by default.

Allowed GitHub payloads are reduced, non-reconstructive and explicitly marked.

Disallowed by default:

- raw claims
- raw prompts
- private images
- private material labels
- embeddings
- profiles
- private ledger entries
- hidden personalization seeds

---

## Export boundary

Before export, the UI should show:

1. What will be exported?
2. Is this private, internal, public or public-anchor?
3. Does it contain raw claims?
4. Does it contain material labels?
5. Can it be reconstructed into private meaning?
6. Is the export opt-in?

Default export mode should be local/private unless explicitly changed.

---

## Ledger boundary

The Receipt-Ledger may be append-only and tamper-evident, but that does not make it public.

Hash-chaining proves consistency of a local or exported state. It does not remove privacy risk.

A valid ledger can still contain private content.

---

## Material pointer boundary

materialPointers may indicate which materials shaped a claim. They must not automatically be treated as evidence.

Roles should be explicit where possible:

- inspiration
- analogy
- evidence
- counterpoint
- artifact
- source

Analogy is not evidence. Inspiration is not proof.

---

## Generated environment boundary

The inspirational environment must not be generated from private User-Claims unless the user explicitly activates that data for the current runtime.

No private activation data should be written back to GitHub by default.

Forbidden default loop:

```text
private user data -> public/github layer -> generated environment -> new private claim
```

Allowed runtime-only flow:

```text
public essence architecture + current user input -> temporary generation -> local user decision
```

---

## Review checklist

Before merging features that touch privacy-sensitive paths:

- Are private claims ever logged?
- Are private claims sent to third-party APIs?
- Are private claims included in GitHub payloads?
- Are material pointers safe and non-reconstructive?
- Is export opt-in and visible?
- Is public-anchor distinct from public content?
- Is any generated personalization derived from private ledger data?
- Is there a recovery/reset path for local data?

If in doubt, default to private/local and add a VOID for review.
