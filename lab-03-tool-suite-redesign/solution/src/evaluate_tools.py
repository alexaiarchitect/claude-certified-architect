from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib import error, request

BASE_DIR = Path(__file__).resolve().parents[1]
TOOL_FILE = BASE_DIR / "tool_specs.json"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-6"

TASKS = [
    {"intent": "validation is complete; issue the duplicate charge refund for order 123", "payload": {"order_id": "123", "amount": 49.99, "reason": "duplicate_charge"}},
    {"intent": "look up order 555 before making a decision", "payload": {"order_id": "555"}},
    {"intent": "escalate this case for policy review", "payload": {"reason": "policy_review", "case_summary": "requested exception"}},
]


def load_tools() -> list[dict[str, object]]:
    return json.loads(TOOL_FILE.read_text())


def detect_overlap(tools: list[dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    for index, left in enumerate(tools):
        for right in tools[index + 1 :]:
            overlap = set(left["keywords"]).intersection(set(right["keywords"]))
            if overlap:
                warnings.append(f"{left['name']} overlaps with {right['name']} on {sorted(overlap)}")
    return warnings


def select_tool(intent: str, tools: list[dict[str, object]]) -> dict[str, object]:
    intent_words = set(intent.lower().split())
    scored = []
    for tool in tools:
        score = len(intent_words.intersection(set(tool["keywords"])))
        scored.append((score, tool))
    scored.sort(key=lambda entry: entry[0], reverse=True)
    return scored[0][1]


def validate_payload(tool: dict[str, object], payload: dict[str, object]) -> dict[str, object] | None:
    missing = [field for field in tool["required_fields"] if field not in payload]
    if missing:
        return {
            "isError": True,
            "category": "validation",
            "retryable": False,
            "message": f"Missing required fields: {', '.join(missing)}",
        }
    return None


def execute_tool(tool: dict[str, object], payload: dict[str, object]) -> dict[str, object]:
    validation_error = validate_payload(tool, payload)
    if validation_error:
        return validation_error
    return {"isError": False, "tool": tool["name"], "payload": payload}


def anthropic_tools(tools: list[dict[str, object]]) -> list[dict[str, object]]:
    converted = []
    for tool in tools:
        properties = {field: {"type": "string"} for field in tool["required_fields"]}
        if "amount" in properties:
            properties["amount"] = {"type": "number"}
        converted.append(
            {
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": {
                    "type": "object",
                    "properties": properties,
                    "required": tool["required_fields"],
                    "additionalProperties": False,
                },
            }
        )
    return converted


def call_anthropic_tool(task: dict[str, object], tools: list[dict[str, object]]) -> dict[str, object]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required for --live mode.")
    payload = {
        "model": os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL),
        "max_tokens": 400,
        "tools": anthropic_tools(tools),
        "tool_choice": {"type": "any"},
        "system": "Select exactly one tool for the action to execute now. Use the provided payload values. If a payload has every required field for an action tool, do not choose a lookup tool first. Do not invent side effects.",
        "messages": [
            {
                "role": "user",
                "content": f"Intent: {task['intent']}\nPayload: {json.dumps(task['payload'])}",
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


def extract_tool_use(response: dict[str, object]) -> dict[str, object]:
    for block in response.get("content", []):
        if isinstance(block, dict) and block.get("type") == "tool_use":
            return block
    raise ValueError("No tool_use block returned.")


def run_offline() -> None:
    tools = load_tools()
    warnings = detect_overlap(tools)
    if warnings:
        raise SystemExit("Tool overlap still present:\n" + "\n".join(warnings))

    print("Tool overlap check passed.")
    for task in TASKS:
        tool = select_tool(task["intent"], tools)
        result = execute_tool(tool, task["payload"])
        print(json.dumps({"intent": task["intent"], "selected_tool": tool["name"], "result": result}, indent=2))


def run_live() -> None:
    tools = load_tools()
    warnings = detect_overlap(tools)
    if warnings:
        raise SystemExit("Tool overlap still present:\n" + "\n".join(warnings))
    tool_by_name = {tool["name"]: tool for tool in tools}
    print("Tool overlap check passed.")
    for task in TASKS:
        expected_tool = select_tool(task["intent"], tools)
        response = call_anthropic_tool(task, tools)
        tool_use = extract_tool_use(response)
        selected_name = str(tool_use["name"])
        tool = tool_by_name[selected_name]
        result = execute_tool(tool, tool_use.get("input", {}))
        if selected_name != expected_tool["name"] or result.get("isError"):
            raise SystemExit(
                "Live tool selection failed:\n"
                + json.dumps(
                    {
                        "intent": task["intent"],
                        "expected_tool": expected_tool["name"],
                        "selected_tool": selected_name,
                        "result": result,
                    },
                    indent=2,
                )
            )
        print(json.dumps({"intent": task["intent"], "selected_tool": selected_name, "result": result}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="LAB-03 tool suite evaluator")
    parser.add_argument("--live", action="store_true", help="Call the Anthropic Messages API using ANTHROPIC_API_KEY.")
    args = parser.parse_args()
    if args.live:
        run_live()
    else:
        run_offline()


if __name__ == "__main__":
    main()
