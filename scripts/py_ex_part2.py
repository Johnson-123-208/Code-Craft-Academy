"""Practice problems for module 04 functions."""
from __future__ import annotations

from py_ex_build import add

add(
    "python-ex-safe-append",
    "Safe Append",
    "easy",
    ["python", "functions"],
    "Implement `solve(items, value)`. `items` is either the string `none` or a list. When it is `none`, start from a fresh list. Append `value` and return the list. A missing list must not be confused with a list the caller already owns: you only allocate when the argument is the token `none`.",
    ["none means the caller passed no list", "value is an integer"],
    [
        "If items is the string none, use a new empty list.",
        "Otherwise copy the incoming list so you do not mutate the caller's object, then append.",
        "Return the list that received the append.",
    ],
    "A default argument of [] is shared across calls. The safe pattern is a default of None and a new list inside the function. Here none is the token for that missing argument. Copying a provided list keeps this function from mutating a list the judge still holds.",
    "O(n)",
    "O(n)",
    """
def solve(items, value):
    base = [] if items == "none" else list(items)
    base.append(value)
    return base
""",
    [
        {"items": "none", "value": 1},
        {"items": [1, 2], "value": 3},
        {"items": "none", "value": 0},
        {"items": [], "value": 4},
    ],
)

add(
    "python-ex-bind-call",
    "Keyword Flags",
    "easy",
    ["python", "functions"],
    "Implement `solve(bound)`. `bound` is a dict of the names a call actually bound: it always contains `verbose` and `dry_run`, each 0 or 1, and it contains `label` only when the caller passed it. Return `{\"verbose\": ..., \"dry_run\": ..., \"label\": ...}`. The label is the string `none` when it was omitted. This is the shape of a function that forces flags to be keyword-only: the mapping is the bound arguments, not a positional pile.",
    ["verbose and dry_run are always present", "A missing label key means the string none"],
    [
        "Read verbose and dry_run directly.",
        "Use bound.get(\"label\", \"none\") for the optional name.",
        "Do not invent defaults other than none for the label.",
    ],
    "Keyword-only parameters stop a caller from passing a boolean in the wrong slot. After the call is bound, the function sees names, not positions. The omitted label is a missing key, reported as the token none so a test can see the difference between omitted and an empty label.",
    "O(1)",
    "O(1)",
    """
def solve(bound):
    return {
        "verbose": bound["verbose"],
        "dry_run": bound["dry_run"],
        "label": bound.get("label", "none"),
    }
""",
    [
        {"bound": {"verbose": 1, "dry_run": 0, "label": "nightly"}},
        {"bound": {"verbose": 0, "dry_run": 1}},
        {"bound": {"verbose": 0, "dry_run": 0, "label": ""}},
        {"bound": {"verbose": 1, "dry_run": 1}},
    ],
)

add(
    "python-ex-merge-options",
    "Forward Options",
    "medium",
    ["python", "functions"],
    "Implement `solve(base, overrides)`. Both are flat dicts of string keys to string values. Return a new dict with every key from either side. When a key is in both, the override wins. Do not drop keys that appear only in overrides. Do not mutate the inputs.",
    ["Values are strings", "Overrides replace base on the same key"],
    [
        "Copy base, then update with overrides. dict unpacking in that order does the same thing.",
        "Keys only in overrides must survive.",
        "Return a new dict.",
    ],
    "Forwarding **options is a merge, not a filter. The callee's explicit arguments should win over defaults, and unexpected keys are the caller's data unless the function is documented to reject them. This merge is last-write-wins with overrides last.",
    "O(n + m)",
    "O(n + m)",
    """
def solve(base, overrides):
    merged = dict(base)
    merged.update(overrides)
    return merged
""",
    [
        {"base": {"host": "localhost", "port": "80"}, "overrides": {"port": "443"}},
        {"base": {"a": "1"}, "overrides": {"b": "2"}},
        {"base": {}, "overrides": {"a": "1"}},
        {"base": {"a": "1"}, "overrides": {}},
    ],
)

add(
    "python-ex-scope-read",
    "Unbound Local",
    "medium",
    ["python", "scope"],
    "Implement `solve(assigns, read_before)`. Both strings are `yes` or `no`. `assigns` is `yes` when the function assigns to the name anywhere in its body. `read_before` is `yes` when the read happens before that assignment. Return `error` when the name is assigned anywhere and the read happens before the assignment (UnboundLocalError). Return `local` when the name is assigned and the read happens after the assignment. Return `global` when the function never assigns the name.",
    ["Inputs are yes or no", "Any assignment in the function makes the name local for the whole function"],
    [
        "If the function never assigns, the read is global.",
        "If it assigns and the read is first, the result is error.",
        "If it assigns and the read is after, the result is local.",
    ],
    "Python decides that a name is local if any assignment to it exists in the function, including an assignment that has not run yet. A read of that name before the assignment raises UnboundLocalError instead of falling through to the global. No assignment at all means the read uses the global.",
    "O(1)",
    "O(1)",
    """
def solve(assigns, read_before):
    if assigns == "no":
        return "global"
    if read_before == "yes":
        return "error"
    return "local"
""",
    [
        {"assigns": "yes", "read_before": "yes"},
        {"assigns": "yes", "read_before": "no"},
        {"assigns": "no", "read_before": "yes"},
        {"assigns": "no", "read_before": "no"},
    ],
)

