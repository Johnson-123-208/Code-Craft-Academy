"""Binary search variants, classic sorts, and Timsort."""

from emit import emit

BINARY = r'''
## Why this matters

Binary search is the algorithm people say they know and then write with an infinite loop. The idea is small. The boundary conditions are not. Once the loop is solid, a family of interview problems opens: first and last occurrence, search in a rotated array, peak finding, and binary search on the answer. The last of those is a pattern, not a library function. You binary-search a threshold when "can I achieve this limit?" is monotone. Koko eating bananas, shipping packages within D days, and splitting an array into k subarrays are the same function with a different feasibility test.

## Intuition

A sorted array is a dictionary. You open the middle. If the word is too far back in the alphabet, you throw away the right half, including the middle you just read when it is not the target. Each question halves the remaining pages, so a million pages costs about twenty questions. The same halving works on a numeric answer space. If a capacity is enough to ship every package on time, every larger capacity is enough. If it is not enough, every smaller capacity fails. You can discard half the capacities per test.

## Core concept in depth

The iterative search maintains an inclusive range lo, hi of indexes that might still hold the target. While lo is at most hi, the mid index is the average, rounded down. If nums[mid] is the target, return it. If the middle value is smaller, the target can only sit strictly to the right, so lo becomes mid + 1. Otherwise hi becomes mid - 1. When the loop ends, the range is empty and the target is absent. The invariant: every index outside lo through hi has been proved not to hold the target. Termination: the range shrinks, because mid is inside the range and is excluded. That is why `hi = mid` without excluding mid, on an inclusive range, can loop forever when lo and hi are neighbors. Pick one convention and stick to it. The half-open convention, lo inclusive and hi exclusive, uses `while lo < hi` and sets hi = mid when the middle is too large. Both conventions work. Mixing them does not.

Lower bound is the first index whose value is at least the target. Upper bound is the first index whose value is strictly greater. First and last occurrence of a target are the lower bound of the target, and the lower bound of the target plus one, minus one. If the lower bound falls off the array or the value there is not the target, the target is absent and the answer is the pair of sentinels. Implement lower bound once and call it twice. A single search that "finds any match and scans outward" is correct and linear in the size of the equal run, which can be the whole array.

A rotated sorted array is two sorted runs. At mid, one of the halves is sorted. If the left half is sorted and the target lies inside it, move left. Otherwise move right. The symmetric test handles a sorted right half. Duplicates break the "one half is sorted" test when nums[lo], nums[mid], and nums[hi] are equal. Then you can only shrink by one, and the worst case becomes linear. The problem without duplicates stays logarithmic. Finding the minimum in a rotated array is the same split: the minimum lies in the unsorted half, which is the half that contains the rotation.

A peak element is strictly greater than its neighbors, with the edges having one neighbor. On a line, if the middle is less than its right neighbor, a peak exists to the right, because the sequence eventually has to stop rising. Otherwise a peak exists at the middle or to the left. Any peak is acceptable in the usual statement, so you do not hunt for the global maximum. The binary search still works. Prove the existence claim. It is the whole correctness argument.

Binary search on the answer needs a monotone predicate feasible(x). Find the smallest x in a range where feasible is true, or the largest where it is true. The range must bracket the answer. For Koko, the low end is 1 and the high end is the largest pile, because eating at least one banana per hour is required and eating the largest pile in one hour always finishes. feasible(speed) computes the hours as the sum of ceil(pile / speed) and compares with the limit. For shipping, the low end is the heaviest package and the high end is the sum. feasible(capacity) is the greedy left-to-right packing. For splitting an array so the largest sum is minimized, the same packing test is the predicate. If feasible(mid) holds, try a smaller answer. Otherwise try a larger one. The loop ends on the boundary. Off-by-one here returns a capacity that is one short of feasible. Test the predicate on the returned value.

The recursive form passes lo and hi and returns the index. It uses logarithmic stack. The loop is preferred. Both must share the invariant. Integer midpoint in a language with fixed-width integers should be computed as lo + (hi - lo) // 2 to avoid overflow. Python integers do not overflow. The safer formula is still a good habit when you write Java or C++ later.

## Diagram and dry run

```mermaid
flowchart TD
    A[Inclusive range lo to hi] --> B{lo at most hi?}
    B -->|No| C[Absent]
    B -->|Yes| D[mid is the midpoint]
    D --> E{Compare nums at mid with the target}
    E -->|Equal| F[Found]
    E -->|Middle too small| G[lo becomes mid plus 1]
    E -->|Middle too large| H[hi becomes mid minus 1]
    G --> A
    H --> A
```

Search for 8 in 1, 3, 4, 8, 9, 12.

| lo | hi | mid | Value | Move |
| --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 4 | too small, lo = 3 |
| 3 | 5 | 4 | 9 | too large, hi = 3 |
| 3 | 3 | 3 | 8 | found |

Lower bound of 8 is index 3. Lower bound of 5 is also index 3, the first value at least 5, which is 8. Lower bound of 13 is 6, one past the end, meaning every element is smaller.

Koko, piles 3, 6, 7, 11, limit 8 hours. Speed 4 takes ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8, which is feasible. Speed 3 takes 1+2+3+4 = 10, which is not. The minimum feasible speed is 4.

## Runnable Python

Lower bound is the primitive. The answer-search wrapper takes a feasibility function. Both are iterative. The recursive classic search is the teaching twin.

```python
def lower_bound(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search_rec(nums: list[int], target: int, lo: int, hi: int) -> int:
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        return binary_search_rec(nums, target, mid + 1, hi)
    return binary_search_rec(nums, target, lo, mid - 1)


def smallest_feasible(lo: int, hi: int, feasible) -> int:
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

`lower_bound` on 1, 3, 4, 8, 9, 12 for target 8 returns 3. The half-open range starts with hi = n, not n - 1. `smallest_feasible` requires that once feasible becomes true it stays true, and that hi itself is feasible so the loop has an answer to land on.

## Complexity and trade-offs

| Search | Time | Extra space | Requirement |
| --- | --- | --- | --- |
| Classic, iterative | Theta(log n) | Theta(1) | Sorted, random access |
| Classic, recursive | Theta(log n) | Theta(log n) stack | Same |
| First and last position | Theta(log n) | Theta(1) | Two lower bounds |
| Rotated, distinct | Theta(log n) | Theta(1) | One half is sorted |
| Rotated, duplicates | O(n) worst | Theta(1) | Equal ends force a shrink by one |
| Answer search | Theta(log R times cost of feasible) | whatever feasible uses | Monotone predicate |

A hash set finds one element in expected constant time and does not find a lower bound, a predecessor, or a feasible threshold. A balanced tree does all of those in logarithmic time and supports inserts. Binary search on a static array is the lightest tool that fits. On a linked list, binary search is a bad idea: reaching the middle is already linear, and the total becomes linearithmic with a worse constant than a straight scan.

## Tricks, tips, and patterns

Write the invariant beside the loop. Decide inclusive or half-open before the first comparison. For answer search, write feasible() as its own function and test it on one value you computed by hand. The search is useless if feasible is wrong. When the predicate is "largest x that still works," flip the branch: if feasible, move lo up past mid, and be careful with the midpoint bias so the range still shrinks. A simple alternative is to search for the smallest value that fails and subtract one. Prefer that if it keeps the loop in the shape you trust.

## Common mistakes and edge cases

Infinite loop from not excluding mid. Returning mid when you wanted a lower bound and the middle merely equals some later duplicate. Empty array. Single element. Target smaller than every element, and larger than every element. Rotated array that is not actually rotated. Duplicates in a rotated array. Feasibility that is not monotone, so binary search returns nonsense. Using integer division for ceil(pile / speed) in a way that rounds the wrong direction. In Python, ceil of a positive division is `(pile + speed - 1) // speed`. A zero speed is excluded by starting lo at 1. Overflow of the answer range: the high end must be feasible. If you set it too low, the algorithm confidently returns an infeasible value.

## Interview notes

Say the invariant. Say which convention you use. Dry-run three steps, including a miss if you have time. For a rotated array, say "one side is sorted, and I test membership on that side." For answer search, say the monotone sentence before the loop, and name lo and hi in terms of the problem, not as magic indexes. Test feasible on the boundaries out loud. Mention that the cost is logarithmic in the answer range times a linear feasibility scan, which is n log R, and check it against the constraints.

## Practice problems

1. [Binary Search](/practice/binary-search) and [Search Insert Position](/practice/search-insert-position).
2. [Find First and Last Position](/practice/find-first-and-last-position).
3. [Search in Rotated Sorted Array](/practice/search-in-rotated-sorted-array) and [Find Minimum in Rotated Sorted Array](/practice/find-minimum-in-rotated-sorted-array).
4. [Find Peak Element](/practice/find-peak-element).
5. [Koko Eating Bananas](/practice/koko-eating-bananas), [Capacity to Ship Packages](/practice/capacity-to-ship-packages-within-d-days), and [Split Array Largest Sum](/practice/split-array-largest-sum).
6. [Sqrt(x)](/practice/sqrtx) — binary search the integer square root.

## Summary and cheat sheet

- Halve an inclusive range by excluding mid. Or use a half-open range and `while lo < hi`.
- Lower bound is the first index at least the target. Last occurrence is the lower bound of target + 1, minus one.
- In a rotated array, one half is sorted. Test the target against that half.
- A peak exists on the side that is still rising.
- Answer search needs a monotone feasible(x) and a bracket that contains a true value.
- The loop is Theta(log of the range). Multiply by the cost of one test.
- Linked lists do not give you random access. Do not binary-search them.

## Further reading

- [Wikipedia — Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)
- [Wikipedia — Lower and upper bounds, the insertion-point view](https://en.wikipedia.org/wiki/Binary_search_algorithm#Procedure_for_finding_the_leftmost_element)
- [CP-Algorithms, binary search](https://cp-algorithms.com/num_methods/binary_search.html)
'''

