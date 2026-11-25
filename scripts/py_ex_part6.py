"""Practice problems for modules 09 through 17."""
from __future__ import annotations

from py_ex_build import add

add(
    "python-ex-import-cache",
    "Resolve Cached",
    "easy",
    ["python", "imports"],
    "Implement `solve(cache, name)`. `cache` maps a module name to its path. If `name` is present, return `{\"loaded\": 1, \"path\": path}`. Otherwise return `{\"loaded\": 0, \"path\": \"\"}`.",
    ["loaded is 0 or 1", "A miss has an empty path"],
    ["Use name in cache.", "Do not invent a path for a miss.", "Return both fields."],
    "sys.modules is the import cache. A hit must not run the loader again. The path in the cache is the one the first import recorded. A miss is how you know a loader would run.",
    "O(1)", "O(1)",
    """
def solve(cache, name):
    if name in cache:
        return {"loaded": 1, "path": cache[name]}
    return {"loaded": 0, "path": ""}
""",
    [
        {"cache": {"json": "stdlib"}, "name": "json"},
        {"cache": {}, "name": "json"},
        {"cache": {"a": "src/a.py"}, "name": "b"},
        {"cache": {"a": ""}, "name": "a"},
    ],
)

add(
    "python-ex-shadow-name",
    "Shadowed Stdlib",
    "easy",
    ["python", "imports"],
    "Implement `solve(name, path, stdlib_names)`. Return `shadow` when `name` is in `stdlib_names` and `path` starts with `proj/`. Otherwise return `ok`. A local file named like a standard library module is the shadow.",
    ["proj/ is the project prefix", "Only known stdlib names can be shadows"],
    ["Check membership in stdlib_names.", "Then check the path prefix.", "Both must hold."],
    "A project file named json.py is imported instead of the standard library when the project directory is on sys.path first. The name alone is not enough: a project file called app.py is not a stdlib shadow. The path prefix says the file is yours.",
    "O(n)", "O(1)",
    """
def solve(name, path, stdlib_names):
    if name in stdlib_names and path.startswith("proj/"):
        return "shadow"
    return "ok"
""",
    [
        {"name": "json", "path": "proj/json.py", "stdlib_names": ["json", "os"]},
        {"name": "app", "path": "proj/app.py", "stdlib_names": ["json"]},
        {"name": "json", "path": "stdlib/json.py", "stdlib_names": ["json"]},
        {"name": "os", "path": "proj/os.py", "stdlib_names": []},
    ],
)

add(
    "python-ex-cycle-break",
    "Cycle Break",
    "medium",
    ["python", "imports"],
    "Implement `solve(kind)`. `kind` is `delay` or `third`. `delay` means break the cycle by importing inside the function that needs it. `third` means move the shared object into a third module both sides import. Return `move-import` for delay and `new-module` for third. Any other kind returns `error`.",
    ["Two legal fixes", "Unknown kinds are error"],
    ["delay maps to move-import.", "third maps to new-module.", "Do not return the input unchanged."],
    "A cycle between two modules often means each wants a name from the other at import time. Moving one import into the function delays it until both modules have finished loading. Moving the shared type into a third module removes the edge. Those are the two structural fixes.",
    "O(1)", "O(1)",
    """
def solve(kind):
    return {"delay": "move-import", "third": "new-module"}.get(kind, "error")
""",
    [{"kind": "delay"}, {"kind": "third"}, {"kind": "merge"}, {"kind": "delay"}],
)

add(
    "python-ex-from-import-bind",
    "Bind Snapshot",
    "medium",
    ["python", "imports"],
    "Implement `solve(first, second)`. A from-import captured `first`. The module later rebinds the name to `second`. Return `{\"local\": first, \"module\": second}`. The local name does not follow the rebind.",
    ["local stays first", "module becomes second"],
    ["Echo first as local.", "Echo second as module.", "Do not return second for both."],
    "from module import name binds the current object into the local namespace. A later assignment in the module changes the module attribute and not the local name. That is why a patch must target the name in the module that uses it, and why a reloaded function does not update old from-imports.",
    "O(1)", "O(1)",
    """
def solve(first, second):
    return {"local": first, "module": second}
""",
    [
        {"first": "v1", "second": "v2"},
        {"first": "v1", "second": "v1"},
        {"first": "", "second": "v2"},
        {"first": "a", "second": "b"},
    ],
)

add(
    "python-ex-public-all",
    "Public All",
    "easy",
    ["python", "packages"],
    "Implement `solve(names)`. Return the names that should appear in `__all__`: those that do not start with an underscore, in the original order.",
    ["A single leading underscore is private", "Keep order"],
    ["Skip names that start with _.", "Keep the others.", "Do not sort."],
    "__all__ is the public export list. A leading underscore is the convention for a private name. Filtering that way matches what from package import * would keep if __all__ is set to this list.",
    "O(n)", "O(n)",
    """
def solve(names):
    return [name for name in names if not name.startswith("_")]
""",
    [
        {"names": ["send", "_helper", "Client"]},
        {"names": ["_a", "_b"]},
        {"names": []},
        {"names": ["a", "b"]},
    ],
)

add(
    "python-ex-relative-ok",
    "Relative Ok",
    "easy",
    ["python", "packages"],
    "Implement `solve(mode)`. `mode` is `module` when the file is loaded as part of a package, and `script` when it is executed as a file path. Return `ok` for module and `error` for script. Relative imports require package context.",
    ["script mode cannot use relative imports", "module mode can"],
    ["module returns ok.", "script returns error.", "Anything else returns error."],
    "A relative import looks up the current package on the module. Running a file as a script sets __package__ empty, so the relative import fails. Running python -m package.mod loads it as a module and the relative import works.",
    "O(1)", "O(1)",
    """
def solve(mode):
    return "ok" if mode == "module" else "error"
""",
    [{"mode": "module"}, {"mode": "script"}, {"mode": ""}, {"mode": "module"}],
)

add(
    "python-ex-init-cost",
    "Init Cost",
    "medium",
    ["python", "packages"],
    "Implement `solve(graph, start)`. `graph` maps a module name to the list of modules it imports while loading. Return the names loaded, including `start`, in depth-first order, each name once. Cycles must not loop forever.",
    ["Include start", "First-seen DFS order"],
    ["Use an explicit stack or recursion with a seen set.", "Append a name when you first enter it.", "Skip names already seen so a cycle stops."],
    "Importing a submodule executes the package __init__ and then the submodule, and each of those imports run once. A seen set is sys.modules in miniature. Depth-first order matches a loader that finishes a dependency before continuing the current module's next import, if you record the name before walking its edges.",
    "O(n)", "O(n)",
    """
def solve(graph, start):
    seen = []
    visiting = set()

    def walk(name):
        if name in visiting:
            return
        visiting.add(name)
        seen.append(name)
        for nxt in graph.get(name, []):
            walk(nxt)

    walk(start)
    return seen
""",
    [
        {"graph": {"pkg": ["pkg.sub"], "pkg.sub": []}, "start": "pkg.sub"},
        {"graph": {"a": ["b"], "b": ["a"]}, "start": "a"},
        {"graph": {"a": []}, "start": "a"},
        {"graph": {"a": ["b", "c"], "b": [], "c": []}, "start": "a"},
    ],
)

add(
    "python-ex-facade-cycle",
    "Facade Cycle",
    "medium",
    ["python", "packages"],
    "Implement `solve(edges)`. `edges` is a list of `[src, dst]` import edges. Return `cycle` if `pkg` imports `pkg.sub` and `pkg.sub` imports `pkg`. Return `ok` otherwise. Only that pair matters.",
    ["The package init and the submodule are named pkg and pkg.sub", "A one-way edge is ok"],
    ["Look for both directions.", "A missing direction is ok.", "Do not flag unrelated pairs."],
    "A package __init__ that imports a submodule, while the submodule imports the package to reach a facade name, is a cycle. The loader is still inside the package when the submodule asks for it. Moving the facade to a third module, or delaying one import, breaks this specific pair.",
    "O(n)", "O(n)",
    """
def solve(edges):
    have = {(src, dst) for src, dst in edges}
    if ("pkg", "pkg.sub") in have and ("pkg.sub", "pkg") in have:
        return "cycle"
    return "ok"
""",
    [
        {"edges": [["pkg", "pkg.sub"], ["pkg.sub", "pkg"]]},
        {"edges": [["pkg", "pkg.sub"]]},
        {"edges": []},
        {"edges": [["pkg.sub", "pkg"], ["other", "pkg"]]},
    ],
)

add(
    "python-ex-adjacent-increases",
    "Adjacent Increases",
    "easy",
    ["python", "itertools"],
    "Implement `solve(items)`. Return how many adjacent pairs have a strictly greater second value. A list shorter than 2 returns 0.",
    ["Pairs overlap", "Equal neighbors do not count"],
    ["Compare items[i+1] with items[i].", "Count strict increases.", "zip of the list with its tail is the pair view."],
    "pairwise, or zip(items, items[1:]), walks neighbors without a manual index. The count is the number of rises. A non-strict comparison would count plateaus, which this series does not want.",
    "O(n)", "O(1)",
    """
def solve(items):
    return sum(1 for left, right in zip(items, items[1:]) if right > left)
""",
    [
        {"items": [1, 2, 2, 3]},
        {"items": [3, 2, 1]},
        {"items": [1]},
        {"items": []},
    ],
)

add(
    "python-ex-group-length-iter",
    "Group Length",
    "medium",
    ["python", "itertools"],
    "Implement `solve(words)`. Sort the words by length, then group consecutive equal lengths. Return a list of `[length, [words...]]` in increasing length. Words inside a group keep the order they had after the sort, which is their original relative order because the sort is stable and the key is only the length.",
    ["Sort before grouping", "group is consecutive only"],
    ["sorted(words, key=len) first.", "Then groupby on len.", "Materialize each group with list() before the next group."],
    "itertools.groupby only merges adjacent equal keys. Without the sort, equal lengths that are not neighbors stay split. Materializing each group immediately matters because the group iterator is tied to the source and is consumed when the next group starts.",
    "O(n log n)", "O(n)",
    """
def solve(words):
    from itertools import groupby
    ordered = sorted(words, key=len)
    out = []
    for length, group in groupby(ordered, key=len):
        out.append([length, list(group)])
    return out
""",
    [
        {"words": ["bb", "a", "ccc", "d"]},
        {"words": []},
        {"words": ["a"]},
        {"words": ["aa", "b", "cc"]},
    ],
)

add(
    "python-ex-first-combinations",
    "First Combinations",
    "medium",
    ["python", "itertools"],
    "Implement `solve(items, k)`. Return the first `k` unordered pairs of distinct items, in the order combinations() would yield them: earlier items are chosen first, and the second index increases before the first moves. If `k` is larger than the number of pairs, return all pairs. `k` of 0 returns an empty list. Items are strings.",
    ["Pairs are lists of two strings", "Do not repeat a pair in reverse"],
    ["Generate combinations of length 2.", "Take only k of them.", "islice avoids building the rest when k is small. Slicing a full list is acceptable for these sizes."],
    "combinations yields each unordered pair once. Generating every pair and then slicing is fine when the input is small. islice stops early when k is small and the input is large. The order is lexicographic on the positions, not on a sort of the values.",
    "O(k)", "O(k)",
    """
def solve(items, k):
    from itertools import combinations, islice
    if k < 1:
        return []
    return [list(pair) for pair in islice(combinations(items, 2), k)]
""",
    [
        {"items": ["a", "b", "c", "d"], "k": 2},
        {"items": ["a", "b"], "k": 5},
        {"items": ["a"], "k": 3},
        {"items": ["a", "b", "c"], "k": 0},
    ],
)

add(
    "python-ex-chain-flatten",
    "Flatten Chain",
    "easy",
    ["python", "itertools"],
    "Implement `solve(rows)`. Flatten one level of a list of lists of integers and return one list. Empty rows contribute nothing.",
    ["One level", "Keep order"],
    ["chain.from_iterable walks each row.", "list() materializes at the end.", "Do not recurse."],
    "chain.from_iterable is the lazy one-level flatten. Building the result list is the caller's materialization. A nested comprehension does the same work. The chain version does not need the inner lists to be concatenated by hand.",
    "O(n)", "O(n)",
    """
def solve(rows):
    from itertools import chain
    return list(chain.from_iterable(rows))
""",
    [
        {"rows": [[1, 2], [], [3]]},
        {"rows": []},
        {"rows": [[]]},
        {"rows": [[1], [1]]},
    ],
)

