"""Sliding window, prefix, interval, and in-place array problems."""

from __future__ import annotations

from collections import Counter, defaultdict, deque

from lib import cases, define


@define(
    slug="longest-substring-without-repeating-characters",
    title="Longest Substring Without Repeating Characters",
    difficulty="medium",
    topics=["strings", "sliding-window"],
    statement="Given a string `s`, return the length of the longest substring that contains no repeated characters.",
    constraints=["0 <= s.length <= 5 * 10^4", "s consists of English letters, digits, symbols, and spaces"],
    signature="def length_of_longest_substring(s: str) -> int:",
    function_name="length_of_longest_substring",
    hints=[
        "A set of the current window tells you whether the next character is already inside.",
        "When a duplicate appears, shrink the left edge until the window is valid again.",
        "Store the last index of each character so the left edge can jump in one step.",
    ],
    approaches=[
        ("Check every substring", "O(n^3)", "O(n)", "Each slice is tested for uniqueness."),
        ("Sliding window with last index", "O(n)", "O(min(n, alphabet))", "The window only moves forward."),
    ],
    editorial=(
        "Keep the left edge of a valid window and the most recent index of every character. "
        "If s[right] was seen at or after left, move left to that index plus one. "
        "The answer is the maximum of right - left + 1. Each index enters and leaves the window at most once."
    ),
    companies=["Amazon", "Bloomberg", "Adobe", "Google"],
)
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def _oracle_length_of_longest_substring(s: str) -> int:
    best = 0
    for i in range(len(s)):
        seen: set[str] = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best


cases(
    "longest-substring-without-repeating-characters",
    _oracle_length_of_longest_substring,
    [
        ("abc", {"s": "abcabcbb"}, True, "The longest piece is abc, length 3."),
        ("repeat", {"s": "bbbbb"}, True, "A single character, length 1."),
        ("empty", {"s": ""}, False, None),
        ("pwwkew", {"s": "pwwkew"}, False, None),
        ("symbols", {"s": "abba"}, False, None),
    ],
)


@define(
    slug="minimum-window-substring",
    title="Minimum Window Substring",
    difficulty="hard",
    topics=["strings", "sliding-window", "hashing"],
    statement=(
        "Return the minimum window in `s` that covers every character of `t`, including duplicates. "
        "If no such window exists, return an empty string. If several windows share the minimum length, return the one that starts earliest."
    ),
    constraints=["0 <= s.length, t.length <= 10^5 on the full problem", "Tests use short strings so a brute oracle stays honest"],
    signature="def min_window(s: str, t: str) -> str:",
    function_name="min_window",
    hints=[
        "Count how many copies of each character t still needs.",
        "Expand the right edge until the window is feasible, then shrink the left edge while it stays feasible.",
        "Remember the best [left, right] pair seen during the shrink phase.",
    ],
    approaches=[
        ("Every window", "O(n^2 * alphabet)", "O(alphabet)", "Test each slice against the need counts."),
        ("Feasible sliding window", "O(n)", "O(alphabet)", "Two pointers plus a satisfied counter."),
    ],
    editorial=(
        "Maintain a need map copied from t and a counter of how many characters are still missing. "
        "Advance right, and when missing hits zero the window is feasible. "
        "Then advance left, recording the window whenever it is shorter than the best, until the window breaks. "
        "The earliest shortest window wins because a later window replaces the best only when it is strictly shorter."
    ),
    companies=["Facebook", "Amazon", "Google", "LinkedIn"],
)
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best = ""
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            window = s[left : right + 1]
            if best == "" or len(window) < len(best):
                best = window
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return best


def _oracle_min_window(s: str, t: str) -> str:
    if not t:
        return ""
    need = Counter(t)
    best = None
    for i in range(len(s)):
        have: dict[str, int] = {}
        for j in range(i, len(s)):
            have[s[j]] = have.get(s[j], 0) + 1
            if all(have.get(ch, 0) >= cnt for ch, cnt in need.items()):
                window = s[i : j + 1]
                if best is None or len(window) < len(best):
                    best = window
                break
    return best or ""


cases(
    "minimum-window-substring",
    _oracle_min_window,
    [
        ("classic", {"s": "ADOBECODEBANC", "t": "ABC"}, True, "The minimum window is BANC."),
        ("exact", {"s": "a", "t": "a"}, True, "The whole string is the window."),
        ("missing", {"s": "a", "t": "aa"}, False, None),
        ("dupes", {"s": "aaflslflsldkalskaaa", "t": "aaa"}, False, None),
        ("order", {"s": "cabwefgewcwaefgcf", "t": "cae"}, False, None),
    ],
)


