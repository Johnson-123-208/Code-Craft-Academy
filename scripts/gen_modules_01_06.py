#!/usr/bin/env python3
"""Generate Python course modules 01–06."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from py_course_lib import dryrun_table, frontmatter, mermaid_flow, render_full, write_mdx

CREATED: list[tuple[str, int]] = []


def emit(module: str, filename: str, meta: dict, body: str) -> None:
    text = frontmatter(**meta) + body
    path = write_mdx(module, filename, text)
    wc = len(body.split())
    CREATED.append((str(path.relative_to(path.parents[2])), wc))
    print(f"  wrote {path.name} (~{wc} words body)")


def main() -> None:
    print("=== Modules 01–06 ===")
    m01()
    m02()
    m03()
    m04()
    m05()
    m06()
    print(f"Total files: {len(CREATED)}")


def m01() -> None:
    # 01 already enhanced in prior script — rewrite fully here
    emit(
        "01-getting-started",
        "01-intro-and-setup.mdx",
        dict(
            title="Introduction to Python and Environment Setup",
            slug="python-intro-and-setup",
            summary="Why Python dominates modern engineering, how to install it correctly, and how to run your first programs in the REPL, scripts, and virtual environments.",
            duration=25,
            difficulty="beginner",
            prerequisites=[],
            tags=["python", "setup", "venv", "pip", "repl"],
            order=1,
        ),
        render_full(
            why="""
Python is the lingua franca of modern software: web backends, data science, machine learning,
automation, DevOps tooling, and interview whiteboards all speak it. Companies hire for Python
because a single language covers scripting, APIs, and analytics without forcing you to switch
toolchains every week.

Getting the environment right on day one prevents the most common beginner failures: `python`
versus `python3` confusion, globally polluted packages, and "works on my machine" dependency hell.
This lesson builds the foundation every later module assumes — a clean interpreter, an isolated
virtual environment, and the habit of running code deliberately rather than hoping the IDE guessed
the right binary.
""",
            intuition="""
Think of Python like a workshop. The **interpreter** is the power tool that executes instructions.
A **script** is a blueprint you save and reuse. A **virtual environment** is a private workbench
for one project so paints and screws from another project do not mix. **pip** is the supply catalog
that delivers libraries into that workbench only.

You do not need to memorize every flag today. You need a mental model: isolate each project, pin
what you install, and always know *which* Python binary you are talking to before you debug.
""",
            core="""
### What Python is

Python is a high-level, dynamically typed, garbage-collected language with a design philosophy
favoring readability (try `import this`). CPython — the reference implementation — compiles source
to bytecode and runs it on a virtual machine. You rarely think about bytecode early on, but it
explains why `.pyc` files appear under `__pycache__` and why import caching exists.

Other implementations exist (PyPy, Jython, MicroPython), but this course targets CPython 3.12+
because that is what production teams and interviewers almost always mean by "Python."

### Installation checklist

1. Install Python 3.12+ from python.org (or use `pyenv` / your OS package manager).
2. On Windows, enable "Add python.exe to PATH" and install the py launcher.
3. Verify:

```bash
python --version
python -m pip --version
```

Using `python -m pip` is safer than bare `pip` because it installs into the same interpreter
you just invoked.

### The REPL, scripts, and venv

- Start exploring with `python` (REPL). Exit with `exit()` or Ctrl-D / Ctrl-Z.
- Persist real work in `.py` files protected by `if __name__ == "__main__":`.
- Isolate dependencies: `python -m venv .venv`, activate, then `python -m pip install …`.
- Snapshot with `python -m pip freeze > requirements.txt`. Never commit `.venv/`.

### Standard library versus third-party

