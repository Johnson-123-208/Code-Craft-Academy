"""Practice problems for module 05 data structures."""
from __future__ import annotations

from py_ex_build import add

add(
    "python-ex-drop-in-place",
    "Drop In Place",
    "easy",
    ["python", "lists"],
    "Implement `solve(items)`. Compact the odd integers to the front of a copy, preserving their order. Return `[length, prefix]` where `prefix` is the kept odds. Zero and negative evens are dropped. Negative odds stay.",
    ["Do not use a filter that forgets the length", "Order of odds is stable"],
    [
        "Walk with a write index. Copy an odd into the next write slot.",
        "The write index at the end is the new length.",
        "Return that length and the slice of kept values.",
    ],
    "The in-place pattern overwrites the front of the array and ignores the tail. Returning only the length would hide whether the prefix is correct, so the result includes the kept values. Evens, including zero, are not copied.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    out = []
    for item in items:
        if item % 2:
            out.append(item)
    return [len(out), out]
""",
    [
        {"items": [1, 2, 3, 4, 5]},
        {"items": [2, 4]},
        {"items": []},
        {"items": [0, -3, -2, 1]},
    ],
    companies=["Amazon", "Microsoft"],
)

add(
    "python-ex-move-zeros",
    "Move Zeros",
    "easy",
    ["python", "lists"],
    "Implement `solve(items)`. Return a new list with the same integers, zeros moved to the end, and the relative order of non-zeros unchanged.",
    ["Zero is the only value that moves", "Keep non-zero order"],
    [
        "Collect non-zeros in one pass.",
        "Append as many zeros as you skipped.",
        "Do not sort. Sorting would reorder the non-zeros.",
    ],
    "A stable partition writes non-zeros first and fills the tail with zeros. Two pointers do this in place. Building a new list is the same partition and is easier to test. Sorting fails because 2, 1, 0 would become 0, 1, 2.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    nonzero = [item for item in items if item != 0]
    zeros = [0] * (len(items) - len(nonzero))
    return nonzero + zeros
""",
    [
        {"items": [0, 1, 0, 3, 12]},
        {"items": [0, 0]},
        {"items": [1, 2]},
        {"items": []},
    ],
    companies=["Amazon", "Apple"],
)

add(
    "python-ex-window-sums",
    "Window Sums",
    "medium",
    ["python", "sliding-window"],
    "Implement `solve(items, k)`. Return the sum of every contiguous window of length `k`. Windows step forward by one index. If `k` is outside 1 through the length, return an empty list. Reuse the previous sum: add the incoming value and subtract the value that left.",
    ["items is a list of integers", "k is an integer"],
    [
        "Reject a bad k first.",
        "The first window is the sum of the prefix of length k.",
        "Each later window is previous + items[i] - items[i-k].",
    ],
    "Recomputing each window from scratch is O(n*k). The sliding update is O(n) because adjacent windows share k-1 terms. The first window is the only one you sum from scratch.",
    "O(n)",
    "O(n-k)",
    """
def solve(items, k):
    if k < 1 or k > len(items):
        return []
    total = sum(items[:k])
    out = [total]
    for index in range(k, len(items)):
        total += items[index] - items[index - k]
        out.append(total)
    return out
""",
    [
        {"items": [1, 2, 3, 4], "k": 2},
        {"items": [1, 2, 3], "k": 3},
        {"items": [1, 2], "k": 3},
        {"items": [5], "k": 1},
    ],
    companies=["Amazon", "Google"],
    approach="Sliding sum",
)

