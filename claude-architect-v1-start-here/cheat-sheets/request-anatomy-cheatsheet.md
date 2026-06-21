# Request Anatomy Cheat Sheet

Use this with M2.1 and LAB-01 to keep Claude API request and response state easy to inspect.

## Request Frame

| Field | What it owns | Keep in mind |
| --- | --- | --- |
| `model` | The Claude model used for the call. | Keep exact model strings in code/config, not scattered through notes. |
| `max_tokens` | The response budget for this call. | Hitting the limit changes the response state; do not treat it as a final answer. |
| `system` | Durable behavior instructions for the assistant. | Use for role, boundaries, and stable operating rules. |
| `messages` | The conversation state sent to the API. | The Messages API is stateless; send the relevant state each request. |
| `tools` | Available tool names, descriptions, and input contracts. | Tool descriptions affect selection, but tool routing is handled by response state. |
| `metadata` | Your app's trace and support context. | Add course, environment, request, or workflow identifiers that help debugging. |

## Response Frame

| Field | What it tells you |
| --- | --- |
| `id` | Response identifier for logs and support review. |
| `type` | The response object type, usually `message`. |
| `role` | The author role for the response, usually `assistant`. |
| `content` | Ordered content blocks such as `text` or `tool_use`. |
| `model` | The model that returned the response. |
| `stop_reason` | Why Claude stopped generating and what your loop should inspect next. |
| `stop_sequence` | The custom stop sequence, when one caused the stop. |
| `usage` | Input and output token counts for cost, debugging, and trace review. |

## Content Blocks

| Block | Meaning | First question |
| --- | --- | --- |
| `text` | Natural-language assistant content. | Is this final content, or explanatory text before another block? |
| `tool_use` | Claude is requesting a tool call. | Which tool, what input, and what should be logged before execution? |
| `tool_result` | Your app returns tool output in the next request. | Is the result structured, safe to share, and tied to the tool request id? |

## Stop-State Vocabulary

Treat `stop_reason` as response state, not decoration. M2.2 teaches detailed routing; M2.1 is about recognizing the field.

| Stop state | Anatomy-level meaning |
| --- | --- |
| `end_turn` | Claude finished this turn normally. |
| `tool_use` | Claude requested one or more tool calls. |
| `max_tokens` | The response hit the configured token budget. |
| `stop_sequence` | A configured stop sequence ended generation. |
| `pause_turn` | A server-side or long-running operation paused and should be resumed or handled deliberately. |
| `refusal` | Claude declined to provide the requested content. |
| `model_context_window_exceeded` | The model ran out of usable context window. |
| unknown | Preserve the payload and escalate instead of guessing. |

## What Belongs In Logs

Log the state needed to debug, support, and review the architecture:

- request or trace id
- response `id`
- `stop_reason`
- tool name and safe input summary
- usage counts
- next action selected by the loop
- retry attempt count, when relevant
- structured error category, when relevant

Do not log:

- API keys, credentials, tokens, or secrets
- unnecessary raw private data
- full documents when a document id or safe excerpt is enough
- one-off planning notes that belong in a ticket, ADR, or course note

## LAB-01 Anchor

The LAB-01 sample response uses:

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

Architecture read:

1. The response is not final just because it includes text.
2. `tool_use` means the application should execute the requested tool.
3. The next request should include the tool result and the relevant conversation state.
4. Logs should preserve `resp_sample_01`, `tool_use`, `get_customer_profile`, `cust_123`, `321`, `129`, and the next action.

## Exam Shortcut

Prefer answers that route from response state and observable logs.

Reject answers that:

- inspect assistant wording instead of `stop_reason`
- retry without a failure class
- ignore `tool_use` blocks
- hide token usage and next-action decisions from logs
- store volatile product details only in video narration
