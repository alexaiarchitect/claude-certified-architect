# Enforcement Choice Matrix

Use this before choosing between plain JSON text, structured JSON output, strict tool inputs, and validation. The exam shortcut is simple: pick the enforcement point that owns the failure mode.

## Quick Matrix

| Need | Best enforcement point | What it protects | What it does not prove |
| --- | --- | --- | --- |
| Human-readable draft that happens to be JSON-shaped | Plain JSON in text | Light formatting and review convenience | Parseability, required fields, source truth, or stable automation |
| Final answer must be valid JSON with required fields and types | Structured JSON output with `output_config.format` | Final response shape, parseability, required fields, basic schema contract | Source accuracy, arithmetic, missing-source handling, saved artifact quality |
| Claude must call a function with valid arguments | Tool JSON / strict tool use with `strict: true` | Tool name and tool input arguments | Final answer shape, tool result quality, business-rule correctness |
| Extracted values must match the document and downstream rules | Validation layer | Source truth, arithmetic, semantic checks, retry feedback, artifact acceptance | Model output generation by itself |

## Plain JSON In Text

Plain JSON is a formatting request.

Use it when:

- the result is low risk
- a human will review it before automation
- broken formatting is inconvenient but not dangerous

Do not rely on it when:

- downstream code will parse the result automatically
- required fields must always exist
- wrong types, missing fields, or malformed JSON would break the workflow

Weak instruction:

```text
Return JSON.
```

Better architecture:

```text
Use a schema-backed output contract and validate the result before saving it.
```

## Structured JSON Output

Structured JSON output is a final-response contract. In the Claude API, current structured-output framing uses `output_config.format` to request JSON that follows a schema.

Use it when:

- the final response must be machine-readable
- required fields and types matter
- parsing failures would create fragile downstream logic
- the application should receive a predictable response shape

Remember:

- it protects schema shape, not source truth
- refusals and `max_tokens` can still prevent a complete valid output
- very complex schemas can add implementation constraints
- keep secrets, PHI, and private raw data out of schema names, enum values, and patterns

## Tool JSON And Strict Tool Use

Tool JSON is an input contract for a tool call. Strict tool use with `strict: true` constrains Claude's tool-call input to match the tool schema.

Use it when:

- Claude must call a function
- invalid tool arguments would break code
- tool selection and input shape need an explicit boundary
- the failure is happening before your application executes the tool

Remember:

- strict tool use protects tool inputs, not the final answer
- tool descriptions and boundaries still matter
- tool results still need error handling and logging

## Validation Layer

Validation owns the truth test after a structured result exists.

Use validation to check:

- required fields are present
- source labels match extracted values
- subtotal, tax, total, and line item math are correct
- absent source fields become `null`, `unclear`, or review flags
- retry feedback names the exact failed checks
- the final accepted result is saved as a downstream artifact

Validation is still required when the output is valid JSON but wrong.

## LAB-02 Invoice Example

For the LAB-02 invoice, plain `return JSON` is not enough. The workflow needs a contract and a validator.

Source facts:

- invoice ID: `INV-2048`
- company: `Northwind Labs`
- currency: `USD`
- subtotal: `1500.00`
- tax: `120.00`
- total: `1620.00`
- line items:
  - `Architecture Review Sprint`, qty `1`, unit price `1200.00`
  - `Reliability Checklist Pack`, qty `2`, unit price `150.00`

Best architecture:

1. Define the required extraction fields.
2. Use structured output or an equivalent schema contract for the final shape.
3. Validate semantic checks such as total math and line item count.
4. Retry only when feedback is exact and bounded.
5. Save the validated artifact.

## Exam Shortcut

When an answer choice proposes a fix, ask which layer failed.

| Failure signal | Prefer | Reject |
| --- | --- | --- |
| Output is JSON-shaped but sometimes malformed | Structured JSON output | "Prompt harder" only |
| Tool receives the wrong argument type | Strict tool input schema | Final-output schema only |
| JSON shape is valid but arithmetic is wrong | Validation and retry feedback | More JSON formatting instructions |
| Source omits a value | Nullable field or review flag | Fabricating a confident value |
| Retry repeats the same bad result | Stop or escalate after bounded attempts | Blind retry loops |

The best answer is usually the smallest enforcement point that directly owns the failure.