add(
    "python-ex-dedup-sorted",
    "Dedup Sorted",
    "medium",
    ["python", "lists"],
    "Implement `solve(items)`. `items` is sorted ascending. Remove adjacent duplicates. Return `[length, prefix]` where `prefix` holds the unique values in order. Non-adjacent logic is unnecessary because equals are already adjacent.",
    ["The input is sorted", "Keep the first copy of each run"],
    [
        "The first element always stays, when the list is non-empty.",
        "Copy an element only when it differs from the last kept value.",
        "The length is the length of that prefix. An empty input returns [0, []].",
    ],
    "On a sorted array, uniqueness is a comparison with the previous kept value. A set would also work and would spend extra memory and lose the reason the input was sorted. The write index is the classic in-place form.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    out = []
    for item in items:
        if not out or item != out[-1]:
            out.append(item)
    return [len(out), out]
""",
    [
        {"items": [1, 1, 2, 2, 3]},
        {"items": [1, 2, 3]},
        {"items": []},
        {"items": [5, 5, 5]},
    ],
    companies=["Microsoft", "Amazon"],
)

add(
    "python-ex-rotate-right",
    "Rotate Right",
    "medium",
    ["python", "lists"],
    "Implement `solve(items, k)`. Return the list rotated right by `k` positions. `k` may be larger than the length. Reduce it modulo the length. An empty list returns an empty list. Rotation by a multiple of the length returns a copy of the same order.",
    ["k is a non-negative integer", "Right rotation moves the tail to the front"],
    [
        "If the list is empty, return an empty list before the modulo.",
        "k %= len(items). A zero k returns a copy.",
        "The new list is items[-k:] + items[:-k]. Reversals are an equivalent in-place method.",
    ],
    "Right rotation by k makes the last k elements the new prefix. Modulo avoids walking k when k is a large multiple of the length. Three reversals do the same rotation with constant extra memory. Either way the order of the two slices stays intact.",
    "O(n)",
    "O(n)",
    """
def solve(items, k):
    if not items:
        return []
    k %= len(items)
    if k == 0:
        return list(items)
    return list(items[-k:]) + list(items[:-k])
""",
    [
        {"items": [1, 2, 3, 4, 5], "k": 2},
        {"items": [1, 2, 3], "k": 3},
        {"items": [], "k": 2},
        {"items": [1, 2], "k": 5},
    ],
    companies=["Amazon", "Microsoft"],
)

add(
    "python-ex-pair-key",
    "Pair Key",
    "easy",
    ["python", "tuples"],
    "Implement `solve(rows, user, day)`. `rows` is a list of `[user, day, score]`. Build a lookup keyed by the pair `(user, day)` and return the score for the requested pair. If the pair is absent, return the string `none`. Later rows overwrite the same pair.",
    ["user and day are strings", "score is an integer"],
    [
        "Use a tuple (user, day) as the dict key. A list cannot be a key.",
        "Insert rows from left to right so the last score wins.",
        "A missing key returns the string none.",
    ],
    "A tuple of the two fields is hashable and distinguishes (a, b) from (b, a). A list is not a key. The lookup is then one dict get. Last write wins when the same user and day appear twice.",
    "O(n)",
    "O(n)",
    """
def solve(rows, user, day):
    table = {}
    for row_user, row_day, score in rows:
        table[(row_user, row_day)] = score
    if (user, day) not in table:
        return "none"
    return table[(user, day)]
""",
    [
        {"rows": [["ada", "mon", 1], ["ada", "tue", 2]], "user": "ada", "day": "tue"},
        {"rows": [["ada", "mon", 1], ["ada", "mon", 4]], "user": "ada", "day": "mon"},
        {"rows": [], "user": "ada", "day": "mon"},
        {"rows": [["grace", "mon", 3]], "user": "ada", "day": "mon"},
    ],
)

add(
    "python-ex-head-tail",
    "Head Tail",
    "easy",
    ["python", "tuples"],
    "Implement `solve(items)`. `items` is a non-empty list. Return `[head, tail]` where `head` is the first element and `tail` is the list of the rest. The rest may be empty. Do not mutate the input.",
    ["The list is non-empty", "tail is a list, not a leftover scalar"],
    [
        "Bind head, *tail = items.",
        "Return [head, tail].",
        "A one-element list has an empty tail.",
    ],
    "Starred unpacking splits a sequence into the first element and a new list of the remainder. That is the head/tail recursion pattern without a slice you might forget is a copy. The tail is always a list so the caller can unpack again.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    head, *tail = items
    return [head, tail]
""",
    [
        {"items": [1, 2, 3]},
        {"items": [7]},
        {"items": ["a", "b"]},
        {"items": [0, 0]},
    ],
)

add(
    "python-ex-move-point",
    "Move Point",
    "easy",
    ["python", "tuples"],
    "Implement `solve(x, y, dx, dy)`. A point is an immutable pair. Return `[x+dx, y+dy]`, a new point. The inputs are the old coordinates. There is nothing to mutate.",
    ["All four inputs are integers", "Return a two-element list"],
    [
        "Add the deltas to the coordinates.",
        "Return a new list. Do not try to update a tuple in place.",
        "Zero deltas return the same numbers.",
    ],
    "Tuples do not support item assignment. A moved point is a new pair. That is the whole model: coordinates in, new coordinates out, no hidden object to update.",
    "O(1)",
    "O(1)",
    """
def solve(x, y, dx, dy):
    return [x + dx, y + dy]
""",
    [
        {"x": 1, "y": 2, "dx": 3, "dy": -1},
        {"x": 0, "y": 0, "dx": 0, "dy": 0},
        {"x": -2, "y": 4, "dx": 2, "dy": 0},
        {"x": 5, "y": 5, "dx": -5, "dy": -5},
    ],
)

