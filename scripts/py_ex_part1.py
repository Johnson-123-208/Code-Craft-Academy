"""Practice problems for modules 01-03."""
from __future__ import annotations

from py_ex_build import add

add(
    "python-ex-env-inspector",
    "Env Inspector",
    "easy",
    ["python", "venv"],
    "Implement `solve(version, prefix, base_prefix)`. `version` is a list of three integers, the same shape as `sys.version_info[:3]`. Return a dict with key `version` (a copy of that list) and key `venv`. `venv` is 1 when `prefix` and `base_prefix` differ, and 0 when they are the same string. A virtual environment is active exactly when those two prefix strings differ.",
    ["prefix and base_prefix are strings", "Do not treat a version mismatch as a venv"],
    [
        "Copy the version list so the caller can mutate it later without changing your result.",
        "Compare prefix and base_prefix with equality. Do not look at the version triple for the venv flag.",
        "Return the integers 0 and 1. The judge compares JSON numbers, not booleans.",
    ],
    "sys.prefix points at the environment prefix and sys.base_prefix points at the installation that created it. They differ inside a venv and match when you are on the base interpreter. The version is reported beside that fact so a diagnostic can show both.",
    "O(1)",
    "O(1)",
    """
def solve(version, prefix, base_prefix):
    return {"version": list(version), "venv": 0 if prefix == base_prefix else 1}
""",
    [
        {"version": [3, 12, 1], "prefix": "/app/.venv", "base_prefix": "/usr"},
        {"version": [3, 11, 0], "prefix": "/usr", "base_prefix": "/usr"},
        {"version": [3, 12, 0], "prefix": "D:/proj/.venv", "base_prefix": "C:/Python312"},
        {"version": [3, 13, 2], "prefix": "/opt/py", "base_prefix": "/opt/py"},
    ],
)

add(
    "python-ex-which-python",
    "Which Python",
    "easy",
    ["python", "toolchain"],
    "Implement `solve(paths, major, minor)`. `paths` is a list of executable paths. Return the first path whose filename contains `{major}.{minor}` (for example `python3.12`) or `python{major}{minor}` / `Python{major}{minor}` (for example `python312`). If none match, return an empty string. Match the filename only, not a parent directory.",
    ["major and minor are integers", "Return the original path string"],
    [
        "Take the last path segment after either slash style before you search.",
        "Build the dotted tag and the compact tags from major and minor.",
        "Return the first hit. Later matches do not matter.",
    ],
    "A launcher list often contains several interpreters. The filename is the contract you can check without executing the binary. Searching the whole path would treat a directory named python3.11 as a match for a 3.12 binary sitting inside it.",
    "O(n)",
    "O(1)",
    """
def solve(paths, major, minor):
    tags = (f"{major}.{minor}", f"python{major}{minor}", f"Python{major}{minor}")
    for path in paths:
        name = path.replace("\\\\", "/").split("/")[-1]
        if any(tag in name for tag in tags):
            return path
    return ""
""",
    [
        {"paths": ["C:/Python311/python.exe", "/usr/bin/python3.12"], "major": 3, "minor": 12},
        {"paths": ["C:/Python312/python.exe"], "major": 3, "minor": 11},
        {"paths": ["/opt/python310/bin/python3.10", "/opt/python312/bin/python3.12"], "major": 3, "minor": 10},
        {"paths": ["D:/tools/python313.exe"], "major": 3, "minor": 13},
    ],
)

add(
    "python-ex-parse-requirements",
    "Requirements Parse",
    "easy",
    ["python", "packaging"],
    "Implement `solve(lines)`. Each line is a string. Ignore blank lines and lines whose stripped text starts with `#`. Every remaining line has the form `name==version`. Return a list of `[name, version]` pairs in order, with surrounding whitespace removed from both sides.",
    ["The separator is exactly ==", "Comments may have leading spaces"],
    [
        "Strip the line before you decide it is blank or a comment.",
        "Split on == once. A version will not contain that separator in these tests.",
        "Keep the original order. Do not sort.",
    ],
    "A requirements file is a line protocol. Comments and blanks are not packages. Splitting a pinned line on == is enough for the direct-dependency pins this course uses. Ranges and extras are out of scope.",
    "O(n)",
    "O(n)",
    """
def solve(lines):
    out = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        name, version = text.split("==", 1)
        out.append([name.strip(), version.strip()])
    return out
""",
    [
        {"lines": ["fastapi==0.115.0", "", "# comment", "uvicorn==0.32.0"]},
        {"lines": ["  requests==2.32.3  ", "#nope"]},
        {"lines": []},
        {"lines": ["# only", "  ", "ruff==0.8.0"]},
    ],
)

add(
    "python-ex-main-guard",
    "Main Guard",
    "medium",
    ["python", "modules"],
    "Implement `solve(name)`. `name` is the value a module sees as `__name__`. Return `script` when `name` is `__main__`. Return `imported` for every other string, including the package's own module name.",
    ["The guard compares against the string __main__", "Any other name means the file was imported"],
    [
        "This is an equality check, not a prefix check. `__main__extra` is imported.",
        "Do not special-case the empty string.",
        "Return those two words exactly.",
    ],
    "Python sets __name__ to __main__ only for the file it was asked to run. Importing that file sets __name__ to the module name, so top-level work hidden behind the guard does not run on import. The function is that comparison and nothing else.",
    "O(1)",
    "O(1)",
    """
def solve(name):
    return "script" if name == "__main__" else "imported"
""",
    [
        {"name": "__main__"},
        {"name": "myapp.api"},
        {"name": "__main__extra"},
        {"name": ""},
    ],
)

add(
    "python-ex-pin-check",
    "Pin Check",
    "medium",
    ["python", "packaging"],
    "Implement `solve(lines, name)`. `lines` are frozen pins of the form `package==version`. Return the version string for `name`. If `name` is absent, return the string `none`. Match the package name exactly. Do not return a JSON null.",
    ["One pin per line", "The missing marker is the string none"],
    [
        "Split each line on ==.",
        "Compare the package side to name before you look at the next line.",
        "Absence is the string none so the judge can see it. Do not skip the return.",
    ],
    "A lock line answers the question a direct dependency asks: what version was installed. Scanning until the name matches is enough because a frozen file lists each distribution once. Returning a visible missing marker keeps the function total.",
    "O(n)",
    "O(1)",
    """
def solve(lines, name):
    for line in lines:
        package, version = line.split("==", 1)
        if package == name:
            return version
    return "none"
""",
    [
        {"lines": ["fastapi==0.115.0", "uvicorn==0.32.0"], "name": "uvicorn"},
        {"lines": ["fastapi==0.115.0"], "name": "ruff"},
        {"lines": ["A==1", "B==2", "A==9"], "name": "A"},
        {"lines": [], "name": "fastapi"},
    ],
)

