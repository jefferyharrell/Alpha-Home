#!/usr/bin/env python3
"""
Session Start Hook

Runs at the start of every Claude Code session. Injects:
- Current time
- Index of Alphapedia files

Location: Alpha-Home/infrastructure/claude-code/hooks/
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def get_context_files(context_dir: Path) -> list[dict]:
    """Scan context directory and extract file info."""
    files = []

    for f in sorted(context_dir.glob("*.md")):
        if f.name == "SKILL.md":
            continue  # Skip legacy skill file if present

        info = {"name": f.name, "path": str(f)}

        # Read first few lines to extract title/description
        try:
            with open(f, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("# "):
                        info["title"] = line[2:].strip()
                        break
        except Exception:
            pass

        files.append(info)

    return files


def build_context() -> str:
    """Build the additionalContext string."""
    parts = []

    # Time awareness
    now = datetime.now()
    time_str = now.strftime("%A, %B %d, %Y at %I:%M %p")
    parts.append(f"**Current time:** {time_str}")

    # Alphapedia
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.home() / "Pondside"))
    context_dir = project_dir / "Alpha-Home" / "Alphapedia"

    if context_dir.exists():
        files = get_context_files(context_dir)

        if files:
            parts.append("")
            parts.append("**Alphapedia** (read files when conversation involves these topics):")
            for f in files:
                title = f.get("title", f["name"])
                parts.append(f"- `{f['path']}` — {title}")

    return "\n".join(parts)


def main():
    # Read hook input (we don't use it yet, but good practice)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # Build and output context
    additional_context = build_context()

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
