"""Classic dynamic-programming problems with brute-force oracles on small inputs."""

from __future__ import annotations

from lib import cases, define


@define(
    slug="climbing-stairs",
    title="Climbing Stairs",
    difficulty="easy",
    topics=["dynamic-programming"],
    statement="You climb `n` stairs taking 1 or 2 steps at a time. Return the number of distinct ways to reach the top. Order matters.",
    constraints=["1 <= n <= 45"],
    signature="def climb_stairs(n: int) -> int:",
    function_name="climb_stairs",
    hints=[
        "To reach step n you last came from n - 1 or n - 2.",
        "That is the Fibonacci recurrence. ways(n) = ways(n - 1) + ways(n - 2).",
        "Two rolling variables compute it in constant space. ways(1) = 1 and ways(2) = 2.",
    ],
    approaches=[
        ("Naive recursion", "O(2^n)", "O(n)", "Overlapping subproblems explode."),
        ("Rolling Fibonacci", "O(n)", "O(1)", "Keep only the previous two answers."),
    ],
    editorial=(
        "Let dp[i] be the number of ways to reach step i. The last step is a single step from i - 1 or a double step from i - 2, and those sets are disjoint. "
        "So dp[i] = dp[i - 1] + dp[i - 2], with dp[1] = 1 and dp[2] = 2. Only two scalars are required."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def _oracle_climb_stairs(n: int) -> int:
    def ways(k: int) -> int:
        if k <= 2:
            return k
        return ways(k - 1) + ways(k - 2)

    return ways(n)


cases(
    "climbing-stairs",
    _oracle_climb_stairs,
    [
        ("two", {"n": 2}, True, "1+1 and 2."),
        ("three", {"n": 3}, True, "Three ways."),
        ("one", {"n": 1}, False, None),
        ("five", {"n": 5}, False, None),
        ("eight", {"n": 8}, False, None),
    ],
)


@define(
    slug="house-robber",
    title="House Robber",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Rob houses in a line. You cannot rob two adjacent houses. Return the maximum amount. `nums[i]` is the money in house i.",
    constraints=["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
    signature="from typing import List\n\ndef rob_line(nums: List[int]) -> int:",
    function_name="rob_line",
    hints=[
        "At each house, either skip it and keep the previous best, or rob it and add the best from two houses back.",
        "dp[i] = max(dp[i - 1], dp[i - 2] + nums[i]).",
        "Two variables replace the array.",
    ],
    approaches=[
        ("Recursion with memo", "O(n)", "O(n)", "The state is the starting index."),
        ("Linear DP", "O(n)", "O(1)", "Rolling skip and take."),
    ],
    editorial=(
        "The optimal decision for a prefix ends by skipping the last house or taking it. "
        "Those two choices look at the answers one and two steps back. "
        "Walk the street once, keeping the best total that does not use the previous house and the best total overall."
    ),
    companies=["Amazon", "Google", "Microsoft", "Airbnb"],
)
def rob_line(nums: list[int]) -> int:
    prev2 = prev1 = 0
    for value in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + value)
    return prev1


def _oracle_rob_line(nums: list[int]) -> int:
    def best(i: int) -> int:
        if i >= len(nums):
            return 0
        return max(best(i + 1), nums[i] + best(i + 2))

    return best(0)


cases(
    "house-robber",
    _oracle_rob_line,
    [
        ("classic", {"nums": [1, 2, 3, 1]}, True, "Rob houses 1 and 3 for 4. Indexing from the example, 1+3."),
        ("alt", {"nums": [2, 7, 9, 3, 1]}, True, "2 + 9 + 1 = 12."),
        ("one", {"nums": [5]}, False, None),
        ("two", {"nums": [2, 1]}, False, None),
        ("zeros", {"nums": [0, 0, 0]}, False, None),
    ],
)


@define(
    slug="house-robber-ii",
    title="House Robber II",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Houses are arranged in a circle, so the first and last houses are adjacent. Return the maximum amount you can rob without robbing adjacent houses.",
    constraints=["1 <= nums.length <= 100", "0 <= nums[i] <= 1000"],
    signature="from typing import List\n\ndef rob_circle(nums: List[int]) -> int:",
    function_name="rob_circle",
    hints=[
        "The circle only adds one constraint: you cannot take both the first and the last house.",
        "Run the linear robber on nums without the last house, and again on nums without the first house.",
        "The answer is the larger of those two results. A single house is its own answer.",
    ],
    approaches=[
        ("Case recursion", "O(2^n)", "O(n)", "Branch on taking the first house."),
        ("Two linear passes", "O(n)", "O(1)", "Reuse House Robber."),
    ],
    editorial=(
        "Any optimal circular plan either excludes the first house or excludes the last house. "
        "The linear algorithm solves each of those ranges. "
        "Take the maximum. The two ranges overlap in the middle, which is allowed because the plans are alternatives, not a combination."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def rob_circle(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    def linear(values: list[int]) -> int:
        prev2 = prev1 = 0
        for value in values:
            prev2, prev1 = prev1, max(prev1, prev2 + value)
        return prev1

    return max(linear(nums[:-1]), linear(nums[1:]))


def _oracle_rob_circle(nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]
    best = 0
    for mask in range(1 << n):
        total = 0
        ok = True
        for i in range(n):
            if mask >> i & 1:
                if mask >> ((i + 1) % n) & 1:
                    ok = False
                    break
                total += nums[i]
        if ok:
            best = max(best, total)
    return best


cases(
    "house-robber-ii",
    _oracle_rob_circle,
    [
        ("classic", {"nums": [2, 3, 2]}, True, "Rob the middle house only."),
        ("four", {"nums": [1, 2, 3, 1]}, True, "Rob the first and third, or the second, for 4? 1+3=4 and first-last conflict. Answer 4."),
        ("one", {"nums": [8]}, False, None),
        ("two", {"nums": [1, 2]}, False, None),
        ("five", {"nums": [1, 3, 1, 3, 100]}, False, None),
    ],
)


@define(
    slug="coin-change",
    title="Coin Change",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Return the fewest coins that sum to `amount`. You have an unlimited supply of each coin in `coins`. Return -1 if the amount cannot be made.",
    constraints=["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
    signature="from typing import List\n\ndef coin_change(coins: List[int], amount: int) -> int:",
    function_name="coin_change",
    hints=[
        "dp[x] is the fewest coins that make x.",
        "dp[x] = 1 + min(dp[x - coin]) over coins that do not exceed x.",
        "Initialize dp[0] to 0 and every other cell to a sentinel larger than any real answer. If the sentinel remains, return -1.",
    ],
    approaches=[
        ("BFS on the remainder", "O(amount * coins)", "O(amount)", "Each edge subtracts one coin. The depth is the fewest coins."),
        ("Unbounded knapsack DP", "O(amount * coins)", "O(amount)", "The classic bottom-up recurrence."),
    ],
    editorial=(
        "This is unbounded knapsack where every item has weight equal to its value and the cost is the number of items. "
        "Filling amounts from 0 to amount, and trying every coin, enforces that a coin may be reused because smaller amounts are already solved. "
        "amount 0 needs 0 coins."
    ),
    companies=["Amazon", "Google", "Bloomberg", "Microsoft"],
)
def coin_change(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value:
                dp[value] = min(dp[value], dp[value - coin] + 1)
    return -1 if dp[amount] > amount else dp[amount]


def _oracle_coin_change(coins: list[int], amount: int) -> int:
    from collections import deque

    queue = deque([(0, 0)])
    seen = {0}
    while queue:
        total, count = queue.popleft()
        if total == amount:
            return count
        for coin in coins:
            nxt = total + coin
            if nxt <= amount and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, count + 1))
    return -1


cases(
    "coin-change",
    _oracle_coin_change,
    [
        ("classic", {"coins": [1, 2, 5], "amount": 11}, True, "5 + 5 + 1 uses three coins."),
        ("impossible", {"coins": [2], "amount": 3}, True, "Odd amounts cannot be made from twos."),
        ("zero", {"coins": [1], "amount": 0}, False, None),
        ("one", {"coins": [1], "amount": 2}, False, None),
        ("choice", {"coins": [1, 3, 4], "amount": 6}, False, None),
    ],
)


@define(
    slug="coin-change-ii",
    title="Coin Change II",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Return the number of combinations that make `amount`. Coin order does not matter, and you have unlimited coins of each type. The answer fits in a 32-bit signed integer for these tests.",
    constraints=["1 <= coins.length <= 300", "1 <= coins[i] <= 5000", "0 <= amount <= 5000"],
    signature="from typing import List\n\ndef change(amount: int, coins: List[int]) -> int:",
    function_name="change",
    hints=[
        "Counting combinations, not permutations, means each coin is considered in an outer loop.",
        "If the coin loop is inside the amount loop, you count ordered sequences.",
        "dp[0] = 1, the empty combination.",
    ],
    approaches=[
        ("Recursion with a start index", "exponential", "O(coins)", "The start index enforces nondecreasing coin order."),
        ("1D unbounded knapsack", "O(amount * coins)", "O(amount)", "Outer coin, inner amount ascending."),
    ],
    editorial=(
        "Iterate coins on the outside. For each coin, update every amount from the coin up to the target by adding dp[amount - coin]. "
        "Because the coin is fixed in the outer loop, combinations are counted once in coin order. "
        "The inner loop ascending is what allows unlimited use of the current coin."
    ),
    companies=["Amazon", "Google", "Bloomberg", "Microsoft"],
)
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for value in range(coin, amount + 1):
            dp[value] += dp[value - coin]
    return dp[amount]


def _oracle_change(amount: int, coins: list[int]) -> int:
    coins = tuple(sorted(coins))

    def ways(remain: int, start: int) -> int:
        if remain == 0:
            return 1
        total = 0
        for i in range(start, len(coins)):
            if coins[i] > remain:
                break
            total += ways(remain - coins[i], i)
        return total

    return ways(amount, 0)


cases(
    "coin-change-ii",
    _oracle_change,
    [
        ("classic", {"amount": 5, "coins": [1, 2, 5]}, True, "Four combinations."),
        ("one-type", {"amount": 3, "coins": [2]}, True, "3 cannot be made."),
        ("zero", {"amount": 0, "coins": [7]}, False, None),
        ("ten", {"amount": 10, "coins": [2, 5]}, False, None),
        ("three", {"amount": 4, "coins": [1, 2, 3]}, False, None),
    ],
)


@define(
    slug="longest-increasing-subsequence",
    title="Longest Increasing Subsequence",
    difficulty="medium",
    topics=["dynamic-programming", "binary-search"],
    statement="Return the length of the longest strictly increasing subsequence of `nums`. The subsequence need not be contiguous.",
    constraints=["1 <= nums.length <= 2500", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef length_of_lis(nums: List[int]) -> int:",
    function_name="length_of_lis",
    hints=[
        "dp[i] is the longest increasing subsequence that ends at i. It is 1 + the best dp[j] for j < i and nums[j] < nums[i].",
        "That is O(n^2).",
        "Patience sorting keeps the smallest possible tail of every length. The tails array is increasing, so a new value binary-searches its place. The length of tails is the answer.",
    ],
    approaches=[
        ("O(n^2) DP", "O(n^2)", "O(n)", "Every pair of indices."),
        ("Patience sorting", "O(n log n)", "O(n)", "Binary search the tails."),
    ],
    editorial=(
        "tails[k] is the smallest tail of any increasing subsequence of length k + 1 found so far. "
        "For each value, replace the first tail that is greater than or equal to it. If it is larger than every tail, append it. "
        "The array length is the LIS length. The array is not always the LIS itself."
    ),
    companies=["Amazon", "Google", "Microsoft", "Bloomberg"],
)
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for value in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < value:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(value)
        else:
            tails[lo] = value
    return len(tails)


def _oracle_length_of_lis(nums: list[int]) -> int:
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


cases(
    "longest-increasing-subsequence",
    _oracle_length_of_lis,
    [
        ("classic", {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, True, "One LIS is 2, 3, 7, 18."),
        ("decreasing", {"nums": [7, 7, 7, 7]}, True, "Strict increase has length 1."),
        ("sorted", {"nums": [1, 2, 3]}, False, None),
        ("one", {"nums": [4]}, False, None),
        ("mixed", {"nums": [0, 1, 0, 3, 2, 3]}, False, None),
    ],
)


@define(
    slug="longest-common-subsequence",
    title="Longest Common Subsequence",
    difficulty="medium",
    topics=["dynamic-programming", "strings"],
    statement="Return the length of the longest subsequence common to strings `text1` and `text2`.",
    constraints=["1 <= text1.length, text2.length <= 1000", "Both strings are lowercase"],
    signature="def longest_common_subsequence(text1: str, text2: str) -> int:",
    function_name="longest_common_subsequence",
    hints=[
        "If the last characters match, they belong to some optimal subsequence. Take them and add one.",
        "If they differ, discard one of them. The answer is the better of the two choices.",
        "A rolling row stores only the previous string index.",
    ],
    approaches=[
        ("Recursion", "exponential", "O(n + m)", "Recomputes pairs of suffixes."),
        ("2D DP", "O(n * m)", "O(n * m)", "dp[i][j] is the LCS of the prefixes of those lengths."),
    ],
    editorial=(
        "dp[i][j] = dp[i - 1][j - 1] + 1 when the characters match, otherwise the max of dropping a character from either string. "
        "The empty prefix has LCS 0. "
        "The bottom-right cell is the answer. Reconstructing the string walks backward through the same decisions."
    ),
    companies=["Amazon", "Google", "Microsoft", "Bloomberg"],
)
def longest_common_subsequence(text1: str, text2: str) -> int:
    prev = [0] * (len(text2) + 1)
    for a in text1:
        cur = [0]
        for j, b in enumerate(text2, 1):
            if a == b:
                cur.append(prev[j - 1] + 1)
            else:
                cur.append(max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def _oracle_longest_common_subsequence(text1: str, text2: str) -> int:
    def lcs(i: int, j: int) -> int:
        if i == len(text1) or j == len(text2):
            return 0
        if text1[i] == text2[j]:
            return 1 + lcs(i + 1, j + 1)
        return max(lcs(i + 1, j), lcs(i, j + 1))

    return lcs(0, 0)


cases(
    "longest-common-subsequence",
    _oracle_longest_common_subsequence,
    [
        ("classic", {"text1": "abcde", "text2": "ace"}, True, "ace has length 3."),
        ("none", {"text1": "abc", "text2": "def"}, True, "No shared characters."),
        ("same", {"text1": "abc", "text2": "abc"}, False, None),
        ("repeat", {"text1": "aaaa", "text2": "aa"}, False, None),
        ("interleave", {"text1": "abcba", "text2": "abcbcba"}, False, None),
    ],
)


@define(
    slug="edit-distance",
    title="Edit Distance",
    difficulty="medium",
    topics=["dynamic-programming", "strings"],
    statement="Return the minimum number of insertions, deletions, and substitutions required to convert `word1` into `word2`.",
    constraints=["0 <= word1.length, word2.length <= 500", "Both strings are lowercase"],
    signature="def min_distance(word1: str, word2: str) -> int:",
    function_name="min_distance",
    hints=[
        "dp[i][j] is the distance between the prefixes word1[:i] and word2[:j].",
        "If the last characters match, the distance equals dp[i - 1][j - 1].",
        "Otherwise it is 1 plus the best of delete, insert, or substitute, which are the three neighboring cells.",
    ],
    approaches=[
        ("Recursion", "exponential", "O(n + m)", "Three branches per mismatch."),
        ("Wagner-Fischer DP", "O(n * m)", "O(n * m)", "The standard table. A rolling row reduces space to O(min(n, m))."),
    ],
    editorial=(
        "The first row and column are the distances from a string to the empty string, which are pure insertions or deletions. "
        "Every other cell takes a free match or pays one for the best edit. "
        "The corner cell is the Levenshtein distance."
    ),
    companies=["Google", "Amazon", "Microsoft", "Uber"],
)
def min_distance(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    dp = list(range(m + 1))
    for i, a in enumerate(word1, 1):
        prev_diag = dp[0]
        dp[0] = i
        for j, b in enumerate(word2, 1):
            saved = dp[j]
            if a == b:
                dp[j] = prev_diag
            else:
                dp[j] = 1 + min(dp[j], dp[j - 1], prev_diag)
            prev_diag = saved
    return dp[-1]


def _oracle_min_distance(word1: str, word2: str) -> int:
    def dist(i: int, j: int) -> int:
        if i == len(word1):
            return len(word2) - j
        if j == len(word2):
            return len(word1) - i
        if word1[i] == word2[j]:
            return dist(i + 1, j + 1)
        return 1 + min(dist(i + 1, j), dist(i, j + 1), dist(i + 1, j + 1))

    return dist(0, 0)


cases(
    "edit-distance",
    _oracle_min_distance,
    [
        ("horse", {"word1": "horse", "word2": "ros"}, True, "horse to ros takes 3 edits."),
        ("intention", {"word1": "intention", "word2": "execution"}, True, "The distance is 5."),
        ("empty", {"word1": "", "word2": "a"}, False, None),
        ("same", {"word1": "abc", "word2": "abc"}, False, None),
        ("one", {"word1": "a", "word2": "b"}, False, None),
    ],
)


@define(
    slug="unique-paths",
    title="Unique Paths",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="A robot starts at the top-left of an `m` by `n` grid and can move only right or down. Return the number of ways to reach the bottom-right.",
    constraints=["1 <= m, n <= 100"],
    signature="def unique_paths(m: int, n: int) -> int:",
    function_name="unique_paths",
    hints=[
        "To enter a cell you came from the left or from above.",
        "dp[r][c] = dp[r - 1][c] + dp[r][c - 1], with the first row and column equal to 1.",
        "The closed form is the binomial coefficient C((m - 1) + (n - 1), m - 1).",
    ],
    approaches=[
        ("Recursion", "exponential", "O(m + n)", "Overlapping paths."),
        ("DP or binomial", "O(m * n) or O(m + n)", "O(min(m, n))", "The grid DP, or a multiplicative binomial."),
    ],
    editorial=(
        "Every path has exactly m - 1 downs and n - 1 rights, in some order. The count is the binomial coefficient. "
        "The DP writes the same number cell by cell and is the version to code when the grid later gains obstacles. "
        "One row is enough: each cell adds the cell to its left, which is already updated, and the cell above, which is the old value."
    ),
    companies=["Amazon", "Google", "Microsoft", "Bloomberg"],
)
def unique_paths(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]


def _oracle_unique_paths(m: int, n: int) -> int:
    def paths(r: int, c: int) -> int:
        if r == m - 1 or c == n - 1:
            return 1
        return paths(r + 1, c) + paths(r, c + 1)

    return paths(0, 0)


cases(
    "unique-paths",
    _oracle_unique_paths,
    [
        ("classic", {"m": 3, "n": 7}, True, "28 paths."),
        ("square", {"m": 3, "n": 2}, True, "3 paths."),
        ("row", {"m": 1, "n": 5}, False, None),
        ("one", {"m": 1, "n": 1}, False, None),
        ("small", {"m": 2, "n": 2}, False, None),
    ],
)


@define(
    slug="unique-paths-ii",
    title="Unique Paths II",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="The same right-and-down robot now faces a grid where 1 is an obstacle and 0 is empty. Return the number of ways from the top-left to the bottom-right. A path cannot enter an obstacle.",
    constraints=["1 <= m, n <= 100", "grid[i][j] is 0 or 1"],
    signature="from typing import List\n\ndef unique_paths_with_obstacles(obstacle_grid: List[List[int]]) -> int:",
    function_name="unique_paths_with_obstacles",
    hints=[
        "An obstacle cell has 0 ways.",
        "Any other cell is the sum of the ways to enter from the left and from above, ignoring missing neighbors.",
        "If the start cell is blocked, the answer is 0.",
    ],
    approaches=[
        ("DFS with memo", "O(mn)", "O(mn)", "State is the cell."),
        ("In-place or row DP", "O(mn)", "O(n)", "Sweep left to right, top to bottom."),
    ],
    editorial=(
        "Initialize the first cell to 1 if it is open. "
        "A cell in the first row can only be reached from the left, and a cell in the first column only from above, until an obstacle zeroes the rest of that line. "
        "Every later open cell adds the two predecessors."
    ),
    companies=["Amazon", "Google", "Bloomberg", "Microsoft"],
)
def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if obstacle_grid[0][0] == 1:
        return 0
    rows, cols = len(obstacle_grid), len(obstacle_grid[0])
    dp = [0] * cols
    dp[0] = 1
    for r in range(rows):
        for c in range(cols):
            if obstacle_grid[r][c] == 1:
                dp[c] = 0
            elif c:
                dp[c] += dp[c - 1]
    return dp[-1]


def _oracle_unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    rows, cols = len(obstacle_grid), len(obstacle_grid[0])

    def ways(r: int, c: int) -> int:
        if r == rows or c == cols or obstacle_grid[r][c] == 1:
            return 0
        if r == rows - 1 and c == cols - 1:
            return 1
        return ways(r + 1, c) + ways(r, c + 1)

    return ways(0, 0)


cases(
    "unique-paths-ii",
    _oracle_unique_paths_with_obstacles,
    [
        ("classic", {"obstacle_grid": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]}, True, "Two paths avoid the center obstacle."),
        ("blocked-start", {"obstacle_grid": [[1, 0]]}, True, "The start is blocked."),
        ("one", {"obstacle_grid": [[0]]}, False, None),
        ("end", {"obstacle_grid": [[0, 1], [0, 0]]}, False, None),
        ("full", {"obstacle_grid": [[0, 0], [0, 0]]}, False, None),
    ],
)


@define(
    slug="minimum-path-sum",
    title="Minimum Path Sum",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Given a grid of non-negative integers, return the minimum sum of a path from the top-left to the bottom-right moving only right or down.",
    constraints=["1 <= m, n <= 200", "0 <= grid[i][j] <= 200"],
    signature="from typing import List\n\ndef min_path_sum(grid: List[List[int]]) -> int:",
    function_name="min_path_sum",
    hints=[
        "The cheapest way into a cell is the cell's value plus the cheaper of the cell above and the cell to the left.",
        "The first row is a prefix of right moves. The first column is a prefix of down moves.",
        "You can overwrite the grid if the caller does not need it. These tests compare the returned number.",
    ],
    approaches=[
        ("Recursion", "exponential", "O(m + n)", "Two choices per cell."),
        ("DP", "O(mn)", "O(1) extra if the grid is overwritten", "One sweep."),
    ],
    editorial=(
        "Let dp[r][c] = grid[r][c] + min(from above, from left), with missing neighbors treated as infinity except at the origin. "
        "Non-negative numbers are not required for correctness of this recurrence, but they match the problem statement. "
        "The bottom-right cell is the answer."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def min_path_sum(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    for c in range(1, cols):
        grid[0][c] += grid[0][c - 1]
    for r in range(1, rows):
        grid[r][0] += grid[r - 1][0]
        for c in range(1, cols):
            grid[r][c] += min(grid[r - 1][c], grid[r][c - 1])
    return grid[-1][-1]


def _oracle_min_path_sum(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def best(r: int, c: int) -> int:
        if r == rows - 1 and c == cols - 1:
            return grid[r][c]
        choices = []
        if r + 1 < rows:
            choices.append(best(r + 1, c))
        if c + 1 < cols:
            choices.append(best(r, c + 1))
        return grid[r][c] + min(choices)

    return best(0, 0)


cases(
    "minimum-path-sum",
    _oracle_min_path_sum,
    [
        ("classic", {"grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]]}, True, "The path 1-3-1-1-1 sums to 7."),
        ("row", {"grid": [[1, 2, 3]]}, True, "The only path sums to 6."),
        ("one", {"grid": [[5]]}, False, None),
        ("square", {"grid": [[1, 2], [1, 1]]}, False, None),
        ("zeros", {"grid": [[0, 0], [0, 0]]}, False, None),
    ],
)


@define(
    slug="decode-ways",
    title="Decode Ways",
    difficulty="medium",
    topics=["dynamic-programming", "strings"],
    statement=(
        "A message of digits encodes A as 1 through Z as 26. "
        "Return how many ways `s` can be decoded. A leading zero makes a code invalid."
    ),
    constraints=["1 <= s.length <= 100", "s consists of digits"],
    signature="def num_decodings(s: str) -> int:",
    function_name="num_decodings",
    hints=[
        "A single digit from 1 to 9 is a letter. 0 is not.",
        "A two-digit window from 10 to 26 is also a letter.",
        "dp[i] adds dp[i - 1] when the last digit is valid and dp[i - 2] when the last two digits are valid.",
    ],
    approaches=[
        ("Recursion on the index", "exponential", "O(n)", "Two choices when both windows are legal."),
        ("Linear DP", "O(n)", "O(1)", "Rolling two values."),
    ],
    editorial=(
        "This is climbing stairs with validity filters. "
        "A zero can only survive as the second digit of 10 or 20. "
        "If a position can be reached by neither a one-digit nor a two-digit code, the whole string has zero decodings."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def num_decodings(s: str) -> int:
    if s[0] == "0":
        return 0
    prev2, prev1 = 1, 1
    for i in range(1, len(s)):
        current = 0
        if s[i] != "0":
            current += prev1
        if 10 <= int(s[i - 1 : i + 1]) <= 26:
            current += prev2
        prev2, prev1 = prev1, current
    return prev1


def _oracle_num_decodings(s: str) -> int:
    def ways(i: int) -> int:
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = ways(i + 1)
        if i + 1 < len(s) and int(s[i : i + 2]) <= 26:
            total += ways(i + 2)
        return total

    return ways(0)


cases(
    "decode-ways",
    _oracle_num_decodings,
    [
        ("twelve", {"s": "12"}, True, "AB or L."),
        ("two-two-six", {"s": "226"}, True, "Three decodings."),
        ("zero", {"s": "0"}, False, None),
        ("ten", {"s": "10"}, False, None),
        ("invalid-middle", {"s": "2101"}, False, None),
    ],
)


@define(
    slug="partition-equal-subset-sum",
    title="Partition Equal Subset Sum",
    difficulty="medium",
    topics=["dynamic-programming", "knapsack"],
    statement="Return true when `nums` can be partitioned into two subsets with equal sums.",
    constraints=["1 <= nums.length <= 200", "1 <= nums[i] <= 100"],
    signature="from typing import List\n\ndef can_partition(nums: List[int]) -> bool:",
    function_name="can_partition",
    hints=[
        "The total must be even. Each subset then needs sum / 2.",
        "This is a 0/1 knapsack: can a subset sum to target?",
        "A boolean set of reachable sums, updated from a snapshot or by iterating downward, prevents using an element twice.",
    ],
    approaches=[
        ("Bitset or recursion", "O(n * sum)", "O(sum)", "The subset-sum decision problem."),
        ("Backward boolean DP", "O(n * sum)", "O(sum)", "Iterate the target downward so each number is used once."),
    ],
    editorial=(
        "If the total is odd, return false. "
        "Otherwise mark reachable sums, starting from 0. For each number, walk the target from high to low and set dp[s] when dp[s - number] is true. "
        "Walking downward is the 0/1 constraint. The answer is dp[total / 2]."
    ),
    companies=["Amazon", "Facebook", "Google", "Microsoft"],
)
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    reachable = {0}
    for value in nums:
        reachable |= {seen + value for seen in reachable if seen + value <= target}
    return target in reachable


def _oracle_can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2

    def search(i: int, remain: int) -> bool:
        if remain == 0:
            return True
        if i == len(nums) or remain < 0:
            return False
        return search(i + 1, remain - nums[i]) or search(i + 1, remain)

    return search(0, target)


cases(
    "partition-equal-subset-sum",
    _oracle_can_partition,
    [
        ("yes", {"nums": [1, 5, 11, 5]}, True, "11+1 and 5+5."),
        ("no", {"nums": [1, 2, 3, 5]}, True, "The total is odd."),
        ("two", {"nums": [1, 1]}, False, None),
        ("one", {"nums": [2]}, False, None),
        ("more", {"nums": [1, 2, 3, 4, 5, 6, 7]}, False, None),
    ],
)


@define(
    slug="target-sum",
    title="Target Sum",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement="Place '+' or '-' before each integer in `nums` so the expression equals `target`. Return the number of ways.",
    constraints=["1 <= nums.length <= 20", "0 <= nums[i] <= 1000", "-1000 <= target <= 1000"],
    signature="from typing import List\n\ndef find_target_sum_ways(nums: List[int], target: int) -> int:",
    function_name="find_target_sum_ways",
    hints=[
        "With n <= 20, assigning every sign is 2^n and is acceptable.",
        "Let P be the positive subset and N the negative subset. P + N = total and P - N = target, so P = (total + target) / 2.",
        "The problem becomes counting subsets that sum to that P, which is a knapsack count.",
    ],
    approaches=[
        ("Enumerate signs", "O(2^n)", "O(n)", "Fine at n = 20."),
        ("Subset-sum count", "O(n * sum)", "O(sum)", "The transformed target must be nonnegative and even relative to the total."),
    ],
    editorial=(
        "The sign transformation is the insight. If total + target is odd or negative or larger than twice the total, there are zero ways. "
        "Otherwise count subsets summing to (total + target) / 2 with the combination knapsack: dp[s] += dp[s - value], iterating amounts upward only after copying or by using a fresh array per item. "
        "The enumeration oracle checks the DP."
    ),
    companies=["Amazon", "Google", "Facebook", "Adobe"],
)
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    if total < abs(target) or (total + target) % 2:
        return 0
    goal = (total + target) // 2
    dp = [0] * (goal + 1)
    dp[0] = 1
    for value in nums:
        for s in range(goal, value - 1, -1):
            dp[s] += dp[s - value]
    return dp[goal]


def _oracle_find_target_sum_ways(nums: list[int], target: int) -> int:
    def ways(i: int, total: int) -> int:
        if i == len(nums):
            return int(total == target)
        return ways(i + 1, total + nums[i]) + ways(i + 1, total - nums[i])

    return ways(0, 0)


cases(
    "target-sum",
    _oracle_find_target_sum_ways,
    [
        ("classic", {"nums": [1, 1, 1, 1, 1], "target": 3}, True, "Five ways."),
        ("zero", {"nums": [1], "target": 1}, True, "Only the plus sign."),
        ("none", {"nums": [1, 2], "target": 4}, False, None),
        ("zeros", {"nums": [0, 0, 0], "target": 0}, False, None),
        ("mixed", {"nums": [1, 2, 3], "target": 0}, False, None),
    ],
)


@define(
    slug="perfect-squares",
    title="Perfect Squares",
    difficulty="medium",
    topics=["dynamic-programming", "math"],
    statement="Return the least number of perfect-square numbers that sum to `n`.",
    constraints=["1 <= n <= 10^4"],
    signature="def num_squares(n: int) -> int:",
    function_name="num_squares",
    hints=[
        "This is coin change where the coins are 1, 4, 9, ... up to n.",
        "BFS from 0, adding a square at each edge, finds the minimum count.",
        "Lagrange's four-square theorem says the answer is at most 4, which is a useful bound but not required to code the DP.",
    ],
    approaches=[
        ("DP coin change", "O(n * sqrt(n))", "O(n)", "dp[x] = 1 + min(dp[x - square])."),
        ("BFS", "O(n * sqrt(n))", "O(n)", "The depth is the answer."),
    ],
    editorial=(
        "Generate the squares once. Then run the fewest-coins recurrence. "
        "dp[0] = 0. Every larger value tries subtracting each square that fits and keeps the minimum. "
        "The answer is never zero for a positive n."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def num_squares(n: int) -> int:
    squares = [k * k for k in range(1, int(n**0.5) + 1)]
    dp = [0] + [n] * n
    for value in range(1, n + 1):
        for square in squares:
            if square > value:
                break
            dp[value] = min(dp[value], dp[value - square] + 1)
    return dp[n]


def _oracle_num_squares(n: int) -> int:
    from collections import deque

    squares = [k * k for k in range(1, int(n**0.5) + 1)]
    queue = deque([(n, 0)])
    seen = {n}
    while queue:
        remain, count = queue.popleft()
        if remain == 0:
            return count
        for square in squares:
            nxt = remain - square
            if nxt >= 0 and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, count + 1))
    return n


cases(
    "perfect-squares",
    _oracle_num_squares,
    [
        ("twelve", {"n": 12}, True, "4 + 4 + 4 uses three squares."),
        ("thirteen", {"n": 13}, True, "4 + 9 uses two squares."),
        ("one", {"n": 1}, False, None),
        ("three", {"n": 3}, False, None),
        ("seven", {"n": 7}, False, None),
    ],
)


@define(
    slug="jump-game-ii",
    title="Jump Game II",
    difficulty="medium",
    topics=["greedy", "dynamic-programming"],
    statement="You start at index 0. `nums[i]` is the maximum jump length from i. Return the minimum number of jumps to reach the last index. A solution always exists.",
    constraints=["1 <= nums.length <= 10^4", "0 <= nums[i] <= 1000"],
    signature="from typing import List\n\ndef jump(nums: List[int]) -> int:",
    function_name="jump",
    hints=[
        "BFS layers on the index line: from the current jump's range, the next range is the farthest you can reach.",
        "You do not need the actual indices, only the end of the current jump window and the farthest index seen inside it.",
        "When the scan index hits the end of the window, you must jump, so increment the count and extend the window to the farthest index.",
    ],
    approaches=[
        ("DP", "O(n^2)", "O(n)", "dp[i] is the minimum jumps to reach i."),
        ("Greedy window", "O(n)", "O(1)", "Implicit BFS layers."),
    ],
    editorial=(
        "The linear scan is BFS on a line. "
        "current_end is the farthest index reachable with the jumps already committed. farthest is the farthest index reachable with one more jump. "
        "When i equals current_end and i is not the last index, commit one jump and set current_end to farthest."
    ),
    companies=["Amazon", "Google", "Microsoft", "Apple"],
)
def jump(nums: list[int]) -> int:
    jumps = current_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps


def _oracle_jump(nums: list[int]) -> int:
    n = len(nums)
    dp = [10**9] * n
    dp[0] = 0
    for i in range(n):
        for step in range(1, nums[i] + 1):
            if i + step < n:
                dp[i + step] = min(dp[i + step], dp[i] + 1)
    return dp[-1]


cases(
    "jump-game-ii",
    _oracle_jump,
    [
        ("classic", {"nums": [2, 3, 1, 1, 4]}, True, "Two jumps: index 0 to 1, then to the end."),
        ("one", {"nums": [2, 1]}, True, "One jump."),
        ("single", {"nums": [0]}, False, None),
        ("long", {"nums": [1, 1, 1, 1]}, False, None),
        ("skip", {"nums": [3, 1, 1, 1]}, False, None),
    ],
)


@define(
    slug="longest-palindromic-subsequence",
    title="Longest Palindromic Subsequence",
    difficulty="medium",
    topics=["dynamic-programming", "strings"],
    statement="Return the length of the longest palindromic subsequence of `s`.",
    constraints=["1 <= s.length <= 1000", "s is lowercase"],
    signature="def longest_palindrome_subseq(s: str) -> int:",
    function_name="longest_palindrome_subseq",
    hints=[
        "A subsequence does not have to be contiguous. This is not the longest palindromic substring.",
        "If the ends match, add 2 to the answer for the inside.",
        "If they differ, drop one end. The answer is the LCS of s and its reverse.",
    ],
    approaches=[
        ("Interval DP", "O(n^2)", "O(n^2)", "dp[i][j] is the answer on s[i:j+1]."),
        ("LCS with the reverse", "O(n^2)", "O(n^2)", "A palindromic subsequence is a common subsequence of s and reverse(s)."),
    ],
    editorial=(
        "The LCS formulation is the shortest proof. Any palindromic subsequence reads the same forward and backward, so it is common to s and reverse(s), and the longest such common subsequence can be realized as a palindrome. "
        "The interval DP writes the same recurrence without building the reverse explicitly."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def longest_palindrome_subseq(s: str) -> int:
    return longest_common_subsequence(s, s[::-1])


def _oracle_longest_palindrome_subseq(s: str) -> int:
    n = len(s)

    def best(i: int, j: int) -> int:
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return 2 + best(i + 1, j - 1)
        return max(best(i + 1, j), best(i, j - 1))

    return best(0, n - 1)


cases(
    "longest-palindromic-subsequence",
    _oracle_longest_palindrome_subseq,
    [
        ("bbbab", {"s": "bbbab"}, True, "bbbb has length 4."),
        ("cbbd", {"s": "cbbd"}, True, "bb has length 2."),
        ("single", {"s": "a"}, False, None),
        ("even", {"s": "abba"}, False, None),
        ("odd", {"s": "abcba"}, False, None),
    ],
)


@define(
    slug="integer-break",
    title="Integer Break",
    difficulty="medium",
    topics=["dynamic-programming", "math"],
    statement="Break the integer `n` into at least two positive integers that sum to n. Return the maximum product of those integers. Order does not matter.",
    constraints=["2 <= n <= 58"],
    signature="def integer_break(n: int) -> int:",
    function_name="integer_break",
    hints=[
        "dp[x] is the maximum product of a break of x. It may also be useful to keep x unbroken when it is a part of a larger number.",
        "For a part, the best contribution is max(k, dp[k]), except the original n must be broken at least once.",
        "The math shortcut is to break into as many 3s as possible, and avoid a remainder of 1 by using a 4 = 2 + 2 instead of 3 + 1.",
    ],
    approaches=[
        ("DP over parts", "O(n^2)", "O(n)", "Try every first part."),
        ("Break into threes", "O(n)", "O(1)", "The optimal part size is 3, with the remainder-1 exception."),
    ],
    editorial=(
        "For the DP, dp[i] = max over k < i of k * max(i - k, dp[i - k]). The max with the unbroken remainder is what lets a part stay whole. "
        "The closed form prefers 3s because 3 gives a better product per unit than 2 or 4, while 1 is never a useful part. "
        "4 is the exception: 2 * 2 beats 3 * 1."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def integer_break(n: int) -> int:
    if n == 2:
        return 1
    if n == 3:
        return 2
    product = 1
    while n > 4:
        product *= 3
        n -= 3
    return product * n


def _oracle_integer_break(n: int) -> int:
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        for k in range(1, i):
            dp[i] = max(dp[i], k * max(i - k, dp[i - k]))
    return dp[n]


cases(
    "integer-break",
    _oracle_integer_break,
    [
        ("two", {"n": 2}, True, "1 + 1, product 1."),
        ("ten", {"n": 10}, True, "3 + 3 + 4 = 36."),
        ("three", {"n": 3}, False, None),
        ("four", {"n": 4}, False, None),
        ("eight", {"n": 8}, False, None),
    ],
)


@define(
    slug="best-time-to-buy-and-sell-stock-ii",
    title="Best Time to Buy and Sell Stock II",
    difficulty="medium",
    topics=["dynamic-programming", "greedy"],
    statement="You may complete as many buy-sell transactions as you like. You may not hold more than one share. Return the maximum profit. Prices are given by day.",
    constraints=["1 <= prices.length <= 3 * 10^4", "0 <= prices[i] <= 10^4"],
    signature="from typing import List\n\ndef max_profit_unlimited(prices: List[int]) -> int:",
    function_name="max_profit_unlimited",
    hints=[
        "Every upward difference can be captured by selling and buying again.",
        "Add prices[i] - prices[i - 1] whenever it is positive.",
        "A state machine with hold and cash also works and generalizes to the cooldown and fee variants.",
    ],
    approaches=[
        ("Peak and valley", "O(n)", "O(1)", "Sum every increasing segment."),
        ("State machine", "O(n)", "O(1)", "cash and hold, updated each day."),
    ],
    editorial=(
        "Because you can transact every day, the optimal policy takes every positive consecutive difference and ignores the negative ones. "
        "A multi-day rise from a to c equals (b - a) + (c - b). "
        "Summing the pieces is the same profit as one trade across the rise."
    ),
    companies=["Amazon", "Bloomberg", "Google", "Microsoft"],
)
def max_profit_unlimited(prices: list[int]) -> int:
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))


def _oracle_max_profit_unlimited(prices: list[int]) -> int:
    cash = 0
    hold = float("-inf")
    for price in prices:
        cash, hold = max(cash, hold + price), max(hold, cash - price)
    return cash


cases(
    "best-time-to-buy-and-sell-stock-ii",
    _oracle_max_profit_unlimited,
    [
        ("classic", {"prices": [7, 1, 5, 3, 6, 4]}, True, "Buy at 1 sell at 5, buy at 3 sell at 6. Profit 7."),
        ("rise", {"prices": [1, 2, 3, 4, 5]}, True, "The whole rise is profit 4."),
        ("fall", {"prices": [7, 6, 4, 3, 1]}, False, None),
        ("flat", {"prices": [3, 3, 3]}, False, None),
        ("one", {"prices": [4]}, False, None),
    ],
)


@define(
    slug="best-time-to-buy-and-sell-stock-with-cooldown",
    title="Best Time to Buy and Sell Stock with Cooldown",
    difficulty="medium",
    topics=["dynamic-programming", "state-machine"],
    statement=(
        "You may buy and sell as often as you like, but after you sell you must cooldown for one day before buying again. "
        "You hold at most one share. Return the maximum profit."
    ),
    constraints=["1 <= prices.length <= 5000", "0 <= prices[i] <= 1000"],
    signature="from typing import List\n\ndef max_profit_cooldown(prices: List[int]) -> int:",
    function_name="max_profit_cooldown",
    hints=[
        "Three states are enough: holding a share, cooling down after a sale, and free to buy.",
        "Holding today comes from holding yesterday or buying from the free state.",
        "Free today comes from free yesterday or from yesterday's cooldown. Cooldown today is yesterday's holding plus today's price.",
    ],
    approaches=[
        ("Memoized recursion on (day, holding)", "O(n)", "O(n)", "The cooldown is a skipped day after a sell."),
        ("Three rolling states", "O(n)", "O(1)", "The state machine above."),
    ],
    editorial=(
        "Let hold be the best profit while owning a share, sold be the profit of selling today, and rest be the best profit while allowed to buy. "
        "Transitions: new_hold = max(hold, rest - price), new_sold = hold + price, new_rest = max(rest, sold). "
        "The answer is the better of rest and sold, because you should not finish still holding a share you could have sold."
    ),
    companies=["Google", "Amazon", "Facebook", "Microsoft"],
)
def max_profit_cooldown(prices: list[int]) -> int:
    hold = float("-inf")
    sold = 0
    rest = 0
    for price in prices:
        prev_sold = sold
        sold = hold + price
        hold = max(hold, rest - price)
        rest = max(rest, prev_sold)
    return max(rest, sold)


def _oracle_max_profit_cooldown(prices: list[int]) -> int:
    n = len(prices)
    memo: dict[tuple[int, bool], int] = {}

    def best(day: int, holding: bool) -> int:
        if day >= n:
            return 0
        key = (day, holding)
        if key in memo:
            return memo[key]
        skip = best(day + 1, holding)
        if holding:
            take = prices[day] + best(day + 2, False)
        else:
            take = -prices[day] + best(day + 1, True)
        memo[key] = max(skip, take)
        return memo[key]

    return best(0, False)


cases(
    "best-time-to-buy-and-sell-stock-with-cooldown",
    _oracle_max_profit_cooldown,
    [
        ("classic", {"prices": [1, 2, 3, 0, 2]}, True, "Buy at 1, sell at 3, cooldown, buy at 0, sell at 2. Profit 3."),
        ("flat", {"prices": [1]}, True, "No transaction."),
        ("two", {"prices": [1, 2]}, False, None),
        ("dip", {"prices": [2, 1, 4]}, False, None),
        ("long", {"prices": [6, 1, 3, 2, 4, 7]}, False, None),
    ],
)


@define(
    slug="delete-and-earn",
    title="Delete and Earn",
    difficulty="medium",
    topics=["dynamic-programming"],
    statement=(
        "Choosing `nums[i]` earns nums[i] points and deletes every occurrence of nums[i] - 1 and nums[i] + 1. "
        "You may continue until the array is empty. Return the maximum points."
    ),
    constraints=["1 <= nums.length <= 2 * 10^4", "1 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef delete_and_earn(nums: List[int]) -> int:",
    function_name="delete_and_earn",
    hints=[
        "Equal values do not delete each other. Taking a value earns value times its count.",
        "Taking x forbids x - 1 and x + 1. This is house robber on the number line.",
        "Build an array points[v] = v * count(v), then run the linear robber from 1 to the maximum value.",
    ],
    approaches=[
        ("Recursion on the set", "exponential", "O(n)", "Choose a remaining value."),
        ("House robber on values", "O(n + max value)", "O(max value)", "Aggregate counts first."),
    ],
    editorial=(
        "Collapse duplicates into points on the integer line. "
        "Adjacent integers conflict, non-adjacent integers do not, even if some integers are missing. A missing integer is a house of value 0 and does not change the robber recurrence. "
        "The answer is the house-robber result on that points array."
    ),
    companies=["Google", "Amazon", "Adobe", "Microsoft"],
)
def delete_and_earn(nums: list[int]) -> int:
    points = [0] * (max(nums) + 1)
    for value in nums:
        points[value] += value
    return rob_line(points)


def _oracle_delete_and_earn(nums: list[int]) -> int:
    from collections import Counter

    counts = Counter(nums)
    values = sorted(counts)
    memo: dict[int, int] = {}

    def best(i: int) -> int:
        if i >= len(values):
            return 0
        if i in memo:
            return memo[i]
        take = values[i] * counts[values[i]]
        nxt = i + 1
        if nxt < len(values) and values[nxt] == values[i] + 1:
            nxt += 1
        memo[i] = max(best(i + 1), take + best(nxt))
        return memo[i]

    return best(0)


cases(
    "delete-and-earn",
    _oracle_delete_and_earn,
    [
        ("classic", {"nums": [3, 4, 2]}, True, "Take 3, delete 2 and 4, earn 3. Or take 2 and 4 for 6."),
        ("repeat", {"nums": [2, 2, 3, 3, 3, 4]}, True, "Take the 3s for 9."),
        ("one", {"nums": [5]}, False, None),
        ("same", {"nums": [1, 1, 1]}, False, None),
        ("gap", {"nums": [1, 1, 3, 3]}, False, None),
    ],
)


@define(
    slug="maximal-square",
    title="Maximal Square",
    difficulty="medium",
    topics=["dynamic-programming", "matrix"],
    statement="Given a binary matrix of characters '0' and '1', return the area of the largest square of '1's.",
    constraints=["1 <= m, n <= 300", "matrix[i][j] is '0' or '1'"],
    signature="from typing import List\n\ndef maximal_square(matrix: List[str]) -> int:",
    function_name="maximal_square",
    hints=[
        "Let dp[r][c] be the side length of the largest square whose bottom-right corner is (r, c).",
        "If the cell is '1', the side is 1 plus the minimum of the left, upper, and upper-left sides.",
        "The answer is the square of the largest side.",
    ],
    approaches=[
        ("Enumerate squares", "O(mn * min(m, n)^2)", "O(1)", "Try every top-left and side."),
        ("DP side lengths", "O(mn)", "O(n)", "One row of side lengths."),
    ],
    editorial=(
        "A square of side k ending at (r, c) exists only when the three neighboring squares of side k - 1 exist and the cell itself is 1. "
        "The min of those three neighbors is exactly the largest such k - 1. "
        "Track the maximum side and square it at the end."
    ),
    companies=["Amazon", "Google", "Microsoft", "Facebook"],
)
def maximal_square(matrix: list[str]) -> int:
    rows, cols = len(matrix), len(matrix[0])
    prev = [0] * (cols + 1)
    best = 0
    for r in range(rows):
        cur = [0] * (cols + 1)
        for c in range(cols):
            if matrix[r][c] == "1":
                cur[c + 1] = 1 + min(prev[c + 1], cur[c], prev[c])
                best = max(best, cur[c + 1])
        prev = cur
    return best * best


def _oracle_maximal_square(matrix: list[str]) -> int:
    rows, cols = len(matrix), len(matrix[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            side = 0
            while r + side < rows and c + side < cols:
                if any(matrix[r + side][c + k] == "0" or matrix[r + k][c + side] == "0" for k in range(side + 1)):
                    break
                side += 1
                best = max(best, side)
    return best * best


cases(
    "maximal-square",
    _oracle_maximal_square,
    [
        ("classic", {"matrix": ["10100", "10111", "11111", "10010"]}, True, "The largest square has area 4."),
        ("zero", {"matrix": ["0"]}, True, "No square of ones."),
        ("one", {"matrix": ["1"]}, False, None),
        ("row", {"matrix": ["111"]}, False, None),
        ("full", {"matrix": ["11", "11"]}, False, None),
    ],
)


@define(
    slug="palindromic-substrings",
    title="Palindromic Substrings",
    difficulty="medium",
    topics=["strings", "dynamic-programming"],
    statement="Return the number of palindromic substrings in `s`. Single characters count. Overlapping substrings count separately.",
    constraints=["1 <= s.length <= 1000"],
    signature="def count_substrings(s: str) -> int:",
    function_name="count_substrings",
    hints=[
        "Every palindrome has a center.",
        "Expand around each of the 2n - 1 centers and count every successful expansion.",
        "A DP table dp[i][j] is true when s[i:j+1] is a palindrome, set from the ends and the inside.",
    ],
    approaches=[
        ("Check every substring", "O(n^3)", "O(1)", "Or O(n^2) with care."),
        ("Expand around centers", "O(n^2)", "O(1)", "Each expansion is charged to a substring."),
    ],
    editorial=(
        "There are n odd centers and n - 1 even centers. "
        "From a center, walk outward while the characters match and add one for each radius, including radius 0 for odd centers. "
        "The total is the number of palindromic substrings."
    ),
    companies=["Facebook", "Amazon", "Adobe", "Microsoft"],
)
def count_substrings(s: str) -> int:
    n = len(s)
    count = 0
    for center in range(2 * n - 1):
        left, right = center // 2, center // 2 + center % 2
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    return count


def _oracle_count_substrings(s: str) -> int:
    count = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            piece = s[i : j + 1]
            if piece == piece[::-1]:
                count += 1
    return count


cases(
    "palindromic-substrings",
    _oracle_count_substrings,
    [
        ("abc", {"s": "abc"}, True, "Three single letters."),
        ("aaa", {"s": "aaa"}, True, "Six palindromes."),
        ("one", {"s": "a"}, False, None),
        ("abba", {"s": "abba"}, False, None),
        ("racecar", {"s": "racecar"}, False, None),
    ],
)


@define(
    slug="knapsack",
    title="0/1 Knapsack",
    difficulty="medium",
    topics=["dynamic-programming", "knapsack"],
    statement=(
        "Each item has a weight and a value. Choose each item at most once. "
        "Return the maximum value whose total weight does not exceed `capacity`."
    ),
    constraints=["1 <= n <= 100", "1 <= capacity <= 1000", "1 <= weight, value <= 1000"],
    signature="from typing import List\n\ndef knapsack(weights: List[int], values: List[int], capacity: int) -> int:",
    function_name="knapsack",
    hints=[
        "dp[w] is the best value using the items considered so far with capacity w.",
        "Process one item at a time. For that item, iterate capacities downward so the item is not used twice.",
        "The transition is dp[w] = max(dp[w], dp[w - weight] + value) when w >= weight.",
    ],
    approaches=[
        ("Recursion with memo", "O(n * capacity)", "O(n * capacity)", "State is (item index, remaining capacity)."),
        ("1D backward DP", "O(n * capacity)", "O(capacity)", "The classic rolling array."),
    ],
    editorial=(
        "The 0/1 constraint is the direction of the inner loop. "
        "Updating capacity from high to low reads the previous item's values, which still sit in the lower cells. "
        "Updating low to high would be the unbounded knapsack, where the same item can be chosen again."
    ),
    companies=["Amazon", "Google", "Microsoft", "Goldman Sachs"],
)
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[capacity]


def _oracle_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    def best(i: int, remain: int) -> int:
        if i == len(weights) or remain <= 0:
            return 0
        skip = best(i + 1, remain)
        if weights[i] > remain:
            return skip
        return max(skip, values[i] + best(i + 1, remain - weights[i]))

    return best(0, capacity)


cases(
    "knapsack",
    _oracle_knapsack,
    [
        ("classic", {"weights": [1, 3, 4, 5], "values": [1, 4, 5, 7], "capacity": 7}, True, "Items of weight 3 and 4 give value 9."),
        ("tight", {"weights": [2, 2], "values": [3, 4], "capacity": 3}, True, "Only the heavier value fits once. Weight 2 value 4."),
        ("none", {"weights": [5], "values": [10], "capacity": 4}, False, None),
        ("all", {"weights": [1, 1], "values": [2, 3], "capacity": 2}, False, None),
        ("one", {"weights": [4], "values": [6], "capacity": 4}, False, None),
    ],
)


@define(
    slug="tribonacci",
    title="Tribonacci",
    difficulty="easy",
    topics=["dynamic-programming"],
    statement="The Tribonacci sequence is T(0) = 0, T(1) = 1, T(2) = 1, and T(n) = T(n - 1) + T(n - 2) + T(n - 3) for n >= 3. Return T(n).",
    constraints=["0 <= n <= 37"],
    signature="def tribonacci(n: int) -> int:",
    function_name="tribonacci",
    hints=[
        "The recurrence uses three previous terms.",
        "Base cases are 0, 1, and 1.",
        "Three rolling variables compute the sequence in constant space.",
    ],
    approaches=[
        ("Recursion", "O(3^n)", "O(n)", "Massive overlap."),
        ("Rolling sum", "O(n)", "O(1)", "Shift a window of three terms."),
    ],
    editorial=(
        "This is the same idea as Fibonacci with one extra term. "
        "Keep a, b, and c. The next value is their sum, then slide the window. "
        "Return early for n < 3 so the loop has a legal start."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def tribonacci(n: int) -> int:
    a, b, c = 0, 1, 1
    if n == 0:
        return 0
    if n < 3:
        return 1
    for _ in range(3, n + 1):
        a, b, c = b, c, a + b + c
    return c


def _oracle_tribonacci(n: int) -> int:
    seq = [0, 1, 1]
    for i in range(3, n + 1):
        seq.append(seq[i - 1] + seq[i - 2] + seq[i - 3])
    return seq[n]


cases(
    "tribonacci",
    _oracle_tribonacci,
    [
        ("four", {"n": 4}, True, "T(4) = 4."),
        ("twenty-five", {"n": 25}, True, "A larger term, still exact in integers."),
        ("zero", {"n": 0}, False, None),
        ("two", {"n": 2}, False, None),
        ("ten", {"n": 10}, False, None),
    ],
)