add(
    "python-ex-tag-key",
    "Unique Key",
    "medium",
    ["python", "tuples"],
    "Implement `solve(tags)`. Build a canonical key for a bag of tags: strip, lowercase, drop empties, unique, then sort. Return that key as a list of strings. Two inputs that differ only by order, case, or duplicate tags must return the same list.",
    ["tags is a list of strings", "The result is sorted"],
    [
        "Normalize each tag before you put it in a set.",
        "Drop empty strings after strip.",
        "Sort the unique values so the key does not depend on input order.",
    ],
    "A set of tags is the right uniqueness structure and the wrong key, because set order is not part of the value. Sorting the normalized unique tags makes a canonical list. Callers can compare those lists, or tuple them, and treat the bags as equal.",
    "O(n log n)",
    "O(n)",
    """
def solve(tags):
    cleaned = set()
    for tag in tags:
        key = tag.strip().lower()
        if key:
            cleaned.add(key)
    return sorted(cleaned)
""",
    [
        {"tags": [" Py ", "py", "Go"]},
        {"tags": ["go", "PY"]},
        {"tags": ["  ", ""]},
        {"tags": ["b", "a", "a"]},
    ],
)

add(
    "python-ex-swap-pair",
    "Swap Fields",
    "easy",
    ["python", "tuples"],
    "Implement `solve(left, right)`. Return `[right, left]`. This is the unpacking swap of a two-field record into a new pair. Do not use a temporary variable.",
    ["Both values are strings", "Return a two-element list"],
    [
        "right, left = left, right is the swap. You can also return [right, left] directly.",
        "The result is a new pair.",
        "Equal inputs stay equal.",
    ],
    "Unpacking assignment swaps names without a temporary. For a two-field record the new tuple is (right, left). The list form is what the judge stores. Nothing is mutated because strings and the new pair are new values.",
    "O(1)",
    "O(1)",
    """
def solve(left, right):
    left, right = right, left
    return [left, right]
""",
    [
        {"left": "a", "right": "b"},
        {"left": "a", "right": "a"},
        {"left": "", "right": "z"},
        {"left": "name", "right": "team"},
    ],
)

