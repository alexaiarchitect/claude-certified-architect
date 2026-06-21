# LAB-03 Troubleshooting

## Common Failures

- keeping two tools with nearly identical keywords
- forgetting to validate payload fields before "executing"
- treating a permission failure as retryable
- adding strict input fields before the tool boundary is clear
- returning plain error strings that do not tell the caller whether to retry, stop, clarify, or escalate

## Fast Checks

1. Run the overlap check first.
2. Confirm each task maps to one obvious tool.
3. Confirm error shapes include `isError`, `category`, and `retryable`.

## Expected Starter Signal

The starter evaluator should print an overlap warning:

```text
WARNING: handle_refund overlaps with resolve_charge_issue on ['charge', 'refund']
```

That warning is the first failure to fix. Do not start by adding more prompt examples or stricter schemas to tools whose jobs still overlap.

## Expected Solution Signal

The solution evaluator should print:

```text
Tool overlap check passed.
```

Then each task should route to one expected tool:

| Intent signal | Expected tool |
| --- | --- |
| duplicate charge refund | `issue_refund` |
| look up order before deciding | `lookup_order` |
| policy review or manual approval | `escalate_case` |

## Failure-Layer Checks

| Symptom | Owning layer | First fix |
| --- | --- | --- |
| Two tools share the same refund or charge language | Tool boundary | Rename, narrow descriptions, and add negative guidance |
| Tool is selected but required fields are missing | Input contract | Add required fields and validate before execution |
| Tool returns `"failed"` or another plain string | Error taxonomy | Return `isError`, `category`, `retryable`, and a useful message |
| Policy or permission failure retries repeatedly | Recovery control | Mark non-retryable and escalate or stop |
| Valid lookup finds no matches | Result semantics | Return success with an empty result, not a tool error |

## When To Use The Support Assets

- Use the tool-spec worksheet when selection is ambiguous.
- Use the strict tool-use checklist when malformed arguments can break execution.
- Use the tool error taxonomy card when the caller needs retry, stop, clarify, or escalation metadata.

## Live API Checks

Live mode is optional and uses Claude Sonnet 4.6 by default:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 solution/src/evaluate_tools.py --live
```

If live mode fails:

- Missing key: export `ANTHROPIC_API_KEY` or load the workspace `.env`.
- Invalid key: create a fresh Anthropic Console key.
- Model unavailable: override `ANTHROPIC_MODEL`.
- Tool mismatch: inspect whether the tool descriptions or required fields create ambiguity.
- Missing tool input: tighten the tool schema before changing recovery code.
