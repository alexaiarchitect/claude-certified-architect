# Mini Project Solution

This solution pack reads two documents, retries failed outputs, saves results, and writes a simple scorecard.

## Run Offline

```bash
python3 src/pipeline.py
```

## Run Live API Check

Live mode uses `ANTHROPIC_API_KEY` from your shell environment and defaults to Claude Sonnet 4.6:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 src/pipeline.py --live
```

The live check processes both sample documents, allows one bounded retry per document, and writes `build/results.json` plus `build/scorecard.json`.
