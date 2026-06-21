# MCP-lite Note Pack

Use this note when a scenario mentions external systems, MCP servers, Claude Code integrations, connectors, resources, or tool access. The v1 goal is not to build a full MCP server. The goal is to decide whether MCP is the right integration boundary.

## Core Idea

MCP is an integration boundary for external tools, data, resources, and workflows.

Pick MCP when the system needs a reusable, shared way to connect an AI application to an outside capability. Do not pick MCP just because a prompt is vague, a JSON schema is weak, a tool description overlaps, or a one-off document needs to be pasted into context.

## Fit Cases

MCP is a good candidate when:

- the task repeatedly needs external-system access
- the integration should be shared across users or projects
- an approved server already exists
- the external system exposes useful tools, resources, or prompts
- credentials and permissions can be handled through a controlled integration surface
- the team needs the same integration behavior to be reviewable and patchable

Examples:

- issue tracker lookup for repeated coding tasks
- docs or database resource lookup during development
- approved internal tool access in Claude Code
- shared integration config for a team workflow

## Non-Fit Cases

Do not reach for MCP first when the owning failure is:

| Failure | Better first lever |
| --- | --- |
| one-off context | attach or paste the needed source |
| vague prompt | define criteria or rewrite instructions |
| invalid final JSON | structured output or schema enforcement |
| wrong extracted fact | semantic validation and source checks |
| overlapping tools | tool names, descriptions, and boundaries |
| invalid tool arguments | strict tool input schema |
| Claude Code behavior drift | `CLAUDE.md`, settings, skills, or notes |
| lost provenance | reliability checklist and source tracking |

## Main Surfaces

| Surface | Use it for | Keep shallow in v1 |
| --- | --- | --- |
| Messages API MCP connector | Remote MCP tools through the API request | exact beta header, transport details, and provider availability |
| Claude Code `.mcp.json` | Project-scoped MCP servers for local/team development | install/auth flows and server execution |
| Managed MCP policy | Organization-level control over allowed servers | enterprise deployment mechanics |

Current implementation details can change. Keep exact setup commands, beta headers, tool-search behavior, and managed-policy syntax in notes or patchable docs rather than long video explanations.

## Current Caveats To Remember

- The Messages API MCP connector uses remote server definitions and supports MCP tool calls.
- Claude Code can use project `.mcp.json` with top-level `mcpServers`.
- Claude Code MCP can expose tools, resources, and prompts depending on the server and client support.
- Some details are volatile: beta headers, tool loading behavior, managed policy fields, provider availability, and exact UI flows.
- Data-retention and Zero Data Retention eligibility can differ by MCP feature. Treat this as a risk-control question, not a memorized slogan.

## Risk Controls

Before choosing MCP, answer:

- Which external system is needed?
- Is there an approved server already?
- What credentials or tokens are required?
- What data can leave the local project or application boundary?
- Which tools or resources should be allowed?
- What should be denied?
- How much context will tool/resource descriptions consume?
- Who owns updates if the server, API, or policy changes?
- What is the patch path if the exact MCP behavior drifts?

## Exam Shortcut

Pick MCP when external-system integration owns the failure.

Reject MCP when the failure is better owned by prompt criteria, schema enforcement, tool boundaries, validation, retry policy, Claude Code configuration, provenance, or human review.

Use this sentence:

```text
Choose MCP only if the scenario needs a reusable external integration boundary; otherwise fix the layer that actually failed.
```

