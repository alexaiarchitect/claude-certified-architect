from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DOC_PATH = BASE_DIR / "data" / "sample_invoice.txt"

FAKE_MODEL_OUTPUT = {
    "invoice_id": "INV-2048",
    "company": "Northwind Labs",
    "currency": "USD",
    "subtotal": 1500.0,
    "tax": 120.0,
    "total": 1500.0,
    "line_items": [{"name": "Architecture Review Sprint", "qty": 1, "unit_price": 1200.0}],
}


def validate_extraction(result: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if result.get("total") != 1620.0:
        errors.append("Total should be 1620.0")
    items = result.get("line_items", [])
    if len(items) < 2:
        errors.append("Two line items were expected")
    return errors


def main() -> None:
    print("Loaded source document from", DOC_PATH)
    print("First-pass model output:")
    print(json.dumps(FAKE_MODEL_OUTPUT, indent=2))
    errors = validate_extraction(FAKE_MODEL_OUTPUT)
    if errors:
        print("Validation failed. Next step: implement retry feedback.")
        for error in errors:
            print("-", error)
    else:
        print("Unexpected pass. Tighten the starter failure case.")


if __name__ == "__main__":
    main()
