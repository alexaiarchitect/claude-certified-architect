# LAB-03 Solution

The solution pack removes the ambiguous refund overlap and returns structured errors when payloads are incomplete.

## Run Offline

```bash
python3 src/evaluate_tools.py
```

## Run Live API Check

Live mode uses `ANTHROPIC_API_KEY` from your shell environment and defaults to Claude Sonnet 4.6:

```bash
export ANTHROPIC_API_KEY=your-key
export ANTHROPIC_MODEL=claude-sonnet-4-6
python3 src/evaluate_tools.py --live
```

The live check sends the local tool specs as Anthropic tools and validates that Claude selects the expected tool with complete inputs. It does not execute real side effects.
