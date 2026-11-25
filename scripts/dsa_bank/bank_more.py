"""Additional distinct classics to clear the 250-problem bar."""

from __future__ import annotations

from collections import Counter, defaultdict, deque

from lib import cases, define


@define(
    slug="fibonacci-number",
    title="Fibonacci Number",
    difficulty="easy",
    topics=["dynamic-programming", "math"],
    statement="Return F(n) where F(0) = 0, F(1) = 1, and F(n) = F(n - 1) + F(n - 2).",
    constraints=["0 <= n <= 30"],
    signature="def fib(n: int) -> int:",
    function_name="fib",
    hints=[
        "The naive recursion recomputes the same F(k) exponentially often.",
        "Bottom-up iteration keeps only the previous two values.",
        "Matrix exponentiation or the closed form are the advanced follow-ups. Iteration is the expected answer.",
    ],
    approaches=[
        ("Recursion", "O(phi^n)", "O(n)", "The call tree."),
        ("Iteration", "O(n)", "O(1)", "Two rolling variables."),
    ],
    editorial=(
        "Initialize a = 0 and b = 1. Repeat n times, replacing the pair with (b, a + b). "
        "After n steps a holds F(n). The loop body is the recurrence with the call stack erased."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _oracle_fib(n: int) -> int:
    if n < 2:
        return n
    x = y = 1
    for _ in range(2, n):
        x, y = y, x + y
    return y if n else 0


cases(
    "fibonacci-number",
    _oracle_fib,
    [
        ("two", {"n": 2}, True, "F(2) = 1."),
        ("four", {"n": 4}, True, "F(4) = 3."),
        ("zero", {"n": 0}, False, None),
        ("one", {"n": 1}, False, None),
        ("ten", {"n": 10}, False, None),
    ],
)


@define(
    slug="min-falling-path-sum",
    title="Minimum Falling Path Sum",
    difficulty="medium",
    topics=["dynamic-programming", "matrix"],
    statement="A falling path starts at any cell in the first row and chooses the cell directly below or diagonally below. Return the minimum sum of any falling path.",
    constraints=["1 <= n <= 100", "-100 <= matrix[i][j] <= 100"],
    signature="from typing import List\n\ndef min_falling_path_sum(matrix: List[List[int]]) -> int:",
    function_name="min_falling_path_sum",
    hints=[
        "The best path ending at (r, c) comes from (r - 1, c - 1), (r - 1, c), or (r - 1, c + 1).",
        "Add matrix[r][c] to the minimum of those in-bounds predecessors.",
        "The answer is the minimum of the last row.",
    ],
    approaches=[
        ("Recursion from the top", "exponential", "O(n)", "Three choices per row."),
        ("In-place row DP", "O(n^2)", "O(1) extra", "Overwrite the matrix downward."),
    ],
    editorial=(
        "Process rows from top to bottom. Each cell becomes its own value plus the best legal parent. "
        "Edge columns have only two parents. "
        "Because each row depends only on the previous row, the original cells can be updated in a copy of the previous row to avoid using already-updated neighbors."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)
    prev = matrix[0][:]
    for r in range(1, n):
        cur = []
        for c in range(n):
            best = prev[c]
            if c:
                best = min(best, prev[c - 1])
            if c + 1 < n:
                best = min(best, prev[c + 1])
            cur.append(matrix[r][c] + best)
        prev = cur
    return min(prev)


def _oracle_min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)

    def best(r: int, c: int) -> int:
        if r == n:
            return 0
        if not 0 <= c < n:
            return 10**9
        return matrix[r][c] + min(best(r + 1, c - 1), best(r + 1, c), best(r + 1, c + 1))

    return min(best(0, c) for c in range(n))


cases(
    "min-falling-path-sum",
    _oracle_min_falling_path_sum,
    [
        ("classic", {"matrix": [[2, 1, 3], [6, 5, 4], [7, 8, 9]]}, True, "The path 1, 4, 7? 1 then 5 or 4. Minimum is 13."),
        ("one", {"matrix": [[-5]]}, True, "The only cell."),
        ("row", {"matrix": [[1, 2, 3]]}, False, None),
        ("neg", {"matrix": [[-1, 2], [3, -4]]}, False, None),
        ("flat", {"matrix": [[1, 1], [1, 1]]}, False, None),
    ],
)


@define(
    slug="paint-house",
    title="Paint House",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="`costs[i]` is the cost of painting house i red, blue, or green, in that order. Adjacent houses cannot share a color. Return the minimum cost to paint every house.",
    constraints=["1 <= houses <= 100", "1 <= costs[i][j] <= 20"],
    signature="from typing import List\n\ndef min_cost_paint(costs: List[List[int]]) -> int:",
    function_name="min_cost_paint",
    hints=[
        "The state is the house and the color you just used.",
        "Painting house i color c costs costs[i][c] plus the cheaper of the other two colors on house i - 1.",
        "Three rolling values are enough.",
    ],
    approaches=[
        ("Recursion", "O(2^n)", "O(n)", "Two legal colors after the first."),
        ("DP over three colors", "O(n)", "O(1)", "A constant number of colors."),
    ],
    editorial=(
        "Keep the minimum cost of reaching the current house in each color. "
        "The next red cost is the red paint plus the min of the previous blue and green. "
        "The answer is the min of the three totals after the last house."
    ),
    companies=["Amazon", "Google", "LinkedIn", "Microsoft"],
)
def min_cost_paint(costs: list[list[int]]) -> int:
    a, b, c = costs[0]
    for red, blue, green in costs[1:]:
        a, b, c = red + min(b, c), blue + min(a, c), green + min(a, b)
    return min(a, b, c)


def _oracle_min_cost_paint(costs: list[list[int]]) -> int:
    def best(i: int, prev: int) -> int:
        if i == len(costs):
            return 0
        return min(costs[i][color] + best(i + 1, color) for color in range(3) if color != prev)

    return best(0, -1)


cases(
    "paint-house",
    _oracle_min_cost_paint,
    [
        ("classic", {"costs": [[17, 2, 17], [16, 16, 5], [14, 3, 19]]}, True, "Paint blue, green, blue for 10."),
        ("one", {"costs": [[7, 6, 2]]}, True, "The cheapest single color."),
        ("two", {"costs": [[1, 10, 10], [10, 1, 10]]}, False, None),
        ("same", {"costs": [[5, 5, 5], [5, 5, 5]]}, False, None),
        ("three", {"costs": [[1, 2, 3], [1, 2, 3], [3, 2, 1]]}, False, None),
    ],
)


@define(
    slug="paint-fence",
    title="Paint Fence",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Paint `n` fence posts with `k` colors so that at most two adjacent posts share a color. Return the number of ways.",
    constraints=["1 <= n <= 50", "1 <= k <= 10^5", "The answer fits in a 32-bit signed integer for these tests"],
    signature="def num_ways_fence(n: int, k: int) -> int:",
    function_name="num_ways_fence",
    hints=[
        "A post can match the previous one, or differ from it.",
        "same(i) = diff(i - 1), because only one post may match in a row beyond the pair... actually same means this post matches the previous, so the previous pair must have differed.",
        "diff(i) = (k - 1) * (same(i - 1) + diff(i - 1)). Total(i) = same + diff.",
    ],
    approaches=[
        ("Recursion on the last run", "O(n)", "O(n)", "Two states."),
        ("Rolling states", "O(n)", "O(1)", "same and diff."),
    ],
    editorial=(
        "Let same be the ways where the last two posts match, and diff the ways where they differ. "
        "For one post, there are k ways, all 'different' from a fictional previous post, and same is 0. "
        "Then same becomes the old diff, and diff becomes (k - 1) times the old total. The answer after n posts is same + diff."
    ),
    companies=["Google", "Amazon", "Adobe", "Microsoft"],
)
def num_ways_fence(n: int, k: int) -> int:
    if n == 1:
        return k
    same, diff = 0, k
    for _ in range(1, n):
        same, diff = diff, (k - 1) * (same + diff)
    return same + diff


def _oracle_num_ways_fence(n: int, k: int) -> int:
    def ways(i: int, prev: int, run: int) -> int:
        if i == n:
            return 1
        total = 0
        for color in range(k):
            if color == prev:
                if run < 2:
                    total += ways(i + 1, color, run + 1)
            else:
                total += ways(i + 1, color, 1)
        return total

    return ways(0, -1, 0)


cases(
    "paint-fence",
    _oracle_num_ways_fence,
    [
        ("classic", {"n": 3, "k": 2}, True, "Six ways."),
        ("one", {"n": 1, "k": 1}, True, "One post, one color."),
        ("two", {"n": 2, "k": 1}, False, None),
        ("seven", {"n": 7, "k": 2}, False, None),
        ("posts", {"n": 2, "k": 4}, False, None),
    ],
)


@define(
    slug="summary-ranges",
    title="Summary Ranges",
    difficulty="easy",
    topics=["arrays", "intervals"],
    statement="`nums` is a sorted list of unique integers. Return the smallest sorted list of ranges that cover it. A range of one number is 'x'. A longer range is 'start->end'.",
    constraints=["0 <= nums.length <= 20", "-2^31 <= nums[i] <= 2^31 - 1", "All values are unique and sorted"],
    signature="from typing import List\n\ndef summary_ranges(nums: List[int]) -> List[str]:",
    function_name="summary_ranges",
    hints=[
        "A new range starts when the current number is not one more than the previous number.",
        "Track the start of the current run and the previous value.",
        "Flush the run at every gap and once more after the loop.",
    ],
    approaches=[
        ("Linear scan", "O(n)", "O(1) extra", "One pass plus the output."),
        ("Groupby on differences", "O(n)", "O(n)", "The same idea with consecutive differences."),
    ],
    editorial=(
        "Walk the sorted values. While each value is exactly one larger than the previous, extend the run. "
        "Otherwise emit the finished run and start a new one. "
        "A run of length one is emitted as a single number."
    ),
    companies=["Amazon", "Google", "Adobe", "Bloomberg"],
)
def summary_ranges(nums: list[int]) -> list[str]:
    if not nums:
        return []
    out: list[str] = []
    start = prev = nums[0]
    for value in nums[1:]:
        if value == prev + 1:
            prev = value
        else:
            out.append(str(start) if start == prev else f"{start}->{prev}")
            start = prev = value
    out.append(str(start) if start == prev else f"{start}->{prev}")
    return out


def _oracle_summary_ranges(nums: list[int]) -> list[str]:
    ranges = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        ranges.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
        i = j + 1
    return ranges


cases(
    "summary-ranges",
    _oracle_summary_ranges,
    [
        ("classic", {"nums": [0, 1, 2, 4, 5, 7]}, True, "0->2, 4->5, and 7."),
        ("singles", {"nums": [0, 2, 3, 4, 6, 8, 9]}, True, "Mixed ranges."),
        ("empty", {"nums": []}, False, None),
        ("one", {"nums": [5]}, False, None),
        ("neg", {"nums": [-3, -2, -1, 1]}, False, None),
    ],
)


@define(
    slug="next-permutation",
    title="Next Permutation",
    difficulty="medium",
    topics=["arrays", "two-pointers"],
    statement="Rearrange `nums` into the next lexicographically greater permutation. If none exists, rearrange it into the lowest order. Return the new order. Do it in place in the algorithm, even though the function returns the list.",
    constraints=["1 <= nums.length <= 100", "0 <= nums[i] <= 100"],
    signature="from typing import List\n\ndef next_permutation(nums: List[int]) -> List[int]:",
    function_name="next_permutation",
    hints=[
        "Find the rightmost index i where nums[i] < nums[i + 1]. That is the pivot that can still grow.",
        "Swap it with the smallest value to its right that is still larger than it. That value is the rightmost successor.",
        "Reverse the suffix after i so it becomes the smallest possible tail. If no pivot exists, reverse the whole array.",
    ],
    approaches=[
        ("Generate all permutations", "O(n!)", "O(n)", "Only for tiny n."),
        ("Pivot and reverse", "O(n)", "O(1)", "One scan back, one scan for the successor, one reverse."),
    ],
    editorial=(
        "The suffix after the pivot is non-increasing, so it is the largest tail. "
        "The successor swap raises the pivot by the smallest possible amount, and reversing the suffix makes that tail the smallest possible. "
        "Together those steps produce the next permutation, and a fully non-increasing array wraps to the sorted order."
    ),
    companies=["Amazon", "Google", "Facebook", "Adobe"],
)
def next_permutation(nums: list[int]) -> list[int]:
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    left, right = i + 1, len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    return nums


def _oracle_next_permutation(nums: list[int]) -> list[int]:
    from itertools import permutations

    ordered = sorted(set(permutations(nums)))
    nxt = ordered[(ordered.index(tuple(nums)) + 1) % len(ordered)]
    return list(nxt)


cases(
    "next-permutation",
    _oracle_next_permutation,
    [
        ("classic", {"nums": [1, 2, 3]}, True, "The next permutation is 1, 3, 2."),
        ("wrap", {"nums": [3, 2, 1]}, True, "The lowest order is 1, 2, 3."),
        ("dups", {"nums": [1, 1, 5]}, False, None),
        ("single", {"nums": [1]}, False, None),
        ("mid", {"nums": [1, 3, 2]}, False, None),
    ],
)


@define(
    slug="can-place-flowers",
    title="Can Place Flowers",
    difficulty="easy",
    topics=["arrays", "greedy"],
    statement="`flowerbed[i]` is 1 if planted and 0 if empty. Flowers cannot be adjacent. Return true when `n` new flowers can be planted without violating that rule.",
    constraints=["1 <= flowerbed.length <= 2 * 10^4", "flowerbed[i] is 0 or 1", "0 <= n <= flowerbed.length"],
    signature="from typing import List\n\ndef can_place_flowers(flowerbed: List[int], n: int) -> bool:",
    function_name="can_place_flowers",
    hints=[
        "A plot is plantable when it and its existing neighbors are empty.",
        "Greedily plant whenever you can. Planting earlier cannot block a later legal plot in a way that reduces the total.",
        "Treat missing neighbors as empty so the ends are easy.",
    ],
    approaches=[
        ("Try every subset", "exponential", "O(n)", "Not needed."),
        ("Greedy scan", "O(n)", "O(1)", "Plant and skip the next plot."),
    ],
    editorial=(
        "Scan the bed. If the current plot and both neighbors are empty, plant and decrement n. "
        "You can return early when n hits zero. "
        "At the end, n must be zero or negative."
    ),
    companies=["Amazon", "Google", "LinkedIn", "Adobe"],
)
def can_place_flowers(flowerbed: list[int], n: int) -> bool:
    bed = flowerbed[:]
    for i in range(len(bed)):
        left = bed[i - 1] if i else 0
        right = bed[i + 1] if i + 1 < len(bed) else 0
        if bed[i] == left == right == 0:
            bed[i] = 1
            n -= 1
    return n <= 0


def _oracle_can_place_flowers(flowerbed: list[int], n: int) -> bool:
    bed = [0] + flowerbed[:] + [0]
    count = 0
    i = 1
    while i < len(bed) - 1:
        if bed[i - 1] == bed[i] == bed[i + 1] == 0:
            bed[i] = 1
            count += 1
            i += 2
        else:
            i += 1
    return count >= n


cases(
    "can-place-flowers",
    _oracle_can_place_flowers,
    [
        ("yes", {"flowerbed": [1, 0, 0, 0, 1], "n": 1}, True, "The middle plot works."),
        ("no", {"flowerbed": [1, 0, 0, 0, 1], "n": 2}, True, "Only one plot is legal."),
        ("empty", {"flowerbed": [0, 0, 0], "n": 2}, False, None),
        ("zero", {"flowerbed": [1, 0, 1], "n": 0}, False, None),
        ("full", {"flowerbed": [0], "n": 1}, False, None),
    ],
)


@define(
    slug="find-first-and-last-position",
    title="Find First and Last Position of Element in Sorted Array",
    difficulty="medium",
    topics=["binary-search"],
    statement="`nums` is sorted non-decreasing. Return the start and end index of `target`. If it is absent, return [-1, -1].",
    constraints=["0 <= nums.length <= 10^5", "-10^9 <= nums[i], target <= 10^9"],
    signature="from typing import List\n\ndef search_range(nums: List[int], target: int) -> List[int]:",
    function_name="search_range",
    hints=[
        "Two binary searches: one for the lower bound and one for the upper bound.",
        "Lower bound is the first index with nums[i] >= target. It is a hit only if the value equals target.",
        "Upper bound is the first index with nums[i] > target. The last occurrence is that index minus one.",
    ],
    approaches=[
        ("Linear scan", "O(n)", "O(1)", "Find the first and keep the last."),
        ("Two lower bounds", "O(log n)", "O(1)", "The standard sorted-range query."),
    ],
    editorial=(
        "Implement lower_bound(x) as the first index whose value is at least x, using a half-open interval. "
        "The start is lower_bound(target) if it lands on target. The end is lower_bound(target + 1) - 1. "
        "If the start is out of range or the value differs, return [-1, -1]."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def search_range(nums: list[int], target: int) -> list[int]:
    def lower(goal: int) -> int:
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < goal:
                lo = mid + 1
            else:
                hi = mid
        return lo

    start = lower(target)
    if start == len(nums) or nums[start] != target:
        return [-1, -1]
    return [start, lower(target + 1) - 1]


def _oracle_search_range(nums: list[int], target: int) -> list[int]:
    indexes = [i for i, value in enumerate(nums) if value == target]
    return [indexes[0], indexes[-1]] if indexes else [-1, -1]


cases(
    "find-first-and-last-position",
    _oracle_search_range,
    [
        ("classic", {"nums": [5, 7, 7, 8, 8, 10], "target": 8}, True, "8 occupies indexes 3 and 4."),
        ("miss", {"nums": [5, 7, 7, 8, 8, 10], "target": 6}, True, "6 is absent."),
        ("empty", {"nums": [], "target": 0}, False, None),
        ("single", {"nums": [1], "target": 1}, False, None),
        ("all", {"nums": [2, 2, 2], "target": 2}, False, None),
    ],
)


@define(
    slug="split-array-largest-sum",
    title="Split Array Largest Sum",
    difficulty="hard",
    topics=["binary-search", "dynamic-programming"],
    statement=(
        "Split `nums` into `k` non-empty contiguous parts. "
        "Return the minimum possible largest sum among the parts."
    ),
    constraints=["1 <= nums.length <= 1000", "1 <= k <= min(50, nums.length)", "0 <= nums[i] <= 10^6"],
    signature="from typing import List\n\ndef split_array(nums: List[int], k: int) -> int:",
    function_name="split_array",
    hints=[
        "The answer lies between the largest element and the total sum.",
        "A candidate maximum sum is feasible when a greedy scan can cover the array in at most k parts without exceeding it.",
        "Binary search the candidate. Feasibility is monotone.",
    ],
    approaches=[
        ("DP", "O(n^2 * k)", "O(n * k)", "dp[parts][index] is the best largest sum."),
        ("Binary search on the sum", "O(n log sum)", "O(1)", "The same pattern as shipping packages."),
    ],
    editorial=(
        "If a maximum part sum M is feasible, every larger M is feasible. "
        "Greedily fill a part until the next element would exceed M, then start a new part. "
        "If the number of parts is at most k, search lower. The lowest feasible M is the answer, and it is at least the heaviest element."
    ),
    companies=["Google", "Amazon", "Facebook", "Microsoft"],
)
def split_array(nums: list[int], k: int) -> int:
    def feasible(limit: int) -> bool:
        parts = 1
        total = 0
        for value in nums:
            if total + value > limit:
                parts += 1
                total = 0
            total += value
        return parts <= k

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def _oracle_split_array(nums: list[int], k: int) -> int:
    def feasible(limit: int) -> bool:
        parts = 1
        total = 0
        for value in nums:
            if value > limit:
                return False
            if total + value > limit:
                parts += 1
                total = 0
            total += value
        return parts <= k

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


cases(
    "split-array-largest-sum",
    _oracle_split_array,
    [
        ("classic", {"nums": [7, 2, 5, 10, 8], "k": 2}, True, "The best largest sum is 18."),
        ("three", {"nums": [1, 2, 3, 4, 5], "k": 2}, True, "The split 1+2+3 and 4+5 has largest sum 9."),
        ("one-part", {"nums": [1, 4, 4], "k": 1}, False, None),
        ("each", {"nums": [1, 4, 4], "k": 3}, False, None),
        ("equal", {"nums": [2, 2, 2, 2], "k": 2}, False, None),
    ],
)


@define(
    slug="set-matrix-zeroes",
    title="Set Matrix Zeroes",
    difficulty="medium",
    topics=["arrays", "matrix"],
    statement="If an element is 0, set its entire row and column to 0. Do it in place in the algorithm and return the matrix. Use constant extra memory besides the matrix.",
    constraints=["1 <= m, n <= 200", "-2^31 <= matrix[i][j] <= 2^31 - 1"],
    signature="from typing import List\n\ndef set_zeroes(matrix: List[List[int]]) -> List[List[int]]:",
    function_name="set_zeroes",
    hints=[
        "A copy of the zero positions is the easy solution and uses extra memory.",
        "Use the first row and first column as markers. Remember separately whether those two lines themselves must be zeroed.",
        "Write markers first, then zero the inner cells, then zero the first row and column if their flags say so.",
    ],
    approaches=[
        ("Store zero coordinates", "O(mn)", "O(m + n)", "Two boolean arrays."),
        ("First row and column as markers", "O(mn)", "O(1)", "The constant-space version."),
    ],
    editorial=(
        "Scan the matrix. If matrix[r][c] is 0, set matrix[r][0] and matrix[0][c] to 0. "
        "Also record whether row 0 or column 0 originally contained a zero, because those cells are now doing double duty. "
        "A second scan, from the bottom-right of the inner matrix, zeroes a cell when its marker row or marker column is zero. Apply the two flags last."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Facebook"],
)
def set_zeroes(matrix: list[list[int]]) -> list[list[int]]:
    rows, cols = len(matrix), len(matrix[0])
    zero_row = any(matrix[0][c] == 0 for c in range(cols))
    zero_col = any(matrix[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if zero_row:
        for c in range(cols):
            matrix[0][c] = 0
    if zero_col:
        for r in range(rows):
            matrix[r][0] = 0
    return matrix


def _oracle_set_zeroes(matrix: list[list[int]]) -> list[list[int]]:
    rows, cols = len(matrix), len(matrix[0])
    zero_rows = {r for r in range(rows) for c in range(cols) if matrix[r][c] == 0}
    zero_cols = {c for r in range(rows) for c in range(cols) if matrix[r][c] == 0}
    out = [row[:] for row in matrix]
    for r in range(rows):
        for c in range(cols):
            if r in zero_rows or c in zero_cols:
                out[r][c] = 0
    return out


cases(
    "set-matrix-zeroes",
    _oracle_set_zeroes,
    [
        ("classic", {"matrix": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]}, True, "The middle row and column become zero."),
        ("corner", {"matrix": [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]}, True, "Both marked rows and columns are cleared."),
        ("none", {"matrix": [[1, 2], [3, 4]]}, False, None),
        ("one", {"matrix": [[0]]}, False, None),
        ("row", {"matrix": [[1, 0]]}, False, None),
    ],
)


@define(
    slug="game-of-life",
    title="Game of Life",
    difficulty="medium",
    topics=["arrays", "matrix", "simulation"],
    statement=(
        "Apply one step of Conway's Game of Life and return the board. "
        "1 is live and 0 is dead. A live cell with two or three live neighbors stays live. A dead cell with exactly three live neighbors becomes live. Every other cell dies or stays dead. Neighbors are the eight surrounding cells."
    ),
    constraints=["1 <= m, n <= 25", "board[i][j] is 0 or 1"],
    signature="from typing import List\n\ndef game_of_life(board: List[List[int]]) -> List[List[int]]:",
    function_name="game_of_life",
    hints=[
        "If you write the next state immediately, later neighbor counts are wrong.",
        "Encode the next state in a second bit. The current state stays in the low bit.",
        "After every cell is encoded, shift each value right by one to drop the old state.",
    ],
    approaches=[
        ("Copy the board", "O(mn)", "O(mn)", "Count neighbors on the copy."),
        ("In-place bit encoding", "O(mn)", "O(1)", "The second bit holds the next state."),
    ],
    editorial=(
        "Count live neighbors using the low bit only. "
        "If the cell should be live next, set the second bit with OR 2. "
        "A final pass replaces every cell with its second bit. The original board is not required after the step, and the encoding never needs a second matrix."
    ),
    companies=["Amazon", "Google", "Dropbox", "Microsoft"],
)
def game_of_life(board: list[list[int]]) -> list[list[int]]:
    rows, cols = len(board), len(board[0])

    def live(r: int, c: int) -> int:
        if 0 <= r < rows and 0 <= c < cols:
            return board[r][c] & 1
        return 0

    for r in range(rows):
        for c in range(cols):
            neighbors = sum(live(r + dr, c + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0))
            if board[r][c] == 1 and neighbors in (2, 3):
                board[r][c] = 3
            if board[r][c] == 0 and neighbors == 3:
                board[r][c] = 2
    for r in range(rows):
        for c in range(cols):
            board[r][c] >>= 1
    return board


def _oracle_game_of_life(board: list[list[int]]) -> list[list[int]]:
    rows, cols = len(board), len(board[0])
    out = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbors += board[nr][nc]
            if board[r][c] == 1 and neighbors in (2, 3):
                out[r][c] = 1
            if board[r][c] == 0 and neighbors == 3:
                out[r][c] = 1
    return out


cases(
    "game-of-life",
    _oracle_game_of_life,
    [
        ("classic", {"board": [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]}, True, "One generation of the classic board."),
        ("dead", {"board": [[0, 0], [0, 0]]}, True, "Stays dead."),
        ("block", {"board": [[1, 1], [1, 1]]}, False, None),
        ("single", {"board": [[1]]}, False, None),
        ("blinker", {"board": [[0, 1, 0], [0, 1, 0], [0, 1, 0]]}, False, None),
    ],
)


@define(
    slug="compare-version-numbers",
    title="Compare Version Numbers",
    difficulty="medium",
    topics=["strings"],
    statement="Compare two version strings of dot-separated revisions. Missing revisions compare as 0. Leading zeros do not change the integer value. Return -1, 0, or 1 when version1 is less than, equal to, or greater than version2.",
    constraints=["1 <= length <= 500", "Revisions fit in a 32-bit integer"],
    signature="def compare_version(version1: str, version2: str) -> int:",
    function_name="compare_version",
    hints=[
        "Split on dots and parse each piece as an integer.",
        "Walk the longer list. A missing piece is 0.",
        "Return as soon as two revisions differ.",
    ],
    approaches=[
        ("Pad and compare", "O(n)", "O(n)", "Zip the integer lists with zeros."),
        ("Two pointers", "O(n)", "O(1)", "Parse the next integer without storing every revision."),
    ],
    editorial=(
        "Split both strings and convert revisions with int, which drops leading zeros. "
        "Compare index by index up to the longer length, using 0 when a version has ended. "
        "The first unequal pair decides the sign. If every pair matches, the versions are equal."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Adobe"],
)
def compare_version(version1: str, version2: str) -> int:
    a = [int(part) for part in version1.split(".")]
    b = [int(part) for part in version2.split(".")]
    for i in range(max(len(a), len(b))):
        left = a[i] if i < len(a) else 0
        right = b[i] if i < len(b) else 0
        if left < right:
            return -1
        if left > right:
            return 1
    return 0


def _oracle_compare_version(version1: str, version2: str) -> int:
    def parts(text: str) -> list[int]:
        return [int(piece) for piece in text.split(".")]

    a, b = parts(version1), parts(version2)
    size = max(len(a), len(b))
    a += [0] * (size - len(a))
    b += [0] * (size - len(b))
    return (a > b) - (a < b)


cases(
    "compare-version-numbers",
    _oracle_compare_version,
    [
        ("greater", {"version1": "1.2", "version2": "1.10"}, True, "2 is less than 10, so version1 is smaller. Wait: 1.2 < 1.10, so -1."),
        ("equal", {"version1": "1.01", "version2": "1.001"}, True, "Leading zeros do not count. They are equal."),
        ("zero-tail", {"version1": "1.0", "version2": "1.0.0"}, False, None),
        ("less", {"version1": "0.1", "version2": "1.1"}, False, None),
        ("same", {"version1": "1", "version2": "1"}, False, None),
    ],
)


@define(
    slug="multiply-strings",
    title="Multiply Strings",
    difficulty="medium",
    topics=["math", "strings"],
    statement="Multiply two non-negative integers given as strings. Return the product as a string. Do not convert the whole inputs with a built-in big-integer parser.",
    constraints=["1 <= num1.length, num2.length <= 200", "No leading zeros except the number 0"],
    signature="def multiply(num1: str, num2: str) -> str:",
    function_name="multiply",
    hints=[
        "The product of an i-digit and a j-digit number has at most i + j digits.",
        "nums1[i] * nums2[j] contributes to positions i + j and i + j + 1, counting from the left, or from the right if you reverse the index.",
        "Accumulate into an integer array, carry once at the end, and strip leading zeros.",
    ],
    approaches=[
        ("Grade-school multiplication", "O(n * m)", "O(n + m)", "The digit array."),
        ("Built-in big integers", "O(n * m)", "O(n + m)", "Correct in Python and not the point of the problem."),
    ],
    editorial=(
        "Allocate n + m zeros. For each pair of digits, add the product into index i + j + 1 and carry the tens into i + j. "
        "A final carry sweep is unnecessary if you carry immediately. "
        "Join the digits and strip leading zeros, leaving a single zero when the product is zero."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Adobe"],
)
def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"
    n, m = len(num1), len(num2)
    pos = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            total = (ord(num1[i]) - 48) * (ord(num2[j]) - 48) + pos[i + j + 1]
            pos[i + j + 1] = total % 10
            pos[i + j] += total // 10
    digits = "".join(str(d) for d in pos).lstrip("0")
    return digits or "0"


def _oracle_multiply(num1: str, num2: str) -> str:
    return str(int(num1) * int(num2))


cases(
    "multiply-strings",
    _oracle_multiply,
    [
        ("classic", {"num1": "2", "num2": "3"}, True, "6."),
        ("bigger", {"num1": "123", "num2": "456"}, True, "56088."),
        ("zero", {"num1": "0", "num2": "52"}, False, None),
        ("ten", {"num1": "10", "num2": "10"}, False, None),
        ("nines", {"num1": "99", "num2": "99"}, False, None),
    ],
)


@define(
    slug="longest-happy-prefix",
    title="Longest Happy Prefix",
    difficulty="hard",
    topics=["strings", "kmp"],
    statement="A happy prefix is a proper prefix that is also a suffix. Return the longest happy prefix of `s`, or an empty string if none exists.",
    constraints=["1 <= s.length <= 10^5"],
    signature="def longest_prefix(s: str) -> str:",
    function_name="longest_prefix",
    hints=[
        "This is the last entry of the KMP longest-prefix-suffix table.",
        "lps[i] is the longest proper prefix of s[:i+1] that is also a suffix.",
        "The answer is s[:lps[-1]]. If that length is 0, return an empty string.",
    ],
    approaches=[
        ("Check every border", "O(n^2)", "O(n)", "Test prefixes from long to short."),
        ("KMP prefix table", "O(n)", "O(n)", "One linear construction."),
    ],
    editorial=(
        "Build the LPS array exactly as in string search. "
        "The value at the last index is the longest border of the whole string. "
        "Slice that many characters from the front. The border is proper because the LPS construction never lets a border equal the whole string."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def longest_prefix(s: str) -> str:
    lps = [0] * len(s)
    length = 0
    i = 1
    while i < len(s):
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1
    return s[: lps[-1]]


def _oracle_longest_prefix(s: str) -> str:
    best = ""
    for size in range(1, len(s)):
        if s[:size] == s[-size:]:
            best = s[:size]
    return best


cases(
    "longest-happy-prefix",
    _oracle_longest_prefix,
    [
        ("level", {"s": "level"}, True, "l is the longest happy prefix."),
        ("ababab", {"s": "ababab"}, True, "abab is both a prefix and a suffix."),
        ("single", {"s": "a"}, False, None),
        ("none", {"s": "abc"}, False, None),
        ("aaaa", {"s": "aaaa"}, False, None),
    ],
)


@define(
    slug="hand-of-straights",
    title="Hand of Straights",
    difficulty="medium",
    topics=["greedy", "hashing"],
    statement="Return true when you can rearrange `hand` into groups of `group_size` consecutive values. Each card is used once.",
    constraints=["1 <= hand.length <= 10^4", "0 <= hand[i] <= 10^9", "1 <= groupSize <= hand.length"],
    signature="from typing import List\n\ndef is_n_straight_hand(hand: List[int], group_size: int) -> bool:",
    function_name="is_n_straight_hand",
    hints=[
        "If the length is not divisible by the group size, return false.",
        "Count the cards. Always start a group at the smallest remaining value.",
        "A group starting at x consumes one of x, x+1, ..., x+group_size-1. If any is missing, return false.",
    ],
    approaches=[
        ("Sort and scan", "O(n log n)", "O(n)", "A counter plus a sorted unique list."),
        ("Ordered map", "O(n log n)", "O(n)", "The same greedy start."),
    ],
    editorial=(
        "The smallest remaining card has nowhere to sit except as the start of a group. "
        "That greedy choice is forced. Consume the next group_size - 1 consecutive values. "
        "Repeat until the counter is empty or a hole appears."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def is_n_straight_hand(hand: list[int], group_size: int) -> bool:
    if len(hand) % group_size:
        return False
    counts = Counter(hand)
    for start in sorted(counts):
        need = counts[start]
        if need == 0:
            continue
        for offset in range(group_size):
            counts[start + offset] -= need
            if counts[start + offset] < 0:
                return False
    return True


def _oracle_is_n_straight_hand(hand: list[int], group_size: int) -> bool:
    if len(hand) % group_size:
        return False
    cards = sorted(hand)
    while cards:
        start = cards[0]
        for offset in range(group_size):
            try:
                cards.remove(start + offset)
            except ValueError:
                return False
    return True


cases(
    "hand-of-straights",
    _oracle_is_n_straight_hand,
    [
        ("yes", {"hand": [1, 2, 3, 6, 2, 3, 4, 7, 8], "group_size": 3}, True, "Three straights."),
        ("no", {"hand": [1, 2, 3, 4, 5], "group_size": 4}, True, "The length is not divisible by 4."),
        ("one", {"hand": [1], "group_size": 1}, False, None),
        ("dups", {"hand": [1, 1, 2, 2, 3, 3], "group_size": 3}, False, None),
        ("gap", {"hand": [1, 2, 4], "group_size": 3}, False, None),
    ],
)


@define(
    slug="reorganize-string",
    title="Reorganize String",
    difficulty="medium",
    topics=["greedy", "heaps", "strings"],
    statement="Rearrange `s` so no two adjacent characters are equal. Return an empty string when it is impossible. When it is possible, return the string formed by sorting characters by descending frequency and then by character, and writing them into even indexes first and odd indexes afterward.",
    constraints=["1 <= s.length <= 500", "s consists of lowercase English letters"],
    signature="def reorganize_string(s: str) -> str:",
    function_name="reorganize_string",
    hints=[
        "If one character appears more than (n + 1) / 2 times, no arrangement exists.",
        "A max-heap of frequencies always places the currently most frequent remaining character, unless it equals the previous character.",
        "To make the result unique, break frequency ties by the character itself.",
    ],
    approaches=[
        ("Fill even indexes then odd indexes", "O(n)", "O(1)", "Sort by frequency and write into even slots first."),
        ("Heap", "O(n log alphabet)", "O(alphabet)", "Greedy most-frequent placement."),
    ],
    editorial=(
        "Sort characters by descending frequency, then by character. "
        "If the top frequency exceeds (n + 1) // 2, return an empty string. "
        "Write the sorted characters into even indexes first and then odd indexes. The most frequent character lands on evens and cannot touch itself when the frequency bound holds. Sorting the characters inside a frequency makes the string deterministic."
    ),
    companies=["Amazon", "Google", "Facebook", "Uber"],
)
def reorganize_string(s: str) -> str:
    counts = Counter(s)
    if max(counts.values()) > (len(s) + 1) // 2:
        return ""
    ordered = sorted(s, key=lambda ch: (-counts[ch], ch))
    result = [""] * len(s)
    index = 0
    for ch in ordered:
        result[index] = ch
        index += 2
        if index >= len(s):
            index = 1
    return "".join(result)


def _oracle_reorganize_string(s: str) -> str:
    counts = Counter(s)
    if not counts or max(counts.values()) > (len(s) + 1) // 2:
        return ""
    slots = [""] * len(s)
    cursor = 0
    for ch, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        for _ in range(count):
            slots[cursor] = ch
            cursor += 2
            if cursor >= len(s):
                cursor = 1
    return "".join(slots)


cases(
    "reorganize-string",
    _oracle_reorganize_string,
    [
        ("aab", {"s": "aab"}, True, "aba is the only shape."),
        ("aaab", {"s": "aaab"}, True, "Impossible."),
        ("vvvlo", {"s": "vvvlo"}, False, None),
        ("a", {"s": "a"}, False, None),
        ("abcd", {"s": "abcd"}, False, None),
    ],
)


@define(
    slug="top-k-frequent-words",
    title="Top K Frequent Words",
    difficulty="medium",
    topics=["heaps", "hashing", "strings"],
    statement="Return the `k` most frequent words. Sort by frequency descending, and break ties by lexicographical order.",
    constraints=["1 <= words.length <= 500", "1 <= k <= number of unique words"],
    signature="from typing import List\n\ndef top_k_frequent_words(words: List[str], k: int) -> List[str]:",
    function_name="top_k_frequent_words",
    hints=[
        "Count the words.",
        "Sort unique words by (-count, word).",
        "A heap of size k with the opposite order also works and is the follow-up for a stream.",
    ],
    approaches=[
        ("Sort", "O(n log n)", "O(n)", "The straightforward ranking."),
        ("Heap of size k", "O(n log k)", "O(n)", "Push unique words with a key that pops the worst candidate."),
    ],
    editorial=(
        "Frequency is the primary key and the word is the secondary key, reversed so that a smaller word wins a tie. "
        "Sort once and slice the first k. "
        "The heap version stores the worst of the current top k at the root, using a key of (count, inverted word) or a custom comparison."
    ),
    companies=["Amazon", "Uber", "Google", "Microsoft"],
)
def top_k_frequent_words(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    ranked = sorted(counts, key=lambda word: (-counts[word], word))
    return ranked[:k]


def _oracle_top_k_frequent_words(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]]


cases(
    "top-k-frequent-words",
    _oracle_top_k_frequent_words,
    [
        ("classic", {"words": ["i", "love", "leetcode", "i", "love", "coding"], "k": 2}, True, "i and love, with i first by alphabet."),
        ("tie", {"words": ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], "k": 4}, True, "Frequency then alphabet."),
        ("one", {"words": ["a"], "k": 1}, False, None),
        ("all", {"words": ["b", "a"], "k": 2}, False, None),
        ("same", {"words": ["a", "a", "b"], "k": 1}, False, None),
    ],
)


@define(
    slug="car-fleet",
    title="Car Fleet",
    difficulty="medium",
    topics=["stacks", "sorting"],
    statement=(
        "Cars start at distinct positions on a one-lane road toward a target. "
        "A car cannot pass the car in front, so it adopts that car's speed and they become a fleet. "
        "Return the number of fleets that arrive at the target. position[i] and speed[i] describe car i."
    ),
    constraints=["1 <= n <= 10^5", "0 < target <= 10^6", "0 <= position[i] < target", "positions are unique"],
    signature="from typing import List\n\ndef car_fleet(target: int, position: List[int], speed: List[int]) -> int:",
    function_name="car_fleet",
    hints=[
        "Time to arrive, if alone, is (target - position) / speed.",
        "Sort cars by position descending, closest to the target first.",
        "A car joins the fleet ahead when its arrival time is less than or equal to that fleet's time. Otherwise it opens a new fleet.",
    ],
    approaches=[
        ("Simulate every time step", "too slow", "O(n)", "Not viable."),
        ("Sort and monotone times", "O(n log n)", "O(n)", "A stack of fleet arrival times."),
    ],
    editorial=(
        "Sort by starting position from the target backward. "
        "The first car is a fleet. Each later car merges into the fleet ahead when it would arrive no later than that fleet, because the one-lane rule prevents passing. "
        "Otherwise its own arrival time becomes a new fleet. The number of fleets is the number of times the arrival time strictly increases as you move away from the target."
    ),
    companies=["Amazon", "Google", "Bloomberg", "Uber"],
)
def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    cars = sorted(zip(position, speed), reverse=True)
    fleets = 0
    latest = 0.0
    for pos, spd in cars:
        time = (target - pos) / spd
        if time > latest:
            fleets += 1
            latest = time
    return fleets


def _oracle_car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    order = sorted(range(len(position)), key=lambda i: -position[i])
    stack: list[float] = []
    for i in order:
        time = (target - position[i]) / speed[i]
        if not stack or time > stack[-1]:
            stack.append(time)
    return len(stack)


cases(
    "car-fleet",
    _oracle_car_fleet,
    [
        ("classic", {"target": 12, "position": [10, 8, 0, 5, 3], "speed": [2, 4, 1, 1, 3]}, True, "Three fleets."),
        ("one", {"target": 10, "position": [3], "speed": [3]}, True, "One car."),
        ("two", {"target": 100, "position": [0, 2], "speed": [1, 1]}, False, None),
        ("catch", {"target": 10, "position": [0, 4], "speed": [2, 1]}, False, None),
        ("same-time", {"target": 10, "position": [6, 8], "speed": [2, 1]}, False, None),
    ],
)


@define(
    slug="score-of-parentheses",
    title="Score of Parentheses",
    difficulty="medium",
    topics=["stacks", "strings"],
    statement="The score of '()' is 1. The score of AB is score(A) + score(B). The score of (A) is 2 * score(A). `s` is a balanced parentheses string. Return its score.",
    constraints=["2 <= s.length <= 50", "s is balanced"],
    signature="def score_of_parentheses(s: str) -> int:",
    function_name="score_of_parentheses",
    hints=[
        "A stack of scores handles nesting. Push 0 on '(' as a frame.",
        "On ')', pop the frame. If it is 0, the pair was (), worth 1. Otherwise the frame is an inner score and the value is twice that.",
        "Add the value onto the new top, which accumulates adjacent groups.",
    ],
    approaches=[
        ("Recursion on matching pairs", "O(n)", "O(n)", "Find the span of each top-level group."),
        ("Stack of frames", "O(n)", "O(n)", "The iterative version."),
    ],
    editorial=(
        "Start with a stack containing 0, the score of the content outside everything. "
        "'(' pushes a fresh 0. ')' pops the inner score, turns 0 into 1 or doubles a positive score, and adds that onto the frame now on top. "
        "The only remaining value is the score of the whole string."
    ),
    companies=["Amazon", "Google", "Uber", "Adobe"],
)
def score_of_parentheses(s: str) -> int:
    stack = [0]
    for ch in s:
        if ch == "(":
            stack.append(0)
        else:
            inner = stack.pop()
            stack[-1] += 1 if inner == 0 else 2 * inner
    return stack[-1]


def _oracle_score_of_parentheses(s: str) -> int:
    def parse(i: int) -> tuple[int, int]:
        score = 0
        while i < len(s) and s[i] == "(":
            if s[i + 1] == ")":
                score += 1
                i += 2
            else:
                inner, i = parse(i + 1)
                score += 2 * inner
                i += 1
        return score, i

    return parse(0)[0]


cases(
    "score-of-parentheses",
    _oracle_score_of_parentheses,
    [
        ("one", {"s": "()"}, True, "Score 1."),
        ("double", {"s": "(())"}, True, "Score 2."),
        ("sum", {"s": "()()"}, False, None),
        ("mixed", {"s": "(()(()))"}, False, None),
        ("deep", {"s": "((()))"}, False, None),
    ],
)


@define(
    slug="remove-all-adjacent-duplicates-in-string",
    title="Remove All Adjacent Duplicates in String",
    difficulty="easy",
    topics=["stacks", "strings"],
    statement="Repeatedly remove adjacent pairs of the same character until none remain. Return the final string.",
    constraints=["1 <= s.length <= 10^5", "s is lowercase"],
    signature="def remove_duplicates(s: str) -> str:",
    function_name="remove_duplicates",
    hints=[
        "A stack stores the characters that have not yet been cancelled.",
        "If the new character equals the top, pop. Otherwise push.",
        "The stack from bottom to top is the answer. Removals cascade because the new top is checked on the next character.",
    ],
    approaches=[
        ("Repeated string replace", "O(n^2)", "O(n)", "Scan until stable."),
        ("Stack", "O(n)", "O(n)", "Each character is pushed and popped at most once."),
    ],
    editorial=(
        "The stack is the string built so far, with every adjacent duplicate already removed. "
        "A new character either cancels the last survivor or becomes a new survivor. "
        "That local rule is enough because a cancellation only exposes the previous survivor, which is exactly the stack top."
    ),
    companies=["Amazon", "Google", "Adobe", "Facebook"],
)
def remove_duplicates(s: str) -> str:
    stack: list[str] = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


def _oracle_remove_duplicates(s: str) -> str:
    stack: list[str] = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


cases(
    "remove-all-adjacent-duplicates-in-string",
    _oracle_remove_duplicates,
    [
        ("classic", {"s": "abbaca"}, True, "The result is ca."),
        ("all", {"s": "azxxzy"}, True, "The result is ay."),
        ("none", {"s": "abc"}, False, None),
        ("empty-result", {"s": "aa"}, False, None),
        ("single", {"s": "a"}, False, None),
    ],
)


@define(
    slug="min-stack",
    title="Min Stack",
    difficulty="medium",
    topics=["stacks", "design"],
    statement=(
        "Simulate a stack that supports push, pop, top, and getMin in constant time. "
        "`operations` names the calls. `arguments[i]` is [x] for push and [] otherwise. "
        "push and pop return null. top and getMin return an integer. getMin is the minimum value currently on the stack. pop is only called when the stack is nonempty."
    ),
    constraints=["-2^31 <= x <= 2^31 - 1", "At most 3 * 10^4 calls"],
    signature="from typing import List, Optional\n\ndef min_stack_ops(operations: List[str], arguments: List[List[int]]) -> List[Optional[int]]:",
    function_name="min_stack_ops",
    hints=[
        "A second stack stores the minimum at every height.",
        "On push, the new minimum is min(x, current minimum). Push that onto the min stack.",
        "Pop both stacks together. top reads the value stack. getMin reads the min stack.",
    ],
    approaches=[
        ("Scan the stack for the minimum", "O(n) per getMin", "O(n)", "Too slow if getMin is frequent."),
        ("Parallel minimum stack", "O(1) per call", "O(n)", "The minimum is stored at each depth."),
    ],
    editorial=(
        "The value stack is an ordinary stack. "
        "The minimum stack's top is the minimum of the value stack up to the same depth. "
        "Pushing writes min(x, previous minimum), using x itself when the stack was empty. Popping restores the previous minimum automatically."
    ),
    companies=["Amazon", "Bloomberg", "Microsoft", "Adobe"],
)
def min_stack_ops(operations: list[str], arguments: list[list[int]]) -> list[int | None]:
    values: list[int] = []
    mins: list[int] = []
    out: list[int | None] = []
    for op, arg in zip(operations, arguments):
        if op == "push":
            values.append(arg[0])
            mins.append(arg[0] if not mins else min(arg[0], mins[-1]))
            out.append(None)
        elif op == "pop":
            values.pop()
            mins.pop()
            out.append(None)
        elif op == "top":
            out.append(values[-1])
        else:
            out.append(mins[-1])
    return out


def _oracle_min_stack_ops(operations: list[str], arguments: list[list[int]]) -> list[int | None]:
    stack: list[int] = []
    out: list[int | None] = []
    for op, arg in zip(operations, arguments):
        if op == "push":
            stack.append(arg[0])
            out.append(None)
        elif op == "pop":
            stack.pop()
            out.append(None)
        elif op == "top":
            out.append(stack[-1])
        else:
            out.append(min(stack))
    return out


cases(
    "min-stack",
    _oracle_min_stack_ops,
    [
        (
            "classic",
            {
                "operations": ["push", "push", "push", "getMin", "pop", "top", "getMin"],
                "arguments": [[-2], [0], [-3], [], [], [], []],
            },
            True,
            "The minimum is -3, then -2 after the pop.",
        ),
        (
            "one",
            {"operations": ["push", "top", "getMin"], "arguments": [[5], [], []]},
            True,
            "A single value is both the top and the minimum.",
        ),
        (
            "ties",
            {"operations": ["push", "push", "getMin", "pop", "getMin"], "arguments": [[1], [1], [], [], []]},
            False,
            None,
        ),
        (
            "rise",
            {"operations": ["push", "push", "getMin", "top"], "arguments": [[2], [3], [], []]},
            False,
            None,
        ),
    ],
)


@define(
    slug="swap-nodes-in-pairs",
    title="Swap Nodes in Pairs",
    difficulty="medium",
    topics=["linked-lists"],
    statement="Swap every two adjacent nodes of the list, given as values, and return the new sequence. The values move with the nodes. Do not just swap the values in the algorithm: rewire next pointers.",
    constraints=["0 <= length <= 100"],
    signature="from typing import List\n\ndef swap_pairs(head: List[int]) -> List[int]:",
    function_name="swap_pairs",
    hints=[
        "A dummy node points at the original head so the first swap is uniform.",
        "Given prev, a, b, the rewiring is prev.next = b, a.next = b.next, b.next = a.",
        "Then move prev to a, which is now the second node of the pair, and repeat while two nodes remain.",
    ],
    approaches=[
        ("Swap values", "O(n)", "O(1)", "Shorter and rejected when the interviewer wants pointer rewiring."),
        ("Pointer swap", "O(n)", "O(1)", "Three links per pair."),
    ],
    editorial=(
        "Build the nodes, then walk pairs from a dummy head. "
        "Each iteration rewires three pointers and advances by two nodes. "
        "A trailing single node is left in place because the loop requires two successors."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Apple"],
)
def swap_pairs(head: list[int]) -> list[int]:
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt

    dummy = Node(0)
    current = dummy
    for value in head:
        current.nxt = Node(value)
        current = current.nxt
    prev = dummy
    while prev.nxt and prev.nxt.nxt:
        first = prev.nxt
        second = first.nxt
        first.nxt = second.nxt
        second.nxt = first
        prev.nxt = second
        prev = first
    out = []
    node = dummy.nxt
    while node:
        out.append(node.value)
        node = node.nxt
    return out


def _oracle_swap_pairs(head: list[int]) -> list[int]:
    out = head[:]
    for i in range(0, len(out) - 1, 2):
        out[i], out[i + 1] = out[i + 1], out[i]
    return out


cases(
    "swap-nodes-in-pairs",
    _oracle_swap_pairs,
    [
        ("classic", {"head": [1, 2, 3, 4]}, True, "The pairs swap to 2, 1, 4, 3."),
        ("odd", {"head": [1, 2, 3]}, True, "The last node stays."),
        ("empty", {"head": []}, False, None),
        ("one", {"head": [1]}, False, None),
        ("two", {"head": [1, 2]}, False, None),
    ],
)


@define(
    slug="odd-even-linked-list",
    title="Odd Even Linked List",
    difficulty="medium",
    topics=["linked-lists"],
    statement=(
        "Group nodes with odd 1-based indices before nodes with even indices, preserving relative order inside each group. "
        "The input is the value sequence. Rewire next pointers rather than building the answer by index arithmetic alone."
    ),
    constraints=["0 <= length <= 10^4"],
    signature="from typing import List\n\ndef odd_even_list(head: List[int]) -> List[int]:",
    function_name="odd_even_list",
    hints=[
        "Keep an odd tail and an even head and even tail.",
        "Weave: odd.next = even.next, then advance odd. even.next = odd.next, then advance even.",
        "Finally connect the odd tail to the even head.",
    ],
    approaches=[
        ("Collect two lists of values", "O(n)", "O(n)", "Index arithmetic."),
        ("Two pointer chains", "O(n)", "O(1)", "The in-place weave."),
    ],
    editorial=(
        "If the list has fewer than two nodes, return it. "
        "Otherwise odd and even walk the two chains. Each step pulls the next odd node forward and leaves the evens linked. "
        "Attaching the even head after the last odd node produces the grouped list without changing the order inside either chain."
    ),
    companies=["Amazon", "Adobe", "Microsoft", "Apple"],
)
def odd_even_list(head: list[int]) -> list[int]:
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt

    dummy = Node(0)
    tail = dummy
    for value in head:
        tail.nxt = Node(value)
        tail = tail.nxt
    if dummy.nxt is None or dummy.nxt.nxt is None:
        return head[:]
    odd = dummy.nxt
    even = odd.nxt
    even_head = even
    while even and even.nxt:
        odd.nxt = even.nxt
        odd = odd.nxt
        even.nxt = odd.nxt
        even = even.nxt
    odd.nxt = even_head
    out = []
    node = dummy.nxt
    while node:
        out.append(node.value)
        node = node.nxt
    return out


def _oracle_odd_even_list(head: list[int]) -> list[int]:
    return head[::2] + head[1::2]


cases(
    "odd-even-linked-list",
    _oracle_odd_even_list,
    [
        ("classic", {"head": [1, 2, 3, 4, 5]}, True, "Odds 1, 3, 5 then evens 2, 4."),
        ("even-length", {"head": [2, 1, 3, 5, 6, 4, 7]}, True, "The odd positions come first."),
        ("empty", {"head": []}, False, None),
        ("one", {"head": [1]}, False, None),
        ("two", {"head": [1, 2]}, False, None),
    ],
)


@define(
    slug="word-search",
    title="Word Search",
    difficulty="medium",
    topics=["backtracking", "matrix"],
    statement="Return true when `word` can be formed by adjacent letters on the board. Adjacent means 4-directional. A cell may be used once per path.",
    constraints=["1 <= m, n <= 6", "1 <= word.length <= 15", "board and word are lowercase"],
    signature="from typing import List\n\ndef exist(board: List[List[str]], word: str) -> bool:",
    function_name="exist",
    hints=[
        "DFS from every cell that matches the first letter.",
        "Mark the current cell as used before exploring neighbors, and unmark it afterward.",
        "Prune when the remaining board cannot contain the next character. The basic version just checks the character.",
    ],
    approaches=[
        ("DFS backtracking", "O(mn * 4^L)", "O(L)", "L is the word length. The board is small."),
        ("Trie of many words", "O(mn * 4^L)", "O(total word letters)", "The Word Search II upgrade."),
    ],
    editorial=(
        "The search state is the cell and the index in the word. "
        "A cell matches when it is in bounds, unused, and equal to word[index]. "
        "Mark it, try four neighbors at index + 1, and unmark it so another path can use it. Reaching the end of the word returns true."
    ),
    companies=["Amazon", "Microsoft", "Bloomberg", "Facebook"],
)
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[k]:
            return False
        saved = board[r][c]
        board[r][c] = "#"
        ok = any(dfs(r + dr, c + dc, k + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = saved
        return ok

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


def _oracle_exist(board: list[list[str]], word: str) -> bool:
    grid = [row[:] for row in board]
    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != word[k]:
            return False
        saved = grid[r][c]
        grid[r][c] = "#"
        found = any(dfs(r + dr, c + dc, k + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        grid[r][c] = saved
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


cases(
    "word-search",
    _oracle_exist,
    [
        ("yes", {"board": [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "word": "ABCCED"}, True, "The word snakes through the board."),
        ("no", {"board": [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "word": "ABCB"}, True, "The path would reuse B."),
        ("single", {"board": [["A"]], "word": "A"}, False, None),
        ("see", {"board": [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "word": "SEE"}, False, None),
        ("miss", {"board": [["A"]], "word": "B"}, False, None),
    ],
)


@define(
    slug="palindrome-partitioning",
    title="Palindrome Partitioning",
    difficulty="medium",
    topics=["backtracking", "dynamic-programming", "strings"],
    statement="Partition `s` so every substring is a palindrome. Return all partitions, each as a list of substrings. Sort the partitions.",
    constraints=["1 <= s.length <= 16", "s is lowercase"],
    signature="from typing import List\n\ndef partition(s: str) -> List[List[str]]:",
    function_name="partition",
    hints=[
        "A cut is legal when the chosen prefix is a palindrome.",
        "Recurse on the suffix and append the prefix to the path.",
        "A boolean table of palindromic slices makes the check O(1) after O(n^2) preprocessing. A direct check is fine at n <= 16.",
    ],
    approaches=[
        ("Backtracking with slice checks", "O(n * 2^n)", "O(n)", "Every partition is a choice of cuts."),
        ("DP palindrome table plus backtracking", "O(n * 2^n)", "O(n^2)", "The check becomes constant time."),
    ],
    editorial=(
        "At index i, try every end j >= i. If s[i:j+1] is a palindrome, append it and partition the rest. "
        "When i reaches the end, copy the path. "
        "Sorting the list of partitions makes tests deterministic. The first cut is forced to be considered in increasing length, which already yields a stable order if you do not sort, but sorting is harmless."
    ),
    companies=["Amazon", "Google", "Bloomberg", "Adobe"],
)
def partition(s: str) -> list[list[str]]:
    out: list[list[str]] = []
    path: list[str] = []

    def dfs(i: int) -> None:
        if i == len(s):
            out.append(path[:])
            return
        for j in range(i, len(s)):
            piece = s[i : j + 1]
            if piece == piece[::-1]:
                path.append(piece)
                dfs(j + 1)
                path.pop()

    dfs(0)
    out.sort()
    return out


def _oracle_partition(s: str) -> list[list[str]]:
    out: list[list[str]] = []

    def dfs(i: int, path: list[str]) -> None:
        if i == len(s):
            out.append(path[:])
            return
        for j in range(i + 1, len(s) + 1):
            piece = s[i:j]
            if piece == piece[::-1]:
                path.append(piece)
                dfs(j, path)
                path.pop()

    dfs(0, [])
    out.sort()
    return out


cases(
    "palindrome-partitioning",
    _oracle_partition,
    [
        ("aab", {"s": "aab"}, True, "Two partitions: a,a,b and aa,b."),
        ("a", {"s": "a"}, True, "One partition."),
        ("aaa", {"s": "aaa"}, False, None),
        ("ab", {"s": "ab"}, False, None),
        ("aba", {"s": "aba"}, False, None),
    ],
)


@define(
    slug="graph-valid-tree",
    title="Graph Valid Tree",
    difficulty="medium",
    topics=["graphs", "union-find"],
    statement=(
        "You have `n` nodes labeled 0..n-1 and an undirected edge list. "
        "Return true when the edges form a tree: they connect every node and contain no cycle."
    ),
    constraints=["1 <= n <= 2000", "0 <= edges.length <= 5000"],
    signature="from typing import List\n\ndef valid_tree(n: int, edges: List[List[int]]) -> bool:",
    function_name="valid_tree",
    hints=[
        "A tree on n nodes has exactly n - 1 edges. Any other count is immediately false.",
        "With exactly n - 1 edges, the graph is a tree exactly when it is connected, or exactly when it has no cycle. Either extra check is enough.",
        "Union-find detects a cycle when an edge joins two nodes already in the same component. After n - 1 successful unions there is one component.",
    ],
    approaches=[
        ("DFS connectivity plus edge count", "O(n + edges)", "O(n + edges)", "Visit every node from 0 and reject a back edge to a non-parent."),
        ("Disjoint set", "O(n + edges)", "O(n)", "Reject early cycles and require n - 1 edges."),
    ],
    editorial=(
        "Check the edge count first. Then union the endpoints of every edge. "
        "If find already agrees, the edge closes a cycle. "
        "With n - 1 successful unions the components collapse to one, which is a tree."
    ),
    companies=["Google", "Amazon", "Facebook", "LinkedIn"],
)
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def _oracle_valid_tree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    seen = [False] * n

    def dfs(node: int, parent: int) -> bool:
        seen[node] = True
        for nxt in graph[node]:
            if nxt == parent:
                continue
            if seen[nxt] or not dfs(nxt, node):
                return False
        return True

    return dfs(0, -1) and all(seen)


cases(
    "graph-valid-tree",
    _oracle_valid_tree,
    [
        ("yes", {"n": 5, "edges": [[0, 1], [0, 2], [0, 3], [1, 4]]}, True, "Five nodes and four edges, connected, no cycle."),
        ("cycle", {"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]}, True, "Five edges on five nodes cannot be a tree."),
        ("one", {"n": 1, "edges": []}, False, None),
        ("disconnected", {"n": 4, "edges": [[0, 1], [2, 3]]}, False, None),
        ("line", {"n": 3, "edges": [[0, 1], [1, 2]]}, False, None),
    ],
)


@define(
    slug="number-of-enclaves",
    title="Number of Enclaves",
    difficulty="medium",
    topics=["graphs", "dfs", "grid"],
    statement="Return the number of land cells (1) that cannot reach the border by 4-directional moves. Land on the border, and land connected to it, can escape.",
    constraints=["1 <= m, n <= 500", "grid[i][j] is 0 or 1"],
    signature="from typing import List\n\ndef num_enclaves(grid: List[List[int]]) -> int:",
    function_name="num_enclaves",
    hints=[
        "Flood every border land cell and mark the connected land as escaped.",
        "Count the land cells that remain unmarked.",
        "This is the same border-flood idea as surrounded regions, counting cells instead of flipping them.",
    ],
    approaches=[
        ("DFS from each land cell", "O(mn)", "O(mn)", "See whether the component touches the border."),
        ("Border flood then count", "O(mn)", "O(mn)", "One flood, one count."),
    ],
    editorial=(
        "Start DFS or BFS from every border land cell and mark visited land. "
        "Those cells can walk off the board. "
        "Every other land cell is an enclave. Count them."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def num_enclaves(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    def flood(r: int, c: int) -> None:
        stack = [(r, c)]
        seen[r][c] = True
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == 1:
                    seen[nx][ny] = True
                    stack.append((nx, ny))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r in (0, rows - 1) or c in (0, cols - 1)):
                flood(r, c)
    return sum(grid[r][c] == 1 and not seen[r][c] for r in range(rows) for c in range(cols))


def _oracle_num_enclaves(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    def escapes(r: int, c: int) -> bool:
        stack = [(r, c)]
        component = []
        seen[r][c] = True
        border = False
        while stack:
            x, y = stack.pop()
            component.append((x, y))
            border = border or x in (0, rows - 1) or y in (0, cols - 1)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == 1:
                    seen[nx][ny] = True
                    stack.append((nx, ny))
        return border

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c] and not escapes(r, c):
                # recount this component
                pass
    # simpler recount
    seen = [[False] * cols for _ in range(rows)]
    answer = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or seen[r][c]:
                continue
            stack = [(r, c)]
            seen[r][c] = True
            cells = 0
            border = False
            while stack:
                x, y = stack.pop()
                cells += 1
                border = border or x in (0, rows - 1) or y in (0, cols - 1)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == 1:
                        seen[nx][ny] = True
                        stack.append((nx, ny))
            if not border:
                answer += cells
    return answer


cases(
    "number-of-enclaves",
    _oracle_num_enclaves,
    [
        ("classic", {"grid": [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]}, True, "Three land cells are trapped."),
        ("escape", {"grid": [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]}, True, "Every land cell can reach the border."),
        ("none", {"grid": [[0, 0], [0, 0]]}, False, None),
        ("one", {"grid": [[1]]}, False, None),
        ("center", {"grid": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]}, False, None),
    ],
)


@define(
    slug="open-the-lock",
    title="Open the Lock",
    difficulty="medium",
    topics=["graphs", "bfs"],
    statement=(
        "A lock has 4 circular wheels, each showing 0..9. It starts at '0000'. "
        "One move turns one wheel by one slot. `deadends` jam the lock if you reach them, including at the start. "
        "Return the minimum moves to reach `target`, or -1."
    ),
    constraints=["1 <= deadends.length <= 500", "deadends and target are 4-digit strings"],
    signature="from typing import List\n\ndef open_lock(deadends: List[str], target: str) -> int:",
    function_name="open_lock",
    hints=[
        "This is an unweighted graph of 10000 nodes. BFS gives the shortest path.",
        "Each node has 8 neighbors: each wheel up or down.",
        "Put deadends in a set and treat them as removed nodes. If the start is dead, return -1.",
    ],
    approaches=[
        ("Bidirectional BFS", "O(10^4)", "O(10^4)", "Search from both ends."),
        ("Ordinary BFS", "O(10^4)", "O(10^4)", "The wheel space is tiny."),
    ],
    editorial=(
        "BFS from 0000 with distance 0, skipping deadends. "
        "Generate a neighbor by adding or subtracting one on one digit, modulo 10. "
        "The first time the target is dequeued, or generated, its distance is optimal."
    ),
    companies=["Amazon", "Google", "Facebook", "Uber"],
)
def open_lock(deadends: list[str], target: str) -> int:
    blocked = set(deadends)
    if "0000" in blocked:
        return -1
    queue = deque([("0000", 0)])
    seen = {"0000"}
    while queue:
        state, dist = queue.popleft()
        if state == target:
            return dist
        chars = list(state)
        for i in range(4):
            original = chars[i]
            for delta in (-1, 1):
                chars[i] = str((int(original) + delta) % 10)
                nxt = "".join(chars)
                if nxt not in seen and nxt not in blocked:
                    seen.add(nxt)
                    queue.append((nxt, dist + 1))
            chars[i] = original
    return -1


def _oracle_open_lock(deadends: list[str], target: str) -> int:
    blocked = set(deadends)
    if "0000" in blocked:
        return -1
    queue = deque([("0000", 0)])
    seen = set(blocked)
    seen.add("0000")
    while queue:
        state, dist = queue.popleft()
        if state == target:
            return dist
        for i in range(4):
            digit = int(state[i])
            for nxt_digit in ((digit + 1) % 10, (digit - 1) % 10):
                nxt = state[:i] + str(nxt_digit) + state[i + 1 :]
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, dist + 1))
    return -1


cases(
    "open-the-lock",
    _oracle_open_lock,
    [
        ("classic", {"deadends": ["0201", "0101", "0102", "1212", "2002"], "target": "0202"}, True, "The shortest path has length 6."),
        ("dead-start", {"deadends": ["0000"], "target": "8888"}, True, "The start is jammed."),
        ("zero", {"deadends": [], "target": "0000"}, False, None),
        ("one", {"deadends": [], "target": "0001"}, False, None),
        ("blocked", {"deadends": ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "target": "8888"}, False, None),
    ],
)


@define(
    slug="find-eventual-safe-states",
    title="Find Eventual Safe States",
    difficulty="medium",
    topics=["graphs", "dfs", "topological-sort"],
    statement=(
        "A node is safe when every path starting there ends at a terminal node. "
        "`graph` is a directed adjacency list. Return every safe node in increasing order."
    ),
    constraints=["1 <= n <= 10^4", "0 <= graph[i].length <= n", "The graph may contain cycles"],
    signature="from typing import List\n\ndef eventual_safe_nodes(graph: List[List[int]]) -> List[int]:",
    function_name="eventual_safe_nodes",
    hints=[
        "A node on a cycle, or that can reach a cycle, is unsafe.",
        "DFS colors: gray means the node is on the current stack. A gray neighbor means a cycle.",
        "A node is safe when every neighbor is safe. Memoize the result.",
    ],
    approaches=[
        ("DFS with memo and a recursion stack", "O(V + E)", "O(V)", "Three colors."),
        ("Reverse edges and Kahn", "O(V + E)", "O(V + E)", "Terminal nodes have outdegree 0. Safe nodes are those that reach only terminals, which is a topological peel on the reversed graph."),
    ],
    editorial=(
        "Color 0 is unseen, 1 is on the stack, and 2 is done and safe. "
        "If a neighbor is gray, this node reaches a cycle and is unsafe. "
        "If every neighbor returns safe, paint this node safe. Collect the safe nodes in order."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def eventual_safe_nodes(graph: list[list[int]]) -> list[int]:
    n = len(graph)
    color = [0] * n

    def safe(node: int) -> bool:
        if color[node]:
            return color[node] == 2
        color[node] = 1
        if any(not safe(nxt) for nxt in graph[node]):
            return False
        color[node] = 2
        return True

    return [node for node in range(n) if safe(node)]


def _oracle_eventual_safe_nodes(graph: list[list[int]]) -> list[int]:
    n = len(graph)
    reverse = [[] for _ in range(n)]
    outdegree = [len(graph[node]) for node in range(n)]
    for node in range(n):
        for nxt in graph[node]:
            reverse[nxt].append(node)
    queue = deque(node for node in range(n) if outdegree[node] == 0)
    safe = []
    while queue:
        node = queue.popleft()
        safe.append(node)
        for prev in reverse[node]:
            outdegree[prev] -= 1
            if outdegree[prev] == 0:
                queue.append(prev)
    return sorted(safe)


cases(
    "find-eventual-safe-states",
    _oracle_eventual_safe_nodes,
    [
        ("classic", {"graph": [[1, 2], [2, 3], [5], [0], [5], [], []]}, True, "Nodes 2, 4, 5, and 6 are safe."),
        ("terminal", {"graph": [[], [0, 2], []]}, True, "Every node reaches a terminal."),
        ("cycle", {"graph": [[1], [0]]}, False, None),
        ("one", {"graph": [[]]}, False, None),
        ("self", {"graph": [[0]]}, False, None),
    ],
)


@define(
    slug="accounts-merge",
    title="Accounts Merge",
    difficulty="medium",
    topics=["graphs", "union-find", "hashing"],
    statement=(
        "Each account is a name followed by email addresses. "
        "Merge accounts that share an email. The same name does not by itself mean the same person. "
        "Return the merged accounts, each starting with the name and then the sorted unique emails. Sort the accounts by name and then by the email list."
    ),
    constraints=["1 <= accounts.length <= 1000", "1 <= emails per account <= 10"],
    signature="from typing import List\n\ndef accounts_merge(accounts: List[List[str]]) -> List[List[str]]:",
    function_name="accounts_merge",
    hints=[
        "Emails are nodes. Emails in the same account are connected.",
        "Union-find groups emails. Remember one name for each email.",
        "After unions, collect emails by root, sort them, and prefix the name.",
    ],
    approaches=[
        ("DFS on an email graph", "O(total emails)", "O(total emails)", "Build edges between consecutive emails of an account."),
        ("Disjoint set", "O(total emails)", "O(total emails)", "Union every email with the first email of its account."),
    ],
    editorial=(
        "Map each email to an integer and union it with the account's first email. "
        "Store the name on the first email. "
        "Group emails by the find-root, sort each group, and emit name plus emails. Sort the accounts so the output is unique."
    ),
    companies=["Facebook", "Amazon", "Google", "Uber"],
)
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    parent: dict[str, str] = {}
    owner: dict[str, str] = {}

    def find(email: str) -> str:
        parent.setdefault(email, email)
        while parent[email] != email:
            parent[email] = parent[parent[email]]
            email = parent[email]
        return email

    for account in accounts:
        name, first, *rest = account
        owner[find(first)] = name
        root = find(first)
        for email in rest:
            parent[find(email)] = root
            owner.setdefault(email, name)
    groups: dict[str, list[str]] = defaultdict(list)
    for email in list(parent):
        groups[find(email)].append(email)
    merged = [[owner[root], *sorted(emails)] for root, emails in groups.items()]
    merged.sort()
    return merged


def _oracle_accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    email_id: dict[str, int] = {}
    names: list[str] = []
    ids = 0
    groups: list[list[str]] = []
    for account in accounts:
        name = account[0]
        ids_here = []
        for email in account[1:]:
            if email not in email_id:
                email_id[email] = ids
                names.append(name)
                groups.append([email])
                ids += 1
            ids_here.append(email_id[email])
        for other in ids_here[1:]:
            a, b = ids_here[0], other
            # union later via DFS graph
            pass
    graph = [[] for _ in range(ids)]
    for account in accounts:
        emails = account[1:]
        for email in emails[1:]:
            a, b = email_id[emails[0]], email_id[email]
            graph[a].append(b)
            graph[b].append(a)
    seen = [False] * ids
    merged = []
    for start in range(ids):
        if seen[start]:
            continue
        stack = [start]
        seen[start] = True
        emails = []
        while stack:
            node = stack.pop()
            emails.append(groups[node][0])
            for nxt in graph[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
        merged.append([names[start], *sorted(emails)])
    merged.sort()
    return merged


cases(
    "accounts-merge",
    _oracle_accounts_merge,
    [
        (
            "classic",
            {
                "accounts": [
                    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                    ["John", "johnsmith@mail.com", "john00@mail.com"],
                    ["Mary", "mary@mail.com"],
                    ["John", "johnnybravo@mail.com"],
                ]
            },
            True,
            "The two John Smith accounts merge. Johnny Bravo stays separate.",
        ),
        (
            "one",
            {"accounts": [["Gabe", "gabe@mail.com"]]},
            True,
            "A single account.",
        ),
        (
            "same-name",
            {"accounts": [["A", "a@x.com"], ["A", "b@x.com"]]},
            False,
            None,
        ),
        (
            "chain",
            {"accounts": [["A", "1@x.com", "2@x.com"], ["A", "2@x.com", "3@x.com"], ["B", "4@x.com"]]},
            False,
            None,
        ),
    ],
)


@define(
    slug="queue-reconstruction-by-height",
    title="Queue Reconstruction by Height",
    difficulty="medium",
    topics=["greedy", "sorting"],
    statement=(
        "people[i] = [h, k] means a person of height h who expects exactly k people in front of them who are at least as tall. "
        "Reconstruct the queue. The input guarantees a solution."
    ),
    constraints=["1 <= people.length <= 1100", "0 <= h, k < people.length? heights up to 10^6"],
    signature="from typing import List\n\ndef reconstruct_queue(people: List[List[int]]) -> List[List[int]]:",
    function_name="reconstruct_queue",
    hints=[
        "Sort by height descending, and for equal height by k ascending.",
        "Insert each person at index k in a list that already contains only taller or equal people.",
        "Because shorter people are inserted later, they do not change the k-count of the taller people already placed.",
    ],
    approaches=[
        ("Sort and insert", "O(n^2)", "O(n)", "List insertion is linear. n is at most about 1100."),
        ("Fenwick or segment tree of empty slots", "O(n log n)", "O(n)", "The faster version of the same placement."),
    ],
    editorial=(
        "Taller people are invisible to shorter people's k counts, but shorter people are invisible to taller people's counts. "
        "Place the tallest first. Their k is then an absolute index. "
        "Each later person inserts at index k among the people already placed, all of whom are at least as tall."
    ),
    companies=["Amazon", "Google", "Adobe", "Bloomberg"],
)
def reconstruct_queue(people: list[list[int]]) -> list[list[int]]:
    people = sorted(people, key=lambda person: (-person[0], person[1]))
    queue: list[list[int]] = []
    for person in people:
        queue.insert(person[1], person)
    return queue


def _oracle_reconstruct_queue(people: list[list[int]]) -> list[list[int]]:
    ordered = sorted(people, key=lambda person: (-person[0], person[1]))
    queue: list[list[int]] = []
    for person in ordered:
        queue.insert(person[1], person[:])
    return queue


cases(
    "queue-reconstruction-by-height",
    _oracle_reconstruct_queue,
    [
        (
            "classic",
            {"people": [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]},
            True,
            "The reconstructed queue places taller people according to k.",
        ),
        ("one", {"people": [[1, 0]]}, True, "A single person."),
        ("two", {"people": [[2, 0], [1, 1]]}, False, None),
        ("same-height", {"people": [[3, 0], [3, 1], [3, 2]]}, False, None),
        ("mixed", {"people": [[6, 0], [5, 0], [4, 0]]}, False, None),
    ],
)


@define(
    slug="rod-cutting",
    title="Rod Cutting",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement=(
        "`prices[i]` is the price of a rod piece of length i + 1. "
        "Return the maximum revenue from cutting a rod of length `n` into pieces. Not cutting is allowed. n equals len(prices)."
    ),
    constraints=["1 <= n <= 100", "1 <= prices[i] <= 1000"],
    signature="from typing import List\n\ndef rod_cutting(prices: List[int]) -> int:",
    function_name="rod_cutting",
    hints=[
        "This is unbounded knapsack. A length can be used many times.",
        "dp[L] is the best revenue for a rod of length L.",
        "dp[L] = max over piece length p <= L of prices[p - 1] + dp[L - p].",
    ],
    approaches=[
        ("Recursion", "exponential", "O(n)", "Try the first cut."),
        ("Unbounded DP", "O(n^2)", "O(n)", "Fill lengths from 1 to n."),
    ],
    editorial=(
        "The first piece has some length p. The remainder is an independent smaller rod. "
        "Trying every p and taking the max, with smaller lengths already solved, is the optimal substructure. "
        "dp[0] is 0. The answer is dp[n]."
    ),
    companies=["Amazon", "Microsoft", "Google", "Adobe"],
)
def rod_cutting(prices: list[int]) -> int:
    n = len(prices)
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        for piece in range(1, length + 1):
            dp[length] = max(dp[length], prices[piece - 1] + dp[length - piece])
    return dp[n]


def _oracle_rod_cutting(prices: list[int]) -> int:
    n = len(prices)

    def best(length: int) -> int:
        if length == 0:
            return 0
        return max(prices[piece - 1] + best(length - piece) for piece in range(1, length + 1))

    return best(n)


cases(
    "rod-cutting",
    _oracle_rod_cutting,
    [
        ("classic", {"prices": [1, 5, 8, 9, 10, 17, 17, 20]}, True, "A rod of length 8 is best cut for 22."),
        ("one", {"prices": [3]}, True, "Do not cut."),
        ("two", {"prices": [1, 5]}, False, None),
        ("prefer-pieces", {"prices": [2, 5, 7]}, False, None),
        ("flat", {"prices": [1, 2, 3, 4]}, False, None),
    ],
)


@define(
    slug="interleaving-string",
    title="Interleaving String",
    difficulty="medium",
    topics=["dynamic-programming", "strings"],
    statement="Return true when `s3` is formed by interleaving `s1` and `s2`. An interleaving preserves the relative order of characters from each string.",
    constraints=["0 <= s1.length, s2.length <= 100", "s3.length == s1.length + s2.length"],
    signature="def is_interleave(s1: str, s2: str, s3: str) -> bool:",
    function_name="is_interleave",
    hints=[
        "If the lengths do not add up, return false immediately.",
        "dp[i][j] means s1[:i] and s2[:j] interleave to s3[:i+j].",
        "The cell is true when the previous row matches the new s1 character, or the previous column matches the new s2 character.",
    ],
    approaches=[
        ("Recursion with memo", "O(n * m)", "O(n * m)", "State is the two indexes."),
        ("Boolean DP", "O(n * m)", "O(n * m)", "Or one rolling row."),
    ],
    editorial=(
        "dp[0][0] is true. "
        "A first-row cell depends only on s2, and a first-column cell only on s1. "
        "Every other cell looks up and left. The bottom-right cell is the answer."
    ),
    companies=["Amazon", "Google", "Bloomberg", "Microsoft"],
)
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    if len(s1) + len(s2) != len(s3):
        return False
    dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    dp[0][0] = True
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True
            if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True
    return dp[-1][-1]


def _oracle_is_interleave(s1: str, s2: str, s3: str) -> bool:
    if len(s1) + len(s2) != len(s3):
        return False

    def ok(i: int, j: int) -> bool:
        if i == len(s1) and j == len(s2):
            return True
        k = i + j
        if i < len(s1) and s1[i] == s3[k] and ok(i + 1, j):
            return True
        if j < len(s2) and s2[j] == s3[k] and ok(i, j + 1):
            return True
        return False

    return ok(0, 0)


cases(
    "interleaving-string",
    _oracle_is_interleave,
    [
        ("yes", {"s1": "aabcc", "s2": "dbbca", "s3": "aadbbcbcac"}, True, "One interleaving exists."),
        ("no", {"s1": "aabcc", "s2": "dbbca", "s3": "aadbbbaccc"}, True, "No interleaving preserves both orders."),
        ("empty", {"s1": "", "s2": "", "s3": ""}, False, None),
        ("one", {"s1": "a", "s2": "", "s3": "a"}, False, None),
        ("short", {"s1": "ab", "s2": "cd", "s3": "acbd"}, False, None),
    ],
)
