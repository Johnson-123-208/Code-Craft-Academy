"""Word-count and MDX-brace check for content/python lessons."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "content" / "python"
FENCE = "```"


def word_count(text: str) -> int:
    body = re.sub(r"```.*?```", " ", text, flags=re.S)
    body = re.sub(r"^---\n.*?\n---\n", " ", body, flags=re.S)
    return len(re.findall(r"\b\w+\b", body))


def bare_braces(text: str) -> list[str]:
    lines = text.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    in_fence = False
    bad: list[str] = []
    for n, line in enumerate(lines[i:], start=i + 1):
        if line.strip().startswith(FENCE):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if "{" in line or "}" in line:
            bad.append(f"{n}: {line}")
    if in_fence:
        bad.append("UNCLOSED FENCE")
    return bad


REQUIRED = [
    "## Why this matters",
    "## Intuition",
    "## Core concept in depth",
    "## Diagram / flowchart",
    "## Code",
    "## Complexity analysis",
    "## Tricks, tips and patterns",
    "## Common mistakes and edge cases",
    "## Interview notes",
    "## Practice problems",
    "## Summary / cheat sheet",
    "## Further reading",
]


def main() -> int:
    files = sorted(COURSE.rglob("*.mdx"))
    failed = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        wc = word_count(text)
        braces = bare_braces(text)
        missing = [s for s in REQUIRED if s not in text]
        rel = path.relative_to(ROOT)
        flags = []
        if wc < 1200 or wc > 3000:
            flags.append(f"WORDS {wc}")
        if braces:
            flags.append("BRACES")
        if missing:
            flags.append("MISSING " + ",".join(missing))
        if "TODO" in text or "TBD" in text:
            flags.append("TODO")
        status = "OK" if not flags else "FAIL"
        if flags:
            failed += 1
        print(f"{status}\t{wc}\t{rel}")
        for flag in flags:
            print(f"  {flag}")
        for b in braces:
            print(f"  {b}")
    print(f"files={len(files)} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
