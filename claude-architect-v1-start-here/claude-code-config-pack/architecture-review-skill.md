# Architecture Review Skill

Use this as a copyable example for a project-level Claude Code skill.

Recommended location:

```text
.claude/skills/architecture-review/SKILL.md
```

Invoke it directly with `/architecture-review`, or let Claude Code discover it when a request matches the `description`.

## Copyable Skill

```markdown
---
description: Compare architecture options and recommend the leanest maintainable choice. Use when a change has multiple viable designs, long-term maintenance risk, or certification-style tradeoffs.
---

# Architecture Review

## When to Use

Use this skill when:

- the decision is architectural, not just syntactic
- multiple options could solve the problem
- maintainability, safety, or reliability tradeoffs matter
- the team needs a reviewable decision frame

Do not use this skill for routine formatting, one-line fixes, or product UI trivia.

## Inputs

Ask for or infer:

- problem statement
- current constraints
- options being considered
- failure mode or risk signal
- files, logs, or examples that ground the review

## Workflow

1. Restate the problem in one sentence.
2. Identify the highest-risk decision.
3. Compare up to three viable options.
4. Reject tempting distractors explicitly.
5. Recommend the leanest acceptable choice.
6. Note what should be tested, documented, or patched later.

## Output Shape

Return:

- recommended option
- why it owns the failure mode
- rejected option and why
- test or validation step
- follow-up note if the workflow is volatile

## Review Guardrails

- Prefer stable system changes over prompt-only fixes when the issue is architectural.
- Keep global `CLAUDE.md` concise; move repeated procedures into skills.
- Do not recommend broad rewrites when a smaller durable control surface owns the failure.
- Separate source-truth concerns from UI drift and patchable notes.
```

## Exam Shortcut

If the failure is repeated manual review work, choose a skill. If the failure is shared behavior, choose `CLAUDE.md`. If the failure is access control, choose settings. If the failure is external system access, choose MCP.
