# Mini Project Kickoff Note

Use this note after you complete LAB-02. The lab is the single-document pattern; the mini project scales that pattern to multiple documents.

## What Carries Forward

- source contract: know what facts the document must support
- schema boundary: require a predictable extraction shape
- semantic validation: check totals, line items, and source-supported values
- exact retry feedback: tell the next attempt what failed
- saved artifact: write only the validated result downstream
- simple scorecard: record which documents passed and how many attempts they needed
- ADR or tradeoff note: explain why this loop is better than plain JSON cleanup

## What Not To Add In V1

Do not expand this into:

- live API integration
- a full capstone
- broad orchestration
- a second mock-exam project
- enterprise governance beyond the tradeoff note

The goal is a small repeatable extraction system, not a platform rewrite.

## Next Files

Open these next:

- `mini-project/structured-extraction-system/README.md`
- `mini-project/structured-extraction-system/starter/README.md`
- `mini-project/structured-extraction-system/rubric.md`
- `mini-project/structured-extraction-system/adr-prompt.md`

## Completion Rule

Before starting the mini project, confirm that LAB-02 can:

- load the invoice source
- report the first failed extraction
- build exact retry feedback
- accept the corrected result
- save the validated JSON artifact
