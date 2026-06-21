# LAB-04 Troubleshooting

## Common Failures

- keeping team instructions only in personal memory instead of `CLAUDE.md`
- missing deny rules for `.env` or `secrets`
- placing project skills under the old top-level `skills/` folder instead of `.claude/skills/`
- creating a skill with no `description`, workflow, or output shape
- using a stale `.mcp.json` shape without top-level `mcpServers`

## Fast Checks

1. Confirm `CLAUDE.md` exists in the repo root.
2. Confirm `.claude/settings.json` includes focused `Read(...)` deny rules.
3. Confirm `.claude/skills/architecture-review/SKILL.md` includes purpose, workflow, and output shape.
4. Confirm `.mcp.json` uses `mcpServers` and stays shallow unless a real integration is being configured.

## Expected Validator Behavior

The starter validator should fail with:

```text
Pack validation failed:
- Add deny rules for .env and secrets access
- Skill is missing a workflow section
```

The solution validator should pass. If it fails, fix the owning surface rather than adding a longer prompt.

## Live API Checks

LAB-04 intentionally stays offline. It validates Claude Code team configuration files, not the Messages API. Do not add an artificial Anthropic API call to make this lab look live.