add(
    "python-ex-takewhile",
    "Take Until",
    "medium",
    ["python", "itertools"],
    "Implement `solve(items, limit)`. Return the prefix of integers that are strictly less than `limit`, stopping at the first value that is not. Later small values after a large one are not included. This is takewhile, not a filter.",
    ["Stop at the first failure", "Do not resume"],
    ["Walk until an item is >= limit.", "Return the items you kept.", "An empty prefix is an empty list."],
    "filter would drop the large value and keep later small ones. takewhile defines a prefix. The difference shows up as soon as a value breaks the predicate and a later value would have passed.",
    "O(n)", "O(n)",
    """
def solve(items, limit):
    out = []
    for item in items:
        if item >= limit:
            break
        out.append(item)
    return out
""",
    [
        {"items": [1, 2, 5, 3], "limit": 4},
        {"items": [5, 1], "limit": 4},
        {"items": [], "limit": 1},
        {"items": [1, 2], "limit": 10},
    ],
)

add(
    "python-ex-cached-fib",
    "Cached Fib",
    "medium",
    ["python", "functools"],
    "Implement `solve(n)`. Return Fibonacci n with F(0)=0 and F(1)=1, in linear time. Negative n returns `error`.",
    ["0 and 1 are base cases", "No exponential recursion"],
    ["Reject negatives.", "Roll two variables forward.", "Do not call the function twice per step."],
    "lru_cache on the naive recursion also makes Fibonacci linear, with a cache entry per n. A loop uses constant memory. Both avoid the binary tree of calls. The negative check belongs before either approach.",
    "O(n)", "O(1)",
    """
def solve(n):
    if n < 0:
        return "error"
    if n < 2:
        return n
    prev, cur = 0, 1
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur
""",
    [{"n": 0}, {"n": 1}, {"n": 10}, {"n": -3}],
    companies=["Amazon", "Microsoft"],
    approach="Linear loop",
)

add(
    "python-ex-parse-hex",
    "Parse Hex",
    "easy",
    ["python", "functools"],
    "Implement `solve(text)`. Parse `text` as base 16 and return the integer. A bad string returns `error`. An empty string is an error. The prefix 0x is not allowed. Use int(text, 16).",
    ["Base 16 only", "No 0x prefix"],
    ["int(text, 16) inside try.", "Catch ValueError.", "Return the integer on success."],
    "functools.partial(int, base=16) binds the base so the caller passes only the string. The bound base is the point of partial. ValueError is the garbage path, including the empty string.",
    "O(n)", "O(1)",
    """
def solve(text):
    try:
        return int(text, 16)
    except ValueError:
        return "error"
""",
    [{"text": "ff"}, {"text": "0"}, {"text": "0x10"}, {"text": "zz"}],
)

add(
    "python-ex-safe-product",
    "Safe Product",
    "easy",
    ["python", "functools"],
    "Implement `solve(nums)`. Return the product of the integers. An empty list returns 1, the identity for multiplication.",
    ["Empty product is 1", "Zeros count"],
    ["math.prod has start=1.", "A loop starting at 1 matches it.", "Do not return 0 for an empty list."],
    "The product of no factors is 1, just as the sum of no terms is 0. Starting the accumulator at 1 makes the empty list work without a special case. A zero in the list still forces the product to 0.",
    "O(n)", "O(1)",
    """
def solve(nums):
    product = 1
    for num in nums:
        product *= num
    return product
""",
    [{"nums": [2, 3, 4]}, {"nums": []}, {"nums": [0, 5]}, {"nums": [-2, 3]}],
)

add(
    "python-ex-cache-key",
    "Cache Key",
    "medium",
    ["python", "functools"],
    "Implement `solve(kind, pure)`. `kind` is `int`, `str`, or `list`. `pure` is 1 when the function has no side effects. Return `cache` only when pure is 1 and kind is `int` or `str`. Return `skip` for lists, for impure functions, and for any other kind.",
    ["Lists are not hashable keys", "Impure functions must not be cached"],
    ["pure must be 1.", "kind must be int or str.", "Everything else skips."],
    "lru_cache keys arguments by hash. A list is unhashable. A function that writes a counter or reads the clock is impure, so a cached return value is a stale lie. Both gates have to pass.",
    "O(1)", "O(1)",
    """
def solve(kind, pure):
    if pure and kind in ("int", "str"):
        return "cache"
    return "skip"
""",
    [
        {"kind": "int", "pure": 1},
        {"kind": "list", "pure": 1},
        {"kind": "str", "pure": 0},
        {"kind": "dict", "pure": 1},
    ],
)

add(
    "python-ex-itemgetter-sort",
    "Item Getter Sort",
    "easy",
    ["python", "functools"],
    "Implement `solve(rows, index)`. Each row is a list of integers. Return the rows sorted by the value at `index`, ascending. If any row is too short, return `error`. Do not catch IndexError and skip the row.",
    ["All rows must be long enough", "Sort is ascending"],
    ["Check lengths first.", "Then sorted with a key on that index.", "Copy each row into the result."],
    "operator.itemgetter(index) is the key. It raises if a row is short, which is what you want: a missing column is a bad table, not a value to drop. Checking first returns a clean error string instead of a traceback.",
    "O(n log n)", "O(n)",
    """
def solve(rows, index):
    if index < 0 or any(len(row) <= index for row in rows):
        return "error"
    ordered = sorted(rows, key=lambda row: row[index])
    return [list(row) for row in ordered]
""",
    [
        {"rows": [[2, 1], [1, 9], [1, 0]], "index": 0},
        {"rows": [[1]], "index": 1},
        {"rows": [], "index": 0},
        {"rows": [[3, 1], [2, 2]], "index": 1},
    ],
)

add(
    "python-ex-find-name",
    "Find Name",
    "easy",
    ["python", "typing"],
    "Implement `solve(pairs, key)`. `pairs` is a list of `[key, name]`. Return the name for `key`. If it is absent, return the string `none`. Do not raise.",
    ["First match wins", "Missing is the string none"],
    ["Scan the pairs.", "Return the name on the first equal key.", "After the loop, return none."],
    "An optional lookup returns a value or a missing marker. Raising KeyError is the other function, written in the next problem. Callers that can handle absence should not pay for an exception. The string none stands in for None so the judge can see it.",
    "O(n)", "O(1)",
    """
def solve(pairs, key):
    for have, name in pairs:
        if have == key:
            return name
    return "none"
""",
    [
        {"pairs": [["a", "ada"], ["b", "grace"]], "key": "b"},
        {"pairs": [["a", "ada"]], "key": "z"},
        {"pairs": [], "key": "a"},
        {"pairs": [["a", ""], ["a", "ada"]], "key": "a"},
    ],
)

add(
    "python-ex-require-name",
    "Require Name",
    "easy",
    ["python", "typing"],
    "Implement `solve(pairs, key)`. Same pairs as a name lookup. Return the name when the key exists. When it does not, return the string `missing`. This is the required-name path: absence is not a successful empty result.",
    ["A present empty name is returned", "Absence is missing"],
    ["Find the first match.", "Do not treat an empty name as missing.", "Return missing only when the key never appears."],
    "The caller that requires a name has already decided absence is a bug. Returning a distinct missing marker is the sandbox form of raising KeyError. Collapsing absence and an empty name hides a stored blank.",
    "O(n)", "O(1)",
    """
def solve(pairs, key):
    for have, name in pairs:
        if have == key:
            return name
    return "missing"
""",
    [
        {"pairs": [["a", "ada"]], "key": "a"},
        {"pairs": [["a", ""]], "key": "a"},
        {"pairs": [], "key": "a"},
        {"pairs": [["b", "grace"]], "key": "a"},
    ],
)

add(
    "python-ex-first-item",
    "First Item",
    "medium",
    ["python", "typing"],
    "Implement `solve(items)`. Return the first element of a non-empty list. If the list is empty, return the string `error`. Do not index an empty list.",
    ["Empty is error", "The first element keeps its type, int or string"],
    ["Check the length.", "Return items[0] when it exists.", "The error string is the empty case."],
    "A function annotated to return a value, not an optional, must refuse the empty sequence. Indexing it raises IndexError. Checking first makes the failure the string the caller expects in this sandbox. The element itself is returned unchanged.",
    "O(1)", "O(1)",
    """
def solve(items):
    if not items:
        return "error"
    return items[0]
""",
    [{"items": [1, 2]}, {"items": []}, {"items": ["a"]}, {"items": [0]}],
)

add(
    "python-ex-sum-sequence",
    "Read Only",
    "medium",
    ["python", "typing"],
    "Implement `solve(items)`. Return the sum of the integers and also return the input unchanged as `{\"total\": ..., \"items\": ...}`. Do not sort or clear the list you were given. Copy it into the result.",
    ["The input order is preserved in the echo", "An empty list sums to 0"],
    ["Sum the numbers.", "Copy the list into the result.", "Do not reverse it."],
    "A Sequence annotation is a promise not to mutate. Summing does not need to. Echoing a copy of the input lets the test see that the order survived. In-place sort would change that echo and still return the right total, which is the bug.",
    "O(n)", "O(n)",
    """
def solve(items):
    return {"total": sum(items), "items": list(items)}
""",
    [{"items": [1, 2, 3]}, {"items": []}, {"items": [0, -1]}, {"items": [4]}],
)

add(
    "python-ex-label-score",
    "Label Score",
    "easy",
    ["python", "typing"],
    "Implement `solve(score)`. `score` is an integer, or the string `none` for a missing score. Return `missing` when the score is none. Return `pass` when the integer is 60 or higher, and `fail` otherwise. Do not compare the missing token with 60.",
    ["none is not a number", "60 is a pass"],
    ["Handle none first.", "Then compare with 60.", "Do not coerce none to 0."],
    "A score annotated as int or None must be narrowed before a numeric comparison. The token none is that missing value. Treating it as 0 would label a missing exam as a fail, which is a different fact from a score of 0.",
    "O(1)", "O(1)",
    """
def solve(score):
    if score == "none":
        return "missing"
    if score >= 60:
        return "pass"
    return "fail"
""",
    [{"score": "none"}, {"score": 60}, {"score": 59}, {"score": 100}],
)

add(
    "python-ex-average-typed",
    "Average",
    "easy",
    ["python", "typing"],
    "Implement `solve(nums)`. Return the integer average of a non-empty list, using floor division by the length. An empty list returns `error`.",
    ["Floor division", "Empty is error"],
    ["Reject an empty list before dividing.", "Sum and divide by the length.", "Do not use a float."],
    "The average of an empty sample is undefined, not zero. Checking the length is the narrowing step a type checker cannot do for you if the list is merely list[int]. Floor division keeps the result an integer the judge can compare exactly.",
    "O(n)", "O(1)",
    """
def solve(nums):
    if not nums:
        return "error"
    return sum(nums) // len(nums)
""",
    [{"nums": [1, 2, 3]}, {"nums": []}, {"nums": [1]}, {"nums": [1, 2]}],
)

add(
    "python-ex-narrow-none",
    "Narrow",
    "medium",
    ["python", "typing"],
    "Implement `solve(value)`. `value` is a string, or the token `none`. Return `value` when it is a string, including empty. Return the string `missing` when the token is none. Do not call string methods on the missing token.",
    ["Empty string is present", "none becomes missing"],
    ["Compare with the token none first.", "Return the string unchanged otherwise.", "Do not strip."],
    "Narrowing is the if that proves a value is a string before you treat it as one. After the check, the type checker accepts the string methods. This function returns the string or a missing marker and does not need a method call to make the branch real.",
    "O(1)", "O(1)",
    """
def solve(value):
    if value == "none":
        return "missing"
    return value
""",
    [{"value": "ada"}, {"value": "none"}, {"value": ""}, {"value": "none"}],
)

