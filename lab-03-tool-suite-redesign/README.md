# LAB-03 Tool Suite Redesign

## Goal

Tighten an ambiguous tool suite into one that routes cleanly and returns machine-usable errors.

## Outcome

Students finish with:

- better tool descriptions
- cleaner required fields
- overlap reduction
- structured error handling

## Walkthrough Flow

Use this lab after completing the Module 4 lessons on tool boundaries, strict tool use, and structured error taxonomy.

1. Inspect the starter tool specs and identify overlap before rewriting anything.
2. Run the starter evaluator and confirm the expected warning:

```text
WARNING: handle_refund overlaps with resolve_charge_issue on ['charge', 'refund']
```

3. Compare the starter pair `handle_refund` and `resolve_charge_issue` with the solution split:

| Job | Solution tool |
| --- | --- |
| retrieve order facts before deciding | `lookup_order` |
| issue a validated duplicate-charge refund | `issue_refund` |
| route policy or manual-approval cases | `escalate_case` |

4. Check required fields in the solution specs:

| Tool | Required fields |
| --- | --- |
| `lookup_order` | `order_id` |
| `issue_refund` | `order_id`, `amount`, `reason` |
| `escalate_case` | `reason`, `case_summary` |

5. Run the solution evaluator and confirm:

- `Tool overlap check passed.`
- refund intent selects `issue_refund`
- lookup intent selects `lookup_order`
- policy review intent selects `escalate_case`

## Support Assets

Keep these course download pack assets nearby while completing the lab:

- `worksheets/tool-spec-worksheet.md`
- `worksheets/strict-tool-use-checklist.md`
- `cheat-sheets/tool-error-taxonomy-card.md`

Use them in this order: define the boundary, tighten the required input contract, then return structured error metadata when a call cannot execute safely.

## Run

```bash
cd solution
python3 src/evaluate_tools.py
```
