# Extraction Criteria Worksheet

Use this before writing or polishing an extraction prompt. The goal is to define what a valid result means, where the result can safely be incomplete, and what the validator should reject.

## Source Example

Use the LAB-02 invoice as the reference example:

- invoice ID: `INV-2048`
- company: `Northwind Labs`
- currency: `USD`
- subtotal: `1500.00`
- tax: `120.00`
- total: `1620.00`
- line items:
  - `Architecture Review Sprint`, qty `1`, unit price `1200.00`
  - `Reliability Checklist Pack`, qty `2`, unit price `150.00`

## 1. Required Fields

List fields that must appear for downstream automation to continue.

| Field | Required? | Source evidence | Reject if missing? |
| --- | --- | --- | --- |
| `invoice_id` | Yes | `Invoice ID: INV-2048` | Yes |
| `company` | Yes | `Company: Northwind Labs` | Yes |
| `currency` | Yes | `Currency: USD` | Yes |
| `subtotal` | Yes | `Subtotal: 1500.00` | Yes |
| `tax` | Yes | `Tax: 120.00` | Yes |
| `total` | Yes | `Total: 1620.00` | Yes |
| `line_items` | Yes | two source rows under `Line Items` | Yes |

## 2. Optional Or Nullable Fields

Use optional or nullable fields when the source may legitimately omit a value. Do not force the model to invent values just to satisfy a schema.

| Field | Why it may be absent | Accepted value when absent | Review trigger |
| --- | --- | --- | --- |
| `purchase_order` | invoice may not include a PO number | `null` | downstream requires PO matching |
| `due_date` | source may omit payment terms | `null` | billing workflow requires due date |
| `customer_contact` | source may not name a person | `null` | human follow-up depends on contact |

## 3. Semantic Checks

Schema shape is not enough. Add checks that prove the extracted values agree with the source.

| Check | Pass condition | Fail condition |
| --- | --- | --- |
| Required fields | every required field exists | any required field is missing |
| Line item count | two line items are present | one or more source line items are missing |
| Subtotal math | `1200.00 + (2 * 150.00) = 1500.00` | extracted subtotal does not match line items |
| Total math | `1500.00 + 120.00 = 1620.00` | extracted total is `1500.00` or another mismatch |
| Currency | all money values use `USD` | currency is missing, mixed, or fabricated |

## 4. False-Positive Risks

Name the categories that would make users stop trusting the extraction.

| Risk | Example | Architecture response |
| --- | --- | --- |
| Fabricated value | model invents a purchase order | allow `null`; reject unsupported values |
| Missing source row | only one line item appears | validate line item count and totals |
| Wrong arithmetic | total equals subtotal | validate semantic math, not only JSON shape |
| Wrong field placement | tax value appears as total | compare field values against source labels |

## 5. Source-Absence Rule

If the source document does not contain a value, the correct extraction is usually `null`, `unclear`, or a structured review flag. It is not a confident fabricated answer.

Use this rule in prompts and validators:

```text
If the source does not contain the value, return null and include the field in review_notes. Do not infer or invent values.
```

## 6. Validation Feedback

Retry feedback should be specific enough to change the next attempt.

Weak feedback:

```text
Try again and be more accurate.
```

Useful feedback:

```text
Return the full schema. Fix these exact issues: total should be 1620.00; two line items were expected.
```

## 7. Saved Artifact Expectation

A valid extraction is not finished until the validated result is saved for downstream use.

Acceptance criteria:

- full schema returned
- required fields present
- optional missing values represented as `null`, `unclear`, or a review flag
- semantic checks pass
- retry feedback generated for failures
- final validated JSON saved as the downstream artifact