@define(
    slug="longest-repeating-character-replacement",
    title="Longest Repeating Character Replacement",
    difficulty="medium",
    topics=["strings", "sliding-window"],
    statement=(
        "You may replace at most `k` characters in `s`. "
        "Return the length of the longest substring that can be made of one repeated character."
    ),
    constraints=["1 <= s.length <= 10^5", "s consists of uppercase English letters", "0 <= k <= s.length"],
    signature="def character_replacement(s: str, k: int) -> int:",
    function_name="character_replacement",
    hints=[
        "A window is valid when its length minus the count of its most frequent character is at most k.",
        "A frequency map of the current window is enough.",
        "The window never needs to shrink by more than it grows, so the best length only increases.",
    ],
    approaches=[
        ("All windows", "O(n^2 * alphabet)", "O(alphabet)", "Test the replacement budget on every slice."),
        ("Sliding window", "O(n)", "O(alphabet)", "Grow the right edge and keep the window valid."),
    ],
    editorial=(
        "For a window, replacements needed equals length minus the highest frequency inside it. "
        "Expand right, update the frequency, and while the window needs more than k replacements, advance left. "
        "The maximum valid length is the answer. The most frequent count inside the window is what decides the budget."
    ),
    companies=["Google", "Amazon", "Microsoft", "Uber"],
)
def character_replacement(s: str, k: int) -> int:
    count: dict[str, int] = {}
    left = best = max_freq = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def _oracle_character_replacement(s: str, k: int) -> int:
    best = 0
    for i in range(len(s)):
        count: dict[str, int] = {}
        for j in range(i, len(s)):
            count[s[j]] = count.get(s[j], 0) + 1
            if (j - i + 1) - max(count.values()) <= k:
                best = max(best, j - i + 1)
            else:
                break
    return best


cases(
    "longest-repeating-character-replacement",
    _oracle_character_replacement,
    [
        ("classic", {"s": "ABAB", "k": 2}, True, "Replace two letters to make AAAA or BBBB."),
        ("one", {"s": "AABABBA", "k": 1}, True, "The best length is 4."),
        ("zero", {"s": "ABCD", "k": 0}, False, None),
        ("all", {"s": "AAAA", "k": 2}, False, None),
        ("budget", {"s": "ABCDE", "k": 1}, False, None),
    ],
)


@define(
    slug="permutation-in-string",
    title="Permutation in String",
    difficulty="medium",
    topics=["strings", "sliding-window"],
    statement="Return true when `s2` contains a permutation of `s1` as a contiguous substring.",
    constraints=["1 <= s1.length, s2.length <= 10^4", "Both strings are lowercase English letters"],
    signature="def check_inclusion(s1: str, s2: str) -> bool:",
    function_name="check_inclusion",
    hints=[
        "A permutation is a window of length len(s1) with the same character counts.",
        "Compare a fixed-size window's counter with the counter of s1.",
        "Slide by adding the incoming character and removing the outgoing one.",
    ],
    approaches=[
        ("Sort every window", "O(n * m log m)", "O(m)", "Sort s1 and each window of that length."),
        ("Fixed window counts", "O(n)", "O(alphabet)", "Maintain a frequency vector of size 26."),
    ],
    editorial=(
        "If s1 is longer than s2 the answer is false. Otherwise build two counters and slide a window of length len(s1). "
        "Equality of counters means the window is a permutation. Decrementing a count to zero should delete the key so dictionary equality stays exact."
    ),
    companies=["Microsoft", "Amazon", "Google", "Bloomberg"],
)
def check_inclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[: len(s1)])
    if window == need:
        return True
    width = len(s1)
    for i in range(width, len(s2)):
        window[s2[i]] += 1
        outgoing = s2[i - width]
        window[outgoing] -= 1
        if window[outgoing] == 0:
            del window[outgoing]
        if window == need:
            return True
    return False


def _oracle_check_inclusion(s1: str, s2: str) -> bool:
    key = sorted(s1)
    width = len(s1)
    for i in range(len(s2) - width + 1):
        if sorted(s2[i : i + width]) == key:
            return True
    return False


cases(
    "permutation-in-string",
    _oracle_check_inclusion,
    [
        ("yes", {"s1": "ab", "s2": "eidbaooo"}, True, "ba is a permutation of ab."),
        ("no", {"s1": "ab", "s2": "eidboaoo"}, True, "No window matches."),
        ("equal", {"s1": "adc", "s2": "dcda"}, False, None),
        ("longer", {"s1": "hello", "s2": "ooolleoooleh"}, False, None),
        ("same", {"s1": "abc", "s2": "abc"}, False, None),
    ],
)


