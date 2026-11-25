"""Hash-map classics and linked-list problems. Lists are serialized as arrays."""

from __future__ import annotations

from collections import Counter, OrderedDict, defaultdict

from lib import cases, define


def _node_chain(values: list[int]):
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt

    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def _to_list(head) -> list[int]:
    out: list[int] = []
    seen = set()
    while head is not None and id(head) not in seen:
        seen.add(id(head))
        out.append(head.value)
        head = head.nxt
        if len(out) > 10000:
            break
    return out


@define(
    slug="group-anagrams",
    title="Group Anagrams",
    difficulty="medium",
    topics=["strings", "hashing"],
    statement=(
        "Group the strings in `strs` that are anagrams of each other. "
        "Return the groups sorted, and sort the strings inside each group."
    ),
    constraints=["1 <= strs.length <= 10^4", "0 <= strs[i].length <= 100", "strs[i] is lowercase English"],
    signature="from typing import List\n\ndef group_anagrams(strs: List[str]) -> List[List[str]]:",
    function_name="group_anagrams",
    hints=[
        "Two strings are anagrams when their sorted characters match.",
        "A frequency tuple of 26 counts is an equivalent key and avoids sorting long strings.",
        "Append each string to the bucket of its key, then normalize the output order for comparison.",
    ],
    approaches=[
        ("Compare every pair", "O(n^2 * m log m)", "O(n)", "Sort each string and compare it with every group representative."),
        ("Hash by signature", "O(n * m log m)", "O(n * m)", "Map the sorted string, or a count tuple, to its group."),
    ],
    editorial=(
        "The signature of an anagram class is invariant under permutation. Sorting the characters is the simplest signature. "
        "A count of each letter is faster when strings are long and the alphabet is small. "
        "Either key belongs in a hash map from signature to the list of original strings."
    ),
    companies=["Amazon", "Microsoft", "Uber", "Goldman Sachs"],
)
def group_anagrams(strs: list[str]) -> list[list[str]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for word in strs:
        buckets["".join(sorted(word))].append(word)
    groups = [sorted(group) for group in buckets.values()]
    groups.sort()
    return groups


def _oracle_group_anagrams(strs: list[str]) -> list[list[str]]:
    used = [False] * len(strs)
    groups: list[list[str]] = []
    for i, word in enumerate(strs):
        if used[i]:
            continue
        key = sorted(word)
        group = []
        for j, other in enumerate(strs):
            if not used[j] and sorted(other) == key:
                used[j] = True
                group.append(other)
        groups.append(sorted(group))
    groups.sort()
    return groups


cases(
    "group-anagrams",
    _oracle_group_anagrams,
    [
        ("classic", {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, True, "Three anagram classes."),
        ("empty", {"strs": [""]}, True, "A single empty string."),
        ("unique", {"strs": ["a", "b", "c"]}, False, None),
        ("dups", {"strs": ["ab", "ba", "ab"]}, False, None),
        ("single", {"strs": ["abc"]}, False, None),
    ],
)


@define(
    slug="valid-anagram",
    title="Valid Anagram",
    difficulty="easy",
    topics=["strings", "hashing"],
    statement="Return true when `t` is an anagram of `s`. Both strings are lowercase English letters.",
    constraints=["1 <= s.length, t.length <= 5 * 10^4"],
    signature="def is_anagram(s: str, t: str) -> bool:",
    function_name="is_anagram",
    hints=[
        "Equal length is required. A longer string cannot be an anagram.",
        "Sorting both strings and comparing them is correct.",
        "A single frequency array of 26 counters is linear and uses constant extra memory.",
    ],
    approaches=[
        ("Sort both", "O(n log n)", "O(n)", "Anagrams share a sorted form."),
        ("Frequency count", "O(n)", "O(1)", "Increment for s and decrement for t. Every counter must end at zero."),
    ],
    editorial=(
        "An anagram preserves character multiplicity and nothing else. "
        "Counting letters in s and subtracting letters in t detects both missing and extra characters. "
        "If the lengths differ you can return immediately."
    ),
    companies=["Amazon", "Microsoft", "Bloomberg", "Uber"],
)
def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)


def _oracle_is_anagram(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)


cases(
    "valid-anagram",
    _oracle_is_anagram,
    [
        ("yes", {"s": "anagram", "t": "nagaram"}, True, "Same letters."),
        ("no", {"s": "rat", "t": "car"}, True, "Counts differ."),
        ("length", {"s": "ab", "t": "a"}, False, None),
        ("empty", {"s": "", "t": ""}, False, None),
        ("repeat", {"s": "aa", "t": "a"}, False, None),
    ],
)


@define(
    slug="top-k-frequent-elements",
    title="Top K Frequent Elements",
    difficulty="medium",
    topics=["hashing", "heaps", "bucket-sort"],
    statement="Return the `k` most frequent values in `nums`, ordered from most frequent to least frequent. If frequencies tie, the smaller value comes first.",
    constraints=["1 <= nums.length <= 10^5", "k is in the range 1..number of unique values", "-10^4 <= nums[i] <= 10^4"],
    signature="from typing import List\n\ndef top_k_frequent(nums: List[int], k: int) -> List[int]:",
    function_name="top_k_frequent",
    hints=[
        "Count with a hash map first. The rest of the problem is selection on the counts.",
        "A heap of size k keeps the current leaders in O(n log k).",
        "Bucket sort by frequency is linear: bucket[count] holds every value that occurs count times.",
    ],
    approaches=[
        ("Sort unique values", "O(n log n)", "O(n)", "Sort by frequency descending."),
        ("Min-heap of size k", "O(n log k)", "O(n)", "Push counts and pop the smallest when the heap exceeds k."),
        ("Frequency buckets", "O(n)", "O(n)", "Index buckets by count and walk from the high end."),
    ],
    editorial=(
        "Frequency counting is mandatory and linear. "
        "Bucket sort then exploits the fact that a count is between 1 and n. "
        "Walk counts from n down to 1 and emit values until k of them have been produced. "
        "Sorting each bucket by value makes ties deterministic."
    ),
    companies=["Amazon", "Facebook", "Google", "Uber"],
)
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)
    out: list[int] = []
    for count in range(len(nums), 0, -1):
        for value in sorted(buckets[count]):
            out.append(value)
            if len(out) == k:
                return out
    return out


def _oracle_top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [value for value, _ in ranked[:k]]


