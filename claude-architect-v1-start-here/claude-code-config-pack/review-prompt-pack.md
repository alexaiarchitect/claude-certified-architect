# Review Prompt Pack

Use these prompts with M5.3 before turning a repeated workflow into a Claude Code skill. If a prompt becomes a recurring team habit, graduate it into `.claude/skills/<name>/SKILL.md`.

## Architecture Review Prompt

```text
Review this architecture decision.

Problem:
<one sentence>

Constraints:
<cost, reliability, maintenance, team, or timeline constraints>

Options:
<option A>
<option B>
<option C if needed>

Return:
1. the highest-risk decision
2. the option that best owns the failure mode
3. the tempting option to reject
4. the leanest acceptable recommendation
5. the validation step before shipping
```

## Risky-Change Review Prompt

```text
Review this change before implementation.

Change:
<what will change>

Risk signal:
<data access, tool boundary, validation, config scope, or reliability risk>

Return:
1. what could break
2. which layer owns the risk
3. the smallest safe implementation path
4. what must be tested
5. what should be documented for future maintainers
```

## Patchability Review Prompt

```text
Review this lesson or workflow for product drift.

Surface:
<API, Claude Code UI, config syntax, MCP, lab code, downloadable asset>

Return:
1. what is stable enough for video
2. what should live in notes or a downloadable
3. what can be fixed with an overlay or audio patch
4. what would require a rerecord
5. the shortest durable wording
```

## Prompt-To-Skill Graduation Rule

Keep a prompt as a prompt when:

- it is experimental
- it is used by one person
- the input shape changes every time
- the workflow is not worth maintaining

Promote it to a skill when:

- the same review flow is repeated
- multiple teammates need it
- the output shape should be consistent
- the workflow has clear inputs and steps
- it would make `CLAUDE.md` too long or procedural

## Exam Shortcut

| Failure signal | Owning surface |
| --- | --- |
| shared behavior is inconsistent | `CLAUDE.md` |
| sensitive access is too open | settings and deny rules |
| repeated workflow is retyped manually | skill |
| external system access is required | MCP |
| exact product UI changed | notes or patch overlay |

Do not choose a skill just because it sounds modern. Choose it when the failure is a repeated team workflow.
