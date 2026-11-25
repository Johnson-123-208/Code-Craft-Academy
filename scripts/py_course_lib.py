#!/usr/bin/env python3
"""Shared helpers for generating CodeCraft Python course content."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "python"
PROBLEMS = ROOT / "content" / "problems"


def frontmatter(
    title: str,
    slug: str,
    summary: str,
    duration: int,
    difficulty: str,
    prerequisites: list[str],
    tags: list[str],
    order: int,
) -> str:
    return (
        "---\n"
        f'title: "{title}"\n'
        f'slug: "{slug}"\n'
        f'summary: "{summary}"\n'
        f"duration: {duration}\n"
        f'difficulty: "{difficulty}"\n'
        f"prerequisites: {json.dumps(prerequisites)}\n"
        f"tags: {json.dumps(tags)}\n"
        f"order: {order}\n"
        "---\n\n"
    )


def mermaid_flow(title: str, steps: list[str]) -> str:
    lines = ["```mermaid", "flowchart TD"]
    for i, step in enumerate(steps):
        nid = f"N{i}"
        safe = step.replace('"', "'")
        lines.append(f'    {nid}["{safe}"]')
        if i:
            lines.append(f"    N{i-1} --> {nid}")
    lines.append("```")
    return "\n".join(lines)


def dryrun_table(rows: list[tuple[str, str, str]]) -> str:
    out = ["| Step | Action / input | Result |", "| --- | --- | --- |"]
    for i, (a, b, c) in enumerate(rows, 1):
        out.append(f"| {i} | {a} | {b if False else b} |".replace(
            f"| {i} | {a} | {b} |", f"| {i} | {a} | {c} |"
        ) if False else f"| {i} | {a} | {c} |")
    # simplify
    out = ["| Step | Action / input | Result |", "| --- | --- | --- |"]
    for i, (action, _mid, result) in enumerate(rows, 1):
        out.append(f"| {i} | {action} | {result} |")
    return "\n".join(out)


def bullet_block(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_full(
    *,
    why: str,
    intuition: str,
    core: str,
    diagram: str,
    dryrun: str,
    code: str,
    complexity: str,
    tricks: list[str],
    mistakes: list[str],
    interview: str,
    practice: list[str],
    summary: list[str],
    further: list[str],
) -> str:
    parts = [
        "## Why this matters\n\n" + why.strip() + "\n",
        "## Intuition\n\n" + intuition.strip() + "\n",
        "## Core concept in depth\n\n" + core.strip() + "\n",
        "## Diagram / flowchart\n\n" + diagram.strip() + "\n",
        "### Dry-run table\n\n" + dryrun.strip() + "\n",
        "## Code\n\n" + code.strip() + "\n",
        "## Complexity analysis\n\n" + complexity.strip() + "\n",
        "## Tricks, tips and patterns\n\n" + bullet_block(tricks) + "\n",
        "## Common mistakes and edge cases\n\n" + bullet_block(mistakes) + "\n",
        "## Interview notes\n\n" + interview.strip() + "\n",
        "## Practice problems\n\n"
        + "\n".join(f"{i}. {p}" for i, p in enumerate(practice, 1))
        + "\n",
        "## Summary / cheat sheet\n\n" + bullet_block(summary) + "\n",
        "## Further reading\n\n" + "\n".join(f"- {u}" for u in further) + "\n",
    ]
    return "\n".join(parts)


def write_mdx(module: str, filename: str, text: str) -> Path:
    path = CONTENT / module / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    # Avoid unescaped lone braces outside code fences as much as possible —
    # callers should already prefer Unicode math. Still sanitize common LaTeX.
    path.write_text(text, encoding="utf-8")
    return path


def word_count(text: str) -> int:
    body = re.sub(r"```.*?```", " ", text, flags=re.S)
    return len(re.findall(r"\b\w+\b", body))


def write_problem(data: dict) -> Path:
    PROBLEMS.mkdir(parents=True, exist_ok=True)
    slug = data["slug"]
    path = PROBLEMS / f"{slug}.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
