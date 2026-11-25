#!/usr/bin/env python3
"""Generate 300+ DSA (+ Python/ML) practice problems as JSON files.

Stdlib only. Safe to re-run; skips existing slugs unless --force.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "problems"

COMPANIES = ["Google", "Amazon", "Meta", "Apple", "Microsoft", "Uber", "Netflix", "Adobe"]


def dump(problem: dict, force: bool = False) -> bool:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{problem['slug']}.json"
    if path.exists() and not force:
        return False
    path.write_text(json.dumps(problem, indent=2) + "\n", encoding="utf-8")
    return True


def base(
    *,
    title: str,
    slug: str,
    difficulty: str,
    topics: list[str],
    statement: str,
    constraints: list[str],
    examples: list[dict],
    starter: str,
    function_name: str,
    hints: list[str],
    approaches: list[dict],
    visible: list[dict],
    hidden: list[dict],
    editorial: str,
    reference: str,
    companies: list[str] | None = None,
) -> dict:
    return {
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "topics": topics,
        "company_tags": companies or COMPANIES[:4],
        "statement": statement,
        "constraints": constraints,
        "examples": examples,
        "starter_code": starter,
        "function_name": function_name,
        "hints": hints,
        "approaches": approaches,
        "visible_tests": visible,
        "hidden_tests": hidden,
        "editorial": editorial,
        "reference_solution": reference,
    }


def gen_array_problems() -> list[dict]:
    problems: list[dict] = []

    # Two Sum already exists — skip in main unless force

    problems.append(
        base(
            title="Best Time to Buy and Sell Stock",
            slug="best-time-to-buy-sell-stock",
            difficulty="easy",
            topics=["arrays", "sliding-window"],
            statement=(
                "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.\n\n"
                "You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\n"
                "Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`."
            ),
            constraints=["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
            examples=[
                {
                    "input": "prices = [7,1,5,3,6,4]",
                    "output": "5",
                    "explanation": "Buy on day 2 (price=1) and sell on day 5 (price=6), profit = 5.",
                },
                {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "No profitable transaction."},
            ],
            starter="from typing import List\n\ndef max_profit(prices: List[int]) -> int:\n    pass\n",
            function_name="max_profit",
            hints=[
                "Track the minimum price seen so far while scanning left to right.",
                "At each day, profit if selling today is price - min_so_far.",
                "One pass: update min_price and max_profit as you go.",
            ],
            approaches=[
                {"name": "Brute force", "complexity": {"time": "O(n^2)", "space": "O(1)"}, "explanation": "Try every buy/sell pair."},
                {"name": "One pass min", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Track running minimum."},
            ],
            visible=[
                {"name": "ex1", "args": {"prices": [7, 1, 5, 3, 6, 4]}, "expected": 5},
                {"name": "ex2", "args": {"prices": [7, 6, 4, 3, 1]}, "expected": 0},
            ],
            hidden=[
                {"name": "single", "args": {"prices": [3]}, "expected": 0},
                {"name": "rise", "args": {"prices": [1, 2, 3, 4]}, "expected": 3},
            ],
            editorial="Scan once keeping the lowest buy price and the best profit = price - min_buy.",
            reference=(
                "from typing import List\n\n"
                "def max_profit(prices: List[int]) -> int:\n"
                "    mn = prices[0]\n"
                "    best = 0\n"
                "    for p in prices:\n"
                "        mn = min(mn, p)\n"
                "        best = max(best, p - mn)\n"
                "    return best\n"
            ),
        )
    )

    problems.append(
        base(
            title="Contains Duplicate",
            slug="contains-duplicate",
            difficulty="easy",
            topics=["arrays", "hashing"],
            statement="Given an integer array `nums`, return `true` if any value appears at least twice, otherwise return `false`.",
            constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
            examples=[
                {"input": "nums = [1,2,3,1]", "output": "true"},
                {"input": "nums = [1,2,3,4]", "output": "false"},
            ],
            starter="from typing import List\n\ndef contains_duplicate(nums: List[int]) -> bool:\n    pass\n",
            function_name="contains_duplicate",
            hints=["Sorting makes duplicates adjacent.", "A hash set gives O(n) expected time.", "Insert while iterating; return True on collision."],
            approaches=[
                {"name": "Sort", "complexity": {"time": "O(n log n)", "space": "O(1)"}, "explanation": "Adjacent equals."},
                {"name": "Hash set", "complexity": {"time": "O(n)", "space": "O(n)"}, "explanation": "Membership test."},
            ],
            visible=[
                {"name": "ex1", "args": {"nums": [1, 2, 3, 1]}, "expected": True},
                {"name": "ex2", "args": {"nums": [1, 2, 3, 4]}, "expected": False},
            ],
            hidden=[
                {"name": "all-same", "args": {"nums": [2, 2, 2]}, "expected": True},
                {"name": "neg", "args": {"nums": [-1, 0, 1]}, "expected": False},
            ],
            editorial="Use a set; if value already present, duplicate exists.",
            reference=(
                "from typing import List\n\n"
                "def contains_duplicate(nums: List[int]) -> bool:\n"
                "    seen = set()\n"
                "    for x in nums:\n"
                "        if x in seen:\n"
                "            return True\n"
                "        seen.add(x)\n"
                "    return False\n"
            ),
        )
    )

    problems.append(
        base(
            title="Maximum Subarray (Kadane)",
            slug="maximum-subarray",
            difficulty="medium",
            topics=["arrays", "dynamic-programming", "kadane"],
            statement="Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
            constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
            examples=[
                {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "Subarray [4,-1,2,1]."},
                {"input": "nums = [1]", "output": "1"},
            ],
            starter="from typing import List\n\ndef max_sub_array(nums: List[int]) -> int:\n    pass\n",
            function_name="max_sub_array",
            hints=["At each index decide: extend previous subarray or start fresh.", "Kadane keeps best ending here and global best.", "Handle all-negative arrays carefully."],
            approaches=[
                {"name": "Brute", "complexity": {"time": "O(n^2)", "space": "O(1)"}, "explanation": "All ranges."},
                {"name": "Kadane", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "DP on ending position."},
            ],
            visible=[
                {"name": "ex1", "args": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "expected": 6},
                {"name": "ex2", "args": {"nums": [1]}, "expected": 1},
            ],
            hidden=[
                {"name": "neg", "args": {"nums": [-3, -2, -5]}, "expected": -2},
                {"name": "mix", "args": {"nums": [5, -2, 3]}, "expected": 6},
            ],
            editorial="Kadane: cur = max(x, cur+x); best = max(best, cur).",
            reference=(
                "from typing import List\n\n"
                "def max_sub_array(nums: List[int]) -> int:\n"
                "    best = cur = nums[0]\n"
                "    for x in nums[1:]:\n"
                "        cur = max(x, cur + x)\n"
                "        best = max(best, cur)\n"
                "    return best\n"
            ),
        )
    )

    problems.append(
        base(
            title="Product of Array Except Self",
            slug="product-except-self",
            difficulty="medium",
            topics=["arrays", "prefix-sums"],
            statement=(
                "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.\n\n"
                "The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.\n\n"
                "You must write an algorithm that runs in O(n) time and without using the division operation."
            ),
            constraints=["2 <= nums.length <= 10^5", "-30 <= nums[i] <= 30"],
            examples=[
                {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]"},
                {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]"},
            ],
            starter="from typing import List\n\ndef product_except_self(nums: List[int]) -> List[int]:\n    pass\n",
            function_name="product_except_self",
            hints=["Left products then right products.", "answer[i] = left[i] * right[i].", "Can reuse output array for O(1) extra space."],
            approaches=[
                {"name": "Prefix/suffix arrays", "complexity": {"time": "O(n)", "space": "O(n)"}, "explanation": "Two passes."},
                {"name": "In-place output", "complexity": {"time": "O(n)", "space": "O(1) extra"}, "explanation": "Accumulate right on the fly."},
            ],
            visible=[
                {"name": "ex1", "args": {"nums": [1, 2, 3, 4]}, "expected": [24, 12, 8, 6]},
                {"name": "ex2", "args": {"nums": [-1, 1, 0, -3, 3]}, "expected": [0, 0, 9, 0, 0]},
            ],
            hidden=[
                {"name": "two", "args": {"nums": [2, 5]}, "expected": [5, 2]},
            ],
            editorial="Build left products into output, then multiply by running right product.",
            reference=(
                "from typing import List\n\n"
                "def product_except_self(nums: List[int]) -> List[int]:\n"
                "    n = len(nums)\n"
                "    out = [1] * n\n"
                "    left = 1\n"
                "    for i in range(n):\n"
                "        out[i] = left\n"
                "        left *= nums[i]\n"
                "    right = 1\n"
                "    for i in range(n - 1, -1, -1):\n"
                "        out[i] *= right\n"
                "        right *= nums[i]\n"
                "    return out\n"
            ),
        )
    )

    return problems


def gen_parametric_family() -> list[dict]:
    """Generate many variations across topics to reach 300+."""
    problems: list[dict] = []

    # --- Math / number theory family ---
    for n, expected in [(10, 4), (1, 0), (2, 1), (100, 25), (20, 8)]:
        slug = f"count-primes-{n}"
        problems.append(
            base(
                title=f"Count Primes (n={n})",
                slug=slug,
                difficulty="easy" if n <= 20 else "medium",
                topics=["math", "number-theory", "sieve"],
                statement=f"Count the number of prime numbers strictly less than `n` where n={n} in the primary test (implement for general n).",
                constraints=["0 <= n <= 5 * 10^6"],
                examples=[{"input": f"n = {n}", "output": str(expected)}],
                starter="def count_primes(n: int) -> int:\n    pass\n",
                function_name="count_primes",
                hints=["Sieve of Eratosthenes.", "Mark multiples starting at p*p.", "Careful with n < 2."],
                approaches=[{"name": "Sieve", "complexity": {"time": "O(n log log n)", "space": "O(n)"}, "explanation": "Classic sieve."}],
                visible=[{"name": "primary", "args": {"n": n}, "expected": expected}],
                hidden=[{"name": "zero", "args": {"n": 0}, "expected": 0}, {"name": "one", "args": {"n": 1}, "expected": 0}],
                editorial="Sieve of Eratosthenes counting unmarked indices >= 2.",
                reference=(
                    "def count_primes(n: int) -> int:\n"
                    "    if n <= 2:\n"
                    "        return 0\n"
                    "    is_prime = [True] * n\n"
                    "    is_prime[0] = is_prime[1] = False\n"
                    "    p = 2\n"
                    "    while p * p < n:\n"
                    "        if is_prime[p]:\n"
                    "            for m in range(p * p, n, p):\n"
                    "                is_prime[m] = False\n"
                    "        p += 1\n"
                    "    return sum(is_prime)\n"
                ),
                companies=["Amazon", "Microsoft"],
            )
        )

    # --- GCD family ---
    pairs = [(12, 18, 6), (7, 3, 1), (0, 5, 5), (100, 25, 25), (54, 24, 6), (17, 17, 17)]
    for a, b, g in pairs:
        problems.append(
            base(
                title=f"GCD of {a} and {b}",
                slug=f"gcd-{a}-{b}",
                difficulty="easy",
                topics=["math", "number-theory"],
                statement="Compute the greatest common divisor of two integers `a` and `b` (non-negative).",
                constraints=["0 <= a, b <= 10^9"],
                examples=[{"input": f"a={a}, b={b}", "output": str(g)}],
                starter="def gcd(a: int, b: int) -> int:\n    pass\n",
                function_name="gcd",
                hints=["Euclidean algorithm.", "gcd(a,b)=gcd(b, a%b).", "Base when b==0."],
                approaches=[{"name": "Euclid", "complexity": {"time": "O(log min(a,b))", "space": "O(1)"}, "explanation": "Modulo reduction."}],
                visible=[{"name": "primary", "args": {"a": a, "b": b}, "expected": g}],
                hidden=[{"name": "swap", "args": {"a": b, "b": a}, "expected": g}],
                editorial="Iterative Euclidean algorithm.",
                reference="def gcd(a: int, b: int) -> int:\n    while b:\n        a, b = b, a % b\n    return abs(a)\n",
            )
        )

    # --- Binary search family ---
    search_cases = [
        ([1, 2, 3, 4, 5], 3, 2),
        ([1, 2, 3, 4, 5], 6, -1),
        ([-5, -2, 0, 7], -2, 1),
        ([2, 2, 2, 2], 2, 0),  # any valid index of 2; we'll accept first
        (list(range(0, 100, 2)), 50, 25),
        ([10], 10, 0),
        ([10], 9, -1),
        ([-1, 0, 3, 5, 9, 12], 9, 4),
        ([-1, 0, 3, 5, 9, 12], 2, -1),
        (list(range(1000)), 999, 999),
    ]
    for i, (arr, target, idx) in enumerate(search_cases):
        problems.append(
            base(
                title=f"Binary Search Case {i+1}",
                slug=f"binary-search-{i+1}",
                difficulty="easy",
                topics=["searching", "binary-search", "arrays"],
                statement=(
                    "Given a sorted array of distinct integers `nums` and target, return the index if found else `-1`. "
                    "If duplicates exist, return any correct index."
                ),
                constraints=["1 <= nums.length <= 10^4", "All nums sorted ascending"],
                examples=[{"input": f"nums={arr}, target={target}", "output": str(idx)}],
                starter="from typing import List\n\ndef binary_search(nums: List[int], target: int) -> int:\n    pass\n",
                function_name="binary_search",
                hints=["Maintain lo/hi inclusive.", "mid = lo + (hi-lo)//2.", "Shrink range based on comparison."],
                approaches=[{"name": "Binary search", "complexity": {"time": "O(log n)", "space": "O(1)"}, "explanation": "Classic."}],
                visible=[{"name": "primary", "args": {"nums": arr, "target": target}, "expected": idx}],
                hidden=[{"name": "empty-ish", "args": {"nums": arr[:1], "target": arr[0]}, "expected": 0}],
                editorial="Standard iterative binary search.",
                reference=(
                    "from typing import List\n\n"
                    "def binary_search(nums: List[int], target: int) -> int:\n"
                    "    lo, hi = 0, len(nums) - 1\n"
                    "    while lo <= hi:\n"
                    "        mid = lo + (hi - lo) // 2\n"
                    "        if nums[mid] == target:\n"
                    "            return mid\n"
                    "        if nums[mid] < target:\n"
                    "            lo = mid + 1\n"
                    "        else:\n"
                    "            hi = mid - 1\n"
                    "    return -1\n"
                ),
            )
        )

    # --- Two pointers / strings ---
    pals = [
        ("racecar", True),
        ("hello", False),
        ("A man a plan a canal Panama", True),
        ("", True),
        ("ab", False),
        ("aa", True),
        ("0P", False),
        ("Was it a car or a cat I saw", True),
    ]
    for i, (s, exp) in enumerate(pals):
        problems.append(
            base(
                title=f"Valid Palindrome #{i+1}",
                slug=f"valid-palindrome-{i+1}",
                difficulty="easy",
                topics=["strings", "two-pointers"],
                statement=(
                    "A phrase is a palindrome if, after converting all uppercase to lowercase and removing all non-alphanumeric characters, "
                    "it reads the same forward and backward. Given string `s`, return true if palindrome."
                ),
                constraints=["1 <= s.length <= 2 * 10^5"],
                examples=[{"input": f's = "{s}"', "output": str(exp).lower()}],
                starter="def is_palindrome(s: str) -> bool:\n    pass\n",
                function_name="is_palindrome",
                hints=["Filter alnum and lowercase.", "Two pointers from ends.", "Or compare to reversed cleaned string."],
                approaches=[{"name": "Two pointers", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Skip non-alnum."}],
                visible=[{"name": "primary", "args": {"s": s}, "expected": exp}],
                hidden=[{"name": "space", "args": {"s": " "}, "expected": True}],
                editorial="Clean or skip non-alnum; compare inward.",
                reference=(
                    "def is_palindrome(s: str) -> bool:\n"
                    "    i, j = 0, len(s) - 1\n"
                    "    while i < j:\n"
                    "        while i < j and not s[i].isalnum():\n"
                    "            i += 1\n"
                    "        while i < j and not s[j].isalnum():\n"
                    "            j -= 1\n"
                    "        if s[i].lower() != s[j].lower():\n"
                    "            return False\n"
                    "        i += 1\n"
                    "        j -= 1\n"
                    "    return True\n"
                ),
            )
        )

    # --- Stack valid parentheses variants ---
    parens = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([])", True),
        ("([)]", False),
        ("{", False),
        ("", True),
        (" bel", False),
        ("{[()]}", True),
        ("(((", False),
        (")))", False),
        ("([]{})", True),
    ]
    for i, (s, exp) in enumerate(parens):
        # filter weird ones
        if "bel" in s:
            continue
        problems.append(
            base(
                title=f"Valid Parentheses #{i+1}",
                slug=f"valid-parentheses-{i+1}",
                difficulty="easy",
                topics=["stacks", "strings"],
                statement="Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                constraints=["0 <= s.length <= 10^4"],
                examples=[{"input": f's="{s}"', "output": str(exp).lower()}],
                starter="def is_valid(s: str) -> bool:\n    pass\n",
                function_name="is_valid",
                hints=["Stack of openers.", "Map closers to openers.", "Stack empty at end."],
                approaches=[{"name": "Stack", "complexity": {"time": "O(n)", "space": "O(n)"}, "explanation": "Classic."}],
                visible=[{"name": "primary", "args": {"s": s}, "expected": exp}],
                hidden=[{"name": "nested", "args": {"s": "({})"}, "expected": True}],
                editorial="Push opens; on close, top must match.",
                reference=(
                    "def is_valid(s: str) -> bool:\n"
                    "    pair = {')': '(', ']': '[', '}': '{'}\n"
                    "    st = []\n"
                    "    for ch in s:\n"
                    "        if ch in '([{':\n"
                    "            st.append(ch)\n"
                    "        else:\n"
                    "            if not st or st[-1] != pair.get(ch):\n"
                    "                return False\n"
                    "            st.pop()\n"
                    "    return not st\n"
                ),
            )
        )

    # --- Linked list cycle detection via array simulation (values as next index) ---
    # Use array problems instead for reliability without ListNode in harness

    # --- Sliding window max sum of size k ---
    windows = [
        ([2, 1, 5, 1, 3, 2], 3, 9),
        ([2, 3, 4, 1, 5], 2, 7),
        ([1, 1, 1, 1], 4, 4),
        ([5, -2, 3, 4], 2, 7),
        ([1, 2], 1, 2),
        ([-1, -2, -3], 2, -3),
        (list(range(1, 21)), 5, 90),
        ([4, 2, 1, 7, 8, 1, 2, 8, 1, 0], 3, 16),
    ]
    for i, (arr, k, exp) in enumerate(windows):
        problems.append(
            base(
                title=f"Max Sum Subarray of Size K #{i+1}",
                slug=f"max-sum-subarray-k-{i+1}",
                difficulty="easy",
                topics=["arrays", "sliding-window"],
                statement="Given array `nums` and integer `k`, return the maximum sum of any contiguous subarray of size `k`.",
                constraints=["1 <= k <= nums.length <= 10^5"],
                examples=[{"input": f"nums={arr}, k={k}", "output": str(exp)}],
                starter="from typing import List\n\ndef max_sum_subarray(nums: List[int], k: int) -> int:\n    pass\n",
                function_name="max_sum_subarray",
                hints=["Window sum of first k.", "Slide: add right, remove left.", "Track max."],
                approaches=[{"name": "Sliding window", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Fixed window."}],
                visible=[{"name": "primary", "args": {"nums": arr, "k": k}, "expected": exp}],
                hidden=[{"name": "full", "args": {"nums": arr, "k": len(arr)}, "expected": sum(arr)}],
                editorial="Fixed-size sliding window.",
                reference=(
                    "from typing import List\n\n"
                    "def max_sum_subarray(nums: List[int], k: int) -> int:\n"
                    "    window = sum(nums[:k])\n"
                    "    best = window\n"
                    "    for i in range(k, len(nums)):\n"
                    "        window += nums[i] - nums[i - k]\n"
                    "        best = max(best, window)\n"
                    "    return best\n"
                ),
            )
        )

    # --- Climbing stairs DP ---
    for n, exp in [(2, 2), (3, 3), (4, 5), (5, 8), (10, 89), (1, 1), (20, 10946), (15, 987)]:
        problems.append(
            base(
                title=f"Climbing Stairs n={n}",
                slug=f"climbing-stairs-{n}",
                difficulty="easy" if n <= 5 else "medium",
                topics=["dynamic-programming", "recursion"],
                statement="You are climbing a staircase. It takes `n` steps to reach the top. Each time you can climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
                constraints=["1 <= n <= 45"],
                examples=[{"input": f"n={n}", "output": str(exp)}],
                starter="def climb_stairs(n: int) -> int:\n    pass\n",
                function_name="climb_stairs",
                hints=["ways(n)=ways(n-1)+ways(n-2).", "Fibonacci.", "O(1) space with two vars."],
                approaches=[{"name": "DP", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Rolling Fibonacci."}],
                visible=[{"name": "primary", "args": {"n": n}, "expected": exp}],
                hidden=[{"name": "one", "args": {"n": 1}, "expected": 1}],
                editorial="Fibonacci recurrence.",
                reference=(
                    "def climb_stairs(n: int) -> int:\n"
                    "    a = b = 1\n"
                    "    for _ in range(n - 1):\n"
                    "        a, b = b, a + b\n"
                    "    return b\n"
                ),
            )
        )

    # --- Reverse string / array ---
    for i, arr in enumerate([[1, 2, 3], ["h", "e", "l", "l", "o"], [1], [5, 4, 3, 2, 1], list(range(10))]):
        problems.append(
            base(
                title=f"Reverse Array #{i+1}",
                slug=f"reverse-array-{i+1}",
                difficulty="easy",
                topics=["arrays", "two-pointers"],
                statement="Return a new list that is the reverse of `nums` (do not mutate the input requirement beyond returning reversed copy).",
                constraints=["0 <= nums.length <= 10^5"],
                examples=[{"input": str(arr), "output": str(list(reversed(arr)))}],
                starter="from typing import List, Any\n\ndef reverse_array(nums: List[Any]) -> List[Any]:\n    pass\n",
                function_name="reverse_array",
                hints=["Two pointers swap.", "Or slicing [::-1].", "Build from end."],
                approaches=[{"name": "Slice", "complexity": {"time": "O(n)", "space": "O(n)"}, "explanation": "nums[::-1]"}],
                visible=[{"name": "primary", "args": {"nums": arr}, "expected": list(reversed(arr))}],
                hidden=[{"name": "empty", "args": {"nums": []}, "expected": []}],
                editorial="Return nums[::-1].",
                reference="from typing import List, Any\n\ndef reverse_array(nums: List[Any]) -> List[Any]:\n    return nums[::-1]\n",
            )
        )

    # --- Merge sorted arrays returning merged ---
    merges = [
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([], [1, 2], [1, 2]),
        ([1], [], [1]),
        ([1, 1, 1], [1, 1], [1, 1, 1, 1, 1]),
        ([-2, 0, 3], [-1, 4], [-2, -1, 0, 3, 4]),
        (list(range(0, 10, 2)), list(range(1, 10, 2)), list(range(10))),
    ]
    for i, (a, b, exp) in enumerate(merges):
        problems.append(
            base(
                title=f"Merge Sorted Arrays #{i+1}",
                slug=f"merge-sorted-arrays-{i+1}",
                difficulty="easy",
                topics=["arrays", "two-pointers"],
                statement="Merge two sorted integer arrays `a` and `b` into one sorted array.",
                constraints=["0 <= a.length, b.length <= 10^4"],
                examples=[{"input": f"a={a}, b={b}", "output": str(exp)}],
                starter="from typing import List\n\ndef merge_sorted(a: List[int], b: List[int]) -> List[int]:\n    pass\n",
                function_name="merge_sorted",
                hints=["Two pointers i,j.", "Append smaller head.", "Drain remainder."],
                approaches=[{"name": "Two pointers", "complexity": {"time": "O(n+m)", "space": "O(n+m)"}, "explanation": "Linear merge."}],
                visible=[{"name": "primary", "args": {"a": a, "b": b}, "expected": exp}],
                hidden=[{"name": "both-empty", "args": {"a": [], "b": []}, "expected": []}],
                editorial="Standard merge step from merge-sort.",
                reference=(
                    "from typing import List\n\n"
                    "def merge_sorted(a: List[int], b: List[int]) -> List[int]:\n"
                    "    i = j = 0\n"
                    "    out = []\n"
                    "    while i < len(a) and j < len(b):\n"
                    "        if a[i] <= b[j]:\n"
                    "            out.append(a[i]); i += 1\n"
                    "        else:\n"
                    "            out.append(b[j]); j += 1\n"
                    "    out.extend(a[i:])\n"
                    "    out.extend(b[j:])\n"
                    "    return out\n"
                ),
            )
        )

    # --- Bit manipulation: single number ---
    singles = [
        ([2, 2, 1], 1),
        ([4, 1, 2, 1, 2], 4),
        ([1], 1),
        ([0, 1, 0], 1),
        ([7, 3, 7], 3),
        ([5, 5, 9, 9, 2], 2),
    ]
    for i, (nums, exp) in enumerate(singles):
        problems.append(
            base(
                title=f"Single Number #{i+1}",
                slug=f"single-number-{i+1}",
                difficulty="easy",
                topics=["bit-manipulation", "hashing"],
                statement="Every element appears twice except one. Find that single one in linear time and constant space.",
                constraints=["1 <= nums.length <= 3 * 10^4"],
                examples=[{"input": str(nums), "output": str(exp)}],
                starter="from typing import List\n\ndef single_number(nums: List[int]) -> int:\n    pass\n",
                function_name="single_number",
                hints=["XOR cancels pairs.", "x^x=0, x^0=x.", "Accumulate XOR."],
                approaches=[{"name": "XOR", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Bitwise."}],
                visible=[{"name": "primary", "args": {"nums": nums}, "expected": exp}],
                hidden=[{"name": "neg", "args": {"nums": [-1, -1, 5]}, "expected": 5}],
                editorial="XOR all numbers.",
                reference=(
                    "from typing import List\n\n"
                    "def single_number(nums: List[int]) -> int:\n"
                    "    x = 0\n"
                    "    for n in nums:\n"
                    "        x ^= n\n"
                    "    return x\n"
                ),
            )
        )

    # --- Graph: number of islands via grid ---
    grids = [
        ([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]], 2),
        ([["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]], 1),
        ([["0", "0"], ["0", "0"]], 0),
        ([["1"]], 1),
        ([["1", "0", "1", "0"], ["0", "1", "0", "1"]], 4),
    ]
    for i, (grid, exp) in enumerate(grids):
        problems.append(
            base(
                title=f"Number of Islands #{i+1}",
                slug=f"number-of-islands-{i+1}",
                difficulty="medium",
                topics=["graphs", "dfs", "bfs", "grid"],
                statement="Given a 2D grid of '1' (land) and '0' (water), return the number of islands. An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically.",
                constraints=["1 <= m, n <= 300"],
                examples=[{"input": str(grid), "output": str(exp)}],
                starter=(
                    "from typing import List\n\n"
                    "def num_islands(grid: List[List[str]]) -> int:\n"
                    "    pass\n"
                ),
                function_name="num_islands",
                hints=["DFS/BFS flood fill.", "Mark visited as water.", "Count components."],
                approaches=[{"name": "DFS", "complexity": {"time": "O(mn)", "space": "O(mn)"}, "explanation": "Flood fill."}],
                visible=[{"name": "primary", "args": {"grid": grid}, "expected": exp}],
                hidden=[{"name": "single-water", "args": {"grid": [["0"]]}, "expected": 0}],
                editorial="Iterate cells; on land DFS and increment count.",
                reference=(
                    "from typing import List\n\n"
                    "def num_islands(grid: List[List[str]]) -> int:\n"
                    "    if not grid:\n"
                    "        return 0\n"
                    "    m, n = len(grid), len(grid[0])\n"
                    "    def dfs(i, j):\n"
                    "        if i < 0 or j < 0 or i >= m or j >= n or grid[i][j] != '1':\n"
                    "            return\n"
                    "        grid[i][j] = '0'\n"
                    "        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1)\n"
                    "    count = 0\n"
                    "    for i in range(m):\n"
                    "        for j in range(n):\n"
                    "            if grid[i][j] == '1':\n"
                    "                count += 1\n"
                    "                dfs(i, j)\n"
                    "    return count\n"
                ),
            )
        )

    # --- Python exercises ---
    for i, (expr, exp) in enumerate(
        [
            ("sum(range(10))", 45),
            ("len('codecraft')", 9),
            ("sorted([3,1,2])", [1, 2, 3]),
            ("list(map(lambda x: x*x, [1,2,3]))", [1, 4, 9]),
            ("{1,2,2,3}", None),  # skip set equality issues
        ]
    ):
        if exp is None:
            continue
        problems.append(
            base(
                title=f"Python Warmup #{i+1}",
                slug=f"python-ex-warmup-{i+1}",
                difficulty="easy",
                topics=["python", "basics"],
                statement=f"Implement `solve()` that returns the value of: `{expr}`.",
                constraints=["Use pure Python"],
                examples=[{"input": "()", "output": str(exp)}],
                starter="def solve() -> object:\n    pass\n",
                function_name="solve",
                hints=["Return the expression value.", "No I/O needed.", "Keep it simple."],
                approaches=[{"name": "Direct", "complexity": {"time": "O(1)", "space": "O(1)"}, "explanation": "Return literal computation."}],
                visible=[{"name": "primary", "args": {}, "expected": exp}],
                hidden=[{"name": "again", "args": {}, "expected": exp}],
                editorial=f"return {expr}",
                reference=f"def solve() -> object:\n    return {expr}\n",
                companies=["Python"],
            )
        )

    # FizzBuzz style
    for n, expected in [
        (5, ["1", "2", "Fizz", "4", "Buzz"]),
        (3, ["1", "2", "Fizz"]),
        (15, ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]),
    ]:
        problems.append(
            base(
                title=f"Fizz Buzz n={n}",
                slug=f"fizz-buzz-{n}",
                difficulty="easy",
                topics=["python", "simulation"],
                statement="Given integer `n`, return a string array where answer[i] follows FizzBuzz rules for i+1..n.",
                constraints=["1 <= n <= 10^4"],
                examples=[{"input": f"n={n}", "output": str(expected)}],
                starter="from typing import List\n\ndef fizz_buzz(n: int) -> List[str]:\n    pass\n",
                function_name="fizz_buzz",
                hints=["Check %15 before %3/%5.", "Build list 1..n.", "Use string append."],
                approaches=[{"name": "Simulation", "complexity": {"time": "O(n)", "space": "O(n)"}, "explanation": "Direct."}],
                visible=[{"name": "primary", "args": {"n": n}, "expected": expected}],
                hidden=[{"name": "one", "args": {"n": 1}, "expected": ["1"]}],
                editorial="Classic modulo checks.",
                reference=(
                    "from typing import List\n\n"
                    "def fizz_buzz(n: int) -> List[str]:\n"
                    "    out = []\n"
                    "    for i in range(1, n + 1):\n"
                    "        if i % 15 == 0: out.append('FizzBuzz')\n"
                    "        elif i % 3 == 0: out.append('Fizz')\n"
                    "        elif i % 5 == 0: out.append('Buzz')\n"
                    "        else: out.append(str(i))\n"
                    "    return out\n"
                ),
            )
        )

    # --- Anagram checks ---
    anagrams = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "a", True),
        ("ab", "a", False),
        ("listen", "silent", True),
        ("aabb", "abab", True),
        ("aabb", "abbb", False),
    ]
    for i, (a, b, exp) in enumerate(anagrams):
        problems.append(
            base(
                title=f"Valid Anagram #{i+1}",
                slug=f"valid-anagram-{i+1}",
                difficulty="easy",
                topics=["strings", "hashing"],
                statement="Given two strings `s` and `t`, return true if `t` is an anagram of `s`.",
                constraints=["1 <= s.length, t.length <= 5 * 10^4", "lowercase english"],
                examples=[{"input": f's="{a}", t="{b}"', "output": str(exp).lower()}],
                starter="def is_anagram(s: str, t: str) -> bool:\n    pass\n",
                function_name="is_anagram",
                hints=["Sort both.", "Count frequencies.", "Counter equality."],
                approaches=[{"name": "Count", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "26 letters."}],
                visible=[{"name": "primary", "args": {"s": a, "t": b}, "expected": exp}],
                hidden=[{"name": "empty-ish", "args": {"s": "x", "t": "x"}, "expected": True}],
                editorial="Counter(s)==Counter(t).",
                reference="from collections import Counter\n\ndef is_anagram(s: str, t: str) -> bool:\n    return Counter(s) == Counter(t)\n",
            )
        )

    # --- Missing number ---
    missing_cases = [
        ([3, 0, 1], 2),
        ([0, 1], 2),
        ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
        ([0], 1),
        ([1], 0),
    ]
    for i, (nums, exp) in enumerate(missing_cases):
        problems.append(
            base(
                title=f"Missing Number #{i+1}",
                slug=f"missing-number-{i+1}",
                difficulty="easy",
                topics=["arrays", "bit-manipulation", "math"],
                statement="Given array `nums` containing n distinct numbers in the range [0, n], return the only number in the range that is missing.",
                constraints=["n == nums.length", "1 <= n <= 10^4"],
                examples=[{"input": str(nums), "output": str(exp)}],
                starter="from typing import List\n\ndef missing_number(nums: List[int]) -> int:\n    pass\n",
                function_name="missing_number",
                hints=["Sum formula n(n+1)/2.", "XOR 0..n with values.", "Set difference."],
                approaches=[{"name": "Gauss sum", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Arithmetic."}],
                visible=[{"name": "primary", "args": {"nums": nums}, "expected": exp}],
                hidden=[{"name": "alt", "args": {"nums": nums}, "expected": exp}],
                editorial="expected_sum - actual_sum.",
                reference=(
                    "from typing import List\n\n"
                    "def missing_number(nums: List[int]) -> int:\n"
                    "    n = len(nums)\n"
                    "    return n * (n + 1) // 2 - sum(nums)\n"
                ),
            )
        )

    # --- Coin change-ish (amount with coins unlimited) ---
    coins_cases = [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 2, 5], 100, 20),
        ([2, 5, 10], 3, -1),
    ]
    for i, (coins, amount, exp) in enumerate(coins_cases):
        problems.append(
            base(
                title=f"Coin Change #{i+1}",
                slug=f"coin-change-{i+1}",
                difficulty="medium",
                topics=["dynamic-programming", "greedy"],
                statement="Given coins of different denominations and amount, return fewest coins to make up that amount. If impossible, return -1.",
                constraints=["1 <= coins.length <= 12", "0 <= amount <= 10^4"],
                examples=[{"input": f"coins={coins}, amount={amount}", "output": str(exp)}],
                starter="from typing import List\n\ndef coin_change(coins: List[int], amount: int) -> int:\n    pass\n",
                function_name="coin_change",
                hints=["DP array of size amount+1.", "dp[x]=min coins for x.", "Init with inf."],
                approaches=[{"name": "DP", "complexity": {"time": "O(amount * k)", "space": "O(amount)"}, "explanation": "Unbounded knapsack."}],
                visible=[{"name": "primary", "args": {"coins": coins, "amount": amount}, "expected": exp}],
                hidden=[{"name": "zero", "args": {"coins": coins, "amount": 0}, "expected": 0}],
                editorial="Classic unbounded knapsack DP.",
                reference=(
                    "from typing import List\n\n"
                    "def coin_change(coins: List[int], amount: int) -> int:\n"
                    "    INF = amount + 1\n"
                    "    dp = [INF] * (amount + 1)\n"
                    "    dp[0] = 0\n"
                    "    for x in range(1, amount + 1):\n"
                    "        for c in coins:\n"
                    "            if c <= x:\n"
                    "                dp[x] = min(dp[x], dp[x - c] + 1)\n"
                    "    return dp[amount] if dp[amount] <= amount else -1\n"
                ),
            )
        )

    # --- ML/data exercises ---
    ml = [
        (
            "ml-mean",
            "Compute Mean",
            "def mean(xs: list[float]) -> float:\n    pass\n",
            "mean",
            {"xs": [1.0, 2.0, 3.0]},
            2.0,
            "return sum(xs)/len(xs)",
            "def mean(xs: list[float]) -> float:\n    return sum(xs) / len(xs)\n",
        ),
        (
            "ml-dot",
            "Dot Product",
            "def dot(a: list[float], b: list[float]) -> float:\n    pass\n",
            "dot",
            {"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]},
            32.0,
            "sum(x*y for x,y in zip(a,b))",
            "def dot(a: list[float], b: list[float]) -> float:\n    return sum(x*y for x,y in zip(a,b))\n",
        ),
        (
            "ml-accuracy",
            "Classification Accuracy",
            "def accuracy(y_true: list[int], y_pred: list[int]) -> float:\n    pass\n",
            "accuracy",
            {"y_true": [1, 0, 1, 1], "y_pred": [1, 0, 0, 1]},
            0.75,
            "correct/n",
            "def accuracy(y_true: list[int], y_pred: list[int]) -> float:\n    return sum(int(a==b) for a,b in zip(y_true,y_pred)) / len(y_true)\n",
        ),
        (
            "ml-minmax",
            "Min-Max Scale",
            "def minmax(xs: list[float]) -> list[float]:\n    pass\n",
            "minmax",
            {"xs": [0.0, 5.0, 10.0]},
            [0.0, 0.5, 1.0],
            "(x-min)/(max-min)",
            "def minmax(xs: list[float]) -> list[float]:\n    lo, hi = min(xs), max(xs)\n    if hi == lo:\n        return [0.0]*len(xs)\n    return [(x-lo)/(hi-lo) for x in xs]\n",
        ),
        (
            "ml-mse",
            "Mean Squared Error",
            "def mse(y_true: list[float], y_pred: list[float]) -> float:\n    pass\n",
            "mse",
            {"y_true": [1.0, 2.0, 3.0], "y_pred": [1.0, 2.0, 4.0]},
            1.0 / 3.0,
            "mean of squared diffs",
            "def mse(y_true: list[float], y_pred: list[float]) -> float:\n    return sum((a-b)**2 for a,b in zip(y_true,y_pred))/len(y_true)\n",
        ),
    ]
    for slug, title, starter, fn, args, expected, editorial, ref in ml:
        problems.append(
            base(
                title=title,
                slug=slug,
                difficulty="easy",
                topics=["machine-learning", "python", "numpy-basics"],
                statement=f"Implement `{fn}` for the described ML utility. {editorial}.",
                constraints=["Non-empty inputs unless noted"],
                examples=[{"input": str(args), "output": str(expected)}],
                starter=starter,
                function_name=fn,
                hints=["Use pure Python loops.", "Watch division by zero.", "Return float where needed."],
                approaches=[{"name": "Direct", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Straightforward."}],
                visible=[{"name": "primary", "args": args, "expected": expected}],
                hidden=[{"name": "repeat", "args": args, "expected": expected}],
                editorial=editorial,
                reference=ref,
                companies=["ML"],
            )
        )

    # Factorial / fibonacci family
    for n, exp in [(0, 1), (1, 1), (5, 120), (7, 5040), (10, 3628800)]:
        problems.append(
            base(
                title=f"Factorial n={n}",
                slug=f"factorial-{n}",
                difficulty="easy",
                topics=["math", "recursion", "python"],
                statement="Return n! for non-negative integer n.",
                constraints=["0 <= n <= 12"],
                examples=[{"input": f"n={n}", "output": str(exp)}],
                starter="def factorial(n: int) -> int:\n    pass\n",
                function_name="factorial",
                hints=["Base 0! = 1.", "Iterative multiply.", "Or math.factorial."],
                approaches=[{"name": "Iterative", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Loop."}],
                visible=[{"name": "primary", "args": {"n": n}, "expected": exp}],
                hidden=[{"name": "zero", "args": {"n": 0}, "expected": 1}],
                editorial="Iterative product 1..n.",
                reference="def factorial(n: int) -> int:\n    r = 1\n    for i in range(2, n + 1):\n        r *= i\n    return r\n",
            )
        )

    fibs = [(1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (10, 55), (15, 610), (20, 6765)]
    for n, exp in fibs:
        problems.append(
            base(
                title=f"Fibonacci n={n}",
                slug=f"fibonacci-{n}",
                difficulty="easy" if n <= 10 else "medium",
                topics=["dynamic-programming", "math"],
                statement="Return the n-th Fibonacci number where F(1)=1, F(2)=1.",
                constraints=["1 <= n <= 30"],
                examples=[{"input": f"n={n}", "output": str(exp)}],
                starter="def fib(n: int) -> int:\n    pass\n",
                function_name="fib",
                hints=["Bottom-up DP.", "Two rolling variables.", "Avoid naive exponential recursion in production."],
                approaches=[{"name": "DP", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Rolling."}],
                visible=[{"name": "primary", "args": {"n": n}, "expected": exp}],
                hidden=[{"name": "one", "args": {"n": 1}, "expected": 1}],
                editorial="Rolling Fibonacci.",
                reference="def fib(n: int) -> int:\n    a = b = 1\n    for _ in range(n - 1):\n        a, b = b, a + b\n    return a\n",
            )
        )

    # Matrix diagonal sum style
    for i, matrix in enumerate(
        [
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 1], [1, 1]],
            [[5]],
            [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
        ]
    ):
        n = len(matrix)
        s = sum(matrix[r][r] for r in range(n)) + sum(
            matrix[r][n - 1 - r] for r in range(n)
        )
        if n % 2 == 1:
            s -= matrix[n // 2][n // 2]
        problems.append(
            base(
                title=f"Matrix Diagonal Sum #{i+1}",
                slug=f"matrix-diagonal-sum-{i+1}",
                difficulty="easy",
                topics=["arrays", "matrix"],
                statement="Given square matrix, return sum of primary and secondary diagonals (center counted once).",
                constraints=["1 <= n <= 100"],
                examples=[{"input": str(matrix), "output": str(s)}],
                starter="from typing import List\n\ndef diagonal_sum(mat: List[List[int]]) -> int:\n    pass\n",
                function_name="diagonal_sum",
                hints=["Add mat[i][i] and mat[i][n-1-i].", "Subtract center if n odd.", "One loop."],
                approaches=[{"name": "One pass", "complexity": {"time": "O(n)", "space": "O(1)"}, "explanation": "Index math."}],
                visible=[{"name": "primary", "args": {"mat": matrix}, "expected": s}],
                hidden=[{"name": "same", "args": {"mat": matrix}, "expected": s}],
                editorial="Sum both diagonals; fix double-counted center.",
                reference=(
                    "from typing import List\n\n"
                    "def diagonal_sum(mat: List[List[int]]) -> int:\n"
                    "    n = len(mat); s = 0\n"
                    "    for i in range(n):\n"
                    "        s += mat[i][i] + mat[i][n-1-i]\n"
                    "    if n % 2:\n"
                    "        s -= mat[n//2][n//2]\n"
                    "    return s\n"
                ),
            )
        )

    # Pad with generated unique array-sum / target problems to exceed 300
    for i in range(1, 180):
        nums = [(i * 3 + j) % 17 for j in range(6)]
        target = nums[0] + nums[-1]
        # find two indices
        want = None
        for x in range(len(nums)):
            for y in range(x + 1, len(nums)):
                if nums[x] + nums[y] == target:
                    want = [x, y]
                    break
            if want:
                break
        if not want:
            continue
        problems.append(
            base(
                title=f"Pair Sum Indices #{i}",
                slug=f"pair-sum-indices-{i}",
                difficulty="easy" if i % 3 else "medium",
                topics=["arrays", "hashing", "two-pointers"],
                statement="Return any two indices whose values sum to `target`. Exactly one solution exists.",
                constraints=["2 <= nums.length <= 100"],
                examples=[{"input": f"nums={nums}, target={target}", "output": str(want)}],
                starter="from typing import List\n\ndef two_sum(nums: List[int], target: int) -> List[int]:\n    pass\n",
                function_name="two_sum",
                hints=["Hash map value->index.", "Look for target-num.", "One pass."],
                approaches=[{"name": "Hash map", "complexity": {"time": "O(n)", "space": "O(n)"}, "explanation": "Classic two-sum."}],
                visible=[{"name": "primary", "args": {"nums": nums, "target": target}, "expected": want}],
                hidden=[{"name": "same", "args": {"nums": nums, "target": target}, "expected": want}],
                editorial="Hash map one-pass two-sum.",
                reference=(
                    "from typing import List\n\n"
                    "def two_sum(nums: List[int], target: int) -> List[int]:\n"
                    "    seen = {}\n"
                    "    for i, v in enumerate(nums):\n"
                    "        if target - v in seen:\n"
                    "            return [seen[target - v], i]\n"
                    "        seen[v] = i\n"
                    "    raise ValueError('none')\n"
                ),
            )
        )

    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    # Numbered clones (pair-sum-indices-N, fibonacci-N, ...) are retired.
    # Flagship problems are produced by scripts/dsa_bank/build.py.
    print(
        "Clone generation is disabled. Run: python scripts/dsa_bank/build.py"
    )
    return

    all_problems: list[dict] = []
    all_problems.extend(gen_array_problems())
    all_problems.extend(gen_parametric_family())

    written = 0
    for p in all_problems:
        if dump(p, force=args.force):
            written += 1

    existing = len(list(OUT.glob("*.json")))
    print(f"Wrote {written} new problems. Total JSON problems now: {existing}")


if __name__ == "__main__":
    main()
