from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
TOOL_FILE = BASE_DIR / "tool_specs.json"

TASK = {
    "intent": "refund the duplicate charge for order 123",
    "payload": {"order_id": "123"},
}


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


def main() -> None:
    tools = load_tools()
    for warning in detect_overlap(tools):
        print("WARNING:", warning)
    print("Task intent:", TASK["intent"])
    print("Starter evaluator stops here. Add cleaner routing and structured errors.")


if __name__ == "__main__":
    main()