add(
    "python-ex-unique-preserve",
    "Unique Preserve",
    "easy",
    ["python", "sets"],
    "Implement `solve(items)`. Return the strings with duplicates removed, keeping the first-seen order. Do not sort. Comparison is exact. Case differences are different strings.",
    ["Keep the first copy", "Do not casefold"],
    [
        "A set records seen strings. A list records order.",
        "Append only when the string is not in the set.",
        "Add it to the set at the same time.",
    ],
    "set(items) drops order. The order-preserving recipe is a seen set plus an output list. Sorting would make a different function. Case is significant because this problem does not say to normalize.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    seen = set()
    out = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out
""",
    [
        {"items": ["a", "b", "a", "c"]},
        {"items": ["A", "a"]},
        {"items": []},
        {"items": ["x", "x"]},
    ],
    companies=["Amazon"],
)

add(
    "python-ex-shared-items",
    "Shared Items",
    "easy",
    ["python", "sets"],
    "Implement `solve(left, right)`. Return the strings that appear in both lists, sorted ascending, each string once. Multiplicity does not matter.",
    ["Return a sorted list", "Intersection, not union"],
    [
        "Build a set from one side and intersect with the other.",
        "Sort the result so the order is deterministic.",
        "An empty side yields an empty list.",
    ],
    "Membership in a set is expected constant time, so the intersection is linear in the two lengths. Returning a set is not JSON-friendly and is unordered. A sorted list is the stable result the tests check.",
    "O(n + m log k)",
    "O(n + m)",
    """
def solve(left, right):
    return sorted(set(left) & set(right))
""",
    [
        {"left": ["a", "b", "a"], "right": ["b", "c"]},
        {"left": ["a"], "right": []},
        {"left": ["b", "a"], "right": ["a", "b"]},
        {"left": ["a"], "right": ["b"]},
    ],
)

add(
    "python-ex-allow-subset",
    "Allow Subset",
    "easy",
    ["python", "sets"],
    "Implement `solve(allowed, requested)`. Both are lists of permission strings. Return 1 when every requested permission is in the allowed set, including when `requested` is empty. Return 0 when any request is missing.",
    ["Empty requested is allowed", "Duplicates do not matter"],
    [
        "Build a set of allowed permissions.",
        "Every requested item must be in that set.",
        "all() of an empty request list is the success case. Return 1.",
    ],
    "Permission checks are a subset test. A list scan per permission is quadratic in a long policy. A set of the allowed names answers each check in expected constant time. An empty request asks for nothing and succeeds.",
    "O(n + m)",
    "O(n)",
    """
def solve(allowed, requested):
    have = set(allowed)
    for name in requested:
        if name not in have:
            return 0
    return 1
""",
    [
        {"allowed": ["read", "write"], "requested": ["read"]},
        {"allowed": ["read"], "requested": ["write"]},
        {"allowed": ["read"], "requested": []},
        {"allowed": [], "requested": ["read"]},
    ],
)

add(
    "python-ex-symmetric",
    "Symmetric Difference",
    "medium",
    ["python", "sets"],
    "Implement `solve(left, right)`. Return the sorted list of strings that appear in exactly one of the two lists. A string in both, even with different counts, is excluded.",
    ["Return sorted unique strings", "Presence matters, not counts"],
    [
        "Convert both sides to sets.",
        "The symmetric difference operator is ^.",
        "Sort before returning.",
    ],
    "Symmetric difference is the union minus the intersection. Counting occurrences would be a different problem. Sets drop counts first, then ^ keeps the elements in one side only, and sorting makes the list stable.",
    "O(n + m log k)",
    "O(n + m)",
    """
def solve(left, right):
    return sorted(set(left) ^ set(right))
""",
    [
        {"left": ["a", "b"], "right": ["b", "c"]},
        {"left": ["a", "a"], "right": ["a"]},
        {"left": [], "right": ["a"]},
        {"left": ["b", "a"], "right": []},
    ],
)

add(
    "python-ex-pair-seen",
    "Pair Seen",
    "medium",
    ["python", "sets"],
    "Implement `solve(points)`. `points` is a list of `[x, y]` integer coordinates. Return how many points were new when seen in order. A repeated coordinate does not increase the count. `(1, 2)` and `(2, 1)` are different points.",
    ["Order of first appearance defines new", "Coordinates are integers"],
    [
        "Store tuples (x, y) in a set. Lists are not hashable.",
        "Increment only when the tuple was absent, then add it.",
        "The answer is the size of that set.",
    ],
    "A coordinate is a pair, and a pair is hashable only as a tuple. Using a list as a set element throws. The count of successful inserts is the number of distinct points, which is also the final size of the set.",
    "O(n)",
    "O(u)",
    """
def solve(points):
    seen = set()
    for x, y in points:
        seen.add((x, y))
    return len(seen)
""",
    [
        {"points": [[1, 2], [2, 1], [1, 2]]},
        {"points": []},
        {"points": [[0, 0], [0, 0]]},
        {"points": [[1, 1], [1, 2]]},
    ],
)

add(
    "python-ex-normalize-dedupe",
    "Normalize Dedupe",
    "medium",
    ["python", "sets"],
    "Implement `solve(tags)`. Strip and casefold each tag, drop empties, and return the first-seen unique values in order. `Py` and `py` are one tag. Do not sort.",
    ["casefold, not just lower, is the case rule", "First-seen order"],
    [
        "casefold after strip.",
        "Skip empty results and values already in the seen set.",
        "Append to the output only on the first insert.",
    ],
    "casefold is the case-insensitive key for text, slightly broader than lower. The seen set uses that key. The output list keeps the first key you inserted. Sorting would throw away the order the caller first used the tag.",
    "O(n)",
    "O(u)",
    """
def solve(tags):
    seen = set()
    out = []
    for tag in tags:
        key = tag.strip().casefold()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out
""",
    [
        {"tags": [" Py ", "py", "Go"]},
        {"tags": ["  ", "A", "a"]},
        {"tags": []},
        {"tags": ["ß", "ss"]},
    ],
)

add(
    "python-ex-counts",
    "Counts",
    "easy",
    ["python", "dicts"],
    "Implement `solve(items)`. Return a dict mapping each string to how many times it appears. An empty list returns an empty dict.",
    ["Keys are the strings", "Counts are positive integers"],
    [
        "Increment a dict, starting from 0 when the key is new. Counter does this.",
        "Every occurrence adds 1, including duplicates in a row.",
        "Do not sort the keys. The dict is the answer.",
    ],
    "A frequency map is one pass of increments. collections.Counter is that dict with a zero default. Building it by hand with setdefault or get is the same algorithm and is what you should be able to write if the import is the thing you are explaining.",
    "O(n)",
    "O(u)",
    """
def solve(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts
""",
    [
        {"items": ["a", "b", "a"]},
        {"items": []},
        {"items": ["a", "a", "a"]},
        {"items": ["b", "a"]},
    ],
)

add(
    "python-ex-group-anagrams",
    "Group Anagrams",
    "medium",
    ["python", "dicts"],
    "Implement `solve(words)`. Group words that are anagrams of each other. The signature is the word's characters sorted. Return a list of groups. Groups follow the order of first appearance of each signature. Words inside a group keep their input order.",
    ["words is a list of lowercase strings in the tests", "Do not sort the groups by size"],
    [
        "The key is ''.join(sorted(word)).",
        "Remember the order in which keys first appear.",
        "Append each word to that key's list.",
    ],
    "An anagram class is the multiset of characters, and the sorted string is a hashable picture of that multiset. A dict of lists groups the words. Tracking key order separately, or using a dict which preserves insertion order, returns groups in first-seen order rather than in hash order.",
    "O(n * k log k)",
    "O(n * k)",
    """
def solve(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
""",
    [
        {"words": ["eat", "tea", "tan", "ate", "nat", "bat"]},
        {"words": [""]},
        {"words": ["a"]},
        {"words": ["ab", "ba", "abc"]},
    ],
    companies=["Amazon", "Google", "Microsoft"],
    approach="Signature map",
)

add(
    "python-ex-first-unique",
    "First Unique",
    "medium",
    ["python", "dicts"],
    "Implement `solve(items)`. Return the earliest string that appears exactly once. If every string repeats or the list is empty, return the string `none`. A later unique value does not beat an earlier one.",
    ["Scan counts first, then scan the list again", "none is the missing marker"],
    [
        "Count every item.",
        "Walk the list a second time and return the first item whose count is 1.",
        "If that walk ends, return none.",
    ],
    "The first unique value is not the same as the last time a count flipped to 1, unless you also remember indexes. Two passes are obvious and linear: counts, then the original order. One pass with a queue of candidates also works if you drop a candidate when it repeats.",
    "O(n)",
    "O(u)",
    """
def solve(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    for item in items:
        if counts[item] == 1:
            return item
    return "none"
""",
    [
        {"items": ["a", "b", "a", "c"]},
        {"items": ["a", "a"]},
        {"items": []},
        {"items": ["b", "a", "a"]},
    ],
    companies=["Amazon", "Bloomberg"],
)

add(
    "python-ex-two-sum",
    "Two Sum",
    "medium",
    ["python", "dicts"],
    "Implement `solve(nums, target)`. Return `[i, j]` with `i < j` and `nums[i] + nums[j] == target`. There is exactly one solution in the tests that should hit, except one case with no pair, which returns `[-1, -1]`. Do not use the same index twice. One pass with a map from value to index is enough.",
    ["At most one valid pair", "Indexes increase"],
    [
        "For each value, the partner is target - value.",
        "Look in the map of values already seen, then store the current index.",
        "Storing after the lookup stops a value from matching itself.",
    ],
    "The map remembers a previous index for each value. When the complement is already there, the pair is the stored index and the current index, which is in increasing order. Checking before inserting is what makes two copies of the same number work, and what stops a single number from pairing with itself.",
    "O(n)",
    "O(n)",
    """
def solve(nums, target):
    seen = {}
    for index, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], index]
        seen[value] = index
    return [-1, -1]
""",
    [
        {"nums": [2, 7, 11, 15], "target": 9},
        {"nums": [3, 2, 4], "target": 6},
        {"nums": [3, 3], "target": 6},
        {"nums": [1, 2], "target": 5},
    ],
    companies=["Google", "Amazon", "Meta", "Adobe"],
    approach="One-pass hash map",
)

add(
    "python-ex-merge-dicts",
    "Shallow Merge",
    "easy",
    ["python", "dicts"],
    "Implement `solve(left, right)`. Return a new flat dict. Start from `left`. Keys in `right` overwrite the same keys. Nested values are not used. Do not mutate the inputs.",
    ["Values are strings", "right wins on conflict"],
    [
        "Copy left.",
        "update with right.",
        "Keys only in right are included.",
    ],
    "A shallow merge is one update. It does not walk nested dicts, and it does not concatenate values. The second mapping wins because it is applied second. Copying first protects the caller's left dict.",
    "O(n + m)",
    "O(n + m)",
    """
def solve(left, right):
    merged = dict(left)
    merged.update(right)
    return merged
""",
    [
        {"left": {"a": "1", "b": "2"}, "right": {"b": "9"}},
        {"left": {}, "right": {"a": "1"}},
        {"left": {"a": "1"}, "right": {}},
        {"left": {"a": "1"}, "right": {"c": "3"}},
    ],
)

add(
    "python-ex-group-indexes",
    "Group Indexes",
    "medium",
    ["python", "dicts"],
    "Implement `solve(items)`. Return a dict mapping each string to the list of indexes where it appears, in increasing index order.",
    ["Indexes start at 0", "Every occurrence is recorded"],
    [
        "enumerate gives the index.",
        "setdefault a list, or use defaultdict, and append the index.",
        "Do not store only the last index.",
    ],
    "Grouping indexes is the same shape as grouping values, with the payload being the index instead of the item. Appending preserves left-to-right order. Overwriting the list would keep only the last index and fail the repeated-key case.",
    "O(n)",
    "O(n)",
    """
def solve(items):
    groups = {}
    for index, item in enumerate(items):
        groups.setdefault(item, []).append(index)
    return groups
""",
    [
        {"items": ["a", "b", "a"]},
        {"items": []},
        {"items": ["a"]},
        {"items": ["b", "b"]},
    ],
)

add(
    "python-ex-last-n",
    "Last N",
    "easy",
    ["python", "deque"],
    "Implement `solve(events, n)`. `events` is a list of strings. Keep only the last `n` events and return them in arrival order. If fewer than `n` events arrived, return all of them. `n` is at least 0. A bound of 0 returns an empty list.",
    ["n is a non-negative integer", "Order is oldest-to-newest among the kept events"],
    [
        "A deque with maxlen n drops from the left automatically.",
        "Append every event, then return list(deque).",
        "Slicing events[-n:] when n is positive is equivalent. Handle n == 0.",
    ],
    "A bounded deque is the structure for a trailing window of events. Append is amortized constant time and the left side falls off once the bound is hit. Taking the tail slice is the same result for a list you already hold. The deque is what you want when the events are a stream.",
    "O(n)",
    "O(k)",
    """
def solve(events, n):
    from collections import deque
    kept = deque(maxlen=n)
    for event in events:
        kept.append(event)
    return list(kept)
""",
    [
        {"events": ["a", "b", "c", "d"], "n": 2},
        {"events": ["a"], "n": 3},
        {"events": ["a", "b"], "n": 0},
        {"events": [], "n": 2},
    ],
)

add(
    "python-ex-top-k-frequent",
    "Top K Frequent",
    "medium",
    ["python", "heaps"],
    "Implement `solve(nums, k)`. Return the `k` most frequent integers. Break ties by the smaller integer. Return those `k` integers sorted by frequency descending, then by integer ascending. `k` is at least 1 and no larger than the number of distinct values.",
    ["Frequency is the primary key", "The smaller integer wins a tie"],
    [
        "Count with a dict or Counter.",
        "A heap of size k can keep the best (count, integer) pairs. Sorting the distinct pairs is also fine at this size and makes the tie break obvious.",
        "Sort the winners by (-count, integer) before you return the integers.",
    ],
    "A size-k min-heap of counts avoids sorting every distinct value when k is small. The tie break has to be in the heap key or in a final sort, or two numbers with the same count come back in an arbitrary order. This function's order is frequency, then the number.",
    "O(n log k)",
    "O(u)",
    """
def solve(nums, k):
    import heapq
    counts = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1
    heap = []
    for num, count in counts.items():
        heapq.heappush(heap, (count, -num))
        if len(heap) > k:
            heapq.heappop(heap)
    winners = [(-neg_num, count) for count, neg_num in heap]
    winners.sort(key=lambda item: (-item[1], item[0]))
    return [num for num, _count in winners]
""",
    [
        {"nums": [1, 1, 1, 2, 2, 3], "k": 2},
        {"nums": [4, 4, 5, 5], "k": 2},
        {"nums": [7], "k": 1},
        {"nums": [1, 2, 2, 3, 3], "k": 1},
    ],
    companies=["Amazon", "Facebook", "Google"],
    approach="Heap of size k",
)

add(
    "python-ex-kth-largest",
    "Kth Largest",
    "medium",
    ["python", "heaps"],
    "Implement `solve(nums, k)`. Return the kth largest integer in `nums`, where `k` is 1-based. Duplicates count separately, so in `[3, 3]` the first and second largest are both 3. `k` is between 1 and the length.",
    ["k is 1-based", "Duplicates are real elements"],
    [
        "A min-heap of size k holds the largest k values seen so far.",
        "Push each number. If the heap exceeds k, pop the smallest of those k.",
        "The root is the kth largest.",
    ],
    "Sorting descending and indexing k-1 is correct and uses more comparisons than you need when k is small. A min-heap of size k stays at the k largest values. Its root is the smallest of those, which is the kth largest overall.",
    "O(n log k)",
    "O(k)",
    """
def solve(nums, k):
    import heapq
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
""",
    [
        {"nums": [3, 2, 1, 5, 6, 4], "k": 2},
        {"nums": [3, 3], "k": 2},
        {"nums": [1], "k": 1},
        {"nums": [7, 1, 7], "k": 1},
    ],
    companies=["Amazon", "Facebook", "Microsoft"],
    approach="Min-heap of size k",
)

add(
    "python-ex-group-length",
    "Group By Length",
    "easy",
    ["python", "collections"],
    "Implement `solve(words)`. Group words by length. Return a dict whose keys are decimal strings of the lengths, because JSON object keys are strings, and whose values are the words of that length in input order.",
    ["Keys are strings of the integer length", "Keep input order inside each bucket"],
    [
        "A defaultdict(list) or setdefault appends each word.",
        "Convert the length to a string when you build the result dict.",
        "Do not sort the words inside a bucket.",
    ],
    "defaultdict(list) removes the missing-key branch. The buckets still have to be ordinary lists in insertion order. String keys are a serialization detail of this judge: JSON cannot use integer keys, and the decimal spelling is the contract.",
    "O(n)",
    "O(n)",
    """
def solve(words):
    from collections import defaultdict
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return {str(length): groups[length] for length in groups}
""",
    [
        {"words": ["a", "bb", "c", "dd"]},
        {"words": []},
        {"words": ["", "a"]},
        {"words": ["abc"]},
    ],
)

add(
    "python-ex-queue-sim",
    "Queue Sim",
    "easy",
    ["python", "deque"],
    "Implement `solve(ops)`. Each op is `[\"enq\", value]` or `[\"deq\"]`. Values are integers. Start with an empty deque. For an enqueue, append to the right and record the string `ok`. For a dequeue, record the removed integer, or the string `error` if the deque is empty. Return the list of those records. Do not use a list pop from the front.",
    ["enq appends on the right", "deq pops from the left"],
    [
        "collections.deque is the queue.",
        "append for enqueue, popleft for dequeue.",
        "Check emptiness before popleft.",
    ],
    "list.pop(0) is linear because every later element shifts. deque.popleft is constant time. The simulation records both the successful values and the empty pop so a caller can see the error instead of an exception.",
    "O(n)",
    "O(n)",
    """
def solve(ops):
    from collections import deque
    queue = deque()
    out = []
    for op in ops:
        if op[0] == "enq":
            queue.append(op[1])
            out.append("ok")
        elif not queue:
            out.append("error")
        else:
            out.append(queue.popleft())
    return out
""",
    [
        {"ops": [["enq", 1], ["enq", 2], ["deq"], ["deq"]]},
        {"ops": [["deq"]]},
        {"ops": [["enq", 5], ["deq"], ["deq"]]},
        {"ops": []},
    ],
)

add(
    "python-ex-merge-k",
    "Merge Sorted",
    "medium",
    ["python", "heaps"],
    "Implement `solve(rows)`. `rows` is a list of lists, each sorted ascending. Merge them into one sorted list. Empty rows contribute nothing. A heap of the current head of each row is enough.",
    ["Each row is sorted ascending", "The merge is stable with respect to values. Equal values may come from any row."],
    [
        "Push (value, row_index, index_in_row) for each non-empty row.",
        "Pop the smallest, append it, and push the next value from that same row if one exists.",
        "The row index in the tuple breaks ties so the heap never compares two lists.",
    ],
    "A heap of k heads merges the rows in O(n log k). Concatenate-and-sort also works and ignores the fact that the rows are already sorted. The index in the heap tuple matters: without it, equal integers are fine, but you must not let the heap fall through to comparing the rest of a row.",
    "O(n log k)",
    "O(k)",
    """
def solve(rows):
    import heapq
    heap = []
    for row_index, row in enumerate(rows):
        if row:
            heapq.heappush(heap, (row[0], row_index, 0))
    out = []
    while heap:
        value, row_index, index = heapq.heappop(heap)
        out.append(value)
        nxt = index + 1
        if nxt < len(rows[row_index]):
            heapq.heappush(heap, (rows[row_index][nxt], row_index, nxt))
    return out
""",
    [
        {"rows": [[1, 4], [1, 3], [2]]},
        {"rows": [[], [1], []]},
        {"rows": []},
        {"rows": [[1, 2, 3]]},
    ],
    companies=["Amazon", "Google", "Microsoft"],
    approach="Heap of heads",
)

add(
    "python-ex-shallow-share",
    "Shallow Share",
    "easy",
    ["python", "copying"],
    "Implement `solve(rows, value)`. `rows` is a list of lists of integers. Make a shallow copy, append `value` to the first inner list through the copy, and return `{\"original\": ..., \"copy\": ...}`. Both sides show the appended value, because a shallow copy shares the inner lists. If `rows` is empty, return both as empty lists and do not append.",
    ["Shallow copy shares inner lists", "An empty outer list has nothing to append to"],
    [
        "Copy the outer list only: list(rows) after you have built real inner lists.",
        "Append through the copy's first row.",
        "Return both structures. They alias.",
    ],
    "list(outer) copies the outer list and not the inner lists. An append to copy[0] is an append to original[0]. That alias is the bug and the demonstration. A deep copy would have hidden the append from the original, which is the next problem.",
    "O(n)",
    "O(n)",
    """
def solve(rows, value):
    original = [list(row) for row in rows]
    if not original:
        return {"original": [], "copy": []}
    copied = list(original)
    copied[0].append(value)
    return {"original": original, "copy": [list(row) for row in copied]}
""",
    [
        {"rows": [[1], [2]], "value": 9},
        {"rows": [[]], "value": 1},
        {"rows": [], "value": 1},
        {"rows": [[1, 2]], "value": 3},
    ],
)

add(
    "python-ex-deep-isolate",
    "Deep Isolate",
    "medium",
    ["python", "copying"],
    "Implement `solve(rows, value)`. Deep-copy `rows`, append `value` to the first inner list of the copy, and return `{\"original\": ..., \"copy\": ...}`. The original must not contain `value`. If `rows` is empty, return two empty lists.",
    ["Use a deep copy", "Only the copy grows"],
    [
        "copy.deepcopy, or a manual copy of every inner list, before the append.",
        "Append only on the copy.",
        "Return both so the test can see the original stayed put.",
    ],
    "A deep copy duplicates the inner lists. Mutating the copy then leaves the original unchanged. deepcopy is the library call. Rebuilding each inner list with list(row) is the same depth for this one-level structure and is what you should recognize as a manual deep copy of a list of lists.",
    "O(n)",
    "O(n)",
    """
def solve(rows, value):
    import copy
    original = [list(row) for row in rows]
    if not original:
        return {"original": [], "copy": []}
    copied = copy.deepcopy(original)
    copied[0].append(value)
    return {"original": original, "copy": copied}
""",
    [
        {"rows": [[1], [2]], "value": 9},
        {"rows": [[]], "value": 1},
        {"rows": [], "value": 1},
        {"rows": [[1, 2], [3]], "value": 4},
    ],
)

add(
    "python-ex-freeze-tags",
    "Freeze Tags",
    "easy",
    ["python", "tuples"],
    "Implement `solve(tags)`. Strip each tag and drop empties. Return the remaining tags as a list, which is the JSON form of the tuple you would store so a caller cannot append. Do not unique them. Order stays.",
    ["Empty tags after strip are dropped", "Duplicates stay"],
    [
        "Strip each tag.",
        "Keep the non-empty ones in order.",
        "Returning a list is the frozen sequence the judge can compare. Building a tuple first is the right Python, then list() it.",
    ],
    "A tuple of tags cannot be appended to. That is the freeze. The judge wants a list with the same items so the expected JSON is a list. Constructing the tuple and converting it makes the immutability step real without changing the values.",
    "O(n)",
    "O(n)",
    """
def solve(tags):
    frozen = tuple(tag.strip() for tag in tags if tag.strip())
    return list(frozen)
""",
    [
        {"tags": [" a ", "b", " "]},
        {"tags": []},
        {"tags": ["a", "a"]},
        {"tags": ["  ", ""]},
    ],
)

add(
    "python-ex-safe-nested-append",
    "Safe Nested Append",
    "medium",
    ["python", "copying"],
    "Implement `solve(rows, extra)`. `rows` is a list of lists of integers. `extra` is one new row. Return `{\"before\": copy of rows, \"after\": rows plus the extra row}`. `before` must not contain the extra row. Copy every inner list so later mutation of the result cannot alias the snapshot.",
    ["extra is a list of integers", "before is independent of after"],
    [
        "Snapshot rows by copying each inner list.",
        "Build after from another copy, then append a copy of extra.",
        "Do not append extra onto the same list you returned as before.",
    ],
    "Returning an internal list lets the caller append into your snapshot. Copying at the boundary is the fix. The before and after lists in this result are two copies, so appending the extra row changes only after.",
    "O(n)",
    "O(n)",
    """
def solve(rows, extra):
    before = [list(row) for row in rows]
    after = [list(row) for row in rows]
    after.append(list(extra))
    return {"before": before, "after": after}
""",
    [
        {"rows": [[1]], "extra": [2, 3]},
        {"rows": [], "extra": [1]},
        {"rows": [[1], [2]], "extra": []},
        {"rows": [[]], "extra": [4]},
    ],
)

add(
    "python-ex-cache-copy",
    "No Alias Return",
    "medium",
    ["python", "copying"],
    "Implement `solve(stored)`. Store a copy of the integer list. Return `{\"stored\": the stored copy, \"read\": a separate copy}`. The two lists must be equal and must not be the same object. The way to show that in JSON is to append 1 to the read copy only, and return both: `stored` stays the original numbers and `read` ends with the extra 1.",
    ["stored is a list of integers", "The extra 1 is appended only to the read side"],
    [
        "Save list(stored) as the cache.",
        "Return another list(cache) as the read, then append 1 to that read list.",
        "Do not append to the cache.",
    ],
    "A cache that returns its internal list invites the caller to mutate the cache. Returning a copy makes the append a private change. The two lists in the result are the evidence: the stored side lacks the trailing 1 that the read side has.",
    "O(n)",
    "O(n)",
    """
def solve(stored):
    cache = list(stored)
    read = list(cache)
    read.append(1)
    return {"stored": cache, "read": read}
""",
    [
        {"stored": [1, 2]},
        {"stored": []},
        {"stored": [0]},
        {"stored": [4, 5, 6]},
    ],
)