add(
    "python-ex-min-max",
    "Multi Return",
    "easy",
    ["python", "functions"],
    "Implement `solve(items)`. `items` is a list of integers. If it is empty, return the string `error`. Otherwise return `[minimum, maximum]` of the values. One pass is enough. Do not sort.",
    ["Empty input is the string error", "A one-element list returns that value twice"],
    [
        "Reject the empty list before you index it.",
        "Track low and high while you scan.",
        "Return a two-element list, not two separate results the caller cannot see.",
    ],
    "A function can return several numbers by returning one list. The empty case has no minimum, so it is an error rather than a silent zero. Scanning once beats sorting when you only need the two extremes.",
    "O(n)",
    "O(1)",
    """
def solve(items):
    if not items:
        return "error"
    low = high = items[0]
    for item in items[1:]:
        if item < low:
            low = item
        if item > high:
            high = item
    return [low, high]
""",
    [
        {"items": [3, 1, 2]},
        {"items": []},
        {"items": [5]},
        {"items": [-1, -4, 0]},
    ],
)

add(
    "python-ex-fresh-default",
    "Once Default",
    "medium",
    ["python", "functions"],
    "Implement `solve(captured, fresh)`. Both are integer timestamps. A default argument captured `captured` when the function was defined. A correct call reads `fresh` at call time. Return `{\"stale\": captured, \"live\": fresh, \"same\": 1 or 0}` where `same` is 1 when the two numbers are equal. The stale value is what a mutable or early-bound default would keep serving.",
    ["Both inputs are integers", "same is 0 or 1"],
    [
        "Echo both numbers. Do not replace one with the other.",
        "same is 1 only when they compare equal.",
        "The point of the function is to show the captured value surviving a later fresh read.",
    ],
    "Default expressions run once, at function definition. A timestamp default therefore freezes the first value. Reading the clock inside the body gets the live value. Returning both makes the staleness visible instead of hiding it behind a single number.",
    "O(1)",
    "O(1)",
    """
def solve(captured, fresh):
    return {"stale": captured, "live": fresh, "same": 1 if captured == fresh else 0}
""",
    [
        {"captured": 10, "fresh": 15},
        {"captured": 10, "fresh": 10},
        {"captured": 0, "fresh": 1},
        {"captured": 4, "fresh": 4},
    ],
)

add(
    "python-ex-counter",
    "Counter",
    "easy",
    ["python", "closures"],
    "Implement `solve(ops)`. `ops` is a list of `inc`, `reset`, or `read`. A closure starts at 0. `inc` adds 1. `reset` sets the value back to 0. `read` does not change it. Return the list of values after each operation, including reads.",
    ["The counter starts at 0", "Return one integer per operation"],
    [
        "Keep the integer in a variable the loop closes over. A list cell works if you want a mutable binding.",
        "Apply each op, then append the current value.",
        "reset goes to 0, not to the previous value.",
    ],
    "A closure counter is a function plus a cell it can write. The operations are the calls. Recording the value after every call is what a test can see, since the function object itself is not a JSON result.",
    "O(n)",
    "O(n)",
    """
def solve(ops):
    value = 0
    out = []
    for op in ops:
        if op == "inc":
            value += 1
        elif op == "reset":
            value = 0
        out.append(value)
    return out
""",
    [
        {"ops": ["inc", "inc", "read", "reset", "read"]},
        {"ops": ["read"]},
        {"ops": ["reset", "inc"]},
        {"ops": ["inc", "reset", "inc", "inc"]},
    ],
)

add(
    "python-ex-loop-snapshot",
    "Loop Snapshot",
    "medium",
    ["python", "closures"],
    "Implement `solve(n)`. Return a list of `n` integers `0, 1, ..., n-1`. This is the result of calling `n` functions created in a loop, each of which captured its own index. The bug to avoid is every function returning `n` or `n-1`. `n` may be 0.",
    ["n is a non-negative integer", "Each index is captured separately"],
    [
        "Build the functions with a default argument, `lambda i=i: i`, or append i into a new cell each iteration.",
        "Call them after the loop.",
        "The results are 0 through n-1, not the final loop variable.",
    ],
    "A lambda that reads the loop variable looks up that variable when it is called, which is after the loop has finished. Binding the current integer as a default argument, or storing it in a new list cell, snapshots the value from that iteration. Calling the functions then yields 0 through n-1.",
    "O(n)",
    "O(n)",
    """
def solve(n):
    fns = []
    for i in range(n):
        fns.append((lambda i=i: i))
    return [fn() for fn in fns]
""",
    [
        {"n": 3},
        {"n": 0},
        {"n": 1},
        {"n": 4},
    ],
)

