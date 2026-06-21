from __future__ import annotations

import json
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env.example"
DATA_FILE = BASE_DIR / "data" / "sample_response.json"


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def route_stop_reason(stop_reason: str) -> str:
    if stop_reason == "tool_use":
        return "Run the requested tool, append the tool result, and continue the loop."
    return "TODO: expand this router for other stop reasons."


def main() -> None:
    env = load_env(ENV_FILE)
    logging.basicConfig(level=getattr(logging, env.get("LOG_LEVEL", "INFO"), logging.INFO))

    payload = json.loads(DATA_FILE.read_text())
    logging.info("Loaded environment for %s", env.get("COURSE_ENV"))
    logging.info("Sample response ID: %s", payload["id"])
    logging.info("Next action: %s", route_stop_reason(payload["stop_reason"]))
    logging.info("Usage: %s input / %s output", payload["usage"]["input_tokens"], payload["usage"]["output_tokens"])


if __name__ == "__main__":
    main()
