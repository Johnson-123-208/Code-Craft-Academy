"""Flagship array, string, and interval problems."""

from __future__ import annotations

from collections import Counter, defaultdict, deque

from lib import cases, define

# ---------------------------------------------------------------------------
# Two Sum
# ---------------------------------------------------------------------------


@define(
    slug="two-sum",
    title="Two Sum",
    difficulty="easy",
    topics=["arrays", "hashing"],
    statement=(
        "Given an integer array `nums` and an integer `target`, return the indices of the two numbers "
        "that add up to `target`. Each input has exactly one solution, and you may not use the same element twice. "
        "Return the indices in increasing order."
    ),
    constraints=[
        "2 <= nums.length <= 10^4",
        "-10^9 <= nums[i], target <= 10^9",
        "Exactly one valid pair exists",
    ],
    signature="from typing import List\n\ndef two_sum(nums: List[int], target: int) -> List[int]:",
    function_name="two_sum",
    hints=[
        "A nested pair scan is correct and quadratic. A dictionary turns the complement lookup into expected constant time.",
        "Scan left to right. For the current value x, the partner you need is target minus x.",
        "Store value to index as you go, and only look backward so an element is never paired with itself.",
    ],
    approaches=[
        ("Brute force pairs", "O(n^2)", "O(1)", "Check every pair i < j."),
        ("Hash map one pass", "O(n)", "O(n)", "Map each seen value to its index and probe the complement."),
    ],
    editorial=(
        "The quadratic solution enumerates pairs. The linear solution remembers every value already seen. "
        "When nums[i] arrives, the complement target - nums[i] is either already in the map, in which case the pair is done, "
        "or it is recorded for a later index. Because a solution exists, the function always returns inside the loop."
    ),
    companies=["Google", "Amazon", "Meta", "Adobe"],
)
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], i]
        seen[value] = i
    raise ValueError("no pair")


