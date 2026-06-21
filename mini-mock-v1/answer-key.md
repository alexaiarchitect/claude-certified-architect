# Mini Mock v1 Answer Key

## Q1

Correct: B
Related lecture: M2.2

Rationales:
- A. Incorrect — stronger instructions still leave loop control dependent on fragile assistant wording.
- B. Correct — loop control should route on `stop_reason`, which is the response-state signal designed for this decision.
- C. Incorrect — a larger context window does not fix the loop's control condition.
- D. Incorrect — more tools add choices but do not solve the termination signal.

## Q2

Correct: A
Related lecture: M6.1

Rationales:
- A. Correct — subagents need the required context bundle passed explicitly so they can make reliable decisions.
- B. Incorrect — inference is fragile when required facts are already known by another component.
- C. Incorrect — adding another coordinator increases complexity without fixing the missing-context boundary.
- D. Incorrect — shortening the prompt may remove even more context.

## Q3

Correct: C
Related lecture: M2.2

Rationales:
- A. Incorrect — ending the loop after tool success can still leave the final user-facing result incomplete.
- B. Incorrect — retrying the original prompt without the tool result discards useful state.
- C. Correct — the tool result should be appended and the loop should continue so the assistant can produce the final answer.
- D. Incorrect — deleting the trace removes evidence needed for debugging and review.

## Q4

Correct: B
Related lecture: M2.3

Rationales:
- A. Incorrect — ignoring an unknown stop state can create unsafe or uncontrolled behavior.
- B. Correct — unknown states should stop the normal path, preserve the raw payload, and escalate for inspection.
- C. Incorrect — converting unknown states to `end_turn` hides a control condition the system does not understand.
- D. Incorrect — removing logging makes the unknown state harder to diagnose.

## Q5

Correct: B
Related lecture: M2.3

Rationales:
- A. Incorrect — emotional wording does not make a retry safe or deterministic.
- B. Correct — bounded retries require idempotency plus explicit criteria for when another attempt is allowed.
- C. Incorrect — a larger model does not remove side-effect or retry-safety concerns.
- D. Incorrect — longer outputs do not define safe retry conditions.

## Q6

Correct: B
Related lecture: M4.1

Rationales:
- A. Incorrect — adding a third tool increases routing ambiguity before the overlap is fixed.
- B. Correct — tightening boundaries and removing overlap is the first fix for tool-selection confusion.
- C. Incorrect — broader tools make the overlap worse.
- D. Incorrect — hiding a tool from logs reduces observability rather than improving the design.

## Q7

Correct: A
Related lecture: M4.3

Rationales:
- A. Correct — `retryable` tells the system whether another attempt is appropriate.
- B. Incorrect — `font` is presentation metadata and irrelevant to structured tool errors.
- C. Incorrect — `caption` does not classify the recovery path.
- D. Incorrect — `thumbnail` is not part of a useful tool error contract.

## Q8

Correct: B
Related lecture: M4.2

Rationales:
- A. Incorrect — strict tool use is not about narration quality.
- B. Correct — strict tool use primarily constrains the shape and safety of tool inputs.
- C. Incorrect — support volume may improve indirectly, but it is not the direct control.
- D. Incorrect — video length has no relationship to runtime tool input safety.

## Q9

Correct: B
Related lecture: M6.2

Rationales:
- A. Incorrect — a deep MCP lab is intentionally deferred because it is volatile and maintenance-heavy.
- B. Correct — lean v1 should use narrow fit/non-fit framing plus note-backed updates.
- C. Incorrect — ignoring MCP completely leaves students without exam-safe framing.
- D. Incorrect — reliability content is core and should not be replaced by MCP coverage.

## Q10

Correct: B
Related lecture: M1.1

Rationales:
- A. Incorrect — waiting for a major release leaves students blocked.
- B. Correct — a broken lab zip should be fixed first because it is the student-facing executable asset.
- C. Incorrect — removing the lab destroys a core learning asset when a patch is usually enough.
- D. Incorrect — rewriting the quiz does not repair the broken downloadable.