add(
    "python-ex-ignore-policy",
    "Ignore Policy",
    "medium",
    ["python", "mypy"],
    "Implement `solve(escapes)`. Each escape is `fix`, `narrow`, or `ignore`. Return a list of decisions: `fix` stays `fix`, `narrow` stays `narrow`, and `ignore` becomes `reject`. A blanket ignore is not an allowed outcome.",
    ["ignore is rejected", "The other two pass through"],
    ["Map ignore to reject.", "Leave fix and narrow.", "Unknown words become reject too."],
    "A type-ignore comment that nobody owns becomes a permanent hole. The allowed responses to a checker error are to fix the code or to narrow the value so the error goes away. Ignoring is the choice this policy refuses.",
    "O(n)", "O(n)",
    """
def solve(escapes):
    out = []
    for escape in escapes:
        if escape in ("fix", "narrow"):
            out.append(escape)
        else:
            out.append("reject")
    return out
""",
    [
        {"escapes": ["fix", "ignore", "narrow"]},
        {"escapes": ["ignore"]},
        {"escapes": []},
        {"escapes": ["narrow", "nope"]},
    ],
)

add(
    "python-ex-parse-user-model",
    "Parse User",
    "medium",
    ["python", "pydantic"],
    "Implement `solve(name, age)`. `name` must be a non-blank string after strip. `age` must be an int, not a bool, and must be >= 0. The tests pass age as an int, or the string `bool` when the payload used a JSON boolean. Return `{\"name\": stripped, \"age\": age}` or `error`.",
    ["bool ages are error", "Blank names are error"],
    ["Reject the string bool before any numeric use.", "Strip the name and reject empty.", "Reject a negative int."],
    "Pydantic will coerce some values and reject others depending on the model. A bool accepted as an age is the subclass trap. This function is the validation you want even if you write it by hand: non-empty name, real int, non-negative.",
    "O(n)", "O(1)",
    """
def solve(name, age):
    if age == "bool" or type(age) is not int or age < 0:
        return "error"
    if type(name) is not str or not name.strip():
        return "error"
    return {"name": name.strip(), "age": age}
""",
    [
        {"name": " Ada ", "age": 36},
        {"name": "Ada", "age": "bool"},
        {"name": "  ", "age": 1},
        {"name": "Ada", "age": -1},
    ],
)

add(
    "python-ex-forbid-extra",
    "Forbid Extra",
    "easy",
    ["python", "pydantic"],
    "Implement `solve(payload, allowed)`. Return `ok` when every payload key is allowed. Return `extra` when any key is not. Missing allowed keys are fine.",
    ["Extras fail the payload", "Missing optional keys do not"],
    ["Subtract the allowed set from the payload keys.", "A non-empty difference is extra.", "An empty difference is ok."],
    "A model that forbids extra keys turns a typo into a 422 instead of a silently dropped field. The check is set difference. It does not require the payload to contain every allowed key, because those may be optional.",
    "O(n)", "O(n)",
    """
def solve(payload, allowed):
    if set(payload) - set(allowed):
        return "extra"
    return "ok"
""",
    [
        {"payload": {"name": "a"}, "allowed": ["name"]},
        {"payload": {"name": "a", "role": "x"}, "allowed": ["name"]},
        {"payload": {}, "allowed": ["name"]},
        {"payload": {"a": 1, "b": 2}, "allowed": ["a"]},
    ],
)

add(
    "python-ex-response-fields",
    "Split Models",
    "medium",
    ["python", "pydantic"],
    "Implement `solve(fields, secrets)`. `fields` is the list of field names on the write model, in order. `secrets` is the list of names that must not appear on the response. Return the response fields, in the original order, with secrets removed.",
    ["Order follows fields", "Secrets that were not present change nothing"],
    ["Walk fields.", "Skip names in the secret set.", "Do not sort."],
    "A response model is an allow-list. Building it by deleting secret names from the write model is the same filter when you start from the write fields and drop the secrets. A new secret field added only to the write model never appears in this list.",
    "O(n)", "O(n)",
    """
def solve(fields, secrets):
    hidden = set(secrets)
    return [name for name in fields if name not in hidden]
""",
    [
        {"fields": ["id", "password", "name"], "secrets": ["password"]},
        {"fields": ["id"], "secrets": ["password"]},
        {"fields": [], "secrets": ["password"]},
        {"fields": ["a", "b"], "secrets": ["a", "b"]},
    ],
)

add(
    "python-ex-age-range",
    "Range Age",
    "easy",
    ["python", "pydantic"],
    "Implement `solve(age)`. Return `ok` when `age` is an int from 0 through 130 inclusive. Return `error` otherwise. The string `bool` is an error.",
    ["0 and 130 are valid", "131 is not"],
    ["Reject the bool token.", "Then require type int.", "Then check the inclusive range."],
    "A bounded age is a field constraint, not a free integer. The ends are inclusive because 0 and 130 are representable ages in this contract. A JSON boolean must not sneak in as 1.",
    "O(1)", "O(1)",
    """
def solve(age):
    if age == "bool" or type(age) is not int:
        return "error"
    if 0 <= age <= 130:
        return "ok"
    return "error"
""",
    [{"age": 0}, {"age": 130}, {"age": 131}, {"age": "bool"}],
)

add(
    "python-ex-locked-increment",
    "Locked Increment",
    "medium",
    ["python", "threading"],
    "Implement `solve(n)`. Return `n`, the total after incrementing a counter `n` times by 1 from 0. `n` is non-negative. The point of the lock is that the total equals the number of increments. This single-threaded function is that correct total.",
    ["Start at 0", "Each step adds 1"],
    ["A loop of n increments is enough here.", "The locked version has the same result.", "Return n."],
    "Without a lock, two threads can read the same value and each write value+1, losing an increment. With a lock around the read-modify-write, n increments finish at n. This function returns that correct total. The lock does not change the arithmetic. It makes the arithmetic the one that happens.",
    "O(n)", "O(1)",
    """
def solve(n):
    total = 0
    for _ in range(n):
        total += 1
    return total
""",
    [{"n": 0}, {"n": 1}, {"n": 5}, {"n": 100}],
)

add(
    "python-ex-cache-fill",
    "Check Then Act",
    "medium",
    ["python", "threading"],
    "Implement `solve(ops)`. `ops` is a list of keys. A cache get-or-set stores a key the first time and returns `hit` when it is already present. Return the list of `miss` or `hit` in order. Under a lock this is one decision per key. Do not record two misses for the same key.",
    ["First time is miss", "Later times are hit"],
    ["Use a set of seen keys.", "A new key appends miss and is added.", "A known key appends hit."],
    "Check-then-act without a lock lets two threads both see a miss and both store. The lock makes the check and the insert one critical section. The sequence of miss and hit is what a single-threaded locked run produces, which is the race-free result.",
    "O(n)", "O(u)",
    """
def solve(ops):
    seen = set()
    out = []
    for key in ops:
        if key in seen:
            out.append("hit")
        else:
            seen.add(key)
            out.append("miss")
    return out
""",
    [
        {"ops": ["a", "a", "b"]},
        {"ops": []},
        {"ops": ["a"]},
        {"ops": ["b", "a", "b"]},
    ],
)

add(
    "python-ex-pool-bound",
    "Pool Bound",
    "easy",
    ["python", "threading"],
    "Implement `solve(cap, jobs)`. Return the worker count to use: the minimum of `cap` and `jobs`, and 0 if either is 0 or negative.",
    ["Do not start more workers than jobs", "Do not exceed the cap"],
    ["Non-positive inputs return 0.", "Otherwise return the smaller of cap and jobs.", "Both are integers."],
    "A pool larger than the job count wastes threads. A pool larger than the cap stampedes a shared resource. The bound is the minimum of the two, after rejecting non-positive configuration that cannot mean a real pool.",
    "O(1)", "O(1)",
    """
def solve(cap, jobs):
    if cap < 1 or jobs < 1:
        return 0
    return cap if cap < jobs else jobs
""",
    [
        {"cap": 4, "jobs": 10},
        {"cap": 8, "jobs": 3},
        {"cap": 0, "jobs": 5},
        {"cap": 2, "jobs": 2},
    ],
)

add(
    "python-ex-race-window",
    "Race Window",
    "medium",
    ["python", "threading"],
    "Implement `solve(order)`. `order` is a list of `check-a`, `check-b`, `store-a`, `store-b`. The key starts absent. A check sees a miss only if no store of that same letter has happened yet... Simplify: return `twice` if both checks appear before either store. Return `once` otherwise. `twice` means both threads decided to load.",
    ["Both checks before any store is the race", "A store before the second check collapses it"],
    ["Find the indexes of the two checks and the first store.", "If both checks are before the first store, return twice.", "Otherwise return once. If there is no store, both checks still return twice."],
    "The race window is the gap between seeing a miss and storing the value. If both threads check inside that gap, the key is loaded twice. A store that happens before the second check closes the window. The interleaving is the input. You do not need threads to classify it.",
    "O(n)", "O(1)",
    """
def solve(order):
    first_store = None
    checks = []
    for index, event in enumerate(order):
        if event.startswith("check"):
            checks.append(index)
        elif event.startswith("store") and first_store is None:
            first_store = index
    if len(checks) >= 2 and (first_store is None or checks[1] < first_store):
        return "twice"
    return "once"
""",
    [
        {"order": ["check-a", "check-b", "store-a", "store-b"]},
        {"order": ["check-a", "store-a", "check-b"]},
        {"order": ["store-a", "check-a", "check-b"]},
        {"order": ["check-a", "check-b"]},
    ],
)

add(
    "python-ex-score-chunk",
    "Score Chunk",
    "easy",
    ["python", "multiprocessing"],
    "Implement `solve(nums)`. Return the sum of squares. This is a pure function of the chunk, safe to ship to another process.",
    ["Empty chunk is 0", "Negatives square to positives"],
    ["Square each number.", "Add them.", "Do not touch global state."],
    "A process pool can only help if the task is pure and the arguments pickle. Sum of squares reads the chunk and returns an int. It does not close over a socket or a lock. That is the shape of work you ship to a worker.",
    "O(n)", "O(1)",
    """
def solve(nums):
    return sum(n * n for n in nums)
""",
    [{"nums": [1, 2, 3]}, {"nums": []}, {"nums": [-2, 2]}, {"nums": [0]}],
)

add(
    "python-ex-batch-size",
    "Batch Size",
    "medium",
    ["python", "multiprocessing"],
    "Implement `solve(items, size)`. Split `items` into contiguous chunks of length `size`. The last chunk may be shorter. `size` less than 1 returns `error`.",
    ["Chunks keep order", "A short tail is kept"],
    ["Reject a non-positive size.", "Slice items[i:i+size] while i walks by size.", "Do not drop a remainder."],
    "Shipping one tiny task per row can cost more in pickle and scheduling than the work itself. Batching into chunks of a chosen size cuts the number of tasks. The last batch is shorter rather than padded, so the worker sees real items only.",
    "O(n)", "O(n)",
    """
def solve(items, size):
    if size < 1:
        return "error"
    return [list(items[i:i + size]) for i in range(0, len(items), size)]
""",
    [
        {"items": [1, 2, 3, 4, 5], "size": 2},
        {"items": [1], "size": 3},
        {"items": [], "size": 2},
        {"items": [1, 2], "size": 0},
    ],
)

add(
    "python-ex-pickle-gate",
    "Pickle Gate",
    "medium",
    ["python", "multiprocessing"],
    "Implement `solve(kind)`. Return `ok` when `kind` is `int`, `str`, `list`, or `dict`. Return `no` when `kind` is `lambda`, `lock`, or `socket`. Those cannot cross a process boundary by pickling.",
    ["Plain data is ok", "Live resources are no"],
    ["Keep a set of ok kinds.", "Everything else, including the three named resources, is no.", "Do not try to pickle a real lock in the solution."],
    "multiprocessing uses pickle to send arguments to the spawned interpreter. Lambdas, locks, and sockets do not pickle. Integers, strings, lists, and dicts of those do. The gate is the decision before you submit the task, not the traceback after the pool fails.",
    "O(1)", "O(1)",
    """
def solve(kind):
    if kind in ("int", "str", "list", "dict"):
        return "ok"
    return "no"
""",
    [{"kind": "list"}, {"kind": "lambda"}, {"kind": "lock"}, {"kind": "int"}],
)

