from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def main() -> None:
    docs = sorted((BASE_DIR / "data").glob("*.txt"))
    print("Starter project found", len(docs), "documents.")
    print("Next step: add validation, retries, and output writing.")


if __name__ == "__main__":
    main()
