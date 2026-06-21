# MCP-lite Decision Memo Prompt

Use this prompt when you need to decide whether an integration should use MCP, a simpler course download pack pattern, a Claude Code config surface, or no integration at all.

## Prompt

```text
Review this MCP-lite decision.

Context:
- Problem:
- External system or data source:
- User workflow:
- Current workaround:
- Risk if this is wrong:

Candidate surfaces:
- one-off context:
- existing tool:
- structured output or validation:
- Claude Code config surface:
- MCP server or connector:
- managed policy:

Make the decision:
1. Name the owning failure layer.
2. Decide MCP or non-MCP.
3. If MCP, name the surface: Messages API connector, Claude Code .mcp.json, or managed MCP policy.
4. If non-MCP, name the simpler lever.
5. Define the minimum scope: allowed tools/resources, denied actions, credential boundary, and owner.
6. Identify data and retention risk.
7. Identify context-load risk.
8. Reject at least two tempting alternatives.
9. Choose the patch path: notes only, overlay, audio patch, or rerecord.
10. Define the review trigger.

Output:
- Decision:
- Why this owns the failure:
- Minimum safe scope:
- Rejected alternatives:
- Remaining risk:
- Patch path:
- Review trigger:
```

## Example Decision Sentence

```text
Use Claude Code project MCP configuration for approved docs lookup because the workflow repeatedly needs external documentation access, but keep implementation details in notes because server setup and policy syntax are volatile.
```

