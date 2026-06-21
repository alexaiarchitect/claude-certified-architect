# Tool Error Taxonomy Card

Use this card when a tool can fail and the caller needs to decide whether to retry, stop, ask for clarification, or escalate.

## Minimum Error Contract

Every tool error should return enough structure for the next controller to make a safe decision.

```json
{
  "isError": true,
  "category": "transient | validation | business | permission",
  "retryable": false,
  "message": "",
  "recovery_hint": ""
}
```

Recommended optional fields:

```json
{
  "attempted_input": {},
  "partial_result": {},
  "user_safe_message": "",
  "next_action": "retry | stop | clarify | escalate"
}
```

## Categories

| Category | Signal | Retry? | Better First Action |
| --- | --- | --- | --- |
| `transient` | timeout, rate limit, temporary service unavailable | Yes, if bounded and idempotent | Retry with backoff and attempt logging |
| `validation` | missing required field, invalid format, unsupported enum | Usually no for tool input; yes only if caller can supply corrected input | Return exact missing or invalid fields |
| `business` | policy threshold, unsupported operation, manual approval required | No | Route to business workflow or human review |
| `permission` | access denied, missing scope, user not authorized | No | Request authorization or escalate |

## Valid Empty Result

An empty result is not automatically an error.

```json
{
  "isError": false,
  "tool": "lookup_order",
  "result": {
    "matches": []
  }
}
```

Use success with an empty result when the query completed correctly and found nothing. Use an error only when the tool could not complete the requested operation.

## Retry / Stop / Escalate

Retry when:

- the category is `transient`
- the operation is idempotent
- the attempt count is bounded
- the next attempt changes something useful

Stop or ask for clarification when:

- required input is missing
- the user request is ambiguous
- the source does not contain enough information

Escalate when:

- a permission or policy boundary blocks progress
- manual approval is required
- the system cannot safely decide the next action

## LAB-03 Example

```json
{
  "isError": true,
  "category": "validation",
  "retryable": false,
  "message": "Missing required fields: amount, reason",
  "recovery_hint": "Ask for the missing refund amount and reason before calling issue_refund."
}
```

Exam shortcut: if the scenario says the caller cannot decide whether to retry, stop, or escalate, the owning layer is tool error handling. Prefer structured error metadata over generic failure strings or blind retries.