add(
    "python-ex-score-serial",
    "Serial Baseline",
    "easy",
    ["python", "multiprocessing"],
    "Implement `solve(chunks)`. Each chunk is a list of integers. Return the sum of the per-chunk sums of squares, in order, as one integer. Do not start processes.",
    ["Add the chunk scores", "Empty input is 0"],
    ["Score a chunk as the sum of squares.", "Add those scores.", "Order does not matter for a sum, but compute every chunk."],
    "The serial baseline is what you compare a process pool against. If the chunks are small, the serial sum can win. The number is the same either way when the work is a pure reduction. This function is that number.",
    "O(n)", "O(1)",
    """
def solve(chunks):
    return sum(n * n for chunk in chunks for n in chunk)
""",
    [{"chunks": [[1, 2], [3]]}, {"chunks": []}, {"chunks": [[]]}, {"chunks": [[-1], [1]]}],
)

add(
    "python-ex-gather-names",
    "Gather Names",
    "medium",
    ["python", "asyncio"],
    "Implement `solve(names)`. Return the names in the same order. A gather of fetches preserves the order of the awaitables, not the order they finish. This pure function returns that ordered list.",
    ["Do not sort", "Do not drop blanks"],
    ["Copy the list.", "Leave the order alone.", "An empty list stays empty."],
    "asyncio.gather returns results in the order of the tasks you passed, even if a later task finishes first. Sorting by completion would surprise the caller who zipped results with ids. The sandbox function returns the input order, which is the gather contract.",
    "O(n)", "O(n)",
    """
def solve(names):
    return list(names)
""",
    [{"names": ["a", "c", "b"]}, {"names": []}, {"names": ["a"]}, {"names": ["", "b"]}],
)

add(
    "python-ex-bound-waves",
    "Bound Waves",
    "medium",
    ["python", "asyncio"],
    "Implement `solve(n, k)`. `n` jobs run with at most `k` in flight. Return how many waves that takes, which is the ceiling of n/k. `k` less than 1 or `n` less than 0 returns `error`. Zero jobs returns 0.",
    ["Ceiling division", "A partial last wave counts"],
    ["Reject a bad k or a negative n.", "Zero jobs is 0.", "Otherwise (n + k - 1) // k."],
    "A semaphore of k permits lets k tasks run. The rest wait. The number of sequential waves, if you batched them, is the ceiling of n/k. That is the latency shape: k-wide, and a short tail still costs a wave.",
    "O(1)", "O(1)",
    """
def solve(n, k):
    if k < 1 or n < 0:
        return "error"
    if n == 0:
        return 0
    return (n + k - 1) // k
""",
    [
        {"n": 10, "k": 4},
        {"n": 0, "k": 4},
        {"n": 3, "k": 0},
        {"n": 4, "k": 4},
    ],
)

add(
    "python-ex-wait-times",
    "Sequential versus Gather",
    "easy",
    ["python", "asyncio"],
    "Implement `solve(a, b)`. Both are non-negative durations. Return `{\"sequential\": a+b, \"concurrent\": the max of a and b}`. Negative inputs return `error`.",
    ["Concurrent time is the slower call", "Sequential time adds"],
    ["Reject negatives.", "Sum for sequential.", "Max for concurrent."],
    "Awaiting two coroutines one after another adds their waits. gather overlaps them, so the wall time is the slower one, plus a little scheduling you can ignore here. The two numbers are the reason to gather independent I/O.",
    "O(1)", "O(1)",
    """
def solve(a, b):
    if a < 0 or b < 0:
        return "error"
    return {"sequential": a + b, "concurrent": a if a > b else b}
""",
    [
        {"a": 2, "b": 5},
        {"a": 0, "b": 0},
        {"a": -1, "b": 2},
        {"a": 3, "b": 3},
    ],
)

add(
    "python-ex-block-smell",
    "Blocking Smell",
    "medium",
    ["python", "asyncio"],
    "Implement `solve(call)`. Return `unsafe` for `time.sleep`, `requests`, and `open`. Return `safe` for `asyncio.sleep` and `httpx-async`. Any other call returns `unknown`.",
    ["Blocking calls are unsafe on the loop", "Async sleeps are safe"],
    ["Map the known names.", "Default to unknown.", "Do not mark requests as safe."],
    "The event loop runs coroutines cooperatively. time.sleep and a synchronous HTTP library hold the thread, so every other task waits. asyncio.sleep yields. An async HTTP client yields on I/O. The classification is the review comment.",
    "O(1)", "O(1)",
    """
def solve(call):
    unsafe = {"time.sleep", "requests", "open"}
    safe = {"asyncio.sleep", "httpx-async"}
    if call in unsafe:
        return "unsafe"
    if call in safe:
        return "safe"
    return "unknown"
""",
    [{"call": "requests"}, {"call": "asyncio.sleep"}, {"call": "open"}, {"call": "print"}],
)

add(
    "python-ex-assert-equal",
    "Assert Shape",
    "easy",
    ["python", "unittest"],
    "Implement `solve(expected, actual)`. Return `pass` when the two values are equal and `fail` when they are not. Integers and strings compare with ordinary equality. Do not coerce.",
    ["1 and the string 1 are not equal", "Equal values pass"],
    ["Use ==.", "Return pass or fail.", "Do not strip strings."],
    "assertEqual fails when the values differ and the message shows both. This function is that comparison's outcome. A truthiness check would treat two different non-empty strings as the same success, which is the weaker assertion.",
    "O(n)", "O(1)",
    """
def solve(expected, actual):
    return "pass" if expected == actual else "fail"
""",
    [
        {"expected": 1, "actual": 1},
        {"expected": 1, "actual": 2},
        {"expected": "1", "actual": 1},
        {"expected": "", "actual": ""},
    ],
)

add(
    "python-ex-fresh-fixture",
    "Fresh Fixture",
    "medium",
    ["python", "unittest"],
    "Implement `solve(reset)`. Two tests each append 1. If `reset` is 1, each test starts from an empty list, so the second test sees `[1]`. If `reset` is 0, they share a list, so the second test sees `[1, 1]`. Return `{\"first\": [...], \"second\": [...]}`.",
    ["reset 1 isolates", "reset 0 leaks"],
    ["Shared mode uses one list for both appends.", "Reset mode uses a new list for the second test.", "Each test appends a single 1."],
    "A class-level list survives from test to test. setUp that assigns a new list on self gives the second test an empty container. The two results are the leak and the fix, side by side.",
    "O(1)", "O(1)",
    """
def solve(reset):
    if reset:
        return {"first": [1], "second": [1]}
    shared = []
    shared.append(1)
    first = list(shared)
    shared.append(1)
    return {"first": first, "second": list(shared)}
""",
    [{"reset": 1}, {"reset": 0}, {"reset": 1}, {"reset": 0}],
)

add(
    "python-ex-parse-blank",
    "Raises",
    "easy",
    ["python", "unittest"],
    "Implement `solve(text)`. A blank string after strip returns `error`. Any other string returns `ok`. This is the parser a test would wrap with assertRaises on the blank input. The sandbox uses the string instead of an exception.",
    ["Whitespace-only is blank", "Other text is ok"],
    ["Strip.", "Empty means error.", "Otherwise ok."],
    "assertRaises passes only when the call inside the block raises. A blank string is the input that should fail. Returning a distinct error string lets the judge see the rejection without depending on the harness to expect an exception.",
    "O(n)", "O(1)",
    """
def solve(text):
    if not text.strip():
        return "error"
    return "ok"
""",
    [{"text": "  "}, {"text": "ada"}, {"text": ""}, {"text": " a "}],
)

add(
    "python-ex-clamp-table",
    "Clamp Table",
    "easy",
    ["python", "pytest"],
    "Implement `solve(values)`. Clamp each integer to the inclusive range 0 through 10. Return the list of clamped values. Bounds are fixed. Values inside stay.",
    ["0 and 10 are legal", "Order is preserved"],
    ["Below 0 becomes 0.", "Above 10 becomes 10.", "Map the list in order."],
    "A parametrized test is a table of inputs and expected outputs. This function is the body those rows call. One implementation serves every row. A branch per test name would mean the rows are not the same behavior.",
    "O(n)", "O(n)",
    """
def solve(values):
    out = []
    for value in values:
        if value < 0:
            out.append(0)
        elif value > 10:
            out.append(10)
        else:
            out.append(value)
    return out
""",
    [
        {"values": [-1, 3, 11]},
        {"values": [0, 10]},
        {"values": []},
        {"values": [4]},
    ],
)

add(
    "python-ex-clamp-bounds",
    "Raises Bounds",
    "easy",
    ["python", "pytest"],
    "Implement `solve(low, high)`. Return `ok` when `low` is less than or equal to `high`. Return `error` when the bounds are inverted.",
    ["Equal bounds are ok", "Inverted bounds are error"],
    ["Compare low and high.", "Return ok or error.", "Do not clamp a value here. This function only checks the bounds."],
    "The raising case does not belong in the same table as the numeric rows, because the result is not a number. A separate test calls the validator. Inverted bounds are the error. Equal bounds are a legal empty-width range.",
    "O(1)", "O(1)",
    """
def solve(low, high):
    if low > high:
        return "error"
    return "ok"
""",
    [
        {"low": 0, "high": 10},
        {"low": 5, "high": 4},
        {"low": 1, "high": 1},
        {"low": 2, "high": 1},
    ],
)

add(
    "python-ex-fixture-scope",
    "Fixture Scope",
    "medium",
    ["python", "pytest"],
    "Implement `solve(scope)`. `scope` is `function` or `module`. Two tests append 1. Function scope gives the second test a fresh list, so it sees `[1]`. Module scope shares the list, so the second test sees `[1, 1]`. Return the second test's list. Any other scope returns `error`.",
    ["function isolates", "module leaks if the fixture is a list"],
    ["function returns [1].", "module returns [1, 1].", "Other words return error."],
    "A module-scoped mutable fixture is one object for every test in the module. Appends accumulate. Function scope builds it again. The second test's list is the observation. Wider scope is a performance choice you only want for immutable fixtures.",
    "O(1)", "O(1)",
    """
def solve(scope):
    if scope == "function":
        return [1]
    if scope == "module":
        return [1, 1]
    return "error"
""",
    [{"scope": "function"}, {"scope": "module"}, {"scope": "session"}, {"scope": "function"}],
)

add(
    "python-ex-mark-split",
    "Waves Mark",
    "easy",
    ["python", "pytest"],
    "Implement `solve(names)`. Each name is a test id. Names containing the substring `integration` go to the integration list. The rest go to fast. Return `{\"fast\": [...], \"integration\": [...]}` in input order.",
    ["The marker word is integration", "A name can land in only one list"],
    ["Test the substring.", "Append to the matching list.", "Do not sort."],
    "A mark lets CI run the fast suite by default and the integration suite later. The split is the selection the mark expresses. A test whose name includes the word is the stand-in for a mark in this sandbox.",
    "O(n)", "O(n)",
    """
def solve(names):
    fast = []
    integration = []
    for name in names:
        if "integration" in name:
            integration.append(name)
        else:
            fast.append(name)
    return {"fast": fast, "integration": integration}
""",
    [
        {"names": ["test_clamp", "test_db_integration", "test_add"]},
        {"names": []},
        {"names": ["integration_only"]},
        {"names": ["a", "b"]},
    ],
)

add(
    "python-ex-memory-save",
    "Memory Save",
    "easy",
    ["python", "testing"],
    "Implement `solve(amount)`. Return `saved` when `amount` is a positive int. Return `error` otherwise. This is the fake repository's save rule.",
    ["Zero is rejected", "Positive ints are saved"],
    ["type must be int.", "The value must be > 0.", "Otherwise error."],
    "A fake that accepts a zero amount is softer than the database constraint and will hide a bug. The memory store rejects non-positive amounts the same way the real one does. The string is the outcome of that one save.",
    "O(1)", "O(1)",
    """
def solve(amount):
    if type(amount) is int and amount > 0:
        return "saved"
    return "error"
""",
    [{"amount": 500}, {"amount": 0}, {"amount": -1}, {"amount": 1}],
)

