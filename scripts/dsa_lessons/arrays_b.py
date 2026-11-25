"""Prefix sums, Kadane, Dutch flag, Boyer-Moore, and intervals."""

from emit import emit

PREFIX = r'''
## Why this matters

Many subarray questions look quadratic because there are quadratically many slices, and then turn linear once you notice that adjacent slices share a sum. A prefix array stores those shared sums. A one-pass recurrence stores only the best slice that ends at the current index. Together they cover range-sum queries, subarray sum equals k, equilibrium indexes, circular maximum sums, and the classic maximum subarray. Interviewers use them as a filter. If you recompute every slice from scratch on an input of size 10 to the 5th, the solution does not fit. If you can point at the repeated addition and replace it with a prefix or with Kadane's variables, it does.

## Intuition

A prefix sum is a running total written down. The sum from index l through r is the total up to r minus the total before l. You paid linear time once, and every later question is a subtraction. Kadane's algorithm is what you do when you do not want every slice, only the best one. At each index the best slice that ends here either starts here, because everything before it was a burden, or it extends the best slice that ended on the previous index. There is no third option. That observation deletes the quadratic search.

## Core concept in depth

Define prefix[0] = 0 and prefix[i + 1] = prefix[i] + nums[i]. Then the sum of nums[l] + ... + nums[r] equals prefix[r + 1] - prefix[l]. The empty prefix makes the left boundary painless: a slice that starts at 0 subtracts zero. Building the prefix is Theta(n) time and Theta(n) memory. If you only need one range you do not need the array at all, but the array is the right tool when many ranges are asked, or when a later algorithm looks up earlier prefixes.

Subarray sum equals k, on arrays that may contain negative numbers, cannot shrink a window, because extending the right end can make the sum fall. Rewrite the condition. The slice from l to r sums to k exactly when prefix[r + 1] - prefix[l] = k, which means prefix[l] = prefix[r + 1] - k. Walk the array once, and keep a map from every prefix sum seen so far to the number of times it occurred. At the current prefix, add the count of prefix - k. Then record the current prefix. The order matters: you must count before you record, and the map starts with 0 seen once, so a slice from the beginning is visible. The same idea modulo m answers subarray sums divisible by m. Store prefix modulo m, and ask for the same residue. Negative numbers modulo m need a non-negative residue. In Python the remainder operator already does that for a positive modulus.

An equilibrium index, or pivot index, is the place where the sum strictly to the left equals the sum strictly to the right. The total sum makes this a constant-time check per index: left sum is the prefix before i, right sum is total - prefix[i + 1]. One pass computes the total, a second pass finds the index. You can also maintain the left sum as you go and derive the right sum from the total.

Kadane's algorithm finds the maximum sum of a non-empty contiguous subarray. Let best_end be the best sum of a slice that ends at the current index, and best the best sum seen anywhere. For each value, best_end becomes the maximum of value and best_end + value. Then best becomes the maximum of best and best_end. Initialize best_end to 0 only if an empty slice is allowed. For a non-empty slice, initialize best and best_end to the first element and start the loop at the second element, otherwise an all-negative array incorrectly returns 0. The proof is a short case split. Any optimal slice ends somewhere. Among slices that end at i, the best one is nums[i] alone or the best slice ending at i - 1 plus nums[i], because if the best slice ending at i - 1 had a negative sum you would have dropped it. Taking the maximum over ending positions finishes the proof.

The circular maximum subarray is the maximum of two candidates: the ordinary Kadane answer, and the total sum minus the minimum non-empty subarray, which represents wrapping around the ends. The minimum subarray is Kadane on the negated array, or the same recurrence with min instead of max. If the entire array is the minimum, wrapping would choose an empty middle and an empty answer. When every element is negative, or more carefully when the minimum subarray is the whole array, the wrap candidate is 0 or empty and you must keep the ordinary answer. The safe test is: if the wrap sum equals the total, ignore it.

Maximum product subarray needs two running values, because a negative number swaps the roles of min and max. Keep the maximum and minimum product ending here. A new value updates both from the set of candidates: the value itself, max_end times the value, and min_end times the value. Zeros reset both to the value 0, and the next element starts fresh because the recurrence takes the value alone.

These recurrences are dynamic programming on a line. The state is "best ending here," and the transition looks one step back. You do not need a table if the older states are never read again. That is why Kadane uses a handful of variables. The prefix array is the version you keep when later indexes must look up arbitrary earlier prefixes, not only the previous one.

## Diagram and dry run

```mermaid
flowchart TD
    A[Value x at this index] --> B{Extend the previous slice or start over?}
    B -->|Previous sum helps| C[best ending becomes previous plus x]
    B -->|Previous sum hurts| D[best ending becomes x]
    C --> E[Global best is the max of itself and best ending]
    D --> E
```

Array -2, 1, -3, 4, -1, 2, 1, -5, 4. Non-empty Kadane.

| Index | Value | Best ending here | Global best | Slice that best ending represents |
| --- | --- | --- | --- | --- |
| 0 | -2 | -2 | -2 | just -2 |
| 1 | 1 | 1 | 1 | start over at 1 |
| 2 | -3 | -2 | 1 | 1 plus -3, still worse than 1 |
| 3 | 4 | 4 | 4 | start over at 4 |
| 4 | -1 | 3 | 4 | 4, -1 |
| 5 | 2 | 5 | 5 | 4, -1, 2 |
| 6 | 1 | 6 | 6 | 4, -1, 2, 1 |
| 7 | -5 | 1 | 6 | extended, but the global stays 6 |
| 8 | 4 | 5 | 6 | not better |

The answer is 6, the slice 4, -1, 2, 1. A prefix check for sum equals 3 would see prefix values 0, -2, -1, -4, 0, -1, 1, 2, -3, 1. The pair of prefixes that differ by 3 includes  -1 and -4, and also 1 and -2, among others.

## Runnable Python

The iterative Kadane is the interview version. The recursive function returns the pair "best ending at this suffix start, best anywhere in the suffix" and walks from the right. It is the same recurrence, with Theta(n) stack, useful as a proof and a poor implementation. Prefer the loop.

```python
def max_subarray(nums: list[int]) -> int:
    best = best_end = nums[0]
    for value in nums[1:]:
        best_end = max(value, best_end + value)
        best = max(best, best_end)
    return best


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """prefix[i] is the sum of the first i elements. right is inclusive."""
    return prefix[right + 1] - prefix[left]


def max_subarray_rec(nums: list[int]) -> int:
    def go(i: int) -> tuple[int, int]:
        if i == len(nums) - 1:
            return nums[i], nums[i]
        end_after, best_after = go(i + 1)
        end_here = max(nums[i], nums[i] + end_after)
        return end_here, max(end_here, best_after)
    return go(0)[1]
```

`max_subarray` on the dry-run array returns 6. `range_sum` on a prefix built from 1, 2, 3, 4 answers the slice from index 1 through 3 as 9. Build that prefix with a running total pushed onto a list that starts with 0.

## Complexity and trade-offs

| Task | Method | Time | Extra space |
| --- | --- | --- | --- |
| One range sum | Direct loop | Theta(length) | Theta(1) |
| Many range sums | Prefix array | Theta(n + queries) | Theta(n) |
| Subarray sum equals k, negatives allowed | Prefix map | Theta(n) expected | Theta(n) |
| Subarray sum equals k, non-negative | Sliding window | Theta(n) | Theta(1) |
| Maximum subarray | Kadane | Theta(n) | Theta(1) |
| Maximum circular subarray | Kadane plus a minimum subarray | Theta(n) | Theta(1) |
| Maximum product | Two running products | Theta(n) | Theta(1) |

A segment tree or a Fenwick tree answers range sums with updates. The prefix array does not. If the interview adds "and then we change elements," say that the prefix would be rebuilt and offer a tree. That structure is taught with trees. Do not reach for it on a static array.

## Tricks, tips, and patterns

Start the prefix with 0. Count a complement before inserting the current prefix. For modulo, normalize the residue into 0 through m - 1. Initialize Kadane from the first element when the slice must be non-empty. For the circular case, reject the wrap that consumes the entire array. For products, a zero splits the array into independent segments, and the two-running-product recurrence handles that without an explicit split. If you need the slice itself and not only the sum, remember the start index. Reset it when you start over, and remember the best start and best end when the global best improves.

## Common mistakes and edge cases

Returning 0 for an all-negative array. Forgetting the initial 0 in the prefix map, so slices that start at index 0 are invisible. Inserting the prefix before counting, so a slice of length 0 looks like a hit when k is 0. Using a window shrink on negative numbers. Off-by-one between a prefix that stores n values and a prefix that stores n + 1 values. Mixing inclusive and exclusive ends in the subtraction. For the circular problem, double-counting the whole array. For the product problem, ignoring the sign and tracking only the maximum. Empty input: Kadane on an empty list should be rejected by the constraints or defined up front. Do not index nums[0] without checking.

## Interview notes

Say the identity "slice sum equals prefix right minus prefix left" before you write a map. Say "best ending here is either the element or the element plus best ending on the left" before you write Kadane. Dry-run an array that contains a negative number between two positive runs, because that is where "start over" happens. Mention expected linear time for the hash map. Mention that non-negative sums can stay in the sliding-window lesson and use constant memory. If the interviewer asks for the indexes, store them. The sum alone is a weaker answer than the one the statement requested.

## Practice problems

1. [Maximum Subarray](/practice/maximum-subarray) — Kadane.
2. [Maximum Sum Circular Subarray](/practice/maximum-sum-circular-subarray).
3. [Maximum Product Subarray](/practice/maximum-product-subarray).
4. [Subarray Sum Equals K](/practice/subarray-sum-equals-k).
5. [Continuous Subarray Sum](/practice/continuous-subarray-sum) and [Subarray Sums Divisible by K](/practice/subarray-sums-divisible-by-k).
6. [Find Pivot Index](/practice/find-pivot-index).
7. [Product of Array Except Self](/practice/product-of-array-except-self) — a prefix product and a suffix product, the same idea with multiplication.

## Summary and cheat sheet

- prefix[i] is the sum of the first i elements. A slice is a subtraction.
- Seed the prefix map with 0 seen once. Query prefix - k before you insert prefix.
- Modulo residues must be non-negative. The same residue means the slice between them is divisible.
- Kadane: best ending here is max of the value and the value plus the previous best ending.
- Initialize from the first element when the slice cannot be empty.
- Circular answer: max of the straight Kadane and total minus the minimum subarray, unless that minimum is everything.
- Products track both ends because a negative swaps them.

## Further reading

- [Wikipedia — Prefix sum](https://en.wikipedia.org/wiki/Prefix_sum)
- [Wikipedia — Maximum subarray problem](https://en.wikipedia.org/wiki/Maximum_subarray_problem)
- [CP-Algorithms, prefix sums](https://cp-algorithms.com/data_structures/prefix_sum.html)
'''

