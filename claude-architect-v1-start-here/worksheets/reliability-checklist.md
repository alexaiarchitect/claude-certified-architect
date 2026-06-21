# Reliability Checklist

Use this checklist before you ship a workflow that summarizes, extracts, calls tools, or makes a recommendation from multiple sources.

Reliability is not one trick. It is a set of design choices that preserve context, keep provenance visible, define failure behavior, and route uncertain cases to review.

## 1. Critical Context

List the facts that must survive every handoff, summary, retry, or tool call.

| Context item | Why it matters | Where it is preserved |
| --- | --- | --- |
| IDs and names | Prevents entity mix-ups | |
| Dates and time windows | Prevents stale or wrong-period answers | |
| Numeric values | Protects totals, limits, prices, and scores | |
| User constraints | Keeps the system inside the stated task | |
| Tool results | Prevents repeated or inconsistent actions | |
| Current state | Shows what has already happened | |

## 2. Provenance Map

Every important claim should keep a link to the source that supports it.

| Claim or extracted fact | Source | Date or version | Evidence note | Confidence |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

Use this rule: if a downstream reviewer cannot tell where a claim came from, the system lost provenance.

## 3. Failure Classes

Classify failures before choosing recovery behavior.

| Failure class | Example signal | Default control |
| --- | --- | --- |
| Missing source | Required fact is not present | Stop, ask, or review. Do not invent. |
| Conflicting source | Two sources disagree | Preserve both claims and escalate if material. |
| Low confidence | Evidence is weak or ambiguous | Route to review or ask for clarification. |
| Tool or system failure | Timeout, unavailable service, parse failure | Retry only with bounds and a useful change. |
| Policy or permission issue | Action may be unsafe or unauthorized | Stop or escalate through the defined path. |
| Valid empty result | Lookup succeeds with no matches | Treat as success with no result, not as a failure. |

## 4. Escalation Criteria

Write explicit criteria. Do not rely on sentiment, vague complexity, or the model's self-reported confidence as the only trigger.

Escalate when:

- the user asks for human review
- the system cannot make progress after bounded recovery
- required evidence is missing
- sources conflict on a material claim
- identity, permissions, policy, or compliance is ambiguous
- the answer could create high-impact financial, legal, security, medical, or operational consequences

Do not escalate only because:

- the message sounds frustrated
- the model says it is "not confident" without evidence
- the prompt is long
- a generic retry failed once

## 5. Human Review Design

Human review belongs in the workflow design, not only in support.

| Review trigger | Reviewer sees | Decision needed |
| --- | --- | --- |
| High-impact field changed | Original source, extracted value, validation result | Approve, correct, or reject |
| Source conflict | Both sources and timestamps | Choose source, annotate conflict, or escalate |
| New document type | Sample input, failed checks, expected output | Add rule, update template, or reject |
| Repeated low-confidence case | Attempts, feedback, final state | Change workflow or add guardrail |
| Random audit sample | Source, output, provenance map | Calibrate quality over time |

## 6. Retry Boundaries

Retries are reliability controls only when they are bounded and informed.

Before retrying, answer:

- What changed for the next attempt?
- Is the action idempotent?
- What is the attempt limit?
- What failure class stops the retry loop?
- What state is logged for review?

## 7. M6.1 Scenario Drill

Scenario: students report that a fast-moving capability lesson now sounds outdated, but the architecture principle is still correct.

Decision frame:

1. Classify the risk: exam-risk or cosmetic-risk.
2. If the principle is still correct, update notes or add an overlay first.
3. Rerecord only if the lesson now teaches the wrong choice.
4. Update the changelog and support response so learners know what changed.

## 8. Exam Shortcut

When a reliability question feels broad, identify the lost layer:

- lost facts
- lost provenance
- misread confidence
- failed escalation
- collapsed distinct sources into one summary
- unbounded retry or repeated action

Then pick the lowest-risk viable design that fixes that layer.
