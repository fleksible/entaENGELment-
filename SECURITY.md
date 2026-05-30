# Security Policy

entaENGELment is an experimental research and governance framework. It is not production-ready software and does not provide a security guarantee.

This policy defines how security-relevant findings should be reported and how the project treats safety boundaries.

## Supported scope

Security-relevant reports may include:

- CI/CD workflow weaknesses
- dependency or supply-chain issues
- unsafe GitHub Actions configuration
- prompt-injection or untrusted-content handling gaps
- receipt, signature, or audit-trail integrity issues
- pointer-validation or claim-lint bypasses
- accidental exposure of sensitive data
- documentation claims that overstate security properties

Out of scope:

- requests to attack third-party systems
- social-engineering attempts
- reports requiring live biological, medical, or sensor data
- speculative harm claims without a reproducible repo path
- production-hardening demands beyond the current experimental status

## Reporting

Please open a GitHub issue when the finding can be public without increasing risk.

Use a private channel or contact the maintainer first when the report includes:

- exploitable details
- secrets, tokens, or credentials
- bypass steps for a live workflow
- personal data
- sensitive screenshots or logs

Do not paste secrets, credentials, tokens, private keys, or unrelated personal data into issues or pull requests.

## Report format

A useful report includes:

- affected file or workflow path
- expected behavior
- observed behavior
- minimal reproduction steps
- risk level: low / medium / high
- suggested fix, if known
- whether the issue is public-safe

## Claim discipline

Security claims must stay bounded.

Preferred language:

- "HMAC-signed receipt"
- "tamper-evident within the documented assumptions"
- "manipulation-resistant audit trail"
- "verification step"

Avoid unqualified claims such as:

- "secure"
- "unbreakable"
- "non-bypassable"
- "non-repudiable"
- "guaranteed"

When unsure, use the weaker claim and link evidence.

## Safety boundaries

This repository must not collect or process live biological, medical, or sensor data.

Security or safety reports involving such data should be reframed as synthetic, documented, non-identifying examples before being added to the repo.

## Response expectations

The maintainer will triage reports according to risk, reproducibility, and project scope.

Because this is an experimental project, some findings may be documented as open VOIDs instead of immediate fixes.
