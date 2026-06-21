# Strict Tool Use Checklist

Use this checklist after the tool boundary is clear and before LAB-03. Strict tool use protects the tool-call interface. It does not replace tool naming, business validation, final-output structure, or structured error handling.

## 1. Use Strict Mode For The Right Failure

Use strict tool use when malformed tool arguments create real execution, safety, or support risk.

Good fit:

- a function receives the wrong type
- required tool inputs are missing
- extra inputs create unsafe behavior
- downstream code assumes a stable argument shape

Wrong fit:

- the model is choosing the wrong tool because descriptions overlap
- the final answer needs a JSON response schema
- the tool result is valid but violates a business rule
- the workflow needs retry, stop, or escalation metadata

Exam shortcut: choose strict tool input schema when the failure is invalid function-call arguments.

## 2. Start With Boundaries

Before adding `strict: true`, confirm the tool has:

- a specific action verb in the tool name
- one primary job
- a clear use-when line
- a clear do-not-use-when line
- similar-tool contrast
- required facts before use

If the model cannot tell which tool owns the job, strict inputs only make the wrong call better shaped.

## 3. Tool Definition Fields

Minimum strict tool definition:

```json
{
  "name": "issue_refund",
  "description": "Issue a refund for a confirmed duplicate or incorrect charge after validation is complete.",
  "strict": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "Order identifier for the confirmed charge."
      },
      "amount": {
        "type": "number",
        "description": "Refund amount after validation."
      },
      "reason": {
        "type": "string",
        "description": "Validated refund reason."
      }
    },
    "required": ["order_id", "amount", "reason"],
    "additionalProperties": false
  }
}
```

## 4. Schema Essentials

Checklist:

- Required fields match what the function truly needs.
- Field types are stable and simple.
- `additionalProperties` is `false` unless there is a deliberate reason.
- Field descriptions explain business meaning, not private data.
- Optional fields are limited.
- Union types are avoided unless they remove real ambiguity.
- Schema names, enum values, const values, and regex patterns do not contain PHI, secrets, or private raw data.

Keep schema complexity low. Complex strict schemas can add compilation and caching considerations.

## 5. What Strict Mode Protects

Strict tool use protects:

- valid tool names from the provided tool set
- tool input shape
- required input presence
- basic field types
- fewer runtime cleanup branches for malformed arguments

Strict tool use does not prove:

- the right tool was selected
- the final answer is structured correctly
- the tool result is truthful or complete
- business policy was satisfied
- the error shape is machine-usable
- the workflow should retry or escalate

## 6. LAB-03 Anchor

Weak starter pair:

| Tool | Risk |
| --- | --- |
| `handle_refund` | Too broad; can hide lookup, validation, and refund execution under one name. |
| `resolve_charge_issue` | Overlaps with refund language and does not make the execution boundary obvious. |

Stronger tool set:

| Tool | Strict input expectation |
| --- | --- |
| `lookup_order` | Requires `order_id`; never issues refunds. |
| `issue_refund` | Requires `order_id`, `amount`, and `reason`; use only after validation confirms the charge issue. |
| `escalate_case` | Requires `reason` and `case_summary`; use for policy review or manual approval. |

Use strict inputs after this split, not before it.

## 7. Final Check Before LAB-03

- Can you explain the tool boundary without reading implementation code?
- Can you name the required fields before writing the schema?
- Would an invalid argument break code or create unsafe behavior?
- Does the schema block extra fields?
- Does a validation failure return structured error metadata?
- Does the exam answer fix the owning layer, not just mention the newest feature?
