# Claude Code Scope Cheatsheet

Use this sheet with M5.2 when deciding where Claude Code team behavior should live. The exam shortcut is simple: pick the smallest stable surface that owns the failure.

## Core Surfaces

| Surface | Scope | Best use | Shared? |
| --- | --- | --- | --- |
| `CLAUDE.md` | project or user instructions | behavior, conventions, review flow, project context | yes when committed at project level |
| `.claude/settings.json` | project settings | team permissions, deny rules, hooks, MCP or plugin defaults | yes |
| `.claude/settings.local.json` | local project settings | personal experiments and machine-specific defaults | no |
| `~/.claude/settings.json` | user settings | personal defaults across projects | no |
| `~/.claude/CLAUDE.md` | user instructions | personal coding preferences and repeated reminders | no |
| managed settings | organization policy | non-overridable security and compliance defaults | yes, by policy |

## What Goes In `CLAUDE.md`

Use `CLAUDE.md` for guidance Claude should read at the start of a session:

- repo conventions and architecture context
- build, test, and validation commands
- review flow and decision style
- team safety reminders
- "always do this" rules that teammates should share

`CLAUDE.md` is not an enforcement layer. It shapes behavior through context. If the risk is access control, use settings.

## What Goes In Settings

Use settings for technical controls:

- `permissions.deny` for files, folders, and commands the team should avoid
- local-only overrides in `.claude/settings.local.json`
- shared project defaults in `.claude/settings.json`
- managed policy for organization-wide controls
- optional verification through `/status` during live setup

Common deny patterns:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Keep deny rules focused. Do not use settings as a dumping ground for project behavior that belongs in `CLAUDE.md` or in a skill.

## Precedence Model

When the same behavior is configured in multiple places, use this mental model:

```text
managed > command-line/session override > local > project > user
```

Practical meaning:

- managed policy wins when the organization needs a non-negotiable rule
- local settings can override shared project settings for one developer
- project settings beat user settings for a shared repo
- user settings are defaults only when nothing closer to the project says otherwise

## LAB-04 Anchor

The LAB-04 solution pack demonstrates the minimum team setup:

- `CLAUDE.md`: shared default behavior, review flow, and safety rules
- `.claude/settings.json`: deny rules for `.env`, `secrets`, and private keys
- `.claude/skills/architecture-review/SKILL.md`: repeatable architecture review workflow
- `.mcp.json`: project-scoped integration surface with top-level `mcpServers`
- `validate_pack.py`: mechanical check that required files and rules exist

Run the validator from the lab solution folder:

```bash
python3 validate_pack.py
```

## Exam Shortcut

| Failure signal | Owning surface |
| --- | --- |
| teammates get different behavior | `CLAUDE.md` or shared project instructions |
| sensitive files may be read accidentally | `.claude/settings.json` with `permissions.deny` |
| one developer needs a local-only preference | `.claude/settings.local.json` |
| everyone needs the same non-overridable rule | managed settings |
| a review workflow is repeated manually | skill |
| external system access is required | MCP configuration |
| exact UI flow changed | notes or patch overlay |

Do not answer with "write a better prompt" when the failure is caused by missing shared configuration.