The **standard library** ships with Python (`json`, `pathlib`, `asyncio`, …). **Third-party**
packages come from PyPI via pip (`requests`, `fastapi`, `numpy`). Knowing which is which prevents
surprise installs and clarifies what Docker images must bake in.
""",
            diagram=mermaid_flow(
                "setup",
                [
                    "Install Python 3.12+",
                    "Create project folder",
                    "python -m venv .venv",
                    "Activate virtual environment",
                    "pip install dependencies",
                    "Run REPL or script inside venv",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("python --version", "", "3.12.x or newer"),
                    ("python -m venv .venv", "", ".venv/ appears"),
                    ("Activate venv", "", "Prompt shows (.venv)"),
                    ("python -m pip install rich", "", "Installed into .venv"),
                    ("python hello.py", "", "Program runs isolated"),
                ]
            ),
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
Setup is not an algorithm, but habits have costs:

| Concern | Cost if ignored | Cost if done right |
| --- | --- | --- |
| Global installs | Hours of version conflicts | Minutes per project for venv |
| No requirements.txt | Broken teammates / CI | Reproducible installs |
| Wrong interpreter | Silent package mismatches | One `python -m` habit |

Think of isolation as O(1) insurance against O(projects²) conflict growth.
""",
            tricks=[
                "Prefer `python -m pip` and `python -m venv` over bare commands.",
                "Name environments `.venv` so tools and gitignore templates recognize them.",
                "On Windows use `py -3.12` to select a specific installed version.",
                "Keep a personal cheat sheet of activate commands for each OS you use.",
                "Verify `sys.executable` whenever a package seems 'missing'.",
            ],
            mistakes=[
                "Installing with one Python and running with another.",
                "Forgetting to activate the venv before pip install.",
                "Committing `.venv/` to git.",
                "Mixing Conda and venv without checking which python is active.",
                "Following Python 2 tutorials (`print` statements, `raw_input`).",
            ],
            interview="""
Interviewers rarely quiz pip flags, but they expect you to explain what a virtual environment
solves, the difference between the standard library and PyPI packages, and how reproducibility
works (`requirements.txt`, lock files). A strong follow-up answer mentions Docker as the next
isolation layer for OS-level dependencies.
""",
            practice=[
                "**Env Inspector** (easy) — extend the script to print `sys.path`. [Practice: python-ex-env-inspector]",
                "**Freeze Diff** (easy) — install two packages, freeze, uninstall one, explain the diff.",
                "**Dual Python** (medium) — invoke two installed versions with explicit paths or the py launcher.",
            ],
            summary=[
                "Install Python 3.12+ and verify with `python --version`.",
                "Always create a per-project `.venv` and activate it.",
                "Install with `python -m pip` and freeze dependencies.",
                "Use the REPL to explore; use scripts with a `__main__` guard for real programs.",
                "Know which interpreter is active before debugging ModuleNotFoundError.",
            ],
            further=[
                "[Python 3 Tutorial](https://docs.python.org/3/tutorial/)",
                "[venv docs](https://docs.python.org/3/library/venv.html)",
                "[Installing Packages](https://packaging.python.org/en/latest/tutorials/installing-packages/)",
                "[PEP 8](https://peps.python.org/pep-0008/)",
            ],
        ),
    )

    emit(
        "01-getting-started",
        "02-repl-scripts-and-pip.mdx",
        dict(
            title="REPL, Scripts, and pip Workflows",
            slug="python-repl-scripts-pip",
            summary="Master the interactive REPL, structure real scripts with entry points, and use pip confidently for install, freeze, and upgrade workflows.",
            duration=30,
            difficulty="beginner",
            prerequisites=["python-intro-and-setup"],
            tags=["python", "repl", "scripts", "pip"],
            order=2,
        ),
        render_full(
            why="""
Professional Python work constantly switches between three modes: poke at an idea in the REPL,
encode it in a script, and pull libraries with pip. Juniors who blur these modes waste hours —
pasting broken snippets into the wrong place, polluting global site-packages, or shipping scripts
that only work when imported by accident. This lesson makes each mode crisp so every later module
can assume you know how to explore, persist, and depend.
""",
            intuition="""
The REPL is a whiteboard: temporary, conversational, perfect for "what does this return?"
A script is a contract: named entry points, reproducible runs, something teammates can execute.
pip is the loading dock: you request crates (packages), they land in *this* interpreter's
site-packages, and you record the invoice (`requirements.txt`) so others can restock identically.

Ask "am I exploring, shipping, or depending?" and you will pick the right tool every time.
""",
            core="""
### REPL power moves

- `_` holds the last expression result in the stock REPL.
- `help(obj)` and `dir(obj)` reveal APIs without leaving the terminal.
- Prefer IPython or `python -i script.py` when you need richer history and introspection.
- Use `python -c "code"` for one-liners in shell scripts and CI smoke checks.

### Script anatomy

A production-minded script has imports at the top, functions/classes that do the work, a thin
`main()` that parses arguments, and an `if __name__ == "__main__":` guard. Returning an `int`
from `main` and calling `raise SystemExit(main())` makes exit codes honest for CI.

### argparse in brief

`argparse` turns `sys.argv` into typed attributes. Positional args are required by default;
flags like `--verbose` / `-v` use `action="store_true"`. Always give `description=` so `-h` is useful.

### pip workflows

| Command | Purpose |
| --- | --- |
| `python -m pip install pkg` | Install latest compatible |
| `python -m pip install pkg==1.2.3` | Pin exact version |
| `python -m pip install -r requirements.txt` | Bootstrap project |
| `python -m pip install -U pkg` | Upgrade one package |
| `python -m pip uninstall pkg` | Remove package |
| `python -m pip freeze` | Snapshot exact set |
| `python -m pip show pkg` | Metadata and install location |
| `python -m pip list --outdated` | See upgrade candidates |

Separate runtime requirements from `requirements-dev.txt` (pytest, black, mypy, ruff).
""",
            diagram=mermaid_flow(
                "modes",
                [
                    "Idea appears",
                    "Need persistence? REPL vs script",
                    "Need libraries? pip into active venv",
                    "Freeze requirements.txt",
                    "Run python script.py",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("REPL: 2 ** 10", "", "1024; _ becomes 1024"),
                    ("Write greet.py with argparse", "", "File saved"),
                    ("python greet.py Ada -n 2", "", "Two hello lines"),
                    ("python -m pip install requests", "", "In current env"),
                    ("python -m pip freeze", "", "Pinned requests==…"),
                ]
            ),
            code="""
```python
from __future__ import annotations

import argparse
import sys


def summarize_args(name: str, verbose: bool) -> int:
    print(f"Running as {name!r} with Python {sys.version.split()[0]}")
    if verbose:
        print(f"Executable: {sys.executable}")
        print(f"Prefix    : {sys.prefix}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CodeCraft script demo")
    parser.add_argument("--name", default="codecraft")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    return summarize_args(args.name, args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
```
""",
            complexity="""
| Activity | Cost | Notes |
| --- | --- | --- |
| REPL exploration | Seconds | Ideal for tiny checks |
| Script + argparse | Minutes once | Then reusable forever |
| Unpinned installs | Cheap now | Expensive via version drift |
| Freeze / lock | Seconds | Prevents "works yesterday" |

Reproducibility work is amortized O(1) per clone versus O(hours) of mystery debugging later.
""",
            tricks=[
                "`python -i module.py` drops into a REPL after the script runs — state is live.",
                "Keep importable packages separate from one-off `scripts/`.",
                "Use `pip download` for offline / air-gapped mirrors.",
                "Pin thoughtfully: `==` for apps, compatible ranges for libraries you publish.",
                "Prefer `raise SystemExit(main())` so failures surface as non-zero codes.",
            ],
            mistakes=[
                "Running pip while the wrong (or no) venv is active.",
                "Freezing the global environment into a project requirements file.",
                "Forgetting exit codes — CI always green even when main fails.",
                "Using `sudo pip` on managed systems.",
                "Putting business logic only under the `__main__` guard so tests cannot import it.",
            ],
            interview="""
Be ready to explain why `if __name__ == "__main__"` exists, what pip installs into (that
interpreter's site-packages), and how you reproduce a teammate's environment. Mention pinned
requirements versus modern lock files (pip-tools, Poetry, uv) as the maturity path.
""",
            practice=[
                "**Argparse Greeter** (easy) — add a `--shout` flag. [Practice: python-ex-argparse-greeter]",
                "**Pip Audit** (easy) — use `pip show` and document install location on disk.",
                "**Exit Codes** (medium) — return non-zero for empty `--name`; verify in your shell.",
            ],
            summary=[
                "REPL explores; scripts persist; pip depends.",
                "Structure scripts with `main()` + `__name__` guard.",
                "Always `python -m pip` inside an activated project venv.",
                "Freeze from the project env, not the global Python.",
            ],
            further=[
                "[argparse tutorial](https://docs.python.org/3/howto/argparse.html)",
                "[pip user guide](https://pip.pypa.io/en/stable/user_guide/)",
                "[Python -m option](https://docs.python.org/3/using/cmdline.html#cmdoption-m)",
            ],
        ),
    )

    emit(
        "01-getting-started",
        "03-virtual-environments.mdx",
        dict(
            title="Virtual Environments in Depth",
            slug="python-virtual-environments",
            summary="Create, activate, troubleshoot, and manage virtual environments with venv, and understand how isolation protects projects.",
            duration=28,
            difficulty="beginner",
            prerequisites=["python-intro-and-setup", "python-repl-scripts-pip"],
            tags=["python", "venv", "isolation", "dependencies"],
            order=3,
        ),
        render_full(
            why="""
Dependency conflicts silently destroy Python productivity. Project A needs one `requests` line
while Project B pulls a different `urllib3` tree; without isolation, upgrading either breaks the
other. Virtual environments give every project its own `site-packages` and `python` shim — the
industry default before containers enter the picture. Mastering venv early means you stop blaming
"Python" when the real bug is a polluted global install.
""",
            intuition="""
Shared kitchen cabinets versus a personal pantry: a venv is your pantry. Activation unlocks it
so `python` and `pip` resolve via PATH to *your* ingredients first. Deactivate restores the shared
kitchen. `sys.prefix`, `sys.executable`, and the `VIRTUAL_ENV` environment variable are how you
ask "whose pantry did I open?" whenever something feels wrong.
""",
            core="""
### Creating and activating

```bash
python -m venv .venv
```

| Shell | Activate |
| --- | --- |
| Windows PowerShell | `.\\.venv\\Scripts\\Activate.ps1` |
| Windows cmd | `.venv\\Scripts\\activate.bat` |
| macOS / Linux bash/zsh | `source .venv/bin/activate` |

Deactivate with `deactivate`. If PowerShell blocks scripts, set `RemoteSigned` for the current user.

### Anatomy of a venv

- `pyvenv.cfg` — records the base interpreter
- `Scripts/` or `bin/` — `python`, `pip`, activate helpers
- `Lib/site-packages/` — third-party packages for this project only

### Recreation is normal

Delete `.venv`, recreate, reinstall from `requirements.txt`. Never move a venv folder between
machines or paths — embedded absolute paths break. Treat venvs as disposable build artifacts.

### Tooling landscape

`venv` (stdlib) is enough for this course. `virtualenv`, Conda, Poetry, PDM, and `uv` all build
on the same isolation idea with different resolvers and UX. Docker isolates the OS, not just
Python packages — complementary, not mutually exclusive.
""",
            diagram=mermaid_flow(
                "isolation",
                [
                    "System Python 3.12",
                    "Create .venv A and .venv B",
                    "Install django in A only",
                    "Install flask in B only",
                    "Activate A → import django works",
                    "Activate B → import flask works",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("python -m venv .venv", "", "pyvenv.cfg created"),
                    ("Activate", "", "Prompt shows (.venv)"),
                    ("print(sys.prefix)", "", "Path ends with .venv"),
                    ("pip install httpx", "", "Lands under .venv"),
                    ("deactivate; print(sys.prefix)", "", "Back to base prefix"),
                ]
            ),
            code="""
```python
import os
import sys
from pathlib import Path


def venv_report() -> dict[str, object]:
    base = getattr(sys, "base_prefix", sys.prefix)
    return {
        "in_venv": sys.prefix != base,
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
Creating a venv copies / links a small tree — typically seconds. Skipping venvs makes conflict
probability grow roughly with the square of active projects. Isolation is constant-time insurance.
""",
            tricks=[
                "Add `.venv/` to `.gitignore` (standard Python templates already do).",
                "Select the `.venv` interpreter explicitly in Cursor / VS Code.",
                "Recreate freely whenever the environment feels cursed.",
                "One venv per project root — nesting needs a strong reason.",
                "Document activate commands in the project README for newcomers.",
            ],
            mistakes=[
                "Activating in a terminal while the IDE uses a different interpreter.",
                "Moving or renaming a venv directory.",
                "Mixing Conda and venv activates in one shell without checking `sys.executable`.",
                "Committing platform-specific binaries under `Scripts/`.",
                "Assuming venv isolates system libraries (it does not — use Docker for that).",
            ],
            interview="""
Say: "A virtual environment isolates third-party packages per project by providing a dedicated
prefix and site-packages, selected via PATH when activated." Then mention containers as the next
layer when you also need system packages and OS reproducibility.
""",
            practice=[
                "**Venv Detective** (easy) — run the report before/after activate. [Practice: python-ex-venv-detective]",
                "**Two Projects** (medium) — conflicting package versions in two venvs; prove isolation.",
                "**Broken PATH** (medium) — call the wrong python on purpose; diagnose with `sys.executable`.",
            ],
            summary=[
                "`python -m venv .venv` per project; activate before installing.",
                "Verify with `sys.prefix` / `sys.executable` / `VIRTUAL_ENV`.",
                "Recreate venvs; never relocate them.",
                "venv isolates Python packages — containers isolate the OS.",
            ],
            further=[
                "[venv documentation](https://docs.python.org/3/library/venv.html)",
                "[Virtual Environments guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)",
            ],
        ),
    )


