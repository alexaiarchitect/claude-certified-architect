# LAB-04 Claude Code Team Setup

## Goal

Package a team-ready Claude Code setup with repo instructions, settings scopes, deny rules, and one reusable skill.

## Outcome

Students finish with a validation-friendly config pack they can reuse in real projects.

## Walkthrough Flow

M5.4 uses this lab as a deterministic before/after screen demo:

1. Run the starter validator and confirm the expected failure.
2. Inspect the missing guardrails in the starter pack.
3. Compare the solution pack surfaces.
4. Run the solution validator and confirm the pack is ready.

The target team setup is small:

- `CLAUDE.md` for shared repo behavior and review flow
- `.claude/settings.json` for project settings and `permissions.deny`
- `.claude/skills/architecture-review/SKILL.md` for the reusable review workflow
- `.mcp.json` for a shallow project-scoped integration example
- `validate_pack.py` for mechanical validation

## Expected Results

The starter should fail with missing deny rules and a missing skill workflow. The solution should print:

```text
Pack validation passed.
```

## Run

```bash
cd solution
python3 validate_pack.py
```