add(
    "python-ex-place-saves",
    "Place Saves",
    "medium",
    ["python", "testing"],
    "Implement `solve(order_id, amount)`. If the amount is not a positive int, return `{\"status\": \"error\", \"row\": \"none\"}`. Otherwise return `{\"status\": \"ok\", \"row\": \"order_id:amount\"}`. Checkout saves through the store. The row is what a test reads back.",
    ["A rejected amount does not write a row", "The row text includes both fields"],
    ["Validate the amount.", "On success, format the row.", "On failure, the row is the string none."],
    "Asserting the saved row is stronger than asserting that a method was called. The fake store's contents are the behavior. A charge that never landed fails this check even if a mock recorded a call with the right name.",
    "O(1)", "O(1)",
    """
def solve(order_id, amount):
    if type(amount) is not int or amount <= 0:
        return {"status": "error", "row": "none"}
    return {"status": "ok", "row": f"{order_id}:{amount}"}
""",
    [
        {"order_id": "o1", "amount": 500},
        {"order_id": "o1", "amount": 0},
        {"order_id": "o2", "amount": 1},
        {"order_id": "", "amount": 5},
    ],
)

add(
    "python-ex-patch-path",
    "Patch Path",
    "medium",
    ["python", "testing"],
    "Implement `solve(importer, name)`. Module `importer` did `from billing import name`, so the name is used as `importer.name`. Return the dotted path `importer.name`, which is the path patch must replace. Do not return `billing.name`.",
    ["Patch where the name is used", "The defining module is not the answer"],
    ["Join importer and name with a dot.", "Ignore the defining module.", "Both parts are non-empty in the tests."],
    "from billing import charge binds charge in the importer's namespace. Patching billing.charge does not change the name the importer already holds. patch('orders.charge') replaces the name orders looks up. The returned path is that use site.",
    "O(n)", "O(n)",
    """
def solve(importer, name):
    return importer + "." + name
""",
    [
        {"importer": "orders", "name": "charge"},
        {"importer": "api", "name": "Client"},
        {"importer": "a", "name": "b"},
        {"importer": "orders", "name": "save"},
    ],
)

add(
    "python-ex-red-first",
    "Red First",
    "easy",
    ["python", "testing"],
    "Implement `solve(actual, expected)`. A buggy clamp returned `actual` and the test expects `expected`. Return `fail` when they differ and `pass` when they match. Include nothing else. The failing test is the first TDD step.",
    ["Different values fail", "Equal values pass"],
    ["Compare the two numbers.", "Return fail or pass.", "Do not clamp them yourself."],
    "The first step of a bugfix in TDD is a test that fails on the current code. If actual is already expected, you have not reproduced the bug. The word fail is the red bar. You write the fix only after you see it.",
    "O(1)", "O(1)",
    """
def solve(actual, expected):
    return "pass" if actual == expected else "fail"
""",
    [
        {"actual": -2, "expected": 0},
        {"actual": 0, "expected": 0},
        {"actual": 11, "expected": 10},
        {"actual": 4, "expected": 4},
    ],
)

add(
    "python-ex-hottest-function",
    "Top Function",
    "easy",
    ["python", "profiling"],
    "Implement `solve(rows)`. `rows` is a list of `[name, time]` with integer times. Return the name with the largest time. Break ties by the name that is smaller. The list is non-empty.",
    ["Higher time wins", "Then the smaller name"],
    ["Track the best pair.", "Replace on a higher time or an equal time with a smaller name.", "Return the name only."],
    "Internal time in a profile is the column that names the function whose body burned CPU. The maximum is the first place you look. A tie should be stable so two equal rows do not flap between runs of a report.",
    "O(n)", "O(1)",
    """
def solve(rows):
    best_name, best_time = rows[0]
    for name, time in rows[1:]:
        if time > best_time or (time == best_time and name < best_name):
            best_name, best_time = name, time
    return best_name
""",
    [
        {"rows": [["a", 5], ["b", 9], ["c", 9]]},
        {"rows": [["only", 1]]},
        {"rows": [["b", 2], ["a", 2]]},
        {"rows": [["z", 0], ["a", 1]]},
    ],
)

add(
    "python-ex-call-drop",
    "Call Drop",
    "medium",
    ["python", "profiling"],
    "Implement `solve(before, after)`. Both are call counts for the same function. Return `hoisted` when `after` is strictly smaller than `before` and `after` is at least 1. Return `same` when they are equal. Return `worse` when after is greater. Return `gone` when after is 0.",
    ["A drop to a positive count is hoisted", "Zero means the call disappeared"],
    ["Compare the two integers.", "Check zero before the strict less-than.", "Equal is same."],
    "Hoisting a regex compile out of a loop drops ncalls from the row count to 1. The profile proves it. A count that does not fall means the hoist did not land on the path you measured. Zero means you deleted the call, which is a different change and worth its own look.",
    "O(1)", "O(1)",
    """
def solve(before, after):
    if after == 0:
        return "gone"
    if after < before:
        return "hoisted"
    if after == before:
        return "same"
    return "worse"
""",
    [
        {"before": 1000, "after": 1},
        {"before": 10, "after": 10},
        {"before": 10, "after": 0},
        {"before": 10, "after": 12},
    ],
)

add(
    "python-ex-growth-class",
    "Two Sizes",
    "medium",
    ["python", "profiling"],
    "Implement `solve(t1, t4)`. `t1` is the time at size n and `t4` is the time at size 4n, both positive integers. Return `linear` when t4 is less than or equal to 6 times t1. Return `super` when it is larger. A rough linear curve grows about 4 times. A quadratic curve grows about 16 times. The threshold 6 separates them.",
    ["Times are positive", "6 is the cutoff, inclusive on the linear side"],
    ["If t4 <= 6 * t1, return linear.", "Otherwise return super.", "Do not require an exact 4 times ratio."],
    "Two sizes distinguish a linear scan from a quadratic one without a formal fit. Noise means a linear function may land a bit above 4. A quadratic jump is far past 6. The cutoff is a decision rule for a profile, not a proof, and it is good enough to choose which function to read.",
    "O(1)", "O(1)",
    """
def solve(t1, t4):
    if t4 <= 6 * t1:
        return "linear"
    return "super"
""",
    [
        {"t1": 10, "t4": 40},
        {"t1": 10, "t4": 160},
        {"t1": 10, "t4": 60},
        {"t1": 5, "t4": 31},
    ],
)

add(
    "python-ex-snapshot-growth",
    "Snapshot Growth",
    "medium",
    ["python", "profiling"],
    "Implement `solve(before, after)`. Both are dicts of line id to allocation count. Return the sorted list of line ids whose count grew. Lines that shrank or stayed equal are omitted. Lines only in `after` count as growth.",
    ["Sort the ids", "Equal counts are not growth"],
    ["Consider the union of keys.", "Keep a key when after's count is greater than before's, treating absence as 0.", "Sort the kept ids."],
    "A tracemalloc diff names the lines that allocated more between two snapshots. Growth is the leak candidate. A line that stayed flat is not. Sorting the report makes the test stable and the ticket readable.",
    "O(n log n)", "O(n)",
    """
def solve(before, after):
    grown = []
    for key in set(before) | set(after):
        if after.get(key, 0) > before.get(key, 0):
            grown.append(key)
    return sorted(grown)
""",
    [
        {"before": {"a": 1, "b": 2}, "after": {"a": 1, "b": 3}},
        {"before": {}, "after": {"a": 1}},
        {"before": {"a": 2}, "after": {"a": 1}},
        {"before": {"b": 1, "a": 1}, "after": {"a": 2, "b": 2}},
    ],
)

add(
    "python-ex-join-pieces",
    "Join Pieces",
    "easy",
    ["python", "performance"],
    "Implement `solve(parts)`. Join the strings with a comma. An empty list returns an empty string. Do not leave a trailing comma.",
    ["Comma between parts only", "Empty input is empty"],
    ["Use str.join.", "Do not append commas in a loop and then strip one.", "One separator rule."],
    "Repeated concatenation copies a growing string. join allocates once and copies each piece once. The comma is the separator, not a terminator, so the empty list and a single piece have no comma.",
    "O(n)", "O(n)",
    """
def solve(parts):
    return ",".join(parts)
""",
    [{"parts": ["a", "b", "c"]}, {"parts": []}, {"parts": ["a"]}, {"parts": ["a", ""]}],
)

add(
    "python-ex-filter-set",
    "Filter Set",
    "medium",
    ["python", "performance"],
    "Implement `solve(left, right)`. Return the items from `left` that appear in `right`, in `left`'s order. Duplicates in `left` are kept when the value is allowed. Build a set from `right` for the membership test.",
    ["Order follows left", "right is a membership set"],
    ["set(right) once.", "Walk left and keep hits.", "Do not sort."],
    "A nested scan is quadratic. A set of the allowed values makes each membership expected constant time, and walking left preserves the order the caller already had. Building the set inside the loop would throw the gain away.",
    "O(n + m)", "O(m)",
    """
def solve(left, right):
    allowed = set(right)
    return [item for item in left if item in allowed]
""",
    [
        {"left": ["a", "b", "a"], "right": ["a"]},
        {"left": ["a"], "right": []},
        {"left": [], "right": ["a"]},
        {"left": ["b", "a"], "right": ["a", "b"]},
    ],
    companies=["Amazon"],
)

add(
    "python-ex-two-sizes",
    "Growth Class",
    "medium",
    ["python", "performance"],
    "Implement `solve(t1, t4)`. Same rule as the profiling classifier: return `linear` when `t4` is at most 6 times `t1`, and `super` otherwise. Times are positive integers.",
    ["Cutoff is 6 times, inclusive", "super means the curve is steeper than linear noise"],
    ["Compare t4 with 6 * t1.", "Less or equal is linear.", "Greater is super."],
    "n versus 4n is the cheap experiment after you change an algorithm. Linear work scales near 4. Quadratic work scales near 16. The factor 6 is the fence between noise and a real exponent change.",
    "O(1)", "O(1)",
    """
def solve(t1, t4):
    if t4 <= 6 * t1:
        return "linear"
    return "super"
""",
    [
        {"t1": 8, "t4": 32},
        {"t1": 8, "t4": 128},
        {"t1": 8, "t4": 48},
        {"t1": 2, "t4": 13},
    ],
)

add(
    "python-ex-queue-order",
    "Queue Cost",
    "easy",
    ["python", "performance"],
    "Implement `solve(ops)`. Ops are `[\"enq\", value]` or `[\"deq\"]`. Use a deque. Return the list of dequeued integers. A dequeue on an empty deque records nothing and is skipped. Values are integers.",
    ["FIFO order", "Empty dequeue is a no-op"],
    ["append and popleft.", "Skip empty pops.", "Return only the popped values."],
    "list.pop(0) moves every later element. deque.popleft does not. The popped sequence is the FIFO order, which is what you assert while the structure choice is what makes the cost constant per operation.",
    "O(n)", "O(n)",
    """
def solve(ops):
    from collections import deque
    queue = deque()
    out = []
    for op in ops:
        if op[0] == "enq":
            queue.append(op[1])
        elif queue:
            out.append(queue.popleft())
    return out
""",
    [
        {"ops": [["enq", 1], ["enq", 2], ["deq"], ["deq"]]},
        {"ops": [["deq"], ["enq", 3], ["deq"]]},
        {"ops": []},
        {"ops": [["enq", 1], ["deq"], ["deq"]]},
    ],
)

add(
    "python-ex-hoist-match",
    "Hoist Check",
    "easy",
    ["python", "performance"],
    "Implement `solve(per_row, once)`. Both are strings, the result of compiling a pattern inside the loop and the result of compiling it once. Return `match` when they are equal and `drift` when they are not. Hoisting must not change the result.",
    ["Equal results match", "Any difference is drift"],
    ["Compare the two strings.", "Return match or drift.", "Do not ignore case unless they already match."],
    "A hoist that changes the output is not an optimization. The before and after strings have to match. The call count drops in the profile. This function is the behavior check that sits next to that profile.",
    "O(n)", "O(1)",
    """
def solve(per_row, once):
    return "match" if per_row == once else "drift"
""",
    [
        {"per_row": "ab", "once": "ab"},
        {"per_row": "ab", "once": "a"},
        {"per_row": "", "once": ""},
        {"per_row": "a", "once": "A"},
    ],
)

