"""Write DSA lessons and reject thin or MDX-unsafe chapters."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content" / "dsa"

SECTIONS = [
    "## Why this matters",
    "## Intuition",
    "## Core concept in depth",
    "## Diagram and dry run",
    "## Runnable Python",
    "## Complexity and trade-offs",
    "## Tricks, tips, and patterns",
    "## Common mistakes and edge cases",
    "## Interview notes",
    "## Practice problems",
    "## Summary and cheat sheet",
    "## Further reading",
]


def _outside_fences(body: str) -> str:
    no_fence = re.sub(r"```.*?```", "", body, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", no_fence)


def emit(
    module: str,
    filename: str,
    *,
    title: str,
    slug: str,
    summary: str,
    duration: int,
    difficulty: str,
    prerequisites: list[str],
    tags: list[str],
    order: int,
    body: str,
) -> tuple[int, Path]:
    body = body.strip() + "\n"
    missing = [heading for heading in SECTIONS if heading not in body]
    if missing:
        raise SystemExit(f"{filename} missing {missing}")
    prose = _outside_fences(body)
    if "{" in prose or "}" in prose:
        raise SystemExit(f"{filename} has bare braces outside fences")
    if "$" in prose:
        raise SystemExit(f"{filename} has a dollar sign outside fences")
    if re.search(r"</?[A-Za-z]", prose):
        raise SystemExit(f"{filename} has a raw tag outside fences")
    words = len(body.split())
    if not 1200 <= words <= 3200:
        raise SystemExit(f"{filename} has {words} words, need 1200-3000")
    prereq = ", ".join(f'"{item}"' for item in prerequisites)
    tag = ", ".join(f'"{item}"' for item in tags)
    text = (
        "---\n"
        f'title: "{title}"\n'
        f'slug: "{slug}"\n'
        f'summary: "{summary}"\n'
        f"duration: {duration}\n"
        f'difficulty: "{difficulty}"\n'
        f"prerequisites: [{prereq}]\n"
        f"tags: [{tag}]\n"
        f"order: {order}\n"
        "---\n\n"
        f"{body}"
    )
    path = ROOT / module / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"{module}/{filename}: {words} words")
    return words, path
