#!/usr/bin/env python3
"""Generate the complete CodeCraft Academy Python course lessons and exercises."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "python"
PROBLEMS = ROOT / "content" / "problems"


def fm(
    title: str,
    slug: str,
    summary: str,
    duration: int,
    difficulty: str,
    prerequisites: list[str],
    tags: list[str],
    order: int,
) -> str:
    prereq = json.dumps(prerequisites)
    tag_s = json.dumps(tags)
    return (
        f'---\n'
        f'title: "{title}"\n'
        f'slug: "{slug}"\n'
        f'summary: "{summary}"\n'
        f"duration: {duration}\n"
        f'difficulty: "{difficulty}"\n'
        f"prerequisites: {prereq}\n"
        f"tags: {tag_s}\n"
        f"order: {order}\n"
        f"---\n\n"
    )


def lesson(
    why: str,
    intuition: str,
    core: str,
    diagram: str,
    dryrun: str,
    code: str,
    complexity: str,
    tricks: str,
    mistakes: str,
    interview: str,
    practice: str,
    summary: str,
    further: str,
) -> str:
    return textwrap.dedent(
        f"""\
## Why this matters

{why.strip()}

## Intuition

{intuition.strip()}

## Core concept in depth

{core.strip()}

## Diagram / flowchart

{diagram.strip()}

### Dry-run table

{dryrun.strip()}

## Code

{code.strip()}

## Complexity analysis

{complexity.strip()}

## Tricks, tips and patterns

{tricks.strip()}

## Common mistakes and edge cases

{mistakes.strip()}

## Interview notes

{interview.strip()}

## Practice problems

{practice.strip()}

## Summary / cheat sheet

{summary.strip()}

## Further reading

{further.strip()}
"""
    )


def write_lesson(module: str, filename: str, front: str, body: str) -> Path:
    path = CONTENT / module / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front + body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Module 01 — Getting Started (lessons 02–03; 01 already exists)
# ---------------------------------------------------------------------------

def gen_01() -> list[Path]:
    paths: list[Path] = []

    # Enhance intro slightly — rewrite with same structure but slightly richer
    intro = fm(
        "Introduction to Python and Environment Setup",
        "python-intro-and-setup",
        "Why Python dominates modern engineering, how to install it correctly, and how to run your first programs in the REPL, scripts, and virtual environments.",
        25,
        "beginner",
        [],
        ["python", "setup", "venv", "pip", "repl"],
        1,
    ) + lesson(
        why="""
Python is the lingua franca of modern software: web backends, data science, machine learning,
automation, DevOps tooling, and interview whiteboards all speak it. Companies hire for Python
because a single language covers scripting, APIs, and analytics without forcing you to switch
toolchains.

Getting the environment right on day one prevents the most common beginner failures: `python`
vs `python3` confusion, globally polluted packages, and "works on my machine" dependency hell.
This lesson builds the foundation every later module assumes: a clean interpreter, an isolated
virtual environment, and the habit of running code deliberately.
""",
        intuition="""
Think of Python like a workshop. The **interpreter** is the power tool that executes instructions.
A **script** is a blueprint you save and reuse. A **virtual environment** is a private workbench
for one project so paints and screws from another project do not mix. **pip** is the supply catalog
that delivers libraries into that workbench only.

You do not need to memorize every flag today. You need a mental model: isolate each project, pin
what you install, and always know *which* Python binary you are talking to.
""",
        core="""
### What Python is

Python is a high-level, dynamically typed, garbage-collected language with a design philosophy
favoring readability (see `import this`). CPython — the reference implementation — compiles
source to bytecode and runs it on a virtual machine. You rarely think about bytecode early on,
but it explains why `.pyc` files appear and why import caching exists.

### Installation checklist

