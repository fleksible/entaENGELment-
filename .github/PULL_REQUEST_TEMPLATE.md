# Pull Request

## Summary
<!-- Provide a brief description of the changes in this PR -->

## Type of Change
<!-- Mark the relevant option with an [x] -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test coverage improvement

## Related Issues
<!-- Link to related issues using #issue_number -->

Closes #

## Changes Made
<!-- List the key changes made in this PR -->

-
-
-

## Testing
<!-- Describe the tests you ran to verify your changes -->

### Test Coverage
- [ ] Unit tests pass locally (`make test-unit`)
- [ ] Integration tests pass locally (`make test-integration`)
- [ ] Ethics/fail-safe tests pass locally (`make test-ethics`)
- [ ] All tests pass (`make test`)

### Code Quality
- [ ] Code passes linting (`make lint`)
- [ ] Code is properly formatted (`make format`)
- [ ] Type checking passes (`make type-check`)

### DeepJump Protocol Validation
<!-- If applicable, verify DeepJump protocol compliance -->
- [ ] Pointers verified (`make verify-pointers`)
- [ ] Claims linted (`make claim-lint`)
- [ ] Port matrix validated (`make port-lint`)
- [ ] Full DeepJump flow passes (`make deepjump`)

## Documentation
- [ ] Code is self-documenting with clear variable/function names
- [ ] Complex logic is commented where necessary
- [ ] README updated (if applicable)
- [ ] Docstrings added/updated for public APIs

## Gate Policy Compliance
<!-- For changes affecting the gate policy or ethical constraints -->
- [ ] Changes respect consent requirements
- [ ] Bandwidth shaping validated (if applicable)
- [ ] No raw identifiers introduced
- [ ] Gate policy tests pass (`make gate-test`)

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Notes
<!-- Add any additional context, screenshots, or notes for reviewers -->


---

**For Reviewers:**
- Please verify all checkboxes are completed
- Run `make deepjump` locally to validate full compliance
- Check for potential security implications
- Verify ethical constraints are maintained
