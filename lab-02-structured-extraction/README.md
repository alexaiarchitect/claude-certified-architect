# LAB-02 Structured Extraction

## Goal

Build a deterministic extraction loop with validation, retry feedback, and a saved final artifact.

## Outcome

Students finish with a pipeline that:

- reads a source document
- checks extraction output against a schema contract
- retries with explicit feedback
- writes the validated JSON result

## Run

```bash
cd solution
python3 src/extract.py
```

## After The Lab

Read `notes/mini-project-kickoff.md` before starting the structured extraction mini project.