add(
    "python-ex-http-classify",
    "Classify Status",
    "medium",
    ["python", "http"],
    "Implement `solve(status, method, idempotent)`. `method` is `GET` or `POST`. `idempotent` is 0 or 1. Return `backoff` for 429, `ok` for 200 through 299, `caller` for 400 through 499 except 429, `retry` for status >= 500 when the method is GET or idempotent is 1, and `unavailable` for other 5xx. Anything else returns `unknown`.",
    ["429 is backoff even though it is a 4xx", "POST without the flag does not retry a 500"],
    ["Check 429 first.", "Then the 2xx and 4xx ranges.", "Then 5xx with the method and the flag."],
    "Retry policy depends on the status and on whether repeating the request can double a charge. GET is safe to retry. POST is safe only with an idempotency key, which the flag represents. 429 means slow down, not immediately try again. 4xx other than 429 is the caller's bug.",
    "O(1)", "O(1)",
    """
def solve(status, method, idempotent):
    if status == 429:
        return "backoff"
    if 200 <= status < 300:
        return "ok"
    if 400 <= status < 500:
        return "caller"
    if status >= 500 and (method == "GET" or idempotent):
        return "retry"
    if status >= 500:
        return "unavailable"
    return "unknown"
""",
    [
        {"status": 200, "method": "GET", "idempotent": 0},
        {"status": 503, "method": "POST", "idempotent": 0},
        {"status": 503, "method": "POST", "idempotent": 1},
        {"status": 404, "method": "GET", "idempotent": 0},
    ],
)

add(
    "python-ex-timeout-pair",
    "Timeout Pair",
    "easy",
    ["python", "http"],
    "Implement `solve(connect, read)`. Both are timeout budgets in seconds, as integers. Return `ok` when both are positive. Return `error` when either is less than 1.",
    ["Zero is not a timeout", "Both sides are required"],
    ["Check connect and read.", "Both must be >= 1.", "Otherwise error."],
    "A missing timeout waits forever. A pair separates connect failure from a stall after the server accepts. Non-positive numbers are not budgets. The check belongs next to the client constructor so a call site cannot forget it.",
    "O(1)", "O(1)",
    """
def solve(connect, read):
    if connect >= 1 and read >= 1:
        return "ok"
    return "error"
""",
    [
        {"connect": 2, "read": 5},
        {"connect": 0, "read": 5},
        {"connect": 2, "read": 0},
        {"connect": 1, "read": 1},
    ],
)

add(
    "python-ex-query-build",
    "Query Build",
    "easy",
    ["python", "http"],
    "Implement `solve(pairs, secret)`. `pairs` is a list of `[key, value]` strings to put in the query. `secret` must not be used as a key or a value. Return the query string `k=v&k=v` in order, with no leading question mark. If any key or value equals `secret`, return `error`. Do not URL-encode. The tests use simple tokens.",
    ["Secret values are rejected", "Order follows pairs"],
    ["Scan for the secret first.", "Join key=value with &.", "An empty pair list returns an empty string when the secret is unused."],
    "Query strings land in access logs. A token in the query is a leak. Building the query from an explicit list, and refusing the secret if it shows up, keeps the Authorization header as the only place the token should live.",
    "O(n)", "O(n)",
    """
def solve(pairs, secret):
    parts = []
    for key, value in pairs:
        if key == secret or value == secret:
            return "error"
        parts.append(key + "=" + value)
    return "&".join(parts)
""",
    [
        {"pairs": [["q", "ada"], ["page", "2"]], "secret": "tok"},
        {"pairs": [["token", "tok"]], "secret": "tok"},
        {"pairs": [], "secret": "tok"},
        {"pairs": [["q", "a b"]], "secret": "tok"},
    ],
)

add(
    "python-ex-retry-cap",
    "Retry Cap",
    "medium",
    ["python", "http"],
    "Implement `solve(failures, cap)`. `failures` is how many times the call failed. `cap` is the maximum number of attempts, including the first. Return `{\"attempts\": used, \"stopped\": word}` where used is the minimum of failures+... You attempt min(failures, cap) if failures means failures before success? Define it as: you may try at most `cap` times. You needed `failures` failures and then would have stopped anyway. used = min(failures, cap). `stopped` is `cap` when failures is greater than or equal to cap, else `done`. `cap` less than 1 returns `error`.",
    ["cap includes the first try", "Exceeding the cap stops"],
    ["Reject cap < 1.", "used is the minimum of failures and cap.", "stopped is cap when you hit the ceiling, else done."],
    "Unbounded retries turn a short outage into a stampede. The cap is the number of attempts, not the number of extra tries after the first. Hitting the cap is a stop the caller can see. Finishing earlier is the done path.",
    "O(1)", "O(1)",
    """
def solve(failures, cap):
    if cap < 1:
        return "error"
    used = failures if failures < cap else cap
    stopped = "cap" if failures >= cap else "done"
    return {"attempts": used, "stopped": stopped}
""",
    [
        {"failures": 2, "cap": 5},
        {"failures": 5, "cap": 3},
        {"failures": 0, "cap": 3},
        {"failures": 1, "cap": 0},
    ],
)

add(
    "python-ex-create-status",
    "Create Status",
    "medium",
    ["python", "fastapi"],
    "Implement `solve(found_user, duplicate, amount)`. `found_user` and `duplicate` are 0 or 1. Return 401 when the user was not found, 422 when `amount` is less than or equal to 0, 409 when duplicate is 1, and 201 otherwise. Check in that order.",
    ["401 before the body rules", "409 only for a valid amount"],
    ["Missing user is 401.", "Non-positive amount is 422.", "Then duplicate is 409, else 201."],
    "The status code is the contract. A missing user is 401 from the auth dependency, before the service runs. A bad amount is a validation failure. A duplicate id is a conflict. Success is 201, not 200, because this route creates.",
    "O(1)", "O(1)",
    """
def solve(found_user, duplicate, amount):
    if not found_user:
        return 401
    if amount <= 0:
        return 422
    if duplicate:
        return 409
    return 201
""",
    [
        {"found_user": 1, "duplicate": 0, "amount": 500},
        {"found_user": 0, "duplicate": 0, "amount": 500},
        {"found_user": 1, "duplicate": 1, "amount": 500},
        {"found_user": 1, "duplicate": 0, "amount": 0},
    ],
)

add(
    "python-ex-strip-secrets",
    "Strip Secrets",
    "easy",
    ["python", "fastapi"],
    "Implement `solve(row)`. `row` is a dict. Remove `password_hash` and `internal_note` if present. Return the remaining dict.",
    ["Other keys stay", "Missing secret keys are fine"],
    ["Copy and drop those two names.", "Do not blank the values and leave the keys.", "Return the copy."],
    "A response model is an allow-list. Deleting known secret keys is the same idea when you are looking at a raw row in a test. Leaving the key with a blank value still tells the client the field exists. Delete the key.",
    "O(n)", "O(n)",
    """
def solve(row):
    hidden = {"password_hash", "internal_note"}
    return {key: value for key, value in row.items() if key not in hidden}
""",
    [
        {"row": {"id": "i1", "password_hash": "x", "amount": 5}},
        {"row": {"id": "i1"}},
        {"row": {}},
        {"row": {"internal_note": "n", "name": "a"}},
    ],
)

add(
    "python-ex-id-mismatch",
    "Path Versus Body",
    "medium",
    ["python", "fastapi"],
    "Implement `solve(path_id, body_id)`. Return `ok` when `body_id` is the empty string, meaning the body omitted the id, or when the two ids are equal. Return `mismatch` when the body id is non-empty and different.",
    ["An omitted body id is the empty string and is ok", "A disagreeing id is mismatch"],
    ["Empty body_id is ok.", "Equal ids are ok.", "Otherwise mismatch."],
    "The resource id lives in the path. A body that repeats a different id is a confused client, and updating the path id while saving the body id splits the record. Reject the mismatch. An omitted body id means the path is the only id, which is the normal case.",
    "O(n)", "O(1)",
    """
def solve(path_id, body_id):
    if body_id == "" or body_id == path_id:
        return "ok"
    return "mismatch"
""",
    [
        {"path_id": "i1", "body_id": ""},
        {"path_id": "i1", "body_id": "i1"},
        {"path_id": "i1", "body_id": "i2"},
        {"path_id": "", "body_id": "i2"},
    ],
)

add(
    "python-ex-route-order",
    "Attempt Order",
    "medium",
    ["python", "fastapi"],
    "Implement `solve(valid, authed)`. Both are 0 or 1. Return the list of stages that run. Validation always runs. Auth runs only when valid is 1. Service runs only when valid and authed are both 1. The names are `validation`, `auth`, and `service`.",
    ["A bad body does not authenticate", "A failed auth does not call the service"],
    ["Start with validation.", "Append auth only after a valid body.", "Append service only after auth."],
    "The pipeline is validate, then dependencies, then the service. A 422 should not show up as a service call in a fake. A 401 should not either. The list is the stages a test asserts by watching which fakes were touched.",
    "O(1)", "O(1)",
    """
def solve(valid, authed):
    stages = ["validation"]
    if valid:
        stages.append("auth")
        if authed:
            stages.append("service")
    return stages
""",
    [
        {"valid": 1, "authed": 1},
        {"valid": 0, "authed": 1},
        {"valid": 1, "authed": 0},
        {"valid": 0, "authed": 0},
    ],
)

add(
    "python-ex-cursor-page",
    "Cursor Page",
    "medium",
    ["python", "rest"],
    "Implement `solve(ids, cursor, limit)`. Sort `ids` ascending. `cursor` is the empty string for the first page, or an id from the list. Return `{\"ids\": page, \"next\": last_id or \"\"}`. `next` is empty when the page is short or there is nothing after it. `limit` outside 1 through 100 returns `error`. An unknown cursor returns `error`.",
    ["Sort before paging", "next is empty when finished"],
    ["Validate limit.", "Find the start just after the cursor, or 0 when the cursor is empty.", "The page is the next limit ids. next is the last id only when more remain."],
    "A cursor that means the last id you returned, plus a stable sort, does not skip or duplicate rows when new ids are inserted above the cursor. Offset pages do. The empty next string tells the client to stop.",
    "O(n log n)", "O(n)",
    """
def solve(ids, cursor, limit):
    if limit < 1 or limit > 100:
        return "error"
    ordered = sorted(ids)
    start = 0
    if cursor:
        if cursor not in ordered:
            return "error"
        start = ordered.index(cursor) + 1
    chunk = ordered[start:start + limit]
    nxt = ""
    if len(chunk) == limit and start + limit < len(ordered):
        nxt = chunk[-1]
    return {"ids": chunk, "next": nxt}
""",
    [
        {"ids": ["b", "a", "c", "d"], "cursor": "", "limit": 2},
        {"ids": ["b", "a", "c", "d"], "cursor": "b", "limit": 2},
        {"ids": ["a"], "cursor": "z", "limit": 2},
        {"ids": ["a", "b"], "cursor": "", "limit": 0},
    ],
)

add(
    "python-ex-idempotent-create",
    "Idempotent Create",
    "medium",
    ["python", "rest"],
    "Implement `solve(seen, key, new_id)`. `seen` is a dict of idempotency key to the first id. If `key` is already there, return that stored id. Otherwise return `new_id`. Do not return `new_id` for a repeated key.",
    ["The first id wins", "seen is not mutated in the return value. Return only the id string."],
    ["Look up the key.", "A hit returns the stored id.", "A miss returns new_id."],
    "A retried POST with the same idempotency key must return the original resource, not create another. The store lives in the same transaction as the insert. This function is the decision: known key keeps the first id.",
    "O(1)", "O(1)",
    """
def solve(seen, key, new_id):
    if key in seen:
        return seen[key]
    return new_id
""",
    [
        {"seen": {"K": "i1"}, "key": "K", "new_id": "i2"},
        {"seen": {}, "key": "K", "new_id": "i1"},
        {"seen": {"A": "i1"}, "key": "B", "new_id": "i2"},
        {"seen": {"K": "i1"}, "key": "K", "new_id": "i1"},
    ],
)

