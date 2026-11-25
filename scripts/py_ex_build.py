"""Build content/problems/python-ex-*.json from registered reference solutions.

Expected values are computed by executing the reference function. Test args and
return values must be JSON values that are also valid Python literals: no
null and no booleans (the submit harness embeds tests with json.dumps).
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "problems"
CATALOG: list[dict] = []


def add(
    slug: str,
    title: str,
    difficulty: str,
    topics: list[str],
    statement: str,
    constraints: list[str],
    hints: list[str],
    editorial: str,
    time: str,
    space: str,
    code: str,
    cases: list[dict],
    companies: list[str] | None = None,
    approach: str = "Direct",
    explanation: str = "",
) -> None:
    if len(hints) != 3:
        raise SystemExit(f"{slug}: need 3 hints")
    if len(cases) < 4:
        raise SystemExit(f"{slug}: need at least 4 cases")
    CATALOG.append(
        {
            "slug": slug,
            "title": title,
            "difficulty": difficulty,
            "topics": topics,
            "statement": statement.strip() + "\n",
            "constraints": constraints,
            "hints": hints,
            "editorial": editorial.strip(),
            "time": time,
            "space": space,
            "code": code.strip() + "\n",
            "cases": cases,
            "companies": companies or ["Backend", "SDE"],
            "approach": approach,
            "explanation": explanation or editorial.strip().split(".")[0] + ".",
        }
    )


def _starter(code: str) -> str:
    for line in code.splitlines():
        if line.startswith("def solve"):
            if not line.rstrip().endswith(":"):
                raise SystemExit(f"signature must be one line: {line}")
            return line + "\n    pass\n"
    raise SystemExit("missing def solve")


def _reject_non_python_json(value: object, slug: str) -> None:
    if value is None or type(value) is bool:
        raise SystemExit(f"{slug}: bool or null in value {value!r}")
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise SystemExit(f"{slug}: non-string key {key!r}")
            _reject_non_python_json(item, slug)
    elif isinstance(value, list):
        for item in value:
            _reject_non_python_json(item, slug)


def _jsonable(value: object, slug: str) -> object:
    _reject_non_python_json(value, slug)
    return json.loads(json.dumps(value))


def _fmt_args(args: dict) -> str:
    parts = []
    for key, value in args.items():
        parts.append(f"{key} = {json.dumps(value)}")
    return ", ".join(parts)


def build_one(prob: dict) -> dict:
    slug = prob["slug"]
    ns: dict = {}
    exec(prob["code"], ns)
    fn = ns.get("solve")
    if fn is None:
        raise SystemExit(f"{slug}: solve missing")
    tests = []
    for i, args in enumerate(prob["cases"], start=1):
        actual = fn(**args)
        actual = _jsonable(actual, slug)
        args_safe = _jsonable(args, slug)
        again = fn(**args)
        if _jsonable(again, slug) != actual:
            raise SystemExit(f"{slug}: nondeterministic case {i}")
        tests.append({"name": f"case-{i}", "args": args_safe, "expected": actual})
    visible, hidden = tests[:2], tests[2:]
    if not hidden:
        raise SystemExit(f"{slug}: no hidden tests")
    examples = []
    for test in visible:
        examples.append(
            {
                "input": _fmt_args(test["args"]),
                "output": json.dumps(test["expected"]),
            }
        )
    return {
        "title": prob["title"],
        "slug": slug,
        "difficulty": prob["difficulty"],
        "topics": prob["topics"],
        "company_tags": prob["companies"],
        "statement": prob["statement"],
        "constraints": prob["constraints"],
        "examples": examples,
        "starter_code": _starter(prob["code"]),
        "function_name": "solve",
        "hints": prob["hints"],
        "approaches": [
            {
                "name": prob["approach"],
                "complexity": {"time": prob["time"], "space": prob["space"]},
                "explanation": prob["explanation"],
            }
        ],
        "visible_tests": visible,
        "hidden_tests": hidden,
        "editorial": prob["editorial"],
        "reference_solution": prob["code"],
    }


def main() -> None:
    sys.modules["py_ex_build"] = sys.modules[__name__]
    sys.path.insert(0, str(ROOT / "scripts"))
    for name in (
        "py_ex_part1",
        "py_ex_part2",
        "py_ex_part3",
        "py_ex_part4",
        "py_ex_part5",
        "py_ex_part6",
    ):
        importlib.import_module(name)
    slugs = [p["slug"] for p in CATALOG]
    if len(slugs) != len(set(slugs)):
        dupes = sorted({s for s in slugs if slugs.count(s) > 1})
        raise SystemExit(f"duplicate slugs: {dupes}")
    written = 0
    for prob in CATALOG:
        doc = build_one(prob)
        path = OUT / f"{prob['slug']}.json"
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        written += 1
    print(f"wrote {written}")


if __name__ == "__main__":
    main()
