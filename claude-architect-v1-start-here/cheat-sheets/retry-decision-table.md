# Retry Decision Table

Use this table for M2.3, M3 validation loops, M4 structured errors, and mini mock review.

The core rule: retry only when the failure is retryable, bounded, observable, and idempotent.

## Decision Table

| Failure Class | Example Signal | Retry? | Better First Action |
| --- | --- | --- | --- |
| Transient access failure | timeout, rate limit, temporary service unavailable | Yes, if bounded and idempotent | Retry with backoff, preserve attempt count, log context |
| Validation failure with fixable feedback | schema mismatch, missing required field, arithmetic mismatch | Yes, if feedback is specific | Retry with exact validation errors, then stop after max attempts |
| Missing source information | document does not contain the requested field | No | Return partial result, ask for source, or route to review |
| Permission failure | access denied, token lacks scope, user cannot perform action | No | Escalate or request authorization; do not loop |
| Policy or business rule failure | refund over approval threshold, restricted operation | No | Route to policy workflow or human review |
| Ambiguity | multiple plausible customer records, conflicting sources | Usually no | Ask a clarifying question or escalate with structured context |
| Unknown response state | unrecognized `stop_reason` or malformed control payload | No blind retry | Persist raw payload, stop the loop, inspect or escalate |

## Idempotency Check

Before retrying, confirm:

- the same action can run twice without duplicate side effects
- the retry has a maximum attempt count
- the next attempt changes something useful, such as waiting for a transient service or adding specific validation feedback
- logs preserve attempt number, failure class, and final decision

## Exam Shortcut

Reject answers that say "retry more" when the scenario describes:

- missing information
- permission failure
- policy boundary
- ambiguity
- unsafe side effects
- no change between attempts

Prefer answers that classify the failure, preserve context, and choose stop/retry/escalate deliberately.