cases(
    "top-k-frequent-elements",
    _oracle_top_k_frequent,
    [
        ("classic", {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, True, "1 appears three times and 2 appears twice."),
        ("one", {"nums": [1], "k": 1}, True, "The only value."),
        ("tie", {"nums": [4, 4, 2, 2, 3], "k": 2}, False, None),
        ("all", {"nums": [5, 6, 5, 6], "k": 2}, False, None),
        ("k-one", {"nums": [3, 0, 1, 0], "k": 1}, False, None),
    ],
)


@define(
    slug="longest-consecutive-sequence",
    title="Longest Consecutive Sequence",
    difficulty="medium",
    topics=["arrays", "hashing"],
    statement="Given an unsorted integer array, return the length of the longest sequence of consecutive values. The sequence does not have to be contiguous in the array.",
    constraints=["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
    signature="from typing import List\n\ndef longest_consecutive(nums: List[int]) -> int:",
    function_name="longest_consecutive",
    hints=[
        "Sorting yields an O(n log n) answer by scanning neighbors.",
        "A set supports O(1) membership. Only start a run at a value whose predecessor is absent.",
        "Each number is visited at most twice: once in the outer loop and once inside a single run.",
    ],
    approaches=[
        ("Sort and scan", "O(n log n)", "O(n)", "Collapse duplicates and measure streaks."),
        ("Hash set runs", "O(n)", "O(n)", "Start counting only at the beginning of a streak."),
    ],
    editorial=(
        "Put every value in a set. A value starts a consecutive run only when value - 1 is missing. "
        "From each start, walk upward while value + 1 exists and track the longest walk. "
        "Numbers in the middle of a run are skipped as starts, so the total walk cost stays linear."
    ),
    companies=["Google", "Amazon", "Facebook", "Microsoft"],
)
def longest_consecutive(nums: list[int]) -> int:
    pool = set(nums)
    best = 0
    for value in pool:
        if value - 1 in pool:
            continue
        length = 1
        while value + length in pool:
            length += 1
        best = max(best, length)
    return best


def _oracle_longest_consecutive(nums: list[int]) -> int:
    if not nums:
        return 0
    ordered = sorted(set(nums))
    best = run = 1
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1] + 1:
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


cases(
    "longest-consecutive-sequence",
    _oracle_longest_consecutive,
    [
        ("classic", {"nums": [100, 4, 200, 1, 3, 2]}, True, "The streak 1, 2, 3, 4 has length 4."),
        ("dups", {"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}, True, "0 through 8 has length 9."),
        ("empty", {"nums": []}, False, None),
        ("single", {"nums": [7]}, False, None),
        ("gap", {"nums": [1, 2, 4, 5, 6]}, False, None),
    ],
)


@define(
    slug="happy-number",
    title="Happy Number",
    difficulty="easy",
    topics=["hashing", "math"],
    statement=(
        "Start with a positive integer. Replace the number by the sum of the squares of its digits, and repeat. "
        "Return true when the process reaches 1. Return false when it enters a cycle that does not include 1."
    ),
    constraints=["1 <= n <= 2^31 - 1"],
    signature="def is_happy(n: int) -> bool:",
    function_name="is_happy",
    hints=[
        "The digit-square sum of any 32-bit integer quickly falls into a small range, so a cycle must appear.",
        "A set of seen values detects the cycle.",
        "Floyd's cycle rule also works: a slow sum and a fast double sum meet on a cycle. They meet at 1 only for happy numbers.",
    ],
    approaches=[
        ("Seen set", "O(log n) per step, few steps", "O(log n)", "Stop when a value repeats."),
        ("Floyd on the sum function", "O(log n) steps", "O(1)", "Slow and fast digit-square walks."),
    ],
    editorial=(
        "Define next(n) as the sum of squares of decimal digits. "
        "The sequence is infinite, and because next(n) is O(log n) in magnitude it eventually repeats. "
        "Store seen values and return true only if 1 appears before a repeat. Unhappy numbers famously fall into the cycle that contains 4."
    ),
    companies=["Amazon", "Apple", "Google", "Uber"],
)
def is_happy(n: int) -> bool:
    def nxt(x: int) -> int:
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total

    seen: set[int] = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = nxt(n)
    return n == 1


def _oracle_is_happy(n: int) -> bool:
    def nxt(x: int) -> int:
        return sum(int(ch) ** 2 for ch in str(x))

    for _ in range(100):
        if n == 1:
            return True
        n = nxt(n)
    return False


cases(
    "happy-number",
    _oracle_is_happy,
    [
        ("happy", {"n": 19}, True, "19 reaches 1."),
        ("unhappy", {"n": 2}, True, "2 falls into the cycle of 4."),
        ("one", {"n": 1}, False, None),
        ("seven", {"n": 7}, False, None),
        ("ten", {"n": 10}, False, None),
    ],
)


@define(
    slug="contains-duplicate-ii",
    title="Contains Duplicate II",
    difficulty="easy",
    topics=["arrays", "hashing", "sliding-window"],
    statement="Return true when two distinct indices i and j exist with nums[i] == nums[j] and abs(i - j) <= k.",
    constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "0 <= k <= 10^5"],
    signature="from typing import List\n\ndef contains_nearby_duplicate(nums: List[int], k: int) -> bool:",
    function_name="contains_nearby_duplicate",
    hints=[
        "Store the last index of each value.",
        "When the value repeats, compare the distance with k.",
        "A sliding set of the last k elements also works: the window never needs to remember older indices.",
    ],
    approaches=[
        ("All pairs", "O(n * k)", "O(1)", "For each index look back k steps."),
        ("Last index map", "O(n)", "O(n)", "Compare the current index with the previous index of the same value."),
    ],
    editorial=(
        "A dictionary from value to the latest index answers the distance test in expected constant time. "
        "Update the index after the test so the next duplicate sees the closest previous occurrence. "
        "If k is 0, no distinct pair can satisfy the distance, and the map still returns false."
    ),
    companies=["Amazon", "Adobe", "Palantir", "Microsoft"],
)
def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    last: dict[int, int] = {}
    for i, value in enumerate(nums):
        if value in last and i - last[value] <= k:
            return True
        last[value] = i
    return False


def _oracle_contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, min(len(nums), i + k + 1)):
            if nums[i] == nums[j]:
                return True
    return False


cases(
    "contains-duplicate-ii",
    _oracle_contains_nearby_duplicate,
    [
        ("yes", {"nums": [1, 2, 3, 1], "k": 3}, True, "The two 1s are distance 3 apart."),
        ("no", {"nums": [1, 0, 1, 1], "k": 1}, True, "The last two 1s are adjacent."),
        ("far", {"nums": [1, 2, 3, 1, 2, 3], "k": 2}, False, None),
        ("zero-k", {"nums": [1, 1], "k": 0}, False, None),
        ("single", {"nums": [4], "k": 2}, False, None),
    ],
)


@define(
    slug="ransom-note",
    title="Ransom Note",
    difficulty="easy",
    topics=["strings", "hashing"],
    statement="Return true when `ransomNote` can be constructed from the letters in `magazine`. Each magazine letter may be used once.",
    constraints=["1 <= ransomNote.length, magazine.length <= 10^5", "Both strings are lowercase English letters"],
    signature="def can_construct(ransom_note: str, magazine: str) -> bool:",
    function_name="can_construct",
    hints=[
        "This is a multiset inclusion test.",
        "Count magazine letters, then decrement for each ransom letter.",
        "Fail as soon as a count would go negative.",
    ],
    approaches=[
        ("Count both", "O(n + m)", "O(1)", "Compare 26 counters."),
        ("Decrement magazine counts", "O(n + m)", "O(1)", "One array, early exit."),
    ],
    editorial=(
        "Build a frequency map of the magazine. Each character of the note consumes one copy. "
        "If a character is missing or already exhausted, the note cannot be built. "
        "The alphabet is constant, so the extra memory is constant."
    ),
    companies=["Amazon", "Apple", "Adobe", "Microsoft"],
)
def can_construct(ransom_note: str, magazine: str) -> bool:
    stock = Counter(magazine)
    for ch in ransom_note:
        if stock[ch] == 0:
            return False
        stock[ch] -= 1
    return True


def _oracle_can_construct(ransom_note: str, magazine: str) -> bool:
    note = Counter(ransom_note)
    have = Counter(magazine)
    return all(have[ch] >= count for ch, count in note.items())


cases(
    "ransom-note",
    _oracle_can_construct,
    [
        ("no", {"ransom_note": "a", "magazine": "b"}, True, "a is not in the magazine."),
        ("yes", {"ransom_note": "aa", "magazine": "aab"}, True, "Two a's are available."),
        ("exact", {"ransom_note": "abc", "magazine": "cba"}, False, None),
        ("extra", {"ransom_note": "aaa", "magazine": "aa"}, False, None),
        ("longer", {"ransom_note": "bg", "magazine": "efjbdfbdgfjhhaiigfhbaejahgfbbgbjagbddfgdiaigdadhcfcj"}, False, None),
    ],
)


@define(
    slug="first-unique-character",
    title="First Unique Character in a String",
    difficulty="easy",
    topics=["strings", "hashing"],
    statement="Return the index of the first character in `s` that appears exactly once. Return -1 when every character repeats.",
    constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters"],
    signature="def first_uniq_char(s: str) -> int:",
    function_name="first_uniq_char",
    hints=[
        "A first pass counts occurrences.",
        "A second pass returns the first index whose count is 1.",
        "One pass is not enough unless you also store indices, because you do not yet know whether a character will repeat.",
    ],
    approaches=[
        ("Count then scan the string again", "O(n)", "O(1)", "26 counters, then the original order."),
        ("Index map", "O(n)", "O(1)", "Store the first index and mark repeats as -1."),
    ],
    editorial=(
        "Count every character, then walk the string in order and return the first index whose count is one. "
        "The second walk is what preserves 'first'. A heap or sort would destroy that order."
    ),
    companies=["Amazon", "Bloomberg", "Microsoft", "Apple"],
)
def first_uniq_char(s: str) -> int:
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def _oracle_first_uniq_char(s: str) -> int:
    for i, ch in enumerate(s):
        if s.count(ch) == 1:
            return i
    return -1


cases(
    "first-unique-character",
    _oracle_first_uniq_char,
    [
        ("classic", {"s": "leetcode"}, True, "l is unique at index 0."),
        ("later", {"s": "loveleetcode"}, True, "v is the first unique character."),
        ("none", {"s": "aabb"}, False, None),
        ("single", {"s": "z"}, False, None),
        ("end", {"s": "aabbc"}, False, None),
    ],
)


@define(
    slug="intersection-of-two-arrays",
    title="Intersection of Two Arrays",
    difficulty="easy",
    topics=["arrays", "hashing"],
    statement="Return the unique values that appear in both `nums1` and `nums2`, sorted in increasing order.",
    constraints=["1 <= nums1.length, nums2.length <= 1000", "0 <= nums[i] <= 1000"],
    signature="from typing import List\n\ndef intersection(nums1: List[int], nums2: List[int]) -> List[int]:",
    function_name="intersection",
    hints=[
        "A set removes duplicates inside each array.",
        "The intersection of two sets is the answer.",
        "Sort the result so the output is deterministic.",
    ],
    approaches=[
        ("Sort and two pointers", "O(n log n)", "O(n)", "Skip duplicates while merging."),
        ("Hash sets", "O(n + m)", "O(n + m)", "Membership of the smaller set."),
    ],
    editorial=(
        "Build a set from the first array and emit values from the second array that the set contains, recording them once. "
        "Sorting the emitted values gives a canonical answer. Two pointers after sorting are the comparison-based alternative."
    ),
    companies=["Facebook", "Amazon", "Adobe", "Google"],
)
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    return sorted(set(nums1) & set(nums2))


def _oracle_intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    return sorted({value for value in nums1 if value in set(nums2)})


cases(
    "intersection-of-two-arrays",
    _oracle_intersection,
    [
        ("classic", {"nums1": [1, 2, 2, 1], "nums2": [2, 2]}, True, "Only 2 is shared."),
        ("two", {"nums1": [4, 9, 5], "nums2": [9, 4, 9, 8, 4]}, True, "4 and 9, sorted."),
        ("none", {"nums1": [1, 2], "nums2": [3]}, False, None),
        ("same", {"nums1": [1, 1], "nums2": [1]}, False, None),
        ("single", {"nums1": [7], "nums2": [7, 7]}, False, None),
    ],
)


@define(
    slug="intersection-of-two-arrays-ii",
    title="Intersection of Two Arrays II",
    difficulty="easy",
    topics=["arrays", "hashing"],
    statement="Return the intersection of `nums1` and `nums2`, keeping the minimum multiplicity of each value. Sort the result.",
    constraints=["1 <= nums1.length, nums2.length <= 1000", "0 <= nums[i] <= 1000"],
    signature="from typing import List\n\ndef intersect(nums1: List[int], nums2: List[int]) -> List[int]:",
    function_name="intersect",
    hints=[
        "Unique intersection drops repeated matches. This problem must keep them.",
        "Count one array, then walk the other and decrement.",
        "Sort both arrays and advance the pointer of the smaller value. Equal values are emitted once and both pointers move.",
    ],
    approaches=[
        ("Sort and two pointers", "O(n log n)", "O(n)", "Emit while values match."),
        ("Frequency map", "O(n + m)", "O(n)", "Decrement counts from the smaller array."),
    ],
    editorial=(
        "Count values in the first array. For each value in the second, if its remaining count is positive, emit it and decrement. "
        "The result length is the sum of minimum frequencies. Sort it for a stable expected value."
    ),
    companies=["Facebook", "Amazon", "Adobe", "Google"],
)
def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    counts = Counter(nums1)
    out: list[int] = []
    for value in nums2:
        if counts[value] > 0:
            out.append(value)
            counts[value] -= 1
    return sorted(out)


def _oracle_intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    a, b = Counter(nums1), Counter(nums2)
    out: list[int] = []
    for value in sorted(set(a) & set(b)):
        out.extend([value] * min(a[value], b[value]))
    return out


cases(
    "intersection-of-two-arrays-ii",
    _oracle_intersect,
    [
        ("classic", {"nums1": [1, 2, 2, 1], "nums2": [2, 2]}, True, "Both twos are kept."),
        ("mixed", {"nums1": [4, 9, 5], "nums2": [9, 4, 9, 8, 4]}, True, "One 4 and one 9."),
        ("none", {"nums1": [1], "nums2": [2]}, False, None),
        ("more", {"nums1": [1, 1, 1], "nums2": [1, 1]}, False, None),
        ("order", {"nums1": [3, 1, 2], "nums2": [1, 1]}, False, None),
    ],
)


@define(
    slug="4sum-ii",
    title="4Sum II",
    difficulty="medium",
    topics=["arrays", "hashing"],
    statement=(
        "You are given four integer arrays `a`, `b`, `c`, and `d`. "
        "Return the number of tuples (i, j, k, l) such that a[i] + b[j] + c[k] + d[l] == 0."
    ),
    constraints=["1 <= n <= 200 for the full problem", "Tests use small n", "-2^28 <= values <= 2^28"],
    signature="from typing import List\n\ndef four_sum_count(a: List[int], b: List[int], c: List[int], d: List[int]) -> int:",
    function_name="four_sum_count",
    hints=[
        "Four nested loops count tuples correctly and are too slow at n = 200.",
        "Split the sum into (a + b) and (c + d). The second pair must be the negation of the first.",
        "Store every a+b sum in a frequency map, then probe -(c+d).",
    ],
    approaches=[
        ("Four loops", "O(n^4)", "O(1)", "Enumerate every tuple."),
        ("Meet in the middle", "O(n^2)", "O(n^2)", "Hash one pair of arrays and probe the other pair."),
    ],
    editorial=(
        "Every tuple splits into two pairs. Compute all n squared sums from the first two arrays and count them. "
        "Each sum from the last two arrays looks up the negation. "
        "Multiplying is unnecessary: the map already stores how many ways the complement can be formed, so you add that count."
    ),
    companies=["Amazon", "Google", "Adobe", "Facebook"],
)
def four_sum_count(a: list[int], b: list[int], c: list[int], d: list[int]) -> int:
    sums = Counter(x + y for x in a for y in b)
    return sum(sums[-(x + y)] for x in c for y in d)


def _oracle_four_sum_count(a: list[int], b: list[int], c: list[int], d: list[int]) -> int:
    answer = 0
    for w in a:
        for x in b:
            for y in c:
                for z in d:
                    if w + x + y + z == 0:
                        answer += 1
    return answer


cases(
    "4sum-ii",
    _oracle_four_sum_count,
    [
        ("classic", {"a": [1, 2], "b": [-2, -1], "c": [-1, 2], "d": [0, 2]}, True, "Two tuples sum to 0."),
        ("zeros", {"a": [0], "b": [0], "c": [0], "d": [0]}, True, "The only tuple sums to 0."),
        ("none", {"a": [1], "b": [1], "c": [1], "d": [1]}, False, None),
        ("mixed", {"a": [0, 1], "b": [0, -1], "c": [0], "d": [0]}, False, None),
        ("neg", {"a": [-1, 1], "b": [1, -1], "c": [0], "d": [0]}, False, None),
    ],
)


@define(
    slug="isomorphic-strings",
    title="Isomorphic Strings",
    difficulty="easy",
    topics=["strings", "hashing"],
    statement=(
        "Two strings are isomorphic when the characters in `s` can be replaced to obtain `t`, "
        "with a one-to-one mapping. Every occurrence of a character must map to the same character, and no two characters share an image."
    ),
    constraints=["1 <= s.length <= 5 * 10^4", "t.length == s.length"],
    signature="def is_isomorphic(s: str, t: str) -> bool:",
    function_name="is_isomorphic",
    hints=[
        "A single map from s to t is not enough. Two source characters could collide on one target character.",
        "Keep a map in each direction, or map both strings onto the first index where each character appeared.",
        "The pattern of first-seen indices must be identical.",
    ],
    approaches=[
        ("Two hash maps", "O(n)", "O(alphabet)", "Reject a conflicting forward or backward mapping."),
        ("Index signature", "O(n)", "O(alphabet)", "Replace each character by the index of its first occurrence."),
    ],
    editorial=(
        "Walk both strings together. If s[i] already maps to something other than t[i], or t[i] already maps to something other than s[i], the mapping is not a bijection. "
        "Otherwise record both directions. Equal strings are isomorphic under the identity map."
    ),
    companies=["Amazon", "Adobe", "Google", "LinkedIn"],
)
def is_isomorphic(s: str, t: str) -> bool:
    sto: dict[str, str] = {}
    tso: dict[str, str] = {}
    for a, b in zip(s, t):
        if a in sto and sto[a] != b:
            return False
        if b in tso and tso[b] != a:
            return False
        sto[a] = b
        tso[b] = a
    return True


def _oracle_is_isomorphic(s: str, t: str) -> bool:
    def sig(text: str) -> list[int]:
        first: dict[str, int] = {}
        out = []
        for i, ch in enumerate(text):
            if ch not in first:
                first[ch] = i
            out.append(first[ch])
        return out

    return sig(s) == sig(t)


cases(
    "isomorphic-strings",
    _oracle_is_isomorphic,
    [
        ("egg", {"s": "egg", "t": "add"}, True, "e maps to a and g maps to d."),
        ("foo", {"s": "foo", "t": "bar"}, True, "o would need two images."),
        ("paper", {"s": "paper", "t": "title"}, False, None),
        ("bad", {"s": "ab", "t": "aa"}, False, None),
        ("same", {"s": "abc", "t": "abc"}, False, None),
    ],
)


@define(
    slug="word-pattern",
    title="Word Pattern",
    difficulty="easy",
    topics=["strings", "hashing"],
    statement=(
        "Return true when `s` follows the pattern `pattern` with a bijection between pattern letters and words. "
        "`s` is a space-separated list of words."
    ),
    constraints=["1 <= pattern.length <= 300", "s has at most 3000 characters"],
    signature="def word_pattern(pattern: str, s: str) -> bool:",
    function_name="word_pattern",
    hints=[
        "Split s on spaces. The number of words must equal the number of pattern characters.",
        "This is isomorphism between the pattern and the word list.",
        "Use two maps, or compare the first-seen index signatures of both sequences.",
    ],
    approaches=[
        ("Two maps", "O(n)", "O(n)", "Letter to word and word to letter."),
        ("Index signature", "O(n)", "O(n)", "Both sequences must produce the same pattern of first indices."),
    ],
    editorial=(
        "After checking lengths, enforce a bijection. "
        "A letter that already maps must map to the current word, and a word that already maps must map back to the current letter. "
        "The classic counterexample is pattern 'abba' with words 'dog dog dog dog', where one word is claimed by two letters."
    ),
    companies=["Amazon", "Uber", "Dropbox", "Microsoft"],
)
def word_pattern(pattern: str, s: str) -> bool:
    words = s.split(" ")
    if len(words) != len(pattern):
        return False
    pw: dict[str, str] = {}
    wp: dict[str, str] = {}
    for letter, word in zip(pattern, words):
        if letter in pw and pw[letter] != word:
            return False
        if word in wp and wp[word] != letter:
            return False
        pw[letter] = word
        wp[word] = letter
    return True


def _oracle_word_pattern(pattern: str, s: str) -> bool:
    words = s.split(" ")
    if len(words) != len(pattern):
        return False

    def sig(items: list[str]) -> list[int]:
        first: dict[str, int] = {}
        out = []
        for i, item in enumerate(items):
            if item not in first:
                first[item] = i
            out.append(first[item])
        return out

    return sig(list(pattern)) == sig(words)


cases(
    "word-pattern",
    _oracle_word_pattern,
    [
        ("yes", {"pattern": "abba", "s": "dog cat cat dog"}, True, "a is dog and b is cat."),
        ("no", {"pattern": "abba", "s": "dog cat cat fish"}, True, "a would map to both dog and fish."),
        ("collision", {"pattern": "abba", "s": "dog dog dog dog"}, False, None),
        ("length", {"pattern": "abc", "s": "a b"}, False, None),
        ("same", {"pattern": "abc", "s": "a b c"}, False, None),
    ],
)


@define(
    slug="reverse-linked-list",
    title="Reverse Linked List",
    difficulty="easy",
    topics=["linked-lists"],
    statement=(
        "`head` is the value sequence of a singly linked list. Reverse the list iteratively with pointer rewiring and return the new value sequence."
    ),
    constraints=["0 <= length <= 5000", "-5000 <= Node.val <= 5000"],
    signature="from typing import List\n\ndef reverse_list(head: List[int]) -> List[int]:",
    function_name="reverse_list",
    hints=[
        "Three references are enough: previous, current, and the saved next node.",
        "Before you overwrite current.next, store it.",
        "When current becomes null, previous is the new head.",
    ],
    approaches=[
        ("Recursion", "O(n)", "O(n)", "The call stack remembers the way back. Reverse the tail, then attach the head at the end."),
        ("Iteration", "O(n)", "O(1)", "Rewire next pointers in one walk."),
    ],
    editorial=(
        "Build the nodes, then walk them. Save next, point current at previous, and advance both pointers. "
        "The empty list and the one-node list fall out naturally: the loop never runs, or it runs once and previous becomes that node. "
        "The recursive form is the same rewiring expressed as 'reverse the tail, then point the old head's next next back at the head'."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Adobe"],
)
def reverse_list(head: list[int]) -> list[int]:
    current = _node_chain(head)
    previous = None
    while current is not None:
        nxt = current.nxt
        current.nxt = previous
        previous = current
        current = nxt
    return _to_list(previous)


def _oracle_reverse_list(head: list[int]) -> list[int]:
    return list(reversed(head))


cases(
    "reverse-linked-list",
    _oracle_reverse_list,
    [
        ("classic", {"head": [1, 2, 3, 4, 5]}, True, "The reversed sequence is 5, 4, 3, 2, 1."),
        ("two", {"head": [1, 2]}, True, "The two nodes swap."),
        ("empty", {"head": []}, False, None),
        ("single", {"head": [7]}, False, None),
        ("negatives", {"head": [-1, 0, 2]}, False, None),
    ],
)


@define(
    slug="reverse-linked-list-ii",
    title="Reverse Linked List II",
    difficulty="medium",
    topics=["linked-lists"],
    statement=(
        "Reverse the nodes of the list from position `left` to position `right`, using 1-based positions, and return the value sequence. "
        "Do it in one pass."
    ),
    constraints=["1 <= length <= 500", "1 <= left <= right <= length"],
    signature="from typing import List\n\ndef reverse_between(head: List[int], left: int, right: int) -> List[int]:",
    function_name="reverse_between",
    hints=[
        "A dummy node removes the special case where left is 1.",
        "Walk left - 1 steps so you stand on the node before the segment.",
        "Reverse the next (right - left + 1) nodes with the ordinary three-pointer loop, then reconnect both ends.",
    ],
    approaches=[
        ("Convert to an array", "O(n)", "O(n)", "Reverse the slice and rebuild."),
        ("One-pass pointer reverse", "O(n)", "O(1)", "Reverse only the requested segment and stitch it back."),
    ],
    editorial=(
        "Let prev be the node before position left, and let start be the first node of the segment. "
        "Reverse the following right - left nodes by inserting each successor of start directly after prev. "
        "That head-insertion formulation keeps start as the tail of the reversed segment, so the final link from start to the remainder is already correct."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Adobe"],
)
def reverse_between(head: list[int], left: int, right: int) -> list[int]:
    dummy = _node_chain([0])
    dummy.nxt = _node_chain(head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.nxt
    start = prev.nxt
    for _ in range(right - left):
        nxt = start.nxt
        start.nxt = nxt.nxt
        nxt.nxt = prev.nxt
        prev.nxt = nxt
    return _to_list(dummy.nxt)


def _oracle_reverse_between(head: list[int], left: int, right: int) -> list[int]:
    out = list(head)
    out[left - 1 : right] = reversed(out[left - 1 : right])
    return out


cases(
    "reverse-linked-list-ii",
    _oracle_reverse_between,
    [
        ("classic", {"head": [1, 2, 3, 4, 5], "left": 2, "right": 4}, True, "The middle segment reverses."),
        ("whole", {"head": [1, 2, 3], "left": 1, "right": 3}, True, "The entire list reverses."),
        ("single", {"head": [5], "left": 1, "right": 1}, False, None),
        ("tail", {"head": [1, 2, 3, 4], "left": 3, "right": 4}, False, None),
        ("head-two", {"head": [1, 2, 3], "left": 1, "right": 2}, False, None),
    ],
)


@define(
    slug="merge-two-sorted-lists",
    title="Merge Two Sorted Lists",
    difficulty="easy",
    topics=["linked-lists", "two-pointers"],
    statement="Merge two sorted linked lists, given as value arrays, into one sorted list. Return the merged values.",
    constraints=["0 <= length <= 50", "-100 <= Node.val <= 100", "Both lists are sorted nondecreasing"],
    signature="from typing import List\n\ndef merge_two_lists(list1: List[int], list2: List[int]) -> List[int]:",
    function_name="merge_two_lists",
    hints=[
        "A dummy head removes the empty-list special case.",
        "Always attach the smaller current node, and advance that list only.",
        "When one list ends, attach the other list in one pointer assignment.",
    ],
    approaches=[
        ("Array merge", "O(n + m)", "O(n + m)", "The same algorithm on arrays."),
        ("Pointer merge", "O(n + m)", "O(1)", "Rewire existing nodes. The output list is the extra structure the caller asked for."),
    ],
    editorial=(
        "This is the merge step of merge sort, played on nodes. "
        "Compare the two heads, splice the smaller one onto the tail, and repeat. "
        "The unused list is already sorted, so it becomes the final suffix."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Adobe"],
)
def merge_two_lists(list1: list[int], list2: list[int]) -> list[int]:
    a = _node_chain(list1)
    b = _node_chain(list2)
    dummy = _node_chain([0])
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.nxt = a
            a = a.nxt
        else:
            tail.nxt = b
            b = b.nxt
        tail = tail.nxt
    tail.nxt = a if a is not None else b
    return _to_list(dummy.nxt)


def _oracle_merge_two_lists(list1: list[int], list2: list[int]) -> list[int]:
    return sorted(list1 + list2)


cases(
    "merge-two-sorted-lists",
    _oracle_merge_two_lists,
    [
        ("classic", {"list1": [1, 2, 4], "list2": [1, 3, 4]}, True, "The merged list is 1, 1, 2, 3, 4, 4."),
        ("empty", {"list1": [], "list2": []}, True, "Both lists are empty."),
        ("one-empty", {"list1": [], "list2": [0]}, False, None),
        ("longer", {"list1": [1, 5, 7], "list2": [2, 3]}, False, None),
        ("negatives", {"list1": [-3, -1], "list2": [-2, 0]}, False, None),
    ],
)


@define(
    slug="linked-list-cycle",
    title="Linked List Cycle",
    difficulty="easy",
    topics=["linked-lists", "two-pointers"],
    statement=(
        "A singly linked list is given by its values and by `pos`, the 0-based index of the node that the tail points at. "
        "`pos` is -1 when there is no cycle. Return true when a cycle exists. Use Floyd's algorithm, not the index."
    ),
    constraints=["0 <= length <= 10^4", "-1 <= pos < length"],
    signature="from typing import List\n\ndef has_cycle(values: List[int], pos: int) -> bool:",
    function_name="has_cycle",
    hints=[
        "A set of node identities detects a repeat visit and uses linear memory.",
        "Floyd uses two pointers. The fast pointer moves two steps and the slow pointer moves one.",
        "If there is a cycle they meet. If the fast pointer reaches the end, there is no cycle.",
    ],
    approaches=[
        ("Hash set of nodes", "O(n)", "O(n)", "A repeated object identity means a cycle."),
        ("Floyd tortoise and hare", "O(n)", "O(1)", "The fast pointer gains one step per iteration inside the cycle."),
    ],
    editorial=(
        "Build the list and, when pos is nonnegative, point the tail at that node. "
        "Then ignore pos. Advance slow by one and fast by two. A meeting proves a cycle because the only way two different speeds reunite on a finite chain is a loop. "
        "A null next pointer proves the list is finite and acyclic."
    ),
    companies=["Amazon", "Microsoft", "Bloomberg", "Adobe"],
)
def has_cycle(values: list[int], pos: int) -> bool:
    nodes = []
    for value in values:
        node = _node_chain([value])
        if nodes:
            nodes[-1].nxt = node
        nodes.append(node)
    if pos >= 0 and nodes:
        nodes[-1].nxt = nodes[pos]
    slow = fast = nodes[0] if nodes else None
    while fast is not None and fast.nxt is not None:
        slow = slow.nxt
        fast = fast.nxt.nxt
        if slow is fast:
            return True
    return False


def _oracle_has_cycle(values: list[int], pos: int) -> bool:
    return pos >= 0 and len(values) > 0


cases(
    "linked-list-cycle",
    _oracle_has_cycle,
    [
        ("cycle", {"values": [3, 2, 0, -4], "pos": 1}, True, "The tail points at index 1."),
        ("none", {"values": [1, 2], "pos": -1}, True, "The tail is null."),
        ("self", {"values": [1], "pos": 0}, False, None),
        ("empty", {"values": [], "pos": -1}, False, None),
        ("head", {"values": [1, 2, 3], "pos": 0}, False, None),
    ],
)


@define(
    slug="linked-list-cycle-ii",
    title="Linked List Cycle II",
    difficulty="medium",
    topics=["linked-lists", "two-pointers"],
    statement=(
        "Using the same `values` and `pos` encoding as cycle detection, return the 0-based index where the cycle begins. "
        "Return -1 when there is no cycle. Floyd's second phase finds the entrance."
    ),
    constraints=["0 <= length <= 10^4", "-1 <= pos < length"],
    signature="from typing import List\n\ndef detect_cycle(values: List[int], pos: int) -> int:",
    function_name="detect_cycle",
    hints=[
        "Phase one is ordinary Floyd. If they never meet, return -1.",
        "Phase two resets one pointer to the head and moves both one step at a time.",
        "Their next meeting is the entrance. The proof is that the head-to-entrance distance equals the meeting-point-to-entrance distance modulo the cycle length.",
    ],
    approaches=[
        ("Set of seen nodes", "O(n)", "O(n)", "The first repeated node is the entrance."),
        ("Floyd two phases", "O(n)", "O(1)", "Meet inside the cycle, then walk from the head."),
    ],
    editorial=(
        "Let L be the distance from the head to the entrance and C the cycle length. "
        "When the pointers meet, the fast pointer has traveled a multiple of C farther than the slow pointer, and that meeting point is some offset into the cycle. "
        "Resetting one pointer to the head and advancing both by one makes them arrive at the entrance together. Map that node back to its index for the serialized answer."
    ),
    companies=["Amazon", "Microsoft", "Oracle", "Bloomberg"],
)
def detect_cycle(values: list[int], pos: int) -> int:
    nodes = []
    for value in values:
        node = _node_chain([value])
        if nodes:
            nodes[-1].nxt = node
        nodes.append(node)
    if not nodes:
        return -1
    if pos >= 0:
        nodes[-1].nxt = nodes[pos]
    slow = fast = nodes[0]
    while fast is not None and fast.nxt is not None:
        slow = slow.nxt
        fast = fast.nxt.nxt
        if slow is fast:
            finder = nodes[0]
            while finder is not slow:
                finder = finder.nxt
                slow = slow.nxt
            return nodes.index(finder)
    return -1


def _oracle_detect_cycle(values: list[int], pos: int) -> int:
    if pos < 0 or not values:
        return -1
    return pos


cases(
    "linked-list-cycle-ii",
    _oracle_detect_cycle,
    [
        ("middle", {"values": [3, 2, 0, -4], "pos": 1}, True, "The cycle begins at index 1."),
        ("none", {"values": [1, 2], "pos": -1}, True, "There is no entrance."),
        ("head", {"values": [1, 2], "pos": 0}, False, None),
        ("empty", {"values": [], "pos": -1}, False, None),
        ("tail", {"values": [1, 2, 3, 4], "pos": 3}, False, None),
    ],
)


@define(
    slug="remove-nth-node-from-end",
    title="Remove Nth Node From End of List",
    difficulty="medium",
    topics=["linked-lists", "two-pointers"],
    statement="Remove the nth node from the end of the list and return the remaining values. `n` is always valid.",
    constraints=["1 <= length <= 30", "1 <= n <= length"],
    signature="from typing import List\n\ndef remove_nth_from_end(head: List[int], n: int) -> List[int]:",
    function_name="remove_nth_from_end",
    hints=[
        "Two passes work: count the length, then delete length - n.",
        "One pass uses a gap of n nodes between a fast pointer and a slow pointer.",
        "A dummy head makes deleting the first node the same as deleting any other node.",
    ],
    approaches=[
        ("Length then delete", "O(n)", "O(1)", "Two walks."),
        ("Fast and slow gap", "O(n)", "O(1)", "When fast falls off, slow stands before the target."),
    ],
    editorial=(
        "Advance fast n + 1 steps from the dummy, so the gap includes the dummy. "
        "Then move both pointers until fast is null. Slow.next is the node to delete. "
        "Splice it out with slow.next = slow.next.next."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Facebook"],
)
def remove_nth_from_end(head: list[int], n: int) -> list[int]:
    dummy = _node_chain([0])
    dummy.nxt = _node_chain(head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.nxt
    while fast is not None:
        fast = fast.nxt
        slow = slow.nxt
    slow.nxt = slow.nxt.nxt
    return _to_list(dummy.nxt)


def _oracle_remove_nth_from_end(head: list[int], n: int) -> list[int]:
    out = list(head)
    del out[-n]
    return out


cases(
    "remove-nth-node-from-end",
    _oracle_remove_nth_from_end,
    [
        ("classic", {"head": [1, 2, 3, 4, 5], "n": 2}, True, "4 is removed."),
        ("only", {"head": [1], "n": 1}, True, "The list becomes empty."),
        ("head", {"head": [1, 2], "n": 2}, False, None),
        ("tail", {"head": [1, 2, 3], "n": 1}, False, None),
        ("middle", {"head": [7, 8, 9, 10], "n": 3}, False, None),
    ],
)


@define(
    slug="middle-of-the-linked-list",
    title="Middle of the Linked List",
    difficulty="easy",
    topics=["linked-lists", "two-pointers"],
    statement=(
        "Return the value sequence starting at the middle node. "
        "If there are two middle nodes, return the second one and everything after it."
    ),
    constraints=["1 <= length <= 100"],
    signature="from typing import List\n\ndef middle_node(head: List[int]) -> List[int]:",
    function_name="middle_node",
    hints=[
        "Counting the length and walking length // 2 steps is correct.",
        "A fast pointer that moves two steps finds the middle when it reaches the end.",
        "On an even length, two steps per one step lands on the later middle.",
    ],
    approaches=[
        ("Count then walk", "O(n)", "O(1)", "Two passes."),
        ("Slow and fast", "O(n)", "O(1)", "One pass, no stored length."),
    ],
    editorial=(
        "Move slow one step and fast two steps until fast cannot move two steps. "
        "Slow is then the middle required by the problem. Return the suffix that starts there."
    ),
    companies=["Amazon", "Adobe", "Apple", "Microsoft"],
)
def middle_node(head: list[int]) -> list[int]:
    slow = fast = _node_chain(head)
    while fast is not None and fast.nxt is not None:
        slow = slow.nxt
        fast = fast.nxt.nxt
    return _to_list(slow)


def _oracle_middle_node(head: list[int]) -> list[int]:
    return head[len(head) // 2 :]


cases(
    "middle-of-the-linked-list",
    _oracle_middle_node,
    [
        ("odd", {"head": [1, 2, 3, 4, 5]}, True, "The middle suffix starts at 3."),
        ("even", {"head": [1, 2, 3, 4, 5, 6]}, True, "The later middle starts at 4."),
        ("one", {"head": [1]}, False, None),
        ("two", {"head": [1, 2]}, False, None),
        ("four", {"head": [8, 7, 6, 5]}, False, None),
    ],
)


@define(
    slug="palindrome-linked-list",
    title="Palindrome Linked List",
    difficulty="easy",
    topics=["linked-lists", "two-pointers"],
    statement="Return true when the singly linked list, given as values, is a palindrome. The O(1) extra-memory method reverses the second half and compares.",
    constraints=["1 <= length <= 10^5", "0 <= Node.val <= 9"],
    signature="from typing import List\n\ndef is_palindrome_list(head: List[int]) -> bool:",
    function_name="is_palindrome_list",
    hints=[
        "Copying values into an array and using two pointers is the easy solution.",
        "Find the middle with slow and fast pointers, reverse the second half, and compare the two halves.",
        "Restore the second half afterward if the caller needs the original list. The boolean answer does not require restoration.",
    ],
    approaches=[
        ("Array copy", "O(n)", "O(n)", "Compare the sequence with its reverse."),
        ("Reverse second half", "O(n)", "O(1)", "Middle, reverse, compare, optional restore."),
    ],
    editorial=(
        "The array solution is the right first answer in an interview. "
        "If the interviewer asks for constant extra memory, find the middle, reverse from there, and walk the first half against the reversed second half. "
        "A mismatch returns false. Equal length handling is automatic: on an odd list the middle value is shared and does not affect the comparison."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Apple"],
)
def is_palindrome_list(head: list[int]) -> bool:
    slow = fast = _node_chain(head)
    while fast is not None and fast.nxt is not None:
        slow = slow.nxt
        fast = fast.nxt.nxt
    prev = None
    while slow is not None:
        nxt = slow.nxt
        slow.nxt = prev
        prev = slow
        slow = nxt
    left = _node_chain(head)
    right = prev
    while right is not None:
        if left.value != right.value:
            return False
        left = left.nxt
        right = right.nxt
    return True


def _oracle_is_palindrome_list(head: list[int]) -> bool:
    return head == head[::-1]


cases(
    "palindrome-linked-list",
    _oracle_is_palindrome_list,
    [
        ("yes", {"head": [1, 2, 2, 1]}, True, "The list reads the same backward."),
        ("no", {"head": [1, 2]}, True, "1, 2 is not a palindrome."),
        ("odd", {"head": [1, 2, 3, 2, 1]}, False, None),
        ("single", {"head": [7]}, False, None),
        ("almost", {"head": [1, 2, 3, 1]}, False, None),
    ],
)


@define(
    slug="add-two-numbers",
    title="Add Two Numbers",
    difficulty="medium",
    topics=["linked-lists", "math"],
    statement=(
        "Two non-negative integers are stored as digit lists in reverse order, one digit per node. "
        "Add them and return the sum in the same representation."
    ),
    constraints=["1 <= length <= 100", "0 <= digit <= 9", "No leading zeros except the number 0"],
    signature="from typing import List\n\ndef add_two_numbers(l1: List[int], l2: List[int]) -> List[int]:",
    function_name="add_two_numbers",
    hints=[
        "Reverse order means the least significant digit is first, which is the order addition wants.",
        "Carry is 0 or 1, or temporarily 1 plus a 9 and a 9 which is still a single extra digit.",
        "Continue while either list remains or the carry is 1. A final carry creates a new digit.",
    ],
    approaches=[
        ("Convert to integers", "O(n + m)", "O(n + m)", "Fine in Python, and it hides the carry lesson."),
        ("Digit walk with carry", "O(n + m)", "O(1)", "Add one column at a time. The output list is the required space."),
    ],
    editorial=(
        "Initialize carry to 0. At each step add the two digits if those nodes exist, plus the carry. "
        "The output digit is the total modulo 10 and the next carry is the total divided by 10. "
        "Because the lists are already least-significant digit first, you never reverse them."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Bloomberg"],
)
def add_two_numbers(l1: list[int], l2: list[int]) -> list[int]:
    a = _node_chain(l1)
    b = _node_chain(l2)
    dummy = tail = _node_chain([0])
    carry = 0
    while a is not None or b is not None or carry:
        total = carry
        if a is not None:
            total += a.value
            a = a.nxt
        if b is not None:
            total += b.value
            b = b.nxt
        carry, digit = divmod(total, 10)
        tail.nxt = _node_chain([digit])
        tail = tail.nxt
    return _to_list(dummy.nxt)


def _oracle_add_two_numbers(l1: list[int], l2: list[int]) -> list[int]:
    def to_int(digits: list[int]) -> int:
        value = 0
        for i, digit in enumerate(digits):
            value += digit * (10**i)
        return value

    total = to_int(l1) + to_int(l2)
    if total == 0:
        return [0]
    out = []
    while total:
        total, digit = divmod(total, 10)
        out.append(digit)
    return out


cases(
    "add-two-numbers",
    _oracle_add_two_numbers,
    [
        ("classic", {"l1": [2, 4, 3], "l2": [5, 6, 4]}, True, "342 + 465 = 807, stored as 7, 0, 8."),
        ("zero", {"l1": [0], "l2": [0]}, True, "0 + 0 = 0."),
        ("carry", {"l1": [9, 9], "l2": [1]}, False, None),
        ("different", {"l1": [1, 8], "l2": [0]}, False, None),
        ("long-carry", {"l1": [9, 9, 9], "l2": [9, 9, 9]}, False, None),
    ],
)


@define(
    slug="lru-cache",
    title="LRU Cache",
    difficulty="medium",
    topics=["hashing", "linked-lists", "design"],
    statement=(
        "Simulate an LRU cache of the given capacity. "
        "`operations` is a list of 'get' and 'put'. `arguments[i]` is `[key]` for get and `[key, value]` for put. "
        "Return a list of results. get returns the value or -1. put returns null. "
        "Capacity is positive. Evict the least recently used key when the cache is full."
    ),
    constraints=["1 <= capacity <= 3000", "0 <= key, value <= 10^4", "At most 2 * 10^5 calls on the full problem"],
    signature="from typing import List, Optional\n\ndef lru_cache_ops(capacity: int, operations: List[str], arguments: List[List[int]]) -> List[Optional[int]]:",
    function_name="lru_cache_ops",
    hints=[
        "A hash map gives O(1) lookup. It does not remember recency by itself.",
        "A doubly linked list ordered from least recent to most recent supports O(1) splice moves.",
        "Python's ordered dict moves a key to the end on access. The first key is then the eviction victim.",
    ],
    approaches=[
        ("List of pairs", "O(n) per call", "O(capacity)", "Scan to find and move the key."),
        ("Hash map plus ordered list", "O(1) per call", "O(capacity)", "Map for lookup, order for eviction."),
    ],
    editorial=(
        "The interview implementation is a hash map from key to a node in a doubly linked list, with sentinel head and tail. "
        "get and put unlink the node and insert it next to the most-recent sentinel. "
        "When size exceeds capacity, evict the node next to the least-recent sentinel and delete its key. "
        "The ordered-dictionary version is the same policy with the language's insertion-ordered map doing the splice."
    ),
    companies=["Amazon", "Microsoft", "Google", "Bloomberg"],
)
def lru_cache_ops(capacity: int, operations: list[str], arguments: list[list[int]]) -> list[int | None]:
    data: dict[int, int] = {}
    out: list[int | None] = []
    for op, arg in zip(operations, arguments):
        if op == "get":
            key = arg[0]
            if key not in data:
                out.append(-1)
            else:
                value = data.pop(key)
                data[key] = value
                out.append(value)
        else:
            key, value = arg
            if key in data:
                data.pop(key)
            data[key] = value
            if len(data) > capacity:
                oldest = next(iter(data))
                data.pop(oldest)
            out.append(None)
    return out


def _oracle_lru_cache_ops(capacity: int, operations: list[str], arguments: list[list[int]]) -> list[int | None]:
    cache: OrderedDict[int, int] = OrderedDict()
    out: list[int | None] = []
    for op, arg in zip(operations, arguments):
        if op == "get":
            key = arg[0]
            if key not in cache:
                out.append(-1)
            else:
                cache.move_to_end(key)
                out.append(cache[key])
        else:
            key, value = arg
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
            out.append(None)
    return out


cases(
    "lru-cache",
    _oracle_lru_cache_ops,
    [
        (
            "classic",
            {
                "capacity": 2,
                "operations": ["put", "put", "get", "put", "get", "put", "get", "get", "get"],
                "arguments": [[1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
            },
            True,
            "get 2 misses after 3 evicts it. get 1 misses after 4 evicts it.",
        ),
        (
            "update",
            {"capacity": 1, "operations": ["put", "put", "get"], "arguments": [[1, 1], [1, 2], [1]]},
            True,
            "The second put updates the only key.",
        ),
        (
            "miss",
            {"capacity": 2, "operations": ["get"], "arguments": [[1]]},
            False,
            None,
        ),
        (
            "evict-oldest",
            {
                "capacity": 2,
                "operations": ["put", "put", "get", "put", "get", "get"],
                "arguments": [[2, 1], [2, 2], [2], [1, 1], [2], [1]],
            },
            False,
            None,
        ),
        (
            "capacity-one",
            {
                "capacity": 1,
                "operations": ["put", "put", "get", "get"],
                "arguments": [[1, 1], [2, 2], [1], [2]],
            },
            False,
            None,
        ),
    ],
)