add(
    "python-ex-co-consts",
    "Constant Fold Peek",
    "easy",
    ["python", "cpython"],
    "Implement `solve(expression)`. Compile `expression` with `compile(..., \"eval\")` and return a list of the integer constants stored on the code object, in the order they appear in `co_consts`. Skip `None` and skip booleans. The list is whatever this interpreter folded. Do not evaluate the expression yourself and invent constants the compiler removed.",
    ["Use compile with mode eval", "bool is a subclass of int. Exclude it."],
    [
        "compile(expression, \"<expr>\", \"eval\") gives you a code object.",
        "Walk co_consts. Keep values whose type is exactly int.",
        "On modern CPython, 1+2 may already be the constant 3. Trust the code object.",
    ],
    "CPython folds literal arithmetic into co_consts at compile time. Reading that tuple is how you see the fold instead of guessing. Filtering with type(value) is int drops the None terminator and any boolean, which would otherwise look like the integers 0 and 1.",
    "O(k)",
    "O(k)",
    """
def solve(expression):
    code = compile(expression, "<expr>", "eval")
    return [value for value in code.co_consts if type(value) is int]
""",
    [
        {"expression": "1+2"},
        {"expression": "3*4+5"},
        {"expression": "x"},
        {"expression": "10"},
    ],
    approach="Read co_consts",
)

add(
    "python-ex-import-once",
    "Import Once",
    "medium",
    ["python", "imports"],
    "Implement `solve(calls)`. `calls` is a list of module names looked up in order. A name is loaded only the first time it appears. Return a dict with `loads`, the list of names that actually loaded, and `cache`, a dict mapping each loaded name to the string `mod:` plus that name. Later lookups must not append another load.",
    ["Order of first appearance matters", "cache keys are the module names"],
    [
        "Keep a dict from name to the built module string.",
        "Append to loads only when the name is missing from that dict.",
        "The module string is the prefix mod: plus the name. Do not number the loads.",
    ],
    "sys.modules is a cache keyed by module name. The first import calls the loader and stores the module. A second import returns the stored object and does not run the module body again. This function is that cache, with a visible list of the loads that really happened.",
    "O(n)",
    "O(u)",
    """
def solve(calls):
    cache = {}
    loads = []
    for name in calls:
        if name not in cache:
            cache[name] = "mod:" + name
            loads.append(name)
    return {"loads": loads, "cache": cache}
""",
    [
        {"calls": ["a", "b", "a"]},
        {"calls": ["a", "a", "a"]},
        {"calls": []},
        {"calls": ["json", "json", "pathlib", "json"]},
    ],
)

add(
    "python-ex-recursion-budget",
    "Recursion Budget",
    "easy",
    ["python", "recursion"],
    "Implement `solve(n, limit)`. A countdown wants to make `n` recursive calls. The interpreter will allow at most `limit` of them. Return how many calls actually run: the smaller of `n` and `limit` when both are positive, otherwise 0.",
    ["n and limit are integers", "A non-positive budget or countdown runs nothing"],
    [
        "If either input is less than 1, return 0.",
        "Otherwise return the minimum of the two numbers.",
        "Do not recurse in your solution. The budget is a closed form.",
    ],
    "A recursive countdown of n needs n frames before it hits the base case. The useful question before you raise the recursion limit is how many of those frames the current budget still allows. min(n, limit) is that number when both are positive.",
    "O(1)",
    "O(1)",
    """
def solve(n, limit):
    if n < 1 or limit < 1:
        return 0
    return n if n < limit else limit
""",
    [
        {"n": 5, "limit": 3},
        {"n": 2, "limit": 10},
        {"n": 0, "limit": 4},
        {"n": 8, "limit": 0},
    ],
)

add(
    "python-ex-traceback-order",
    "Frame Labels",
    "medium",
    ["python", "tracebacks"],
    "Implement `solve(names)`. `names` is the call stack from the oldest frame to the frame that raised, so the last name is where the exception started. A traceback prints the failing frame last in the usual text view only after it has walked from the top. Return the names in the order a reader sees if the list is printed bottom-of-traceback first: the raiser first, then its caller, ending with the oldest frame.",
    ["Reverse the list", "Do not drop the oldest frame"],
    [
        "The last input name is the function that raised.",
        "Return a new list. Reversing a copy is enough.",
        "An empty stack returns an empty list.",
    ],
    "Python tracebacks are stored on the exception as a linked list from the oldest frame toward the raise. Printing walks that chain, so the first line of code you read in the text is the outermost frame and the last line is the raise. This function returns the opposite order: the raise first, which is the order you get by reversing the oldest-to-newest list.",
    "O(n)",
    "O(n)",
    """
def solve(names):
    return list(reversed(names))
""",
    [
        {"names": ["main", "place", "charge"]},
        {"names": ["only"]},
        {"names": []},
        {"names": ["a", "b", "c", "d"]},
    ],
)

add(
    "python-ex-lookup-cost",
    "Hot Local",
    "medium",
    ["python", "cpython"],
    "Implement `solve(n, binds_local)`. A loop body reads one name `n` times. `binds_local` is 1 when that name is a local variable and 0 when it is a global. Return a dict with keys `global` and `local`. The side that applies gets `n` and the other side gets 0. A local is one slot load. A global is one dictionary load. They do not both happen for the same read.",
    ["n is a non-negative integer", "binds_local is 0 or 1"],
    [
        "If binds_local is 1, local is n and global is 0.",
        "If binds_local is 0, swap those counts.",
        "Do not add extra lookups for the loop counter. Count only the named read.",
    ],
    "CPython loads a local by index into the frame's fast locals and loads a global by a dictionary lookup on the module. In a tight loop the same read is one or the other for every iteration. The model charges n to exactly one of the two counters.",
    "O(1)",
    "O(1)",
    """
def solve(n, binds_local):
    if binds_local:
        return {"global": 0, "local": n}
    return {"global": n, "local": 0}
""",
    [
        {"n": 1000, "binds_local": 1},
        {"n": 1000, "binds_local": 0},
        {"n": 0, "binds_local": 1},
        {"n": 3, "binds_local": 0},
    ],
)

add(
    "python-ex-argv-sum",
    "Argv Sum",
    "easy",
    ["python", "cli"],
    "Implement `solve(values)`. `values` is a list of integers that already came off the command line. If any value is negative, return `{\"status\": 1, \"total\": 0}` and do not add the others. Otherwise return `{\"status\": 0, \"total\": sum}`. An empty list is a successful total of 0.",
    ["Negatives are a usage error, status 1", "Do not skip negatives and sum the rest"],
    [
        "Scan for a negative before you trust the sum, or sum and reject if you saw one.",
        "status 0 means the total is the real sum.",
        "An empty list has nothing illegal in it.",
    ],
    "A CLI should refuse a partial answer when an argument is illegal. Summing the non-negative prefix hides the bad argument. The status is the exit-code idea: 0 is success, 1 is a bad argument, and the total is only meaningful on success.",
    "O(n)",
    "O(1)",
    """
def solve(values):
    if any(value < 0 for value in values):
        return {"status": 1, "total": 0}
    return {"status": 0, "total": sum(values)}
""",
    [
        {"values": [1, 2, 3]},
        {"values": [1, -1, 4]},
        {"values": []},
        {"values": [0, 0]},
    ],
)

