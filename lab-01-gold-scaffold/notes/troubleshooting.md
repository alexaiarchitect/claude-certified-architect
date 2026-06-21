# LAB-01 Troubleshooting

## Common Failures

- Running from the wrong directory and losing relative paths
- Editing `.env.example` instead of creating a local `.env`
- Confusing request metadata with runtime logs

## Fast Checks

1. Run the script from the lab pack root.
2. Confirm the sample response file exists in `data/`.
3. Confirm the logger prints a routing decision, not raw JSON only.

## Live API Checks

Live mode is optional and uses Claude Sonnet 4.6 by default:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 solution/src/app.py --live
```

If live mode fails:

- Missing key: export `ANTHROPIC_API_KEY` or load the workspace `.env`.
- Invalid key: create a fresh Anthropic Console key.
- Model unavailable: set `ANTHROPIC_MODEL` to a model returned by the Models API.
- Network or rate limit failure: retry later; do not edit the offline lab to hide API issues.
