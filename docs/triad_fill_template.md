# Triad Fill Template — ☐[CLAUDE↔GPT↔FLEKS]

**Purpose:** Standardized slot format for each participant to independently write their perspective for triad comparison.

## Metadata (fill at top)
- author: <Claude | GPT | Fleks>
- date: YYYY-MM-DD
- kenogram_id: ☐-TRIAD-<short>
- tags: [list of tags]

## 1. Short Statement (max 300 words)
Describe in your own words the core primitives you think are essential to the project (e.g., "7x9 matrix", "mutual perception gate", "receipt chain").

## 2. Structural Primitives (bullet list)
List canonical names of artifacts/specs (one per line) and their referenced paths in the repo.
Example:
- 7x9 Matrix — spec/kenogram_7x9.md
- MutualPerception — src/cglg/mutual_perception.py

## 3. Thresholds & Numbers (if any)
List concrete numbers you used or propose (e.g., mu_thr=0.60, chi_release=0.35).

## 4. Measurable Signals (features)
List signals you consider primary (e.g., Likert, HRV_RMSSD, PLV, pause_density, embedding_MI).

## 5. Kenogram Hypothesis (1-2 lines)
State a testable hypothesis about the slot (e.g., "Lyra 7 bands align with first 7 Riemann zero spacings (GUE-like correlation)").

## 6. Data / Artifacts pointer
Provide path(s) to any local examples or simulated data that support your claim.

## 7. Short Ethical Note
Any consent/PII constraints relevant for this submission.

---

**Instructions:** Each participant fills the template independently. The triad_compare script will canonicalize, vectorize and compute overlap statistics.