add(
    "python-ex-exit-code",
    "Exit Class",
    "easy",
    ["python", "cli"],
    "Implement `solve(outcome)`. Map `ok` to 0, `fail` to 1, and `usage` to 2. Any other word maps to 1. These are process exit codes: success, a handled failure, and a bad invocation.",
    ["Return an integer", "Unknown outcomes are failures"],
    [
        "Use a dict from the three known words to their codes.",
        "Default the lookup to 1.",
        "Do not return the word itself.",
    ],
    "Exit codes are a tiny protocol between your program and the shell. 0 is success. 2 is reserved here for usage mistakes so a wrapper can tell a bad flag from a failed charge. Everything else is a generic failure.",
    "O(1)",
    "O(1)",
    """
def solve(outcome):
    return {"ok": 0, "fail": 1, "usage": 2}.get(outcome, 1)
""",
    [
        {"outcome": "ok"},
        {"outcome": "usage"},
        {"outcome": "fail"},
        {"outcome": "timeout"},
    ],
)

add(
    "python-ex-env-bool",
    "Env Bool",
    "medium",
    ["python", "config"],
    "Implement `solve(text)`. Interpret an environment-style string. After strip and casefold, `1`, `true`, `yes`, and `on` return 1. `0`, `false`, `no`, `off`, and the empty string return 0. Any other text returns the string `error`. The word `false` must not count as true just because the string is non-empty.",
    ["Case does not matter", "Surrounding spaces do not matter"],
    [
        "Strip and casefold before the membership tests.",
        "Check the true set and the false set separately.",
        "A non-empty unrecognized word is error, not 1.",
    ],
    "bool(\"false\") is true in Python because the string is non-empty. Environment flags are a different language. The recognized words are a closed set, and everything else is a configuration error rather than a silent true.",
    "O(k)",
    "O(1)",
    """
def solve(text):
    key = text.strip().casefold()
    if key in ("1", "true", "yes", "on"):
        return 1
    if key in ("0", "false", "no", "off", ""):
        return 0
    return "error"
""",
    [
        {"text": "false"},
        {"text": " YES "},
        {"text": "maybe"},
        {"text": ""},
    ],
)

add(
    "python-ex-stream-sum",
    "Stream Sum",
    "easy",
    ["python", "files"],
    "Implement `solve(lines)`. Each item is one line of text. Skip lines that are empty after stripping. Interpret every other line as a base-10 integer and return the sum. The lines are already in memory. Do not require a file.",
    ["Blanks and whitespace-only lines are skipped", "Every other line is a valid integer"],
    [
        "Strip each line. An empty result is a skip, not a zero you parsed.",
        "int() parses the remaining text.",
        "A running total does not need a second list.",
    ],
    "A stream of integers often has blank lines from the way a human wrapped the file. Skipping blanks and adding the rest is a single pass. Building a list of the numbers first would work and would hold the data twice.",
    "O(n)",
    "O(1)",
    """
def solve(lines):
    total = 0
    for line in lines:
        text = line.strip()
        if text:
            total += int(text)
    return total
""",
    [
        {"lines": ["1", "", "2", "  3"]},
        {"lines": ["10", "  "]},
        {"lines": []},
        {"lines": ["-2", "5"]},
    ],
)

add(
    "python-ex-shout-label",
    "Shout Label",
    "easy",
    ["python", "cli"],
    "Implement `solve(label, times, shout)`. `shout` is 1 or 0. If it is 1, uppercase `label`. Repeat that text `times` times and return the list of lines. `times` may be 0, which returns an empty list. Do not print.",
    ["shout is 0 or 1", "times is a non-negative integer"],
    [
        "Choose the text once, then repeat it.",
        "str.upper is the shout. Do not change label when shout is 0.",
        "Return a list of length times.",
    ],
    "A tiny CLI decides the text, then decides how many times to emit it. Doing the uppercase inside the loop is the same result and extra work. Returning the lines lets a test assert them without capturing stdout.",
    "O(times)",
    "O(times)",
    """
def solve(label, times, shout):
    text = label.upper() if shout else label
    return [text for _ in range(times)]
""",
    [
        {"label": "ready", "times": 2, "shout": 1},
        {"label": "ready", "times": 1, "shout": 0},
        {"label": "Go", "times": 0, "shout": 1},
        {"label": "ok", "times": 3, "shout": 0},
    ],
)

add(
    "python-ex-alias-trace",
    "Alias Trace",
    "easy",
    ["python", "mutability"],
    "Implement `solve(ops)`. Two names, `a` and `b`, refer to the same list. `ops` is a list of `[\"append\", who, value]` steps. Apply each append to that shared list. Return `{\"a\": [...], \"b\": [...]}` with the final contents. Because the names alias one list, both results are equal and contain every append, no matter which name was used.",
    ["who is the string a or b", "value is an integer"],
    [
        "Start from one list and point both names at it.",
        "Append on the list the name refers to. Do not copy between steps.",
        "When you build the result dict, copy the list twice so each side is a snapshot of the same contents.",
    ],
    "Assignment never copies a list. After b = a, an append through either name is visible through the other. The trace makes that concrete: the final contents depend on the shared object, not on which variable the source code mentioned.",
    "O(n)",
    "O(n)",
    """
def solve(ops):
    shared = []
    names = {"a": shared, "b": shared}
    for _op, who, value in ops:
        names[who].append(value)
    return {"a": list(shared), "b": list(shared)}
""",
    [
        {"ops": [["append", "a", 1], ["append", "b", 2]]},
        {"ops": [["append", "b", 5]]},
        {"ops": []},
        {"ops": [["append", "a", 1], ["append", "a", 1], ["append", "b", 3]]},
    ],
)

add(
    "python-ex-clamp",
    "Clamp",
    "easy",
    ["python", "comparisons"],
    "Implement `solve(value, low, high)`. If `low` is greater than `high`, return the string `value-error`. Otherwise return `value` limited to the inclusive range: `low` when `value` is below it, `high` when `value` is above it, and `value` when it is inside. Use comparisons. Do not call min or max if you want the comparison practice, though a correct min/max after the bounds check also passes.",
    ["All three inputs are integers", "The range is inclusive"],
    [
        "Reject inverted bounds before you clamp.",
        "One comparison against low and one against high cover the three regions.",
        "Return the number itself when it is already inside. Do not return a string on success.",
    ],
    "Clamp is the boundary pattern behind scores, pagination limits, and timeouts. The illegal case is low greater than high, which is a caller bug, not a value you can snap. Inclusive ends mean the endpoints are valid results.",
    "O(1)",
    "O(1)",
    """
def solve(value, low, high):
    if low > high:
        return "value-error"
    if value < low:
        return low
    if value > high:
        return high
    return value
""",
    [
        {"value": 20, "low": 0, "high": 10},
        {"value": -2, "low": 0, "high": 10},
        {"value": 3, "low": 0, "high": 10},
        {"value": 1, "low": 5, "high": 4},
    ],
    companies=["Amazon", "Microsoft", "Backend"],
)