add(
    "python-ex-status-pick",
    "Status Pick",
    "easy",
    ["python", "rest"],
    "Implement `solve(situation)`. Map `fetched` to 200, `created` to 201, `deleted` to 204, `missing` to 404, and `conflict` to 409. Any other word returns 500.",
    ["deleted is 204, not 200", "Unknown is 500"],
    ["Use a dict.", "Default to 500.", "Return an integer."],
    "Clients and monitors branch on status codes. Using 200 for every outcome hides failures. The five situations here are the ones a small resource API actually returns. 500 is the leftover for a bug, not for a missing row.",
    "O(1)", "O(1)",
    """
def solve(situation):
    return {"fetched": 200, "created": 201, "deleted": 204, "missing": 404, "conflict": 409}.get(situation, 500)
""",
    [
        {"situation": "created"},
        {"situation": "deleted"},
        {"situation": "missing"},
        {"situation": "nope"},
    ],
)

add(
    "python-ex-version-conflict",
    "Version Conflict",
    "medium",
    ["python", "rest"],
    "Implement `solve(stored, client, new_value)`. If `client` equals `stored`, return `{\"version\": stored + 1, \"value\": new_value}`. Otherwise return `conflict`. The successful write bumps the version by 1.",
    ["Stale clients conflict", "A match increments"],
    ["Compare client and stored.", "On a match, add 1 to the version and keep the new value.", "On a miss, return the string conflict."],
    "Two clients that read version 3 and both write will lose one update if the second overwrites the first. Comparing the version and updating only when it matches turns the second write into a 409. The client refetches. The stored version advances by one on success.",
    "O(1)", "O(1)",
    """
def solve(stored, client, new_value):
    if client != stored:
        return "conflict"
    return {"version": stored + 1, "value": new_value}
""",
    [
        {"stored": 3, "client": 3, "new_value": "b"},
        {"stored": 4, "client": 3, "new_value": "b"},
        {"stored": 0, "client": 0, "new_value": "a"},
        {"stored": 1, "client": 2, "new_value": "a"},
    ],
)

add(
    "python-ex-conditional-debit",
    "Conditional Debit",
    "medium",
    ["python", "sql"],
    "Implement `solve(balance, amount)`. If `amount` is not a positive int, return `error`. If `balance` is less than `amount`, return `miss`. Otherwise return the new balance. Do not clamp a short balance to zero.",
    ["A short balance is a miss", "The new balance is balance - amount"],
    ["Reject a non-positive amount.", "Compare balance with amount.", "Subtract only when it covers."],
    "The SQL is an UPDATE that subtracts only when the balance covers the debit, and the row count tells you whether it happened. Computing the new balance in Python from a stale read loses updates. This function is the predicate and the arithmetic of that one statement.",
    "O(1)", "O(1)",
    """
def solve(balance, amount):
    if type(amount) is not int or amount <= 0:
        return "error"
    if balance < amount:
        return "miss"
    return balance - amount
""",
    [
        {"balance": 100, "amount": 40},
        {"balance": 30, "amount": 40},
        {"balance": 40, "amount": 40},
        {"balance": 10, "amount": 0},
    ],
)

add(
    "python-ex-invoice-count",
    "Invoice Count",
    "easy",
    ["python", "sql"],
    "Implement `solve(rows)`. Each row is `[customer, invoice]` where `invoice` is an int or the string `none` for an unmatched parent from a left join. Return how many rows have a real invoice id.",
    ["none does not count", "Zero is a real id if you ever see it. The tests use positive ids or none."],
    ["Count rows whose invoice is not the string none.", "Do not count the length of the list.", "Customers with only a null invoice add nothing."],
    "COUNT(*) after a left join counts parent rows. COUNT(invoice_id) skips nulls. The string none is that null. Counting the wrong one invents invoices for customers who have none.",
    "O(n)", "O(1)",
    """
def solve(rows):
    return sum(1 for _customer, invoice in rows if invoice != "none")
""",
    [
        {"rows": [["ada", 1], ["ada", 2], ["grace", "none"]]},
        {"rows": [["grace", "none"]]},
        {"rows": []},
        {"rows": [["ada", 3]]},
    ],
)

add(
    "python-ex-index-prefix",
    "Index Prefix",
    "medium",
    ["python", "sql"],
    "Implement `solve(columns, filters, order_by)`. `columns` is the composite index, left to right. `filters` is the list of equality columns in the query, in index order. `order_by` is a column name or an empty string. Return `yes` when `filters` is a prefix of `columns` and `order_by` is either empty or the next column in the index. Return `no` otherwise.",
    ["Equality columns must be the leading prefix", "The sort can use the next column"],
    ["filters must equal columns[:len(filters)].", "Then the next column may match order_by.", "A filter that skips a leading column is no."],
    "A composite index serves a leftmost prefix. Equality on the leading columns, then a sort on the following column, can walk the index in order. Filtering only on a later column cannot. This function is that rule for one index and one query shape.",
    "O(n)", "O(1)",
    """
def solve(columns, filters, order_by):
    if columns[:len(filters)] != filters:
        return "no"
    if order_by == "":
        return "yes"
    nxt = len(filters)
    if nxt < len(columns) and columns[nxt] == order_by:
        return "yes"
    return "no"
""",
    [
        {"columns": ["customer_id", "created_at"], "filters": ["customer_id"], "order_by": "created_at"},
        {"columns": ["customer_id", "created_at"], "filters": ["created_at"], "order_by": ""},
        {"columns": ["customer_id", "created_at"], "filters": ["customer_id"], "order_by": ""},
        {"columns": ["a", "b", "c"], "filters": ["a", "b"], "order_by": "c"},
    ],
)

add(
    "python-ex-having-split",
    "Having Split",
    "medium",
    ["python", "sql"],
    "Implement `solve(clauses)`. Each clause is `[text, kind]` where kind is `row` or `agg`. Return `{\"where\": [...], \"having\": [...]}` with the texts. Row filters go to where. Aggregate filters go to having. Order is preserved.",
    ["kind decides the clause", "Do not look at the text to guess"],
    ["Append row texts to where.", "Append agg texts to having.", "Unknown kinds are dropped."],
    "WHERE runs before grouping and cannot see aggregates. HAVING runs after. Putting a customer filter in HAVING is legal in some engines and wasteful. Putting COUNT in WHERE is an error. The kind flag is the writer's decision, and the split is where the SQL clauses go.",
    "O(n)", "O(n)",
    """
def solve(clauses):
    where = []
    having = []
    for text, kind in clauses:
        if kind == "row":
            where.append(text)
        elif kind == "agg":
            having.append(text)
    return {"where": where, "having": having}
""",
    [
        {"clauses": [["status = open", "row"], ["COUNT(*) > 2", "agg"]]},
        {"clauses": []},
        {"clauses": [["a", "row"], ["b", "row"]]},
        {"clauses": [["nope", "other"], ["c", "agg"]]},
    ],
)

add(
    "python-ex-guarded-transfer",
    "Guarded Transfer",
    "medium",
    ["python", "sqlite"],
    "Implement `solve(balance, amount)`. Apply a debit only when `amount` is positive and `balance` covers it. Return `{\"balance\": new_or_old, \"ledger\": 1 or 0}`. On success the balance shrinks and ledger is 1. On failure the balance is unchanged and ledger is 0.",
    ["A failed debit writes no ledger row", "Success writes one"],
    ["Check the amount and the balance.", "Subtract and set ledger to 1 only on success.", "Otherwise echo the balance and ledger 0."],
    "The transfer and the ledger insert commit together or not at all. A guard that updates zero rows must not insert a ledger line. Returning both the balance and the flag is the pair of tables after the transaction.",
    "O(1)", "O(1)",
    """
def solve(balance, amount):
    if type(amount) is int and amount > 0 and balance >= amount:
        return {"balance": balance - amount, "ledger": 1}
    return {"balance": balance, "ledger": 0}
""",
    [
        {"balance": 100, "amount": 40},
        {"balance": 30, "amount": 40},
        {"balance": 10, "amount": 0},
        {"balance": 10, "amount": 10},
    ],
)

add(
    "python-ex-placeholder-count",
    "Placeholder Count",
    "easy",
    ["python", "sqlite"],
    "Implement `solve(sql, params)`. Count question marks in `sql`. Return `ok` when the count equals `params`, and `mismatch` otherwise. Do not ignore question marks inside text. The tests have no quoted question marks.",
    ["Each ? is one placeholder", "params is the count you were given"],
    ["Count the character ?.", "Compare to params.", "Return ok or mismatch."],
    "A one-tuple needs a trailing comma, and a placeholder count that does not match the parameter sequence raises at execute time. Counting question marks against the length of the parameter list catches the bug before the driver does, for SQL that does not hide question marks in string literals.",
    "O(n)", "O(1)",
    """
def solve(sql, params):
    return "ok" if sql.count("?") == params else "mismatch"
""",
    [
        {"sql": "SELECT * FROM t WHERE id = ?", "params": 1},
        {"sql": "UPDATE t SET a = ? WHERE id = ?", "params": 1},
        {"sql": "SELECT 1", "params": 0},
        {"sql": "SELECT ?", "params": 2},
    ],
)

add(
    "python-ex-allow-sort",
    "Allow Sort",
    "medium",
    ["python", "sqlite"],
    "Implement `solve(choice, allowed)`. `allowed` maps a client sort key to a real column name. Return the column name when `choice` is a key. Return `error` when it is not. Do not return `choice` itself unless the mapping says so.",
    ["Unknown keys are error", "The mapped column is the SQL fragment"],
    ["Use the dict.", "A miss is error.", "A hit returns the column, which may differ from the key."],
    "ORDER BY cannot take a bound parameter for the column name. Interpolating the client's string is injection. An allow-list maps a public key to a column you wrote. Anything else is rejected. The mapped name is what you would splice in.",
    "O(1)", "O(1)",
    """
def solve(choice, allowed):
    if choice not in allowed:
        return "error"
    return allowed[choice]
""",
    [
        {"choice": "new", "allowed": {"new": "created_at", "name": "name"}},
        {"choice": "drop", "allowed": {"new": "created_at"}},
        {"choice": "name", "allowed": {"name": "name"}},
        {"choice": "", "allowed": {}},
    ],
)

add(
    "python-ex-fk-flag",
    "Foreign Key Flag",
    "easy",
    ["python", "sqlite"],
    "Implement `solve(pragma_on, bad_child)`. `pragma_on` is 1 when foreign keys were enabled. `bad_child` is 1 when the insert references a missing parent. Return `rejected` only when both are 1. Return `accepted` otherwise, including a bad child when the pragma is off.",
    ["SQLite does not enforce foreign keys until the pragma", "A good child is accepted"],
    ["Both flags must be 1 to reject.", "Any other combination accepts.", "Do not reject a valid child."],
    "SQLite leaves foreign_keys off unless every connection runs the pragma. A bad child insert then succeeds and the schema looks stricter than it is. Turning the pragma on makes the same insert fail. The two flags are that matrix.",
    "O(1)", "O(1)",
    """
def solve(pragma_on, bad_child):
    if pragma_on and bad_child:
        return "rejected"
    return "accepted"
""",
    [
        {"pragma_on": 1, "bad_child": 1},
        {"pragma_on": 0, "bad_child": 1},
        {"pragma_on": 1, "bad_child": 0},
        {"pragma_on": 0, "bad_child": 0},
    ],
)