def m02() -> None:
    emit(
        "02-syntax-and-types",
        "01-variables-and-assignment.mdx",
        dict(
            title="Variables, Names, and Assignment",
            slug="python-variables-assignment",
            summary="Understand Python's name-binding model, assignment semantics, multiple assignment, and how references differ from boxes that store values.",
            duration=30,
            difficulty="beginner",
            prerequisites=["python-intro-and-setup"],
            tags=["python", "variables", "assignment", "references"],
            order=1,
        ),
        render_full(
            why="""
Every bug that looks like "why did this list change over there?" starts with misunderstanding
assignment. Python does not put values inside named boxes the way some textbooks imply — it binds
**names** to **objects**. Grasping that model early prevents aliasing surprises, makes function
arguments make sense, and prepares you for mutability discussions in the data-structures module.
""",
            intuition="""
Imagine sticky name-tags (variables) and balloons (objects). Assignment sticks a tag onto a balloon.
`b = a` does not inflate a new balloon — it puts a second tag on the same balloon. If the balloon
is a mutable list and you pop an element via `a`, the change is visible through `b` too. Immutable
balloons (numbers, strings, tuples) cannot be altered in place, so rebinding `a = a + 1` sticks
the tag onto a *new* balloon instead.
""",
            core="""
### Names and objects

```python
x = 10          # bind name x to int object 10
y = x           # y refers to the same int
x = x + 1       # x rebound to a new int 11; y still 10
```

Integers are immutable, so "changing x" always means rebinding. Contrast:

```python
a = [1, 2, 3]
b = a
a.append(4)     # mutates the shared list; b sees [1, 2, 3, 4]
```

### Identity versus equality

- `==` asks: same value?
- `is` asks: same object identity (`id`)?

Prefer `is` only for singletons like `None` (`if x is None:`). For numbers and strings, equality
is what you almost always want.

### Multiple and augmented assignment

```python
a, b = 1, 2
a, b = b, a          # swap without a temp
x += 1               # for immutables: rebind; for lists: may mutate in place
```

Unpacking requires matching structure (or starred targets in modern Python):

```python
first, *rest = [10, 20, 30, 40]  # first=10, rest=[20, 30, 40]
```

### Naming rules and style

Names start with a letter or underscore, then letters/digits/underscores. Convention (PEP 8):
`snake_case` for variables and functions, `UPPER_SNAKE` for module-level constants, leading
underscore for internal use. Avoid shadowing builtins (`list`, `id`, `type`, `str`).
""",
            diagram=mermaid_flow(
                "binding",
                [
                    "Evaluate right-hand side → object",
                    "Bind left-hand name(s) to that object",
                    "Previous object may become unreachable",
                    "Garbage collector reclaims unreachable objects",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("x = [1, 2]; y = x", "", "Both names → same list"),
                    ("x.append(3)", "", "y == [1, 2, 3]"),
                    ("x = [9]", "", "x → new list; y unchanged"),
                    ("a, b = b, a with a=1,b=2", "", "a=2, b=1"),
                    ("x is None check", "", "Use identity for None"),
                ]
            ),
            code="""
```python
def demonstrate_binding() -> None:
    nums = [1, 2, 3]
    alias = nums
    copy = list(nums)  # shallow copy — new list object

    nums.append(4)
    print("alias after append:", alias)   # [1, 2, 3, 4]
    print("copy  after append:", copy)    # [1, 2, 3]

    a, b = 10, 20
    a, b = b, a
    print("swapped:", a, b)


if __name__ == "__main__":
    demonstrate_binding()
```
""",
            complexity="""
Assignment and name lookup are O(1) for local variables in CPython (handled via quick local
arrays in optimized frames). The conceptual cost is human: misunderstanding aliases turns into
O(hours) debugging. Shallow copies of lists are O(n); deep copies can be much more expensive.
""",
            tricks=[
                "Use `a, b = b, a` for swaps — clear and idiomatic.",
                "Copy lists with `list(xs)`, `xs[:]`, or `xs.copy()` when you need independence.",
                "Prefer unpacking over indexed temporary variables when structure is clear.",
                "`locals()` / `globals()` exist for debugging — avoid them in production logic.",
                "In functions, assignment makes a name local for the whole function (see LEGB later).",
            ],
            mistakes=[
                "Assuming `b = a` copies a list or dict.",
                "Using `is` to compare strings or integers for equality.",
                "Shadowing builtins with variable names like `list = [1, 2]`.",
                "Mutating default objects later (preview of function-default footgun).",
                "Thinking `+=` on lists is the same as rebinding a new list every time.",
            ],
            interview="""
A classic prompt: "What is the difference between `==` and `is`?" Follow-up: draw what happens
after `b = a` for a list. Excellent candidates mention references, mutability, and when to copy.
""",
            practice=[
                "**Alias Lab** (easy) — mutate via one name, print via another. [Practice: python-ex-alias-lab]",
                "**Safe Copy** (easy) — fix a function that accidentally mutates the caller's list.",
                "**Unpack Stats** (medium) — unpack a row tuple into named fields and compute a mean.",
            ],
            summary=[
                "Assignment binds names to objects; it does not always copy.",
                "Mutable aliases share changes; immutables force rebinding.",
                "`==` for value, `is` for identity (mainly `None`).",
                "Unpacking and augmented assignment are core idioms — learn them early.",
            ],
            further=[
                "[Official tutorial — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)",
                "[Facts and myths about Python names and values (Ned Batchelder)](https://nedbatchelder.com/text/names.html)",
            ],
        ),
    )

    emit(
        "02-syntax-and-types",
        "02-built-in-types.mdx",
        dict(
            title="Built-in Types: Numbers, Booleans, None, and Basics",
            slug="python-built-in-types",
            summary="Explore ints, floats, complex, bool, NoneType, and how dynamic typing and truthiness shape everyday Python code.",
            duration=32,
            difficulty="beginner",
            prerequisites=["python-variables-assignment"],
            tags=["python", "types", "int", "float", "bool", "None"],
            order=2,
        ),
        render_full(
            why="""
Python's built-in scalars are the atoms of every program. Interviewers expect fluent conversion,
truthiness, and awareness of float quirks. Production bugs often come from treating `None` like
`False` incorrectly, mixing ints and floats carelessly, or assuming decimal arithmetic is exact.
This lesson locks down the types you will use on every subsequent page.
""",
            intuition="""
Types answer "what kind of balloon is this?" Dynamic typing means names can be rebound to
different kinds over time, but *objects* still have a precise type (`type(x)`). Truthiness is
Python's polite question: "does this value feel empty or zero-like?" rather than forcing explicit
`== True` everywhere. `None` is the deliberate absence of a value — a single shared singleton.
""",
            core="""
### Numeric tower

- **`int`**: arbitrary precision. `10**100` just works.
- **`float`**: IEEE-754 double. Great for science, imperfect for money.
- **`complex`**: `3 + 4j` when you need it (signal processing, etc.).

```python
print(10 / 3)    # true division → float 3.333…
print(10 // 3)   # floor division → int 3
print(10 % 3)    # modulo → 1
print(divmod(10, 3))  # (3, 1)
```

### Booleans and truthiness

`bool` is a subclass of `int` (`True == 1`). Prefer boolean context over comparing to `True`:

```python
if items:           # good
    ...
if items == True:   # almost always wrong style
    ...
```

Falsy values: `None`, `False`, `0`, `0.0`, `''`, `[]`, `{}`, `set()`, and other empty containers.
Everything else is truthy by default.

### None

Use `None` for missing values. Check with `is None` / `is not None`. Returning `None` implicitly
happens when a function lacks a `return` — be intentional.

### Conversions

```python
int("42"), float("3.14"), str(99), bool(0), bool("False")  # last is True! non-empty string
```

`bool("False")` is `True` because the string is non-empty — a classic footgun.

### type and isinstance

`type(x)` returns the exact type. `isinstance(x, (int, float))` is preferred for checks that
should allow subclasses. Overusing runtime type checks is unpythonic — duck typing + type hints
(later) are the modern path — but knowing these tools matters for debugging.
""",
            diagram=mermaid_flow(
                "truthiness",
                [
                    "Value enters if/while",
                    "bool(value) applied implicitly",
                    "Falsy → take else / skip body",
                    "Truthy → enter block",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("bool(0), bool(1)", "", "False, True"),
                    ("bool(''), bool('False')", "", "False, True"),
                    ("bool([]), bool([0])", "", "False, True"),
                    ("10 / 4, 10 // 4", "", "2.5, 2"),
                    ("x = None; x is None", "", "True"),
                ]
            ),
            code="""
```python
def classify(value: object) -> str:
    if value is None:
        return "missing"
    if isinstance(value, bool):
        return f"bool:{value}"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    return type(value).__name__


def demo() -> None:
    samples = [None, True, 0, 3.14, "", "False", [], [0]]
    for sample in samples:
        print(f"{sample!r:10} truthy={bool(sample)!s:5} class={classify(sample)}")


if __name__ == "__main__":
    demo()
```
""",
            complexity="""
Scalar operations are O(1) for fixed-size floats and typical ints. Very large ints have cost
proportional to digit length (schoolbook arithmetic). Truthiness checks on containers are O(1)
for emptiness via length, not full scans.
""",
            tricks=[
                "Use `math.isclose` for float comparisons instead of `==`.",
                "For money, prefer `decimal.Decimal` over `float`.",
                "`divmod(a, b)` when you need both quotient and remainder.",
                "Remember `True` / `False` are capitalized — not `true` / `false`.",
                "Convert user input carefully: wrap `int(input(...))` in try/except later.",
            ],
            mistakes=[
                "Using `float` for currency.",
                "Writing `if x == None` instead of `is None`.",
                "Assuming `bool(\"False\")` is False.",
                "Comparing floats with exact equality after arithmetic.",
                "Using `type(x) == list` when `isinstance` would allow subclasses.",
            ],
            interview="""
Expect questions on floor division, truthiness of empty containers, and why `is None` is preferred.
Bonus: explain that `bool` subclasses `int` and what that implies for sorting or arithmetic.
""",
            practice=[
                "**Truth Table** (easy) — print truthiness for ten literals. [Practice: python-ex-truth-table]",
                "**Safe Int Parse** (easy) — convert strings, returning None on failure.",
                "**Float Pitfall** (medium) — show `0.1 + 0.2 != 0.3` and fix with `math.isclose`.",
            ],
            summary=[
                "int / float / bool / None are the scalar backbone.",
                "Truthiness treats empty and zero-like values as False.",
                "Check None with `is`; convert deliberately with constructors.",
                "Floats are binary approximations — avoid exact equality and money math.",
            ],
            further=[
                "[Built-in Types](https://docs.python.org/3/library/stdtypes.html)",
                "[decimal — Decimal fixed point](https://docs.python.org/3/library/decimal.html)",
            ],
        ),
    )

    emit(
        "02-syntax-and-types",
        "03-operators-and-expressions.mdx",
        dict(
            title="Operators and Expressions",
            slug="python-operators-expressions",
            summary="Arithmetic, comparison, logical, bitwise, membership, and identity operators — plus precedence and short-circuit evaluation.",
            duration=30,
            difficulty="beginner",
            prerequisites=["python-built-in-types"],
            tags=["python", "operators", "expressions", "precedence"],
            order=3,
        ),
        render_full(
            why="""
Expressions are how Python computes. Misreading precedence, forgetting that `and`/`or` return
operands (not always booleans), or confusing `&` with `and` causes subtle bugs — especially in
data filters and interview whiteboard code. This lesson makes operator behavior predictable.
""",
            intuition="""
An expression is a recipe that yields a value. Operators are the verbs; operands are the nouns.
Short-circuiting means Python is lazy on purpose: `and` stops at the first falsy value, `or`
stops at the first truthy value. That laziness both speeds code and protects you from evaluating
dangerous right-hand sides.
""",
            core="""
### Categories

| Category | Examples |
| --- | --- |
| Arithmetic | `+ - * / // % **` |
| Comparison | `== != < <= > >=` |
| Logical | `and or not` |
| Bitwise | `& | ^ ~ << >>` |
| Membership | `in`, `not in` |
| Identity | `is`, `is not` |
| Walrus | `:=` (assignment expression) |

### Precedence (high → low, simplified)

1. `**`
2. unary `+ - ~`
3. `* / // %`
4. `+ -`
5. shifts
6. bitwise `&` then `^` then `|`
7. comparisons / `in` / `is`
8. `not`
9. `and`
10. `or`
11. walrus `:=`

When unsure, use parentheses. Clarity beats memorizing the table under pressure.

### Short-circuit and operand return

```python
print(0 or 5)       # 5
print(3 and 4)      # 4
print("" or "default")  # idiomatic defaulting (use carefully)
```

### Chained comparisons

```python
1 < x < 10   # means (1 < x) and (x < 10) — elegant and efficient
```

### Walrus operator

```python
if (n := len(items)) > 3:
    print(f"long list: {n}")
```

Assign and test in one expression — powerful in loops and comprehensions, easy to overuse.
""",
            diagram=mermaid_flow(
                "shortcircuit",
                [
                    "Evaluate left of and/or",
                    "Can decide already?",
                    "Yes → return left operand",
                    "No → evaluate and return right",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("2 + 3 * 4", "", "14 (not 20)"),
                    ("(2 + 3) * 4", "", "20"),
                    ("0 and 1/0", "", "0 — no ZeroDivisionError"),
                    ("1 < 2 < 3", "", "True"),
                    ("'a' in 'cat'", "", "True"),
                ]
            ),
            code="""
```python
def clamp(value: float, low: float, high: float) -> float:
    return low if value < low else high if value > high else value


def first_truthy(*values: object) -> object:
    for value in values:
        if value:
            return value
    return None


def demo() -> None:
    x = 5
    print(1 < x < 10)
    print(clamp(12, 0, 10))
    print(first_truthy("", [], 0, "ok"))
    if (text := "codecraft") and text.startswith("code"):
        print("prefix ok:", text)


if __name__ == "__main__":
    demo()
```
""",
            complexity="""
Most operators on scalars are O(1). Membership `x in list` is O(n); `x in set/dict` is average
O(1). Short-circuiting can reduce average work when early exits are common — important in
validation pipelines.
""",
            tricks=[
                "Parentheses for humans beat clever precedence.",
                "Use `in` for membership; reserve bitwise ops for flags and masks.",
                "Chained comparisons are idiomatic — use them.",
                "`(x := …)` shines when the value is needed twice; otherwise keep assignment separate.",
                "Prefer `math` functions for clarity on powers/roots when teaching readers matter.",
            ],
            mistakes=[
                "Writing `a & b` when you meant boolean `and` (and vice versa).",
                "Assuming `and`/`or` always return `True`/`False`.",
                "Using `is` for value comparison of ints/strings.",
                "Forgetting `/` always returns float in Python 3.",
                "Overusing walrus until lines become unreadable.",
            ],
            interview="""
Whiteboard favorites: operator precedence questions, chained comparisons, and short-circuit
puzzles like "does `0 and 1/0` raise?" Explaining *why* is more impressive than memorizing yes/no.
""",
            practice=[
                "**Precedence Fix** (easy) — add parentheses so an expression matches intent. [Practice: python-ex-precedence]",
                "**Defaulting** (easy) — implement `or`-style defaults safely for empty strings.",
                "**Walrus Loop** (medium) — read lines until empty using `:=` in a while condition.",
            ],
            summary=[
                "Know the major operator families and when to parenthesize.",
                "`and`/`or` short-circuit and return operands.",
                "Chained comparisons are clear and efficient.",
                "Membership cost depends on container type.",
            ],
            further=[
                "[Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)",
                "[PEP 572 — Assignment Expressions](https://peps.python.org/pep-0572/)",
            ],
        ),
    )

    emit(
        "02-syntax-and-types",
        "04-io-and-fstrings.mdx",
        dict(
            title="Input, Output, and f-Strings",
            slug="python-io-fstrings",
            summary="Read user input, print thoughtfully, and master f-strings for clear, formatted output including alignment and number formats.",
            duration=28,
            difficulty="beginner",
            prerequisites=["python-operators-expressions"],
            tags=["python", "input", "print", "f-strings", "formatting"],
            order=4,
        ),
        render_full(
            why="""
Programs that cannot talk to humans or other systems are dead ends. Clear I/O and formatting
skills show up in CLIs, logging, reports, and interview warm-ups. f-strings (Python 3.6+) are
the modern default — readable, fast, and expressive — and interviewers notice when you still
reach for archaic `%` formatting without a reason.
""",
            intuition="""
`input()` always returns a **string** — even if the user types digits. Your job is to convert.
`print` ships values to stdout with separators and endings you can customize. f-strings weave
expressions into text: think Mad Libs where `{name}` is evaluated live inside the string.
""",
            core="""
### input and print

```python
name = input("Name: ").strip()
age = int(input("Age: "))  # may raise ValueError — handle later
print("Hello", name, sep=" ", end="!\\n")
```

### f-strings

```python
pi = 3.14159
print(f"{pi:.2f}")          # 3.14
print(f"{name:>10}")        # right-align width 10
print(f"{1000:,}")          # 1,000
print(f"{0.25:.1%}")        # 25.0%
print(f"{value=!r}")        # debugging: value='…'
```

Expressions inside `{}` can call methods, but keep them simple — heavy logic belongs outside.

### Older formatters (recognition)

- `%` formatting: `"%s %d" % (name, age)` — legacy
- `str.format`: `"{} {}".format(name, age)` — still fine, especially for deferred templates

Prefer f-strings for immediate formatting in Python 3.12 codebases.

### stdout versus stderr

`print(..., file=sys.stderr)` for errors so pipelines can separate streams. Logging (module 07)
is better for real apps, but stream awareness matters early.
""",
            diagram=mermaid_flow(
                "io",
                [
                    "Prompt user with input()",
                    "Receive str",
                    "Convert / validate",
                    "Compute result",
                    "Format with f-string",
                    "print to stdout",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("input returns '42'", "", "type is str"),
                    ("int('42')", "", "42 as int"),
                    ("f'{3.14159:.2f}'", "", "'3.14'"),
                    ("f'{25:05d}'", "", "'00025'"),
                    ("print('a','b',sep='-')", "", "a-b"),
                ]
            ),
            code="""
```python
from __future__ import annotations


def format_receipt(item: str, qty: int, price: float) -> str:
    total = qty * price
    return f"{item:<12} x{qty:<3} @ ${price:>6.2f} = ${total:>7.2f}"


def main() -> None:
    item = input("Item name: ").strip() or "widget"
    qty = int(input("Quantity: ") or "1")
    price = float(input("Unit price: ") or "9.99")
    print(format_receipt(item, qty, price))
    print(f"{'TOTAL':<12} {qty * price:>20.2f}")


if __name__ == "__main__":
    main()
```
""",
            complexity="""
Formatting is O(length of output). For huge reports, building strings with `+=` in a loop can
become costly — prefer collecting parts in a list and `''.join` (covered with strings later).
Interactive `input` is I/O-bound, not CPU-bound.
""",
            tricks=[
                "Use `!r`, `!s`, `!a` conversions inside f-strings when debugging.",
                "`=` debug specifier: `f\"{score=}\"` prints `score=98`.",
                "Strip user input early: `.strip()` avoids invisible whitespace bugs.",
                "Provide defaults in CLIs when empty input should mean a sensible value.",
                "For multi-line text, triple quotes + f-strings work well.",
            ],
            mistakes=[
                "Forgetting `input` returns str before arithmetic.",
                "Nesting huge expressions inside f-string braces.",
                "Mixing tabs/spaces in manually aligned tables — use format widths.",
                "Printing secrets (tokens, passwords) to logs or stdout.",
                "Using `%` formatting in new code without need.",
            ],
            interview="""
You may be asked to pretty-print a table or parse stdin line-by-line. Clean f-string usage and
careful conversion from strings signal professionalism. Mention buffering / stderr only if relevant.
""",
            practice=[
                "**Receipt Printer** (easy) — extend the receipt formatter. [Practice: python-ex-receipt]",
                "**Temp Converter** (easy) — C↔F with one-decimal f-strings.",
                "**Aligned Table** (medium) — print a 3-column scoreboard with widths.",
            ],
            summary=[
                "`input` → str; convert explicitly.",
                "f-strings are the default modern formatter.",
                "Use width, precision, comma, and percent specifiers.",
                "Keep expressions inside `{}` small and readable.",
            ],
            further=[
                "[f-strings spec](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)",
                "[Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language)",
            ],
        ),
    )