@define(
    slug="find-all-anagrams-in-a-string",
    title="Find All Anagrams in a String",
    difficulty="medium",
    topics=["strings", "sliding-window"],
    statement="Return every start index in `s` where the substring of length len(p) is an anagram of `p`. Indices are in increasing order.",
    constraints=["1 <= s.length, p.length <= 3 * 10^4", "Both strings are lowercase English letters"],
    signature="from typing import List\n\ndef find_anagrams(s: str, p: str) -> List[int]:",
    function_name="find_anagrams",
    hints=[
        "This is permutation-in-string, but you collect every matching index instead of returning early.",
        "A fixed window of length len(p) is the only candidate size.",
        "Update counts in O(1) per slide and compare the frequency vectors.",
    ],
    approaches=[
        ("Sort each window", "O(n * m log m)", "O(m)", "Compare sorted windows with sorted p."),
        ("Sliding counts", "O(n)", "O(alphabet)", "Record the left index whenever the counters match."),
    ],
    editorial=(
        "Build the frequency of p and of the first window. Whenever they match, record index 0 or the current left index. "
        "Then slide: add the new character, remove the character that falls off, and compare again."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Adobe"],
)
def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []
    need = Counter(p)
    window = Counter(s[: len(p)])
    out: list[int] = []
    if window == need:
        out.append(0)
    width = len(p)
    for right in range(width, len(s)):
        window[s[right]] += 1
        left_ch = s[right - width]
        window[left_ch] -= 1
        if window[left_ch] == 0:
            del window[left_ch]
        if window == need:
            out.append(right - width + 1)
    return out


def _oracle_find_anagrams(s: str, p: str) -> list[int]:
    key = sorted(p)
    width = len(p)
    return [i for i in range(len(s) - width + 1) if sorted(s[i : i + width]) == key]


cases(
    "find-all-anagrams-in-a-string",
    _oracle_find_anagrams,
    [
        ("classic", {"s": "cbaebabacd", "p": "abc"}, True, "Anagrams start at 0 and 6."),
        ("overlap", {"s": "abab", "p": "ab"}, True, "Windows start at 0, 1, and 2."),
        ("none", {"s": "aaaa", "p": "b"}, False, None),
        ("longer-p", {"s": "ab", "p": "abc"}, False, None),
        ("single", {"s": "baa", "p": "aa"}, False, None),
    ],
)


@define(
    slug="sliding-window-maximum",
    title="Sliding Window Maximum",
    difficulty="hard",
    topics=["arrays", "sliding-window", "monotonic-deque"],
    statement="Return an array of the maximum value in every contiguous window of length `k` inside `nums`.",
    constraints=["1 <= nums.length <= 10^5", "1 <= k <= nums.length", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef max_sliding_window(nums: List[int], k: int) -> List[int]:",
    function_name="max_sliding_window",
    hints=[
        "Recomputing the max of each window is correct and costs O(nk).",
        "A deque can store indices in decreasing order of value.",
        "Drop indices that fall out of the window from the front, and drop weaker values from the back before pushing the new index.",
    ],
    approaches=[
        ("Scan each window", "O(nk)", "O(1)", "Take max of nums[i:i+k] for each i."),
        ("Monotonic deque", "O(n)", "O(k)", "Each index is pushed and popped at most once."),
    ],
    editorial=(
        "The deque holds candidate indices from front (largest and oldest) to back. "
        "Before using the front, pop it if it is left of the window. "
        "Before pushing i, pop every back index whose value is less than or equal to nums[i], because those candidates can never win while i is inside the window. "
        "Once the window is full, nums[deque[0]] is the answer for that window."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()
    out: list[int] = []
    for i, value in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= value:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def _oracle_max_sliding_window(nums: list[int], k: int) -> list[int]:
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]


cases(
    "sliding-window-maximum",
    _oracle_max_sliding_window,
    [
        ("classic", {"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3}, True, "Window maxima are 3, 3, 5, 5, 6, 7."),
        ("k-one", {"nums": [4, 2, 9], "k": 1}, True, "Each element is its own window."),
        ("whole", {"nums": [9, 8, 7], "k": 3}, False, None),
        ("increasing", {"nums": [1, 2, 3, 4], "k": 2}, False, None),
        ("dups", {"nums": [5, 5, 5, 1], "k": 2}, False, None),
    ],
)


@define(
    slug="minimum-size-subarray-sum",
    title="Minimum Size Subarray Sum",
    difficulty="medium",
    topics=["arrays", "sliding-window", "prefix-sums"],
    statement=(
        "Return the minimal length of a contiguous subarray of `nums` whose sum is at least `target`. "
        "If no such subarray exists, return 0. Every element is positive."
    ),
    constraints=["1 <= target <= 10^9", "1 <= nums.length <= 10^5", "1 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef min_subarray_len(target: int, nums: List[int]) -> int:",
    function_name="min_subarray_len",
    hints=[
        "Positive numbers mean the window sum grows as the right edge moves and shrinks as the left edge moves.",
        "Expand until the sum is large enough, then shrink while it stays large enough.",
        "Track the smallest window length seen during shrinking. Return 0 when the total sum is too small.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Extend each start until the sum reaches the target."),
        ("Positive sliding window", "O(n)", "O(1)", "Each index is added and removed at most once."),
    ],
    editorial=(
        "This is the canonical variable-size window for a monotone condition. "
        "Add nums[right] into the sum. While the sum is at least target, update the best length and subtract nums[left]. "
        "Positivity is the invariant that lets you discard the left element forever."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def min_subarray_len(target: int, nums: list[int]) -> int:
    left = total = 0
    best = len(nums) + 1
    for right, value in enumerate(nums):
        total += value
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best > len(nums) else best


def _oracle_min_subarray_len(target: int, nums: list[int]) -> int:
    best = len(nums) + 1
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                best = min(best, j - i + 1)
                break
    return 0 if best > len(nums) else best


cases(
    "minimum-size-subarray-sum",
    _oracle_min_subarray_len,
    [
        ("classic", {"target": 7, "nums": [2, 3, 1, 2, 4, 3]}, True, "The subarray [4, 3] has length 2."),
        ("none", {"target": 11, "nums": [1, 1, 1, 1]}, True, "The total is 4, so the answer is 0."),
        ("single", {"target": 4, "nums": [1, 4, 4]}, False, None),
        ("whole", {"target": 15, "nums": [1, 2, 3, 4, 5]}, False, None),
        ("exact", {"target": 3, "nums": [1, 2, 3]}, False, None),
    ],
)


@define(
    slug="subarray-sum-equals-k",
    title="Subarray Sum Equals K",
    difficulty="medium",
    topics=["arrays", "prefix-sums", "hashing"],
    statement="Return the number of contiguous subarrays whose elements sum to `k`. Values may be negative.",
    constraints=["1 <= nums.length <= 2 * 10^4", "-1000 <= nums[i] <= 1000", "-10^7 <= k <= 10^7"],
    signature="from typing import List\n\ndef subarray_sum(nums: List[int], k: int) -> int:",
    function_name="subarray_sum",
    hints=[
        "A sliding window fails once negatives appear, because growing the window does not grow the sum.",
        "If prefix[j] - prefix[i] = k, the subarray (i, j] sums to k.",
        "A hash map from prefix sum to how many times it has occurred answers the lookup in expected constant time.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Extend every start and add the running sum."),
        ("Prefix frequency map", "O(n)", "O(n)", "Count earlier prefixes equal to current prefix minus k."),
    ],
    editorial=(
        "Seed the map with prefix 0 occurring once, which accounts for subarrays that start at index 0. "
        "Walk the array, add the current value into the prefix, and add map[prefix - k] to the answer before recording the new prefix. "
        "Order matters: count first, then increment, so an empty subarray is not counted unless k is zero and you intentionally allow it. Here the seed handles only real ranges."
    ),
    companies=["Facebook", "Amazon", "Google", "Microsoft"],
)
def subarray_sum(nums: list[int], k: int) -> int:
    seen = {0: 1}
    prefix = answer = 0
    for value in nums:
        prefix += value
        answer += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return answer


def _oracle_subarray_sum(nums: list[int], k: int) -> int:
    answer = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                answer += 1
    return answer


cases(
    "subarray-sum-equals-k",
    _oracle_subarray_sum,
    [
        ("classic", {"nums": [1, 1, 1], "k": 2}, True, "Two subarrays sum to 2."),
        ("mixed", {"nums": [1, 2, 3], "k": 3}, True, "Both [1, 2] and [3] qualify."),
        ("negatives", {"nums": [1, -1, 0], "k": 0}, False, None),
        ("none", {"nums": [1, 2], "k": 5}, False, None),
        ("whole", {"nums": [3, 4, 7, -2], "k": 12}, False, None),
    ],
)


@define(
    slug="subarray-product-less-than-k",
    title="Subarray Product Less Than K",
    difficulty="medium",
    topics=["arrays", "sliding-window"],
    statement="Return the number of contiguous subarrays where the product of the elements is strictly less than `k`. Every element is positive.",
    constraints=["1 <= nums.length <= 3 * 10^4", "1 <= nums[i] <= 1000", "0 <= k <= 10^6"],
    signature="from typing import List\n\ndef num_subarray_product_less_than_k(nums: List[int], k: int) -> int:",
    function_name="num_subarray_product_less_than_k",
    hints=[
        "If k is 0 or 1, no positive product can be strictly smaller.",
        "A product of positives grows as the window grows, so a sliding window applies.",
        "When the window [left, right] is valid, every subarray ending at right and starting between left and right is valid. That is right - left + 1 new subarrays.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Multiply until the product reaches k."),
        ("Sliding window count", "O(n)", "O(1)", "Add the number of valid subarrays ending at right."),
    ],
    editorial=(
        "Maintain a product and a left edge. While the product is at least k, divide out nums[left]. "
        "A valid window ending at right contributes right - left + 1 subarrays, one for each possible start. "
        "This counts each subarray once, at its right endpoint."
    ),
    companies=["Amazon", "Google", "Adobe", "Yandex"],
)
def num_subarray_product_less_than_k(nums: list[int], k: int) -> int:
    if k <= 1:
        return 0
    prod = 1
    left = answer = 0
    for right, value in enumerate(nums):
        prod *= value
        while prod >= k:
            prod //= nums[left]
            left += 1
        answer += right - left + 1
    return answer


def _oracle_num_subarray_product_less_than_k(nums: list[int], k: int) -> int:
    answer = 0
    for i in range(len(nums)):
        prod = 1
        for j in range(i, len(nums)):
            prod *= nums[j]
            if prod < k:
                answer += 1
            else:
                break
    return answer


cases(
    "subarray-product-less-than-k",
    _oracle_num_subarray_product_less_than_k,
    [
        ("classic", {"nums": [10, 5, 2, 6], "k": 100}, True, "Eight subarrays have product below 100."),
        ("none", {"nums": [1, 2, 3], "k": 0}, True, "No positive product is below 0."),
        ("all", {"nums": [1, 1, 1], "k": 2}, False, None),
        ("single-fail", {"nums": [10, 5], "k": 5}, False, None),
        ("window", {"nums": [1, 2, 3, 4], "k": 10}, False, None),
    ],
)


@define(
    slug="max-consecutive-ones-iii",
    title="Max Consecutive Ones III",
    difficulty="medium",
    topics=["arrays", "sliding-window"],
    statement="You may flip at most `k` zeros in the binary array `nums`. Return the maximum number of consecutive 1s you can produce.",
    constraints=["1 <= nums.length <= 10^5", "nums[i] is 0 or 1", "0 <= k <= nums.length"],
    signature="from typing import List\n\ndef longest_ones(nums: List[int], k: int) -> int:",
    function_name="longest_ones",
    hints=[
        "A window is valid when it contains at most k zeros.",
        "Expand the right edge. When zeros exceed k, advance the left edge.",
        "The longest valid window length is the answer.",
    ],
    approaches=[
        ("All windows", "O(n^2)", "O(1)", "Count zeros in every slice."),
        ("Sliding window", "O(n)", "O(1)", "Keep a running zero count."),
    ],
    editorial=(
        "This is the at-most-k variant of the sliding window. "
        "Count zeros inside the window. While the count exceeds k, move left and decrement when a zero leaves. "
        "Every valid window length is a candidate. Because both edges only move forward, the scan is linear."
    ),
    companies=["Google", "Amazon", "Facebook", "Microsoft"],
)
def longest_ones(nums: list[int], k: int) -> int:
    left = zeros = best = 0
    for right, value in enumerate(nums):
        zeros += value == 0
        while zeros > k:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1)
    return best


def _oracle_longest_ones(nums: list[int], k: int) -> int:
    best = 0
    for i in range(len(nums)):
        zeros = 0
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)
    return best


cases(
    "max-consecutive-ones-iii",
    _oracle_longest_ones,
    [
        ("classic", {"nums": [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], "k": 2}, True, "Flipping two zeros yields six 1s."),
        ("none", {"nums": [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], "k": 3}, True, "The best length is 10."),
        ("zero-budget", {"nums": [1, 0, 1], "k": 0}, False, None),
        ("all-zero", {"nums": [0, 0, 0], "k": 1}, False, None),
        ("all-one", {"nums": [1, 1, 1], "k": 0}, False, None),
    ],
)


@define(
    slug="fruit-into-baskets",
    title="Fruit Into Baskets",
    difficulty="medium",
    topics=["arrays", "sliding-window"],
    statement=(
        "You have two baskets, and each basket holds only one type of fruit. "
        "`fruits[i]` is the type of fruit on tree i in a row. "
        "Pick one contiguous stretch of trees, putting each fruit into a basket of its type. Return the maximum number of fruits you can pick."
    ),
    constraints=["1 <= fruits.length <= 10^5", "0 <= fruits[i] < fruits.length"],
    signature="from typing import List\n\ndef total_fruit(fruits: List[int]) -> int:",
    function_name="total_fruit",
    hints=[
        "The stretch may contain at most two distinct values.",
        "A sliding window with a frequency map enforces that limit.",
        "Shrink from the left while the map holds three types.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Track the set size of every slice."),
        ("At most two types", "O(n)", "O(1)", "The map never holds more than three keys."),
    ],
    editorial=(
        "This is longest subarray with at most two distinct values. "
        "Expand the window, and while a third type appears, decrement the left fruit and delete it from the map when its count hits zero. "
        "The longest window is the answer."
    ),
    companies=["Google", "Amazon", "Adobe", "Uber"],
)
def total_fruit(fruits: list[int]) -> int:
    count: dict[int, int] = {}
    left = best = 0
    for right, fruit in enumerate(fruits):
        count[fruit] = count.get(fruit, 0) + 1
        while len(count) > 2:
            count[fruits[left]] -= 1
            if count[fruits[left]] == 0:
                del count[fruits[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def _oracle_total_fruit(fruits: list[int]) -> int:
    best = 0
    for i in range(len(fruits)):
        seen: set[int] = set()
        for j in range(i, len(fruits)):
            seen.add(fruits[j])
            if len(seen) > 2:
                break
            best = max(best, j - i + 1)
    return best


cases(
    "fruit-into-baskets",
    _oracle_total_fruit,
    [
        ("classic", {"fruits": [1, 2, 1]}, True, "The whole row uses two types."),
        ("three", {"fruits": [0, 1, 2, 2]}, True, "The best stretch is [1, 2, 2]."),
        ("one", {"fruits": [1, 1, 1]}, False, None),
        ("alt", {"fruits": [1, 2, 3, 2, 2]}, False, None),
        ("single", {"fruits": [4]}, False, None),
    ],
)


@define(
    slug="find-pivot-index",
    title="Find Pivot Index",
    difficulty="easy",
    topics=["arrays", "prefix-sums"],
    statement=(
        "The pivot index is the index where the sum of the numbers strictly to the left equals the sum of the numbers strictly to the right. "
        "Return the leftmost pivot index, or -1 if none exists. An empty side sums to 0."
    ),
    constraints=["1 <= nums.length <= 10^4", "-1000 <= nums[i] <= 1000"],
    signature="from typing import List\n\ndef pivot_index(nums: List[int]) -> int:",
    function_name="pivot_index",
    hints=[
        "The total sum is fixed. At index i the right sum is total minus left sum minus nums[i].",
        "Walk once, adding nums[i] into the left sum after the comparison.",
        "Return the first index that balances. Do not restart the scan.",
    ],
    approaches=[
        ("Recompute both sides", "O(n^2)", "O(1)", "Sum left and right at every index."),
        ("One running left sum", "O(n)", "O(1)", "Right sum is derived from the total."),
    ],
    editorial=(
        "Let total be the sum of the array. Initialize left to 0. "
        "At index i, the right sum is total - left - nums[i]. If left equals that value, return i. "
        "Otherwise add nums[i] into left. The empty-side case falls out when i is 0 or n - 1."
    ),
    companies=["Amazon", "Facebook", "Google", "Microsoft"],
)
def pivot_index(nums: list[int]) -> int:
    total = sum(nums)
    left = 0
    for i, value in enumerate(nums):
        if left == total - left - value:
            return i
        left += value
    return -1


def _oracle_pivot_index(nums: list[int]) -> int:
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1 :]):
            return i
    return -1


cases(
    "find-pivot-index",
    _oracle_pivot_index,
    [
        ("classic", {"nums": [1, 7, 3, 6, 5, 6]}, True, "Index 3 balances both sides at 11."),
        ("none", {"nums": [1, 2, 3]}, True, "No index balances."),
        ("left-empty", {"nums": [2, 1, -1]}, False, None),
        ("zeros", {"nums": [0, 0, 0, 0]}, False, None),
        ("single", {"nums": [5]}, False, None),
    ],
)


@define(
    slug="subarray-sums-divisible-by-k",
    title="Subarray Sums Divisible by K",
    difficulty="medium",
    topics=["arrays", "prefix-sums", "hashing"],
    statement="Return the number of non-empty contiguous subarrays whose sum is divisible by `k`.",
    constraints=["1 <= nums.length <= 3 * 10^4", "-10^4 <= nums[i] <= 10^4", "2 <= k <= 10^4"],
    signature="from typing import List\n\ndef subarrays_div_by_k(nums: List[int], k: int) -> int:",
    function_name="subarrays_div_by_k",
    hints=[
        "A subarray sum is a difference of prefix sums. That difference is divisible by k when the prefixes share a remainder.",
        "Negative prefixes need a nonnegative remainder. In Python the % operator already does that.",
        "Count how many earlier prefixes have the same remainder, including remainder 0 before the array starts.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Test every range sum modulo k."),
        ("Remainder frequency", "O(n)", "O(k)", "Map each prefix remainder to its count."),
    ],
    editorial=(
        "prefix[j] - prefix[i] is divisible by k exactly when prefix[j] and prefix[i] are congruent modulo k. "
        "Seed remainder 0 with count 1. For each new prefix remainder, add the number of times it has already occurred, then increment its count."
    ),
    companies=["Amazon", "Google", "Facebook", "Mathworks"],
)
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = {0: 1}
    prefix = answer = 0
    for value in nums:
        prefix = (prefix + value) % k
        answer += seen.get(prefix, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return answer


def _oracle_subarrays_div_by_k(nums: list[int], k: int) -> int:
    answer = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total % k == 0:
                answer += 1
    return answer


cases(
    "subarray-sums-divisible-by-k",
    _oracle_subarrays_div_by_k,
    [
        ("classic", {"nums": [4, 5, 0, -2, -3, 1], "k": 5}, True, "Seven subarrays are divisible by 5."),
        ("simple", {"nums": [5], "k": 9}, True, "5 is not divisible by 9."),
        ("zeros", {"nums": [0, 0], "k": 2}, False, None),
        ("negatives", {"nums": [-1, 2, 9], "k": 2}, False, None),
        ("all", {"nums": [2, 4, 6], "k": 2}, False, None),
    ],
)


@define(
    slug="continuous-subarray-sum",
    title="Continuous Subarray Sum",
    difficulty="medium",
    topics=["arrays", "prefix-sums", "hashing"],
    statement=(
        "Return true when `nums` has a contiguous subarray of length at least 2 whose sum is a multiple of `k`. "
        "A multiple includes 0. `k` is at least 1."
    ),
    constraints=["1 <= nums.length <= 10^5", "0 <= nums[i] <= 10^9", "1 <= k <= 2^31 - 1"],
    signature="from typing import List\n\ndef check_subarray_sum(nums: List[int], k: int) -> bool:",
    function_name="check_subarray_sum",
    hints=[
        "Equal prefix remainders mark a multiple, but the two prefixes must be at least two indices apart.",
        "Store the first index of each remainder.",
        "Seed remainder 0 at index -1 so a prefix that itself is a multiple of length at least 2 is detected.",
    ],
    approaches=[
        ("All subarrays", "O(n^2)", "O(1)", "Test every range of length at least 2."),
        ("First remainder index", "O(n)", "O(min(n, k))", "Stop when the same remainder is at least two steps old."),
    ],
    editorial=(
        "If prefix[j] and prefix[i] share a remainder and j - i >= 2, the subarray (i, j] has length at least 2 and a sum divisible by k. "
        "Record a remainder only the first time you see it, so the gap is as large as possible. "
        "The seed (0, -1) handles subarrays that start at index 0."
    ),
    companies=["Amazon", "Facebook", "Mathworks", "Adobe"],
)
def check_subarray_sum(nums: list[int], k: int) -> bool:
    seen = {0: -1}
    prefix = 0
    for i, value in enumerate(nums):
        prefix = (prefix + value) % k
        if prefix in seen:
            if i - seen[prefix] >= 2:
                return True
        else:
            seen[prefix] = i
    return False


def _oracle_check_subarray_sum(nums: list[int], k: int) -> bool:
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if j - i >= 1 and total % k == 0:
                return True
    return False


cases(
    "continuous-subarray-sum",
    _oracle_check_subarray_sum,
    [
        ("yes", {"nums": [23, 2, 4, 6, 7], "k": 6}, True, "[2, 4] sums to 6."),
        ("no", {"nums": [23, 2, 6, 4, 7], "k": 13}, True, "No qualifying subarray."),
        ("zeros", {"nums": [0, 0], "k": 1}, False, None),
        ("short", {"nums": [5], "k": 5}, False, None),
        ("pair", {"nums": [1, 2, 3], "k": 5}, False, None),
    ],
)


@define(
    slug="maximum-sum-circular-subarray",
    title="Maximum Sum Circular Subarray",
    difficulty="medium",
    topics=["arrays", "kadane"],
    statement=(
        "Return the maximum possible sum of a non-empty subarray of `nums`, where the array is circular. "
        "A circular subarray may wrap from the end back to the start. A one-interval ordinary subarray is also allowed."
    ),
    constraints=["1 <= nums.length <= 3 * 10^4", "-3 * 10^4 <= nums[i] <= 3 * 10^4"],
    signature="from typing import List\n\ndef max_subarray_sum_circular(nums: List[int]) -> int:",
    function_name="max_subarray_sum_circular",
    hints=[
        "The answer is either a normal Kadane maximum or the total sum minus a minimum subarray in the middle.",
        "The wrap-around case is invalid when the minimum subarray is the entire array, which happens when every element is negative.",
        "Run max-Kadane and min-Kadane in one pass, then take max(best_max, total - best_min) unless best_max is negative.",
    ],
    approaches=[
        ("Duplicate the array", "O(n^2)", "O(n)", "Search every start and a length up to n on nums + nums."),
        ("Kadane plus inverted Kadane", "O(n)", "O(1)", "Max subarray, or total minus min subarray."),
    ],
    editorial=(
        "A maximum circular subarray either does not wrap, which is ordinary Kadane, or it wraps. "
        "The wrapping case is the total sum minus the minimum non-wrapping subarray that was excluded from the middle. "
        "If the maximum element is negative, that exclusion would be the whole array and the wrap sum would be 0, so return the ordinary maximum instead."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def max_subarray_sum_circular(nums: list[int]) -> int:
    total = best_max = cur_max = best_min = cur_min = nums[0]
    for value in nums[1:]:
        total += value
        cur_max = max(value, cur_max + value)
        best_max = max(best_max, cur_max)
        cur_min = min(value, cur_min + value)
        best_min = min(best_min, cur_min)
    if best_max < 0:
        return best_max
    return max(best_max, total - best_min)


def _oracle_max_subarray_sum_circular(nums: list[int]) -> int:
    n = len(nums)
    best = nums[0]
    doubled = nums + nums
    for i in range(n):
        total = 0
        for length in range(1, n + 1):
            total += doubled[i + length - 1]
            best = max(best, total)
    return best


cases(
    "maximum-sum-circular-subarray",
    _oracle_max_subarray_sum_circular,
    [
        ("wrap", {"nums": [5, -3, 5]}, True, "The wrap [5, 5] sums to 10."),
        ("normal", {"nums": [1, -2, 3, -2]}, True, "The subarray [3] sums to 3."),
        ("all-negative", {"nums": [-3, -2, -3]}, False, None),
        ("single", {"nums": [8]}, False, None),
        ("mixed", {"nums": [3, -1, 2, -1]}, False, None),
    ],
)


@define(
    slug="maximum-sum-subarray-of-size-k",
    title="Maximum Sum Subarray of Size K",
    difficulty="easy",
    topics=["arrays", "sliding-window"],
    statement="Return the maximum sum of any contiguous subarray of length exactly `k`.",
    constraints=["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef max_sum_subarray_k(nums: List[int], k: int) -> int:",
    function_name="max_sum_subarray_k",
    hints=[
        "The first window sum is the sum of the first k elements.",
        "The next window drops nums[i - k] and adds nums[i].",
        "Track the maximum window sum as you slide.",
    ],
    approaches=[
        ("Recompute each window", "O(nk)", "O(1)", "Sum every slice of length k."),
        ("Fixed sliding window", "O(n)", "O(1)", "Update the sum in constant time per step."),
    ],
    editorial=(
        "A fixed-size window is the simplest sliding-window form. "
        "Compute the first sum, then for each new right edge subtract the element that leaves and add the element that enters. "
        "The maximum of those sums is the answer. This is also the integer core of the maximum-average problem, since the average is the sum divided by k."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def max_sum_subarray_k(nums: list[int], k: int) -> int:
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


def _oracle_max_sum_subarray_k(nums: list[int], k: int) -> int:
    return max(sum(nums[i : i + k]) for i in range(len(nums) - k + 1))


cases(
    "maximum-sum-subarray-of-size-k",
    _oracle_max_sum_subarray_k,
    [
        ("classic", {"nums": [2, 1, 5, 1, 3, 2], "k": 3}, True, "The window [5, 1, 3] sums to 9."),
        ("negatives", {"nums": [-1, -2, 3, 4], "k": 2}, True, "The window [3, 4] sums to 7."),
        ("k-one", {"nums": [4, 1, 9], "k": 1}, False, None),
        ("whole", {"nums": [1, 2, 3], "k": 3}, False, None),
        ("ties", {"nums": [1, 2, 1, 2], "k": 2}, False, None),
    ],
)
