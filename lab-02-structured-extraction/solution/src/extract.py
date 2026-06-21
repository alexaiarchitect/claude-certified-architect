from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib import error, request

BASE_DIR = Path(__file__).resolve().parents[1]
DOC_PATH = BASE_DIR / "data" / "sample_invoice.txt"
BUILD_DIR = BASE_DIR / "build"
OUTPUT_PATH = BUILD_DIR / "validated_extraction.json"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-6"

FAKE_MODEL_ATTEMPTS = [
    {
        "invoice_id": "INV-2048",
        "company": "Northwind Labs",
        "currency": "USD",
        "subtotal": 1500.0,
        "tax": 120.0,
        "total": 1500.0,
        "line_items": [{"name": "Architecture Review Sprint", "qty": 1, "unit_price": 1200.0}],
    },
    {
        "invoice_id": "INV-2048",
        "company": "Northwind Labs",
        "currency": "USD",
        "subtotal": 1500.0,
        "tax": 120.0,
        "total": 1620.0,
        "line_items": [
            {"name": "Architecture Review Sprint", "qty": 1, "unit_price": 1200.0},
            {"name": "Reliability Checklist Pack", "qty": 2, "unit_price": 150.0},
        ],
    },
]


def validate_extraction(result: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for field in ("invoice_id", "company", "currency", "subtotal", "tax", "total", "line_items"):
        if field not in result:
            errors.append(f"Missing required field: {field}")
    if result.get("total") != 1620.0:
        errors.append("Total should be 1620.0")
    items = result.get("line_items", [])
    if not isinstance(items, list) or len(items) < 2:
        errors.append("Two line items were expected")
    return errors


def build_feedback(errors: list[str]) -> str:
    bullets = "; ".join(errors)
    return f"Return the full schema. Fix these issues: {bullets}."


def call_anthropic(prompt: str) -> dict[str, object]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required for --live mode.")
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL),
        "max_tokens": 700,
        "system": "Extract invoice data. Return only valid JSON with no markdown.",
        "messages": [{"role": "user", "content": prompt}],
    }
    req = request.Request(
        ANTHROPIC_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Anthropic API request failed with HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Anthropic API request failed: {exc.reason}") from exc


def response_text(response: dict[str, object]) -> str:
    parts = []
    for block in response.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
    return "\n".join(parts).strip()


def parse_json_object(text: str) -> dict[str, object]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise
        value = json.loads(match.group(0))
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object.")
    return value


def extraction_prompt(feedback: str | None = None) -> str:
    feedback_text = f"\nPrevious validation feedback: {feedback}\n" if feedback else ""
    return f"""Extract this invoice into JSON.

Required schema:
- invoice_id: string
- company: string
- currency: string
- subtotal: number
- tax: number
- total: number
- line_items: array of objects with name, qty, unit_price

{feedback_text}
Invoice:
{DOC_PATH.read_text()}
"""


def run_offline() -> None:
    print("Loaded source document from", DOC_PATH)
    BUILD_DIR.mkdir(exist_ok=True)

    for attempt_number, attempt in enumerate(FAKE_MODEL_ATTEMPTS, start=1):
        print(f"Attempt {attempt_number}")
        print(json.dumps(attempt, indent=2))
        errors = validate_extraction(attempt)
        if not errors:
            OUTPUT_PATH.write_text(json.dumps(attempt, indent=2))
            print("Validation passed. Saved result to", OUTPUT_PATH)
            return
        print("Validation failed:")
        for error in errors:
            print("-", error)
        print("Retry feedback:", build_feedback(errors))

    raise SystemExit("The extraction never produced a valid result.")


def run_live() -> None:
    print("Loaded source document from", DOC_PATH)
    BUILD_DIR.mkdir(exist_ok=True)
    feedback: str | None = None
    for attempt_number in range(1, 3):
        print(f"Live attempt {attempt_number}")
        response = call_anthropic(extraction_prompt(feedback))
        try:
            result = parse_json_object(response_text(response))
        except (json.JSONDecodeError, ValueError) as exc:
            feedback = f"Return one valid JSON object only. Parser error: {exc}"
            print("Validation failed:", feedback)
            continue
        errors = validate_extraction(result)
        if not errors:
            OUTPUT_PATH.write_text(json.dumps(result, indent=2))
            print("Live validation passed. Saved result to", OUTPUT_PATH)
            return
        feedback = build_feedback(errors)
        print("Validation failed:")
        for error_item in errors:
            print("-", error_item)
        print("Retry feedback:", feedback)
    raise SystemExit("Live extraction did not produce a valid result after one retry.")


def main() -> None:
    parser = argparse.ArgumentParser(description="LAB-02 structured extraction")
    parser.add_argument("--live", action="store_true", help="Call the Anthropic Messages API using ANTHROPIC_API_KEY.")
    args = parser.parse_args()
    if args.live:
        run_live()
    else:
        run_offline()


if __name__ == "__main__":
    main()