add(
    "python-ex-floor-pair",
    "Floor Pair",
    "medium",
    ["python", "numbers"],
    "Implement `solve(a, b)`. Return `[a // b, a % b]`, Python's floor quotient and remainder. `b` is never 0. For negatives, the remainder has the sign of the divisor and the identity `b * quotient + remainder == a` holds. Do not use int() truncation toward zero.",
    ["b is not zero", "Return a list of two integers"],
    [
        "The // and % operators already implement floor division.",
        "Check a negative dividend. Toward-zero division is the bug.",
        "The remainder's sign follows b, not a.",
    ],
    "Python's floor division rounds toward negative infinity, so -7 // 3 is -3 and the remainder is 2, because 3 * -3 + 2 = -7. Languages that truncate toward zero produce a different pair. Matching Python means using // and % rather than reimplementing C division.",
    "O(1)",
    "O(1)",
    """
def solve(a, b):
    return [a // b, a % b]
""",
    [
        {"a": 7, "b": 3},
        {"a": -7, "b": 3},
        {"a": 7, "b": -3},
        {"a": -7, "b": -3},
    ],
)

add(
    "python-ex-none-default",
    "Or Default",
    "medium",
    ["python", "none"],
    "Implement `solve(value, default)`. `value` and `default` are strings. The token `none` stands for a missing value. Return `default` only when `value` is exactly `none`. Return `value` unchanged when it is `0` or an empty string. Do not use a truthiness test.",
    ["The missing token is the string none", "0 and the empty string are real values"],
    [
        "Compare value to the string none.",
        "Any other string, including 0 and the empty string, is returned as itself.",
        "or would treat those as missing. Do not use it.",
    ],
    "The expression value or default replaces every falsy value, and 0 and the empty string are falsy. A missing configuration field is None, which this problem spells as the token none. Only that token takes the default.",
    "O(1)",
    "O(1)",
    """
def solve(value, default):
    if value == "none":
        return default
    return value
""",
    [
        {"value": "none", "default": "guest"},
        {"value": "0", "default": "guest"},
        {"value": "", "default": "guest"},
        {"value": "ada", "default": "guest"},
    ],
)

add(
    "python-ex-truthy-count",
    "Truthy Count",
    "easy",
    ["python", "truthiness"],
    "Implement `solve(items)`. Count how many items are truthy. Integers use normal truthiness, so 0 is falsy and every other integer is truthy. The empty string is falsy. The string `none` is falsy and stands for None. Every other non-empty string is truthy, including the strings `false` and `0`. Return the count.",
    ["none is a string token for None", "The string 0 is truthy"],
    [
        "Treat the string none like None.",
        "Use a normal truthiness test for ints and for every other string.",
        "Do not special-case the word false. It is a non-empty string.",
    ],
    "Truthiness is a fixed table: None, 0, and the empty string are falsy. A string of the digit 0 is not the integer 0. Counting with that table is the whole problem. The token none is how the judge passes a missing value without a JSON null.",
    "O(n)",
    "O(1)",
    """
def solve(items):
    count = 0
    for item in items:
        if item == "none":
            continue
        if item:
            count += 1
    return count
""",
    [
        {"items": [0, 1, "", "a", "none"]},
        {"items": ["false", "0", 0]},
        {"items": []},
        {"items": ["none", "none"]},
    ],
)

add(
    "python-ex-swap-indexes",
    "Safe Swap",
    "easy",
    ["python", "unpacking"],
    "Implement `solve(items, i, j)`. Return a new list where the values at indexes `i` and `j` are swapped. Do not change the input list. One unpacking assignment is enough. Indexes are in range and may be equal.",
    ["items is a list of integers", "i and j are valid indexes"],
    [
        "Copy the list first.",
        "Unpack the two positions in one assignment.",
        "Swapping an index with itself is a no-op.",
    ],
    "Tuple unpacking swaps two slots without a temporary name. Copying first keeps the caller's list intact, which is the difference between a pure function and an in-place edit the caller did not ask for.",
    "O(n)",
    "O(n)",
    """
def solve(items, i, j):
    out = list(items)
    out[i], out[j] = out[j], out[i]
    return out
""",
    [
        {"items": [1, 2, 3], "i": 0, "j": 2},
        {"items": [4], "i": 0, "j": 0},
        {"items": [1, 2, 3, 4], "i": 1, "j": 2},
        {"items": [9, 8], "i": 1, "j": 0},
    ],
)

add(
    "python-ex-paise-add",
    "Paise Add",
    "easy",
    ["python", "money"],
    "Implement `solve(a_rupee, a_paise, b_rupee, b_paise)`. Convert each rupee-paise pair to paise (100 paise in a rupee) and return the sum as an integer number of paise. Do not use binary floats. Inputs are integers and paise may be 100 or more.",
    ["All four inputs are integers", "Return total paise, not a rupee pair"],
    [
        "Multiply rupees by 100 and add the paise.",
        "Do the same for both amounts, then add.",
        "There is no carry step to write if the unit is already paise.",
    ],
    "Money in this course is an integer of minor units. Adding rupees in float introduces binary dust. Converting both amounts to paise first makes the sum exact and makes a later carry, if you ever need a rupee display, a separate formatting step.",
    "O(1)",
    "O(1)",
    """
def solve(a_rupee, a_paise, b_rupee, b_paise):
    return (a_rupee * 100 + a_paise) + (b_rupee * 100 + b_paise)
""",
    [
        {"a_rupee": 1, "a_paise": 50, "b_rupee": 2, "b_paise": 50},
        {"a_rupee": 0, "a_paise": 99, "b_rupee": 0, "b_paise": 2},
        {"a_rupee": 0, "a_paise": 0, "b_rupee": 0, "b_paise": 0},
        {"a_rupee": 3, "a_paise": 150, "b_rupee": 1, "b_paise": 0},
    ],
)

add(
    "python-ex-decimal-sum",
    "Float Dust",
    "easy",
    ["python", "decimal"],
    "Implement `solve(values)`. `values` is a list of decimal strings such as `0.10`. Sum them with `decimal.Decimal`, quantize the total to two places with round-half-even (the default), and return the total as a string. Do not use binary float.",
    ["Each string is a base-10 decimal", "The result always has two decimal places"],
    [
        "Construct Decimal from each string, not from a float.",
        "Sum from Decimal(0), then quantize to Decimal(0.01).",
        "str() of that Decimal is the return value.",
    ],
    "0.1 plus 0.2 is not 0.3 in binary floating point. Decimal parses the base-10 string you actually meant. Quantizing to cents after the sum matches a money display and avoids a long expansion of a repeating internal value.",
    "O(n)",
    "O(1)",
    """
def solve(values):
    from decimal import Decimal
    total = sum((Decimal(value) for value in values), Decimal("0"))
    return str(total.quantize(Decimal("0.01")))
""",
    [
        {"values": ["0.10", "0.20"]},
        {"values": ["0.1", "0.2"]},
        {"values": ["1.00"]},
        {"values": ["0.05", "0.05", "0.05"]},
    ],
)