## Q11

Correct: B
Related lecture: M5.2

Rationales:
- A. Incorrect — team standards should be visible and reviewable, not hidden.
- B. Correct — `CLAUDE.md` creates repo-level, inspectable, shared defaults for the team.
- C. Incorrect — `CLAUDE.md` does not replace settings entirely; settings still control scopes and permissions.
- D. Incorrect — the file is documentation-as-configuration, not a way to avoid documentation.

## Q12

Correct: B
Related lecture: M5.2

Rationales:
- A. Incorrect — longer prompts are weaker than explicit access controls.
- B. Correct — deny rules are the direct file-access control for reducing accidental access to `.env` files.
- C. Incorrect — quizzes test knowledge but do not enforce access boundaries.
- D. Incorrect — screenshots document a flow; they do not prevent file access.

## Q13

Correct: B
Related lecture: M5.3

Rationales:
- A. Incorrect — a vague paragraph is not enough to make a workflow repeatable.
- B. Correct — a reusable skill needs a clear purpose, expected inputs, and workflow.
- C. Incorrect — one clever sentence does not provide operational guidance.
- D. Incorrect — without invocation guidance, users will not know when or how to apply the skill.

## Q14

Correct: B
Related lecture: M5.1

Rationales:
- A. Incorrect — M5 has architecture value; the risk is drift, not lack of value.
- B. Correct — config examples and UI flows can change quickly, so M5 needs a patchable treatment.
- C. Incorrect — M5 includes a lab and is not high drift because it lacks practice.
- D. Incorrect — notes are exactly how volatile M5 details should be maintained.

## Q15

Correct: A
Related lecture: M3.1

Rationales:
- A. Correct — pass/fail criteria define what a successful extraction means before prompt polish.
- B. Incorrect — screenshots do not define extraction correctness.
- C. Incorrect — branding is irrelevant until the extraction contract is measurable.
- D. Incorrect — a second mock does not improve the prompt design process.

## Q16

Correct: B
Related lecture: M3.3

Rationales:
- A. Incorrect — longer responses are not necessarily more valid.
- B. Correct — validation feedback should tell the next attempt exactly what failed.
- C. Incorrect — retry feedback should reduce randomness, not increase it.
- D. Incorrect — feedback works with the schema and validation; it does not replace them.

## Q17

Correct: B
Related lecture: M3.3

Rationales:
- A. Incorrect — plain JSON alone is too weak because it lacks robust enforcement and validation.
- B. Correct — reliable extraction combines structured output enforcement with validation and retry.
- C. Incorrect — screenshots and captions do not make extraction outputs reliable.
- D. Incorrect — more tools alone do not validate extracted data.

## Q18

Correct: B
Related lecture: M1.1

Rationales:
- A. Incorrect — a full rerecord is too heavy when the principle is still correct.
- B. Correct — note-only or overlay patches preserve the lesson while correcting volatile UI details.
- C. Incorrect — deleting the lesson removes stable content that still has value.
- D. Incorrect — ignoring known drift creates trust and exam-prep risk.

## Q19

Correct: B
Related lecture: M6.3

Rationales:
- A. Incorrect — novelty can be a distractor when it adds risk without solving the constraint.
- B. Correct — best-answer reasoning means choosing the lowest-risk viable design under the stated constraints.
- C. Incorrect — more components usually increase complexity and maintenance burden.
- D. Incorrect — the shortest answer may still be incomplete or target the wrong layer.

## Q20

Correct: B
Related lecture: M6.4

Rationales:
- A. Incorrect — more runtime alone is not evidence of student value.
- B. Correct — strong v1.1 candidates combine high demand, high exam value, and low maintenance burden.
- C. Incorrect — requiring a new platform increases operating cost and should not be a default expansion trigger.
- D. Incorrect — rerecording half the course is a high-maintenance expansion, not a lean v1.1 candidate.
