# Tool-Spec Worksheet

Use this worksheet before adding or renaming a tool. The goal is to make the correct tool obvious, make the wrong tool unattractive, and give the caller enough structure to recover when something fails.

## 1. Tool Identity

| Field | Notes |
| --- | --- |
| Tool name | Use a specific action verb, such as `issue_refund`, `lookup_order`, or `escalate_case`. |
| Primary job | One sentence. Name the exact job this tool owns. |
| Business object | Customer, order, charge, document, case, repository, or another clear object. |
| Similar tools | List tools a model might confuse with this one. |
| Boundary note | Explain the difference from the most similar tool. |

## 2. Selection Boundary

| Prompt | Fill In |
| --- | --- |
| Use this tool when | |
| Do not use this tool when | |
| Required facts before use | |
| Caller should ask for clarification when | |
| Caller should escalate when | |

## 3. Input Contract

| Input | Required? | Type / Format | Validation Rule | Example |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

## 4. Output Contract

Success shape:

```json
{
  "isError": false,
  "tool": "",
  "result": {}
}
```

Error shape:

```json
{
  "isError": true,
  "category": "validation | business | permission | transient",
  "retryable": false,
  "message": "",
  "recovery_hint": ""
}
```

Retryable conditions:

- Example: transient timeout, temporary service unavailable, or fixable validation error.

Non-retryable conditions:

- Example: policy violation, permission denial, missing source fact, or unsupported request.

## 5. Selection Test Cases

Write short user intents and the one tool that should win. Include at least one near-miss where this tool should not be selected.

| User Intent | Expected Tool | Why |
| --- | --- | --- |
| | | |
| | | |
| | | |

## 6. LAB-03 Boundary Example

Weak starter pair:

| Tool | Problem |
| --- | --- |
| `handle_refund` | Too broad: "Handle refund work for order issues." |
| `resolve_charge_issue` | Overlaps on refund and charge language, so routing is ambiguous. |

Stronger split:

| Tool | Boundary |
| --- | --- |
| `issue_refund` | Use only after validation confirms a duplicate or incorrect charge. Do not use for order lookup or policy exceptions. |
| `lookup_order` | Use when the system needs order facts before deciding the next action. Do not issue refunds. |
| `escalate_case` | Use when policy review or manual approval is required. Do not use for routine lookup or validated refunds. |

Boundary check:

- If two tools share the same action verb, object, and keywords, rewrite before adding examples.
- If the model needs hidden business knowledge to choose correctly, the descriptions are not explicit enough.
- If "do not use me for" is hard to write, the tool probably owns too much.