add(
    "python-ex-classify-number",
    "Classify Number",
    "medium",
    ["python", "types"],
    "Implement `solve(type_name)`. `type_name` is one of `none`, `bool`, `int`, `float`, or something else. Return that label for the four known names, and return `other` otherwise. A correct checker tests bool before int, because bool is a subclass of int. Your function receives the already-correct type name, and it must not collapse `bool` into `int`.",
    ["Return one of none, bool, int, float, other"],
    [
        "Compare type_name to bool before you compare it to int.",
        "none and float are their own labels.",
        "Every unrecognized word is other.",
    ],
    "isinstance(True, int) is true. A classifier that asks about int first labels every boolean as an int and then never reaches the boolean branch. Ordering the checks bool, then int, then float, then none, is the rule. This function encodes the labels that order produces.",
    "O(1)",
    "O(1)",
    """
def solve(type_name):
    if type_name == "bool":
        return "bool"
    if type_name == "int":
        return "int"
    if type_name == "float":
        return "float"
    if type_name == "none":
        return "none"
    return "other"
""",
    [
        {"type_name": "bool"},
        {"type_name": "int"},
        {"type_name": "none"},
        {"type_name": "str"},
    ],
)

add(
    "python-ex-floor-div",
    "Floor Div",
    "medium",
    ["python", "numbers"],
    "Implement `solve(a, b)`. Return `[quotient, remainder]` for Python floor division of `a` by `b`. `b` is not 0. The identity `b * quotient + remainder == a` must hold, including when `a` or `b` is negative.",
    ["Use floor division, not truncating division", "Return a two-element list"],
    [
        "quotient is a // b and remainder is a % b.",
        "Verify the identity on a negative dividend.",
        "Do not take abs() and restore a sign by hand unless you also match the remainder's sign.",
    ],
    "The pair (a // b, a % b) is defined so the remainder has the divisor's sign and the quotient is rounded toward negative infinity. That is the pair to return. Hand-rolled truncation matches C and fails the negative cases.",
    "O(1)",
    "O(1)",
    """
def solve(a, b):
    return [a // b, a % b]
""",
    [
        {"a": 8, "b": 3},
        {"a": -8, "b": 3},
        {"a": -8, "b": -3},
        {"a": 5, "b": -2},
    ],
)

add(
    "python-ex-optional-count",
    "Optional Count",
    "medium",
    ["python", "none"],
    "Implement `solve(values)`. Each item is either an integer count or the string `none` for a missing observation. Return `{\"sum\": total, \"missing\": count}` where `sum` adds only the integers and `missing` is how many `none` tokens you saw. A missing observation is not a zero. Zero is a real count and adds nothing, and it is not missing.",
    ["none is the only non-integer", "Zero is present"],
    [
        "Branch on the string none versus an int.",
        "Add ints into sum, including zeros.",
        "Count the none tokens separately. Do not add them as zero.",
    ],
    "Folding optional counts with `or 0` cannot tell a missing sample from a measured zero, but the return value here can. The sum is the measured total. The missing count is how much of the list never produced a measurement.",
    "O(n)",
    "O(1)",
    """
def solve(values):
    total = 0
    missing = 0
    for value in values:
        if value == "none":
            missing += 1
        else:
            total += value
    return {"sum": total, "missing": missing}
""",
    [
        {"values": [1, "none", 0, 2]},
        {"values": ["none", "none"]},
        {"values": [0, 0]},
        {"values": []},
    ],
)

add(
    "python-ex-in-range",
    "In Range",
    "easy",
    ["python", "comparisons"],
    "Implement `solve(value, low, high)`. Return 1 when `low <= value <= high`, and 0 otherwise. The range is inclusive. Use one chained comparison.",
    ["All inputs are integers", "Return 0 or 1"],
    [
        "Write low <= value <= high. Python chains it.",
        "Map the condition to 1 and 0.",
        "The endpoints belong inside the range.",
    ],
    "A chained comparison is two comparisons and a conjunction, evaluated without storing a temporary boolean you then forget to combine. Inclusive ends are the usual contract for scores and indexes that name a closed interval.",
    "O(1)",
    "O(1)",
    """
def solve(value, low, high):
    if low <= value <= high:
        return 1
    return 0
""",
    [
        {"value": 5, "low": 1, "high": 5},
        {"value": 0, "low": 1, "high": 5},
        {"value": 1, "low": 1, "high": 1},
        {"value": 6, "low": 1, "high": 5},
    ],
)

add(
    "python-ex-coalesce-none",
    "Coalesce None",
    "easy",
    ["python", "none"],
    "Implement `solve(value, default)`. Both arguments are strings. Return `default` when `value` is the token `none`. Return `value` for every other string, including `0` and the empty string.",
    ["none is the missing token", "Falsy strings are kept"],
    [
        "Test equality with none. Do not test truthiness.",
        "Return value unchanged in the other branch.",
        "default is used only for the missing token.",
    ],
    "Coalescing is a missing-value operation, not a truthiness operation. The token none is the only input that should be replaced. Keeping zero-like strings is the behavior `or` gets wrong.",
    "O(1)",
    "O(1)",
    """
def solve(value, default):
    if value == "none":
        return default
    return value
""",
    [
        {"value": "none", "default": "n/a"},
        {"value": "0", "default": "n/a"},
        {"value": "", "default": "n/a"},
        {"value": "ok", "default": "n/a"},
    ],
)

add(
    "python-ex-first-present",
    "First Present",
    "medium",
    ["python", "none"],
    "Implement `solve(values)`. `values` is a list of strings. Return the first item that is neither the token `none` nor the empty string. The string `0` counts as present. If every item is missing or empty, return the string `none`.",
    ["Scan from the left", "0 is present"],
    [
        "Skip none and the empty string.",
        "Return the first remaining item immediately.",
        "If the loop ends, return none.",
    ],
    "A chain of optional fields should stop at the first real value. Empty string and the missing token are both absent. The string 0 is a real value a truthiness test would drop, so the skip list has to be explicit.",
    "O(n)",
    "O(1)",
    """
def solve(values):
    for value in values:
        if value != "none" and value != "":
            return value
    return "none"
""",
    [
        {"values": ["none", "", "0", "ada"]},
        {"values": ["", "none"]},
        {"values": ["ada", "grace"]},
        {"values": ["none", "grace"]},
    ],
)

add(
    "python-ex-all-valid",
    "All Valid",
    "medium",
    ["python", "truthiness"],
    "Implement `solve(flags)`. `flags` is a list of 0 and 1. Return 1 when every flag is 1. Return 0 when any flag is 0. An empty list returns 1, matching `all([])`, because there is no failing rule. Do not treat empty as a failure.",
    ["flags contains only 0 and 1", "Empty means vacuously valid"],
    [
        "If you find a 0, return 0.",
        "If the loop finishes, return 1.",
        "Do not special-case empty as 0. The loop already returns 1.",
    ],
    "all() of an empty iterable is true. A rules engine that rejects an empty rule list surprises callers who meant \"no extra constraints.\" The scan is the same function: a single 0 fails the batch, and the absence of a 0 passes it.",
    "O(n)",
    "O(1)",
    """
def solve(flags):
    for flag in flags:
        if flag == 0:
            return 0
    return 1
""",
    [
        {"flags": [1, 1, 1]},
        {"flags": [1, 0, 1]},
        {"flags": []},
        {"flags": [0]},
    ],
)

