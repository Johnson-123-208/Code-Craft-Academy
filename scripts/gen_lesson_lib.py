"""Shared helpers for generating CodeCraft Academy MDX lessons."""
from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

REQUIRED_SECTIONS = [
    "Why this matters",
    "Intuition",
    "Core concept in depth",
    "Diagram / flowchart",
    "Code",
    "Complexity analysis",
    "Tricks, tips and patterns",
    "Common mistakes and edge cases",
    "Interview notes",
    "Practice problems",
    "Summary / cheat sheet",
    "Further reading",
]


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
    prereq = "[" + ", ".join(f'"{p}"' for p in prerequisites) + "]"
    tag_s = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
    return "\n".join(
        [
            "---",
            f'title: "{title}"',
            f'slug: "{slug}"',
            f'summary: "{summary}"',
            f"duration: {duration}",
            f'difficulty: "{difficulty}"',
            f"prerequisites: {prereq}",
            f"tags: {tag_s}",
            f"order: {order}",
            "---",
            "",
        ]
    )


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{i+1}. {t}" for i, t in enumerate(items))


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    return f"{head}\n{sep}\n{body}"


def mermaid(body: str) -> str:
    return f"```mermaid\n{body.strip()}\n```"


def code_block(lang: str, body: str) -> str:
    return f"```{lang}\n{body.rstrip()}\n```"


def reading(links: list[tuple[str, str]]) -> str:
    return "\n".join(f"- [{t}]({u})" for t, u in links)


def render_lesson(meta: dict[str, Any], sections: dict[str, str]) -> str:
    missing = [s for s in REQUIRED_SECTIONS if s not in sections]
    if missing:
        raise ValueError(f"Missing sections for {meta['slug']}: {missing}")
    parts = [
        frontmatter(
            meta["title"],
            meta["slug"],
            meta["summary"],
            meta["duration"],
            meta["difficulty"],
            meta.get("prerequisites", []),
            meta.get("tags", []),
            meta["order"],
        )
    ]
    for name in REQUIRED_SECTIONS:
        parts.append(f"## {name}\n\n{sections[name].rstrip()}\n")
    return "\n".join(parts).rstrip() + "\n"


def write_lesson(course: str, module: str, filename: str, text: str) -> Path:
    dest = CONTENT / course / module / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return dest


def assert_no_bare_braces(text: str, path: str) -> None:
    """Flag unescaped curly braces outside fenced blocks (MDX hazard)."""
    lines = text.splitlines()
    in_fence = False
    # skip frontmatter
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    for lineno, line in enumerate(lines[i:], start=i + 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # allow empty
        if "{" in line or "}" in line:
            raise ValueError(f"Bare brace in {path}:{lineno}: {line}")