add(
    "python-ex-adder",
    "Adder",
    "easy",
    ["python", "closures"],
    "Implement `solve(offset, values)`. Return a list of `offset + value` for each integer in `values`. `offset` may be 0 or negative. This is a factory that captured `offset` and was then called on each value.",
    ["offset is an integer", "Keep input order"],
    [
        "The offset is fixed for the whole call.",
        "Add it to each value. Do not multiply.",
        "An empty values list returns an empty list.",
    ],
    "A closure factory returns a function that already knows its offset. Applying that function to each value is the list this problem returns. Zero is a meaningful offset: every result equals the input value, which is how you know the offset was added and not ignored.",
    "O(n)",
    "O(n)",
    """
def solve(offset, values):
    def add(value):
        return offset + value
    return [add(value) for value in values]
""",
    [
        {"offset": 2, "values": [1, 2, 3]},
        {"offset": 0, "values": [5]},
        {"offset": -1, "values": [1, 0]},
        {"offset": 3, "values": []},
    ],
)

add(
    "python-ex-shared-cell",
    "Shared Cell",
    "medium",
    ["python", "closures"],
    "Implement `solve(ops)`. Two operations share one integer cell, starting at 0. `inc` adds 1. `read` leaves it unchanged. Return the list of cell values after each operation. An increment must be visible to a later read, which is the point of one cell rather than two copies.",
    ["ops contains inc and read", "The cell starts at 0"],
    [
        "One variable is the cell. Both operations close over it.",
        "inc changes it. read only reports it.",
        "Append the value after every operation.",
    ],
    "Two functions that close over the same variable see the same writes. If each call created a new integer, a read would stay at 0 after increments. The shared cell is what makes the sequence cumulative.",
    "O(n)",
    "O(n)",
    """
def solve(ops):
    cell = [0]

    def inc():
        cell[0] += 1

    def read():
        return cell[0]

    out = []
    for op in ops:
        if op == "inc":
            inc()
        out.append(read())
    return out
""",
    [
        {"ops": ["read", "inc", "inc", "read"]},
        {"ops": ["inc"]},
        {"ops": ["read"]},
        {"ops": ["inc", "read", "inc"]},
    ],
)

add(
    "python-ex-capture-id",
    "Capture Id",
    "medium",
    ["python", "closures"],
    "Implement `solve(ids, queries)`. `ids` is a list of strings. Build one predicate per id that matches only that id, capturing the id at creation time. `queries` is a list of strings. Return a list of 0/1 values, one per query, where the value is 1 when any captured predicate matches the query. Predicates must not all match only the last id.",
    ["Matching is exact string equality", "Return 0 or 1 per query"],
    [
        "Create each predicate with a default argument bound to the current id.",
        "A query matches if any predicate returns true.",
        "An id that never appears in ids matches nothing.",
    ],
    "The late-binding bug makes every predicate close over the final loop variable, so only the last id matches. Binding `id=id` on each function stores the string from that iteration. A query then asks the set of captured ids, which is also what a set would answer. The predicates are the point.",
    "O(n + q)",
    "O(n)",
    """
def solve(ids, queries):
    preds = []
    for item in ids:
        preds.append((lambda query, item=item: query == item))
    out = []
    for query in queries:
        out.append(1 if any(pred(query) for pred in preds) else 0)
    return out
""",
    [
        {"ids": ["a", "b"], "queries": ["a", "b", "c"]},
        {"ids": ["a", "a"], "queries": ["a", "b"]},
        {"ids": [], "queries": ["a"]},
        {"ids": ["z"], "queries": ["z"]},
    ],
)

add(
    "python-ex-call-count",
    "Call Count",
    "medium",
    ["python", "decorators"],
    "Implement `solve(times)`. A wrapper counts how many times it is entered. Call it `times` times and return the count. `times` may be 0, which returns 0. The wrapped function does nothing visible. The count is the decorator's state.",
    ["times is a non-negative integer", "Each call adds exactly 1"],
    [
        "A list cell or nonlocal integer holds the count.",
        "The wrapper increments, then calls the inner function.",
        "Return the count after the loop, not a list of partial counts.",
    ],
    "A counting decorator wraps the call. The counter lives in the wrapper's closure, not on the inner function, unless you attach it there on purpose. Calling the wrapper times times yields the integer times, including zero when you never enter it.",
    "O(times)",
    "O(1)",
    """
def solve(times):
    count = [0]

    def wrapped():
        count[0] += 1

    for _ in range(times):
        wrapped()
    return count[0]
""",
    [
        {"times": 3},
        {"times": 0},
        {"times": 1},
        {"times": 5},
    ],
)