add(
    "python-ex-precedence",
    "Precedence Fix",
    "medium",
    ["python", "operators"],
    "Implement `solve(price, percent, fee)`. `price` and `fee` are integer paise. `percent` is an integer percent. The discount is `price * percent // 100`, subtracted from the price, and then `fee` is added. Return that integer. Multiplication and floor division bind before addition and subtraction, so you do not need parentheses for the arithmetic, but the discount must be computed from the original price, not from `price + fee`.",
    ["Use integer arithmetic", "Fee is added after the discount"],
    [
        "Compute the discount from price alone.",
        "Subtract it from price, then add fee.",
        "Floor division is the integer percent. Do not use float.",
    ],
    "The bug this function refuses is applying the percent to price plus fee, or adding the fee before the discount is taken. Operator precedence already does the multiply before the subtract. The grouping that still needs a human is which quantity the percent applies to.",
    "O(1)",
    "O(1)",
    """
def solve(price, percent, fee):
    discount = price * percent // 100
    return price - discount + fee
""",
    [
        {"price": 1000, "percent": 10, "fee": 50},
        {"price": 199, "percent": 10, "fee": 0},
        {"price": 0, "percent": 50, "fee": 20},
        {"price": 250, "percent": 0, "fee": 15},
    ],
)

add(
    "python-ex-guard-active",
    "Guard Active",
    "easy",
    ["python", "truthiness"],
    "Implement `solve(user)`. `user` is either the string `none` or a dict with an integer `active` field that is 0 or 1. Return 1 only when the user is a dict and `active` is 1. Return 0 when the user is missing or inactive. Do not index a missing user.",
    ["A missing user is the string none", "active is 0 or 1 when the dict is present"],
    [
        "Return 0 immediately when user is the string none.",
        "Then read the active field.",
        "Only an active value of 1 returns 1.",
    ],
    "The expression user and user[\"active\"] is the guard, written without a crash: you never subscript the missing token. An inactive user is present and still not allowed through. Both failures return 0 so the caller has one check.",
    "O(1)",
    "O(1)",
    """
def solve(user):
    if user == "none":
        return 0
    if user.get("active") == 1:
        return 1
    return 0
""",
    [
        {"user": "none"},
        {"user": {"active": 1}},
        {"user": {"active": 0}},
        {"user": {"active": 1, "name": "ada"}},
    ],
)

add(
    "python-ex-grade-band",
    "Grade Band",
    "easy",
    ["python", "conditionals"],
    "Implement `solve(score)`. Return `A` for 90 and above, `B` for 75 through 89, `C` for 60 through 74, and `F` below 60. `score` is an integer from 0 through 100. Test the thresholds from high to low so the first match wins.",
    ["score is an integer from 0 to 100", "Boundaries 90, 75, and 60 are inside the higher band"],
    [
        "Check >= 90, then >= 75, then >= 60.",
        "The last return is F. You do not need a final comparison.",
        "The boundary values belong to the band whose threshold they equal.",
    ],
    "Ordered thresholds are a chain of exclusive bands only if you return on the first hit. Checking a lower band first and then adding a higher band is how a score becomes two letters. High to low, one return, is the whole structure.",
    "O(1)",
    "O(1)",
    """
def solve(score):
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "F"
""",
    [
        {"score": 90},
        {"score": 75},
        {"score": 60},
        {"score": 59},
    ],
)

add(
    "python-ex-fizzbuzz",
    "Fizz Buzz",
    "easy",
    ["python", "conditionals"],
    "Implement `solve(n)`. Return a list of strings for the numbers 1 through `n` inclusive. A multiple of both 3 and 5 is `FizzBuzz`. A multiple of 3 only is `Fizz`. A multiple of 5 only is `Buzz`. Every other number is its decimal representation. Check the combined case before the single divisors.",
    ["1 <= n <= 100 in the tests", "The combined word is FizzBuzz"],
    [
        "Loop from 1 through n inclusive.",
        "Test divisible by 15, or by 3 and by 5, before the single tests.",
        "Convert the plain numbers with str.",
    ],
    "If the 3 test comes first, 15 becomes Fizz and the combined branch is dead. The order of the conditions is the algorithm. 15 is the least common multiple, so one modulo handles the intersection.",
    "O(n)",
    "O(n)",
    """
def solve(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out
""",
    [
        {"n": 5},
        {"n": 15},
        {"n": 1},
        {"n": 3},
    ],
    companies=["Microsoft", "Amazon", "Backend"],
)

add(
    "python-ex-command-dispatch",
    "Command Dispatch",
    "medium",
    ["python", "match"],
    "Implement `solve(cmd)`. `cmd` is a list. `[\"ping\"]` returns `pong`. `[\"echo\", text]` returns `text`. `[\"add\", a, b]` returns the integer `a + b`. Any other first element returns the string `error`. Do not crash on an unknown command.",
    ["echo's text is a string", "add's operands are integers"],
    [
        "Branch on cmd[0].",
        "echo returns the second element unchanged.",
        "The default branch is the string error.",
    ],
    "A command list is a tiny match subject. Unknown commands are a result, not an IndexError and not a fall-through into add. Each arm reads only the fields that arm needs.",
    "O(1)",
    "O(1)",
    """
def solve(cmd):
    name = cmd[0]
    if name == "ping":
        return "pong"
    if name == "echo":
        return cmd[1]
    if name == "add":
        return cmd[1] + cmd[2]
    return "error"
""",
    [
        {"cmd": ["ping"]},
        {"cmd": ["echo", "hi"]},
        {"cmd": ["add", 2, 3]},
        {"cmd": ["drop"]},
    ],
)

add(
    "python-ex-status-step",
    "Status Step",
    "medium",
    ["python", "state"],
    "Implement `solve(current, nxt)`. An order may move `cart` to `placed`, `placed` to `paid` or `cancelled`, and `paid` to `shipped`. Any other jump returns `current` unchanged. `shipped` and `cancelled` have no exits.",
    ["Both arguments are status strings", "Illegal jumps do not raise"],
    [
        "Store the allowed next statuses in a dict of lists.",
        "If nxt is in the list for current, return nxt.",
        "Otherwise return current. A missing status has an empty list.",
    ],
    "A status graph is data. Encoding it as a dict makes an illegal edge obvious and keeps the function from growing a new condition per edge. Returning the old status, rather than raising, matches a handler that ignores a duplicate click.",
    "O(1)",
    "O(1)",
    """
def solve(current, nxt):
    allowed = {
        "cart": ["placed"],
        "placed": ["paid", "cancelled"],
        "paid": ["shipped"],
        "shipped": [],
        "cancelled": [],
    }
    if nxt in allowed.get(current, []):
        return nxt
    return current
""",
    [
        {"current": "cart", "nxt": "placed"},
        {"current": "cart", "nxt": "shipped"},
        {"current": "placed", "nxt": "cancelled"},
        {"current": "shipped", "nxt": "paid"},
    ],
)

