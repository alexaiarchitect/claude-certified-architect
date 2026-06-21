# Risk Note Template

Use a risk note when a choice is acceptable for v1 but may need review, patching, or escalation later.

## Risk

- Risk ID:
- Related module/lab:
- Date:
- Owner:

## Failure Layer

Choose one:

- loop control
- tool boundary
- structured output
- validation retry
- Claude Code team configuration
- context/provenance
- escalation or human review
- platform or UI drift

## Impact

What breaks or becomes misleading if this risk happens?

## Current Mitigation

What keeps the course, lab, or architecture safe enough for now?

## Patch Path

Choose one:

- notes only
- overlay patch
- audio patch
- full rerecord

## Review Trigger

Revisit this when:

- official docs or product behavior changes
- a lab breaks
- students report the same confusion three or more times
- a quiz/mock rationale would train the wrong answer

## Decision

For now, we will:

```text
[current choice], because [why it is acceptable for v1].
```