add(
    "python-ex-repeat-last",
    "Repeat Last",
    "medium",
    ["python", "decorators"],
    "Implement `solve(value, times)`. Call an inner function `times` times. The inner function returns `value` plus the zero-based call index, so the results are `value, value+1, ...`. Return the last result. If `times` is 0, return the string `error` because there is no last result. Also return the wrapper name as the second list element: the list is `[last, \"wrapped\"]`.",
    ["times is a non-negative integer", "The name is the string wrapped"],
    [
        "Reject times less than 1 with the string error. Return that string alone, not a list.",
        "Otherwise keep only the latest return value while you loop.",
        "The second element of a successful result is the wrapper's __name__, which you set to wrapped.",
    ],
    "A decorator that calls the inner function several times still has one return value: the last one, unless it is documented to collect them. functools.wraps would preserve the inner name. This wrapper is named wrapped so the test can see that the name is part of the decorator's contract, not an accident.",
    "O(times)",
    "O(1)",
    """
def solve(value, times):
    def inner(index):
        return value + index

    def wrapped():
        last = "error"
        for index in range(times):
            last = inner(index)
        return last

    wrapped.__name__ = "wrapped"
    if times < 1:
        return "error"
    return [wrapped(), wrapped.__name__]
""",
    [
        {"value": 10, "times": 3},
        {"value": 10, "times": 0},
        {"value": 0, "times": 1},
        {"value": -2, "times": 2},
    ],
)

add(
    "python-ex-require-positive",
    "Require Positive",
    "medium",
    ["python", "decorators"],
    "Implement `solve(values)`. A parameterized check rejects any integer that is less than or equal to 0 before the work runs. For each value, return `ok` if it is a positive integer and `reject` otherwise. Booleans are not in the input. Return the list of those words.",
    ["values is a list of integers", "Zero is not positive"],
    [
        "The check happens before you would call the wrapped function.",
        "value > 0 is the accept condition.",
        "Do not treat negative numbers as ok by taking abs.",
    ],
    "A parameterized decorator is a function that takes the bound, here the positive rule, and returns the real decorator. The wrapper refuses the argument and never calls the inner function. The result list is the decision for each argument.",
    "O(n)",
    "O(n)",
    """
def solve(values):
    def accept(value):
        if type(value) is int and value > 0:
            return "ok"
        return "reject"
    return [accept(value) for value in values]
""",
    [
        {"values": [1, 0, -3, 4]},
        {"values": [1]},
        {"values": [0]},
        {"values": []},
    ],
)

add(
    "python-ex-decorator-order",
    "Wraps Chain",
    "easy",
    ["python", "decorators"],
    "Implement `solve(names)`. `names` is the decorator stack written top to bottom, the same order as `@` lines above a function. The top decorator is the first name. On a call, the outermost wrapper runs first, and that outermost wrapper is the bottom decorator in the source, because it was applied last. Return the names in the order they run on the way in: bottom of the source list first, ending with the top of the source list.",
    ["names[0] is the top decorator in source", "Return the call order on the way in"],
    [
        "Decorators apply from the function upward, so the bottom source name is outermost.",
        "The call enters the outermost wrapper first.",
        "Reversing the source list is the call order.",
    ],
    "Application order is bottom-up. Call order on the way in is outside-in, which is the reverse of the source list when index 0 is the top line. Forgetting the reverse is the usual explanation of a trace that prints the inner wrapper first.",
    "O(n)",
    "O(n)",
    """
def solve(names):
    return list(reversed(names))
""",
    [
        {"names": ["log", "auth"]},
        {"names": ["only"]},
        {"names": []},
        {"names": ["a", "b", "c"]},
    ],
)

add(
    "python-ex-retry-tags",
    "Retry Transient",
    "medium",
    ["python", "decorators"],
    "Implement `solve(attempts, tag, limit)`. `attempts` is a list of result tags in order. Retry only while the tag equals `tag`, and stop after `limit` tries. Return the first tag that is not the retryable one, or the last tag you actually tried if every try was retryable. `limit` is the maximum number of attempts, not the number of extra retries.",
    ["limit is at least 1 in the successful-path tests, and may be 0", "A limit of 0 returns the string error"],
    [
        "If limit is less than 1, return error.",
        "Walk attempts, but never more than limit of them.",
        "Return immediately when the tag is not the retryable tag.",
    ],
    "A retry decorator that retries every exception will retry a ValueError the caller caused. Filtering on one tag, and capping the attempts, is the policy. The returned tag is the one the caller would observe: the first permanent result, or the final transient failure if the budget ends there.",
    "O(limit)",
    "O(1)",
    """
def solve(attempts, tag, limit):
    if limit < 1:
        return "error"
    seen = "error"
    for index, result in enumerate(attempts):
        if index == limit:
            break
        seen = result
        if result != tag:
            return result
    return seen
""",
    [
        {"attempts": ["timeout", "timeout", "ok"], "tag": "timeout", "limit": 3},
        {"attempts": ["timeout", "ok"], "tag": "timeout", "limit": 1},
        {"attempts": ["busy", "busy"], "tag": "busy", "limit": 2},
        {"attempts": ["ok"], "tag": "timeout", "limit": 0},
    ],
)

