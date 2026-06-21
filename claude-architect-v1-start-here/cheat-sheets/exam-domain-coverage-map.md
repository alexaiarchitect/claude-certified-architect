# Exam Domain Coverage Map

This map connects the official certification domains to the lean v1 course.

Lean v1 is intentionally focused. Some official task statements are covered deeply through labs. Others are covered as decision framing or self-study prompts to avoid overbuilding volatile sections before launch.

## Coverage Summary

| Domain | Official Weight | V1 Coverage | Primary Course Assets |
| --- | ---: | --- | --- |
| Domain 1: Agentic Architecture & Orchestration | 27% | Medium | M2 loop control, M2 safe retries, LAB-01, M6 reliability |
| Domain 2: Tool Design & MCP Integration | 18% | Strong for tool design, light for MCP implementation | M4, LAB-03, M6.2 MCP-lite |
| Domain 3: Claude Code Configuration & Workflows | 20% | Strong for team config, light for CI/CD depth | M5, LAB-04, Claude Code config pack |
| Domain 4: Prompt Engineering & Structured Output | 20% | Strong | M3, LAB-02, mini project |
| Domain 5: Context Management & Reliability | 15% | Medium | M2 safe control, M6 reliability checklist, all labs |

## Domain 1: Agentic Architecture & Orchestration

Covered in v1:

- Agentic loop lifecycle and `stop_reason` routing
- Tool result continuation
- Retry, escalation, and safe control basics
- Failure analysis through logs

Lean v1 gap to self-study:

- Full Agent SDK hooks
- Rich coordinator/subagent spawning
- Forking and named session resumption
- Deep multi-agent decomposition builds

Self-study action:

- For any multi-agent question, identify whether the failure is loop control, context passing, coordinator decomposition, or deterministic enforcement.

## Domain 2: Tool Design & MCP Integration

Covered in v1:

- Tool descriptions and boundaries
- Overlap removal
- Strict tool inputs
- Structured error taxonomy
- Retryability and escalation metadata

Lean v1 gap to self-study:

- Full MCP server implementation
- MCP resources and catalogs
- Project-level versus user-level MCP server scoping in depth

Self-study action:

- For MCP questions, focus first on tool/resource fit, scope, credentials, and whether existing servers are enough before custom implementation.

## Domain 3: Claude Code Configuration & Workflows

Covered in v1:

- `CLAUDE.md` team defaults
- Settings scopes and deny rules
- Skills as reusable workflows
- Team setup lab

Lean v1 gap to self-study:

- Custom slash commands in depth
- `.claude/rules/` path-specific loading
- Claude Code CI/CD flags and JSON output details
- Plan mode versus direct execution edge cases

Self-study action:

- For Claude Code questions, ask whether behavior should live in user memory, repo configuration, path-scoped rules, skills, commands, or CI invocation.

## Domain 4: Prompt Engineering & Structured Output

Covered in v1:

- Criteria-first prompting
- Structured output versus plain JSON
- Tool JSON versus final structured output
- Validation, retry feedback, and extraction quality
- Mini project extraction system

Lean v1 gap to self-study:

- Few-shot prompting depth
- Batch processing strategy details
- Multi-pass review architecture beyond conceptual framing

Self-study action:

- For extraction questions, separate syntax enforcement from semantic validation. Schemas do not prove totals, provenance, or source truth.

## Domain 5: Context Management & Reliability

Covered in v1:

- Reliability checklist
- Escalation and human review framing
- Failure boundaries and provenance basics
- Changelog/update model for course maintenance

Lean v1 gap to self-study:

- Long-session scratchpad patterns
- Stratified sampling and confidence calibration
- Detailed source-conflict handling in multi-source synthesis

Self-study action:

- For reliability questions, identify whether the system lost facts, lost provenance, misread confidence, failed to escalate, or collapsed distinct sources into one summary.

## Review Priority

If your time is limited:

1. Domain 1 and Domain 4 first: they have high weight and strong architectural failure modes.
2. Domain 3 next: many questions are configuration-placement questions.
3. Domain 2 and Domain 5 together: tool boundaries, MCP fit, context, and escalation often overlap in scenarios.