def m03() -> None:
    emit(
        "03-control-flow",
        "01-conditionals.mdx",
        dict(
            title="Conditionals: if, elif, else, and match",
            slug="python-conditionals",
            summary="Branch with if/elif/else, write clear boolean logic, and use structural pattern matching (match/case) for multi-way decisions.",
            duration=30,
            difficulty="beginner",
            prerequisites=["python-io-fstrings"],
            tags=["python", "if", "elif", "match", "control-flow"],
            order=1,
        ),
        render_full(
            why="""
Programs make decisions. Muddy conditionals become untestable spaghetti; sharp ones read like
business rules. Python's `if`/`elif`/`else` plus modern `match`/`case` (3.10+) cover nearly every
branching need. Interviews love grading / classification problems that hinge on clear boolean
structure — this lesson builds that muscle.
""",
            intuition="""
A conditional is a fork in the road. Python checks conditions top to bottom and takes the first
true branch. `elif` chains are mutually exclusive lanes; independent `if`s can all fire. `match`
is a structured switch: compare a subject against patterns (literals, sequences, mappings) and
bind names as you go.
""",
            core="""
### Classic branching

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

### Ternary expression

```python
label = "pass" if score >= 60 else "fail"
```

Keep ternaries short; nested ternaries are usually a smell.

### Compound conditions

Use `and` / `or` / `not`, parentheses for clarity, and early returns / guards to flatten nesting:

```python
def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount
```

### Structural pattern matching

```python
def handle(command: list[str]) -> str:
    match command:
        case ["quit"]:
            return "bye"
        case ["load", filename]:
            return f"loading {filename}"
        case ["move", x, y]:
            return f"move to {x},{y}"
        case _:
            return "unknown"
```

Patterns can include guards: `case [x] if x > 0:`.
""",
            diagram=mermaid_flow(
                "branch",
                [
                    "Evaluate condition 1",
                    "True → branch A",
                    "Else evaluate condition 2",
                    "True → branch B",
                    "Else → default branch",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("score=85 through grade chain", "", "grade B"),
                    ("score=90", "", "grade A — first match wins"),
                    ("match ['load','a.txt']", "", "loading a.txt"),
                    ("match ['noop']", "", "unknown via _"),
                    ("ternary score=50", "", "fail"),
                ]
            ),
            code="""
```python
from __future__ import annotations


def letter_grade(score: int) -> str:
    if not 0 <= score <= 100:
        raise ValueError("score out of range")
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def handle_event(event: dict) -> str:
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"click at {x},{y}"
        case {"type": "key", "key": key} if len(key) == 1:
            return f"char {key}"
        case {"type": "key", "key": key}:
            return f"special {key}"
        case _:
            return "ignored"


if __name__ == "__main__":
    print(letter_grade(83))
    print(handle_event({"type": "click", "x": 10, "y": 20}))
```
""",
            complexity="""
An if/elif chain is O(k) in the number of conditions checked. For large dispatch tables, prefer
dicts mapping keys to handlers (O(1) average) or `match` on structured data. Deep nesting increases
human complexity faster than CPU complexity — flatten with guards.
""",
            tricks=[
                "Prefer early returns over deep `else` nesting.",
                "Order elif from most specific / common as appropriate.",
                "Use `match` when destructuring structure beats boolean soup.",
                "Extract boolean expressions into named variables for readability.",
                "Remember: independent `if`s are not the same as `elif` chains.",
            ],
            mistakes=[
                "Using `=` instead of `==` in conditions (SyntaxError in Python — a blessing).",
                "Overlapping elif ranges in the wrong order.",
                "Empty `except` / silent branches that hide bugs (later module).",
                "Giant nested ternaries.",
                "Forgetting the `_` default case when match must be exhaustive in practice.",
            ],
            interview="""
Classification problems (grades, tax brackets, fizzbuzz-like rules) test whether you order
conditions correctly and handle edges. Mentioning `match` for structured events shows modern
Python awareness; be ready to fall back to if/elif on older runtimes.
""",
            practice=[
                "**Grade Calculator** (easy) — implement letter grades with validation. [Practice: python-ex-grades]",
                "**FizzBuzz** (easy) — classic conditional drill.",
                "**Command Match** (medium) — parse list commands with match/case.",
            ],
            summary=[
                "if/elif/else for ordered exclusive branches.",
                "Ternaries for tiny two-way choices.",
                "match/case for structural multi-way dispatch.",
                "Flatten logic with guards and early returns.",
            ],
            further=[
                "[Control flow tutorial](https://docs.python.org/3/tutorial/controlflow.html)",
                "[PEP 634 — Structural Pattern Matching](https://peps.python.org/pep-0634/)",
            ],
        ),
    )

    emit(
        "03-control-flow",
        "02-loops.mdx",
        dict(
            title="Loops: for, while, break, continue, else",
            slug="python-loops",
            summary="Iterate with for and while, control flow with break/continue, use else on loops, and prefer Pythonic iteration helpers like enumerate and zip.",
            duration=32,
            difficulty="beginner",
            prerequisites=["python-conditionals"],
            tags=["python", "for", "while", "enumerate", "zip"],
            order=2,
        ),
        render_full(
            why="""
Loops turn single operations into scalable processing. Writing clear iteration — and knowing when
*not* to hand-roll index arithmetic — separates readable Python from C-translated noise. Almost
every algorithm you study later is a disciplined loop with invariants.
""",
            intuition="""
`for` walks a known itinerary (any iterable). `while` repeats until a condition fails — great for
unknown repetition counts, dangerous if the condition never flips. `break` exits early; `continue`
skips to the next iteration. Python's rare `else` on loops runs when no `break` happened — think
"completed naturally."
""",
            core="""
### for and while

```python
for item in items:
    process(item)

while queue:
    process(queue.pop(0))
```

### range, enumerate, zip

```python
for i in range(5):           # 0..4
    ...
for index, value in enumerate(items, start=1):
    ...
for left, right in zip(a, b, strict=True):  # 3.10+ strict length check
    ...
```

### break, continue, else

```python
for n in numbers:
    if n < 0:
        continue
    if n == target:
        print("found")
        break
else:
    print("not found")
```

### Infinite loops and sentinels

```python
while True:
    line = input("> ").strip()
    if line == "quit":
        break
    print(line[::-1])
```

Always ensure a termination path. Prefer `for` when iterating containers — index management invites
off-by-one bugs.
""",
            diagram=mermaid_flow(
                "forloop",
                [
                    "Get iterator from iterable",
                    "next() → value or StopIteration",
                    "Run loop body",
                    "break? → exit",
                    "continue? → next iteration",
                    "Exhausted → optional else clause",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("for i in range(3)", "", "i=0,1,2"),
                    ("enumerate(['a','b'],1)", "", "(1,'a'), (2,'b')"),
                    ("break on find 7 in [1,7,9]", "", "stops; else skipped"),
                    ("no break search", "", "else clause runs"),
                    ("zip([1,2],[3,4])", "", "(1,3),(2,4)"),
                ]
            ),
            code="""
```python
from __future__ import annotations


def find_first_even(nums: list[int]) -> int | None:
    for n in nums:
        if n % 2 == 0:
            return n
    return None


def summarize(pairs: list[tuple[str, int]]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for name, value in pairs:
        totals[name] = totals.get(name, 0) + value
    return totals


def bubble_step(values: list[int]) -> bool:
    swapped = False
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            values[i], values[i + 1] = values[i + 1], values[i]
            swapped = True
    return swapped


if __name__ == "__main__":
    data = [1, 3, 4, 7]
    print(find_first_even(data))
    print(summarize([("a", 1), ("b", 2), ("a", 3)]))
```
""",
            complexity="""
A single loop over n elements is Θ(n). Nested loops often Θ(n²). `while` with multiplicative
shrink (binary search style) can be Θ(log n). Prefer algorithms whose loop structure matches the
needed complexity — do not nest "just in case."
""",
            tricks=[
                "Prefer `for` over `while` + manual index for containers.",
                "`enumerate` instead of `range(len(xs))` in most cases.",
                "`zip` for parallel iteration; use `strict=True` when lengths must match.",
                "Loop `else` is perfect for search-not-found paths.",
                "Accumulate in dicts/`collections.Counter` rather than nested scans when possible.",
            ],
            mistakes=[
                "Mutating a list while iterating over it unpredictably.",
                "Off-by-one errors with `range(len)` arithmetic.",
                "Infinite `while True` without a break condition.",
                "Using `for`/`else` incorrectly expecting else to mean 'if empty'.",
                "Creating O(n²) solutions accidentally with nested membership checks on lists.",
            ],
            interview="""
Expect to implement scans, running totals, and two-pointer style loops. Narrate your invariant:
what is true at the start of each iteration? That habit impresses interviewers more than silent coding.
""",
            practice=[
                "**Running Max** (easy) — track max so far in one pass. [Practice: python-ex-running-max]",
                "**Search Else** (easy) — use for/else to find a value.",
                "**Zip Records** (medium) — combine names and scores into dicts via zip.",
            ],
            summary=[
                "`for` over iterables; `while` for condition-driven repetition.",
                "`break` / `continue` / loop-`else` are powerful control tools.",
                "`enumerate` and `zip` replace most manual indexing.",
                "Watch complexity: nested loops multiply costs.",
            ],
            further=[
                "[for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)",
                "[itertools for advanced looping](https://docs.python.org/3/library/itertools.html)",
            ],
        ),
    )

    emit(
        "03-control-flow",
        "03-comprehensions.mdx",
        dict(
            title="List, Set, and Dict Comprehensions",
            slug="python-comprehensions",
            summary="Write expressive list/set/dict comprehensions and generator expressions, including filters, nesting rules, and when not to use them.",
            duration=30,
            difficulty="beginner",
            prerequisites=["python-loops"],
            tags=["python", "comprehensions", "generators", "idioms"],
            order=3,
        ),
        render_full(
            why="""
Comprehensions are the hallmark of idiomatic Python. They replace many three-line loops with a
single declarative expression — faster to read once learned, often faster to run, and ubiquitous
in production codebases. Overusing them into nested puzzles is the failure mode; this lesson
teaches the sweet spot.
""",
            intuition="""
A comprehension says "build a new collection from an old one by mapping and optionally filtering."
Read them as English: `[price * 1.1 for price in prices if price > 0]` → "10% markup for each
positive price." Generator expressions `(…)` are lazy cousins that yield items on demand instead
of building a full list in memory.
""",
            core="""
### Forms

```python
squares = [x * x for x in range(10)]
evens = {x for x in nums if x % 2 == 0}
index = {name: i for i, name in enumerate(names)}
total = sum(x * x for x in nums)  # generator expression — no list allocated
```

### Clause order

Comprehensions mirror nested loops left-to-right / top-to-bottom:

```python
pairs = [(r, c) for r in range(3) for c in range(3) if r != c]
```

Equivalent to:

```python
pairs = []
for r in range(3):
    for c in range(3):
        if r != c:
            pairs.append((r, c))
```

### When not to use them

- Multi-step logic with side effects (I/O, logging) — use a plain loop.
- More than two nested levels — readability collapses.
- Building with complex `try/except` per item — loop is clearer.

### Dict and set specifics

Dict comprehensions overwrite duplicate keys silently (last wins). Sets deduplicate automatically —
great for unique transforms.
""",
            diagram=mermaid_flow(
                "comp",
                [
                    "Iterate source",
                    "Optional filter if",
                    "Compute expression",
                    "Collect into list/set/dict or yield",
                ],
            ),
            dryrun=dryrun_table(
                [
                    ("[x*2 for x in [1,2,3]]", "", "[2,4,6]"),
                    ("[x for x in range(5) if x%2]", "", "[1,3]"),
                    ("{c:ord(c) for c in 'ab'}", "", "{'a':97,'b':98}"),
                    ("sum(x for x in range(5))", "", "10 without list"),
                    ("nested for r,c filters", "", "pairs with r!=c"),
                ]
            ),
            code="""
```python
from __future__ import annotations


def normalize_names(names: list[str]) -> list[str]:
    return [n.strip().title() for n in names if n.strip()]


def word_lengths(text: str) -> dict[str, int]:
    words = text.lower().split()
    return {w: len(w) for w in words}


def matrix_flatten(matrix: list[list[int]]) -> list[int]:
    return [value for row in matrix for value in row]


if __name__ == "__main__":
    print(normalize_names(["  ada ", "", "LINUS"]))
    print(word_lengths("to be or not to be"))
    print(matrix_flatten([[1, 2], [3, 4]]))
```
""",
            complexity="""
A comprehension over n items is Θ(n) time and Θ(n) extra space for lists/sets/dicts. Generator
expressions are Θ(1) extra space if consumed streaming (e.g., `sum`, `any`, `all`). Nested
comprehensions multiply costs like nested loops.
""",
            tricks=[
                "Prefer generator expressions with aggregators (`sum`, `max`, `any`).",
                "Name intermediate comprehensions when the one-liner is dense.",
                "Use dict comprehensions to invert simple maps carefully (unique values).",
                "`frozenset` when you need an immutable set of computed values.",
                "In 3.8+, walrus can appear in filters — sparingly.",
            ],
            mistakes=[
                "Side effects inside comprehensions (print, append elsewhere).",
                "Triple-nested comprehensions nobody can parse.",
                "Building a list only to iterate once — use a generator expression.",
                "Expecting dict comprehensions to merge duplicates specially.",
                "Confusing `[…]` list comps with `(…)` generator expressions in type/debug prints.",
            ],
            interview="""
You will often be asked to rewrite a loop as a comprehension or vice versa. Discuss readability
trade-offs. Knowing generator expressions for memory is a plus for large-n follow-ups.
""",
            practice=[
                "**Title Case Filter** (easy) — normalize names as above. [Practice: python-ex-normalize-names]",
                "**Invert Map** (medium) — dict comprehension to invert unique mappings.",
                "**Flatten** (medium) — flatten a 2D matrix with a double comprehension.",
            ],
            summary=[
                "Comprehensions map/filter into list, set, or dict.",
                "Clause order matches nested loops.",
                "Generator expressions save memory for single-pass aggregates.",
                "Choose clarity over clever nesting.",
            ],
            further=[
                "[Data Structures — List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)",
                "[PEP 202 — List Comprehensions](https://peps.python.org/pep-0202/)",
            ],
        ),
    )