add(
    "python-ex-countdown",
    "Countdown",
    "easy",
    ["python", "generators"],
    "Implement `solve(n)`. Return a list of the integers a countdown generator would yield: `n, n-1, ..., 1`. If `n` is less than 1, return an empty list. Do not include 0.",
    ["n is an integer", "Descending order"],
    [
        "range(n, 0, -1) is the sequence.",
        "A non-positive n yields nothing.",
        "Return a list so the judge can see the yields.",
    ],
    "A generator yields one integer at a time and stops before 0. Materializing it with list() is the caller's choice. The producer itself should not prebuild the list if you write it as a generator. The values are the same either way.",
    "O(n)",
    "O(n)",
    """
def solve(n):
    def countdown(start):
        while start >= 1:
            yield start
            start -= 1
    return list(countdown(n))
""",
    [
        {"n": 3},
        {"n": 1},
        {"n": 0},
        {"n": -2},
    ],
)

add(
    "python-ex-unique-yield",
    "Unique Yield",
    "medium",
    ["python", "generators"],
    "Implement `solve(items)`. Yield the first occurrence of each string and return those yields as a list, in order. Later duplicates disappear. The producer may keep a set of seen values. It must not need the full output list in order to decide the next yield.",
    ["items is a list of strings", "First-seen order"],
    [
        "A set records what you have already yielded.",
        "Yield, or append to the result, only when the item is new.",
        "Do not sort. Order is appearance order.",
    ],
    "A generator can remember seen keys without storing the output. The caller materializes the yields. Sorting first would group duplicates and destroy first-seen order, which is a different function from unique-in-order.",
    "O(n)",
    "O(u)",
    """
def solve(items):
    def unique(source):
        seen = set()
        for item in source:
            if item in seen:
                continue
            seen.add(item)
            yield item
    return list(unique(items))
""",
    [
        {"items": ["a", "b", "a", "c", "b"]},
        {"items": []},
        {"items": ["a", "a"]},
        {"items": ["b", "a"]},
    ],
)

add(
    "python-ex-flatten-yield",
    "Flatten Yield",
    "easy",
    ["python", "generators"],
    "Implement `solve(rows)`. `rows` is a list of lists of integers. Yield every inner item once, in order, and return the list of yields. Do not flatten further. Empty inner lists contribute nothing.",
    ["One level only", "Keep order"],
    [
        "For each inner list, yield from it or loop and yield each item.",
        "Do not wrap items in another list.",
        "Materialize at the end for the return value.",
    ],
    "yield from walks an inner iterable and yields its items one by one. That is one-level flatten as a generator. Building the full list inside the producer throws away the reason to yield. The returned list is the caller's materialization.",
    "O(n)",
    "O(n)",
    """
def solve(rows):
    def flat(source):
        for row in source:
            yield from row
    return list(flat(rows))
""",
    [
        {"rows": [[1, 2], [], [3]]},
        {"rows": []},
        {"rows": [[4]]},
        {"rows": [[1], [2, 2]]},
    ],
)

add(
    "python-ex-first-above",
    "First Above",
    "easy",
    ["python", "generators"],
    "Implement `solve(items, limit)`. Return the first integer strictly greater than `limit`. If none exists, return the string `none`. Stop at the first hit. Later larger values do not matter.",
    ["items is a list of integers", "The comparison is strict"],
    [
        "Walk from the left.",
        "Return the item as soon as it is greater than limit.",
        "If the loop ends, return the string none.",
    ],
    "A generator that yields until a condition fails is takewhile. This function is the dual: the first success. Scanning the rest of the list after a hit cannot change the answer and is the bug when the tail is expensive.",
    "O(n)",
    "O(1)",
    """
def solve(items, limit):
    for item in items:
        if item > limit:
            return item
    return "none"
""",
    [
        {"items": [1, 4, 9], "limit": 3},
        {"items": [1, 2], "limit": 5},
        {"items": [], "limit": 0},
        {"items": [3, 3, 4], "limit": 3},
    ],
)

