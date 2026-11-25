"""Interview pattern catalog and timed mock strategy."""

from emit import emit

PATTERNS = r'''
## Why this matters

A 45-minute interview is a recognition problem before it is a coding problem. The candidates who stall are often fluent in isolation and slow to name the family. This lesson is the index for the course: about twenty patterns that cover the coding rounds aimed at the 15 to 20 LPA band. A pattern is not a slogan you paste onto a problem. It is a contract between the shape of the input and a technique whose correctness you already proved in an earlier lesson. You use the index to choose a family in the first few minutes, then you drop into that lesson's argument. Memorizing two hundred solutions without the contracts does not survive a reworded prompt.

## Intuition

Read the contract out loud. Contiguous subarray, sorted pair, monotone predicate, shortest unweighted path, dependencies, optimal substructure, a prefix code, a stream of the top k. Each phrase points at one or two families and rules out the rest. If two families still fit, compare their parameters. A subset question with n near 40 is meet-in-the-middle. The same question with a small target is knapsack. A range sum of an invertible array is a prefix or a Fenwick tree, not a fresh scan, once the queries repeat. The diagram below is the first cut. The catalog is the second.

## Core concept in depth

1. Two pointers. Trigger: a sorted array, a pair that sums to a target, a palindrome check, or a partition you can move inward. Tool: one index from each end, or a slow write index and a fast read index. The proof is that each discarded side cannot contain the answer. Lesson: [Two pointers](/lessons/two-pointers). Start with [Two Sum II](/practice/two-sum-ii), [Container With Most Water](/practice/container-with-most-water), and [Valid Palindrome](/practice/valid-palindrome). The usual bug is moving both pointers on an unsorted array and claiming the pair is gone.

2. Sliding window. Trigger: a contiguous slice, a longest or shortest slice under a constraint that only gets tighter when the slice grows. Tool: advance the right edge, and advance the left edge while the constraint is broken. Lesson: [Sliding window](/lessons/sliding-window). Problems: [Longest Substring Without Repeating Characters](/practice/longest-substring-without-repeating-characters), [Minimum Window Substring](/practice/minimum-window-substring), [Longest Repeating Character Replacement](/practice/longest-repeating-character-replacement). If the constraint is not monotone, the window is the wrong family and a prefix map may be the right one.

3. Prefix sums. Trigger: many range sums, a subarray sum equal to k, or "divisible by k." Tool: a prefix array, or a map from prefix value to how often you have seen it. Lesson: [Prefix sums and Kadane](/lessons/prefix-sums-and-kadane). Problems: [Subarray Sum Equals K](/practice/subarray-sum-equals-k), [Product of Array Except Self](/practice/product-of-array-except-self), [Continuous Subarray Sum](/practice/continuous-subarray-sum). Remember that a prefix of 0 is already in the map before the loop, or the subarray that starts at index 0 disappears.

4. Kadane and running extrema. Trigger: a maximum subarray, a maximum product, or a best-so-far price. Tool: a running best that resets when the past cannot help the future. Same lesson as prefixes. Problems: [Maximum Subarray](/practice/maximum-subarray), [Maximum Product Subarray](/practice/maximum-product-subarray), [Best Time to Buy and Sell Stock](/practice/best-time-to-buy-and-sell-stock). The product version tracks both the best and the worst ending here, because a negative can flip.

5. Binary search on a predicate. Trigger: a sorted array, or an unsorted array hiding a monotone yes-or-no function of a numeric answer, such as "can this capacity ship in time." Tool: the lower-bound loop from the searching lesson, and a linear check of the candidate. Lesson: [Binary search variants](/lessons/binary-search-variants). Problems: [Koko Eating Bananas](/practice/koko-eating-bananas), [Split Array Largest Sum](/practice/split-array-largest-sum), [Capacity to Ship Packages Within D Days](/practice/capacity-to-ship-packages-within-d-days). Draw the predicate. If it is not monotone, you are not allowed to discard a half.

6. Fast and slow pointers. Trigger: a cycle in a linked list, the middle of a list, or a duplicate in a restricted range that you can treat as a functional graph. Tool: Floyd's cycle finding. Lesson: [Linked list patterns](/lessons/linked-list-patterns). Problems: [Linked List Cycle](/practice/linked-list-cycle), [Linked List Cycle II](/practice/linked-list-cycle-ii), [Find the Duplicate Number](/practice/find-the-duplicate-number). Do not destroy the list if the problem forbids it.

7. Linked list reversal. Trigger: reverse a whole list, a sublist, or groups of k. Tool: three references, previous, current, and next, or a recursive reverse of the tail that you only use when you can explain the stack. Same lesson. Problems: [Reverse Linked List](/practice/reverse-linked-list), [Reverse Linked List II](/practice/reverse-linked-list-ii), [Reverse Nodes in k-Group](/practice/reverse-nodes-in-k-group). Draw the empty list and a list of one node before you touch k-group.

8. Monotonic stack. Trigger: the next greater element, the previous smaller element, or the largest rectangle in a histogram. Tool: a stack of indexes whose values stay increasing or decreasing, popping when the newcomer breaks the order. Lesson: [Monotonic stacks](/lessons/monotonic-stacks). Problems: [Daily Temperatures](/practice/daily-temperatures), [Next Greater Element I](/practice/next-greater-element-i), [Largest Rectangle in Histogram](/practice/largest-rectangle-in-histogram). Store indexes, not values, when the answer is a distance.

9. Monotonic deque. Trigger: the maximum or minimum inside every window of a fixed length. Tool: a deque of indexes, dropping the back while it is worse than the newcomer, and dropping the front when it slides out of the window. Problem: [Sliding Window Maximum](/practice/sliding-window-maximum). A heap also works and costs an extra log factor, plus lazy deletion. The deque is linear.

10. Hash counting. Trigger: a complement you can look up, a frequency, an anagram, a longest consecutive run. Tool: a map or a set, and a statement about expected constant time. Lesson: [Hash maps and sets](/lessons/hash-maps-and-sets). Problems: [Two Sum](/practice/two-sum), [Group Anagrams](/practice/group-anagrams), [Longest Consecutive Sequence](/practice/longest-consecutive-sequence). Worst-case hash time is linear per operation. Say "expected." Caches with eviction are the design problems [LRU Cache](/practice/lru-cache) and [LFU Cache](/practice/lfu-cache), taught in [LRU and LFU](/lessons/lru-and-lfu).

11. BFS for shortest paths. Trigger: an unweighted graph or a grid, and a minimum number of edges or steps. Tool: a queue and a visited set marked when you enqueue, not when you dequeue. Lesson: [BFS, DFS, and grids](/lessons/bfs-dfs-and-grids). Problems: [Number of Islands](/practice/number-of-islands), [Rotting Oranges](/practice/rotting-oranges), [Word Ladder](/practice/word-ladder), [Shortest Path in Binary Matrix](/practice/shortest-path-in-binary-matrix). Weighted edges with non-negative weights are Dijkstra, from the shortest-paths lesson, not this queue.

12. Backtracking. Trigger: generate combinations, permutations, partitions, or a search that must undo a choice. Tool: recurse, mark, explore, unmark. Lesson: [Backtracking](/lessons/backtracking). Problems: [Subsets](/practice/subsets), [Permutations](/practice/permutations), [Combination Sum](/practice/combination-sum), [Word Search](/practice/word-search), [N-Queens II](/practice/n-queens-ii), [Palindrome Partitioning](/practice/palindrome-partitioning). Prune with a bound when you have one. Do not prune with a wish.

13. Topological sort. Trigger: prerequisites, a course schedule, an alien order you do not have in this bank, or any DAG where an edge means "before." Tool: Kahn's algorithm, indegrees and a queue, or DFS with colors. A cycle means no order. Lesson: [Topological sort](/lessons/topological-sort). Problems: [Course Schedule](/practice/course-schedule) and [Course Schedule II](/practice/course-schedule-ii). If the graph is undirected, this is the wrong tool.

14. Union-find. Trigger: connectivity under unions, a redundant edge, accounts that share an email, or Kruskal. Tool: parent pointers, union by rank, and path compression. Lesson: [MST, DSU, and bridges](/lessons/mst-dsu-and-bridges). Problems: [Number of Provinces](/practice/number-of-provinces), [Redundant Connection](/practice/redundant-connection), [Accounts Merge](/practice/accounts-merge). If you need the path itself, BFS or DFS is the better answer. DSU answers "same component," not "the route."

15. Heaps and top-k. Trigger: the k largest, a running median, or merging k sorted lists. Tool: a binary heap. For the kth largest, a heap of size k is enough. Lesson: [Binary heaps](/lessons/binary-heaps). Problems: [Kth Largest Element in an Array](/practice/kth-largest-element-in-an-array), [Top K Frequent Elements](/practice/top-k-frequent-elements), [Merge k Sorted Lists](/practice/merge-k-sorted-lists), [K Closest Points to Origin](/practice/k-closest-points-to-origin). Quickselect has a better expected bound and a worse constant in practice. Name both if they ask.

16. Intervals. Trigger: merge overlaps, how many rooms, how many arrows, or a schedule sorted by finish time. Tool: sort by the endpoint the argument names, then scan. Lesson: [Partitions, majority, and intervals](/lessons/partitions-majority-and-intervals). Problems: [Merge Intervals](/practice/merge-intervals), [Meeting Rooms II](/practice/meeting-rooms-ii), [Non-overlapping Intervals](/practice/non-overlapping-intervals), [Insert Interval](/practice/insert-interval). Sorting by the wrong endpoint is the entire bug.

17. Greedy exchange. Trigger: a local choice you can swap into any optimal solution, jumps, gas, or the smallest number after deletions. Tool: one forward pass after you can say the swap. Lesson: [Greedy algorithms](/lessons/greedy-algorithms). Problems: [Jump Game](/practice/jump-game), [Gas Station](/practice/gas-station), [Partition Labels](/practice/partition-labels), [Task Scheduler](/practice/task-scheduler). If you cannot finish the exchange sentence, go back to DP. Non-canonical coins are the counterexample.

18. Knapsack dynamic programming. Trigger: optimal substructure on a capacity, a count of ways, or a take-or-skip decision, with n and the capacity both moderate. Tool: the 0/1 loop that walks capacity backward, or the unbounded loop that walks it forward. Lesson: [Classic DP families](/lessons/classic-dp-families), after the [DP framework](/lessons/dp-framework). Problems: [Knapsack](/practice/knapsack), [Coin Change](/practice/coin-change), [Coin Change II](/practice/coin-change-ii), [Partition Equal Subset Sum](/practice/partition-equal-subset-sum), [House Robber](/practice/house-robber), [Word Break](/practice/word-break), [Longest Common Subsequence](/practice/longest-common-subsequence), [Edit Distance](/practice/edit-distance). Combinations and permutations of coins are different loop orders. Do not mix them.

19. Bitmask and state-machine DP. Trigger: a subset of a small ground set, or a stock problem whose state is "holding, sold, cooling." Tool: an integer mask, or a fixed handful of rolling variables. Lesson: [Advanced DP](/lessons/advanced-dp) and the mask arithmetic in [Bit manipulation](/lessons/bit-manipulation). Problem: [Best Time to Buy and Sell Stock with Cooldown](/practice/best-time-to-buy-and-sell-stock-with-cooldown). If the ground set is larger than about 20, the mask does not fit. Use the bit lesson's test, set, and clear operations, and do not reinvent them in the DP loop.

20. Tries and string matching. Trigger: many prefixes, a dictionary of words, or a single pattern searched in a long text. Tool: a trie node per character, or the prefix function, or a rolling hash. Lessons: [Segment trees, Fenwick trees, and tries](/lessons/segment-fenwick-and-tries) and [KMP, Rabin-Karp, and Z](/lessons/kmp-rabin-karp-z). Problems: [Implement Trie](/practice/implement-trie), [Word Break](/practice/word-break), [Find the Index of the First Occurrence](/practice/find-the-index-of-the-first-occurrence), [Longest Happy Prefix](/practice/longest-happy-prefix). Word break is DP over the dictionary. The trie is how the dictionary is stored when the word list is the heavy part. They compose.

Two shapes sit underneath almost every entry. A search that tries a choice and undoes it is recursive backtracking. A scan that maintains an invariant and moves an endpoint is an iterative window, pointer, or stack. When a problem is new, write the recursive specification if the object is a decision tree, or the invariant if the object is a scan, and only then tighten it. The [approach guide](/lessons/interview-approach-guide) is the order of work. This catalog is the menu that guide points at.

## Diagram and dry run

```mermaid
flowchart TD
    A[Name the object the answer is about] --> B{A contiguous slice?}
    B -->|Yes| C{Does growing the slice only tighten the constraint?}
    C -->|Yes| D[Sliding window]
    C -->|No| E[Prefix map or Kadane]
    B -->|No| F{A monotone predicate or a sorted pair?}
    F -->|Yes| G[Binary search or two pointers]
    F -->|No| H{Dependencies, components, or decisions?}
    H -->|Dependencies| I[Topological sort or DSU]
    H -->|Decisions with optimal substructure| J[DP or a proved greedy]
    H -->|Generate every answer| K[Backtracking]
```

Classify four prompts before writing code.

| Prompt | Family | Why the neighbors lose |
| --- | --- | --- |
| Longest subarray with at most two distinct values | Sliding window | Prefix sums do not express "at most two distinct" as a numeric target |
| Minimum capacity so the packages ship within D days | Binary search on the answer | The capacity is monotone, and a greedy check is linear |
| Can these courses be finished given prerequisites | Topological sort | Union-find would ignore edge direction |
| Count subsets of 40 integers that sum to a huge target | Meet-in-the-middle | The knapsack table is the size of the target, which does not fit |

A fifth prompt, "range sum with point updates, many of them," is a Fenwick tree or a segment tree, from the trees module, not a pattern you invent during the round. If you only remember blocks, say "sqrt(n) per query" and offer the tree as the improvement.

## Runnable Python

The same two-sum specification, first as a recursive search that tries the rest of the array, then as the iterative hash scan you should actually submit. The recursion is the brute force. It makes the complement explicit. The loop keeps the invariant that every index before i is already stored.

```python
def two_sum_rec(nums: list[int], target: int, i: int = 0) -> list[int]:
    if i >= len(nums):
        return []
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
    return two_sum_rec(nums, target, i + 1)


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], i]
        seen[value] = i
    return []
```

On 2, 7, 11, 15 with target 9, the recursive search returns indexes 0 and 1 after one successful pair check. The hash scan stores 2 at index 0, then sees 7 whose complement is already stored, and returns the same indexes. Both are correct. The recursion does Theta(n squared) additions in the worst case. The hash scan is expected linear. In a round you may say the recursive version in one sentence and write the loop.

## Complexity and trade-offs

| If you recognize | You usually pay | If you miss it, you pay |
| --- | --- | --- |
| Sliding window or two pointers | linear after a possible sort | a quadratic double loop |
| Binary search on the answer | the check times log of the range | a linear scan of every candidate answer |
| Monotonic stack or deque | linear | a nested "scan until greater" |
| Hash complement | expected linear, linear space | a sort plus two pointers, or worse |
| BFS on an unweighted graph | linear in vertices plus edges | Dijkstra's extra log, still correct |
| DSU | almost linear | a BFS per query |
| 0/1 knapsack | n times capacity | 2 to the n subsets |
| Meet-in-the-middle | 2 to the n over 2 | a DP table that does not fit |
| Trie or KMP | linear in the total characters | a scan of the text per pattern |

Recognition does not change the optimal complexity. It changes whether you reach it before the clock does. A correct quadratic solution that you finish and test is worth more than a named linear solution you do not finish. State the quadratic, then improve it if the constraints require it.

## Tricks, tips, and patterns

Keep a one-page index of the twenty triggers, not the twenty codes. In the round, write the trigger you think you heard and the invariant it needs. If you cannot write the invariant, you have not recognized the pattern, you have remembered a title. Sort endpoints only after you know which endpoint the exchange uses. Mark visited when you enqueue. Walk capacity backward for 0/1 knapsack. Include the empty prefix in a prefix map. Draw 2n - 1 palindrome centers. For graphs, ask directed or undirected, weighted or not, and whether a cycle is possible. Those three questions choose BFS, Dijkstra, topo, or DSU. When the problem says "return any" you may break ties however the code finds them. When it says "return all," you need the generator, which is usually backtracking.

## Common mistakes and edge cases

Forcing a window onto a non-monotone constraint and skipping the true answer. Binary searching a predicate you have not tested at the boundaries. Using BFS on negative weights. Using DSU on a directed dependency. A greedy coin solution on a non-canonical system. Mixing coin combinations with coin permutations. Forgetting the empty-prefix key. Popping a monotonic stack of values when the answer needs indexes. Generating subsets with duplicate branches because you did not sort and skip. A trie that marks every character as a word end. An off-by-one in binary search that loops forever because the mid update does not shrink the range. Pattern names used in the interview without a complexity. The name is not the solution.

## Interview notes

Spend the first three minutes on the contract and the family. Say "this is a monotone capacity, I will binary search it and check a day count" rather than "I have seen this." If you are wrong, the invariant will fail on the example and you still have time to switch. The [approach guide](/lessons/interview-approach-guide) tells you how to spend the rest of the slot. The next lesson is a timed rehearsal of that spending. Do not collect new patterns during a mock. Use this list.

## Practice problems

Work one problem from each family you cannot yet name in under a minute. A compact set that touches the catalog:

1. [Two Sum](/practice/two-sum), [Longest Substring Without Repeating Characters](/practice/longest-substring-without-repeating-characters), and [Subarray Sum Equals K](/practice/subarray-sum-equals-k).
2. [Koko Eating Bananas](/practice/koko-eating-bananas), [Daily Temperatures](/practice/daily-temperatures), and [Sliding Window Maximum](/practice/sliding-window-maximum).
3. [Course Schedule](/practice/course-schedule), [Number of Islands](/practice/number-of-islands), and [Redundant Connection](/practice/redundant-connection).
4. [Coin Change](/practice/coin-change), [House Robber](/practice/house-robber), and [Word Break](/practice/word-break).
5. [Jump Game](/practice/jump-game), [Merge Intervals](/practice/merge-intervals), and [Implement Trie](/practice/implement-trie).

## Summary and cheat sheet

- A pattern is a trigger plus an invariant you can prove, not a problem title.
- Window and two pointers need a monotone reason to move an endpoint.
- Binary search needs a monotone predicate. Test both bounds.
- Stacks and deques stay ordered. Store indexes when distance matters.
- BFS is for unweighted distance. Dijkstra is for non-negative weights. Topo is for directed prerequisites. DSU is for undirected connectivity.
- 0/1 knapsack walks capacity backward. Unbounded walks it forward. Masks need a small ground set.
- Meet-in-the-middle is the subset tool when n is near 40. DP is the tool when the target is small.
- Tries store prefixes. KMP stores borders. Do not confuse a substring with a subsequence.
- Say the family, the complexity, and the invariant before you code.

## Further reading

- [Wikipedia — Algorithmic paradigm](https://en.wikipedia.org/wiki/Algorithmic_paradigm)
- [CP-Algorithms](https://cp-algorithms.com/) — the same families, written as reference implementations.
- [CLRS, Introduction to Algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — the proofs this catalog points at.
- The previous lesson in this course, [Interview approach](/lessons/interview-approach-guide), for the order of work inside one problem.
'''

