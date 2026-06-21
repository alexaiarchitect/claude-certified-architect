# Claude Code Team Model Note

Use this note before the Claude Code demos. The goal is to reason about stable team control surfaces instead of chasing every UI detail.

## Mental Model

Claude Code is a terminal-based agent operating in a local repository. It can inspect files, propose edits, run commands when allowed, and use configured tools. Treat it as an operating environment with guardrails, not as a blank chat window.

Strong team setup answers three questions:

1. What shared behavior should every teammate get?
2. What access should be allowed, denied, or reviewed?
3. Which repeatable workflows should be packaged instead of retyped?

## Stable Control Surfaces

| Need | Stable surface | Use for |
| --- | --- | --- |
| Shared repo behavior | `CLAUDE.md` | Project conventions, review flow, common commands, architecture context |
| Tool and file access | `.claude/settings.json` | Permissions, deny rules, environment defaults, review expectations |
| Repeatable workflow | Skill | Packaged review, planning, debugging, or team-specific workflow |
| External tools/data | `.mcp.json` | Project-level MCP server configuration and integration examples |
| Deterministic guard | Hook | Advanced automatic checks before or after tool use |

Keep M5.1 at this control-surface level. M5.2 covers `CLAUDE.md` and settings scopes in detail. M5.3 covers skills and review workflows. M5.4 validates the full LAB-04 pack.

## Scope And Precedence Concept

Claude Code behavior can come from several scopes. Exact product details can evolve, but the team design principle is stable: shared, reviewable rules should live close to the project, and organization policy should override personal preference.

| Scope | Typical owner | Best use |
| --- | --- | --- |
| Personal memory | Individual | Personal preferences and local habits |
| Repo or project memory | Team | Shared instructions that belong with the codebase |
| Local project settings | Individual | Local-only experimentation and personal defaults |
| Shared project settings | Team | Reviewable permissions and team defaults |
| Enterprise policy | Organization | Non-negotiable security or compliance controls |

Avoid relying on personal memory for team behavior. If two teammates need the same behavior, put it in the course download pack pattern: repo instructions, settings, and reusable skills.

## Team Safety Defaults

Use these defaults before adding advanced workflow automation:

- Put shared behavior in `CLAUDE.md`, not in a private prompt habit.
- Deny sensitive files such as `.env`, secrets folders, and private keys.
- Require review or explicit planning for risky changes.
- Keep skills focused on repeatable workflows with clear invocation guidance.
- Keep volatile UI specifics in notes or patch overlays, not long video claims.
- Validate the pack mechanically before treating it as team-ready.

## LAB-04 Bridge

LAB-04 turns the model into a reusable config pack:

| LAB-04 piece | What it proves |
| --- | --- |
| Starter pack | Shows what is missing when defaults are incomplete |
| Solution `CLAUDE.md` | Shared repo-level behavior and review flow |
| Solution `.claude/settings.json` | Deny rules and review defaults |
| Solution `.claude/skills/architecture-review/SKILL.md` | Repeatable workflow packaged outside the base instructions |
| Validator | Mechanical check that required team surfaces exist |

Use the validator as the final gate:

```bash
cd lab-04-claude-code-team-setup/solution
python3 validate_pack.py
```

## Exam Shortcut

Pick the stable owning surface:

| Failure signal | Prefer |
| --- | --- |
| Teammates get different behavior | `CLAUDE.md` or shared repo instructions |
| Sensitive files may be read accidentally | settings deny rules |
| A review workflow is repeated manually | Skill |
| External system access is needed | MCP configuration |
| A rule must run every time | Hook or deterministic guard |
| Exact UI flow changed | notes or overlay patch, not a full rerecord |

The best answer is usually the smallest durable control surface that owns the failure.