add(
    "python-ex-windows",
    "Window",
    "medium",
    ["python", "generators"],
    "Implement `solve(items, k)`. Return every contiguous window of length `k` as a list of lists. Windows overlap and step by 1. If `k` is less than 1 or greater than the length, return an empty list. Each window is a new list.",
    ["k is an integer", "Items are integers"],
    [
        "The number of windows is len(items) - k + 1 when k is valid.",
        "Slice items[i:i+k] for each start.",
        "Reject a non-positive k before you slice.",
    ],
    "Overlapping windows are a sliding slice. A generator can yield one slice at a time. Copying each slice matters because a later mutation of a shared buffer would corrupt earlier windows. An illegal k yields nothing rather than a partial tail.",
    "O(n*k)",
    "O(n*k)",
    """
def solve(items, k):
    if k < 1 or k > len(items):
        return []
    return [list(items[i:i + k]) for i in range(len(items) - k + 1)]
""",
    [
        {"items": [1, 2, 3, 4], "k": 2},
        {"items": [1, 2, 3], "k": 3},
        {"items": [1, 2], "k": 0},
        {"items": [1], "k": 2},
    ],
)

add(
    "python-ex-pipeline",
    "Pipeline",
    "medium",
    ["python", "generators"],
    "Implement `solve(words)`. Normalize by stripping and lowercasing, then drop blanks. Return the remaining words in order. Do the work as two stages: a normalize stage and a drop-blank stage. The result is what the caller sees after composing them.",
    ["words is a list of strings", "Empty after strip is dropped"],
    [
        "First stage: strip and lower each word, including ones that become empty.",
        "Second stage: skip empty strings.",
        "Do not drop before lowercasing. The case fold happens on the stripped text.",
    ],
    "Two generators compose by iteration: the second pulls from the first. Mixing both decisions into one loop is shorter and harder to reuse. The tests check the composition, including a word that is only spaces and a word whose case changes.",
    "O(n)",
    "O(n)",
    """
def solve(words):
    def normalize(source):
        for word in source:
            yield word.strip().lower()

    def drop_blank(source):
        for word in source:
            if word:
                yield word

    return list(drop_blank(normalize(words)))
""",
    [
        {"words": [" Ada ", " ", "GRACE"]},
        {"words": []},
        {"words": ["  "]},
        {"words": ["A", "b"]},
    ],
)

add(
    "python-ex-sort-key",
    "Sort Key",
    "easy",
    ["python", "sorting"],
    "Implement `solve(words)`. Return the words sorted by length ascending, and by the word itself ascending when lengths tie. The sort must be the tuple key `(len(word), word)`.",
    ["words is a list of strings", "Sorting is stable, and the tuple makes the tie explicit"],
    [
        "Use sorted with key=lambda word: (len(word), word).",
        "Do not sort by length only and hope the original order matches the tests. The tests include ties whose alphabetical order differs from input order.",
        "Return a new list.",
    ],
    "A tuple key compares the first field and only then the second. That is length, then the string. Two sorts in the right order also work because sorted is stable, but the tuple is one comparison and does not depend on you remembering which sort runs last.",
    "O(n log n)",
    "O(n)",
    """
def solve(words):
    return sorted(words, key=lambda word: (len(word), word))
""",
    [
        {"words": ["bb", "a", "b", "aa"]},
        {"words": []},
        {"words": ["a"]},
        {"words": ["ccc", "a", "bb"]},
    ],
)

add(
    "python-ex-top-score",
    "Top Score",
    "medium",
    ["python", "sorting"],
    "Implement `solve(rows)`. `rows` is a list of `[name, score]` pairs, scores integers, names strings. Return the name with the highest score. Break ties by the name that is smallest in dictionary order. The list is non-empty.",
    ["At least one row", "Higher score wins. Then smaller name."],
    [
        "The sort key is (-score, name) if you sort ascending, so the first row is the winner.",
        "Or track the best pair while you scan, replacing on a higher score or an equal score with a smaller name.",
        "Return the name, not the row.",
    ],
    "Negating the score turns a maximum into the first position of an ascending sort, and the name is the tie break in the same tuple. A scan does the same comparison without allocating a sorted copy. Both are correct. The tie is the part a max() on score alone gets wrong.",
    "O(n)",
    "O(1)",
    """
def solve(rows):
    best_name, best_score = rows[0]
    for name, score in rows[1:]:
        if score > best_score or (score == best_score and name < best_name):
            best_name, best_score = name, score
    return best_name
""",
    [
        {"rows": [["ada", 10], ["grace", 12], ["lin", 12]]},
        {"rows": [["zoe", 1], ["amy", 1]]},
        {"rows": [["only", 0]]},
        {"rows": [["b", 5], ["a", 4], ["c", 5]]},
    ],
)

