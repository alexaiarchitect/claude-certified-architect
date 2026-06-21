# Claude Code Team Conventions

## Default Behavior

- inspect the repo before making recommendations
- prefer stable system changes over flashy one-off fixes
- explain architectural tradeoffs directly

## Review Flow

1. summarize the problem in one sentence
2. identify the highest-risk decision
3. propose the leanest acceptable fix
4. note what should stay in notes rather than video

## Safety Rules

- avoid reading `.env` and secrets by default
- do not bypass deny rules
- log assumptions when a workflow is volatile