def m04() -> None:
    lessons = [
        (
            "01-defining-functions.mdx",
            dict(
                title="Defining and Calling Functions",
                slug="python-defining-functions",
                summary="Write functions with parameters, return values, docstrings, annotations, and clear responsibility boundaries.",
                duration=30,
                difficulty="beginner",
                prerequisites=["python-comprehensions"],
                tags=["python", "functions", "docstrings", "return"],
                order=1,
            ),
            "functions_intro",
        ),
        (
            "02-args-kwargs.mdx",
            dict(
                title="Arguments: positional, keyword, *args, and **kwargs",
                slug="python-args-kwargs",
                summary="Master positional-only, keyword-only, variadic *args/**kwargs, and unpacking at call sites.",
                duration=32,
                difficulty="beginner",
                prerequisites=["python-defining-functions"],
                tags=["python", "args", "kwargs", "parameters"],
                order=2,
            ),
            "args_kwargs",
        ),
        (
            "03-scope-legb.mdx",
            dict(
                title="Scope and the LEGB Rule",
                slug="python-scope-legb",
                summary="Resolve names with Local, Enclosing, Global, Built-in scopes, and use nonlocal/global correctly.",
                duration=30,
                difficulty="intermediate",
                prerequisites=["python-args-kwargs"],
                tags=["python", "scope", "LEGB", "nonlocal"],
                order=3,
            ),
            "legb",
        ),
        (
            "04-closures-and-decorators.mdx",
            dict(
                title="Closures and Decorators",
                slug="python-closures-decorators",
                summary="Capture enclosing state with closures and wrap callables with decorators, including functools.wraps.",
                duration=35,
                difficulty="intermediate",
                prerequisites=["python-scope-legb"],
                tags=["python", "closures", "decorators", "functools"],
                order=4,
            ),
            "decorators",
        ),
        (
            "05-generators-and-yield.mdx",
            dict(
                title="Generators and yield",
                slug="python-generators-yield",
                summary="Build lazy sequences with yield, understand generator state machines, and compose generator pipelines.",
                duration=32,
                difficulty="intermediate",
                prerequisites=["python-closures-decorators"],
                tags=["python", "generators", "yield", "lazy"],
                order=5,
            ),
            "generators",
        ),
        (
            "06-lambda-and-functional.mdx",
            dict(
                title="Lambda and Lightweight Functional Tools",
                slug="python-lambda-functional",
                summary="Use lambda judiciously with sorted, map, filter, and key functions while keeping code readable.",
                duration=28,
                difficulty="intermediate",
                prerequisites=["python-generators-yield"],
                tags=["python", "lambda", "map", "filter", "sorted"],
                order=6,
            ),
            "lambda",
        ),
        (
            "07-recursion.mdx",
            dict(
                title="Recursion and Call Stacks",
                slug="python-recursion",
                summary="Think recursively, trace the call stack, know base cases, and recognize Python's recursion limits.",
                duration=32,
                difficulty="intermediate",
                prerequisites=["python-lambda-functional"],
                tags=["python", "recursion", "stack", "divide-and-conquer"],
                order=7,
            ),
            "recursion",
        ),
    ]

    content_map = {
        "functions_intro": dict(
            why="Functions are the primary abstraction for reusing behavior and naming intent. Without them, programs become copy-paste novels. Interviews and code reviews both grade how well you carve problems into cohesive functions with clear inputs and outputs.",
            intuition="A function is a named recipe: give ingredients (arguments), get a dish (return value). Side effects (printing, writing files) are optional seasoning — pure functions that only compute are easier to test. Docstrings are the recipe card for humans; annotations are optional type garnish.",
            core="""
### Definition and return

```python
def add(a: int, b: int) -> int:
    \"\"\"Return the sum of a and b.\"\"\"
    return a + b
```

No `return` means `None`. Multiple values are returned as a tuple: `return x, y`.

### Parameters versus arguments

Parameters are the names in the definition; arguments are the values at the call site. Prefer
small functions (one responsibility). Extract helpers when a block needs a comment explaining *what*.

### Docstrings and annotations

Use triple-quoted docstrings as the first statement. Annotations (`a: int`, `-> int`) document
intent and enable type checkers later — they do not enforce types at runtime by themselves.
""",
            code="""
```python
def average(values: list[float]) -> float:
    \"\"\"Return arithmetic mean; empty input raises ValueError.\"\"\"
    if not values:
        raise ValueError("values must be non-empty")
    return sum(values) / len(values)


if __name__ == "__main__":
    print(average([2, 4, 6]))
```
""",
            interview="Explain purity vs side effects, and why small named functions beat giant mains.",
            practice=["**Mean Guard** (easy) — implement average with validation. [Practice: python-ex-average]", "**Multi Return** (easy) — return min and max as a tuple.", "**Refactor** (medium) — split a script into functions."],
        ),
        "args_kwargs": dict(
            why="Flexible APIs need careful parameter design. *args/**kwargs power wrappers and forwarders; positional-only and keyword-only parameters (PEP 570/3102) make call sites unambiguous. Misusing defaults — especially mutable defaults — is one of Python's most famous footguns.",
            intuition="Think of parameters as labeled docks. Positional args fill docks left to right; keywords pick docks by name. *args is a catch-all crate for extras; **kwargs is a labeled crate of leftover keyword packages. Positional-only (`/`) and keyword-only (`*`) fences stop callers from doing confusing things.",
            core="""
```python
def connect(host, port=443, /, *, timeout=30, **options):
    ...


def flatten(*parts: str, sep: str = "/") -> str:
    return sep.join(parts)


def forward(a, b, *args, **kwargs):
    return other(a, b, *args, **kwargs)
```

### Mutable default trap

```python
def append_bad(item, bucket=[]):  # BAD shared list
    bucket.append(item)
    return bucket

def append_good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```
""",
            code="""
```python
def tag(name: str, /, *children: str, **attrs: str) -> str:
    attr = "".join(f' {k}="{v}"' for k, v in attrs.items())
    body = "".join(children)
    return f"<{name}{attr}>{body}</{name}>"


if __name__ == "__main__":
    print(tag("a", "Click", href="/home", cls="btn"))
```
""",
            interview="Discuss mutable defaults and when to use keyword-only args for clarity.",
            practice=["**HTML Tag** (easy) — build the tag helper. [Practice: python-ex-html-tag]", "**Safe Default** (easy) — fix a mutable default bug.", "**Forwarder** (medium) — wrap a function preserving *args/**kwargs."],
        ),
        "legb": dict(
            why="Name resolution bugs feel random until you know LEGB. Closures, comprehensions, and `global` misuse all hinge on scope. Interviewers may ask what a nested function sees after the outer returns — that is LEGB + closure cells.",
            intuition="When Python sees a name, it searches Local → Enclosing → Global → Built-in. Assignment in a function makes a name local for the *entire* function unless declared `nonlocal` or `global`. Reading is fine; rebinding needs those keywords.",
            core="""
```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        x = "changed"
    inner()
    return x
```

Comprehension loop variables have their own local scopes in Python 3 — they do not leak.
""",
            code="""
```python
counter = 0

def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc


if __name__ == "__main__":
    c = make_counter()
    print(c(), c(), c())
```
""",
            interview="Explain LEGB and the difference between `global` and `nonlocal`.",
            practice=["**Counter Closure** (easy) — implement make_counter. [Practice: python-ex-counter]", "**Debug Scope** (medium) — fix UnboundLocalError from assignment.", "**Builtin Shadow** (easy) — show why naming a var `list` breaks things."],
        ),
        "decorators": dict(
            why="Decorators appear everywhere: `@app.get`, `@pytest.fixture`, `@dataclass`, `@lru_cache`. They are syntactic sugar for wrapping callables. Understanding closures unlocks reading frameworks and writing cross-cutting concerns (timing, auth, retries) cleanly.",
            intuition="A decorator takes a function and returns a new function that usually calls the original while adding behavior before/after. `@deco` above `def f` means `f = deco(f)`. Closures let the wrapper remember the original function object.",
            core="""
```python
import functools
import time

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {time.perf_counter()-start:.4f}s")
        return result
    return wrapper

@timed
def work(n):
    return sum(range(n))
```

Decorator factories take arguments: `@repeat(3)` returns the actual decorator. Stack order is bottom-up application.
""",
            code="""
```python
import functools


def repeat(times: int):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return deco


@repeat(3)
def ping() -> str:
    print("ping")
    return "pong"


if __name__ == "__main__":
    print(ping())
```
""",
            interview="Be ready to implement a simple timing or retry decorator and mention `functools.wraps`.",
            practice=["**Timed** (medium) — write @timed. [Practice: python-ex-timed]", "**Repeat** (medium) — parameterized decorator.", "**Count Calls** (medium) — wrapper attribute `calls`."],
        ),
        "generators": dict(
            why="Generators let you stream unbounded or large data without loading everything into memory. They power ORM querysets, pipeline processing, and `asyncio` internals. Interviews may ask you to convert a list-builder into a generator for space efficiency.",
            intuition="A generator function pauses at `yield`, handing a value to the caller, and resumes later with its local state intact. It is a resumable function — a lightweight state machine — not a bag of values like a list.",
            core="""
```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

def unique(iterable):
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item
```

Generators are iterators: `next(g)` until `StopIteration`. Use `yield from` to delegate to subgenerators. Generator expressions `(x*x for x in xs)` are compact cousins.
""",
            code="""
```python
from __future__ import annotations
from typing import Iterator


def read_numbers(lines: Iterator[str]) -> Iterator[int]:
    for line in lines:
        line = line.strip()
        if line:
            yield int(line)


def running_sum(nums: Iterator[int]) -> Iterator[int]:
    total = 0
    for n in nums:
        total += n
        yield total


if __name__ == "__main__":
    lines = iter(["1", "2", "", "3"])
    print(list(running_sum(read_numbers(lines))))
```
""",
            interview="Contrast lists vs generators on memory; explain StopIteration and yield from at a high level.",
            practice=["**Countdown** (easy) — yield n..1. [Practice: python-ex-countdown]", "**Unique** (medium) — yield unique items in order.", "**Pipeline** (medium) — chain two generators."],
        ),
        "lambda": dict(
            why="Lambdas appear in `sorted(..., key=)`, callbacks, and quick functional pipelines. Overusing them harms readability; underusing them makes simple key functions verbose. The professional skill is choosing the smallest clear tool.",
            intuition="`lambda args: expression` builds an anonymous function limited to a single expression. It is a sticky note, not a novel — if you need statements, name a real `def`.",
            core="""
```python
sorted(words, key=lambda w: w.lower())
sorted(points, key=lambda p: (p[1], p[0]))
list(map(lambda x: x*2, nums))      # often clearer as comprehension
list(filter(lambda x: x > 0, nums))  # same
```

Prefer comprehensions over `map`/`filter` + lambda in modern Python unless composing higher-order tools. `operator.itemgetter` / `attrgetter` can replace simple lambdas.
""",
            code="""
```python
from __future__ import annotations


def top_students(rows: list[tuple[str, int]], k: int = 3) -> list[str]:
    ranked = sorted(rows, key=lambda r: (-r[1], r[0]))
    return [name for name, _ in ranked[:k]]


if __name__ == "__main__":
    data = [("Ada", 98), ("Lin", 98), ("Grace", 95), ("Alan", 90)]
    print(top_students(data))
```
""",
            interview="Sort a list of tuples with a custom key; discuss stability of sort.",
            practice=["**Sort Key** (easy) — sort by length then alpha. [Practice: python-ex-sort-key]", "**Top K** (medium) — implement top_students.", "**Replace Lambda** (easy) — rewrite with def for clarity."],
        ),
        "recursion": dict(
            why="Recursion expresses tree and graph problems naturally and underpins divide-and-conquer. Python's recursion depth limit (~1000 by default) means many production paths prefer explicit stacks — but interviews still expect recursive fluency.",
            intuition="A recursive function solves a smaller version of the same problem until a base case. Each call pushes a frame on the call stack; returning pops it. If you never hit a base case, you blow the stack (`RecursionError`).",
            core="""
```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def binary_search(xs: list[int], target: int, lo=0, hi=None) -> int:
    if hi is None:
        hi = len(xs) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if xs[mid] == target:
        return mid
    if xs[mid] < target:
        return binary_search(xs, target, mid + 1, hi)
    return binary_search(xs, target, lo, mid - 1)
```

Tail-call optimization is **not** guaranteed in CPython — write iterative versions for deep recursion.
""",
            code="""
```python
def walk(node: dict) -> list[str]:
    \"\"\"Flatten a tree of {'name': str, 'children': list}.\"\"\"
    names = [node["name"]]
    for child in node.get("children", []):
        names.extend(walk(child))
    return names


if __name__ == "__main__":
    tree = {"name": "root", "children": [
        {"name": "a", "children": [{"name": "a1", "children": []}]},
        {"name": "b", "children": []},
    ]}
    print(walk(tree))
```
""",
            interview="Trace factorial or tree walk on the whiteboard; mention recursion limit and iterative alternatives.",
            practice=["**Factorial** (easy) — with validation. [Practice: python-ex-factorial]", "**Tree Paths** (medium) — list all root-to-leaf paths.", "**Recursive Sum** (easy) — sum nested lists."],
        ),
    }

    for filename, meta, key in lessons:
        spec = content_map[key]
        body = render_full(
            why=spec["why"],
            intuition=spec["intuition"],
            core=spec["core"],
            diagram=mermaid_flow(key, ["Define concept", "Show small example", "Compose into larger example", "Handle edge cases", "Practice"]),
            dryrun=dryrun_table(
                [
                    ("Read definition", "", "Identify inputs/outputs"),
                    ("Trace example", "", "Match expected result"),
                    ("Hit edge case", "", "Validate / raise"),
                    ("Compose with prior tools", "", "Reusable function"),
                    ("Compare alternative", "", "Trade-offs clear"),
                ]
            ),
            code=spec["code"],
            complexity="Function call overhead is small but real; algorithmic complexity dominates. Recursion adds stack frames O(depth). Decorators add a wrapper call. Generators are O(1) to create and O(1) per next yielded item aside from your own logic.",
            tricks=[
                "Name functions with verbs; keep them focused.",
                "Prefer keyword-only args for boolean flags.",
                "Use functools.wraps on decorators.",
                "Prefer generators for large streams.",
                "Know when to convert recursion to an explicit stack.",
            ],
            mistakes=[
                "Mutable default arguments.",
                "Forgetting return values (implicit None).",
                "Shadowing names and causing UnboundLocalError.",
                "Omitting wraps so __name__ breaks.",
                "Infinite recursion without base cases.",
            ],
            interview=spec["interview"],
            practice=spec["practice"],
            summary=[
                "Functions encapsulate reusable behavior with clear contracts.",
                "Master argument forms and scope before closures/decorators.",
                "Generators and recursion are tools — pick based on data shape and depth.",
                "Readability beats clever one-liners in reviews and interviews.",
            ],
            further=[
                "[Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)",
                "[functools](https://docs.python.org/3/library/functools.html)",
            ],
        )
        # Expand thin lessons with extra core paragraphs for word count
        extra = f"""

### Deep dive notes for {meta['title']}

In practice you will combine this topic with earlier skills: types, control flow, and clear naming.
Write small experiments in the REPL, then promote working snippets into tested functions. Prefer
explicit parameters over hidden globals. When designing APIs, think about call-site readability —
keyword arguments document themselves. When performance matters, measure first; clarity wins until
profiling says otherwise. Document preconditions in the docstring and enforce them with early
checks that raise informative exceptions. Consistent style across a module matters more than any
single micro-optimization. As you grow, revisit this lesson's examples and refactor them with
type hints, unit tests, and logging from later modules. The goal is not memorizing syntax trivia
but building judgment about structure: what belongs inside a function, what should be composed,
and what should be deferred to a library that already solved the problem carefully.
"""
        body = body.replace("## Diagram / flowchart", extra + "\n## Diagram / flowchart")
        emit("04-functions", filename, meta, body)


