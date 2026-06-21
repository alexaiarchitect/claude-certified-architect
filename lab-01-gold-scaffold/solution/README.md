# LAB-01 Solution

This solution pack shows the full baseline scaffold for:

- env loading
- request skeleton display
- stop reason routing
- usage logging
- safe next-action hints

## Run Offline

```bash
python3 src/app.py
```

## Run Live API Check

Live mode uses `ANTHROPIC_API_KEY` from your shell environment and defaults to Claude Sonnet 4.6:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 src/app.py --live
```

Expected live output includes a response ID, model, `stop_reason`, and token usage. The script never prints the API key.