add(
    "python-ex-tax-slab",
    "Tax Slab",
    "medium",
    ["python", "conditionals"],
    "Implement `solve(income)`. Apply one slab to the whole income, in integer arithmetic. Income above 20000 is taxed at 20 percent (`income * 20 // 100`). Income above 10000 and up through 20000 is taxed at 10 percent. Income of 10000 or below is taxed 0. Do not add the 10 percent tax and the 20 percent tax together. The first matching slab, checked from the top, is the only one.",
    ["income is a non-negative integer", "Use floor division"],
    [
        "Test the highest threshold first and return immediately.",
        "Then test the middle threshold.",
        "The remainder is zero. Do not accumulate a tax from several branches.",
    ],
    "A slab table that adds every matching branch double-charges the top band. Returning on the first hit, with the highest band tested first, applies exactly one rate to the whole income. This is a flat band, not a progressive marginal calculation.",
    "O(1)",
    "O(1)",
    """
def solve(income):
    if income > 20000:
        return income * 20 // 100
    if income > 10000:
        return income * 10 // 100
    return 0
""",
    [
        {"income": 5000},
        {"income": 10000},
        {"income": 15000},
        {"income": 25000},
    ],
)

add(
    "python-ex-first-index",
    "First Index",
    "easy",
    ["python", "loops"],
    "Implement `solve(items, target)`. Return the smallest index `i` such that `items[i] == target`. If the target is absent, return -1. A later duplicate does not matter.",
    ["items is a list of strings", "Scan from the left"],
    [
        "enumerate gives you the index.",
        "Return as soon as you see the target.",
        "After the loop, return -1.",
    ],
    "Linear search returns the first hit. Continuing after a match would find the last index instead, which is a different function. -1 is the conventional missing index because 0 is a valid hit.",
    "O(n)",
    "O(1)",
    """
def solve(items, target):
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1
""",
    [
        {"items": ["a", "b", "a"], "target": "a"},
        {"items": ["a", "b"], "target": "c"},
        {"items": [], "target": "a"},
        {"items": ["b"], "target": "b"},
    ],
)

