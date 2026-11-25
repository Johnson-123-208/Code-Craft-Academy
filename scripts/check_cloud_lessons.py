"""Validate cloud-devops MDX lessons against the content standard."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "content" / "cloud-devops"
REQUIRED = [
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


def body_of(text: str) -> str:
    return re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.S)


def word_count(body: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", body))


def bare_issues(text: str) -> list[str]:
    lines = text.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    in_fence = False
    problems = []
    for lineno, line in enumerate(lines[i:], start=i + 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if "{" in line or "}" in line:
            problems.append(f"brace:{lineno}:{line.strip()[:120]}")
        if re.search(r"</?[A-Za-z]", line):
            problems.append(f"jsx:{lineno}:{line.strip()[:120]}")
        if "TODO" in line or "FIXME" in line or "TBD" in line:
            problems.append(f"todo:{lineno}:{line.strip()[:120]}")
    return problems


def main() -> int:
    rows = []
    failed = 0
    for path in sorted(COURSE.rglob("*.mdx")):
        text = path.read_text(encoding="utf-8")
        body = body_of(text)
        words = word_count(body)
        rel = path.relative_to(COURSE).as_posix()
        missing = [s for s in REQUIRED if f"## {s}" not in body]
        mermaid = "```mermaid" in body
        issues = bare_issues(text)
        ok = 1200 <= words <= 3200 and not missing and mermaid and not issues
        if not ok:
            failed += 1
        rows.append((words, rel, ok, missing, mermaid, issues))
    rows.sort()
    for words, rel, ok, missing, mermaid, issues in rows:
        flag = "OK" if ok else "FAIL"
        extra = ""
        if missing:
            extra += " missing=" + ",".join(missing)
        if not mermaid:
            extra += " no-mermaid"
        if issues:
            extra += " " + " | ".join(issues[:4])
        if words < 1200 or words > 3200:
            extra += f" words-out-of-range"
        print(f"{flag:4} {words:5} {rel}{extra}")
    print(f"TOTAL {len(rows)} FAIL {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
