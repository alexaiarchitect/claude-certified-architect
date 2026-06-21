# ADR Kit

Use this kit to preserve architecture reasoning while you work through the course.

The goal is not paperwork. The goal is to make a decision reusable: what failed, what you chose, what you rejected, and what risk remains.

## Files

- `ADR-template.md`: use when the choice affects architecture, workflow behavior, reliability, or team defaults.
- `tradeoff-memo-template.md`: use when the main value is comparing options under constraints.
- `risk-note-template.md`: use when a choice is acceptable for v1 but needs a patch path or review trigger.
- `examples/ADR-001-strict-tool-use-vs-prompt-only.md`: example ADR used in M1.3.
- `mcp-lite-decision-memo-prompt.md`: M6.2 prompt for deciding whether MCP is the right integration boundary.

## Which Artifact Should I Use?

| Situation | Use | Keep It To |
| --- | --- | --- |
| You are making a durable architecture or behavior choice | ADR | 1 page |
| You need to explain why one option wins and others are deferred | Tradeoff memo | 10-15 lines |
| You found a known weakness, volatile detail, or maintenance concern | Risk note | 5-8 lines |
| You need to decide if MCP is the right boundary | MCP-lite decision memo | 10-15 lines |

## Course Rule

For labs and mini projects, write the shortest artifact that explains the decision.

Do not document every implementation detail. Document the decision that would help you answer an exam scenario or maintain the system later.

## Review Prompt

After each quiz, scenario check, or lab, ask:

```text
What was the decision?
What alternative was tempting?
Why was that alternative weaker?
What risk remains?
When would I revisit the choice?
```
