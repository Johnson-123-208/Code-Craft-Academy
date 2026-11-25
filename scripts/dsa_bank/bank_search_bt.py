"""Backtracking, binary search, and a second wave of array classics."""

from __future__ import annotations

from itertools import combinations, permutations

from lib import cases, define


@define(
    slug="subsets",
    title="Subsets",
    difficulty="medium",
    topics=["backtracking", "bit-manipulation"],
    statement="Return every subset of distinct integers `nums`, including the empty subset. Sort each subset and sort the list of subsets.",
    constraints=["1 <= nums.length <= 10", "-10 <= nums[i] <= 10", "All values are distinct"],
    signature="from typing import List\n\ndef subsets(nums: List[int]) -> List[List[int]]:",
    function_name="subsets",
    hints=[
        "Every element is either in the subset or out of it. That is 2^n choices.",
        "A depth-first walk that branches on include and exclude builds each subset once.",
        "Bit masks from 0 to 2^n - 1 encode the same choices. Bit i selects nums[i].",
    ],
    approaches=[
        ("Cascading copy", "O(n * 2^n)", "O(n * 2^n)", "Start from [[]]. For each number, duplicate every existing subset and append the number."),
        ("Backtracking", "O(n * 2^n)", "O(n)", "The output dominates memory. The recursion depth is n."),
    ],
    editorial=(
        "The include/exclude recursion is the decision tree of the power set. "
        "Record a copy of the path at every node, or only at the leaves if you branch on both choices down to the end. "
        "Sorting the input first makes the emitted subsets comparable across implementations."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def subsets(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(i: int) -> None:
        if i == len(nums):
            out.append(path[:])
            return
        dfs(i + 1)
        path.append(nums[i])
        dfs(i + 1)
        path.pop()

    dfs(0)
    out.sort()
    return out


def _oracle_subsets(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    out = [list(comb) for k in range(len(nums) + 1) for comb in combinations(nums, k)]
    out.sort()
    return out


cases(
    "subsets",
    _oracle_subsets,
    [
        ("classic", {"nums": [1, 2, 3]}, True, "Eight subsets, including the empty one."),
        ("single", {"nums": [0]}, True, "Empty subset and [0]."),
        ("two", {"nums": [4, 1]}, False, None),
        ("neg", {"nums": [-1, 2]}, False, None),
        ("three-mixed", {"nums": [3, 2, 4, 1]}, False, None),
    ],
)


@define(
    slug="subsets-ii",
    title="Subsets II",
    difficulty="medium",
    topics=["backtracking"],
    statement="`nums` may contain duplicates. Return every unique subset, sorted internally and as a list.",
    constraints=["1 <= nums.length <= 10"],
    signature="from typing import List\n\ndef subsets_with_dup(nums: List[int]) -> List[List[int]]:",
    function_name="subsets_with_dup",
    hints=[
        "Sort so equal values are adjacent.",
        "At each level, skip a value that equals the previous value when the previous value was not chosen.",
        "That skip is what prevents emitting the same subset from two identical numbers.",
    ],
    approaches=[
        ("Set of tuples", "O(n * 2^n)", "O(n * 2^n)", "Generate the full power set and uniquify."),
        ("Sorted backtracking with a skip", "O(n * 2^n)", "O(n)", "Never start a branch on a duplicate that the previous sibling skipped."),
    ],
    editorial=(
        "Sort, then do the combination-style recursion that chooses a start index. "
        "Inside the loop, if i > start and nums[i] == nums[i - 1], continue. "
        "The first copy of a value is allowed to open the branch. Later copies are used only deeper, after that first copy was taken."
    ),
    companies=["Amazon", "Facebook", "Bloomberg", "Adobe"],
)
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        out.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    out.sort()
    return out


def _oracle_subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    found = {tuple(comb) for k in range(len(nums) + 1) for comb in combinations(nums, k)}
    return [list(item) for item in sorted(found)]


cases(
    "subsets-ii",
    _oracle_subsets_with_dup,
    [
        ("classic", {"nums": [1, 2, 2]}, True, "Duplicate 2s collapse identical subsets."),
        ("all-same", {"nums": [1, 1]}, True, "Subsets are [], [1], and [1, 1]."),
        ("unique", {"nums": [1, 2]}, False, None),
        ("three", {"nums": [4, 4, 4, 1]}, False, None),
        ("single", {"nums": [0]}, False, None),
    ],
)


@define(
    slug="permutations",
    title="Permutations",
    difficulty="medium",
    topics=["backtracking"],
    statement="Return every permutation of distinct integers `nums`. Sort the list of permutations lexicographically.",
    constraints=["1 <= nums.length <= 6", "All values are distinct"],
    signature="from typing import List\n\ndef permute(nums: List[int]) -> List[List[int]]:",
    function_name="permute",
    hints=[
        "Swap the current index with each later index, recurse, then swap back.",
        "A used array also works: choose any unused value at the next depth.",
        "There are n! leaves. The work is proportional to n times that, because each leaf copies a list of length n.",
    ],
    approaches=[
        ("Library enumeration", "O(n * n!)", "O(n)", "Fine as an oracle, not as the interview answer."),
        ("Backtracking with swaps or a used set", "O(n * n!)", "O(n)", "Depth n, branching n, n-1, and so on."),
    ],
    editorial=(
        "At depth d the path has d chosen values. The next value is any value not yet chosen. "
        "Mark it, recurse, and unmark it. Copy the path when its length is n. "
        "Sorting the collected permutations makes the answer deterministic."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "LinkedIn"],
)
def permute(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def dfs() -> None:
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i, value in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(value)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    out.sort()
    return out


def _oracle_permute(nums: list[int]) -> list[list[int]]:
    return [list(item) for item in sorted(permutations(nums))]


cases(
    "permutations",
    _oracle_permute,
    [
        ("classic", {"nums": [1, 2, 3]}, True, "Six permutations."),
        ("two", {"nums": [0, 1]}, True, "Two orders."),
        ("single", {"nums": [5]}, False, None),
        ("neg", {"nums": [-1, 0, 2]}, False, None),
        ("four", {"nums": [1, 2, 3, 4]}, False, None),
    ],
)


@define(
    slug="permutations-ii",
    title="Permutations II",
    difficulty="medium",
    topics=["backtracking"],
    statement="Return the unique permutations of `nums`, which may contain duplicates. Sort the result.",
    constraints=["1 <= nums.length <= 8"],
    signature="from typing import List\n\ndef permute_unique(nums: List[int]) -> List[List[int]]:",
    function_name="permute_unique",
    hints=[
        "Sort first so equal values are neighbors.",
        "Skip a value when it equals the previous value and the previous value has not been used at this depth.",
        "The used array is what distinguishes 'this duplicate was already chosen as the previous sibling' from 'this duplicate extends a deeper position'.",
    ],
    approaches=[
        ("Set of permutations", "O(n * n!)", "O(n * n!)", "Generate all and uniquify."),
        ("Sorted skip", "O(n * n!)", "O(n)", "Prune duplicate branches before they run."),
    ],
    editorial=(
        "After sorting, a duplicate value may be chosen at a depth only if the identical previous value was also chosen in this permutation. "
        "The condition `i > 0 and nums[i] == nums[i - 1] and not used[i - 1]` detects the illegal sibling branch and skips it."
    ),
    companies=["Amazon", "Microsoft", "LinkedIn", "Bloomberg"],
)
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    out: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def dfs() -> None:
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i, value in enumerate(nums):
            if used[i] or (i and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            path.append(value)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return out


def _oracle_permute_unique(nums: list[int]) -> list[list[int]]:
    return [list(item) for item in sorted(set(permutations(nums)))]


cases(
    "permutations-ii",
    _oracle_permute_unique,
    [
        ("classic", {"nums": [1, 1, 2]}, True, "Three unique permutations."),
        ("all-same", {"nums": [2, 2]}, True, "Only one permutation."),
        ("unique", {"nums": [1, 2]}, False, None),
        ("three", {"nums": [1, 2, 1]}, False, None),
        ("single", {"nums": [0]}, False, None),
    ],
)


@define(
    slug="combination-sum",
    title="Combination Sum",
    difficulty="medium",
    topics=["backtracking"],
    statement=(
        "Return every unique combination of `candidates` that sums to `target`. The same number may be chosen unlimited times. "
        "Combinations are sets of choices, so order does not matter. Sort each combination and sort the list."
    ),
    constraints=["1 <= candidates.length <= 30", "2 <= candidates[i] <= 40", "All values distinct", "1 <= target <= 40"],
    signature="from typing import List\n\ndef combination_sum(candidates: List[int], target: int) -> List[List[int]]:",
    function_name="combination_sum",
    hints=[
        "Sort the candidates so you can stop when a candidate exceeds the remaining target.",
        "Reuse the current index on the recursive call to allow unlimited copies. Advance the index to move to the next candidate.",
        "Record the path when the remainder hits zero.",
    ],
    approaches=[
        ("Unbounded recursion without pruning", "exponential", "O(target)", "Correct and messy."),
        ("Sorted backtracking", "O(n^(target/min))", "O(target)", "Prune when the candidate exceeds the remainder."),
    ],
    editorial=(
        "This is unbounded knapsack written as search. "
        "The start index enforces nondecreasing order, which is what makes [2, 2, 3] and [3, 2, 2] the same combination. "
        "Passing i, not i + 1, is the single line that allows reuse."
    ),
    companies=["Amazon", "Adobe", "Uber", "Airbnb"],
)
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            dfs(i, remain - candidates[i])
            path.pop()

    dfs(0, target)
    return out


def _oracle_combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(set(candidates))
    out: list[list[int]] = []

    def dfs(start: int, remain: int, path: list[int]) -> None:
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            dfs(i, remain - candidates[i], path)
            path.pop()

    dfs(0, target, [])
    return out


cases(
    "combination-sum",
    _oracle_combination_sum,
    [
        ("classic", {"candidates": [2, 3, 6, 7], "target": 7}, True, "The combinations are [2, 2, 3] and [7]."),
        ("repeat", {"candidates": [2, 3, 5], "target": 8}, True, "Three combinations sum to 8."),
        ("none", {"candidates": [2], "target": 1}, False, None),
        ("one", {"candidates": [3], "target": 9}, False, None),
        ("mixed", {"candidates": [8, 7, 4, 3], "target": 11}, False, None),
    ],
)


@define(
    slug="combinations",
    title="Combinations",
    difficulty="medium",
    topics=["backtracking"],
    statement="Return every combination of `k` numbers chosen from 1..n, sorted.",
    constraints=["1 <= n <= 20", "1 <= k <= n"],
    signature="from typing import List\n\ndef combine(n: int, k: int) -> List[List[int]]:",
    function_name="combine",
    hints=[
        "This is subsets of a fixed size.",
        "Choose the next number from start..n, then recurse with k decreased.",
        "Stop a branch early when the remaining numbers cannot fill the combination.",
    ],
    approaches=[
        ("Library combinations", "O(k * C(n, k))", "O(k)", "The closed form of the same recursion."),
        ("Backtracking with pruning", "O(k * C(n, k))", "O(k)", "The remaining-count check cuts hopeless branches."),
    ],
    editorial=(
        "At each step append a number at least one larger than the previous, which enforces increasing order. "
        "If the numbers left in 1..n are fewer than the slots left in the combination, return. "
        "That prune is the difference between a toy recursion and an interview-quality one."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def combine(n: int, k: int) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        if len(path) == k:
            out.append(path[:])
            return
        need = k - len(path)
        for value in range(start, n - need + 2):
            path.append(value)
            dfs(value + 1)
            path.pop()

    dfs(1)
    return out


def _oracle_combine(n: int, k: int) -> list[list[int]]:
    return [list(comb) for comb in combinations(range(1, n + 1), k)]


cases(
    "combinations",
    _oracle_combine,
    [
        ("classic", {"n": 4, "k": 2}, True, "Every pair from 1..4."),
        ("full", {"n": 3, "k": 3}, True, "Only [1, 2, 3]."),
        ("one", {"n": 3, "k": 1}, False, None),
        ("k3", {"n": 5, "k": 3}, False, None),
        ("n1", {"n": 1, "k": 1}, False, None),
    ],
)


@define(
    slug="letter-combinations-of-a-phone-number",
    title="Letter Combinations of a Phone Number",
    difficulty="medium",
    topics=["backtracking", "strings"],
    statement="Given a digit string from 2 to 9, return every letter combination the phone keypad can produce. Sort the result. An empty digit string returns an empty list.",
    constraints=["0 <= digits.length <= 4", "digits[i] is in '2'..'9'"],
    signature="from typing import List\n\ndef letter_combinations(digits: str) -> List[str]:",
    function_name="letter_combinations",
    hints=[
        "Map each digit to its letters. Digit 7 has four letters and digit 9 has four letters.",
        "The recursion depth is the index in the digit string.",
        "Append one letter, recurse, and pop it. At the last digit, join the path.",
    ],
    approaches=[
        ("Iterative product", "O(4^n * n)", "O(4^n * n)", "Start from ['' ] and extend by each digit's letters."),
        ("Backtracking", "O(4^n * n)", "O(n)", "Same product, built depth-first."),
    ],
    editorial=(
        "This is the cartesian product of the letter lists. "
        "Backtracking builds one string at a time and reuses the path buffer. "
        "The empty input is the base case that must return an empty list rather than a list containing an empty string."
    ),
    companies=["Amazon", "Microsoft", "Uber", "Facebook"],
)
def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []
    pad = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }
    out: list[str] = []
    path: list[str] = []

    def dfs(i: int) -> None:
        if i == len(digits):
            out.append("".join(path))
            return
        for ch in pad[digits[i]]:
            path.append(ch)
            dfs(i + 1)
            path.pop()

    dfs(0)
    return sorted(out)


def _oracle_letter_combinations(digits: str) -> list[str]:
    pad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    if not digits:
        return []
    out = [""]
    for digit in digits:
        out = [prefix + ch for prefix in out for ch in pad[digit]]
    return sorted(out)


cases(
    "letter-combinations-of-a-phone-number",
    _oracle_letter_combinations,
    [
        ("two", {"digits": "23"}, True, "Nine combinations from abc and def."),
        ("empty", {"digits": ""}, True, "No digits means no combinations."),
        ("one", {"digits": "2"}, False, None),
        ("seven", {"digits": "7"}, False, None),
        ("long", {"digits": "79"}, False, None),
    ],
)


@define(
    slug="generate-parentheses",
    title="Generate Parentheses",
    difficulty="medium",
    topics=["backtracking", "strings"],
    statement="Return every string of `n` pairs of well-formed parentheses, sorted.",
    constraints=["1 <= n <= 8"],
    signature="from typing import List\n\ndef generate_parenthesis(n: int) -> List[str]:",
    function_name="generate_parenthesis",
    hints=[
        "You may place an opening parenthesis when fewer than n have been placed.",
        "You may place a closing parenthesis only when it would not exceed the number of opens.",
        "A string of length 2n built under those rules is always valid, and every valid string is built.",
    ],
    approaches=[
        ("Filter all strings", "O(2^(2n) * n)", "O(n)", "Generate every string of length 2n and keep the valid ones."),
        ("Constrained backtracking", "O(4^n / sqrt(n))", "O(n)", "The Catalan-number number of leaves, with pruned branches."),
    ],
    editorial=(
        "Track how many opens and closes have been used. "
        "The close count may never exceed the open count, and the open count may never exceed n. "
        "Those two inequalities are necessary and sufficient for a prefix of a parentheses string, so the search emits exactly the Catalan structures."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def generate_parenthesis(n: int) -> list[str]:
    out: list[str] = []
    path: list[str] = []

    def dfs(opened: int, closed: int) -> None:
        if len(path) == 2 * n:
            out.append("".join(path))
            return
        if opened < n:
            path.append("(")
            dfs(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            dfs(opened, closed + 1)
            path.pop()

    dfs(0, 0)
    return sorted(out)


def _oracle_generate_parenthesis(n: int) -> list[str]:
    out = []

    def ok(text: str) -> bool:
        balance = 0
        for ch in text:
            balance += 1 if ch == "(" else -1
            if balance < 0:
                return False
        return balance == 0

    def walk(text: str) -> None:
        if len(text) == 2 * n:
            if ok(text):
                out.append(text)
            return
        walk(text + "(")
        walk(text + ")")

    walk("")
    return sorted(out)


cases(
    "generate-parentheses",
    _oracle_generate_parenthesis,
    [
        ("one", {"n": 1}, True, "Only ()."),
        ("two", {"n": 2}, True, "Two shapes: (()) and ()()."),
        ("three", {"n": 3}, False, None),
        ("four", {"n": 4}, False, None),
    ],
)


@define(
    slug="word-break",
    title="Word Break",
    difficulty="medium",
    topics=["dynamic-programming", "backtracking", "strings"],
    statement="Return true when `s` can be segmented into a space-separated sequence of dictionary words. The same word may be reused.",
    constraints=["1 <= s.length <= 30 for these tests", "1 <= wordDict.length <= 100", "words and s are lowercase"],
    signature="from typing import List\n\ndef word_break(s: str, word_dict: List[str]) -> bool:",
    function_name="word_break",
    hints=[
        "A plain recursion tries every dictionary word at the current index and explodes on overlapping prefixes.",
        "Let dp[i] mean the prefix s[:i] can be segmented.",
        "dp[j] is true when some i < j has dp[i] and s[i:j] is in the dictionary. dp[0] is true.",
    ],
    approaches=[
        ("Recursion without memory", "exponential", "O(n)", "Recomputes the same suffix many times."),
        ("Boolean prefix DP", "O(n^2 + total word length)", "O(n)", "One boolean per prefix, dictionary lookup per slice."),
    ],
    editorial=(
        "Put the dictionary in a set. dp[0] = True represents the empty prefix. "
        "For each end j, try every start i < j and set dp[j] when dp[i] and the slice is a word. "
        "The answer is dp[len(s)]. Memoized search is the same recurrence written from the other end."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for end in range(1, len(s) + 1):
        for start in range(end):
            if dp[start] and s[start:end] in words:
                dp[end] = True
                break
    return dp[-1]


def _oracle_word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)

    def ok(i: int) -> bool:
        if i == len(s):
            return True
        for j in range(i + 1, len(s) + 1):
            if s[i:j] in words and ok(j):
                return True
        return False

    return ok(0)


cases(
    "word-break",
    _oracle_word_break,
    [
        ("yes", {"s": "leetcode", "word_dict": ["leet", "code"]}, True, "leet + code."),
        ("reuse", {"s": "applepenapple", "word_dict": ["apple", "pen"]}, True, "apple is reused."),
        ("no", {"s": "catsandog", "word_dict": ["cats", "dog", "sand", "and", "cat"]}, False, None),
        ("single", {"s": "a", "word_dict": ["a"]}, False, None),
        ("overlap", {"s": "aaaaaaa", "word_dict": ["aaaa", "aaa"]}, False, None),
    ],
)


@define(
    slug="binary-search",
    title="Binary Search",
    difficulty="easy",
    topics=["binary-search"],
    statement="`nums` is sorted ascending and contains distinct values. Return the index of `target`, or -1 when it is absent.",
    constraints=["1 <= nums.length <= 10^4", "-10^4 < nums[i], target < 10^4"],
    signature="from typing import List\n\ndef search(nums: List[int], target: int) -> int:",
    function_name="search",
    hints=[
        "Keep a closed interval [lo, hi] of indices that might still hold the target.",
        "Compare the middle element and discard the half that cannot contain it.",
        "Loop while lo <= hi. Returning on an empty interval means the target is absent.",
    ],
    approaches=[
        ("Linear scan", "O(n)", "O(1)", "Ignore the sorted order."),
        ("Binary search", "O(log n)", "O(1)", "Halve the closed interval each step."),
    ],
    editorial=(
        "Set lo to 0 and hi to n - 1. While the interval is nonempty, let mid = (lo + hi) // 2. "
        "Equality returns mid. A smaller target moves hi to mid - 1. A larger target moves lo to mid + 1. "
        "Using mid + 1 and mid - 1 is what guarantees the interval shrinks, including when mid equals lo."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def _oracle_search(nums: list[int], target: int) -> int:
    try:
        return nums.index(target)
    except ValueError:
        return -1


cases(
    "binary-search",
    _oracle_search,
    [
        ("hit", {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, True, "9 sits at index 4."),
        ("miss", {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, True, "2 is absent."),
        ("ends", {"nums": [1, 2, 3], "target": 1}, False, None),
        ("last", {"nums": [1, 2, 3], "target": 3}, False, None),
        ("single", {"nums": [5], "target": 5}, False, None),
    ],
)


@define(
    slug="search-insert-position",
    title="Search Insert Position",
    difficulty="easy",
    topics=["binary-search"],
    statement="Given a sorted array of distinct integers, return the index of `target` if it exists. Otherwise return the index where it would be inserted to keep the array sorted.",
    constraints=["1 <= nums.length <= 10^4"],
    signature="from typing import List\n\ndef search_insert(nums: List[int], target: int) -> int:",
    function_name="search_insert",
    hints=[
        "This is lower bound: the first index whose value is greater than or equal to target.",
        "Keep the invariant that the answer lies in [lo, hi].",
        "When the loop ends, lo is the insertion point, even if it equals n.",
    ],
    approaches=[
        ("Linear scan", "O(n)", "O(1)", "Stop at the first value that is not smaller than target."),
        ("Lower-bound binary search", "O(log n)", "O(1)", "Half-open or closed search for the first nums[i] >= target."),
    ],
    editorial=(
        "Use a half-open interval [lo, hi). If nums[mid] < target, the insertion point is after mid. Otherwise it is at mid or before. "
        "When lo == hi the interval is empty and lo is the first position that is not strictly smaller than target."
    ),
    companies=["Amazon", "Adobe", "Apple", "Google"],
)
def search_insert(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _oracle_search_insert(nums: list[int], target: int) -> int:
    for i, value in enumerate(nums):
        if value >= target:
            return i
    return len(nums)


cases(
    "search-insert-position",
    _oracle_search_insert,
    [
        ("present", {"nums": [1, 3, 5, 6], "target": 5}, True, "5 is already at index 2."),
        ("insert", {"nums": [1, 3, 5, 6], "target": 2}, True, "2 belongs at index 1."),
        ("after", {"nums": [1, 3, 5, 6], "target": 7}, False, None),
        ("before", {"nums": [1, 3, 5, 6], "target": 0}, False, None),
        ("single", {"nums": [1], "target": 1}, False, None),
    ],
)


@define(
    slug="search-in-rotated-sorted-array",
    title="Search in Rotated Sorted Array",
    difficulty="medium",
    topics=["binary-search"],
    statement=(
        "`nums` was sorted ascending with distinct values, then rotated. "
        "Return the index of `target`, or -1."
    ),
    constraints=["1 <= nums.length <= 5000", "All values are distinct"],
    signature="from typing import List\n\ndef search_rotated(nums: List[int], target: int) -> int:",
    function_name="search_rotated",
    hints=[
        "One half of a rotated array is still sorted. Identify which one by comparing nums[lo] and nums[mid].",
        "If the target lies inside the sorted half, discard the other half. Otherwise discard the sorted half.",
        "The comparison target < nums[mid] must be combined with the half's bounds, not used alone.",
    ],
    approaches=[
        ("Find the pivot, then binary search", "O(log n)", "O(1)", "Two binary searches."),
        ("One binary search", "O(log n)", "O(1)", "Decide the sorted half on every step."),
    ],
    editorial=(
        "At each mid, either the left half [lo, mid] is sorted or the right half [mid, hi] is sorted. "
        "Test whether the target sits inside that sorted range, using inclusive bounds on the outer end. "
        "If it does, keep that half. If it does not, the target is in the other half, which contains the rotation."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Bloomberg"],
)
def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        elif nums[mid] < target <= nums[hi]:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def _oracle_search_rotated(nums: list[int], target: int) -> int:
    return nums.index(target) if target in nums else -1


cases(
    "search-in-rotated-sorted-array",
    _oracle_search_rotated,
    [
        ("classic", {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}, True, "0 sits at index 4."),
        ("miss", {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}, True, "3 is absent."),
        ("unrotated", {"nums": [1, 2, 3, 4], "target": 3}, False, None),
        ("pivot-target", {"nums": [3, 1], "target": 1}, False, None),
        ("single", {"nums": [1], "target": 0}, False, None),
    ],
)


@define(
    slug="find-minimum-in-rotated-sorted-array",
    title="Find Minimum in Rotated Sorted Array",
    difficulty="medium",
    topics=["binary-search"],
    statement="Return the minimum element of a rotated sorted array of distinct values.",
    constraints=["1 <= nums.length <= 5000", "All values are distinct"],
    signature="from typing import List\n\ndef find_min(nums: List[int]) -> int:",
    function_name="find_min",
    hints=[
        "The minimum is the only element that is smaller than its left neighbor, unless the array is not rotated.",
        "Compare nums[mid] with nums[hi]. If mid is larger, the minimum is to the right of mid.",
        "Otherwise the minimum is at mid or to its left, so hi becomes mid.",
    ],
    approaches=[
        ("Linear scan", "O(n)", "O(1)", "min(nums)."),
        ("Binary search on the rotation", "O(log n)", "O(1)", "Shrink toward the unsorted side."),
    ],
    editorial=(
        "If nums[mid] > nums[hi], the rotation point, and therefore the minimum, is strictly to the right of mid. "
        "Otherwise mid could be the minimum, so hi moves to mid and mid stays inside the interval. "
        "The loop uses lo < hi and finishes with both ends on the minimum."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


def _oracle_find_min(nums: list[int]) -> int:
    return min(nums)


cases(
    "find-minimum-in-rotated-sorted-array",
    _oracle_find_min,
    [
        ("rotated", {"nums": [3, 4, 5, 1, 2]}, True, "The minimum is 1."),
        ("unrotated", {"nums": [1, 2, 3, 4]}, True, "The minimum is the first element."),
        ("two", {"nums": [2, 1]}, False, None),
        ("single", {"nums": [8]}, False, None),
        ("tail", {"nums": [4, 5, 6, 7, 0]}, False, None),
    ],
)


@define(
    slug="koko-eating-bananas",
    title="Koko Eating Bananas",
    difficulty="medium",
    topics=["binary-search"],
    statement=(
        "Koko eats all bananas from one pile before starting another, at a constant integer speed of k bananas per hour. "
        "Each pile takes ceil(pile / k) hours. Return the minimum k that finishes every pile within `h` hours."
    ),
    constraints=["1 <= piles.length <= 10^4", "1 <= piles[i] <= 10^9", "piles.length <= h"],
    signature="from typing import List\n\ndef min_eating_speed(piles: List[int], h: int) -> int:",
    function_name="min_eating_speed",
    hints=[
        "Hours needed is monotone in the speed: a faster speed never takes more hours.",
        "The search range is 1..max(piles). At max(piles), every pile takes one hour.",
        "Binary search the smallest speed whose hour count is at most h.",
    ],
    approaches=[
        ("Linear search of speeds", "O(max(pile) * n)", "O(1)", "Try every speed."),
        ("Binary search on the answer", "O(n log max(pile))", "O(1)", "The feasibility predicate is monotone."),
    ],
    editorial=(
        "This is binary search on the answer, not on an array index. "
        "The predicate 'speed k finishes in at most h hours' is false, then true, as k grows. "
        "Compute hours with integer ceiling division (pile + k - 1) // k and shrink to the first true speed."
    ),
    companies=["Amazon", "Google", "Facebook", "Uber"],
)
def min_eating_speed(piles: list[int], h: int) -> int:
    def hours(speed: int) -> int:
        return sum((pile + speed - 1) // speed for pile in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _oracle_min_eating_speed(piles: list[int], h: int) -> int:
    def hours(speed: int) -> int:
        return sum((pile + speed - 1) // speed for pile in piles)

    speed = 1
    while hours(speed) > h:
        speed += 1
    return speed


cases(
    "koko-eating-bananas",
    _oracle_min_eating_speed,
    [
        ("classic", {"piles": [3, 6, 7, 11], "h": 8}, True, "Speed 4 finishes in 8 hours."),
        ("tight", {"piles": [30, 11, 23, 4, 20], "h": 5}, True, "Speed equals the largest pile."),
        ("loose", {"piles": [30, 11, 23, 4, 20], "h": 6}, False, None),
        ("one", {"piles": [5], "h": 2}, False, None),
        ("exact", {"piles": [1, 1, 1], "h": 3}, False, None),
    ],
)


@define(
    slug="capacity-to-ship-packages-within-d-days",
    title="Capacity To Ship Packages Within D Days",
    difficulty="medium",
    topics=["binary-search"],
    statement=(
        "Packages must ship in order. A ship of capacity `cap` loads packages until the next one would exceed cap, then the day ends. "
        "Return the minimum capacity that ships every package within `days` days."
    ),
    constraints=["1 <= weights.length <= 5 * 10^4", "1 <= days <= weights.length"],
    signature="from typing import List\n\ndef ship_within_days(weights: List[int], days: int) -> int:",
    function_name="ship_within_days",
    hints=[
        "Capacity must be at least the heaviest package, and at most the sum of the weights.",
        "Given a capacity, a linear scan counts how many days that capacity needs.",
        "Binary search the smallest capacity whose day count is at most days.",
    ],
    approaches=[
        ("Try every capacity", "O(sum * n)", "O(1)", "Feasible only for tiny sums."),
        ("Binary search on capacity", "O(n log sum)", "O(1)", "Monotone feasibility."),
    ],
    editorial=(
        "The lower bound is max(weights) because a package cannot be split. The upper bound is sum(weights), which finishes in one day. "
        "The day-count predicate decreases as capacity grows, so binary search finds the first feasible capacity. "
        "The greedy loader is optimal for a fixed capacity: delaying a package that fits cannot reduce the number of days."
    ),
    companies=["Amazon", "Google", "Uber", "Microsoft"],
)
def ship_within_days(weights: list[int], days: int) -> int:
    def needed(cap: int) -> int:
        used = 1
        load = 0
        for weight in weights:
            if load + weight > cap:
                used += 1
                load = 0
            load += weight
        return used

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _oracle_ship_within_days(weights: list[int], days: int) -> int:
    def needed(cap: int) -> int:
        used = 1
        load = 0
        for weight in weights:
            if load + weight > cap:
                used += 1
                load = 0
            load += weight
        return used

    cap = max(weights)
    while needed(cap) > days:
        cap += 1
    return cap


cases(
    "capacity-to-ship-packages-within-d-days",
    _oracle_ship_within_days,
    [
        ("classic", {"weights": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "days": 5}, True, "The minimum capacity is 15."),
        ("one-day", {"weights": [3, 2, 2, 4, 1, 4], "days": 1}, True, "The capacity is the total weight."),
        ("per-package", {"weights": [1, 2, 3, 1, 1], "days": 4}, False, None),
        ("two", {"weights": [5, 5, 5], "days": 2}, False, None),
        ("equal", {"weights": [2, 2, 2], "days": 3}, False, None),
    ],
)


@define(
    slug="sqrtx",
    title="Sqrt(x)",
    difficulty="easy",
    topics=["binary-search", "math"],
    statement="Return the floor of the square root of non-negative integer `x`. Use integer arithmetic only.",
    constraints=["0 <= x <= 2^31 - 1"],
    signature="def my_sqrt(x: int) -> int:",
    function_name="my_sqrt",
    hints=[
        "The answer r satisfies r * r <= x and (r + 1) * (r + 1) > x.",
        "Binary search r over 0..x. For large x, searching up to 2^16 is enough, but 0..x is correct.",
        "Compare mid * mid with x using integers. Watch overflow in languages with fixed-width ints. Python integers do not overflow.",
    ],
    approaches=[
        ("Linear probe", "O(sqrt(x))", "O(1)", "Increment until the square passes x."),
        ("Binary search", "O(log x)", "O(1)", "Search the integer root directly."),
    ],
    editorial=(
        "Search the largest integer whose square is at most x. "
        "If mid * mid <= x, the answer is at least mid, so move lo to mid + 1 and remember mid. "
        "Otherwise move hi to mid - 1. The remembered value, which is hi at the end of a careful loop, is the floor root."
    ),
    companies=["Amazon", "Apple", "Microsoft", "Bloomberg"],
)
def my_sqrt(x: int) -> int:
    lo, hi = 0, x
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def _oracle_my_sqrt(x: int) -> int:
    root = 0
    while (root + 1) * (root + 1) <= x:
        root += 1
    return root


cases(
    "sqrtx",
    _oracle_my_sqrt,
    [
        ("eight", {"x": 8}, True, "The floor root of 8 is 2."),
        ("four", {"x": 4}, True, "The floor root of 4 is 2."),
        ("zero", {"x": 0}, False, None),
        ("one", {"x": 1}, False, None),
        ("large", {"x": 100}, False, None),
    ],
)


@define(
    slug="powx-n",
    title="Pow(x, n)",
    difficulty="medium",
    topics=["binary-search", "math", "divide-and-conquer"],
    statement="Compute the integer power `x` raised to the non-negative integer `n` using fast exponentiation. The tests keep the result inside a 64-bit signed range.",
    constraints=["-100 <= x <= 100", "0 <= n <= 30 for these tests"],
    signature="def my_pow(x: int, n: int) -> int:",
    function_name="my_pow",
    hints=[
        "x^n = (x^(n/2))^2 when n is even, and x * (x^(n//2))^2 when n is odd.",
        "The iterative form squares the base and halves the exponent, multiplying into the result when the exponent is odd.",
        "n = 0 returns 1, including 0^0 in this problem's convention.",
    ],
    approaches=[
        ("Multiply in a loop", "O(n)", "O(1)", "Too slow when n is 10^9, which the full problem allows."),
        ("Binary exponentiation", "O(log n)", "O(1)", "Every bit of the exponent does constant work."),
    ],
    editorial=(
        "Binary exponentiation reads the binary expansion of n. "
        "Each set bit contributes the current base to the result, and the base is squared as the exponent shifts right. "
        "The number of multiplications is proportional to the number of bits, not to n."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def my_pow(x: int, n: int) -> int:
    result = 1
    base = x
    exp = n
    while exp:
        if exp & 1:
            result *= base
        base *= base
        exp >>= 1
    return result


def _oracle_my_pow(x: int, n: int) -> int:
    return x**n


cases(
    "powx-n",
    _oracle_my_pow,
    [
        ("classic", {"x": 2, "n": 10}, True, "2^10 = 1024."),
        ("odd", {"x": 2, "n": 3}, True, "2^3 = 8."),
        ("zero-exp", {"x": 5, "n": 0}, False, None),
        ("negative-base", {"x": -2, "n": 5}, False, None),
        ("one", {"x": 1, "n": 20}, False, None),
    ],
)


@define(
    slug="majority-element",
    title="Majority Element",
    difficulty="easy",
    topics=["arrays", "boyer-moore", "bit-manipulation"],
    statement="Return the element that appears more than n / 2 times. The majority element always exists.",
    constraints=["1 <= nums.length <= 5 * 10^4"],
    signature="from typing import List\n\ndef majority_element(nums: List[int]) -> int:",
    function_name="majority_element",
    hints=[
        "A hash map count is the direct solution.",
        "Sorting puts the majority element at index n // 2.",
        "Boyer-Moore voting pairs the candidate against every other value. The majority cannot be cancelled completely.",
    ],
    approaches=[
        ("Hash count", "O(n)", "O(n)", "Return the value whose count exceeds n / 2."),
        ("Boyer-Moore vote", "O(n)", "O(1)", "One candidate and one counter."),
    ],
    editorial=(
        "Initialize candidate and count to the first element and 1. "
        "A matching value increments the count. Any other value decrements it. When the count hits zero, the next value becomes the candidate. "
        "Because a strict majority exists, it is the last candidate standing. A second pass would verify the candidate if the problem did not guarantee existence."
    ),
    companies=["Amazon", "Adobe", "Google", "Microsoft"],
)
def majority_element(nums: list[int]) -> int:
    candidate = count = 0
    for value in nums:
        if count == 0:
            candidate = value
        count += 1 if value == candidate else -1
    return candidate


def _oracle_majority_element(nums: list[int]) -> int:
    from collections import Counter

    n = len(nums)
    for value, count in Counter(nums).items():
        if count > n / 2:
            return value
    raise ValueError("no majority")


cases(
    "majority-element",
    _oracle_majority_element,
    [
        ("classic", {"nums": [3, 2, 3]}, True, "3 appears twice."),
        ("long", {"nums": [2, 2, 1, 1, 1, 2, 2]}, True, "2 appears four times."),
        ("single", {"nums": [1]}, False, None),
        ("all", {"nums": [4, 4, 4, 4]}, False, None),
        ("edge", {"nums": [6, 5, 5]}, False, None),
    ],
)


@define(
    slug="missing-number",
    title="Missing Number",
    difficulty="easy",
    topics=["arrays", "bit-manipulation", "math"],
    statement="`nums` contains n distinct numbers from the range 0..n. Return the one number that is missing.",
    constraints=["1 <= n <= 10^4", "0 <= nums[i] <= n", "All values are unique"],
    signature="from typing import List\n\ndef missing_number(nums: List[int]) -> int:",
    function_name="missing_number",
    hints=[
        "The sum of 0..n is n * (n + 1) / 2. Subtract the array sum.",
        "XOR of 0..n XOR every nums[i] leaves the missing number, because pairs cancel.",
        "Cyclic placement also works: put value v at index v and look for the empty slot.",
    ],
    approaches=[
        ("Sort and scan", "O(n log n)", "O(1)", "The first index that does not match its value is the gap."),
        ("Gauss or XOR", "O(n)", "O(1)", "A closed formula or a cancellation."),
    ],
    editorial=(
        "The arithmetic solution is one subtraction. Use integer division, which is exact because n(n+1) is even. "
        "The XOR solution avoids overflow in fixed-width languages: XOR every index and every value, and XOR n at the end. "
        "Both are O(1) extra memory."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Apple"],
)
def missing_number(nums: list[int]) -> int:
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


def _oracle_missing_number(nums: list[int]) -> int:
    present = set(nums)
    for value in range(len(nums) + 1):
        if value not in present:
            return value
    raise ValueError("none")


cases(
    "missing-number",
    _oracle_missing_number,
    [
        ("classic", {"nums": [3, 0, 1]}, True, "2 is missing from 0..3."),
        ("end", {"nums": [0, 1]}, True, "2 is missing."),
        ("zero", {"nums": [1]}, False, None),
        ("middle", {"nums": [9, 6, 4, 2, 3, 5, 7, 0, 1]}, False, None),
        ("single-zero", {"nums": [0]}, False, None),
    ],
)


@define(
    slug="first-missing-positive",
    title="First Missing Positive",
    difficulty="hard",
    topics=["arrays", "cyclic-sort"],
    statement="Return the smallest missing positive integer in an unsorted array. The interview constraint is O(n) time and O(1) extra memory, which cyclic placement achieves.",
    constraints=["1 <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1"],
    signature="from typing import List\n\ndef first_missing_positive(nums: List[int]) -> int:",
    function_name="first_missing_positive",
    hints=[
        "The answer is in 1..n+1. Values outside that range can be ignored.",
        "Place each value v onto index v - 1 by swapping, and keep swapping while the new value also belongs in range.",
        "The first index i whose value is not i + 1 is the answer. If every index matches, the answer is n + 1.",
    ],
    approaches=[
        ("Hash set", "O(n)", "O(n)", "Look for 1, 2, 3, ... until a gap."),
        ("Index as a hash", "O(n)", "O(1)", "Swap values into their home slots. Each swap places one value permanently."),
    ],
    editorial=(
        "For an array of length n the smallest missing positive is at most n + 1. "
        "Use the array itself as a set of presence flags by swapping nums[i] into index nums[i] - 1 whenever that index is in range and does not already hold the value. "
        "A second scan returns the first mismatch. The swap loop is linear because every swap puts at least one value on its home index."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def _oracle_first_missing_positive(nums: list[int]) -> int:
    present = set(nums)
    value = 1
    while value in present:
        value += 1
    return value


cases(
    "first-missing-positive",
    _oracle_first_missing_positive,
    [
        ("classic", {"nums": [1, 2, 0]}, True, "3 is the smallest missing positive."),
        ("gap", {"nums": [3, 4, -1, 1]}, True, "2 is missing."),
        ("seven", {"nums": [7, 8, 9, 11, 12]}, False, None),
        ("one", {"nums": [1]}, False, None),
        ("dups", {"nums": [1, 1]}, False, None),
    ],
)


@define(
    slug="jump-game",
    title="Jump Game",
    difficulty="medium",
    topics=["arrays", "greedy"],
    statement="You start at index 0. `nums[i]` is the maximum forward jump length from i. Return true when index n - 1 is reachable.",
    constraints=["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^5"],
    signature="from typing import List\n\ndef can_jump(nums: List[int]) -> bool:",
    function_name="can_jump",
    hints=[
        "A BFS on indices is correct and uses a queue.",
        "Greedy: track the farthest index reachable so far.",
        "If the scan index ever passes that farthest index, you are stuck.",
    ],
    approaches=[
        ("DFS or BFS", "O(n)", "O(n)", "Visit each index once if you mark it."),
        ("Farthest reach", "O(n)", "O(1)", "One integer summarizes every earlier jump."),
    ],
    editorial=(
        "Let reach be the largest index you can stand on. For each i from 0 while i <= reach, set reach = max(reach, i + nums[i]). "
        "If reach ever becomes at least n - 1, return true. "
        "If the loop ends because i walked past reach, a zero gap blocked every jump."
    ),
    companies=["Amazon", "Google", "Microsoft", "Apple"],
)
def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True


def _oracle_can_jump(nums: list[int]) -> bool:
    reach = 0
    i = 0
    while i <= reach and reach < len(nums) - 1:
        reach = max(reach, i + nums[i])
        i += 1
    return reach >= len(nums) - 1


cases(
    "jump-game",
    _oracle_can_jump,
    [
        ("yes", {"nums": [2, 3, 1, 1, 4]}, True, "One jump of 2 and then 3 reaches the end."),
        ("no", {"nums": [3, 2, 1, 0, 4]}, True, "The 0 blocks the last index."),
        ("single", {"nums": [0]}, False, None),
        ("zeros", {"nums": [1, 0, 1]}, False, None),
        ("exact", {"nums": [2, 0, 0]}, False, None),
    ],
)


@define(
    slug="gas-station",
    title="Gas Station",
    difficulty="medium",
    topics=["arrays", "greedy"],
    statement=(
        "There are n gas stations on a circle. `gas[i]` is the fuel at station i and `cost[i]` is the fuel required to travel to the next station. "
        "You start with an empty tank. Return the unique starting station index that completes the circuit, or -1 if none exists."
    ),
    constraints=["1 <= n <= 10^5", "0 <= gas[i], cost[i] <= 10^4"],
    signature="from typing import List\n\ndef can_complete_circuit(gas: List[int], cost: List[int]) -> int:",
    function_name="can_complete_circuit",
    hints=[
        "If the total gas is less than the total cost, no start works.",
        "If the total is sufficient, a start exists. The greedy start is the station after the last time the running tank went negative.",
        "A negative tank means every station in the current segment fails as a start. Reset the tank and try the next station.",
    ],
    approaches=[
        ("Simulate every start", "O(n^2)", "O(1)", "Drive the circle from each index."),
        ("One pass with a reset", "O(n)", "O(1)", "Total surplus proves existence. The last reset is the start."),
    ],
    editorial=(
        "Let diff[i] = gas[i] - cost[i]. A feasible start has every prefix of the circular walk nonnegative. "
        "If the sum of diff is negative, return -1. Otherwise walk once, and whenever the tank drops below zero, the next index is the new candidate and the tank resets. "
        "That candidate works because every earlier segment had negative surplus and cannot be part of a feasible prefix."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):
        return -1
    tank = start = 0
    for i, (fuel, spend) in enumerate(zip(gas, cost)):
        tank += fuel - spend
        if tank < 0:
            start = i + 1
            tank = 0
    return start


def _oracle_can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    n = len(gas)
    for start in range(n):
        tank = 0
        ok = True
        for step in range(n):
            i = (start + step) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False
                break
        if ok:
            return start
    return -1


cases(
    "gas-station",
    _oracle_can_complete_circuit,
    [
        ("classic", {"gas": [1, 2, 3, 4, 5], "cost": [3, 4, 5, 1, 2]}, True, "Start at index 3."),
        ("impossible", {"gas": [2, 3, 4], "cost": [3, 4, 3]}, True, "Total gas is short."),
        ("one", {"gas": [5], "cost": [4]}, False, None),
        ("zero", {"gas": [1, 1], "cost": [1, 1]}, False, None),
        ("late", {"gas": [4, 5, 2], "cost": [5, 1, 3]}, False, None),
    ],
)


@define(
    slug="spiral-matrix",
    title="Spiral Matrix",
    difficulty="medium",
    topics=["arrays", "matrix", "simulation"],
    statement="Return all elements of the m by n matrix in clockwise spiral order.",
    constraints=["1 <= m, n <= 10", "-100 <= matrix[i][j] <= 100"],
    signature="from typing import List\n\ndef spiral_order(matrix: List[List[int]]) -> List[int]:",
    function_name="spiral_order",
    hints=[
        "Maintain four bounds: top, bottom, left, and right.",
        "Walk right along top, down along right, left along bottom, and up along left. Shrink the bound you just finished.",
        "Before the leftward and upward walks, check that the layer is still nonempty. A single row or column would otherwise be walked twice.",
    ],
    approaches=[
        ("Visited matrix", "O(mn)", "O(mn)", "Turn right whenever the next cell is out of bounds or visited."),
        ("Layer bounds", "O(mn)", "O(1)", "Four loops per layer. Output space is required either way."),
    ],
    editorial=(
        "Each layer is a rectangle. Consume its four sides and contract the bounds. "
        "The guards `top <= bottom` and `left <= right` before the reverse directions protect the middle row and the middle column of odd-sized matrices. "
        "Stop when the number of recorded cells equals m * n."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Apple"],
)
def spiral_order(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []
    out: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            out.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):
            out.append(matrix[row][right])
        right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1):
                out.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                out.append(matrix[row][left])
            left += 1
    return out


def _oracle_spiral_order(matrix: list[list[int]]) -> list[int]:
    grid = [row[:] for row in matrix]
    out: list[int] = []
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d = 0
    r = c = 0
    for _ in range(len(grid) * len(grid[0])):
        out.append(grid[r][c])
        grid[r][c] = None
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] is not None):
            d = (d + 1) % 4
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return out


cases(
    "spiral-matrix",
    _oracle_spiral_order,
    [
        ("classic", {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, True, "The spiral is 1, 2, 3, 6, 9, 8, 7, 4, 5."),
        ("rect", {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]}, True, "A 3 by 4 spiral."),
        ("row", {"matrix": [[1, 2, 3]]}, False, None),
        ("col", {"matrix": [[1], [2], [3]]}, False, None),
        ("one", {"matrix": [[7]]}, False, None),
    ],
)


@define(
    slug="valid-palindrome",
    title="Valid Palindrome",
    difficulty="easy",
    topics=["strings", "two-pointers"],
    statement="Return true when `s`, considering only alphanumeric characters and ignoring case, reads the same forward and backward.",
    constraints=["1 <= s.length <= 2 * 10^5", "s contains printable ASCII"],
    signature="def is_palindrome(s: str) -> bool:",
    function_name="is_palindrome",
    hints=[
        "Filter to lowercase alphanumeric characters, then compare with the reverse.",
        "Two pointers avoid the extra string: skip non-alphanumeric characters from both ends.",
        "Compare casefolded characters and stop at the first mismatch.",
    ],
    approaches=[
        ("Filter and reverse", "O(n)", "O(n)", "Build the cleaned string."),
        ("Two pointers", "O(n)", "O(1)", "Skip junk from both ends."),
    ],
    editorial=(
        "A palindrome here is defined on the cleaned character sequence, not on the raw string. "
        "Move the left pointer forward and the right pointer backward while they point at non-alphanumeric characters. "
        "Compare the two characters in lowercase. A mismatch returns false. Meeting in the middle returns true."
    ),
    companies=["Facebook", "Amazon", "Microsoft", "Apple"],
)
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def _oracle_is_palindrome(s: str) -> bool:
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]


cases(
    "valid-palindrome",
    _oracle_is_palindrome,
    [
        ("phrase", {"s": "A man, a plan, a canal: Panama"}, True, "The letters form a palindrome."),
        ("no", {"s": "race a car"}, True, "After cleaning, the string is not a palindrome."),
        ("empty", {"s": " "}, False, None),
        ("digits", {"s": "0P"}, False, None),
        ("simple", {"s": "abba"}, False, None),
    ],
)


@define(
    slug="roman-to-integer",
    title="Roman to Integer",
    difficulty="easy",
    topics=["strings", "math"],
    statement="Convert a valid Roman numeral `s` to an integer. Subtractive pairs are IV, IX, XL, XC, CD, and CM.",
    constraints=["1 <= s.length <= 15", "s is a valid Roman numeral in the range 1..3999"],
    signature="def roman_to_int(s: str) -> int:",
    function_name="roman_to_int",
    hints=[
        "Map I, V, X, L, C, D, and M to 1, 5, 10, 50, 100, 500, and 1000.",
        "If a smaller value appears immediately before a larger value, subtract it instead of adding it.",
        "Scanning right to left also works: add the symbol, and remember the previous value so a smaller symbol becomes negative.",
    ],
    approaches=[
        ("Replace subtractive pairs, then sum", "O(n)", "O(n)", "Turn IV into IIII-equivalent by subtracting."),
        ("One pass comparing neighbors", "O(n)", "O(1)", "Add values[s[i]] with a sign chosen by the next symbol."),
    ],
    editorial=(
        "Walk left to right. If the current symbol is smaller than the next one, subtract its value. Otherwise add it. "
        "The last symbol is always added. This encodes every subtractive pair without a special-case table, and it rejects nothing because the problem promises a valid numeral."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def roman_to_int(s: str) -> int:
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and values[ch] < values[s[i + 1]]:
            total -= values[ch]
        else:
            total += values[ch]
    return total


def _oracle_roman_to_int(s: str) -> int:
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        value = values[ch]
        if value < prev:
            total -= value
        else:
            total += value
        prev = value
    return total


cases(
    "roman-to-integer",
    _oracle_roman_to_int,
    [
        ("three", {"s": "III"}, True, "3."),
        ("four", {"s": "IV"}, True, "4, the subtractive pair."),
        ("nine", {"s": "IX"}, False, None),
        ("fifty-eight", {"s": "LVIII"}, False, None),
        ("nineteen-ninety-four", {"s": "MCMXCIV"}, False, None),
    ],
)


@define(
    slug="longest-common-prefix",
    title="Longest Common Prefix",
    difficulty="easy",
    topics=["strings"],
    statement="Return the longest common prefix shared by every string in `strs`. If there is none, return an empty string.",
    constraints=["1 <= strs.length <= 200", "0 <= strs[i].length <= 200"],
    signature="from typing import List\n\ndef longest_common_prefix(strs: List[str]) -> str:",
    function_name="longest_common_prefix",
    hints=[
        "Horizontal scanning: start with the first string and trim it against each later string.",
        "Vertical scanning: compare column i of every string until one disagrees or ends.",
        "A trie also works. For this input size it is unnecessary machinery.",
    ],
    approaches=[
        ("Sort and compare the extremes", "O(n log n * m)", "O(1)", "The common prefix of the whole set is the common prefix of the first and last strings after sorting."),
        ("Vertical scan", "O(n * m)", "O(1)", "Stop at the first mismatched column."),
    ],
    editorial=(
        "Take the first string as the candidate prefix. For each later string, shorten the candidate until that string starts with it. "
        "If the candidate becomes empty, return immediately. "
        "The vertical scan is equivalent and makes the column-wise disagreement obvious."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def longest_common_prefix(strs: list[str]) -> str:
    prefix = strs[0]
    for word in strs[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def _oracle_longest_common_prefix(strs: list[str]) -> str:
    prefix = ""
    for column in zip(*strs):
        if len(set(column)) != 1:
            break
        prefix += column[0]
    return prefix


cases(
    "longest-common-prefix",
    _oracle_longest_common_prefix,
    [
        ("flower", {"strs": ["flower", "flow", "flight"]}, True, "The prefix is fl."),
        ("none", {"strs": ["dog", "racecar", "car"]}, True, "There is no common prefix."),
        ("one", {"strs": ["alone"]}, False, None),
        ("empty-word", {"strs": ["", "a"]}, False, None),
        ("full", {"strs": ["ab", "abc", "abcd"]}, False, None),
    ],
)


@define(
    slug="longest-palindromic-substring",
    title="Longest Palindromic Substring",
    difficulty="medium",
    topics=["strings", "dynamic-programming"],
    statement=(
        "Return the longest palindromic substring of `s`. "
        "If several share the maximum length, return the one that starts earliest."
    ),
    constraints=["1 <= s.length <= 1000"],
    signature="def longest_palindrome(s: str) -> str:",
    function_name="longest_palindrome",
    hints=[
        "Every palindrome has a center. The center is one character, or the gap between two characters.",
        "Expand while the two sides match, and remember the best window.",
        "Update the best window only when the new palindrome is strictly longer, so the earliest start wins ties.",
    ],
    approaches=[
        ("Check every substring", "O(n^3)", "O(1)", "Or O(n^2) if each slice reversal is charged carefully. Still quadratic-plus."),
        ("Expand around centers", "O(n^2)", "O(1)", "2n - 1 centers, each expanded at most n steps."),
        ("Manacher", "O(n)", "O(n)", "The linear algorithm, covered again in the string-algorithms module."),
    ],
    editorial=(
        "A palindrome is determined by its center and its radius. "
        "For each index, expand the odd-length palindrome centered on the character and the even-length palindrome centered between that character and the next. "
        "Keep the longest window seen. Because centers are visited left to right and a tie does not replace the incumbent, the earliest longest substring is returned."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def longest_palindrome(s: str) -> str:
    start = end = 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for i in range(len(s)):
        for left, right in (expand(i, i), expand(i, i + 1)):
            if right - left > end - start:
                start, end = left, right
    return s[start : end + 1]


def _oracle_longest_palindrome(s: str) -> str:
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            piece = s[i:j]
            if len(piece) > len(best) and piece == piece[::-1]:
                best = piece
    return best


cases(
    "longest-palindromic-substring",
    _oracle_longest_palindrome,
    [
        ("babad", {"s": "babad"}, True, "bab starts before aba and both have length 3."),
        ("cbbd", {"s": "cbbd"}, True, "bb is the longest palindrome."),
        ("single", {"s": "a"}, False, None),
        ("even", {"s": "abba"}, False, None),
        ("whole", {"s": "racecar"}, False, None),
    ],
)
