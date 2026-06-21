# ADR Template

## Metadata

- ADR ID:
- Date:
- Status: Proposed | Accepted | Superseded
- Owner:
- Related module/lab:

## Context

What problem, constraint, or risk forced a decision?

Include the failure layer if relevant:

- loop control
- tool boundary
- structured output
- validation retry
- Claude Code team configuration
- context/provenance
- escalation or human review

## Constraints

- delivery speed:
- reliability requirement:
- maintenance cost:
- platform volatility:
- student/exam relevance:

## Decision

State the chosen approach in one sentence.

```text
We will [chosen approach] because [root reason].
```

## Options Considered

| Option | Why it was considered | Why it wins or loses |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

## Decision Criteria

Check the criteria that matter for this decision:

- [ ] fixes the owning failure layer
- [ ] lowers operational risk
- [ ] keeps maintenance cost reasonable
- [ ] preserves observability or validation
- [ ] avoids unnecessary platform-specific coupling
- [ ] helps answer exam-style scenarios

## Tradeoffs

- Benefits:
- Costs:
- Failure modes:
- Operational burden:
- What becomes harder later:

## Consequences

- What gets easier?
- What gets harder?
- What should be monitored?
- What student or team behavior changes?

## Review Trigger

Revisit this ADR when:

- the relevant Claude/API/Claude Code behavior changes
- a lab or workflow breaks
- students repeatedly misunderstand the decision
- a later module introduces a better lower-risk lever