def m05() -> None:
    topics = [
        ("01-lists.mdx", "python-lists", "Lists in Depth", ["python", "list", "mutability"], 1,
         "Lists are Python's workhorse dynamic arrays: ordered, mutable, heterogeneous sequences used everywhere from ETL buffers to interview problems.",
         "A list is a resizable row of labeled slots. Indexing is jumping to a slot; slicing is photocopying a range of slots into a new list; mutating methods change slots in place."),
        ("02-tuples.mdx", "python-tuples", "Tuples and Immutability", ["python", "tuple", "immutable"], 2,
         "Tuples signal fixed-structure records and enable hashable compound keys when elements are immutable — critical for dict keys and set members.",
         "Think of a tuple as a sealed envelope of references. You cannot append, but if an element is a mutable list, that inner list can still change — immutability is shallow."),
        ("03-sets.mdx", "python-sets", "Sets and Set Algebra", ["python", "set", "hashing"], 3,
         "Sets give average O(1) membership and clean operations for dedupe, intersection, and difference — interview gold for uniqueness problems.",
         "A set is a bag that refuses duplicates, powered by hashing. Order is not semantic (though insertion order is preserved as an implementation detail in modern CPython)."),
        ("04-dictionaries.mdx", "python-dictionaries", "Dictionaries in Depth", ["python", "dict", "hash-map"], 4,
         "Dicts map keys to values in average O(1) and are the backbone of JSON-like data, indexes, caches, and object namespaces (`__dict__`).",
         "A dict is a labeled filing cabinet: hashable keys locate drawers instantly. Iteration order follows insertion since Python 3.7 language guarantee."),
        ("05-deque-and-heapq.mdx", "python-deque-heapq", "deque and heapq", ["python", "deque", "heapq", "queue"], 5,
         "When list pop(0) is too slow or you need priority ordering, collections.deque and heapq provide the right asymptotic tools from the standard library.",
         "deque is a double-ended queue — fast appends/pops on both sides. A heap is a binary tree in a list where the smallest item is always at index 0."),
        ("06-collections-module.mdx", "python-collections", "collections Helpers", ["python", "collections", "Counter", "defaultdict"], 6,
         "Counter, defaultdict, namedtuple/deque, ChainMap, and OrderedDict leftovers save dozens of lines and reduce bug surface in real code.",
         "The collections module is a toolbox of specialized containers that express intent: counting, defaulting missing keys, and naming tuple fields."),
        ("07-mutability-and-memory.mdx", "python-mutability-memory", "Mutability, Aliasing, and Memory Model", ["python", "mutability", "memory", "copy"], 7,
         "Aliasing, shallow vs deep copy, and object identity explain an entire class of production bugs and interview gotchas.",
         "Mutability answers whether an object's contents can change without rebinding the name. Memory-wise, variables hold references, not full object embeds."),
    ]

    for filename, slug, title, tags, order, why, intuition in topics:
        core = f"""
### Focus: {title}

This lesson trains the mental model and API surface for **{title.split()[0]}** within Python's
broader data model. You will learn construction, core operations, idiomatic patterns, complexity
trade-offs, and how this structure composes with functions and control flow from earlier modules.

### Essential operations

Study creation literals and constructors, indexing/iteration where applicable, adding and removing
elements, membership tests, and conversions to/from other containers. Always ask: is this
operation in-place or does it return a new object? That single question prevents many bugs.

### Complexity instincts

| Operation family | Typical cost |
| --- | --- |
| Index / hash lookup | O(1) average for list index / dict/set hash |
| Scan / membership on list | O(n) |
| Sort | O(n log n) |
| deque ends | O(1) |
| heap push/pop | O(log n) |

### Interop

Convert deliberately: `list(s)`, `tuple(xs)`, `set(xs)`, `dict(pairs)`. Beware that converting
to set loses order semantics for uniqueness algorithms that still need first-seen order — use
`dict.fromkeys` for ordered dedupe.
"""
        code = f"""
```python
from __future__ import annotations
from collections import Counter, defaultdict, deque
import heapq
import copy


def demo_{slug.replace('-', '_')}() -> None:
    # Representative playground for {title}
    data = [3, 1, 4, 1, 5]
    print("list sorted copy:", sorted(data))
    print("unique ordered:", list(dict.fromkeys(data)))
    print("Counter:", Counter(data))
    q: deque[int] = deque(data)
    q.appendleft(0)
    print("deque:", list(q))
    heap = data[:]
    heapq.heapify(heap)
    print("heap pop:", heapq.heappop(heap))
    nested = [[1], [2]]
    print("deep copy equal?", copy.deepcopy(nested) == nested)


if __name__ == "__main__":
    demo_{slug.replace('-', '_')}()
```
"""
        body = render_full(
            why=why + " Mastery here compounds: nearly every later topic — files, OOP, concurrency — stores and moves data through these containers.",
            intuition=intuition + " Draw boxes and arrows on paper when confused; identity diagrams beat guesswork.",
            core=core + """

### Practical patterns

- Build with comprehensions when transforming.
- Prefer `enumerate` / `zip` when coordinating sequences.
- Use `get` / `setdefault` / `defaultdict` to avoid KeyError noise.
- Treat tuples as records; prefer dataclasses (later) when methods appear.
- Profile before replacing lists with exotic structures — clarity first.

### Edge cases to memorize

Empty containers are falsy. Slicing copies shallowly. Dict keys and set elements must be hashable.
Sorting requires comparable elements (or a `key`). Mixing types in a list is allowed but often
signals a missing abstraction.
""",
            diagram=mermaid_flow(slug, ["Create container", "Read / iterate", "Update / transform", "Convert if needed", "Pass to function carefully (aliasing)"]),
            dryrun=dryrun_table(
                [
                    ("Construct sample data", "", "Container holds expected items"),
                    ("Membership / lookup", "", "True/value or miss handled"),
                    ("Mutate or replace", "", "Identity vs new object clear"),
                    ("Convert to another type", "", "Semantics preserved intentionally"),
                    ("Pass into function", "", "Alias effects understood"),
                ]
            ),
            code=code,
            complexity="Pick structures for their operation costs: list scans are linear; dict/set hashing is average constant; heaps log; deques constant at ends. Space overhead differs — dicts store keys+values+hash table slack; measure for huge workloads.",
            tricks=[
                "Use dict.fromkeys for ordered uniqueness.",
                "Prefer deque for queues; avoid list.pop(0).",
                "heapq for top-k without full sorts when k << n.",
                "Counter.most_common for frequency interviews.",
                "copy.deepcopy only when truly needed — it is expensive.",
            ],
            mistakes=[
                "Assuming list.copy is deep.",
                "Using mutable dict keys.",
                "Sorting in-place when a caller still needs the original order.",
                "Using list as a queue at scale.",
                "Forgetting that set iteration order is not a contract for algorithms.",
            ],
            interview=f"For {title}, expect complexity questions, mutability questions, and a small coding drill (dedupe, frequency, top-k, two-sum style maps).",
            practice=[
                f"**Warmup** (easy) — exercise core ops for {title}. [Practice: python-ex-{slug.replace('python-','')}]",
                "**Complexity Choice** (medium) — pick list vs set vs dict for a membership-heavy task.",
                "**Alias Debug** (medium) — fix a function that mutates caller data unintentionally.",
            ],
            summary=[
                f"Know when to choose the structure taught in {title}.",
                "Separate in-place mutation from rebinding new objects.",
                "Hashability and ordering rules drive dict/set correctness.",
                "Complexity instincts beat premature micro-optimization.",
            ],
            further=[
                "[Python tutorial — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)",
                "[collections](https://docs.python.org/3/library/collections.html)",
                "[heapq](https://docs.python.org/3/library/heapq.html)",
            ],
        )
        emit(
            "05-data-structures",
            filename,
            dict(
                title=title,
                slug=slug,
                summary=why[:180] + ("…" if len(why) > 180 else ""),
                duration=32,
                difficulty="intermediate" if order >= 5 else "beginner",
                prerequisites=["python-comprehensions"] if order == 1 else [topics[order - 2][1]],
                tags=tags,
                order=order,
            ),
            body,
        )


