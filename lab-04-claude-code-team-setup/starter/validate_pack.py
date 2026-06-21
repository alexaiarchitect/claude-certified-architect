from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    errors: list[str] = []

    claude_md = ROOT / "CLAUDE.md"
    settings_path = ROOT / ".claude" / "settings.json"
    skill_path = ROOT / ".claude" / "skills" / "architecture-review" / "SKILL.md"
    mcp_path = ROOT / ".mcp.json"

    if not claude_md.exists():
        errors.append("Missing CLAUDE.md")
    else:
        claude_text = claude_md.read_text()
        if "## Review Flow" not in claude_text:
            errors.append("CLAUDE.md must define a review flow section")

    if not settings_path.exists():
        errors.append("Missing settings.json")
    else:
        settings = json.loads(settings_path.read_text())
        deny = settings.get("permissions", {}).get("deny", [])
        if not any(".env" in item for item in deny):
            errors.append("Add a deny rule for .env files")
        if not any("secrets" in item for item in deny):
            errors.append("Add a deny rule for secrets directories")

    if not skill_path.exists():
        errors.append("Missing architecture-review skill")
    else:
        text = skill_path.read_text()
        if "description:" not in text:
            errors.append("Skill frontmatter must include a description")
        for section in ("## When to Use", "## Workflow", "## Output Shape"):
            if section not in text:
                errors.append(f"Skill is missing section: {section}")

    if not mcp_path.exists():
        errors.append("Missing example .mcp.json")
    else:
        mcp = json.loads(mcp_path.read_text())
        if "mcpServers" not in mcp:
            errors.append(".mcp.json must define mcpServers")

    if errors:
        print("Pack validation failed:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("Pack validation passed.")


if __name__ == "__main__":
    main()
