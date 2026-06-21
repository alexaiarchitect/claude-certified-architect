from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib import error, request

BASE_DIR = Path(__file__).resolve().parents[1]
BUILD_DIR = BASE_DIR / "build"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-6"

FAKE_ATTEMPTS = {
    "doc-01.txt": [
        {
            "invoice_id": "INV-777",
            "company": "Example Health",
            "currency": "USD",
            "subtotal": 1100.0,
            "tax": 88.0,
            "total": 1100.0,
            "line_items": [{"name": "Initial Review", "qty": 1, "unit_price": 800.0}],
        },
        {
            "invoice_id": "INV-777",
            "company": "Example Health",
            "currency": "USD",
            "subtotal": 1100.0,
            "tax": 88.0,
            "total": 1188.0,
            "line_items": [
                {"name": "Initial Review", "qty": 1, "unit_price": 800.0},
                {"name": "Policy Mapping", "qty": 1, "unit_price": 300.0},
            ],
        },
    ],
    "doc-02.txt": [
        {
            "invoice_id": "INV-778",
            "company": "Example Retail",
            "currency": "EUR",
            "subtotal": 1100.0,
            "tax": 220.0,
            "total": 1320.0,
            "line_items": [
                {"name": "Tool Audit", "qty": 2, "unit_price": 250.0},
                {"name": "Retry Design", "qty": 1, "unit_price": 600.0},
            ],
        }
    ],
}


def validate_result(file_name: str, result: dict[str, object]) -> list[str]:
    expected_totals = {"doc-01.txt": 1188.0, "doc-02.txt": 1320.0}
    expected_items = {"doc-01.txt": 2, "doc-02.txt": 2}
    errors: list[str] = []
    if result.get("total") != expected_totals[file_name]:
        errors.append(f"Total should be {expected_totals[file_name]}")
    line_items = result.get("line_items", [])
    if not isinstance(line_items, list) or len(line_items) != expected_items[file_name]:
        errors.append(f"Expected {expected_items[file_name]} line items")
    return errors


def build_feedback(errors: list[str]) -> str:
    return "Fix the schema contract issues: " + "; ".join(errors)


def call_anthropic(doc_text: str, feedback: str | None = None) -> dict[str, object]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required for --live mode.")
    feedback_text = f"\nPrevious validation feedback: {feedback}\n" if feedback else ""
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL),
        "max_tokens": 700,
        "system": "Extract invoice data. Return only valid JSON with no markdown.",
        "messages": [
            {
                "role": "user",
                "content": f"""Extract this document into JSON.

Required schema:
- invoice_id: string
- company: string
- currency: string
- subtotal: number
- tax: number
- total: number
- line_items: array of objects with name, qty, unit_price
{feedback_text}
Document:
{doc_text}
""",
            }
        ],
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


def run_offline() -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    results: dict[str, dict[str, object]] = {}
    scorecard: dict[str, object] = {"documents": []}

    for doc_path in sorted((BASE_DIR / "data").glob("*.txt")):
        attempts = FAKE_ATTEMPTS[doc_path.name]
        for attempt_number, attempt in enumerate(attempts, start=1):
            errors = validate_result(doc_path.name, attempt)
            if not errors:
                results[doc_path.name] = attempt
                scorecard["documents"].append({"file": doc_path.name, "attempts": attempt_number, "status": "passed"})
                print(doc_path.name, "passed on attempt", attempt_number)
                break
            print(doc_path.name, "attempt", attempt_number, "failed validation; retrying:", build_feedback(errors))
        else:
            raise SystemExit(f"{doc_path.name} never produced a valid result")

    (BUILD_DIR / "results.json").write_text(json.dumps(results, indent=2))
    (BUILD_DIR / "scorecard.json").write_text(json.dumps(scorecard, indent=2))
    print("Saved results to", BUILD_DIR)


def run_live() -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    results: dict[str, dict[str, object]] = {}
    scorecard: dict[str, object] = {"documents": []}

    for doc_path in sorted((BASE_DIR / "data").glob("*.txt")):
        feedback: str | None = None
        for attempt_number in range(1, 3):
            response = call_anthropic(doc_path.read_text(), feedback)
            try:
                result = parse_json_object(response_text(response))
            except (json.JSONDecodeError, ValueError) as exc:
                feedback = f"Return one valid JSON object only. Parser error: {exc}"
                print(doc_path.name, "attempt", attempt_number, "failed validation; retrying:", feedback)
                continue
            errors = validate_result(doc_path.name, result)
            if not errors:
                results[doc_path.name] = result
                scorecard["documents"].append({"file": doc_path.name, "attempts": attempt_number, "status": "passed", "mode": "live"})
                print(doc_path.name, "passed on live attempt", attempt_number)
                break
            feedback = build_feedback(errors)
            print(doc_path.name, "attempt", attempt_number, "failed validation; retrying:", feedback)
        else:
            raise SystemExit(f"{doc_path.name} never produced a valid live result")

    (BUILD_DIR / "results.json").write_text(json.dumps(results, indent=2))
    (BUILD_DIR / "scorecard.json").write_text(json.dumps(scorecard, indent=2))
    print("Saved live results to", BUILD_DIR)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini project structured extraction pipeline")
    parser.add_argument("--live", action="store_true", help="Call the Anthropic Messages API using ANTHROPIC_API_KEY.")
    args = parser.parse_args()
    if args.live:
        run_live()
    else:
        run_offline()


if __name__ == "__main__":
    main()