add(
    "python-ex-running-max",
    "Running Max",
    "easy",
    ["python", "loops"],
    "Implement `solve(items)`. `items` is a non-empty list of integers. Return a list of the same length where position `i` is the maximum of `items[0]` through `items[i]` inclusive.",
    ["The list is non-empty", "One pass"],
    [
        "Start the best value at the first element.",
        "Walk left to right, raising best when the current item is larger.",
        "Append best on every step, including the first.",
    ],
    "Prefix maxima are one variable and one pass. Re-scanning the prefix at every index is quadratic and produces the same list. The first element is the maximum of a prefix of length 1, so it is always copied into the output.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    best = items[0]
    out = []
    for item in items:
        if item > best:
            best = item
        out.append(best)
    return out
""",
    [
        {"items": [1, 3, 2, 5]},
        {"items": [4, 4, 1]},
        {"items": [7]},
        {"items": [3, 2, 1]},
    ],
)

add(
    "python-ex-drop-evens",
    "Drop Evens",
    "easy",
    ["python", "loops"],
    "Implement `solve(items)`. Return a new list of the odd integers, in the original order. Do not mutate the input. Zero is even.",
    ["items is a list of integers", "Keep relative order"],
    [
        "A number is odd when n % 2 is non-zero. In Python that also keeps negatives that are odd.",
        "Append to a new list. Do not delete from items while you iterate it.",
        "An empty input returns an empty list.",
    ],
    "Deleting from a list while iterating skips the element after a removal. Building a new list of the odds avoids that class of bug and leaves the caller’s list alone. The filter is one condition.",
    "O(n)",
    "O(k)",
    """
def solve(items):
    return [n for n in items if n % 2]
""",
    [
        {"items": [1, 2, 3, 4]},
        {"items": [2, 4, 6]},
        {"items": []},
        {"items": [0, -1, -2, 5]},
    ],
)

add(
    "python-ex-retry-budget",
    "Retry Budget",
    "medium",
    ["python", "loops"],
    "Implement `solve(outcomes, budget)`. `outcomes` is a list of `ok` or `fail` in the order attempts would happen. You may consume at most `budget` outcomes. Stop at the first `ok` and return `{\"attempts\": used, \"result\": \"ok\"}`. If the budget runs out or the list runs out on failures, return `{\"attempts\": used, \"result\": \"fail\"}`. Do not read past the budget.",
    ["budget is a non-negative integer", "attempts counts outcomes you actually consumed"],
    [
        "Increment used before you look at the outcome, and stop when used would exceed budget.",
        "Return immediately on ok.",
        "If you never see ok, the result is fail and attempts is how many you consumed.",
    ],
    "A retry loop has two exits: success, and the budget. Consuming an outcome past the budget is the bug, even if a later ok exists. The attempts field is the number of outcomes read, which is what a metric would increment.",
    "O(budget)",
    "O(1)",
    """
def solve(outcomes, budget):
    used = 0
    for outcome in outcomes:
        if used == budget:
            break
        used += 1
        if outcome == "ok":
            return {"attempts": used, "result": "ok"}
    return {"attempts": used, "result": "fail"}
""",
    [
        {"outcomes": ["fail", "ok", "ok"], "budget": 3},
        {"outcomes": ["fail", "fail"], "budget": 2},
        {"outcomes": ["ok"], "budget": 0},
        {"outcomes": ["fail", "ok"], "budget": 1},
    ],
)

add(
    "python-ex-two-sum-sorted",
    "Two Sum Sorted",
    "medium",
    ["python", "two-pointers"],
    "Implement `solve(nums, target)`. `nums` is sorted ascending and contains distinct integers. Return `[i, j]` with `i < j` and `nums[i] + nums[j] == target`. If no pair exists, return `[-1, -1]`. Move the left index right when the sum is too small and the right index left when the sum is too large.",
    ["nums is sorted ascending", "At most one pair"],
    [
        "Start indexes at the two ends.",
        "Equal sum returns immediately.",
        "A low sum moves the left index because the right value is already the largest available partner.",
    ],
    "On a sorted array the ends are the smallest and largest remaining values. If the sum is low, only a larger left value can help. If it is high, only a smaller right value can help. Each step discards an index, so the scan is linear and does not need a hash map.",
    "O(n)",
    "O(1)",
    """
def solve(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
""",
    [
        {"nums": [1, 2, 4, 7], "target": 6},
        {"nums": [1, 2, 3], "target": 7},
        {"nums": [1, 2], "target": 3},
        {"nums": [-3, -1, 0, 2, 4], "target": 1},
    ],
    companies=["Amazon", "Google", "Microsoft"],
    approach="Two pointers",
)

add(
    "python-ex-run-length",
    "Compress Run",
    "medium",
    ["python", "loops"],
    "Implement `solve(items)`. `items` is a list of strings. Group consecutive equal values. Return a list of `[value, count]` pairs. A new group starts when the value changes. An empty list returns an empty list. Non-consecutive duplicates are separate groups.",
    ["Only consecutive equals merge", "Counts are positive integers"],
    [
        "If the list is empty, return an empty list.",
        "Track the current value and its count.",
        "Flush the open group when the value changes, and flush once more at the end.",
    ],
    "Run-length encoding is one pass with a single open group. Comparing each element to the previous one avoids a nested scan. Values that match later, after a different value, start a new group. That is what consecutive means.",
    "O(n)",
    "O(g)",
    """
def solve(items):
    if not items:
        return []
    out = []
    current = items[0]
    count = 1
    for item in items[1:]:
        if item == current:
            count += 1
        else:
            out.append([current, count])
            current = item
            count = 1
    out.append([current, count])
    return out
""",
    [
        {"items": ["a", "a", "b", "a"]},
        {"items": []},
        {"items": ["x"]},
        {"items": ["a", "b", "b", "b"]},
    ],
)

add(
    "python-ex-even-squares",
    "Even Squares",
    "easy",
    ["python", "comprehensions"],
    "Implement `solve(items)`. Return the sum of squares of the even integers in `items`. Do it in one pass without building a temporary list of the squares. Zero is even. An empty list or a list of odds returns 0.",
    ["items is a list of integers", "Return an integer"],
    [
        "A generator expression or a running total both avoid the temporary list.",
        "n % 2 == 0 selects evens, including zero and negative evens.",
        "Square by multiplying the number by itself.",
    ],
    "The sum does not need the squares to exist as a list. A running total is linear time and constant extra memory. Materializing the squares is also correct and spends memory the caller never sees.",
    "O(n)",
    "O(1)",
    """
def solve(items):
    return sum(n * n for n in items if n % 2 == 0)
""",
    [
        {"items": [1, 2, 3, 4]},
        {"items": [1, 3, 5]},
        {"items": []},
        {"items": [0, -2]},
    ],
)

add(
    "python-ex-flatten-once",
    "Flatten Once",
    "easy",
    ["python", "comprehensions"],
    "Implement `solve(rows)`. `rows` is a list of lists of integers. Return one list with each inner list's items in order. Do not flatten any deeper: the inputs are exactly one level. An empty outer list or empty inner lists contribute nothing.",
    ["Exactly one level", "Keep order"],
    [
        "A double iteration, outer row then item, is the whole algorithm.",
        "Do not recurse.",
        "Empty rows add no items.",
    ],
    "One-level flatten is a nested loop, which a comprehension writes in one expression. Recursion would matter for irregular trees. These rows are rectangular in depth, so the extra machinery can only hide an off-by-one level.",
    "O(n)",
    "O(n)",
    """
def solve(rows):
    return [item for row in rows for item in row]
""",
    [
        {"rows": [[1, 2], [3], []]},
        {"rows": []},
        {"rows": [[], [4]]},
        {"rows": [[1], [2], [3]]},
    ],
)

add(
    "python-ex-word-lengths",
    "Word Lengths",
    "easy",
    ["python", "dicts"],
    "Implement `solve(words)`. Return a dict mapping each word to its length. If a word repeats, the later occurrence overwrites the same key. The length does not change, so the overwrite is about which key remains, and the value is `len(word)`.",
    ["words is a list of strings", "Keys are the words themselves"],
    [
        "Assign length into a dict in one pass.",
        "A repeated key replaces the previous entry. That is ordinary dict behavior.",
        "An empty list returns an empty dict.",
    ],
    "A dict comprehension `{word: len(word) for word in words}` is the assignment loop. Duplicate keys keep one entry. The interesting part is not the length. It is that the mapping is last-write-wins and is keyed by the string, not by the index.",
    "O(n)",
    "O(u)",
    """
def solve(words):
    return {word: len(word) for word in words}
""",
    [
        {"words": ["ada", "a", "ada"]},
        {"words": []},
        {"words": ["", "ab"]},
        {"words": ["py"]},
    ],
)

add(
    "python-ex-unique-tags",
    "Unique Tags",
    "medium",
    ["python", "sets"],
    "Implement `solve(tags)`. Strip each tag and lowercase it. Drop empty results. Return the first-seen unique tags in that normalized form, in the order they first appeared. A later duplicate, after normalization, does not move the first occurrence.",
    ["Case and surrounding spaces do not make a new tag", "Order is first seen"],
    [
        "Normalize before you test membership.",
        "A set gives the membership test. A list keeps the order. You need both.",
        "Skip a tag whose normalized form is empty.",
    ],
    "A set alone loses order. A list alone makes the membership test linear. The usual pattern is a set of seen keys plus a result list you append to only on the first insert. Normalizing first is what makes `Py` and `py` the same tag.",
    "O(n)",
    "O(u)",
    """
def solve(tags):
    seen = set()
    out = []
    for tag in tags:
        key = tag.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out
""",
    [
        {"tags": [" Py ", "py", "Go", ""]},
        {"tags": ["a", "b", "a"]},
        {"tags": ["  ", ""]},
        {"tags": ["SQL", "sql", "Sql"]},
    ],
    companies=["Amazon", "Backend"],
)

add(
    "python-ex-invert-unique",
    "Invert Unique",
    "medium",
    ["python", "dicts"],
    "Implement `solve(pairs)`. `pairs` is a list of `[key, value]` strings. Build a dict from value to key. If two pairs share a value, return the string `error` and do not return a partial dict. Otherwise return the inverted dict.",
    ["Keys and values are strings", "A repeated value is an error even if the keys differ"],
    [
        "Insert value to key one pair at a time.",
        "If the value is already present, return error immediately.",
        "The original key becomes the stored value.",
    ],
    "Inverting a mapping is safe only when values are unique. A silent overwrite drops a key and the caller cannot tell. Checking membership before the insert turns that collision into an explicit error, which is the contract this function tests.",
    "O(n)",
    "O(n)",
    """
def solve(pairs):
    out = {}
    for key, value in pairs:
        if value in out:
            return "error"
        out[value] = key
    return out
""",
    [
        {"pairs": [["a", "1"], ["b", "2"]]},
        {"pairs": [["a", "1"], ["b", "1"]]},
        {"pairs": []},
        {"pairs": [["a", "1"], ["a", "2"]]},
    ],
)

add(
    "python-ex-pairs",
    "Pairs",
    "easy",
    ["python", "loops"],
    "Implement `solve(left, right)`. Return the cartesian product as a list of `[a, b]` pairs. `a` changes in the outer loop, so all pairs for the first left item come before the next left item. Either side empty returns an empty list.",
    ["left and right are lists of strings", "Outer loop is left"],
    [
        "For each a in left, for each b in right, emit [a, b].",
        "Do not emit [b, a] unless the inputs happen to make that equal.",
        "Empty on either side short-circuits to no pairs.",
    ],
    "Nested loops are the product. The outer choice fixes the order tests will check. Swapping the loops is a different sequence, not a sorting detail, because the problem asks for outer-left order.",
    "O(n*m)",
    "O(n*m)",
    """
def solve(left, right):
    return [[a, b] for a in left for b in right]
""",
    [
        {"left": ["a", "b"], "right": ["1", "2"]},
        {"left": [], "right": ["1"]},
        {"left": ["a"], "right": []},
        {"left": ["a"], "right": ["1"]},
    ],
)
