# Trace Review Checklist

Use this with M2.4, LAB-01, LAB-02, quizzes, and scenario checks. The goal is to prove the owning layer before changing prompts, schemas, tools, or retry policy.

## Trace Snapshot

Capture the smallest useful evidence set.

| Field | What to capture | Why it matters |
| --- | --- | --- |
| Case or trace id | Your app's request id, workflow id, or ticket id. | Lets support and review find the same run again. |
| API request id | The provider request id or error `request_id`, when available. | Needed for vendor support and exact-request debugging. |
| Response id | The model response id, when available. | Ties logs to the response frame. |
| `stop_reason` | The response stop state. | Distinguishes routing failures from prompt or schema failures. |
| Content blocks | `text`, `tool_use`, `tool_result`, or structured output. | Shows whether the app handled the right block type. |
| Usage | Input and output token counts. | Helps detect truncation, cost, and context issues. |
| Tool or validator signal | Tool name/input summary or validation errors. | Proves whether the failure belongs to routing, tool design, schema, or validation. |
| Next action | Continue, retry, stop, or escalate. | Makes control decisions reviewable. |

Do not capture secrets, API keys, raw private data, or full documents when an id or safe excerpt is enough.

## First Read

Before changing the design, answer:

1. What did the system observe?
2. What did the application do next?
3. Which layer owned the decision?
4. Was the next action logged clearly?
5. Which weaker fix is tempting but wrong?

## Failure-Layer Triage

| Signal in the trace | Likely owning layer | First fix to consider |
| --- | --- | --- |
| `stop_reason` is `tool_use`, but the app returns final text. | Loop routing | Execute the tool, append `tool_result`, continue. |
| `stop_reason` is `end_turn`, but the app loops again. | Loop routing | Return final answer and persist logs. |
| `max_tokens` appears with partial content. | Context or token budget | Continue deliberately, reduce scope, or raise budget. |
| Tool names overlap or wrong tool is selected. | Tool design | Clarify tool names, descriptions, and boundaries. |
| Output has required fields but wrong arithmetic or missing source support. | Validation | Add semantic checks and specific retry feedback. |
| Retry repeats without new information. | Safe control | Classify failure, check idempotency, stop or escalate. |
| Permission, policy, refusal, or missing source data appears. | Authority or source boundary | Stop blind retries and escalate with structured context. |
| Logs have only raw payloads and no next action. | Observability | Log response id, stop state, next action, and safe summaries. |

## LAB-01 Routing Trace

Look for:

- `resp_sample_01`
- `stop_reason: tool_use`
- `get_customer_profile`
- `customer_id: cust_123`
- usage `321 input / 129 output`
- next action: run tool, append `tool_result`, continue

If the app ends immediately, the owning layer is loop routing, not prompt wording.

## LAB-02 Validation Trace

Look for:

- first attempt fails validation
- total should be `1620.0`
- two line items are expected
- retry feedback names the exact validation errors
- final saved artifact passes schema and semantic checks

If the output is shaped like JSON but arithmetic is wrong, the owning layer is validation, not stop routing.

## Exam Shortcut

Prefer answers that read the trace before changing the design.

Reject answers that:

- change the prompt before naming the observed failure
- retry without a failure class
- treat schema, routing, and permission failures as the same issue
- hide usage, stop state, validation errors, or next action from logs
- expose secrets or unnecessary private data in debug output
