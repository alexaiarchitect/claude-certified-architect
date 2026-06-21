# Request Routing Cheat Sheet

Use this with M2.2, LAB-01, and the M2 scenario check. The core rule is simple:
route from response state, not from assistant wording.

## Stop-Reason Router

| `stop_reason` | First control action | Watch for |
| --- | --- | --- |
| `tool_use` | Extract tool request, execute client tool, append `tool_result`, continue. | Text before the tool request is not a final answer. |
| `end_turn` | Return the final answer and persist logs. | Do not infer completion from a keyword like "done"; inspect the state. |
| `max_tokens` | Treat as incomplete; continue or raise the token budget deliberately. | If a tool call was truncated, retry with enough budget to capture the full tool request. |
| `stop_sequence` | Respect the configured boundary unless a deliberate continuation is needed. | The stop sequence is your app's boundary, not a model failure. |
| `pause_turn` | For server-tool loops, send the assistant response back and continue within bounds. | Log continuation count and stop if the loop keeps pausing. |
| `refusal` | Stop, reframe, or escalate with context. | Do not blind retry safety refusals. |
| `model_context_window_exceeded` | Compact, chunk, summarize, or escalate context handling. | More retries do not fix a context strategy failure. |
| unknown state | Preserve the payload, stop blind looping, inspect or escalate. | Unknown state is not permission to guess. |

## Client Tool-Use Flow

When `stop_reason` is `tool_use`, inspect each `tool_use` content block:

1. Extract `id`, `name`, and `input`.
2. Execute the matching tool in your application.
3. Send a new user message with a `tool_result` block.
4. Include `tool_use_id`, `content`, and optional `is_error`.
5. Continue the loop with the relevant conversation state.

Minimal shape:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "safe result or structured error"
    }
  ]
}
```

Formatting rules:

- The user message with `tool_result` must immediately follow the assistant message that contained the matching `tool_use`.
- In the user content array, all `tool_result` blocks come before any text blocks.
- Use `is_error: true` only when tool execution failed; a valid empty result is not automatically an error.
- Preserve the tool id so Claude can match result to request.

## LAB-01 Anchor

The sample response contains:

```json
{
  "id": "resp_sample_01",
  "stop_reason": "tool_use",
  "content": [
    { "type": "text" },
    {
      "type": "tool_use",
      "name": "get_customer_profile",
      "input": { "customer_id": "cust_123" }
    }
  ],
  "usage": {
    "input_tokens": 321,
    "output_tokens": 129
  }
}
```

First routing decision:

- Do not return the text as final.
- Run `get_customer_profile` with a safe input summary.
- Append a matching `tool_result`.
- Continue the loop with updated messages.
- Log the response id, stop reason, tool name, safe input summary, usage, and next action.

## Logging Boundary

Log:

- response id
- `stop_reason`
- tool `id`, `name`, and safe input summary
- usage counts
- chosen next action
- continuation or retry attempt count
- structured error category, when relevant

Do not log:

- secrets, API keys, tokens, or credentials
- unnecessary private raw data
- full documents when an id or excerpt is enough
- assistant text as the only control signal

## Safe Control Rule

Do not retry just because the loop failed.

Before retrying, answer:

1. What failed?
2. Is the next action idempotent?
3. Will the retry change the inputs or recover from a transient condition?
4. What partial result or error context must be logged?
5. Is this really a policy, permission, ambiguity, or missing-information failure that should escalate instead?

## Exam Shortcut

Prefer answers that:

- route on `stop_reason`
- return tool results with the correct message order
- keep loop boundaries visible in logs
- classify failures before retrying
- stop or escalate for permission, policy, ambiguity, missing source information, refusals, or unknown states

Reject answers that:

- check whether assistant text says "done"
- end immediately after `tool_use`
- add more prompt wording instead of fixing loop control
- retry every failure class
- hide routing decisions from logs