SORTS = r'''
## Why this matters

Sorting is the reduction that makes later linear scans possible: two pointers, interval sweeps, binary search, and duplicate grouping. You are expected to know a quadratic sort well enough to explain why it is quadratic, a correct O(n log n) sort well enough to code under pressure, and the comparison lower bound that says you cannot comparison-sort arbitrary objects any faster than n log n in the worst case. Stability matters when the key is only part of the record. Timsort, in the next lesson, is what Python actually runs. This lesson is the family it was built from.

## Intuition

A comparison sort learns the order by asking "is this element less than that one?" Each answer has two outcomes, so k questions distinguish at most 2 to the k possible answers. There are n! possible orders. Therefore k must be at least log2 of n!, which Stirling's approximation puts at about n log n. Merge sort and heapsort meet that bound in the worst case. Quicksort meets it on average and can be made very likely to meet it with random pivots. Insertion sort does not meet it, and yet it is the fastest sort in the room when the array is already nearly sorted, because it only pays for the inversions that exist.

## Core concept in depth

Selection sort finds the minimum of the unsorted suffix and swaps it into place. It does about n squared / 2 comparisons whether the array is sorted or not. It is in-place and not stable unless you shift instead of swapping, which makes it slower. Bubble sort swaps adjacent inversions. Its best case can be linear if you stop when a pass swaps nothing. Its worst case is quadratic. Neither algorithm is a final answer on a large array. Both are the right answer to "what does quadratic look like?"

Insertion sort keeps a sorted prefix. It inserts the next element by shifting larger prefix elements one step right. The inner loop stops early when the prefix is already in order. On a sorted array the cost is Theta(n). On a reversed array it is Theta(n squared). The precise cost is Theta(n + I) where I is the number of inversions, pairs that are out of order. It is stable if you only shift strictly greater elements, so equal keys keep their original order. It is the sort you use for tiny n, and it is the base case of better sorts.

Merge sort splits, sorts both halves, and merges. The merge walks two sorted lists and writes the smaller head, and it is stable if you take from the left half when the keys are equal. The recurrence is T(n) = 2 T(n/2) + Theta(n), which is Theta(n log n) in every case, not only the average. The extra memory for the merge buffer is Theta(n). Linked-list merge sort needs no random access and can reuse nodes, which is why sorting a linked list is merge sort. Bottom-up merge sort iterates width 1, 2, 4, and so on, and removes the recursion. The same bound holds.

Quicksort picks a pivot, partitions the array into "less than the pivot" and "greater than the pivot," and sorts the sides. Partition is the Dutch-flag idea restricted to two bands, or three if you isolate equals. Lomuto's partition is simple and degrades on duplicates. Hoare's partition uses two pointers walking inward and does fewer swaps. The average time, with a decent pivot, is Theta(n log n). The worst case, always pivoting the extreme element, is Theta(n squared), and the recursion depth is linear. Randomized quicksort picks the pivot uniformly. Its expected time is Theta(n log n) for every input. The worst case is still possible and vanishingly unlikely. Introsort, used by several standard libraries, switches to heapsort when the depth gets too large, so the worst case becomes n log n. Quicksort is typically in-place and unstable.

Heapsort builds a max-heap and repeatedly extracts the maximum into the end of the array. It is Theta(n log n) worst case and in-place. It is not stable, and the constant factors and cache behavior are worse than quicksort and Timsort. The heap lesson builds the structure. Here you only need the bound and the in-place claim.

Counting sort is not a comparison sort. If keys are integers in a small range U, count frequencies and write the output from the counts. Stable counting sort writes backward into an output array so equal keys keep their order. Time is Theta(n + U). Radix sort applies a stable sort to digits from least significant to most significant. For fixed-width integers the time is linear in n times the number of digits. These sorts break the comparison lower bound by using the structure of the key. They do not sort arbitrary comparable objects.

Stability means that equal keys keep their input order. Merge sort and insertion sort are stable if implemented carefully. Quicksort and heapsort are not. A stable sort lets you sort by a secondary key first and a primary key second, and the secondary order survives. Python's sort is stable. Rely on it, and say that you rely on it.

## Diagram and dry run

```mermaid
flowchart TD
    A[Split the array] --> B[Sort the left half]
    A --> C[Sort the right half]
    B --> D[Merge, taking the smaller head]
    C --> D
    D --> E[Equal keys come from the left half first, so the merge is stable]
```

Insertion sort on 4, 2, 4, 1. The two 4s are distinguished as 4a and 4b so stability is visible.

| Prefix considered | Array | What moved |
| --- | --- | --- |
| 4a | 4a, 2, 4b, 1 | already sorted |
| 4a, 2 | 2, 4a, 4b, 1 | 4a shifted right, 2 inserted. 4b untouched |
| 2, 4a, 4b | 2, 4a, 4b, 1 | 4b was already in place after 4a |
| full | 1, 2, 4a, 4b | 1 inserted at the front. The two 4s kept their order |

Merge of the sorted halves 2, 4a and 1, 4b. Compare 2 with 1, take 1. Compare 2 with 4b, take 2. Compare 4a with 4b, take 4a because ties prefer the left half. Then take 4b. Result 1, 2, 4a, 4b. A merge that preferred the right half on ties would emit 4b before 4a and would be unstable.

## Runnable Python

Insertion sort is the one to code when n is tiny or nearly sorted. Merge sort is the one to code when you need a worst-case guarantee and stability. Both are shown. The recursive merge sort is the natural form. The insertion sort is a loop.

```python
def insertion_sort(nums: list[int]) -> list[int]:
    a = nums[:]
    for i in range(1, len(a)):
        value = a[i]
        j = i - 1
        while j >= 0 and a[j] > value:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = value
    return a


def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:
        return nums[:]
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

The comparison `a[j] > value`, rather than `>=`, is what keeps insertion sort stable. The comparison `left[i] <= right[j]` is what keeps the merge stable. Change either one and equal keys can cross. `insertion_sort` on 4, 2, 4, 1 returns 1, 2, 4, 4 with the original 4s in their original relative order.

## Complexity and trade-offs

| Sort | Worst time | Average time | Extra space | Stable |
| --- | --- | --- | --- | --- |
| Selection | Theta(n squared) | Theta(n squared) | Theta(1) | no, if you swap |
| Bubble, early exit | Theta(n squared) | Theta(n squared) | Theta(1) | yes |
| Insertion | Theta(n squared) | Theta(n squared) | Theta(1) | yes |
| Merge sort | Theta(n log n) | Theta(n log n) | Theta(n) | yes |
| Quicksort, random pivot | Theta(n squared) | Theta(n log n) expected | Theta(log n) stack expected | no |
| Heapsort | Theta(n log n) | Theta(n log n) | Theta(1) | no |
| Counting sort | Theta(n + U) | Theta(n + U) | Theta(n + U) | yes, if written carefully |

Choose merge sort when you must be stable and worst-case linearithmic. Choose heapsort when you must be worst-case linearithmic and in-place and you can give up stability. Choose randomized quicksort when average speed and memory locality matter and stability does not. Choose insertion sort below a few dozen elements or on nearly sorted data. Choose counting or radix sort when the keys are integers in a modest range. In Python, call the built-in sort unless the point of the question is to implement one.

## Tricks, tips, and patterns

Know the lower bound so you do not promise a comparison sort faster than n log n. Know that counting sort is the escape hatch, and name the range. For quicksort, mention the worst case and the random pivot in the same sentence. For merge sort, mention the buffer. If you need to sort indexes by a key, sort pairs of key and index, and a stable sort will preserve index order among equal keys even if you did not include the index. Including the index makes any sort stable with respect to the original order. That trick rehabilitates quicksort when stability is required and you can afford to compare pairs.

## Common mistakes and edge cases

A merge that drops the leftover half. A partition that does not shrink the side containing the pivot, so quicksort recurses on the same array forever. Unstable tie handling described as stable. Using quicksort on equal keys with Lomuto and being surprised by quadratic time. Forgetting that the comparison lower bound does not apply to radix sort. Sorting a list of pairs when the problem wanted the original indexes, and not carrying the indexes along. An empty array and a one-element array must be base cases of merge sort. Integer keys that are negative break a naive counting sort that uses the key as an array index. Shift by the minimum first.

## Interview notes

If the prompt is "sort this," ask whether stability and worst-case time matter, then pick from the table. If the prompt is a search problem in disguise, sort and say the n log n cost. Code merge sort if they ask you to implement an n log n sort and you want a bound you can prove while you type. Code insertion sort if they ask for the nearly-sorted case. Do not code bubble sort as a final answer. State the lower bound in one sentence if someone asks for linear comparison sorting.

## Practice problems

1. [Sort List](/practice/sort-list) — merge sort on nodes.
2. [Count Inversions](/practice/count-inversions) — the merge counts split inversions.
3. [Merge Sorted Array](/practice/merge-sorted-array) — the merge, in place from the end.
4. [Sort Colors](/practice/sort-colors) — a three-way partition, the quicksort cousin.
5. [Kth Largest Element](/practice/kth-largest-element-in-an-array) — quickselect or a heap. Quickselect is partition without sorting both sides.

## Summary and cheat sheet

- Comparison sorting is Omega(n log n) in the worst case. n! orders, two-way questions.
- Insertion sort is Theta(n + inversions) and stable. Use it when the array is short or almost sorted.
- Merge sort is worst-case n log n, stable, and needs a linear buffer.
- Quicksort is expected n log n with a random pivot, unstable, and quadratic in the worst case.
- Heapsort is worst-case n log n and in-place and unstable.
- Counting and radix sorts are linear in n plus the key range or the number of digits. They are not comparison sorts.
- Stability is a property of the implementation of ties, not a vibe.

## Further reading

- [Wikipedia — Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm)
- [Wikipedia — Quicksort](https://en.wikipedia.org/wiki/Quicksort)
- [Wikipedia — Merge sort](https://en.wikipedia.org/wiki/Merge_sort)
- [CP-Algorithms, merge sort](https://cp-algorithms.com/others/merge_sort.html)
'''