def _oracle_two_sum(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    raise ValueError("no pair")


cases(
    "two-sum",
    _oracle_two_sum,
    [
        ("example-1", {"nums": [2, 7, 11, 15], "target": 9}, True, "2 + 7 = 9 at indices 0 and 1."),
        ("example-2", {"nums": [3, 2, 4], "target": 6}, True, "2 + 4 = 6 at indices 1 and 2."),
        ("duplicates", {"nums": [3, 3], "target": 6}, False, None),
        ("negatives", {"nums": [-1, -2, -3, -4, -5], "target": -8}, False, None),
        ("later-pair", {"nums": [1, 5, 3, 7, 2, 9], "target": 11}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Contains Duplicate
# ---------------------------------------------------------------------------


@define(
    slug="contains-duplicate",
    title="Contains Duplicate",
    difficulty="easy",
    topics=["arrays", "hashing"],
    statement="Return true when any integer appears at least twice in `nums`, and false when every value is unique.",
    constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
    signature="from typing import List\n\ndef contains_duplicate(nums: List[int]) -> bool:",
    function_name="contains_duplicate",
    hints=[
        "Sorting clusters equal values, so a duplicate is a pair of neighbors.",
        "A set answers membership in expected constant time.",
        "Insert as you scan. The first failed insert is a duplicate.",
    ],
    approaches=[
        ("Sort and scan neighbors", "O(n log n)", "O(1)", "After sorting, equal values sit next to each other."),
        ("Hash set", "O(n)", "O(n)", "Reject a value that is already present."),
    ],
    editorial=(
        "A set stores the values observed so far. If the current value is already in the set, the array contains a duplicate. "
        "Otherwise insert it. The extra memory is linear, and the expected time is linear."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Bloomberg"],
)
def contains_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))


def _oracle_contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()
    for value in nums:
        if value in seen:
            return True
        seen.add(value)
    return False


cases(
    "contains-duplicate",
    _oracle_contains_duplicate,
    [
        ("has-dup", {"nums": [1, 2, 3, 1]}, True, "1 appears twice."),
        ("unique", {"nums": [1, 2, 3, 4]}, True, "All values are distinct."),
        ("single", {"nums": [7]}, False, None),
        ("tail", {"nums": [8, 6, 4, 2, 6]}, False, None),
        ("negatives", {"nums": [-1, -1]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Best Time to Buy and Sell Stock
# ---------------------------------------------------------------------------


@define(
    slug="best-time-to-buy-and-sell-stock",
    title="Best Time to Buy and Sell Stock",
    difficulty="easy",
    topics=["arrays", "sliding-window"],
    statement=(
        "You are given `prices`, where `prices[i]` is the price of a stock on day i. "
        "Choose one day to buy and a later day to sell. Return the maximum profit. If no profit is possible, return 0."
    ),
    constraints=["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
    signature="from typing import List\n\ndef max_profit(prices: List[int]) -> int:",
    function_name="max_profit",
    hints=[
        "Every pair of days is a candidate, but only later days can be sell days.",
        "The best sell on day i is prices[i] minus the cheapest price seen before i.",
        "Track the minimum price so far and the best difference in one left-to-right pass.",
    ],
    approaches=[
        ("All pairs", "O(n^2)", "O(1)", "Try every buy day and every later sell day."),
        ("Running minimum", "O(n)", "O(1)", "Sell against the lowest price observed so far."),
    ],
    editorial=(
        "A profitable sale on day i must buy at the minimum of prices[0..i-1]. "
        "Maintain that minimum while scanning, and keep the largest nonnegative difference. "
        "One pass is enough because every earlier price has already competed for the minimum."
    ),
    companies=["Amazon", "Bloomberg", "Microsoft", "Facebook"],
)
def max_profit(prices: list[int]) -> int:
    best = 0
    low = prices[0]
    for price in prices[1:]:
        best = max(best, price - low)
        low = min(low, price)
    return best


def _oracle_max_profit(prices: list[int]) -> int:
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


cases(
    "best-time-to-buy-and-sell-stock",
    _oracle_max_profit,
    [
        ("rise", {"prices": [7, 1, 5, 3, 6, 4]}, True, "Buy at 1 and sell at 6."),
        ("fall", {"prices": [7, 6, 4, 3, 1]}, True, "Prices only fall, so the profit is 0."),
        ("one-day", {"prices": [4]}, False, None),
        ("flat", {"prices": [3, 3, 3]}, False, None),
        ("late-peak", {"prices": [2, 4, 1, 7]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Product of Array Except Self
# ---------------------------------------------------------------------------


@define(
    slug="product-of-array-except-self",
    title="Product of Array Except Self",
    difficulty="medium",
    topics=["arrays", "prefix-sums"],
    statement=(
        "Return an array `answer` where `answer[i]` is the product of every element of `nums` except `nums[i]`. "
        "Solve it without using division, in O(n) time."
    ),
    constraints=["2 <= nums.length <= 10^5", "-30 <= nums[i] <= 30", "The product fits in a 32-bit signed integer"],
    signature="from typing import List\n\ndef product_except_self(nums: List[int]) -> List[int]:",
    function_name="product_except_self",
    hints=[
        "Division by nums[i] fails when a value is zero and hides the structure of the problem.",
        "answer[i] is the product of the prefix before i times the product of the suffix after i.",
        "Build the prefix products in the output array, then fold the suffix product from the right in a second pass.",
    ],
    approaches=[
        ("Prefix and suffix arrays", "O(n)", "O(n)", "Store products to the left and to the right, then multiply them."),
        ("Output array as prefix", "O(n)", "O(1)", "Reuse the answer buffer, then multiply a running suffix. Output space is not counted."),
    ],
    editorial=(
        "Left-to-right, answer[i] becomes the product of nums[0..i-1]. "
        "Right-to-left, a running suffix product multiplies those prefixes. "
        "Zeros need no special case: a zero in the prefix or suffix naturally zeroes every other slot, and the zero's own slot receives the product of the rest."
    ),
    companies=["Facebook", "Amazon", "Apple", "Microsoft"],
)
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer


def _oracle_product_except_self(nums: list[int]) -> list[int]:
    out = []
    for i in range(len(nums)):
        prod = 1
        for j, value in enumerate(nums):
            if i != j:
                prod *= value
        out.append(prod)
    return out


cases(
    "product-of-array-except-self",
    _oracle_product_except_self,
    [
        ("example", {"nums": [1, 2, 3, 4]}, True, "Products are 24, 12, 8, 6."),
        ("zero", {"nums": [-1, 1, 0, -3, 3]}, True, "Only the zero slot is nonzero."),
        ("two", {"nums": [2, 5]}, False, None),
        ("negatives", {"nums": [-2, -3, 4]}, False, None),
        ("double-zero", {"nums": [0, 4, 0]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Maximum Subarray
# ---------------------------------------------------------------------------


@define(
    slug="maximum-subarray",
    title="Maximum Subarray",
    difficulty="medium",
    topics=["arrays", "kadane", "dynamic-programming"],
    statement="Given an integer array `nums`, return the largest sum of any contiguous subarray. The subarray must contain at least one element.",
    constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef max_sub_array(nums: List[int]) -> int:",
    function_name="max_sub_array",
    hints=[
        "Every pair of endpoints defines a subarray, and prefix sums turn each sum into a subtraction.",
        "A negative running sum will never help a future element. Drop it.",
        "Kadane keeps the best sum ending at i, which is max(nums[i], best_ending_here + nums[i]), and a separate global best.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Extend each start index until the end."),
        ("Kadane", "O(n)", "O(1)", "Dynamic programming on the subarray that ends at the current index."),
    ],
    editorial=(
        "Let dp[i] be the maximum sum of a subarray that ends at i. Then dp[i] = nums[i] + max(dp[i-1], 0). "
        "The answer is the maximum dp[i]. Only the previous value is required, so two scalars replace the table. "
        "Initialize both from nums[0] so an all-negative array returns the largest element instead of zero."
    ),
    companies=["Google", "Amazon", "Microsoft", "LinkedIn"],
)
def max_sub_array(nums: list[int]) -> int:
    best = running = nums[0]
    for value in nums[1:]:
        running = max(value, running + value)
        best = max(best, running)
    return best


def _oracle_max_sub_array(nums: list[int]) -> int:
    best = nums[0]
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, total)
    return best


cases(
    "maximum-subarray",
    _oracle_max_sub_array,
    [
        ("classic", {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, True, "The subarray [4, -1, 2, 1] sums to 6."),
        ("single", {"nums": [1]}, True, "One element."),
        ("all-negative", {"nums": [-3, -2, -5]}, False, None),
        ("mixed", {"nums": [5, -2, 3]}, False, None),
        ("restart", {"nums": [1, -4, 3, -1, 2]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Maximum Product Subarray
# ---------------------------------------------------------------------------


@define(
    slug="maximum-product-subarray",
    title="Maximum Product Subarray",
    difficulty="medium",
    topics=["arrays", "dynamic-programming"],
    statement="Return the largest product of any contiguous subarray of `nums`. The subarray must be non-empty.",
    constraints=["1 <= nums.length <= 2 * 10^4", "-10 <= nums[i] <= 10"],
    signature="from typing import List\n\ndef max_product(nums: List[int]) -> int:",
    function_name="max_product",
    hints=[
        "A negative number flips the winner: the smallest product so far can become the largest after one more negative.",
        "Zero breaks every product that crosses it. Starting fresh at the next element handles that.",
        "Track both the maximum and the minimum product ending at the current index.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Multiply every range."),
        ("Two running products", "O(n)", "O(1)", "Keep min and max products ending here."),
    ],
    editorial=(
        "Unlike Kadane for sums, a very negative running product is useful because another negative will flip its sign. "
        "At each index the candidates are the value itself, that value times the previous max, and that value times the previous min. "
        "The global answer is the largest max observed."
    ),
    companies=["Amazon", "Google", "LinkedIn", "Microsoft"],
)
def max_product(nums: list[int]) -> int:
    best = low = high = nums[0]
    for value in nums[1:]:
        candidates = (value, high * value, low * value)
        high = max(candidates)
        low = min(candidates)
        best = max(best, high)
    return best


def _oracle_max_product(nums: list[int]) -> int:
    best = nums[0]
    for i in range(len(nums)):
        prod = 1
        for j in range(i, len(nums)):
            prod *= nums[j]
            best = max(best, prod)
    return best


cases(
    "maximum-product-subarray",
    _oracle_max_product,
    [
        ("classic", {"nums": [2, 3, -2, 4]}, True, "The subarray [2, 3] has product 6."),
        ("negatives", {"nums": [-2, 0, -1]}, True, "The best product is 0."),
        ("two-negatives", {"nums": [-2, 3, -4]}, False, None),
        ("single-negative", {"nums": [-5]}, False, None),
        ("with-zero", {"nums": [-2, 4, 0, 3, -1]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Two Sum II
# ---------------------------------------------------------------------------


@define(
    slug="two-sum-ii",
    title="Two Sum II - Input Array Is Sorted",
    difficulty="easy",
    topics=["arrays", "two-pointers"],
    statement=(
        "`numbers` is sorted in nondecreasing order. Find two different indices whose values sum to `target`. "
        "Return those indices as 1-based positions `[index1, index2]` with index1 < index2. Exactly one solution exists."
    ),
    constraints=["2 <= numbers.length <= 3 * 10^4", "-1000 <= numbers[i], target <= 1000"],
    signature="from typing import List\n\ndef two_sum_sorted(numbers: List[int], target: int) -> List[int]:",
    function_name="two_sum_sorted",
    hints=[
        "Because the array is sorted, moving the right pointer left decreases the sum and moving the left pointer right increases it.",
        "Start with the first and last positions.",
        "Return 1-based indices, not 0-based positions.",
    ],
    approaches=[
        ("Binary search each complement", "O(n log n)", "O(1)", "For each left value, binary-search the partner to its right."),
        ("Opposite pointers", "O(n)", "O(1)", "Shrink the interval from both ends."),
    ],
    editorial=(
        "Place one pointer at each end. If the sum is too small, the left value is too small, so advance the left pointer. "
        "If the sum is too large, retreat the right pointer. The sorted order makes each decision safe, and each pointer moves at most n times."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    raise ValueError("no pair")


def _oracle_two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
    raise ValueError("no pair")


cases(
    "two-sum-ii",
    _oracle_two_sum_sorted,
    [
        ("example", {"numbers": [2, 7, 11, 15], "target": 9}, True, "1-based indices of 2 and 7."),
        ("inner", {"numbers": [2, 3, 4], "target": 6}, True, "3 + 3 is not available; 2 + 4 works."),
        ("negatives", {"numbers": [-5, -2, 0, 3, 8], "target": 1}, False, None),
        ("ends", {"numbers": [1, 2, 3, 4, 5], "target": 6}, False, None),
        ("duplicates", {"numbers": [1, 2, 3, 3], "target": 6}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# 3Sum
# ---------------------------------------------------------------------------


@define(
    slug="3sum",
    title="3Sum",
    difficulty="medium",
    topics=["arrays", "two-pointers"],
    statement=(
        "Return every unique triplet `[a, b, c]` in `nums` such that a + b + c = 0. "
        "The result must not contain duplicate triplets. Return the triplets sorted, and sort the list of triplets."
    ),
    constraints=["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
    signature="from typing import List\n\ndef three_sum(nums: List[int]) -> List[List[int]]:",
    function_name="three_sum",
    hints=[
        "Sort first. Duplicate values then sit together and can be skipped.",
        "Fix one number and solve two-sum on the remainder with opposite pointers.",
        "After recording a triplet, advance both pointers past copies of the values you just used.",
    ],
    approaches=[
        ("Triple loop with a set", "O(n^3)", "O(n)", "Enumerate triples and store canonical sorted tuples."),
        ("Sort plus two pointers", "O(n^2)", "O(1)", "Fix the smallest element, then scan the rest inward. Output space is extra."),
    ],
    editorial=(
        "Sorting costs n log n and makes uniqueness local. For each index i, skip it when nums[i] equals nums[i-1]. "
        "Then run the sorted two-sum procedure on i+1 and the end, targeting -nums[i]. "
        "Each successful hit skips duplicate left and right values so the same triplet is not emitted again."
    ),
    companies=["Amazon", "Facebook", "Adobe", "Microsoft"],
)
def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    found: list[list[int]] = []
    n = len(nums)
    for i in range(n):
        if i and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                found.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return found


def _oracle_three_sum(nums: list[int]) -> list[list[int]]:
    found: set[tuple[int, int, int]] = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in sorted(found)]


cases(
    "3sum",
    _oracle_three_sum,
    [
        ("classic", {"nums": [-1, 0, 1, 2, -1, -4]}, True, "The unique triplets are [-1, -1, 2] and [-1, 0, 1]."),
        ("zeros", {"nums": [0, 0, 0]}, True, "Only [0, 0, 0]."),
        ("none", {"nums": [1, 2, 3]}, False, None),
        ("mixed", {"nums": [-2, 0, 1, 1, 2]}, False, None),
        ("duplicates", {"nums": [-4, -1, -1, 0, 1, 2]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# 3Sum Closest
# ---------------------------------------------------------------------------


@define(
    slug="3sum-closest",
    title="3Sum Closest",
    difficulty="medium",
    topics=["arrays", "two-pointers"],
    statement="Return the sum of three integers in `nums` that is closest to `target`. Each input has exactly one closest sum.",
    constraints=["3 <= nums.length <= 500", "-1000 <= nums[i], target <= 1000"],
    signature="from typing import List\n\ndef three_sum_closest(nums: List[int], target: int) -> int:",
    function_name="three_sum_closest",
    hints=[
        "Sort, then the same two-pointer walk used for 3Sum can track distance instead of equality.",
        "If the current sum is smaller than the target, move the left pointer. If it is larger, move the right pointer.",
        "Keep the sum whose absolute difference from the target is smallest.",
    ],
    approaches=[
        ("All triples", "O(n^3)", "O(1)", "Track the closest sum."),
        ("Sort plus two pointers", "O(n^2)", "O(1)", "Prune the inner search with sorted order."),
    ],
    editorial=(
        "After sorting, fix one index and move two pointers. The sum moves monotonically as a pointer moves, "
        "so you never need to restart the inner scan. Update the best sum whenever the absolute error improves, "
        "and stop early if you hit the target exactly."
    ),
    companies=["Amazon", "Adobe", "Bloomberg", "Google"],
)
def three_sum_closest(nums: list[int], target: int) -> int:
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums)):
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if abs(total - target) < abs(best - target):
                best = total
            if total < target:
                left += 1
            elif total > target:
                right -= 1
            else:
                return total
    return best


def _oracle_three_sum_closest(nums: list[int], target: int) -> int:
    best = nums[0] + nums[1] + nums[2]
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                total = nums[i] + nums[j] + nums[k]
                if abs(total - target) < abs(best - target):
                    best = total
    return best


cases(
    "3sum-closest",
    _oracle_three_sum_closest,
    [
        ("classic", {"nums": [-1, 2, 1, -4], "target": 1}, True, "The closest sum is 2."),
        ("exact", {"nums": [0, 0, 0], "target": 1}, True, "The only sum is 0."),
        ("positive", {"nums": [1, 1, 1, 0], "target": 100}, False, None),
        ("negative-target", {"nums": [1, 2, 4, 8, 16], "target": 10}, False, None),
        ("small", {"nums": [-3, -2, -1, 0], "target": -4}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# 4Sum
# ---------------------------------------------------------------------------


@define(
    slug="4sum",
    title="4Sum",
    difficulty="medium",
    topics=["arrays", "two-pointers"],
    statement=(
        "Return every unique quadruplet that sums to `target`. "
        "Sort each quadruplet and sort the list of quadruplets."
    ),
    constraints=["1 <= nums.length <= 200", "-10^9 <= nums[i], target <= 10^9"],
    signature="from typing import List\n\ndef four_sum(nums: List[int], target: int) -> List[List[int]]:",
    function_name="four_sum",
    hints=[
        "4Sum is 3Sum with one extra fixed index.",
        "Sort, skip duplicates at every fixed index, and finish with two pointers.",
        "Reduce the target by the two fixed values before the inner scan.",
    ],
    approaches=[
        ("Four nested loops", "O(n^4)", "O(n)", "Canonicalize tuples in a set."),
        ("Sort plus k-sum recursion of depth 2", "O(n^3)", "O(1)", "Two fixed indices, then a linear two-pointer scan."),
    ],
    editorial=(
        "Sort the array. The outer two loops choose the first two values and skip duplicates the same way 3Sum does. "
        "The inner two pointers search for target minus those two values. "
        "The pattern generalizes to kSum: k-2 nested loops and one two-pointer base case."
    ),
    companies=["Amazon", "Google", "Apple", "LinkedIn"],
)
def four_sum(nums: list[int], target: int) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    found: list[list[int]] = []
    for i in range(n):
        if i and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, n):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            left, right = j + 1, n - 1
            while left < right:
                total = nums[i] + nums[j] + nums[left] + nums[right]
                if total == target:
                    found.append([nums[i], nums[j], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
    return found


def _oracle_four_sum(nums: list[int], target: int) -> list[list[int]]:
    found: set[tuple[int, ...]] = set()
    n = len(nums)
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    if nums[a] + nums[b] + nums[c] + nums[d] == target:
                        found.add(tuple(sorted((nums[a], nums[b], nums[c], nums[d]))))
    return [list(t) for t in sorted(found)]


cases(
    "4sum",
    _oracle_four_sum,
    [
        ("classic", {"nums": [1, 0, -1, 0, -2, 2], "target": 0}, True, "Four unique quadruplets sum to 0."),
        ("one", {"nums": [2, 2, 2, 2, 2], "target": 8}, True, "Only [2, 2, 2, 2]."),
        ("none", {"nums": [1, 2, 3, 4], "target": 100}, False, None),
        ("mixed", {"nums": [-2, -1, 0, 0, 1, 2], "target": 0}, False, None),
        ("short", {"nums": [1, 2, 3], "target": 6}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Container With Most Water
# ---------------------------------------------------------------------------


@define(
    slug="container-with-most-water",
    title="Container With Most Water",
    difficulty="medium",
    topics=["arrays", "two-pointers"],
    statement=(
        "`height[i]` is the height of a vertical line at x = i. "
        "Choose two lines that, together with the x-axis, form a container holding the most water. Return that maximum area."
    ),
    constraints=["2 <= height.length <= 10^5", "0 <= height[i] <= 10^4"],
    signature="from typing import List\n\ndef max_area(height: List[int]) -> int:",
    function_name="max_area",
    hints=[
        "Area is min(height[left], height[right]) times (right - left).",
        "The width only shrinks as the pointers move inward, so you must gain height to improve.",
        "Always discard the shorter line. The taller line might still pair with a closer line of greater height.",
    ],
    approaches=[
        ("All pairs", "O(n^2)", "O(1)", "Compute every width and limiting height."),
        ("Two pointers", "O(n)", "O(1)", "Start wide and move the shorter side inward."),
    ],
    editorial=(
        "Start at the maximum width. The area is limited by the shorter line. "
        "Moving the taller line inward cannot increase the area, because the width falls and the limiting height cannot rise. "
        "Moving the shorter line is the only move that might help. Each step discards one index, so the scan is linear."
    ),
    companies=["Amazon", "Google", "Adobe", "Bloomberg"],
)
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1
    return best


def _oracle_max_area(height: list[int]) -> int:
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best


cases(
    "container-with-most-water",
    _oracle_max_area,
    [
        ("classic", {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, True, "The best area is 49."),
        ("two", {"height": [1, 1]}, True, "Width 1 and height 1."),
        ("increasing", {"height": [1, 2, 3, 4]}, False, None),
        ("valley", {"height": [5, 1, 1, 5]}, False, None),
        ("peak", {"height": [2, 9, 2]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Trapping Rain Water
# ---------------------------------------------------------------------------


@define(
    slug="trapping-rain-water",
    title="Trapping Rain Water",
    difficulty="hard",
    topics=["arrays", "two-pointers", "stacks"],
    statement=(
        "`height` is a elevation map where each bar has width 1. "
        "Return how many units of water the map can trap after raining."
    ),
    constraints=["1 <= height.length <= 2 * 10^4", "0 <= height[i] <= 10^5"],
    signature="from typing import List\n\ndef trap(height: List[int]) -> int:",
    function_name="trap",
    hints=[
        "Water above index i is min(highest bar on the left, highest bar on the right) minus height[i], when that value is positive.",
        "Precompute left-max and right-max arrays to turn the formula into a linear pass.",
        "Two pointers keep only the current left-max and right-max, because the smaller side is the limiting wall.",
    ],
    approaches=[
        ("Per index scan", "O(n^2)", "O(1)", "Recompute left and right maxima for every bar."),
        ("Prefix maxima", "O(n)", "O(n)", "Two arrays, then one accumulation pass."),
        ("Two pointers", "O(n)", "O(1)", "Process the side whose max wall is smaller."),
    ],
    editorial=(
        "The water at a cell is decided by the shorter of the tallest walls on either side. "
        "With two pointers, if the left wall is the shorter one, every unprocessed cell on the left is limited by left-max, "
        "regardless of what the right side still holds. Add left-max minus height[left], then advance. The symmetric case handles the right side."
    ),
    companies=["Amazon", "Google", "Goldman Sachs", "Microsoft"],
)
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] <= height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


def _oracle_trap(height: list[int]) -> int:
    water = 0
    for i in range(len(height)):
        left = max(height[: i + 1])
        right = max(height[i:])
        water += min(left, right) - height[i]
    return water


cases(
    "trapping-rain-water",
    _oracle_trap,
    [
        ("classic", {"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}, True, "Six units are trapped."),
        ("flat", {"height": [4, 2, 3]}, True, "One unit sits between 4 and 3."),
        ("none", {"height": [1, 2, 3, 4]}, False, None),
        ("valley", {"height": [3, 0, 2]}, False, None),
        ("single", {"height": [5]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Sort Colors
# ---------------------------------------------------------------------------


@define(
    slug="sort-colors",
    title="Sort Colors",
    difficulty="medium",
    topics=["arrays", "two-pointers", "dutch-flag"],
    statement=(
        "`nums` contains only 0, 1, and 2, representing red, white, and blue. "
        "Sort the array in place so that colors are grouped in that order, and return the sorted array. Use a one-pass algorithm."
    ),
    constraints=["1 <= nums.length <= 300", "nums[i] is 0, 1, or 2"],
    signature="from typing import List\n\ndef sort_colors(nums: List[int]) -> List[int]:",
    function_name="sort_colors",
    hints=[
        "Counting each color and rewriting the array is a correct two-pass solution.",
        "The Dutch national flag partition keeps three regions: confirmed 0s, confirmed 2s, and the unknown middle.",
        "Maintain a write index for the next 0 and a write index for the next 2. The scan index only advances on 0 and 1.",
    ],
    approaches=[
        ("Counting sort", "O(n)", "O(1)", "Count 0, 1, and 2, then overwrite the array."),
        ("Dutch national flag", "O(n)", "O(1)", "One pass, three-way partition."),
    ],
    editorial=(
        "Dijkstra's three-way partition uses pointers `low` and `high` around an unknown window. "
        "A 0 at the scan index is swapped to `low` and both advance. A 2 is swapped with `high` and only `high` retreats, "
        "because the swapped-in value has not been inspected. A 1 simply advances the scan."
    ),
    companies=["Microsoft", "Amazon", "Adobe", "Bloomberg"],
)
def sort_colors(nums: list[int]) -> list[int]:
    low = mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
        else:
            mid += 1
    return nums


def _oracle_sort_colors(nums: list[int]) -> list[int]:
    return sorted(nums)


cases(
    "sort-colors",
    _oracle_sort_colors,
    [
        ("classic", {"nums": [2, 0, 2, 1, 1, 0]}, True, "Sorted order is 0, 0, 1, 1, 2, 2."),
        ("sorted", {"nums": [0, 1, 2]}, True, "Already partitioned."),
        ("ones", {"nums": [1, 1, 1]}, False, None),
        ("reversed", {"nums": [2, 2, 1, 0, 0]}, False, None),
        ("single", {"nums": [2]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Move Zeroes
# ---------------------------------------------------------------------------


@define(
    slug="move-zeroes",
    title="Move Zeroes",
    difficulty="easy",
    topics=["arrays", "two-pointers"],
    statement="Move every 0 in `nums` to the end while preserving the relative order of the nonzero elements. Return the rearranged array.",
    constraints=["1 <= nums.length <= 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
    signature="from typing import List\n\ndef move_zeroes(nums: List[int]) -> List[int]:",
    function_name="move_zeroes",
    hints=[
        "A stable filter of nonzeros, followed by zeros, is correct and uses extra memory.",
        "A write pointer marks the next position that should hold a nonzero.",
        "After copying nonzeros forward, fill the tail with zeros. Swapping works too and keeps the algorithm in place.",
    ],
    approaches=[
        ("Stable filter", "O(n)", "O(n)", "Collect nonzeros, then append zeros."),
        ("In-place write pointer", "O(n)", "O(1)", "Compact nonzeros, then zero-fill the suffix."),
    ],
    editorial=(
        "The write pointer is the classic stable partition. Every nonzero is copied to the next write slot and the pointer advances. "
        "The number of leftover slots is the number of zeros, so a second short loop fills them. Order of nonzeros is unchanged because they are copied left to right."
    ),
    companies=["Facebook", "Amazon", "Apple", "Bloomberg"],
)
def move_zeroes(nums: list[int]) -> list[int]:
    write = 0
    for value in nums:
        if value != 0:
            nums[write] = value
            write += 1
    for i in range(write, len(nums)):
        nums[i] = 0
    return nums


def _oracle_move_zeroes(nums: list[int]) -> list[int]:
    nonzero = [value for value in nums if value != 0]
    return nonzero + [0] * (len(nums) - len(nonzero))


cases(
    "move-zeroes",
    _oracle_move_zeroes,
    [
        ("classic", {"nums": [0, 1, 0, 3, 12]}, True, "Nonzeros keep their order."),
        ("no-zero", {"nums": [1, 2, 3]}, True, "Nothing moves."),
        ("all-zero", {"nums": [0, 0]}, False, None),
        ("leading", {"nums": [0, 0, 1]}, False, None),
        ("negatives", {"nums": [0, -1, 0, -2]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Remove Duplicates from Sorted Array
# ---------------------------------------------------------------------------


@define(
    slug="remove-duplicates-from-sorted-array",
    title="Remove Duplicates from Sorted Array",
    difficulty="easy",
    topics=["arrays", "two-pointers"],
    statement=(
        "`nums` is sorted in nondecreasing order. Remove the duplicates in place so each unique value appears once, "
        "preserving order. Return the compacted list of unique values."
    ),
    constraints=["1 <= nums.length <= 3 * 10^4", "-100 <= nums[i] <= 100"],
    signature="from typing import List\n\ndef remove_duplicates(nums: List[int]) -> List[int]:",
    function_name="remove_duplicates",
    hints=[
        "Because the array is sorted, a duplicate is always equal to the previous kept value.",
        "A slow pointer marks the last unique value written.",
        "Copy nums[fast] onto the next slot only when it differs from the last kept value.",
    ],
    approaches=[
        ("Set then sort", "O(n log n)", "O(n)", "Correct but ignores the sorted input."),
        ("Slow and fast pointers", "O(n)", "O(1)", "One forward scan writes each new value once."),
    ],
    editorial=(
        "Initialize the write pointer at 1 if the array is non-empty. "
        "For each later value, write it and advance only when it differs from the value just written. "
        "The prefix of length equal to the write pointer is the answer."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Apple"],
)
def remove_duplicates(nums: list[int]) -> list[int]:
    if not nums:
        return []
    write = 1
    for fast in range(1, len(nums)):
        if nums[fast] != nums[write - 1]:
            nums[write] = nums[fast]
            write += 1
    return nums[:write]


def _oracle_remove_duplicates(nums: list[int]) -> list[int]:
    out: list[int] = []
    for value in nums:
        if not out or out[-1] != value:
            out.append(value)
    return out


cases(
    "remove-duplicates-from-sorted-array",
    _oracle_remove_duplicates,
    [
        ("classic", {"nums": [1, 1, 2]}, True, "Unique prefix is [1, 2]."),
        ("longer", {"nums": [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]}, True, "Five unique values remain."),
        ("single", {"nums": [5]}, False, None),
        ("all-same", {"nums": [7, 7, 7]}, False, None),
        ("already", {"nums": [1, 2, 3]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Squares of a Sorted Array
# ---------------------------------------------------------------------------


@define(
    slug="squares-of-a-sorted-array",
    title="Squares of a Sorted Array",
    difficulty="easy",
    topics=["arrays", "two-pointers"],
    statement="Given a nondecreasing array `nums`, return an array of the squares of each value, also sorted nondecreasing.",
    constraints=["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef sorted_squares(nums: List[int]) -> List[int]:",
    function_name="sorted_squares",
    hints=[
        "Squaring destroys sorted order when negatives are present, because a large negative becomes a large positive.",
        "The largest square is at one of the two ends.",
        "Fill the answer from the back, always taking the end whose absolute value is larger.",
    ],
    approaches=[
        ("Square and sort", "O(n log n)", "O(n)", "Simple and correct."),
        ("Two pointers", "O(n)", "O(n)", "Merge the two increasing rays of absolute values."),
    ],
    editorial=(
        "On a sorted array the absolute values form a valley. "
        "Two pointers at the ends walk up both slopes, and the larger absolute value is written next into the result from right to left."
    ),
    companies=["Facebook", "Amazon", "Google", "Adobe"],
)
def sorted_squares(nums: list[int]) -> list[int]:
    left, right = 0, len(nums) - 1
    out = [0] * len(nums)
    for pos in range(len(nums) - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            out[pos] = nums[left] * nums[left]
            left += 1
        else:
            out[pos] = nums[right] * nums[right]
            right -= 1
    return out


def _oracle_sorted_squares(nums: list[int]) -> list[int]:
    return sorted(value * value for value in nums)


cases(
    "squares-of-a-sorted-array",
    _oracle_sorted_squares,
    [
        ("classic", {"nums": [-4, -1, 0, 3, 10]}, True, "Squares sorted are 0, 1, 9, 16, 100."),
        ("negatives", {"nums": [-7, -3, 2, 3, 11]}, True, "49 and 121 land at the ends."),
        ("positive", {"nums": [1, 2, 3]}, False, None),
        ("single", {"nums": [-5]}, False, None),
        ("zeros", {"nums": [-2, -2, 0]}, False, None),
    ],
)


# ---------------------------------------------------------------------------
# Merge Sorted Array
# ---------------------------------------------------------------------------


@define(
    slug="merge-sorted-array",
    title="Merge Sorted Array",
    difficulty="easy",
    topics=["arrays", "two-pointers"],
    statement=(
        "`nums1` has length m + n. The first m elements are a sorted array, and the last n slots are placeholders. "
        "`nums2` has n sorted elements. Merge nums2 into nums1 so that nums1 becomes one sorted array, and return it."
    ),
    constraints=["0 <= m, n <= 200", "1 <= m + n <= 200", "-10^9 <= values <= 10^9"],
    signature="from typing import List\n\ndef merge_sorted(nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:",
    function_name="merge_sorted",
    hints=[
        "Writing from the left overwrites values in nums1 that have not been merged yet.",
        "The largest remaining element is at the tail of one of the two arrays.",
        "Fill nums1 from index m + n - 1 backward.",
    ],
    approaches=[
        ("Copy and sort", "O((m+n) log(m+n))", "O(1)", "Place nums2 into the tail and sort."),
        ("Reverse two pointers", "O(m+n)", "O(1)", "Merge from the back into free slots."),
    ],
    editorial=(
        "Three pointers: i at the last real element of nums1, j at the last element of nums2, and k at the last slot of nums1. "
        "Write the larger of nums1[i] and nums2[j] at k, and retreat that pointer. "
        "If nums2 is exhausted first, the remaining nums1 prefix is already in place."
    ),
    companies=["Microsoft", "Amazon", "Facebook", "Apple"],
)
def merge_sorted(nums1: list[int], m: int, nums2: list[int], n: int) -> list[int]:
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    return nums1


def _oracle_merge_sorted(nums1: list[int], m: int, nums2: list[int], n: int) -> list[int]:
    return sorted(nums1[:m] + nums2[:n])


cases(
    "merge-sorted-array",
    _oracle_merge_sorted,
    [
        ("classic", {"nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [2, 5, 6], "n": 3}, True, "Merged array is [1, 2, 2, 3, 5, 6]."),
        ("empty-second", {"nums1": [1], "m": 1, "nums2": [], "n": 0}, True, "Nothing to merge."),
        ("empty-first", {"nums1": [0], "m": 0, "nums2": [1], "n": 1}, False, None),
        ("interleave", {"nums1": [1, 3, 5, 0, 0], "m": 3, "nums2": [2, 4], "n": 2}, False, None),
        ("all-larger", {"nums1": [1, 2, 0, 0], "m": 2, "nums2": [3, 4], "n": 2}, False, None),
    ],
)