MOCK = r'''
## Why this matters

Knowing the twenty patterns and using one of them at minute six are different skills. A hiring loop aimed at about 15 to 20 LPA is usually an online assessment and then one or two live coding rounds, sometimes with a short conversation about a project you actually built. Each live slot is about 45 to 60 minutes and contains one hard problem or two medium ones. The interviewer is scoring whether you can clarify a contract, reach a correct approach, code it, and test it, while they can still follow you. This lesson is the rehearsal protocol for that slot. The approach guide is the checklist for a single problem. The pattern catalog is the menu. This chapter is the clock.

## Intuition

Treat a mock as a closed-book performance, not as a study session. Pick a problem you have not solved this week. Start a timer. Speak the way you will speak on the call. When you get stuck, follow the stuck protocol below instead of opening the editorial. After the timer, and only then, read the editorial and write a short after-action note: which trigger you missed, which test would have caught the bug, and which lesson to reread. Five honest mocks will teach you more than twenty editorial read-throughs. The point of the note is to change the next mock, not to collect remorse.

## Core concept in depth

The loop, so you can aim at it. An online assessment is two or three problems in 60 to 90 minutes, often with hidden tests and no interviewer to rescue a misread constraint. Practice those as silent timed sets: no hints, submit only when the examples and your own edge cases pass. A live round is slower and more verbal. You can ask whether the array is sorted, whether values fit in 32 bits, and whether "substring" was meant rather than "subsequence." Ask. A wrong assumption you did not check becomes a wrong program you then debug in public. A hiring-manager conversation at this band is about a project, a bug you owned, and how you tested it. It is not a third algorithms final. Do not neglect it, and do not let it crowd out the coding practice that decides the earlier rounds.

The 45-minute script for one medium-hard problem. Minutes 0 to 3: restate the problem in one sentence, name the input size, and ask the two constraints that choose a family. Write an example the interviewer did not give you, including an empty input or a one-element input. Minutes 3 to 8: state a correct brute force and its complexity. If the constraints allow it, say so and offer to code it. If they do not, name the family from the catalog and the invariant. Minutes 8 to 12: dry-run the intended approach on the example, by hand, before any code. This is where off-by-one and "I actually needed indexes" show up cheaply. Minutes 12 to 30: code the approach in order, helper functions first if the helper is the risky part. Compile early. Minutes 30 to 38: run the given example, then the empty case, the single-element case, and one case that used to break your invariant. Minutes 38 to 45: state complexity again, mention one improvement you did not implement, and stop talking yourself into a rewrite. If the slot is two problems, the first one must be done by minute 20. A perfect solution to problem one and silence on problem two loses to two correct medium solutions.

The stuck protocol. At minute 10, if you have no family, shrink the problem. Drop a constraint, solve that, and say which constraint you dropped. At minute 20, if the approach is named but the code is tangled, stop typing and rewrite the invariant in one line. Delete code that does not serve that line. At minute 30, if the idea is still incomplete, code the brute force you already believe, test it, and spend the rest on one optimization you can finish. A tested quadratic beats an untested linear sketch. Never spend the last ten minutes rewriting a working solution into a different style.

What you say while you code. Narrate decisions, not keystrokes. "I store indexes because the answer is a distance." "I walk the capacity backward so each item is used once." "I mark the cell when I enqueue it, otherwise the queue holds duplicates." Silence of a minute while you think is fine if you announce it. Silence of five minutes while the interviewer wonders whether you are stuck is how rounds die. If you want a hint, ask a precise question: "Is the graph guaranteed to be a DAG?" is a clarifying question. "Can you tell me the trick?" is a request for them to solve it. Prefer the first.

How to practice across six weeks with this course, assuming you already write ordinary Python. Week 1: foundations, arrays, hashing, and ten problems from those lessons, untimed, with the editorial only after a real attempt. Week 2: lists, stacks, recursion, backtracking, fifteen problems, and one 45-minute mock at the end. Week 3: binary search, sorts, trees, heaps, fifteen problems, two mocks. Week 4: graphs, including one weighted shortest path and one DSU problem, two mocks. Week 5: the three DP lessons, greedy, and bits, fifteen problems, two mocks. Week 6: number theory, string algorithms, the advanced techniques, the pattern catalog, and a mock every other day. The point of the early weeks is correctness and vocabulary. The point of week 6 is the clock. If a mock collapses, the after-action note names a lesson, and the next day you reread that lesson rather than collecting a new problem set.

The scorecard, out of ten, filled in after every mock before you read the editorial. One point for a restated contract and a real question about constraints. One point for a brute force and its cost. Two points for a correct approach you can justify. One point for stating complexity before the code. Two points for code that passes the example and your edge cases. One point for those edge cases actually being the dangerous ones. One point for narration the interviewer could follow. One point for either a second problem or a substantive follow-up, such as "what if the weights can be negative." A seven is a passable round. A nine is a strong one. A four with a beautiful solution you found at minute 50 is a failed slot. Write the number down. The trend is the feedback.

The after-action note has four lines and no more. What family was it. What trigger you should have heard. What bug a test would have caught. Which lesson section to reread, by name. If you missed a pattern that is on the catalog, you do not need a new resource. You need another problem from that row of the catalog, solved cold two days later. Spacing matters. Solving the same problem again the same evening mostly tests your short-term memory.

What to stop doing. Reading an editorial in the first fifteen minutes. Collecting problems into a list you never close. Rewatching a solution video at 2x and counting it as practice. Grinding near-duplicate prompts that change only a number. This course already replaced that style of drill with distinct classics. Use them. Also stop claiming a complexity you did not derive. If the interviewer asks "why is this linear" and you say "because it is a sliding window," you have not answered. The answer is "each index enters and leaves the window at most once."

A note on tools. In a shared editor you may not have your snippets. Practice without them. Type the binary-search skeleton, the BFS skeleton, and the knapsack loop from memory once a week until they are boring. You are allowed to use clear names. You are not required to compress the program into a single expression. Interview code should be readable by the person who has to decide whether to hire you.

The project conversation, briefly, because it shares the slot budget on some loops. Pick one project. Be ready to explain the data, the slow query or the bug, the measurement that showed the fix, and what you would redo. That story is not a substitute for the pattern catalog. It is the part of the loop the catalog does not cover. Four or five sentences, then a pause for their question, beats a tour of every file.

## Diagram and dry run

```mermaid
flowchart TD
    A[Minute 0: restate and constrain] --> B[Minute 3: brute force and its cost]
    B --> C[Minute 8: name the family and dry-run it]
    C --> D[Minute 12: code the invariant]
    D --> E[Minute 30: example plus edge cases]
    E --> F[Minute 38: complexity and stop]
    C --> G[Stuck at minute 10: shrink the problem]
    D --> H[Stuck at minute 20: rewrite the invariant]
    E --> I[Stuck at minute 30: submit the tested brute force]
```

A reconstructed round on "longest substring without repeating characters," with the clock.

| Minute | What you do | What you do not do |
| --- | --- | --- |
| 1 | Restate: longest contiguous slice with all distinct characters. Ask the character set and the length. | Start a nested loop in the editor |
| 4 | Brute force: every pair of endpoints, check the slice with a set. Quadratic times the alphabet, or cubic if you rescan. | Claim it is fine for length 10 to the 5th |
| 7 | Family: sliding window. Invariant: the window holds distinct characters. Move the left edge while the new character is already inside. | Reach for a suffix array |
| 11 | Dry-run "abba" or "abcabcbb" on paper. Window lengths 1, 2, 3, then a repeat forces the left edge forward. Answer 3. | Dry-run in your head only |
| 25 | Code the map from character to last index, or a frequency map. Both are fine if the invariant holds. | Rewrite twice between the two styles |
| 34 | Run the example, the empty string, a string of one character, and a string of all identical characters. | Invent a new approach because the all-identical case was boring |
| 40 | Time is linear because each index is pushed and popped at most once. Space is the alphabet. Stop. | Micro-optimize the hash |

That round scores the approach points, the code points, and the edge-case point. It loses the second-problem point because there was no time left, which is acceptable when the single problem was the hard one. If this had been the first of two mediums, minute 40 would be a failure of pacing, and the after-action note would say so.

## Runnable Python

Keep the brute-force specification next to the window, so the mock has something to test against. The recursive checker below answers "does this slice contain a duplicate" by scanning the tail. It is intentionally naive. The iterative window is the solution you code after minute 7. Use the checker on short strings when you want an oracle. Use the window in the interview.

```python
def has_repeat(s: str, left: int, right: int) -> bool:
    if left >= right:
        return False
    if s[right] in s[left:right]:
        return True
    return has_repeat(s, left, right - 1)


def longest_unique_brute(s: str) -> int:
    best = 0
    for left in range(len(s)):
        for right in range(left, len(s)):
            if has_repeat(s, left, right):
                break
            best = max(best, right - left + 1)
    return best


def longest_unique(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

On "abcabcbb" both functions return 3. On the empty string both return 0. On "aaaa" both return 1. The brute force is the one you describe at minute 4. The window is the one you code. If they disagree on a case you invented, believe neither until you dry-run that case by hand. The hand dry-run is the third implementation, and it is the one that adjudicates.

## Complexity and trade-offs

| Way of spending the 45 minutes | What the interviewer can grade | Likely score on the card |
| --- | --- | --- |
| Clarify, brute force, invariant, code, tests | the whole round | 7 to 10 if the idea is sound |
| Silent coding of a memorized solution | only the final program | high if it is the right memory, harsh if the prompt differs |
| Twenty minutes of theory, little code | communication, not execution | stuck near 4 |
| A tested quadratic when the linear form would not fit the clock | honesty and correctness | often enough, and you can name the improvement |
| A rewrite in the last eight minutes | almost nothing, the tests were wiped | the failure mode this protocol exists to prevent |

Mocks are more expensive than untimed practice and more informative per hour. Two a week is enough in the last fortnight. More than that, without after-action notes, is just fatigue. Untimed work is where you learn a proof. Timed work is where you learn whether you can find the proof under a clock. You need both, in that order.

## Tricks, tips, and patterns

Put the constraints at the top of the editor as a comment before you code. Write the function signature early so you stop solving a different problem. Keep a tiny list of edge cases you always consider: empty, one element, all equal, already sorted, reverse sorted, duplicates, negative numbers if the statement allows them, and the maximum size. Not every case applies. Choosing which ones apply is the skill. When the interviewer offers a follow-up, repeat the new constraint and say what it breaks in your current invariant before you edit. For the assessment, read all problems for two minutes and start with the one you can finish, not the one that looks impressive.

## Common mistakes and edge cases

Starting the timer and opening a tab of hints. Counting a reread of your own code as a mock. Skipping the hand dry-run because the problem felt familiar. Familiar problems are where you narrate badly, because you skip the invariant the interviewer needed to hear. Failing to ask whether indexes or values are required. Off-by-one errors you would have seen on paper. A binary search whose range does not shrink. Forgetting to reset state between tests in an assessment. Talking for fifteen minutes without a function signature. Ending the mock without the four-line note, so the next mock repeats the same miss. Treating a score of 5 as "almost" and not rereading the lesson. Five means a specific family is still cold.

## Interview notes

On the day, use the same script. Bring a blank page for the dry-run. If you blank on a pattern name, describe the invariant anyway. "Each index moves forward only" is enough to start a window even if you forget the phrase sliding window. If you finish early, ask what they would like next: a harder constraint, tests, or complexity. Do not invent a third problem they did not ask for. Thank them and stop. The catalog and the approach guide are the two pages to review the evening before, not a new chapter.

## Practice problems

Run these as mocks, one per sitting, closed notes. Stop at 45 minutes even if you are close, then write the four-line note.

1. [Minimum Window Substring](/practice/minimum-window-substring) — window, easy to over-talk.
2. [Course Schedule II](/practice/course-schedule-ii) — graph family choice in the first three minutes.
3. [Edit Distance](/practice/edit-distance) — DP table, dry-run a 3 by 3 before coding.
4. [LRU Cache](/practice/lru-cache) — design plus code, a common second half of a round.
5. [Count Subsets With Sum](/practice/count-subsets-with-sum) — forces the parameter question, n versus target.

Then one mixed pair in a single 45-minute sitting: [Valid Parentheses](/practice/valid-parentheses) and [Coin Change](/practice/coin-change). The pair is the pacing drill. The first should be done while the clock still has twenty minutes.

## Summary and cheat sheet

- A mock is closed-book and timed. The editorial comes after the note.
- Minutes 0 to 3 restate. Minutes 3 to 8 are the brute force. Minutes 8 to 12 are the hand dry-run. Then code, then edge cases, then stop.
- At minute 30, a tested simpler solution beats a rewrite.
- Score out of ten before you read the solution. Keep a four-line note: family, trigger, bug, lesson.
- Six weeks: vocabulary first, clock last. Two mocks a week near the end.
- Ask about constraints. Narrate decisions. Type the skeletons from memory.
- The assessment is silent. The live round is the same algorithms plus the script.
- Review the pattern catalog and the approach guide the evening before, then sleep.

## Further reading

- [Wikipedia — Software engineering interview](https://en.wikipedia.org/wiki/Job_interview) is broader than a coding round. Use it for the conversational half.
- [CP-Algorithms](https://cp-algorithms.com/) when an after-action note names a technique you want stated formally.
- The two companions in this course: [Interview approach](/lessons/interview-approach-guide) and [Interview patterns](/lessons/interview-patterns).
'''

emit(
    "17-patterns-interview",
    "01-interview-patterns.mdx",
    title="Twenty Interview Patterns",
    slug="interview-patterns",
    summary="A recognition index: the trigger, the invariant, and the lesson for the families that show up in coding rounds.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["advanced-techniques"],
    tags=["patterns", "interviews"],
    order=1,
    body=PATTERNS,
)
emit(
    "17-patterns-interview",
    "02-mock-interview-strategy.mdx",
    title="Mock Interviews and the 45-Minute Script",
    slug="mock-interview-strategy",
    summary="How to rehearse a live coding round: the clock, the stuck protocol, the scorecard, and the after-action note.",
    duration=30,
    difficulty="intermediate",
    prerequisites=["interview-patterns"],
    tags=["interviews"],
    order=2,
    body=MOCK,
)
