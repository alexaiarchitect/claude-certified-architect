# Mini Mock v1

## Q1
An agent loop is currently controlled by checking whether the assistant said “done.” What is the best fix?  
A. Add stronger instructions  
B. Route on `stop_reason`  
C. Increase context window  
D. Add more tools

## Q2
A subagent keeps missing key facts already known by the coordinator. What is the best change?  
A. Explicitly pass the required context bundle  
B. Let the subagent infer the missing facts  
C. Add a second coordinator  
D. Shorten the prompt

## Q3
A tool request succeeded but the final result is still incomplete. What should happen next?  
A. End the loop  
B. Retry the original user prompt without the tool result  
C. Append the tool result and continue the loop  
D. Delete the trace

## Q4
Which design most safely handles an unknown stop state?  
A. Ignore it and continue  
B. Escalate and inspect the raw payload  
C. Convert it to `end_turn`  
D. Remove logging

## Q5
Which option best supports bounded retries?  
A. Emotional wording  
B. Idempotency plus explicit retry criteria  
C. Larger model only  
D. Longer outputs

## Q6
Two tools both claim to handle charge disputes. What is the best first fix?  
A. Add a third tool  
B. Tighten boundaries and remove overlap  
C. Make both tools broader  
D. Hide one tool from logs

## Q7
Which field is most important in a structured tool error?  
A. `retryable`  
B. `font`  
C. `caption`  
D. `thumbnail`

## Q8
What does strict tool use primarily constrain?  
A. Final narration  
B. Tool input shape  
C. Student support volume  
D. Video length

## Q9
Which option is the best v1 treatment for MCP?  
A. Deep implementation lab  
B. Narrow fit/non-fit framing plus note pack  
C. Ignore it completely  
D. Replace reliability content with it

## Q10
What should happen first when a lab zip is broken?  
A. Wait for the next major release  
B. Fix the downloadable first  
C. Remove the lab  
D. Rewrite the quiz

## Q11
Why keep shared Claude Code guidance in `CLAUDE.md`?  
A. It hides team standards  
B. It creates repo-level, reviewable defaults  
C. It replaces settings entirely  
D. It avoids documentation

## Q12
Which control best reduces accidental access to `.env` files?  
A. Longer prompts  
B. Deny rules  
C. More quizzes  
D. More screenshots

## Q13
What makes a skill reusable?  
A. A vague paragraph  
B. Purpose, inputs, and workflow  
C. One clever sentence  
D. No invocation guidance

## Q14
Why is M5 treated as high drift?  
A. It has no architecture value  
B. Config examples and UI flows can change quickly  
C. It has no labs  
D. It never uses notes

## Q15
What should come before polishing an extraction prompt?  
A. Pass/fail criteria  
B. More screenshots  
C. New branding  
D. A second mock

## Q16
What is the main job of validation feedback in a retry loop?  
A. Make the response longer  
B. Tell the next attempt exactly what failed  
C. Increase randomness  
D. Replace the schema

## Q17
Which combination best fits a reliable extraction system?  
A. Plain JSON only  
B. Structured output enforcement plus validation and retry  
C. Screenshots plus captions  
D. More tools only

## Q18
A lesson’s UI example drifted, but the core principle is still right. What is the best default response?  
A. Full rerecord immediately  
B. Notes-only or overlay patch first  
C. Delete the lesson  
D. Ignore it forever

## Q19
What is the best-answer rule for this course?  
A. Pick the newest feature  
B. Pick the lowest-risk viable design under constraints  
C. Pick the answer with the most components  
D. Pick the shortest answer

## Q20
What makes an item a strong v1.1 candidate?  
A. It increases runtime only  
B. High demand, high exam value, low maintenance burden  
C. It requires a new platform  
D. It depends on rerecording half the course
