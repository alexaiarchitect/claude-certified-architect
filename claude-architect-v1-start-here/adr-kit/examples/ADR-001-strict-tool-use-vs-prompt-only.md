# ADR-001: Strict Tool Use vs Prompt-Only Enforcement

## Metadata

- ADR ID: ADR-001
- Date: 2026-05-01
- Status: Accepted for v1 course example
- Owner: Course creator
- Related module/lab: M1.3, M4 Tool Design

## Context

An agent can call tools, but some tool calls require deterministic boundaries. If the system relies only on prompt wording, the model may still choose an unsafe or malformed tool path when the scenario is ambiguous.

The failure layer is tool boundary and workflow enforcement, not wording polish.

## Constraints

- delivery speed: keep the v1 pattern simple enough to teach quickly
- reliability requirement: tool calls must be constrained where business risk exists
- maintenance cost: avoid a large orchestration system before the tool boundary is clear
- platform volatility: keep the durable decision in the ADR and exact API details in lab notes
- student/exam relevance: students must learn to reject prompt-only fixes when deterministic enforcement is needed

## Decision

We will use strict tool inputs and schema-constrained control where workflow reliability matters because the interface boundary is safer than relying on prompt wording alone.

## Options Considered

| Option | Why it was considered | Why it wins or loses |
| --- | --- | --- |
| Stronger prompt wording | Fast and cheap to add | Loses because it does not enforce deterministic boundaries |
| Strict tool inputs and schema constraints | Adds design work but narrows invalid calls | Wins because it fixes the owning failure layer |
| Larger orchestration layer | Could centralize more control | Loses for v1 because it adds maintenance before the tool boundary is proven |

## Decision Criteria

- [x] fixes the owning failure layer
- [x] lowers operational risk
- [x] keeps maintenance cost reasonable
- [x] preserves observability or validation
- [x] helps answer exam-style scenarios

## Tradeoffs

- Benefits: clearer tool boundaries, better validation, easier debugging
- Costs: more upfront schema and tool-spec design
- Failure modes: schema may still miss semantic business rules
- Operational burden: tool specs must stay aligned with implementation
- What becomes harder later: changing tool contracts requires updating validators and examples

## Consequences

- Safer tool calls become easier to reason about.
- Prompt-only fixes are treated as distractors for deterministic workflows.
- The lab and later tool-design lessons can reuse the same decision frame.
- Students should monitor whether the schema explains errors clearly enough for retry or escalation.

## Review Trigger

Revisit this ADR when:

- the strict tool-use API behavior changes
- the tool-design lab no longer matches current docs
- students repeatedly choose prompt-only answers for enforcement scenarios
- later course versions add deeper orchestration examples