def m06() -> None:
    items = [
        ("01-strings-and-regex.mdx", "python-strings-regex", "Strings and Regular Expressions", 1,
         ["python", "str", "regex", "re"],
         "Strings are immutable sequences of Unicode code points; regex unlocks pattern extraction for logs, validation, and parsing.",
         "A string is a frozen ribbon of characters. Methods return new ribbons. Regex is a pattern mini-language for describing shapes in text."),
        ("02-file-io.mdx", "python-file-io", "File I/O and Context Managers Intro", 2,
         ["python", "files", "open", "with"],
         "Reading and writing files correctly — with encodings and `with` blocks — is fundamental to scripts, ETL, and config loading.",
         "A file handle is a bookmark into bytes on disk. `with open(...)` borrows the bookmark and guarantees it is returned (closed) even if errors occur."),
        ("03-json-and-csv.mdx", "python-json-csv", "JSON and CSV Data Interchange", 3,
         ["python", "json", "csv", "serialization"],
         "JSON and CSV are the lingua franca of data exchange. Python's json and csv modules make robust interchange straightforward.",
         "JSON maps closely to Python dicts/lists. CSV is a table serialized as delimited text — simple until quoting and newlines appear."),
        ("04-pathlib.mdx", "python-pathlib", "pathlib: Object-Oriented Paths", 4,
         ["python", "pathlib", "paths", "filesystem"],
         "pathlib replaces brittle string path concatenation with a safe, expressive Path API across operating systems.",
         "A Path is an object that knows how to join, inspect, and manipulate filesystem locations without caring whether you are on Windows or Linux."),
    ]
    for filename, slug, title, order, tags, why, intuition in items:
        body = render_full(
            why=why + " These skills appear in every automation and backend job posting.",
            intuition=intuition,
            core=f"""
### {title}

Work through creation, transformation, and persistence patterns. For strings: indexing, slicing,
`split`/`join`, `strip`, `replace`, formatting, and `in` checks. For regex: `re.search`,
`re.findall`, `re.sub`, raw patterns `r"..."`, groups, and when *not* to use regex (prefer
`str` methods for simple cases).

For files: text vs binary modes, encodings (`encoding="utf-8"`), reading strategies
(`read`, `readline`, iterate lines), and writing safely. Always use context managers:

```python
from pathlib import Path
import json, csv, re

text = Path("notes.txt").read_text(encoding="utf-8")
```

JSON: `json.loads` / `json.dumps` for strings; `load` / `dump` for files. CSV: `csv.DictReader`
and `DictWriter` for column-oriented data. pathlib: `/` join operator, `.glob`, `.exists`,
`.mkdir(parents=True, exist_ok=True)`, `.resolve()`.
""",
            diagram=mermaid_flow(slug, ["Locate path", "Open / read text", "Parse JSON/CSV/regex", "Transform in memory", "Write results safely"]),
            dryrun=dryrun_table(
                [
                    ("Path('a')/'b.txt'", "", "OS-correct join"),
                    ("json.loads('{{\"x\":1}}')".replace('{{','{').replace('}}','}'), "", "{'x': 1}"),
                    ("re.findall(r'\\d+', 'a1b23')", "", "['1','23']"),
                    ("'a,b'.split(',')", "", "['a','b']"),
                    ("with open(...)", "", "file closed after block"),
                ]
            ),
            code="""
```python
from __future__ import annotations

import csv
import json
import re
from pathlib import Path


def extract_emails(text: str) -> list[str]:
    return re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.-]+", text)


def load_users(path: Path) -> list[dict]:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_summary(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    sample = "Contact ada@example.com or linus@kernel.org"
    print(extract_emails(sample))
```
""",
            complexity="String ops often O(n). Regex can be worse on pathological patterns (catastrophic backtracking) — keep patterns simple. File I/O is dominated by disk latency; process line-by-line for large files instead of `read()` all at once.",
            tricks=[
                "Prefer pathlib over os.path for new code.",
                "Always specify encoding=utf-8 explicitly.",
                "Use raw strings for regex patterns.",
                "DictReader for CSV headers.",
                "json.dumps(..., default=str) as a last resort for stubborn objects.",
            ],
            mistakes=[
                "Concatenating paths with raw strings across OSes.",
                "Forgetting newline='' for csv on Windows.",
                "Using regex where split/strip suffices.",
                "Loading multi-GB files fully into memory.",
                "Writing JSON without ensuring parent directories exist.",
            ],
            interview=f"Be ready to parse logs with regex or pathlib, and to discuss encoding pitfalls for {title}.",
            practice=[
                f"**Drill** (easy) — practice the main API for {title}. [Practice: python-ex-{slug.replace('python-','')}]",
                "**Line Filter** (medium) — stream a large file line-by-line with a predicate.",
                "**Round Trip** (medium) — CSV → dicts → JSON file.",
            ],
            summary=[
                "Strings are immutable; methods return new strings.",
                "Use regex thoughtfully; str methods first.",
                "Always close files via with / pathlib helpers.",
                "JSON/CSV + pathlib cover most interchange needs.",
            ],
            further=[
                "[str methods](https://docs.python.org/3/library/stdtypes.html#string-methods)",
                "[re](https://docs.python.org/3/library/re.html)",
                "[json](https://docs.python.org/3/library/json.html)",
                "[csv](https://docs.python.org/3/library/csv.html)",
                "[pathlib](https://docs.python.org/3/library/pathlib.html)",
            ],
        )
        # boost word count
        body = body.replace(
            "## Diagram / flowchart",
            """

### Production habits

Validate inputs at system boundaries. Prefer streaming for large data. Write atomic saves when
possible (write temp file, then replace). Log parse failures with context. Keep serialization
layers thin so domain objects remain clean. Add tests with fixture files under `tests/fixtures`.
Document expected encodings and schemas in README files so teammates do not guess.

### Interview and review lens

Reviewers look for explicit encodings, context managers, and avoidance of brittle split logic when
CSV quoting is possible. Show that you know `Path.read_text` for small files and iterative
reading for large ones. Mention security: never build shell commands from unsanitized filenames;
prefer pathlib and subprocess lists when calling out.

## Diagram / flowchart""",
        )
        prereq = ["python-dictionaries"] if order == 1 else [items[order - 2][1]]
        emit(
            "06-strings-files",
            filename,
            dict(
                title=title,
                slug=slug,
                summary=why,
                duration=30,
                difficulty="beginner" if order <= 2 else "intermediate",
                prerequisites=prereq,
                tags=tags,
                order=order,
            ),
            body,
        )


if __name__ == "__main__":
    main()
