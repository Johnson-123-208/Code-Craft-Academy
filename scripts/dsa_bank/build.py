"""Write verified flagship DSA problems and delete numbered clones."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import PROBLEMS, materialize, write_all  # noqa: E402


def main() -> None:
    modules = sorted(
        path.stem
        for path in Path(__file__).resolve().parent.glob("bank_*.py")
    )
    for name in modules:
        path = Path(__file__).resolve().parent / f"{name}.py"
        if path.exists():
            importlib.import_module(name)
    problems = materialize()
    slugs = [p["slug"] for p in problems]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("duplicate slugs")
    write_all(problems)
    print(f"unique slugs: {len(PROBLEMS)}")


if __name__ == "__main__":
    main()
