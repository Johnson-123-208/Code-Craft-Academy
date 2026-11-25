"""Shared schema, oracles, and JSON writer for flagship DSA problems."""

from __future__ import annotations

import inspect
import json
import textwrap
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "content" / "problems"

COMPANIES = [
    "Google",
    "Amazon",
    "Meta",
    "Microsoft",
    "Apple",
    "Uber",
    "Adobe",
    "Bloomberg",
    "Flipkart",
    "Atlassian",
]

PROBLEMS: list[dict[str, Any]] = []
_FUNCS: dict[str, Callable[..., Any]] = {}
_ORACLES: dict[str, Callable[..., Any]] = {}
_TESTS: dict[str, list[dict[str, Any]]] = {}


def _json_eq(a: Any, b: Any) -> bool:
    return json.dumps(a, sort_keys=True, default=str) == json.dumps(
        b, sort_keys=True, default=str
    )


def _roundtrip(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _source(fn: Callable[..., Any]) -> str:
    src = textwrap.dedent(inspect.getsource(fn)).strip() + "\n"
    lines = src.splitlines()
    while lines and not lines[0].startswith("def "):
        lines = lines[1:]
    src = "\n".join(lines).strip() + "\n"
    header = (
        "from typing import Dict, List, Optional, Tuple\n"
        "from collections import Counter, OrderedDict, defaultdict, deque\n"
        "import heapq\n\n"
    )
    return header + src


def define(
    *,
    slug: str,
    title: str,
    difficulty: str,
    topics: list[str],
    statement: str,
    constraints: list[str],
    signature: str,
    function_name: str,
    hints: list[str],
    approaches: list[tuple[str, str, str, str]],
    editorial: str,
    companies: list[str] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Register metadata. The wrapped function is the reference solution."""

    if len(hints) != 3:
        raise ValueError(f"{slug}: need exactly 3 hints, got {len(hints)}")
    if len(approaches) < 2:
        raise ValueError(f"{slug}: need brute-to-optimal approaches")

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        if fn.__name__ != function_name:
            raise ValueError(f"{slug}: function {fn.__name__} != {function_name}")
        meta = {
            "title": title,
            "slug": slug,
            "difficulty": difficulty,
            "topics": topics,
            "company_tags": companies or COMPANIES[:4],
            "statement": statement.strip() + "\n",
            "constraints": constraints,
            "signature": signature,
            "function_name": function_name,
            "hints": hints,
            "approaches": [
                {
                    "name": name,
                    "complexity": {"time": time, "space": space},
                    "explanation": expl,
                }
                for name, time, space, expl in approaches
            ],
            "editorial": editorial.strip(),
            "reference_solution": _source(fn),
            "starter_code": signature.rstrip() + "\n    pass\n",
        }
        PROBLEMS.append(meta)
        _FUNCS[slug] = fn
        return fn

    return deco


def cases(
    slug: str,
    oracle: Callable[..., Any],
    tests: list[tuple[str, dict[str, Any], bool, str | None]],
) -> None:
    """Each test is (name, args, visible, explanation).

    Expected output is computed by `oracle` and must match the reference.
    """

    if slug not in _FUNCS:
        raise KeyError(f"cases() before define() for {slug}")
    if slug in _TESTS:
        raise ValueError(f"duplicate cases for {slug}")
    if len(tests) < 4:
        raise ValueError(f"{slug}: need at least 4 tests")
    visible = [t for t in tests if t[2]]
    hidden = [t for t in tests if not t[2]]
    if len(visible) < 2 or len(hidden) < 2:
        raise ValueError(f"{slug}: need >=2 visible and >=2 hidden tests")
    _ORACLES[slug] = oracle
    _TESTS[slug] = [
        {"name": name, "args": args, "visible": visible_flag, "explanation": expl}
        for name, args, visible_flag, expl in tests
    ]


def materialize() -> list[dict[str, Any]]:
    by_slug = {p["slug"]: p for p in PROBLEMS}
    if len(by_slug) != len(PROBLEMS):
        raise ValueError("duplicate problem slug in registry")
    missing = [s for s in by_slug if s not in _TESTS]
    if missing:
        raise ValueError(f"missing tests: {missing[:8]} ({len(missing)} total)")
    out: list[dict[str, Any]] = []
    for slug, meta in by_slug.items():
        fn = _FUNCS[slug]
        oracle = _ORACLES[slug]
        examples: list[dict[str, str]] = []
        visible_tests: list[dict[str, Any]] = []
        hidden_tests: list[dict[str, Any]] = []
        for t in _TESTS[slug]:
            args = _roundtrip(t["args"])
            expected = _roundtrip(oracle(**_roundtrip(args)))
            actual = _roundtrip(fn(**_roundtrip(args)))
            if not _json_eq(actual, expected):
                raise AssertionError(
                    f"{slug}/{t['name']}: reference {actual!r} != oracle {expected!r}"
                )
            row = {"name": t["name"], "args": args, "expected": expected}
            if t["visible"]:
                visible_tests.append(row)
                if len(examples) < 3:
                    arg_bits = ", ".join(f"{k} = {v!r}" for k, v in args.items())
                    ex: dict[str, str] = {
                        "input": arg_bits,
                        "output": json.dumps(expected),
                    }
                    if t["explanation"]:
                        ex["explanation"] = t["explanation"]
                    examples.append(ex)
            else:
                hidden_tests.append(row)
        built = {
            k: v
            for k, v in meta.items()
            if k not in {"signature"}
        }
        built["examples"] = examples
        built["visible_tests"] = visible_tests
        built["hidden_tests"] = hidden_tests
        out.append(built)
    return out


def write_all(problems: list[dict[str, Any]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    keep_prefixes = ("ml-", "python-ex-", "fizz-buzz-")
    flagship = {p["slug"] for p in problems}
    for p in problems:
        path = OUT / f"{p['slug']}.json"
        path.write_text(json.dumps(p, indent=2) + "\n", encoding="utf-8")
    removed = 0
    for path in OUT.glob("*.json"):
        slug = path.stem
        if slug in flagship or slug.startswith(keep_prefixes):
            continue
        path.unlink()
        removed += 1
    print(f"Wrote {len(problems)} flagship problems. Removed {removed} superseded files.")