add(
    "python-ex-clamp-factory",
    "Clamp Factory",
    "easy",
    ["python", "closures"],
    "Implement `solve(low, high, values)`. The bounds are closed over by a clamp function. Return the clamped `values`. If `low` is greater than `high`, return the string `error` and do not clamp. Each value below `low` becomes `low`, each value above `high` becomes `high`, and interior values stay.",
    ["Bounds are integers", "values is a list of integers"],
    [
        "Check the bounds once, before the loop.",
        "The inner function reads low and high from the enclosing scope.",
        "Apply it to every value.",
    ],
    "A factory returns a function that already knows its bounds, which is what you want when the same clamp is applied to a stream. Checking the bounds once avoids repeating a configuration error on every value. The map over values is the call list.",
    "O(n)",
    "O(n)",
    """
def solve(low, high, values):
    if low > high:
        return "error"

    def clamp(value):
        if value < low:
            return low
        if value > high:
            return high
        return value

    return [clamp(value) for value in values]
""",
    [
        {"low": 0, "high": 10, "values": [-1, 3, 20]},
        {"low": 5, "high": 4, "values": [1]},
        {"low": 1, "high": 1, "values": [0, 1, 2]},
        {"low": 0, "high": 2, "values": []},
    ],
)

add(
    "python-ex-stable-dept",
    "Stable Names",
    "medium",
    ["python", "sorting"],
    "Implement `solve(rows)`. `rows` is a list of `[name, dept]`. Return the rows sorted by department ascending, preserving the original order of rows that share a department. Python's sort is stable. Sort only by department.",
    ["Do not sort by name inside a department", "Return new row lists"],
    [
        "sorted(rows, key=lambda row: row[1]) is enough because the sort is stable.",
        "Copy each row so the result lists are new.",
        "A second key on name would break the original-order requirement.",
    ],
    "Stability means equal keys keep the order they had in the input. Sorting only by department therefore keeps the original name order inside a department. Adding the name as a second key is a different spec and fails that test.",
    "O(n log n)",
    "O(n)",
    """
def solve(rows):
    ordered = sorted(rows, key=lambda row: row[1])
    return [list(row) for row in ordered]
""",
    [
        {"rows": [["b", "eng"], ["a", "eng"], ["c", "design"]]},
        {"rows": [["a", "z"], ["b", "a"]]},
        {"rows": [["only", "eng"]]},
        {"rows": []},
    ],
)

add(
    "python-ex-score-name",
    "Negate Score",
    "medium",
    ["python", "sorting"],
    "Implement `solve(rows)`. `rows` is a list of `[name, score]`. Return the rows sorted by score descending, then by name ascending. Use one tuple key. Do not sort twice unless the directions are both ascending after you transform the score.",
    ["Higher score comes first", "Names break ties ascending"],
    [
        "The key (-score, name) sorts ascending into the order you want.",
        "Negating the score is what flips that field.",
        "Return copies of the rows in the sorted order.",
    ],
    "sorted is ascending. A descending score is an ascending negated score. The name stays unnegated so ties go from a to z. One key keeps the two directions from fighting across two sorts.",
    "O(n log n)",
    "O(n)",
    """
def solve(rows):
    ordered = sorted(rows, key=lambda row: (-row[1], row[0]))
    return [list(row) for row in ordered]
""",
    [
        {"rows": [["ada", 10], ["grace", 12], ["lin", 12]]},
        {"rows": [["b", 1], ["a", 1]]},
        {"rows": [["a", 0]]},
        {"rows": []},
    ],
)

add(
    "python-ex-factorial",
    "Factorial Loop",
    "easy",
    ["python", "recursion"],
    "Implement `solve(n)`. Return `n!` for a non-negative integer, with `0! = 1`. If `n` is negative, return the string `error`. Use a loop, not recursion. The tests pass integers only.",
    ["0! is 1", "Negatives are error"],
    [
        "Reject n < 0.",
        "Start the product at 1 and multiply 1 through n.",
        "A loop of length n is enough. Do not call yourself.",
    ],
    "Factorial of n is a product, and the product of no terms is 1, which is why 0! is 1. A loop uses constant stack. Recursion here would spend a frame per factor and adds nothing once the recurrence is this simple. Negatives are not in the function's domain.",
    "O(n)",
    "O(1)",
    """
def solve(n):
    if n < 0:
        return "error"
    product = 1
    for factor in range(2, n + 1):
        product *= factor
    return product
""",
    [
        {"n": 5},
        {"n": 0},
        {"n": 1},
        {"n": -1},
    ],
)