add(
    "python-ex-query-count",
    "Query Count",
    "medium",
    ["python", "sqlalchemy"],
    "Implement `solve(parents, strategy)`. `strategy` is `lazy`, `selectin`, or `join`. Lazy runs 1 plus `parents` statements. Selectin runs 2 when parents is positive and 1 when parents is 0. Join runs 1. Any other strategy returns `error`. Negative parents returns `error`.",
    ["lazy grows with the page", "selectin stays flat"],
    ["Reject a negative page size.", "Branch on the three strategies.", "Unknown strategies are error."],
    "Lazy loading a collection inside a loop is the N+1 query. selectinload issues one follow-up query for the page. joinedload folds the children into the parent query, which is one statement and a different LIMIT story. The count is what you assert in a test so a later edit cannot bring the loop back quietly.",
    "O(1)", "O(1)",
    """
def solve(parents, strategy):
    if parents < 0:
        return "error"
    if strategy == "lazy":
        return 1 + parents
    if strategy == "selectin":
        return 2 if parents else 1
    if strategy == "join":
        return 1
    return "error"
""",
    [
        {"parents": 50, "strategy": "lazy"},
        {"parents": 50, "strategy": "selectin"},
        {"parents": 0, "strategy": "selectin"},
        {"parents": 3, "strategy": "join"},
    ],
)

add(
    "python-ex-guarded-balance",
    "Guarded Balance",
    "medium",
    ["python", "sqlalchemy"],
    "Implement `solve(balance, amount)`. Same debit guard as the SQL form: positive amount, sufficient balance, otherwise `conflict`. Success returns the new balance.",
    ["Insufficient funds are conflict", "Non-positive amounts are conflict"],
    ["Reject a bad amount as conflict.", "Reject a short balance as conflict.", "Otherwise subtract."],
    "Editing account.balance in Python from a value you loaded earlier is a lost update. The guarded UPDATE changes the row only when the current balance covers the debit. This function is that statement's result: a new balance or a conflict the caller turns into 409.",
    "O(1)", "O(1)",
    """
def solve(balance, amount):
    if type(amount) is not int or amount <= 0 or balance < amount:
        return "conflict"
    return balance - amount
""",
    [
        {"balance": 100, "amount": 40},
        {"balance": 10, "amount": 40},
        {"balance": 10, "amount": 0},
        {"balance": 5, "amount": 5},
    ],
)

add(
    "python-ex-unique-parents",
    "Unique Parents",
    "easy",
    ["python", "sqlalchemy"],
    "Implement `solve(ids)`. `ids` is a list of parent ids repeated once per joined child. Return the unique ids in first-seen order.",
    ["First-seen order", "Duplicates from the join collapse"],
    ["A seen set plus a result list.", "Append only the first time.", "Do not sort."],
    "joinedload of a collection repeats the parent row once per child in the raw result. unique() collapses those repeats. Forgetting it returns duplicate parents to the API. First-seen order matches the parent's order in the joined stream.",
    "O(n)", "O(n)",
    """
def solve(ids):
    seen = set()
    out = []
    for item in ids:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out
""",
    [
        {"ids": ["a", "a", "b", "a"]},
        {"ids": []},
        {"ids": ["a"]},
        {"ids": ["b", "a", "b"]},
    ],
)

add(
    "python-ex-session-scope",
    "Session Scope",
    "easy",
    ["python", "sqlalchemy"],
    "Implement `solve(lifetime)`. `lifetime` is `request` or `process`. Return `fresh` for a session that lives one request, and `stale` for a session that lives for the process. Any other word returns `error`.",
    ["A process-wide session can serve stale state", "A request session is fresh"],
    ["request returns fresh.", "process returns stale.", "Other values return error."],
    "The identity map returns the same instance for a primary key inside one session. A session that never closes keeps the object from an earlier request and can write it back over newer commits. Closing at the end of the request drops that cache. The process lifetime is the stale one.",
    "O(1)", "O(1)",
    """
def solve(lifetime):
    if lifetime == "request":
        return "fresh"
    if lifetime == "process":
        return "stale"
    return "error"
""",
    [
        {"lifetime": "request"},
        {"lifetime": "process"},
        {"lifetime": "thread"},
        {"lifetime": "request"},
    ],
)

add(
    "python-ex-python-gate",
    "Python Gate",
    "easy",
    ["python", "packaging"],
    "Implement `solve(major, minor)`. Return `ok` when the version is at least 3.12, and `reject` otherwise. Compare the pair, not a float.",
    ["3.12 is ok", "3.11 is reject"],
    ["Compare (major, minor) with (3, 12).", "Greater or equal is ok.", "Do not concatenate the numbers into 312."],
    "requires-python rejects an interpreter that is too old at install time. Comparing tuples avoids the trick where 3.9 would look larger than 3.12 if you compared strings poorly, and where 3.10 is not the float 3.1. The gate is the minimum the service is tested on.",
    "O(1)", "O(1)",
    """
def solve(major, minor):
    if (major, minor) >= (3, 12):
        return "ok"
    return "reject"
""",
    [
        {"major": 3, "minor": 12},
        {"major": 3, "minor": 11},
        {"major": 3, "minor": 13},
        {"major": 2, "minor": 7},
    ],
)

add(
    "python-ex-runtime-extra",
    "Runtime Extra",
    "easy",
    ["python", "packaging"],
    "Implement `solve(deps, dev_only)`. `deps` is the full list of package names. `dev_only` is the list that must stay out of the runtime image. Return the runtime names in the original order.",
    ["Order follows deps", "Dev tools are removed"],
    ["Build a set of the dev names.", "Keep deps that are not in it.", "Do not sort."],
    "The runtime image installs the project without the dev extra. pytest and ruff are not needed to serve traffic, and they widen the image. Filtering them out is the install line. The lockfile still pins them for CI.",
    "O(n)", "O(n)",
    """
def solve(deps, dev_only):
    skip = set(dev_only)
    return [name for name in deps if name not in skip]
""",
    [
        {"deps": ["fastapi", "pytest", "ruff"], "dev_only": ["pytest", "ruff"]},
        {"deps": ["fastapi"], "dev_only": ["pytest"]},
        {"deps": [], "dev_only": ["pytest"]},
        {"deps": ["a", "b"], "dev_only": []},
    ],
)

add(
    "python-ex-import-winner",
    "Import Winner",
    "medium",
    ["python", "packaging"],
    "Implement `solve(entries)`. `entries` is a list of path strings in sys.path order. Return the first entry that contains the substring `myapp`, or `missing` if none do. The first hit wins.",
    ["Earlier paths shadow later ones", "missing when the package is absent"],
    ["Walk from the left.", "Return the first path containing myapp.", "If the loop ends, return missing."],
    "sys.path is searched in order. A checkout directory earlier than site-packages imports the checkout, which is how a laptop and a container disagree. The winner is the first entry that can provide the package. Later copies are invisible.",
    "O(n)", "O(1)",
    """
def solve(entries):
    for entry in entries:
        if "myapp" in entry:
            return entry
    return "missing"
""",
    [
        {"entries": ["/repo/src", "/venv/site-packages/myapp"]},
        {"entries": ["/usr", "/venv/myapp"]},
        {"entries": []},
        {"entries": ["myapp", "other"]},
    ],
)

add(
    "python-ex-script-entry",
    "Script Entry",
    "easy",
    ["python", "packaging"],
    "Implement `solve(spec)`. `spec` is `module:function`. Return `[module, function]`. If there is not exactly one colon, or either side is empty, return `error`.",
    ["Exactly one colon", "Both sides non-empty"],
    ["Split on colon once and check the remainder has none... or count colons.", "Reject empty sides.", "Return the two strings."],
    "A console script entry point is module:function. The installer builds a small launcher that imports the module and calls the function. A missing colon or an empty side is a broken pyproject table, and it should fail at packaging time rather than when a user runs the command.",
    "O(n)", "O(n)",
    """
def solve(spec):
    if spec.count(":") != 1:
        return "error"
    module, function = spec.split(":")
    if not module or not function:
        return "error"
    return [module, function]
""",
    [
        {"spec": "myapp.cli:main"},
        {"spec": "myapp.cli"},
        {"spec": ":main"},
        {"spec": "a:b:c"},
    ],
)

add(
    "python-ex-first-failure",
    "First Failure",
    "easy",
    ["python", "quality"],
    "Implement `solve(lint_ok, types_ok, tests_ok)`. Each flag is 0 or 1. Return `ruff` if lint failed, else `mypy` if types failed, else `pytest` if tests failed, else `pass`. The first failing stage is the one you report.",
    ["Lint is checked first", "pass requires all three"],
    ["A 0 lint flag returns ruff.", "Then types.", "Then tests. All ones return pass."],
    "The gate is ordered so the cheapest, most local failure is named first when you stop early. A pass is all three green. Reporting pytest when ruff already failed hides the formatting error the author should fix before reading a test log.",
    "O(1)", "O(1)",
    """
def solve(lint_ok, types_ok, tests_ok):
    if not lint_ok:
        return "ruff"
    if not types_ok:
        return "mypy"
    if not tests_ok:
        return "pytest"
    return "pass"
""",
    [
        {"lint_ok": 0, "types_ok": 1, "tests_ok": 1},
        {"lint_ok": 1, "types_ok": 0, "tests_ok": 1},
        {"lint_ok": 1, "types_ok": 1, "tests_ok": 0},
        {"lint_ok": 1, "types_ok": 1, "tests_ok": 1},
    ],
)

add(
    "python-ex-dev-image",
    "Dev Image",
    "easy",
    ["python", "quality"],
    "Implement `solve(names)`. Return the names that must stay out of the runtime image: `pytest`, `ruff`, and `mypy`, in the order they appear in `names`. Other names are omitted.",
    ["Only those three tools", "Keep input order"],
    ["Membership in the dev set.", "Walk names in order.", "Do not include fastapi."],
    "The production image installs the application, not the gate. pytest, ruff, and mypy belong in the dev extra and in CI. Shipping them does not make the service more correct. It makes the image larger and the attack surface wider.",
    "O(n)", "O(n)",
    """
def solve(names):
    dev = {"pytest", "ruff", "mypy"}
    return [name for name in names if name in dev]
""",
    [
        {"names": ["fastapi", "pytest", "ruff", "uvicorn", "mypy"]},
        {"names": ["fastapi"]},
        {"names": []},
        {"names": ["mypy", "mypy"]},
    ],
)

add(
    "python-ex-marker-strict",
    "Marker Strict",
    "medium",
    ["python", "quality"],
    "Implement `solve(mark, known)`. `known` is the list of registered pytest marks. Return `ok` when `mark` is in the list. Return `unknown` when it is not. A typo should not silently do nothing.",
    ["Exact match", "Empty known list rejects every mark"],
    ["Membership test.", "Return ok or unknown.", "Do not prefix-match."],
    "pytest can warn or fail on an unregistered mark. Strict markers turn a typo in a skip or an integration mark into a failed collection instead of a test that always runs. The known list is the registry in pyproject.",
    "O(n)", "O(1)",
    """
def solve(mark, known):
    return "ok" if mark in known else "unknown"
""",
    [
        {"mark": "integration", "known": ["integration", "slow"]},
        {"mark": "integation", "known": ["integration"]},
        {"mark": "slow", "known": []},
        {"mark": "slow", "known": ["slow"]},
    ],
)

add(
    "python-ex-venv-cache",
    "Cache Key",
    "medium",
    ["python", "quality"],
    "Implement `solve(cached_lock, new_lock)`. Both are lockfile hashes. Return `reuse` when they are equal and non-empty. Return `rebuild` when they differ or either is empty.",
    ["An empty hash never reuses", "Equal hashes reuse"],
    ["Reject empty strings.", "Equal non-empty hashes return reuse.", "Everything else rebuilds."],
    "A CI cache of the virtualenv is safe only when the lockfile that produced it is the lockfile you have now. Keying the cache on the lock hash makes a dependency bump rebuild. Reusing a cache from a different lock tests the old graph and can go green for the wrong reason.",
    "O(n)", "O(1)",
    """
def solve(cached_lock, new_lock):
    if cached_lock and cached_lock == new_lock:
        return "reuse"
    return "rebuild"
""",
    [
        {"cached_lock": "abc", "new_lock": "abc"},
        {"cached_lock": "abc", "new_lock": "def"},
        {"cached_lock": "", "new_lock": ""},
        {"cached_lock": "abc", "new_lock": ""},
    ],
)
