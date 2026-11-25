"""Two pointers and sliding windows."""

from emit import emit

TWO = r'''
## Why this matters

A huge fraction of array and string interviews are a scan that keeps two indexes with a simple invariant. The naive version tries every pair or every slice and pays a quadratic cost. Two pointers turn that search into one pass when the array is sorted, or when moving one pointer only makes the answer more feasible. You will use the pattern for pair sums, partitions, palindromes, trapping water, merging, and the Dutch national flag. If you can state the invariant, the code is short. If you cannot, the code becomes a pile of special cases that fail on duplicates.

## Intuition

Think of two people walking on a number line. When the array is sorted and you want a pair that sums to a target, one person starts at the left and one at the right. If the sum is too small, the left person must move right, because every value to the left is even smaller. If the sum is too large, the right person must move left. Each move throws away a whole row or column of the pair matrix, not a single pair. That is why the algorithm is linear after the sort. The same "this side can never win" idea appears when you shrink a window, partition around a pivot, or move a read pointer and a write pointer through an array you are compacting.

## Core concept in depth

A two-pointer algorithm maintains indexes i and j, usually with i less than or equal to j, and a statement that is true at the start of every iteration. The body moves at least one index so the unsearched region shrinks. Termination is the moment the region is empty. Correctness is the invariant plus the fact that every discarded index was impossible.

Opposite-end pointers want a monotone property. On a sorted array, the pair sum increases when the left index increases and decreases when the right index decreases. Therefore a too-small sum cannot be fixed by moving the right index left, and you may discard the left index forever. Container With Most Water uses a different monotone argument. The area is width times the shorter line. If the left line is shorter, every container that keeps that left line and a nearer right line is weakly worse, because the width shrinks and the height cannot exceed the left line. So you advance the shorter side. This argument fails if you advance the taller side: you might skip the only wide container that used the short side against a still-tall partner.

Same-direction pointers compact or partition. The write pointer marks the end of the region that already satisfies the output property. The read pointer scans forward. Move Zeroes keeps the write pointer on the next slot that should hold a non-zero. Remove Duplicates from a sorted array keeps the write pointer on the last unique value kept so far. The read pointer runs to the end, so the algorithm is one pass and the extra memory is constant. The prefix of length write + 1 is the answer. You do not need a second array.

Three pointers show up in the Dutch national flag and in merging. Sort Colors uses lo, mid, and hi. Values before lo are 0, values after hi are 2, and values before mid have been classified. The mid pointer is the one that moves through unknown territory. A 0 swaps with lo and both lo and mid advance. A 2 swaps with hi and only hi retreats, because the swapped-in value has not been classified. A 1 just advances mid. That asymmetry is the whole algorithm. Merging two sorted lists uses one pointer into each list and writes the smaller head. It is the same idea as the opposite-end scan, except both pointers move only forward and the output grows.

Trapping rain water can be solved with opposite-end pointers too. The water above a position is limited by the taller of the shorter bounding walls. Maintain the best wall seen from the left and from the right. The side with the smaller best wall is the one whose next position has a known water level, because the opposite side promises at least that height. Add the difference, then advance that side. The prefix-max and suffix-max arrays are the memory-heavy version of the same fact. The two-pointer version stores only the two running maxima.

Palindromes use opposite ends on a string. Move inward while the characters match. Valid Palindrome II allows one skip. The moment they differ, you check the two possibilities "skip left" and "skip right" with an ordinary palindrome test that is allowed no further skips. That is still linear, because each skip branch is a single inward scan and you do it only once.

Not every pair problem is a two-pointer problem. Two Sum on an unsorted array does not have the monotone property until you sort, and sorting loses the original indexes unless you sort pairs of value and index. A hash map is the better trade when indexes matter and an expected linear bound is acceptable. Two pointers are the better trade when the data is already sorted or when you must use constant extra memory.

## Diagram and dry run

```mermaid
flowchart TD
    A[Sorted array, target sum] --> B[lo at the left, hi at the right]
    B --> C{Sum versus target}
    C -->|Too small| D[Advance lo. Every pair with this lo is too small]
    C -->|Too large| E[Retreat hi. Every pair with this hi is too large]
    C -->|Equal| F[Record the pair and move both, skipping duplicates if you need unique pairs]
    D --> B
    E --> B
```

Sorted numbers 1, 2, 4, 6, 8, 11. Target 10.

| lo | hi | Values | Sum | Move | Why the discarded side is impossible |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 1 and 11 | 12 | hi to 4 | Any pair with 11 is at least 12 |
| 0 | 4 | 1 and 8 | 9 | lo to 1 | Any pair with 1 is at most 9 |
| 1 | 4 | 2 and 8 | 10 | done | The invariant found the unique pair of values |

Each step deletes one index. At most n steps occur. The same table with duplicates, such as 1, 1, 1, 2, needs an extra rule if the problem wants unique pairs: after a hit, advance lo and retreat hi, and keep advancing while the value repeats. The invariant becomes "every unique pair that lives entirely inside the open middle has not been considered, and every unique pair that used a discarded index was already emitted or was impossible."

## Runnable Python

The iterative pair search is the one to memorize. The recursive form is the same invariant with the call stack holding lo and hi. Prefer the loop in an interview. The recursive version makes the shrink obvious when you are teaching the proof.

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return [lo, hi]
        if total < target:
            lo += 1
        else:
            hi -= 1
    return []


def two_sum_sorted_rec(nums: list[int], target: int, lo: int, hi: int) -> list[int]:
    if lo >= hi:
        return []
    total = nums[lo] + nums[hi]
    if total == target:
        return [lo, hi]
    if total < target:
        return two_sum_sorted_rec(nums, target, lo + 1, hi)
    return two_sum_sorted_rec(nums, target, lo, hi - 1)
```

On the dry-run array and target 10, both return indexes 1 and 4. If the problem asks for values, return the values. If several answers exist, the first one this scan finds is the pair with the smallest possible lo among pairs that sum to the target, because lo only increases after all larger partners have been rejected. Say that if the contract asks for any pair, and do not claim a specific pair if you did not prove which one you return.

## Complexity and trade-offs

| Problem shape | Method | Time | Extra space |
| --- | --- | --- | --- |
| Pair sum, already sorted | Opposite ends | Theta(n) | Theta(1) |
| Pair sum, unsorted, need indexes | Hash map | Theta(n) expected | Theta(n) |
| Pair sum, unsorted, constant memory, indexes not required | Sort, then pointers | Theta(n log n) | Theta(1) extra if you may reorder, otherwise Theta(n) |
| Partition into three classes | Dutch flag, three pointers | Theta(n) | Theta(1) |
| Compaction, such as move zeroes | Read and write | Theta(n) | Theta(1) |
| Water trapped | Two running maxima | Theta(n) | Theta(1) |

Sorting just to run two pointers is honest and often optimal when you need a worst-case bound. Hashing is faster on average and uses memory. State the choice. Recursive two pointers use Theta(n) stack in the worst case, which is a pointless cost for this pattern. Use the loop.

## Tricks, tips, and patterns

Write the discard sentence before the code. "If the sum is too small, the left value can never participate." If you cannot finish that sentence, you do not have a two-pointer algorithm yet. Skip duplicates only when the output must be unique. Do it on the side you just used, and do it after you record the answer, not before, or you will skip the only copy you needed. When three pointers partition, draw the regions on paper: processed zeros, processed ones, unknown, processed twos. The unknown region is what shrinks. For palindromes, strip or skip the characters the statement says to ignore before you compare, or skip them inside the scan with a nested move. Do not build a cleaned string unless the interviewer accepts the extra memory.

## Common mistakes and edge cases

Moving both pointers when only one side is guilty. That can skip the only answer. Using two pointers on an unsorted array and hoping. Infinite loops from failing to advance after a swap, especially in the Dutch flag when a 2 is swapped in and you advance mid anyway. Off-by-one on the compacted length: the write pointer is often one past the last kept element, or it is the last kept index. Pick one convention and test it on an array that is already valid and on an array that becomes empty. Integer overflow does not affect Python pair sums. The empty array and the single-element array must return the "not found" value without indexing off the end. For water trapping, a strictly decreasing skyline traps nothing. Test it.

## Interview notes

Start with the invariant, not with "I'll use two pointers." The interviewer wants the reason a pointer may move. Mention sorting cost if you sort. Mention that a hash map is the alternative when indexes matter. Dry-run a four-element example, including a case that forces both directions. If the problem is 3Sum, fix one index and run this pair scan on the suffix. That is n times a linear scan, which is n squared, the standard bound. Skipping duplicates inside both the outer index and the pair scan is part of the contract when unique triplets are required. Say so before you code the continues.

## Practice problems

1. [Two Sum II](/practice/two-sum-ii) — the sorted pair scan.
2. [3Sum](/practice/3sum) — fix one value, then two pointers, with duplicate skips.
3. [Container With Most Water](/practice/container-with-most-water) — advance the shorter line.
4. [Trapping Rain Water](/practice/trapping-rain-water) — running maxima from both ends.
5. [Move Zeroes](/practice/move-zeroes) — read and write pointers.
6. [Sort Colors](/practice/sort-colors) — three pointers. The Dutch flag has its own lesson too.
7. [Valid Palindrome](/practice/valid-palindrome) and [Valid Palindrome II](/practice/valid-palindrome-ii).

## Summary and cheat sheet

- Opposite ends need a monotone discard rule. Sorted pair sums and the water container are the templates.
- Same-direction read and write pointers compact an array in place.
- Three pointers partition into three regions. Do not advance the middle pointer after swapping in an unknown value.
- The invariant names which indexes are already impossible or already correct.
- Each iteration must shrink the unknown region.
- Hash maps beat pointers when the array is unsorted and you need original indexes.
- 3Sum is n outer choices plus this linear scan.

## Further reading

- [Wikipedia — Two pointers technique, discussed inside many articles; start with the Dutch national flag](https://en.wikipedia.org/wiki/Dutch_national_flag_problem)
- [Wikipedia — Two-sum is a standard exercise; see also the sorted-array pair problem in CLRS exercises](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [LeetCode explore cards are not a textbook; prefer the CLRS partitioning chapter](https://en.wikipedia.org/wiki/Quicksort)
'''

