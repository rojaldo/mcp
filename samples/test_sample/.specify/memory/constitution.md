<!--
  Sync Impact Report:
  Version change: none → 1.0.0
  Modified principles: N/A (initial creation)
  Added sections:
    - Core Principles (5 quality-focused principles)
    - Quality Gates section
    - Review Process section
    - Governance section
  Removed sections: none
  Templates requiring updates:
    - .specify/templates/plan-template.md: ✅ Constitution Check section compatible
    - .specify/templates/spec-template.md: ✅ Requirements format compatible
    - .specify/templates/tasks-template.md: ✅ Task categorization compatible
  Follow-up TODOs: none
-->

# test_sample Constitution

## Core Principles

### I. Test-First Development (NON-NEGOTIABLE)

All production code MUST be preceded by failing tests. The development cycle follows strict Red-Green-Refactor:
1. Write a test that fails
2. Get user approval on the test
3. Confirm test fails for the right reason
4. Write minimal code to make test pass
5. Refactor while keeping tests green

Rationale: Tests serve as executable specifications, enabling confident refactoring and preventing regressions.

### II. Code Review Standards

All code changes MUST undergo peer review before merge. Reviews MUST verify:
- Test coverage exists and tests pass
- Code follows established patterns and conventions
- No security vulnerabilities or hardcoded secrets
- Documentation updated for public APIs
- No unnecessary complexity

Rationale: Second set of eyes catches bugs, shares knowledge, and maintains consistency across the codebase.

### III. Static Analysis Enforcement

All codebases MUST pass static analysis checks before commit:
- Linting with zero warnings policy
- Type checking where applicable
- Security scanning for known vulnerabilities
- Complexity metrics within defined thresholds

Rationale: Automated checks catch issues early, reducing reviewer burden and maintaining code quality baseline.

### IV. Documentation Quality

Documentation MUST be:
- Written for public APIs and complex logic
- Updated alongside code changes
- Clear enough for a new team member to understand
- Version-controlled alongside source code

Rationale: Undocumented code is technical debt. Future maintainers need context to make informed changes.

### V. Continuous Integration Quality Gates

All merges MUST pass CI pipeline checks:
- All tests pass (unit, integration, contract)
- Code coverage meets minimum threshold (80%)
- No new security vulnerabilities detected
- Build artifacts generated successfully
- Performance benchmarks within acceptable range

Rationale: Automated quality gates ensure consistent standards and prevent broken code from reaching main branches.

## Quality Gates

### Minimum Requirements

- **Test Coverage**: Minimum 80% line coverage for new code
- **Lint Status**: Zero warnings, zero errors
- **Type Check**: 100% type coverage for typed languages
- **Build Status**: Clean build with no warnings
- **Security Scan**: No high/critical vulnerabilities

### Merge Requirements

- At least one approving review
- All CI checks passing
- No unresolved conversation threads
- Branch up-to-date with target branch

## Review Process

### Code Review Checklist

Reviewers MUST verify before approval:
- [ ] Tests exist and cover the change adequately
- [ ] Code follows project conventions
- [ ] No obvious security issues
- [ ] Error handling is appropriate
- [ ] Logging is sufficient for debugging
- [ ] Performance implications considered
- [ ] Documentation updated if needed

### Review Timeline

- Initial review response: Within 1 business day
- Follow-up responses: Within 4 hours during business hours
- Stale reviews (>7 days): Author should re-request or close

## Governance

### Amendment Process

Constitution changes require:
1. Written proposal documenting the change and rationale
2. Team discussion and consensus
3. Migration plan for existing code if needed
4. Update to this document with version bump

### Version Policy

- **MAJOR**: Backward incompatible principle changes
- **MINOR**: New principles or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance

All pull requests MUST verify compliance with current constitution. Complexity beyond defined thresholds requires documented justification in the implementation plan.

**Version**: 1.0.0 | **Ratified**: 2026-04-22 | **Last Amended**: 2026-04-22