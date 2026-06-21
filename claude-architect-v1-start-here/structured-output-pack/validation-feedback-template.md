# Validation Feedback Template

Use this when an extraction fails validation and a retry can plausibly fix the result. The goal is to give the next attempt exact, useful feedback instead of vague pressure.

## 1. Retry Decision Gate

Retry only when all required conditions are true.

| Gate | Retry when true | Do not retry when false |
| --- | --- | --- |
| Source contains the needed information | the value exists in the provided document | the value is absent or only exists in an external source |
| Failure is correctable | format mismatch, missing field, wrong field placement, arithmetic mismatch | permission, policy, ambiguity, missing source data, unsafe side effect |
| Feedback is specific | the validator names exact failed checks | feedback says only "try again" or "be more accurate" |
| Attempts are bounded | retry budget remains | retry budget is exhausted |
| State is safe | retry will not duplicate an unsafe side effect | retry could duplicate a charge, refund, email, or final action |

Decision:

```text
Retry: yes / no
Reason:
Next action if no retry:
```

## 2. Retry Feedback Message

Use this structure for the follow-up request.

```text
Return the full schema.
Use the original source document and the failed extraction below.
Fix these exact validation errors:

- [validation_error_1]
- [validation_error_2]
- [validation_error_3]

Do not change fields that already passed validation unless the correction requires it.
If the source does not contain a value, return null and add the field to review_notes.
```

Include with the retry:

- original source document
- failed extraction
- exact validation errors
- schema or required output contract
- attempt number and remaining retry budget

## 3. Error Categories

| Error category | Example | Retry? | Feedback shape |
| --- | --- | --- | --- |
| Missing required field | `currency` absent | Yes, if present in source | `Missing required field: currency. Extract it from the source.` |
| Invalid total | total is `1500.00`, source total is `1620.00` | Yes | `Total should be 1620.00. Recalculate from subtotal plus tax.` |
| Missing line item | one item returned, source has two | Yes | `Two line items were expected. Include all source rows.` |
| Wrong field placement | tax appears as total | Yes | `Move the tax value to tax and use the stated total for total.` |
| Unsupported value | invented purchase order | No, unless source contains it | `Do not infer. Return null and add review_notes.` |
| Missing source data | source omits due date | No | `Return null or route to review; do not retry blindly.` |

## 4. Retry Log Entry

Every retry should leave a small audit trail.

```text
attempt:
validation_status: failed / passed
failed_checks:
retry_feedback:
retry_decision: retry / stop / review
reason:
next_attempt_result:
final_artifact_path:
```

## 5. LAB-02 Example

Failed extraction:

```json
{
  "invoice_id": "INV-2048",
  "company": "Northwind Labs",
  "currency": "USD",
  "subtotal": 1500.0,
  "tax": 120.0,
  "total": 1500.0,
  "line_items": [
    {"name": "Architecture Review Sprint", "qty": 1, "unit_price": 1200.0}
  ]
}
```

Validation errors:

```text
- Total should be 1620.0.
- Two line items were expected.
```

Useful retry feedback:

```text
Return the full schema. Fix these exact issues: total should be 1620.0; two line items were expected. Preserve invoice_id, company, currency, subtotal, and tax because they already match the source.
```

Stop condition:

```text
If the next attempt still fails these same checks, stop and route to review instead of looping.
```
