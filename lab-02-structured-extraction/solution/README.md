# LAB-02 Solution

This solution pack retries once with explicit feedback and writes a validated extraction artifact into `build/`.

## Run Offline

```bash
python3 src/extract.py
```

## Run Live API Check

Live mode uses `ANTHROPIC_API_KEY` from your shell environment and defaults to Claude Sonnet 4.6:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 src/extract.py --live
```

The live check asks Claude to extract the sample invoice as JSON, validates totals and line items, and writes `build/validated_extraction.json` only after validation passes.