INTERVALS = r'''
## Why this matters

Partitioning, majority votes, and interval scheduling look unrelated until you see that each one is a linear or linearithmic scan with a tiny state and a sharp invariant. The Dutch national flag partitions an array into three bands in one pass. Boyer-Moore finds a majority element with constant memory. Interval problems become greedy once you sort by the right endpoint or sweep a timeline. These show up constantly in onsite rounds because the code is short and the proof is the part candidates skip. This lesson is the proof.

## Intuition

The Dutch flag is three labeled bins and one unknown stretch. You only ever look at the left edge of the unknown stretch, and you push that element into the bin it belongs to. Boyer-Moore is a duel. Different values cancel. If one value occupies more than half the seats, it cannot be cancelled completely, so the survivor of the duel is the only possible majority. You still count it at the end if the problem does not promise that a majority exists. Intervals are a calendar. If you sort meetings by the time they finish, the meeting that frees the room first is the one that leaves the most room for whoever remains. That is the exchange argument behind the classic scheduling greedy.

## Core concept in depth

Sort Colors, the Dutch national flag, partitions values that are only 0, 1, or 2. Maintain three regions on the array: indexes below lo hold 0, indexes from lo up to but not including mid hold 1, indexes above hi hold 2, and the rest is unknown. Start with lo = 0, mid = 0, hi = n - 1. While mid is at most hi, look at nums[mid]. A 0 swaps with nums[lo], and both lo and mid advance, because the value swapped into mid came from the 0 region and is known. A 1 only advances mid. A 2 swaps with nums[hi] and hi retreats, and mid stays, because the value that arrived from hi is unknown. The loop ends when mid passes hi. Every element was examined, and no element was examined twice except a value swapped in from the right, which is then classified. The invariant implies the array is sorted.

Boyer-Moore majority vote maintains a candidate and a counter, both starting empty. For each value, if the counter is 0, adopt the value as the candidate and set the counter to 1. Otherwise increment when the value matches and decrement when it does not. Pairs of different values cancel. Suppose a majority value m occurs more than n/2 times. Every cancellation consumes at most one copy of m along with something else. The copies of m cannot all be consumed, so the final candidate is m. If the statement does not promise a majority, run a second linear count and accept the candidate only when its count exceeds n/2. Majority Element II asks for every value that occurs more than n/3 times. There are at most two such values. Keep two candidates and two counters. A new value that matches neither decrements both. The same cancellation argument applies, and a second pass verifies both survivors. Do not emit a candidate that fell to a count of 0 and was never replaced, and do not emit duplicates.

Merge Intervals sorts by start time. Sweep left to right, and keep the current merged segment. If the next interval starts after the current end, flush the current segment and start a new one. If it overlaps or touches, extend the current end to the maximum of the two ends. Touching endpoints merge when the problem treats intervals as closed. Ask. The sweep is correct because any interval that could have merged with an earlier flushed segment would start no later than that segment's end, and sorting by start makes that impossible. Insert Interval is the same sweep with one extra interval that you fold in when its start time comes due. You can also binary-search the insertion point and then merge only the local run. Both are fine. The linear merge after the sort or the insertion is the clear version.

Non-overlapping intervals, the minimum number of intervals to remove, sorts by end time. Take the interval that ends first. Remove every later interval that overlaps it, which means every later interval that starts before this end. Then repeat. Equivalently, keep a count of how many you are able to keep: if the next interval starts at or after the last kept end, keep it and move the end. The number removed is n minus the number kept. The exchange argument: some optimal solution keeps an interval that ends first among the remaining set, because if it kept a different one you could swap in the earlier-finishing interval without creating a new overlap. That is why sorting by end, not by start, is the right order for "how many can I keep." Sorting by start is the right order for "merge what overlaps."

Meeting Rooms asks whether any two overlap. Sort by start and compare each end with the next start. Meeting Rooms II asks for the number of rooms, which is the maximum number of meetings open at once. A sweep stores events: plus one at each start, minus one at each end. Sort events, and process ends before starts when times tie if a meeting that ends at t frees the room for a meeting that starts at t. A min-heap of end times does the same job. Push the first meeting. For each later meeting in start order, if the earliest ending meeting is done, pop it. Push the current end. The heap size is the number of rooms in use, and the maximum size is the answer.

Minimum arrows to burst balloons is the non-overlapping problem in costume. Sort by end, shoot at the end of the first balloon, and skip every balloon that contains that x-coordinate. Each shot is one arrow. Partition labels, the places a string must be cut so that each letter lives in one part, is an interval problem too. Each letter occupies an interval from its first index to its last. The cuts are the points where a sweep of those intervals returns to zero open intervals.

## Diagram and dry run

```mermaid
flowchart TD
    A[mid looks at an unknown value] --> B{Value}
    B -->|0| C[Swap with lo. Advance lo and mid]
    B -->|1| D[Advance mid only]
    B -->|2| E[Swap with hi. Retreat hi. Do not advance mid]
    C --> A
    D --> A
    E --> A
```

Dutch flag on 2, 0, 2, 1, 1, 0. Start lo = 0, mid = 0, hi = 5.

| Array | lo | mid | hi | Action |
| --- | --- | --- | --- | --- |
| 2 0 2 1 1 0 | 0 | 0 | 5 | See 2. Swap with hi. |
| 0 0 2 1 1 2 | 0 | 0 | 4 | See 0. Swap with lo. Advance both. |
| 0 0 2 1 1 2 | 1 | 1 | 4 | See 0. Swap with lo. Advance both. |
| 0 0 2 1 1 2 | 2 | 2 | 4 | See 2. Swap with hi. |
| 0 0 1 1 2 2 | 2 | 2 | 3 | See 1. Advance mid. |
| 0 0 1 1 2 2 | 2 | 3 | 3 | See 1. Advance mid. mid passes hi. |

Boyer-Moore on 2, 2, 1, 1, 1, 2, 2. The candidate finishes as 2, and a verification count confirms it. Cancel the trace on paper: 2 versus 1 cancels, another 2 versus 1 cancels, and the extra 2s remain.

## Runnable Python

The flag is iterative. A recursive partition would only hide the same swaps in the stack. Boyer-Moore is a loop plus a verification loop. Both are the versions to write from memory.

```python
def sort_colors(nums: list[int]) -> list[int]:
    lo = mid = 0
    hi = len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[hi], nums[mid] = nums[mid], nums[hi]
            hi -= 1
    return nums


def majority(nums: list[int]) -> int:
    candidate = count = 0
    for value in nums:
        if count == 0:
            candidate = value
        count += 1 if value == candidate else -1
    if sum(value == candidate for value in nums) * 2 > len(nums):
        return candidate
    return -1
```

The flag returns the partitioned list. `majority` returns the majority value or -1 when the promise is absent. The comparison `* 2 > len` avoids a trick with integer division and states "more than half" directly.

## Complexity and trade-offs

| Algorithm | Time | Extra space | Needs a promise? |
| --- | --- | --- | --- |
| Dutch flag | Theta(n) | Theta(1) | Values are only 0, 1, 2 |
| Counting sort of three values | Theta(n) | Theta(1) | Same, and you may write a second pass from counts |
| Boyer-Moore plus verify | Theta(n) | Theta(1) | Verification required unless a majority is guaranteed |
| Hash counts | Theta(n) expected | Theta(n) | No |
| Merge intervals | Theta(n log n) | Theta(n) for the output | Closed versus open must be known |
| Keep non-overlapping, sort by end | Theta(n log n) | Theta(1) extra beyond the sort | The objective is the maximum number kept |
| Meeting rooms II, sweep | Theta(n log n) | Theta(n) | Tie-breaking of equal timestamps |

Counting sort is simpler than the flag when you may overwrite the array from three counters. The flag is the one to use when the interviewer asks for one pass and constant memory and wants the swaps. A heap for meeting rooms is Theta(n log n) as well. The sweep is usually less code once the tie break is clear.

## Tricks, tips, and patterns

Draw the regions before you write the flag. The unknown value that arrives from the right is not classified. Sort intervals by the key that matches the exchange argument: start time to merge, end time to schedule. Process ends before starts at the same timestamp when a room can be reused immediately. For Boyer-Moore, always know whether you must verify. For two candidates, write the second pass, and remember that a count of zero means "no candidate," not "the value zero," so keep a separate flag or use an optional candidate. Partition labels and burst balloons are the same sweep as non-overlapping intervals once you build the intervals.

## Common mistakes and edge cases

Advancing mid after a swap with hi. The invariant breaks and a 2 can hide in the middle. Using a strict less-than in the flag loop so the last unknown element is skipped. Treating a half-frequency element as a majority. Integer division of n/2 is the right threshold only when you compare the count to it carefully: more than n/2 means the count is at least floor(n/2) + 1. Forgetting to verify. Merging intervals that merely touch when the problem says overlap must be a positive-length intersection, or failing to merge them when touching counts. Sorting scheduling problems by start and then being unable to prove the greedy choice. Dropping the tie break in the room sweep so a meeting that ends at time t looks like it still occupies a room that a new meeting needs at t.

## Interview notes

For the flag, state the four regions, including the unknown one, and then code the three cases. Dry-run a single swap of a 2 from the front. For Boyer-Moore, explain cancellation before the loop, and say the second pass out loud even if you are sure a majority exists, so the interviewer knows you know the hypothesis. For intervals, say which endpoint you sort by and why, in one sentence, before you sort. If you cannot say why, you have a 50 percent chance of sorting by the wrong end. Offer the heap and the sweep as equivalent for meeting rooms, and pick the one you can implement cleanly.

## Practice problems

1. [Sort Colors](/practice/sort-colors).
2. [Majority Element](/practice/majority-element) and [Majority Element II](/practice/majority-element-ii).
3. [Merge Intervals](/practice/merge-intervals) and [Insert Interval](/practice/insert-interval).
4. [Non-overlapping Intervals](/practice/non-overlapping-intervals).
5. [Meeting Rooms](/practice/meeting-rooms) and [Meeting Rooms II](/practice/meeting-rooms-ii).
6. [Minimum Number of Arrows](/practice/minimum-number-of-arrows-to-burst-balloons) and [Partition Labels](/practice/partition-labels).

## Summary and cheat sheet

- Dutch flag regions: 0s, then 1s, then unknown, then 2s. Do not classify the value that arrives from the right until the next loop.
- Boyer-Moore cancels different values. The majority survives. Verify unless the problem promises.
- At most two values can exceed n/3. Keep two candidates and verify both.
- Merge: sort by start, extend the current end.
- Schedule: sort by end, keep a meeting when it starts after the last kept end.
- Rooms: sweep plus one and minus one, or a heap of end times. Ends free a room before starts reuse it at the same timestamp.

## Further reading

- [Wikipedia — Dutch national flag problem](https://en.wikipedia.org/wiki/Dutch_national_flag_problem)
- [Wikipedia — Boyer-Moore majority vote algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm)
- [Wikipedia — Interval scheduling](https://en.wikipedia.org/wiki/Interval_scheduling)
- [CP-Algorithms, scheduling jobs](https://cp-algorithms.com/schedules/schedule-with-completion-duration.html)
'''

emit(
    "02-arrays-strings",
    "03-prefix-sums-and-kadane.mdx",
    title="Prefix Sums and Kadane's Algorithm",
    slug="prefix-sums-and-kadane",
    summary="Range sums, the prefix-hash identity for subarray sums, and the one-pass recurrences for maximum sum and product.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["sliding-window"],
    tags=["prefix-sums", "kadane", "arrays"],
    order=3,
    body=PREFIX,
)
emit(
    "02-arrays-strings",
    "04-partitions-majority-and-intervals.mdx",
    title="Dutch Flag, Boyer-Moore, and Intervals",
    slug="partitions-majority-and-intervals",
    summary="Three-way partition, constant-space majority voting, and the sort order that makes interval greedy proofs work.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["prefix-sums-and-kadane"],
    tags=["dutch-flag", "boyer-moore", "intervals"],
    order=4,
    body=INTERVALS,
)