add(
    "python-ex-flatten-nested",
    "Flatten Nested",
    "medium",
    ["python", "recursion"],
    "Implement `solve(value)`. `value` is a tree of lists. Lists may contain integers or further lists. Strings are not used. Return one flat list of the integers in left-to-right order. An integer at the top level is a one-element list. An empty list returns an empty list.",
    ["Leaves are integers", "Order is preorder of the leaves"],
    [
        "If the value is a list, extend the result with a recursive flatten of each child.",
        "If the value is an int, it is a leaf.",
        "Do not flatten by assuming a fixed depth.",
    ],
    "The type test is the recursion structure: a list is an internal node and an int is a leaf. A one-level comprehension stops too early on a nested list. The base case is the integer, not the empty list. The empty list simply contributes no children.",
    "O(n)",
    "O(d)",
    """
def solve(value):
    if type(value) is int:
        return [value]
    out = []
    for child in value:
        out.extend(solve(child))
    return out
""",
    [
        {"value": [1, [2, [3]], 4]},
        {"value": []},
        {"value": 5},
        {"value": [[], [1]]},
    ],
)

add(
    "python-ex-nested-sum",
    "Recursive Sum",
    "easy",
    ["python", "recursion"],
    "Implement `solve(value)`. Sum every integer in a nested list. An integer returns itself. An empty list returns 0. Lists contain only integers and lists.",
    ["Leaves are integers", "Empty sums to 0"],
    [
        "The integer case returns the integer.",
        "The list case returns the sum of the recursive results.",
        "Do not use a global accumulator you forget to reset.",
    ],
    "The sum of a nested list is the sum of the sums of its children, and the sum of a number is the number. That recurrence does not need a flattened copy. A global accumulator also works and is easier to get wrong across calls.",
    "O(n)",
    "O(d)",
    """
def solve(value):
    if type(value) is int:
        return value
    return sum(solve(child) for child in value)
""",
    [
        {"value": [1, [2, 3], 4]},
        {"value": []},
        {"value": 0},
        {"value": [[1], []]},
    ],
)

add(
    "python-ex-fib-rolling",
    "Fib Rolling",
    "medium",
    ["python", "recursion"],
    "Implement `solve(n)`. Return the `n`th Fibonacci number with `F(0) = 0` and `F(1) = 1`. If `n` is negative, return the string `error`. Use an iterative rolling pair or an equivalent linear loop. Do not use the exponential double recursion.",
    ["n is an integer", "Linear time, constant extra space"],
    [
        "Handle 0, 1, and negatives before the loop.",
        "Keep the previous two numbers and advance n-1 times from 1.",
        "The naive recursive fib recomputes overlapping calls. Do not write it.",
    ],
    "The recurrence needs only two predecessors. Rolling them forward is linear time and constant space. Memoized recursion is also linear and spends stack and a cache. The exponential tree is the version that times out for modest n.",
    "O(n)",
    "O(1)",
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
    [
        {"n": 0},
        {"n": 1},
        {"n": 10},
        {"n": -1},
    ],
    companies=["Amazon", "Microsoft"],
    approach="Rolling pair",
)

add(
    "python-ex-bisect-left",
    "Bisect",
    "medium",
    ["python", "binary-search"],
    "Implement `solve(nums, target)`. `nums` is sorted ascending and may contain duplicates. Return the leftmost index at which `target` could be inserted without breaking the order. That index is also the first index of `target` if it is present. If `target` is greater than every element, return `len(nums)`.",
    ["nums is sorted", "The insertion index may equal the length"],
    [
        "Keep a half-open window lo, hi.",
        "When nums[mid] < target, the insertion point is to the right of mid.",
        "Otherwise it is at mid or to the left. End with lo.",
    ],
    "bisect_left is the lower bound. Moving left on every equal element is what makes the index the first match rather than an arbitrary match. The window is empty when lo == hi, and lo is the answer, including the end of the list.",
    "O(log n)",
    "O(1)",
    """
def solve(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
""",
    [
        {"nums": [1, 2, 2, 3], "target": 2},
        {"nums": [1, 3, 5], "target": 4},
        {"nums": [1, 3, 5], "target": 0},
        {"nums": [1, 3], "target": 9},
    ],
    companies=["Google", "Amazon", "Microsoft"],
    approach="Lower bound",
)

add(
    "python-ex-max-depth",
    "Max Depth",
    "medium",
    ["python", "recursion"],
    "Implement `solve(value)`. A non-list has depth 0. A list's depth is 1 plus the maximum depth of its children. An empty list has depth 1. Return that integer.",
    ["Children are integers or lists", "Empty list depth is 1"],
    [
        "If the value is not a list, return 0.",
        "If the list is empty, return 1.",
        "Otherwise return 1 plus the max child depth.",
    ],
    "Depth counts list layers, not integers. An integer is a leaf at depth 0, so a list of integers has depth 1. An empty list is still a list, so it has depth 1 and no children to take a max over. Forgetting the empty case and calling max() on no children throws.",
    "O(n)",
    "O(d)",
    """
def solve(value):
    if type(value) is not list:
        return 0
    if not value:
        return 1
    return 1 + max(solve(child) for child in value)
""",
    [
        {"value": [1, [2, [3]]]},
        {"value": []},
        {"value": 4},
        {"value": [[], [1]]},
    ],
)
