from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from urllib import error, request

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env.example"
DATA_FILE = BASE_DIR / "data" / "sample_response.json"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-6"


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def build_request_skeleton(model: str | None = None) -> dict[str, object]:
    return {
        "model": model or os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL),
        "system": "Be reliable, explicit, and safe with tool use.",
        "messages": [{"role": "user", "content": "Review this case and decide the next safe step."}],
        "tools": [{"name": "get_customer_profile", "description": "Fetch customer profile for escalation review."}],
        "metadata": {"course_module": "M2", "lab_id": "LAB-01"},
    }


def route_stop_reason(stop_reason: str) -> list[str]:
    routes = {
        "tool_use": [
            "Run the requested tool.",
            "Append a tool_result block.",
            "Continue the loop with the updated conversation.",
        ],
        "end_turn": [
            "Return the final answer to the caller.",
            "Persist logs and decision metadata.",
        ],
        "pause_turn": [
            "Persist state.",
            "Wait for the external process or human review.",
        ],
        "max_tokens": [
            "Treat the answer as incomplete.",
            "Reissue with a continuation strategy or escalate.",
        ],
    }
    return routes.get(stop_reason, ["Escalate unknown stop reason and inspect the raw payload."])


def call_anthropic(payload: dict[str, object]) -> dict[str, object]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required for --live mode.")

    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        ANTHROPIC_API_URL,
        data=body,
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


def run_offline() -> None:
    env = load_env(ENV_FILE)
    logging.basicConfig(level=getattr(logging, env.get("LOG_LEVEL", "INFO"), logging.INFO), format="%(levelname)s: %(message)s")

    payload = json.loads(DATA_FILE.read_text())
    request = build_request_skeleton(env.get("ANTHROPIC_MODEL"))

    logging.info("Environment: %s", env.get("COURSE_ENV"))
    logging.info("Request skeleton: %s", json.dumps(request, indent=2))
    logging.info("Response ID: %s", payload["id"])
    logging.info("Stop reason: %s", payload["stop_reason"])
    for step in route_stop_reason(payload["stop_reason"]):
        logging.info("Next action: %s", step)
    logging.info("Usage: %s input / %s output", payload["usage"]["input_tokens"], payload["usage"]["output_tokens"])


def run_live() -> None:
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    response = call_anthropic(
        {
            "model": model,
            "max_tokens": 80,
            "system": "Return exactly one short sentence under 25 words. Mention whether to continue, retry, stop, or escalate.",
            "messages": [{"role": "user", "content": "A tool call timed out while reading order metadata. No side effect was committed. What is the next safe action? Answer in one sentence."}],
        }
    )
    usage = response.get("usage", {})
    print("Live API check passed.")
    print("Response ID:", response.get("id"))
    print("Model:", response.get("model"))
    print("Stop reason:", response.get("stop_reason"))
    print("Usage:", usage.get("input_tokens"), "input /", usage.get("output_tokens"), "output")
    for step in route_stop_reason(str(response.get("stop_reason"))):
        print("Next action:", step)


def main() -> None:
    parser = argparse.ArgumentParser(description="LAB-01 scaffold smoke test")
    parser.add_argument("--live", action="store_true", help="Call the Anthropic Messages API using ANTHROPIC_API_KEY.")
    args = parser.parse_args()
    if args.live:
        run_live()
    else:
        run_offline()


if __name__ == "__main__":
    main()
