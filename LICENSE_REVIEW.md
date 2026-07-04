# License Review Notes

This document records the current governance question around open source, commercial use and anti-capture goals.

It is not legal advice.

---

## Current state

The repository currently uses Apache License 2.0.

Apache-2.0 is a permissive open source license. It allows broad use, modification, distribution and sublicensing under its terms.

This is compatible with open development, but it is not designed as an anti-capture or anti-commercial license.

---

## Open source and field-of-use restrictions

Classic OSI open source licenses cannot restrict use by field of endeavor.

That means an OSI-open-source license cannot simply forbid business use, commercial use or a specific sector while remaining OSI-open-source.

Therefore, the project should avoid saying:

> This is open source and forbids commercial use.

A more accurate statement is:

> The project supports open development and anti-capture governance. License choices require separate review.

---

## Commercial use is not the same as capture

Commercial use and extractive capture are different questions.

A commercial actor may operate responsibly. A noncommercial actor may still be extractive.

The anti-capture concern is primarily about:

- surveillance
- profiling
- hidden personalization loops
- lock-in
- semantic extraction of private meaning
- behavioral manipulation
- private data feedback into generated environments

---

## AGPL note

AGPL-3.0-or-later may be useful if the project wants stronger transparency for modified network services.

AGPL can reduce SaaS opacity because modified versions used over a network must provide corresponding source under the license.

AGPL does not forbid commercial use.

It is a transparency and copyleft tool, not an anti-commerce tool.

---

## Possible paths

### Option A: OSI open source with stronger copyleft

- Review AGPL-3.0-or-later for code.
- Commercial use remains allowed.
- Anti-capture is handled through governance, privacy architecture, trademarks and hosted-service terms.

### Option B: Source-available / noncommercial / ethical-source approach

- May better match strict anti-commercial goals.
- Would not be OSI open source if it restricts fields of endeavor or commercial use.
- Requires careful legal review and clear public wording.

### Option C: Hybrid

- Code license remains OSI-open-source or moves to AGPL after review.
- Documentation, essence architecture and symbolic materials may use separate content licenses after review.
- Official hosted service terms forbid surveillance, profiling and hidden personalization.
- Trademark/name usage is governed separately.
- GitHub remains an essence/witness layer, not a store for private user data.

---

## Recommended next step

Do not change the license by vibe.

Create a dedicated legal/governance review before any license migration:

1. Inventory code, docs, generated assets and symbolic materials.
2. Identify third-party license constraints.
3. Decide which obligations must be legally enforceable and which remain governance norms.
4. Compare Apache-2.0, AGPL-3.0-or-later and source-available options.
5. Update README, WELCOME, CONTRIBUTING, NOTICE and policy files consistently.