TIM = r'''
## Why this matters

When you call `sorted` or `list.sort` in Python, you are not calling quicksort. You are calling Timsort, a stable hybrid designed for arrays that contain ordered runs, which is what real data often looks like. Interviewers who hear "Python's sort is n log n" want the next sentence: it is stable, its worst case is n log n, and its best case on already-sorted data is linear. That sentence changes designs. You can sort by a secondary key and then a primary key. You can sort a nearly sorted log without paying the full linearithmic cost. You should not reimplement Timsort in a 45-minute round. You should know why the library is allowed to be as fast as it is, and when your own merge sort is the thing to code instead.

## Intuition

Insertion sort is wonderful on a run that is already sorted, and painful on a long random array. Merge sort is steady on a random array, and it wastes work rediscovering runs that were already sorted. Timsort finds the runs that already exist, extends short ones with insertion sort until they are worth merging, and then merges runs in an order that keeps the merge tree balanced. The already-sorted array is one big run and needs no merge. The random array becomes a sequence of short runs and falls back to something with the shape of merge sort.

## Core concept in depth

A run is a consecutive slice that is non-decreasing, or strictly decreasing. A strictly decreasing run can be reversed in place into an increasing run. The reversal is stable for our purposes only because the run is strictly decreasing, so there are no equal keys whose order would flip. If equals were included in the reversed region, stability would break. Timsort therefore reverses only strict descents.

If the natural run is shorter than a minimum run length, insertion sort extends it until it reaches that length or the array ends. The minimum is chosen based on n, often a power of two near 32 or 64, so later merges are aligned. Insertion sort on a slice of fixed length minrun is cheap: the quadratic term is constant with respect to n, and across n/minrun such slices the total insertion work is linear.

The stack of pending runs is the part with the real invariant. Timsort pushes runs onto a stack and merges adjacent runs to maintain two numerical rules, often called the balance invariants: the lengths of runs from the top decrease in a way that prevents a long run from sitting on two tiny ones, and no run length equals or exceeds the sum of the two above it in the dangerous direction. The exact inequalities have been adjusted over the years after bugs were found. The idea you should keep is the one merge sort already taught you. Merging similar sizes is efficient. Merging a huge run with a tiny run, over and over, can degenerate. The stack invariants force merges that keep the costs linearithmic.

Merging two runs uses a temporary buffer. Timsort includes a galloping mode. When one run wins many comparisons in a row, the algorithm switches to galloping: it searches ahead exponentially to find how far the winning run continues, then copies that span in one move, using a binary search to finish the location. On data with long pre-ordered pieces, galloping skips comparisons. On random data, galloping rarely triggers, and the merge looks like an ordinary merge. Galloping is an optimization, not the correctness argument. A student implementation that always does a straight merge is still a correct stable merge of the runs Timsort identified.

The worst case remains Theta(n log n). You cannot beat the comparison lower bound on arbitrary keys, and Timsort is a comparison sort. The best case is Theta(n): one natural run covers the array, insertion sort does not have to extend it, and no merge happens. Nearly sorted arrays, arrays with a few long runs, and arrays sorted in reverse (one strict descent, reversed once) are the cases where Timsort earns its reputation. The extra memory is O(n) in the worst case for merge buffers, often less because the buffer can be sized to the smaller run.

Stability is preserved at each step. Insertion sort on a run is stable. Reversal is only applied to strict descents. The merge takes from the left run on equal keys. Therefore the whole algorithm is stable. This is why the Python idiom "sort by secondary key, then sort by primary key" works. The second stable sort keeps the relative order of records that share a primary key, and that order is the secondary key you established first. A single sort with a tuple key `(primary, secondary)` does the same job in one call, because tuples compare lexicographically. Prefer the tuple when you control the key. Prefer two sorts when the secondary order is the current order of the list and you do not want to name it.

Timsort is not a radix sort and it does not exploit integer structure. Integers, strings, and custom objects all go through comparisons. A custom object's ordering must be a strict weak order: irreflexive, transitive on the "less than" relation in the usual way, and consistent with equality if you also define equality. A comparison that is not transitive produces undefined behavior that can surface as an exception or as a silently wrong order. Do not sort by a key that mutates.

CPython's list.sort is in-place Timsort. `sorted` copies and then sorts. Both are stable. The key function, if you pass one, is called once per element. That is the decorate-sort-undecorate pattern, also called Schwartzian transform: compute the keys up front so an expensive key is not recomputed on every comparison. You can rely on that. It is part of the documented contract, not an accident.

## Diagram and dry run

```mermaid
flowchart TD
    A[Scan for the next natural run] --> B{Run shorter than minrun?}
    B -->|Yes| C[Extend with insertion sort]
    B -->|No| D[Push the run]
    C --> D
    D --> E{Stack invariants violated?}
    E -->|Yes| F[Merge adjacent runs]
    F --> E
    E -->|No| G{More of the array?}
    G -->|Yes| A
    G -->|No| H[Collapse the stack by merging]
```

Array 1, 2, 3, 7, 6, 5, 4, 8, with a small minrun of 4, told as a simplified story rather than as a line-by-line CPython trace.

| Step | What is recognized | Resulting runs |
| --- | --- | --- |
| 1 | 1, 2, 3 is ascending and shorter than 4 | insertion sort pulls in 7. Run is 1, 2, 3, 7 |
| 2 | 6, 5, 4 is a strict descent | reverse it to 4, 5, 6, then insertion sort pulls in 8. Run is 4, 5, 6, 8 |
| 3 | two runs remain | merge them stably into 1, 2, 3, 4, 5, 6, 7, 8 |

The first run did not need a merge with itself. The descent was reversed before any equal-key worry, and there were no equals. A fully sorted array would stop after step 1 with a single run and no merge. That is the linear best case, up to the scan that verified the run.

## Runnable Python

You will call the library. The wrapper below sorts records by last name and then first name using a tuple key, and it sorts the same records in two stable passes so you can see the idiom. A tiny run detector shows the linear scan that starts Timsort, without claiming to be the full algorithm.

```python
def sort_people(people: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """people are (first, last). Order by last name, then first name."""
    return sorted(people, key=lambda person: (person[1], person[0]))


def sort_people_two_passes(people: list[tuple[str, str]]) -> list[tuple[str, str]]:
    by_first = sorted(people, key=lambda person: person[0])
    return sorted(by_first, key=lambda person: person[1])


def natural_run_length(nums: list[int]) -> int:
    if not nums:
        return 0
    i = 1
    if i < len(nums) and nums[i] < nums[0]:
        while i < len(nums) and nums[i] < nums[i - 1]:
            i += 1
        return i
    while i < len(nums) and nums[i] >= nums[i - 1]:
        i += 1
    return i
```

On the people Ada Lovelace, Grace Hopper, and Ada Byron, both sorters emit Ada Byron, Grace Hopper, Ada Lovelace. `natural_run_length` on 1, 2, 3, 7, 6 returns 4. On 6, 5, 4, 8 it returns 3, the strict descent, leaving 8 for the next run. It does not reverse. It only measures.

## Complexity and trade-offs

| Input shape | Timsort time | Extra space | Stable |
| --- | --- | --- | --- |
| Arbitrary comparisons | Theta(n log n) worst case | O(n) | yes |
| Already sorted | Theta(n) | O(1) beyond a few words | yes |
| Reversed, distinct keys | Theta(n) | O(1) | yes |
| A constant number of long runs | Theta(n log R) with R runs, often close to linear | O(n) | yes |
| Your own merge sort | Theta(n log n) always | Theta(n) | yes if ties prefer the left |

Implementing full Timsort in an interview is a poor use of time. Implementing merge sort is the right substitute when the question is "write a stable n log n sort." Saying "I would call the built-in stable sort" is the right answer when the question is a scheduling or anagram problem that needs ordering as a step. Do not write a quadratic sort and then sort the output of a library by accident twice without accounting for it. Two stable library sorts are still n log n.

## Tricks, tips, and patterns

Pass a tuple key when the order is lexicographic. Use two stable passes when the secondary key is "whatever order I have now." Remember that `list.sort` mutates and returns None. `sorted` returns a new list. The key function runs once per element. For a descending numeric key, negate the number or pass `reverse=True`, and think about how reverse interacts with stability: reversing the comparison keeps stability with respect to the reversed order, which is what you want if you asked for it. Do not mutate the list inside the key function.

## Common mistakes and edge cases

Claiming quicksort is what Python uses. Claiming the best case is n log n. Reversing a non-strict descending run and scrambling equal keys. Forgetting that minrun insertion sort is why tiny arrays are fast. Using an unstable mental model and sorting by the primary key first, which destroys the secondary order you have not established yet. The order of two passes is: secondary first, primary second. A comparison key that returns inconsistent answers. Sorting a list of lists by a key that is itself a list you later mutate. Empty input. One element. All keys equal, which must keep the original order because the sort is stable. That last case is the test you should run when you implement your own merge.

## Interview notes

The expected sentence is: "Python's sort is Timsort, stable, worst case n log n, linear on sorted input." If they ask why it is faster on real data, say natural runs plus insertion sort on short runs plus balanced merges. If they ask you to implement the sort, implement merge sort and mention that Timsort is merge sort that starts from natural runs. Do not recite galloping offsets from memory. Do mention stability and the two-pass idiom, because that is the part you will use on the next problem.

## Practice problems

1. [Merge Intervals](/practice/merge-intervals) — library sort by start, then a linear sweep.
2. [Group Anagrams](/practice/group-anagrams) — sorting each word is a key. The words are short, so the n log n of Timsort is on the word length.
3. [Queue Reconstruction by Height](/practice/queue-reconstruction-by-height) — sort by height, then insert. The sort is the stable or tuple-key step.
4. [Count Inversions](/practice/count-inversions) — implement the merge yourself, because the library sort will not count inversions for you.
5. [Sort List](/practice/sort-list) — merge sort on nodes, where Timsort's random-access run scan does not apply directly.

## Summary and cheat sheet

- Timsort finds natural runs, extends short ones with insertion sort, and merges under stack invariants.
- It is stable. Equal keys keep their order. Two-pass sorting works.
- Worst case Theta(n log n). Best case Theta(n) on one run.
- Galloping speeds up lopsided merges. Correctness comes from the stable merge, not from galloping.
- `sorted` copies. `list.sort` mutates and returns None. Key functions run once per element.
- In an interview, call the library when sorting is a step, and code merge sort when the sort itself is the question.

## Further reading

- [Wikipedia — Timsort](https://en.wikipedia.org/wiki/Timsort)
- [Python list.sort documentation](https://docs.python.org/3/library/stdtypes.html#list.sort)
- [Tim Peters, the original Timsort description, linked from the Python source](https://github.com/python/cpython/blob/main/Objects/listsort.txt)
'''

emit(
    "07-searching-sorting",
    "01-binary-search-variants.mdx",
    title="Binary Search and Search on the Answer",
    slug="binary-search-variants",
    summary="Inclusive and half-open loops, bounds, rotated arrays, peaks, and monotone feasibility tests.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["backtracking"],
    tags=["binary-search", "sorting"],
    order=1,
    body=BINARY,
)
emit(
    "07-searching-sorting",
    "02-classic-sorts.mdx",
    title="Classic Sorting Algorithms",
    slug="classic-sorts",
    summary="Insertion, merge, quick, heap, counting, and the comparison lower bound, with stability treated as a real invariant.",
    duration=45,
    difficulty="intermediate",
    prerequisites=["binary-search-variants"],
    tags=["sorting", "merge-sort", "quicksort"],
    order=2,
    body=SORTS,
)
emit(
    "07-searching-sorting",
    "03-timsort.mdx",
    title="Timsort and Python's Stable Sort",
    slug="timsort",
    summary="Natural runs, minrun insertion sort, balanced merges, and the stability contract behind sorted and list.sort.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["classic-sorts"],
    tags=["timsort", "sorting", "python"],
    order=3,
    body=TIM,
)