1. Install Python 3.12+ from [python.org](https://www.python.org/downloads/) (or use `pyenv` / your OS package manager).
2. Verify the binary:

```bash
python --version
# or on some systems:
python3 --version
```

3. Ensure `pip` is available:

```bash
python -m pip --version
```

Using `python -m pip` is safer than bare `pip` because it guarantees you install into the same
interpreter you just invoked.

### The REPL

Start an interactive session with `python`. Explore expressions, call `help()`, and exit with
`exit()` or Ctrl-D. The REPL (Read–Eval–Print Loop) is ideal for exploring APIs and verifying
small ideas. Anything serious belongs in a `.py` file.

### Scripts and the main guard

Create `hello.py` with a `main()` function and protect the entry point with
`if __name__ == "__main__":`. That guard ensures `main()` runs only when the file is executed
as a program, not when imported as a module.

### Virtual environments and pip

Create a venv with `python -m venv .venv`, activate it, then install with
`python -m pip install …` and freeze with `python -m pip freeze > requirements.txt`.
Never commit `.venv/` — commit the requirements (or a lock file) instead.
""",
        diagram="""
```mermaid
flowchart TD
    A[Install Python 3.12+] --> B[Create project folder]
    B --> C["python -m venv .venv"]
    C --> D[Activate virtual environment]
    D --> E["python -m pip install dependencies"]
    E --> F{How do you run code?}
    F -->|Explore| G[REPL: python]
    F -->|Program| H[Script: python app.py]
    F -->|Notebook later| I[Jupyter / playground]
    G --> J[Iterate safely inside .venv]
    H --> J
    I --> J
```
""",
        dryrun="""
| Step | Action | Expected result |
| --- | --- | --- |
| 1 | `python --version` | Prints 3.12.x or newer |
| 2 | `python -m venv .venv` | `.venv/` directory appears |
| 3 | Activate venv | Prompt shows `(.venv)` |
| 4 | `python -m pip install rich` | Package installs into `.venv` |
| 5 | `python hello.py` | Program runs with isolated deps |
""",
        code="""
```python
import platform
import sys


def describe_environment() -> None:
    print("=== CodeCraft Environment Check ===")
    print(f"Python version : {sys.version.split()[0]}")
    print(f"Executable     : {sys.executable}")
    print(f"Platform       : {platform.platform()}")
    print(f"Prefix         : {sys.prefix}")
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    print(f"Inside venv?   : {in_venv}")


if __name__ == "__main__":
    describe_environment()
```
""",
        complexity="""
Environment setup is not an algorithm, but forming good habits has a complexity of its own:

| Concern | Cost if ignored | Cost if done right |
| --- | --- | --- |
| Global installs | Hours debugging version conflicts | Minutes per project for venv |
| No requirements.txt | Broken teammates / CI | Reproducible installs |
| Wrong interpreter | Silent package mismatches | One `python -m` habit |
""",
        tricks="""
- Prefer `python -m pip` and `python -m venv` over bare commands.
- Name environments `.venv` so tools and `.gitignore` templates recognize them.
- On Windows, use `py -3.12` via the Python launcher to select a specific version.
- Keep a personal cheat sheet of activate commands for each OS you use.
""",
        mistakes="""
- Installing packages with one Python and running scripts with another.
- Forgetting to activate the venv (symptoms: `ModuleNotFoundError`).
- Committing `.venv/` to git — bloated repos and non-portable binaries.
- Mixing Conda and venv without knowing which `python` is active.
- Following Python 2 tutorials (`print` statements, `raw_input`).
""",
        interview="""
Interviewers rarely ask you to recite pip flags, but they do expect you can explain what a
virtual environment solves, the difference between the standard library and third-party packages,
and how reproducibility works (`requirements.txt`, lock files). Follow-up: containerize with Docker.
""",
        practice="""
1. **Env Inspector** (easy) — extend the script above to also print `sys.path` entries. [Practice: python-ex-env-inspector]
2. **Freeze Diff** (easy) — install two packages, freeze requirements, uninstall one, explain the diff.
3. **Dual Python** (medium) — install two Python versions and demonstrate invoking each explicitly.
""",
        summary="""
- Install Python 3.12+, verify with `python --version`.
- Always create a per-project `.venv` and activate it.
- Install with `python -m pip install …` and freeze dependencies.
- Use the REPL to explore; use scripts with a `__main__` guard for real programs.
- Know which interpreter is active before you debug missing-module errors.
""",
        further="""
- [Python 3 Tutorial](https://docs.python.org/3/tutorial/)
- [venv docs](https://docs.python.org/3/library/venv.html)
- [Packaging User Guide — Installing Packages](https://packaging.python.org/en/latest/tutorials/installing-packages/)
- [PEP 8](https://peps.python.org/pep-0008/)
""",
    )
    paths.append(write_lesson("01-getting-started", "01-intro-and-setup.mdx", intro[:0], intro))
    # fix: write_lesson expects front+body separately; rewrite properly
    paths[-1].write_text(intro, encoding="utf-8")

    paths.append(
        write_lesson(
            "01-getting-started",
            "02-repl-scripts-and-pip.mdx",
            fm(
                "REPL, Scripts, and pip Workflows",
                "python-repl-scripts-pip",
                "Master the interactive REPL, structure real scripts with entry points, and use pip confidently for install, freeze, and upgrade workflows.",
                30,
                "beginner",
                ["python-intro-and-setup"],
                ["python", "repl", "scripts", "pip"],
                2,
            ),
            lesson(
                why="""
Day-to-day Python work oscillates between three modes: poke at an idea in the REPL, encode it in
a script, and pull in libraries with pip. Juniors who blur these modes waste hours — paste broken
snippets into the wrong place, pollute the global site-packages, or ship scripts that only work
when imported by accident. This lesson makes each mode crisp so later modules can assume you
know how to explore, persist, and depend.
""",
                intuition="""
The REPL is a whiteboard: temporary, conversational, perfect for "what does this return?"
A script is a contract: named entry points, reproducible runs, something teammates can execute.
pip is the loading dock: you request crates (packages), they land in *this* interpreter's
site-packages, and you record the invoice (`requirements.txt`) so others can restock identically.

If you always ask "am I exploring, shipping, or depending?" you pick the right tool every time.
""",
                core="""
### REPL power moves

- `_` holds the last expression result.
- `help(obj)` and `dir(obj)` reveal APIs without leaving the terminal.
- Paste multi-line blocks carefully; prefer IPython or `python -i script.py` for richer sessions.
- Use `python -c "print(2+2)"` for one-liners in shell scripts and CI checks.

### Script anatomy

A production-minded script has:

1. Imports at the top (stdlib, then third-party, then local).
2. Functions and classes that do the work.
3. A thin `main()` that parses args / orchestrates.
4. An `if __name__ == "__main__":` guard calling `main()`.

```python
import argparse


def greet(name: str, times: int = 1) -> None:
    for _ in range(times):
        print(f"Hello, {name}!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Friendly greeter")
    parser.add_argument("name")
    parser.add_argument("-n", "--times", type=int, default=1)
    args = parser.parse_args()
    greet(args.name, args.times)


if __name__ == "__main__":
    main()
```

### pip workflows in depth

| Command | When to use |
| --- | --- |
| `python -m pip install pkg` | Add a dependency now |
| `python -m pip install pkg==1.2.3` | Pin an exact version |
| `python -m pip install -r requirements.txt` | Bootstrap a project |
| `python -m pip install -U pkg` | Upgrade one package |
| `python -m pip uninstall pkg` | Remove a package |
| `python -m pip freeze` | Snapshot exact installed set |
| `python -m pip show pkg` | Inspect metadata / location |
| `python -m pip list --outdated` | See what can upgrade |

Prefer **`python -m pip`** always. On Windows, `py -m pip` selects via the launcher.

### Editable installs (preview)

For your own packages: `python -m pip install -e .` links the project so edits apply without
reinstalling. Full packaging arrives in module 17.
""",
                diagram="""
```mermaid
flowchart LR
    A[Idea] --> B{Need persistence?}
    B -->|No| C[REPL / python -c]
    B -->|Yes| D[Write .py script]
    D --> E{Need libraries?}
    E -->|No| F[stdlib only]
    E -->|Yes| G[pip install into active venv]
    G --> H[freeze to requirements.txt]
    F --> I[python script.py]
    H --> I
```
""",
                dryrun="""
| Step | Command / action | Result |
| --- | --- | --- |
| 1 | `python` then `2 ** 10` | Prints `1024`, `_` is 1024 |
| 2 | Write `greet.py` with argparse | File saved |
| 3 | `python greet.py Ada -n 2` | Two hello lines |
| 4 | `python -m pip install requests` | Package in current env |
| 5 | `python -m pip freeze \\| findstr requests` | Shows pinned line |
""",
                code="""
```python
\"\"\"Minimal CLI that demonstrates script + pip-friendly structure.\"\"\"
from __future__ import annotations

import argparse
import sys


def summarize_args(name: str, verbose: bool) -> int:
    message = f"Running as {name!r} with Python {sys.version.split()[0]}"
    print(message)
    if verbose:
        print(f"Executable: {sys.executable}")
        print(f"Prefix    : {sys.prefix}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="codecraft")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    return summarize_args(args.name, args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
```
""",
                complexity="""
| Activity | Time cost | Notes |
| --- | --- | --- |
| REPL exploration | Seconds | Great for O(1) curiosity checks |
| Script + argparse | Minutes once, then reusable | Beats retyping |
| Unpinned pip installs | Cheap now, expensive later | Version drift is Θ(chaos) |
| Freeze / lock | Seconds | Prevents "works yesterday" bugs |
""",
                tricks="""
- `python -i module.py` drops into REPL *after* running the script — state is live.
- Put scripts under a `scripts/` folder; keep importable packages elsewhere.
- Use `pip download` offline mirrors when air-gapped.
- Separate `requirements.txt` (prod) from `requirements-dev.txt` (pytest, black, mypy).
""",
                mistakes="""
- Running `pip install` while the wrong venv (or none) is active.
- Calling `python script.py` from a different directory than expected without fixing paths.
- Forgetting `raise SystemExit(main())` so exit codes are always 0 in CI.
- Freezing the entire global environment into a project's requirements.
- Using `sudo pip` — almost never correct on modern systems.
""",
                interview="""
Be ready to explain: Why `if __name__ == "__main__"`? What does pip install into? How do you
reproduce a teammate's environment? Strong answers mention site-packages, venv isolation, and
pinned requirements vs lock files (pip-tools / Poetry / uv).
""",
                practice="""
1. **Argparse Greeter** (easy) — build the greeter above; add a `--shout` flag. [Practice: python-ex-argparse-greeter]
2. **Pip Audit** (easy) — `pip list`, `pip show`, and document where a package lives on disk.
3. **Exit Codes** (medium) — return non-zero when `--name` is empty; verify with `echo $LASTEXITCODE` / `$?`.
""",
                summary="""
- REPL for exploration; scripts for persistence; pip for dependencies.
- Always structure scripts with `main()` + `__name__` guard.
- Prefer `python -m pip` and pin what you ship.
- Freeze requirements from an *activated project venv*, not the global Python.
""",
                further="""
- [argparse tutorial](https://docs.python.org/3/howto/argparse.html)
- [pip user guide](https://pip.pypa.io/en/stable/user_guide/)
- [Python -m switch](https://docs.python.org/3/using/cmdline.html#cmdoption-m)
""",
            ),
        )
    )

    paths.append(
        write_lesson(
            "01-getting-started",
            "03-virtual-environments.mdx",
            fm(
                "Virtual Environments in Depth",
                "python-virtual-environments",
                "Create, activate, troubleshoot, and manage virtual environments with venv, and understand how isolation protects projects.",
                28,
                "beginner",
                ["python-intro-and-setup", "python-repl-scripts-pip"],
                ["python", "venv", "isolation", "dependencies"],
                3,
            ),
            lesson(
                why="""
Dependency conflicts are the silent killer of Python productivity. Project A needs `requests==2.28`
while Project B needs a fork that pulls `urllib3` differently; without isolation, upgrading one
breaks the other. Virtual environments give every project its own `site-packages`, `python`
binary shim, and activation story — the industry default before containers enter the picture.
""",
                intuition="""
Imagine shared kitchen cabinets vs a personal pantry. A venv is your pantry: flour (packages)
you buy stays here. Activation is unlocking that pantry so cooking commands (`python`, `pip`)
reach *your* ingredients first via `PATH`. Deactivate restores the shared kitchen.

`sys.prefix` and `sys.executable` tell you whose pantry you opened. Always check them when
confused.
""",
                core="""
### Creating environments

```bash
python -m venv .venv
# optional: without pip (rare)
python -m venv --without-pip .venv
# optional: copy instead of symlink (some Windows cases)
python -m venv --copies .venv
```

### Activation matrix

| OS / shell | Activate | Deactivate |
| --- | --- | --- |
| Windows PowerShell | `.\\.venv\\Scripts\\Activate.ps1` | `deactivate` |
| Windows cmd | `.venv\\Scripts\\activate.bat` | `deactivate` |
| macOS / Linux bash/zsh | `source .venv/bin/activate` | `deactivate` |
| Fish | `source .venv/bin/activate.fish` | `deactivate` |

If PowerShell blocks scripts, run once (current user):
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

### What a venv contains

- `pyvenv.cfg` — points at the base interpreter
- `Scripts/` or `bin/` — `python`, `pip`, activate scripts
- `Lib/site-packages/` — installed third-party code

### Alternatives (awareness)

| Tool | Role |
| --- | --- |
| `venv` | Stdlib, enough for most courses and apps |
| `virtualenv` | Faster / older alternative, more flags |
| Conda | Env + binary packages (data science) |
| Poetry / PDM / uv | Env + dependency resolver + packaging |
| Docker | OS-level isolation beyond Python packages |

For this academy, master `venv` first; other tools build on the same isolation idea.
""",
                diagram="""
```mermaid
flowchart TB
    Base[System Python 3.12] --> V1[.venv Project A]
    Base --> V2[.venv Project B]
    V1 --> SA[site-packages A: django==4.2]
    V2 --> SB[site-packages B: flask==3.0]
    Act[Activate A] --> PathA[PATH prefers V1/Scripts]
    PathA --> RunA["python sees django, not flask"]
```
""",
                dryrun="""
| Step | Action | Check |
| --- | --- | --- |
| 1 | `python -m venv .venv` | `.venv/pyvenv.cfg` exists |
| 2 | Activate | Prompt prefix `(.venv)` |
| 3 | `python -c "import sys; print(sys.prefix)"` | Path ends with `.venv` |
| 4 | `python -m pip install httpx` | Lands under `.venv` |
| 5 | `deactivate` then same print | Prefix is base Python again |
""",
                code="""
```python
import os
import sys
from pathlib import Path


def venv_report() -> dict[str, object]:
    base = getattr(sys, "base_prefix", sys.prefix)
    in_venv = sys.prefix != base
    return {
        "in_venv": in_venv,
        "prefix": sys.prefix,
        "base_prefix": base,
        "executable": sys.executable,
        "VIRTUAL_ENV": os.environ.get("VIRTUAL_ENV"),
        "site_packages_guess": str(Path(sys.prefix) / "Lib" / "site-packages"),
    }


if __name__ == "__main__":
    for key, value in venv_report().items():
        print(f"{key:20} {value}")
```
""",
                complexity="""
Creating a venv is O(files copied) — typically seconds. The *human* complexity of skipping
venvs grows with project count: each new global package multiplies conflict probability.
Treat isolation as constant-time insurance.
""",
                tricks="""
- Add `.venv/` to `.gitignore` (GitHub's Python gitignore already does).
- In VS Code / Cursor, select the interpreter inside `.venv` explicitly.
- Recreate freely: delete `.venv`, remake, `pip install -r requirements.txt`.
- Use one venv per project root; nest only if you truly know why.
""",
                mistakes="""
- Activating in one terminal, running the IDE's different interpreter.
- Moving a venv folder — paths break; recreate instead.
- Mixing Conda `activate` with venv activate in the same shell without checking `which python`.
- Committing platform-specific binaries from `Scripts/`.
""",
                interview="""
Explain: "A virtual environment isolates third-party packages per project by giving you a
dedicated prefix and site-packages, selected via PATH when activated." Mention Docker as the
next isolation layer for OS dependencies.
""",
                practice="""
1. **Venv Detective** (easy) — run the report script before/after activate. [Practice: python-ex-venv-detective]
2. **Two Projects** (medium) — two folders, two venvs, conflicting package versions; prove isolation.
3. **Broken PATH** (medium) — intentionally call the wrong python; diagnose with `sys.executable`.
""",
                summary="""
- `python -m venv .venv` per project; activate before installing.
- Verify with `sys.prefix` / `sys.executable` / `$env:VIRTUAL_ENV`.
- Recreate venvs; never relocate them.
- venv isolates Python packages — not the whole OS (that's containers).
""",
                further="""
- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Python Packaging User Guide — Virtual Environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
""",
            ),
        )
    )
    return paths


if __name__ == "__main__":
    # Smoke test module 01 only first
    gen_01()
    print("module 01 ok")
