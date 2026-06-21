# Exam Answer Framework

Use this framework for every quiz, scenario check, and mini mock question.

The best answer is usually the lowest-risk viable design under the stated constraints. Do not default to the newest feature, the biggest system, or more prompt text.

## Five-Step Ranking Loop

1. What failed?
2. Which layer owns that failure?
3. Which lever fixes that layer most directly?
4. What lower-maintenance option still works?
5. What tempting distractor solves the wrong problem?

## Failure Layers

| Layer | Common Signal | Strong Lever |
| --- | --- | --- |
| Agentic loop control | Loop ends early, loops forever, or ignores tool result lifecycle | Route on response state and append tool results correctly |
| Coordinator/subagent orchestration | Subagents miss context, duplicate work, or cover the wrong scope | Pass explicit structured context and route through coordinator |
| Tool selection | Similar tools are confused or broad tools are misused | Clarify names, descriptions, boundaries, and scoped access |
| Tool error handling | Caller cannot decide retry, stop, or escalate | Return structured error metadata and retryability |
| Claude Code team config | Team behavior differs across developers | Move shared rules into repo-level config and reviewable skills |
| Structured output | Output looks like JSON but breaks downstream | Enforce schema at the right interface and validate semantics |
| Validation retry | Retry repeats the same failure | Feed specific validation errors into the next attempt |
| Context and provenance | Facts, dates, source links, or confidence get lost | Preserve structured facts, source mapping, and review thresholds |
| Escalation | System keeps trying when policy or ambiguity blocks progress | Ask for clarification or route to human review |

## Distractor Patterns

| Distractor | Why It Is Tempting | Why It Is Often Wrong |
| --- | --- | --- |
| More prompting | It feels cheap and fast | It may not enforce deterministic control or business rules |
| More tools | It feels more capable | It can increase selection confusion and scope misuse |
| More retries | It feels resilient | It wastes work when errors are non-retryable or information is absent |
| Bigger model or context | It feels safer | It may not fix attention dilution, validation gaps, or wrong architecture |
| Newest feature | It sounds advanced | The exam often rewards the simplest reliable lever |

## Final Answer Template

Use this short justification after choosing an answer:

```text
The failure is [failure].
The owning layer is [layer].
The best lever is [choice] because it directly fixes [root cause].
I rejected [distractor] because it solves [wrong layer] or adds [unneeded cost/risk].
```

## Fast Elimination Rules

- Reject answers that solve a different failure than the scenario describes.
- Reject prompt-only answers when the scenario requires deterministic enforcement.
- Reject infrastructure-heavy answers when a simpler interface or configuration fix directly addresses the issue.
- Reject retry answers when the failure is policy, permission, missing source information, or ambiguity.
- Prefer answers that preserve observability, structured state, and clear recovery paths.