WINDOW = r'''
## Why this matters

A sliding window is a contiguous slice whose ends only move forward. It answers questions about subarrays and substrings: the longest substring without a repeated character, the smallest window that covers a pattern, the maximum sum of a fixed length, the number of subarrays whose product is less than a limit. The brute force rebuilds every slice from scratch. The window reuses the previous slice by adding the new right element and removing left elements that no longer belong. That reuse is the difference between quadratic and linear. At this interview level you are expected to know when the window is fixed and when it grows and shrinks, and you are expected to name the state you store so the shrink is fast.

## Intuition

Imagine reading a paragraph with a cardboard frame. You never move the frame backward over characters you have permanently rejected. You widen it to the right when the frame is still valid, and you narrow it from the left when the frame has become invalid or when you are hunting the smallest valid frame. Because both edges move only right, each character enters once and leaves once. Any work you do per entry and per exit, if that work is constant or amortized constant, makes the whole scan linear. The frame's contents are summarized by a counter, a sum, a bitmask, or a deque of candidates, not by the raw slice.

## Core concept in depth

Fixed windows have a constant length k. Compute the first window honestly. Then each step adds the element that enters on the right and subtracts the element that leaves on the left. Maximum sum of a subarray of length k is this update plus a running maximum. The state is a single integer. You need k to be at least 1 and at most n, and you should decide what to return on an empty array before you code.

Variable windows have a predicate that is monotone in the window size for a fixed right endpoint. "No repeated characters" becomes true when you shrink and stays true if you shrink more. "The window contains every required character" becomes false when you shrink past the last extra copy of some character. The canonical loop advances the right endpoint by one, updates the state, then advances the left endpoint while the window violates the condition you care about. For a longest-valid problem, you shrink while the window is invalid, then you record the length. For a shortest-valid problem, you shrink while the window stays valid, and you record the length before each shrink that would still leave it valid. Getting those two whiles backwards is the main bug.

Longest substring without a repeating character stores the last index of each character, or a frequency map. With last indexes, the left endpoint jumps to one past the previous occurrence of the character you just added, but never moves left. The "never move left" part matters when an older duplicate sits outside the current window. With frequencies, you add the right character, then while some frequency is 2 or more you decrement the left character and advance left. Both are linear. The last-index version uses constant extra memory if the alphabet is constant, and it makes the jump obvious.

Minimum window substring stores how many required characters are still missing, plus frequencies of the pattern and of the window. Advance right. When the missing count hits zero, the window is feasible. While it stays feasible, record the length if it is the best, then drop the left character and advance left. A character that appears more times than the pattern needs is slack. Dropping it does not increase the missing count. Dropping a critical character does. The invariant: missing is the number of pattern characters whose window count is still below the pattern count, and every index before left has been rejected as a left endpoint for this right endpoint.

At most k distinct characters, or at most k replacements so that the window becomes one character, uses the same expand-and-shrink loop. For replacements, the state is the frequency map and the count of the most frequent character in the window. The window is valid while its length minus that count is at most k, because those are the cells you must replace. You do not need to decrease the "most frequent" value when you shrink, if you only use it as a historical maximum, but the clean version recomputes or updates carefully. For interviews, a frequency map and a recount of the max when the window is small enough to scan is acceptable only if the alphabet is tiny. With a fixed alphabet of 26, you can recompute the max in constant time.

Sliding-window maximum is the point where a window needs a monotonic deque. The deque stores indexes in increasing position and decreasing value. Before you push the new index, pop the back while it is less than or equal to the new value, because a shorter, smaller candidate can never be the maximum of a future window. Pop the front while it has fallen out of the window. The front is the maximum. Each index is pushed once and popped once, so the whole pass is amortized linear. This structure returns in the stacks module as well, because the deque is a monotonic queue. The window view and the stack view are the same algorithm.

Prefix sums, covered next, answer a different question: the sum of any slice in constant time after a linear preprocess, including slices that are not discovered by a moving frame. If the predicate is not about a contiguous frame you can grow and shrink monotonically, do not force a window. Subarray sum equals k on arrays that may contain negatives is a prefix-and-hash problem, not a two-pointer shrink, because growing the right end can decrease the sum.

## Diagram and dry run

```mermaid
flowchart LR
    A[Advance right by one] --> B[Update the window state]
    B --> C{Window violates the recorded condition?}
    C -->|Yes| D[Advance left and repair the state]
    D --> C
    C -->|No| E[Record length or sum if it improves the answer]
    E --> A
```

Longest substring without repeats on "abba". The map stores the last index.

| Right | Character | Last index seen | Left after the update | Window | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | a | none | 0 | a | 1 |
| 1 | b | none | 0 | ab | 2 |
| 2 | b | 1, which is inside | 2 | b | 2 |
| 3 | a | 0, which is outside the new left | 2 | ba | 2 |

When the second b arrives, left jumps to 2, not to 0. The old a is already outside. The answer is 2. A frequency version would increment b to 2, then shrink from the left through a and the first b until b's frequency is 1. Same windows, more steps, same answer.

## Runnable Python

Both versions of the repeat-free substring are here. The loop is the one to type in an interview. The recursive function on the right endpoint shows the same transition, with the left edge and the map carried along. It uses linear stack space and is only a teaching copy.

```python
def longest_unique(s: str) -> int:
    last: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def longest_unique_rec(s: str) -> int:
    last: dict[str, int] = {}

    def go(right: int, left: int) -> int:
        if right == len(s):
            return 0
        ch = s[right]
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        return max(right - left + 1, go(right + 1, left))

    return go(0, 0)
```

On "abba" both return 2. On an empty string both return 0. On a string of identical characters the answer is 1. On a string of distinct characters the answer is the length.

## Complexity and trade-offs

| Window | State | Time | Extra space |
| --- | --- | --- | --- |
| Fixed length sum | Running sum | Theta(n) | Theta(1) |
| No repeated characters | Last index or frequencies | Theta(n) | Theta(min of n and the alphabet) |
| Minimum window covering a pattern | Two frequency maps and a missing count | Theta(n) | Theta(alphabet) |
| At most k replacements | Frequencies and a max count | Theta(n) | Theta(alphabet) |
| Window maximum | Monotonic deque of indexes | Theta(n) amortized | Theta(k) |

If you rebuild the set of the window from scratch at every right endpoint, you are back to quadratic time. The state update must be constant or amortized constant. Hash maps give expected constant updates. The deque gives amortized constant updates. A balanced tree of the window's values gives a logarithmic window maximum with a worse constant, and it is the right fallback if the "pop smaller backs" argument does not apply because you need the full multiset.

## Tricks, tips, and patterns

Decide longest versus shortest before you write the while loop. Longest: shrink only while invalid, then measure. Shortest: once valid, shrink while you can and measure during the shrink. Left only moves forward. If your code assigns left to something smaller, the last-index formula is wrong. Counts of "still missing" are easier to update than rescanning the pattern. For fixed windows, special-case n less than k. For product windows that must stay under a limit, a zero in the array breaks the product. Restart the window after the zero, or the shrink will divide by zero and will also keep a zero inside a product that can never recover except by leaving it behind.

## Common mistakes and edge cases

Shrinking past a still-valid window in a longest problem, which makes the answer too short. Forgetting that left must not move backward when the previous duplicate is outside the window. Using a set instead of counts when the pattern has duplicate characters, so two a's in the pattern look satisfied by one a in the window. Off-by-one in the length formula right - left + 1. Clearing the whole map when one character repeats, which drops characters that were still unique. For the minimum window, returning 0 and returning an empty string are different contracts. Read the statement. A pattern longer than the text is impossible. A pattern that is empty is a special case you should ask about. It usually matches at index 0 with length 0, or it is excluded by the constraints.

## Interview notes

Say "both ends move only forward, so each index enters and leaves once" before you choose a map. Name the state in one sentence. Dry-run a string where a duplicate sits outside the window, because that is the case buggy last-index code fails. If the interviewer asks for the actual substring rather than the length, store the best left and best length, and slice once at the end. Slicing on every improvement can be quadratic in the cost of copying strings. Mention that negative numbers disqualify the shrink-while-sum-too-large trick, and switch to prefixes. Mention the deque when the window must report a maximum or a minimum, not just a sum or a count.

## Practice problems

1. [Longest Substring Without Repeating Characters](/practice/longest-substring-without-repeating-characters).
2. [Minimum Window Substring](/practice/minimum-window-substring).
3. [Longest Repeating Character Replacement](/practice/longest-repeating-character-replacement).
4. [Permutation in String](/practice/permutation-in-string) and [Find All Anagrams](/practice/find-all-anagrams-in-a-string) — fixed windows compared by counts.
5. [Sliding Window Maximum](/practice/sliding-window-maximum).
6. [Minimum Size Subarray Sum](/practice/minimum-size-subarray-sum) — shortest window with sum at least the target, for non-negative numbers.
7. [Fruit Into Baskets](/practice/fruit-into-baskets) and [Max Consecutive Ones III](/practice/max-consecutive-ones-iii).

## Summary and cheat sheet

- A window is a contiguous slice. Both ends move forward. Each index enters and leaves once.
- Fixed length: add the newcomer, remove the exile, update the answer.
- Variable longest: expand, shrink while invalid, then measure.
- Variable shortest: expand until valid, shrink while valid, measure during the shrink.
- State is a count, a sum, a last index, or a monotonic deque. Rebuilding the slice is quadratic.
- Negatives break sum-shrinking. Use a prefix map instead.
- Length is right - left + 1.

## Further reading

- [Wikipedia — Streaming algorithm, for the one-pass mindset](https://en.wikipedia.org/wiki/Streaming_algorithm)
- [Wikipedia — Double-ended queue](https://en.wikipedia.org/wiki/Double-ended_queue)
- [CP-Algorithms, two pointers](https://cp-algorithms.com/others/two-pointers.html)
'''

emit(
    "02-arrays-strings",
    "01-two-pointers.mdx",
    title="Two Pointers",
    slug="two-pointers",
    summary="Opposite-end and same-direction scans, the discard invariant, and the three-pointer partition.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["interview-approach-guide"],
    tags=["two-pointers", "arrays", "strings"],
    order=1,
    body=TWO,
)
emit(
    "02-arrays-strings",
    "02-sliding-window.mdx",
    title="Sliding Windows",
    slug="sliding-window",
    summary="Fixed and variable windows, the expand-and-shrink invariant, and the monotonic deque for window maxima.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["two-pointers"],
    tags=["sliding-window", "arrays", "strings"],
    order=2,
    body=WINDOW,
)
