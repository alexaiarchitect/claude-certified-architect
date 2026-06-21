# LAB-02 Troubleshooting

## Common Failures

- forgetting to create the `build/` directory
- validating only required fields and skipping arithmetic checks
- writing vague retry feedback like "try again"

## Fast Checks

1. Confirm the source document lives in `data/`.
2. Confirm the validator checks totals and line items.
3. Confirm the second attempt uses feedback from the first failure.

## Live API Checks

Live mode is optional and uses Claude Sonnet 4.6 by default:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 solution/src/extract.py --live
```

If live mode fails:

- Missing key: export `ANTHROPIC_API_KEY` or load the workspace `.env`.
- Invalid key: create a fresh Anthropic Console key.
- Model unavailable: override `ANTHROPIC_MODEL`.
- Malformed JSON: keep the validator strict and rerun; do not accept prose output.
- Validation failure: use the printed retry feedback to diagnose the schema contract issue.
