"""Recursion and backtracking."""

from emit import emit

REC = r'''
## Why this matters

Recursion is the way you state an algorithm in terms of a smaller copy of itself. Binary search, merge sort, tree walks, depth-first search, and dynamic programming all start as recurrences. An interviewer who asks for a recursive solution is asking whether you can name the base case, the smaller subproblem, and the work that combines them. An interviewer who then asks for the iterative solution is asking whether you know what the call stack was doing. You need both, and you need the cost of the tree you just defined, because a correct Fibonacci recursion is exponential and will not survive the constraints.

## Intuition

A recursive function is a worker who handles one layer and hands the rest to an identical worker. The base case is the worker who can finish without hiring anyone. If nobody is the base case, hiring continues forever. The call stack is the list of workers waiting for their hires to return. The top frame is the worker currently running. When a hire returns, the waiting worker combines the result and returns to their own boss. That picture is exactly depth-first search, and it is exactly the parenthesis frames from the expression lesson. Iteration stores the same waiting work in an explicit stack or in a handful of variables when the waiting work is simple enough.

## Core concept in depth

A recursive definition has three parts. The base case returns without a recursive call. The recursive case calls the same function on a strictly smaller input, where smaller is measured by a quantity that cannot decrease forever: n minus one, the length of a suffix, the height of a tree, the number of unset bits. The combine step uses the recursive result to build this call's result. If you cannot point at the quantity that shrinks, you do not have a proof of termination.

Linear recursion makes one recursive call. Factorial is the example: n! is 1 when n is 0, and n times (n - 1)! otherwise. The call stack reaches depth n, then unwinds, multiplying on the way back. Time is Theta(n). Stack space is Theta(n). An iterative product from 1 to n uses constant extra memory and the same multiplications. Tail recursion puts the recursive call in tail position, with the multiplication carried as an accumulator argument. Languages that optimize tail calls reuse the frame. CPython does not. A tail-recursive factorial in Python still uses linear stack. Rewrite it as a loop when the depth can be large.

Tree recursion makes more than one recursive call. Naive Fibonacci, F(n) = F(n - 1) + F(n - 2), with F(0) = 0 and F(1) = 1, is the warning label. The recursion tree has exponentially many leaves. A tight bound is Theta(phi to the n), where phi is the golden ratio, about 1.618. You can see the blow-up without the closed form: the tree of F(n) contains two copies of most subproblems. Memoization stores F(k) the first time it is computed. The recursive function with a memo array fills each k once and is Theta(n) time. The iterative version keeps only the previous two values and is Theta(n) time and Theta(1) extra memory. All three compute the same sequence. Only the last two fit a large n. This is the bridge to dynamic programming: tree recursion that overlaps is a specification, and the table is the implementation.

Binary search is linear recursion with a logarithmic depth. One call on half the range, constant work beside it. The Master theorem says Theta(log n) time. The iterative loop has the same comparisons and constant extra memory. Merge sort is tree recursion with a balanced split and a linear combine. The depth is logarithmic and the work per level is linear, so the time is Theta(n log n). The stack is logarithmic. The merge buffers are linear. Draw the tree before you quote the bound.

Mutual recursion is two functions that call each other. It is still recursion. Give both a base case and one shrinking measure that covers the pair. Indirect recursion through a callback is the same idea and the same risk of a cycle.

The recursion tree's time is proportional to the number of calls times the non-recursive work per call, unless memoization collapses duplicate calls. Space is the maximum depth, not the number of calls, because frames are freed on return. A depth-first traversal of a balanced binary tree uses logarithmic stack and linear time. The same traversal of a skewed tree uses linear stack. That distinction is an interview favorite on tree problems. An explicit stack in a loop has the same worst-case memory and avoids the language's recursion limit. Python's default limit is near one thousand frames. A recursive walk of a linked list of length 10 to the 5th will crash even though the algorithm is "linear." Mention the limit, and offer the loop.

Correctness is induction on the shrinking quantity. Assume the recursive call is correct on smaller inputs. Show that the combine step is correct, and show the base case. This is why a sloppy base case ruins the whole function: the induction has nothing to stand on. Off-by-one base cases are the usual bug in factorial, Fibonacci, and tree height.

## Diagram and dry run

```mermaid
flowchart TD
    A[Call on n] --> B{Base case?}
    B -->|Yes| C[Return the constant]
    B -->|No| D[Call on a smaller input]
    D --> E[Combine and return]
    E --> F[Frame is popped]
```

Naive Fibonacci calls for n = 4. Count the calls of each argument.

| Argument | Number of calls |
| --- | --- |
| 4 | 1 |
| 3 | 1 |
| 2 | 2 |
| 1 | 3 |
| 0 | 2 |

Nine calls to get a number you can compute with a loop of length 4. Memoized Fibonacci calls each argument once: five calls, plus the constant-time lookups when a duplicate is requested. Iterative Fibonacci stores only F(2) and F(3) while it computes F(4) = 3. The sequence is 0, 1, 1, 2, 3.

Factorial of 4 unwinds as 4 times factorial of 3, which is 3 times factorial of 2, which is 2 times factorial of 1, which is 1 times factorial of 0, which is 1. The products on the way back are 1, 1, 2, 6, 24.

## Runnable Python

Three Fibonaccis: the exponential specification, the memoized recursion, and the loop. Factorial is shown as a loop and as a recursion so the stack difference is visible in the source.

```python
def fib_naive(n: int) -> int:
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n: int) -> int:
    memo = [-1] * (n + 1)

    def go(k: int) -> int:
        if k < 2:
            return k
        if memo[k] != -1:
            return memo[k]
        memo[k] = go(k - 1) + go(k - 2)
        return memo[k]

    return go(n)


def fib_loop(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def factorial_rec(n: int) -> int:
    if n == 0:
        return 1
    return n * factorial_rec(n - 1)
```

`fib_loop(10)` is 55. `fib_memo(10)` is 55. Do not call `fib_naive` on anything past the mid-thirties. `factorial_rec(5)` is 120. The loop form multiplies `answer *= k` from 1 through n and never nests frames.

## Complexity and trade-offs

| Algorithm | Time | Extra space |
| --- | --- | --- |
| Iterative factorial | Theta(n) | Theta(1) |
| Recursive factorial | Theta(n) | Theta(n) stack |
| Naive Fibonacci | Theta(phi to the n) | Theta(n) stack |
| Memoized Fibonacci | Theta(n) | Theta(n) |
| Iterative Fibonacci | Theta(n) | Theta(1) |
| Recursive binary search | Theta(log n) | Theta(log n) stack |
| Iterative binary search | Theta(log n) | Theta(1) |

Memoization trades memory for the removal of duplicate calls. It does not help a recursion tree that has no duplicates, such as generating every subset. That tree really does have 2 to the n leaves, and you must visit them if the output requires them. Do not memoize a function whose arguments include a mutable structure you also mutate, unless the key captures the state. That bug returns a stale answer.

## Tricks, tips, and patterns

Write the base case first. Name the quantity that shrinks. If you see two recursive calls on n - 1 and n - 2, or on overlapping subarrays, assume you will need a table. If the recursion is tail-shaped, write the loop. If the depth can exceed a few thousand, write the loop or an explicit stack. For trees, the base case is a null node. For arrays, the base case is an empty range or a one-element range. Induction is the proof. A dry run of n = 4 is the check that the base case lines up.

## Common mistakes and edge cases

No base case, or a base case that is not reached because the step goes from n to n without shrinking. Fibonacci that returns 1 for n = 0. Factorial of a negative number, which must be rejected. Integer overflow in languages with fixed-width integers. In Python the integer grows, and the time of the multiplication is no longer constant once the numbers have n bits. For interview factorial and Fibonacci on small n, you may treat arithmetic as constant and say so. Recursion past the interpreter limit. Memo arrays sized n instead of n + 1. Sharing a memo between tests without clearing it. Printing during the unwind and thinking the print order is the call order. The call order is the way down. The print-after-call order is the way up.

## Interview notes

State base case, subproblem, and combine, in that order. Then the complexity, including stack. If the tree overlaps, say you would memoize or iterate. Offer the loop when the stack is the only reason the recursive code is risky. Dry-run a small n and point at which calls are duplicates. Do not start coding naive Fibonacci as a final answer for "compute the nth Fibonacci number" when n can be large. It is the right first sentence and the wrong last one.

## Practice problems

1. [Fibonacci Number](/practice/fibonacci-number) — write the loop.
2. [Climbing Stairs](/practice/climbing-stairs) — the same recurrence with a different base.
3. [Pow(x, n)](/practice/powx-n) — halve the exponent. Write the recurrence and the Master-theorem case.
4. [Merge Two Sorted Lists](/practice/merge-two-sorted-lists) — the recursive combine is one call, not two.

## Summary and cheat sheet

- Base case, strictly smaller subproblem, combine step. That is the whole definition.
- Time follows the recursion tree. Space follows the depth, not the number of calls.
- Linear recursion of depth n is a loop in disguise. Tree recursion may be exponential.
- Overlapping subproblems get a memo or a table. That is dynamic programming.
- CPython does not optimize tail calls. Deep recursions should be loops.
- Prove correctness by induction on the shrinking quantity.

## Further reading

- [Wikipedia — Recursion (computer science)](https://en.wikipedia.org/wiki/Recursion_(computer_science))
- [Wikipedia — Call stack](https://en.wikipedia.org/wiki/Call_stack)
- [Wikipedia — Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_sequence)
- [Python's recursion limit is documented with sys.setrecursionlimit](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)
'''

BACK = r'''
## Why this matters

Backtracking is depth-first search over a space of decisions, with the courage to undo a decision that did not work. Subsets, permutations, combination sums, parentheses, word search, and N-Queens are this algorithm with different choices and different prune rules. The template is short. The skill is choosing the state, knowing when to record an answer, and restoring the state exactly. Dynamic programming later replaces some of these trees with tables when the question is a count or a feasibility bit rather than the list of objects. If the question asks for the objects, you still walk the tree.

## Intuition

You are walking a maze and carrying a pencil. At each junction you pick a corridor, draw a mark, and go deeper. If the corridor is a dead end you erase the mark and try the next corridor. The mark is the partial solution. Erasing it is the undo. You never need a copy of the maze for each path if the undo is perfect, because the maze plus the current marks are the whole state. Forgetting to erase a mark makes a later path inherit a wall it did not build. That bug is the source of almost every wrong backtracking submission.

## Core concept in depth

The template has four parts. The state is the partial solution and whatever index or used-set the next choice needs. The base case records a copy of the partial solution when it is complete, or returns a boolean when the problem is a search for one success. The loop tries each legal choice. Making a choice updates the state, the recursive call explores, and the undo reverses the update. The undo must run on the way back, including when the recursive call found nothing. In Python, append and pop on a shared path list are the usual update and undo. If you pass `path + [choice]` you are copying instead of undoing. That is correct and spends extra time and memory. The in-place version is the one to analyze as Theta(depth) extra memory beyond the output.

Subsets of an array. The decision at index i is to skip nums[i] or to take it. The index moves forward either way, so each element is considered once and there is no duplicate work on the same subset. There are 2 to the n subsets. Building each costs time proportional to its length, so the total time is Theta(n times 2 to the n). If the array contains duplicates and the problem wants unique subsets, sort first and, in the take-or-skip loop over a range, skip a value that equals the previous value when the previous value was not taken at this level. That is the subsets-II prune. Combination sum, where each candidate may be reused, recurses on the same index after a take, and moves forward after a skip, or equivalently loops from a start index and recurses on i rather than i + 1. Combination sum II does not reuse, and it uses the duplicate skip.

Permutations. The choice is any unused element. A boolean array, or a set, marks what is used. You can also swap the current position with each later index, recurse, and swap back. The swap version uses no extra used-array. There are n! permutations. Generating them all is Theta(n times n!) because each permutation is written down. Duplicates in the input need a sort and a skip of identical unused values, or a frequency map, so you do not emit the same permutation twice.

Generate parentheses of n pairs. The state is the counts of open and close already used. You may write an open parenthesis when open is less than n. You may write a close parenthesis when close is less than open. That prune is also the proof that every string you emit is valid, and that you emit all of them. The number of such strings is the Catalan number. You do not need the formula to generate them.

Word search on a grid is backtracking with a board mutation. From a cell that matches the next character, mark the cell as used, try four neighbors, and unmark the cell. The mark can be a temporary character replacement so you do not need a parallel visited matrix. Forgetting the unmark lets one path consume a letter that another path needed. The time is exponential in the word length in the worst case, bounded by the branching factor 4, and the grids in interviews are small. Prune when the remaining suffix cannot be built, if you want a faster practical search. The worst-case bound does not become polynomial.

N-Queens places a queen per row. The choice is the column. Three sets prune: occupied columns, occupied diagonals of row - col, and occupied diagonals of row + col. A placement that hits a set is skipped. At row n you have a solution. Counting solutions is the same tree without storing the boards. The template does not change. Only the prune changes.

Letter case permutations and restore-IP-addresses are the same tree with different alphabets. IP addresses add a numerical prune: a segment has 1 to 3 digits, no leading zero except the number 0 itself, and a value at most 255. Prunes belong in the choice loop, before the recursive call, so you do not pay a call to discover them.

Iterative backtracking uses an explicit stack of frames, each frame holding the index of the next choice to try. It is how you remove recursion-depth risk. It is harder to read. Write the recursive form unless the depth can exceed the interpreter limit. Subsets of 20 elements have depth 20. N-Queens for n = 12 has depth 12. Word search depth is the word length. These fit.

When the problem asks for a count rather than the list, the same tree can often become dynamic programming. Count subsets with a given sum, for n around 20, is meet-in-the-middle or a knapsack table. For n around 40, the table may not fit and the split enumeration does. Backtracking is the right tool when you must list structures with constraints that do not collapse into a small state.

## Diagram and dry run

```mermaid
flowchart TD
    A[Partial path] --> B{Complete?}
    B -->|Yes| C[Copy the path into the answers]
    B -->|No| D[Try the next legal choice]
    D --> E[Apply the choice]
    E --> F[Recurse]
    F --> G[Undo the choice]
    G --> D
```

Subsets of 1, 2. The path is a list. Order is skip-then-take, or take-then-skip. Here the loop tries taking from the start index onward, which yields combinations in lexicographic order.

| Call | Start index | Path | Action |
| --- | --- | --- | --- |
| 1 | 0 | empty | record the empty subset, then try 1 and 2 |
| 2 | 1 | 1 | record 1, then try 2 |
| 3 | 2 | 1, 2 | record 1, 2, no further choices |
| 4 | 2 | 2 | record 2, after the undo of 1 |

The undo after call 3 pops 2 and then pops 1 before call 4 pushes 2. If you forget the pop, call 4 starts from 1, 2 and appends another 2. The answers are empty, then 1, then 1 2, then 2. Four subsets, which is 2 to the n.

Parentheses for n = 2. The legal strings are (()) and ()(). An open is allowed twice. A close is allowed only when it does not exceed the opens. The illegal prefix ) is never attempted.

## Runnable Python

The subset generator uses append and pop. The recursive structure is the algorithm. An iterative generator of subsets by bit masks is the non-recursive twin: each mask from 0 to 2^n - 1 selects the elements whose bits are set. Both are included.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        out.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return out


def subsets_bits(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    n = len(nums)
    for mask in range(1 << n):
        out.append([nums[i] for i in range(n) if mask & (1 << i)])
    return out
```

On 1, 2 both return four subsets. The order differs. If the contract demands a sorted list of subsets, sort the output. The bit version is iterative and uses no call stack. It does not generalize to "permutations with pruning" as cleanly as the depth-first search does. Use bits when every subset is legal. Use backtracking when most branches die early.

## Complexity and trade-offs

| Search | Leaves | Time to list them | Extra space besides the output |
| --- | --- | --- | --- |
| Subsets | 2 to the n | Theta(n times 2 to the n) | Theta(n) path |
| Permutations | n! | Theta(n times n!) | Theta(n) |
| Combination sum, bounded | depends on the target | exponential in the target or in n | Theta(target) depth |
| Parentheses, n pairs | the Catalan number | proportional to the output | Theta(n) |
| Word search | up to 4 to the length | exponential in the word | Theta(length) |
| N-Queens | pruned, still exponential | fine for small n | Theta(n) |

Copying the path at the base case is required if the path list is reused. Appending the path object itself stores a pointer to a list you will mutate later, and every answer becomes the final path. That bug looks like "all answers are identical." Sort or unique only when the statement asks. Pruning duplicate choices is better than generating duplicates and stuffing them into a set, because the set hides an exponential amount of wasted work.

## Tricks, tips, and patterns

Pass a start index when order does not matter, so you generate combinations rather than permutations. Pass a used array when order matters. Undo immediately after the recursive call, in a finally-shaped pattern you do not actually need a finally for, as long as every return path undoes. In Python, do not return inside the loop before the pop unless you are searching for the first success and you are done with the path. If you return true up the stack, you may skip the undo. That is acceptable only when you will not use the board again. If the caller needs the board restored, undo on the success path too. For counts, return an integer sum of the recursive calls instead of storing lists. The tree stays the same and the memory drops.

## Common mistakes and edge cases

Forgetting to copy the path. Forgetting to pop. Skipping the start index and generating permutations of a combination problem, which times out or duplicates. Allowing a leading zero in an IP segment. Placing a close parenthesis before an open one. Marking a grid cell and not unmarking it. Sorting the input for duplicate-skipping but still using index equality wrong, so the first duplicate is skipped as well. An empty input has one subset, the empty subset, not zero subsets. Permutations of an empty list: one empty permutation. Combination sum with a target of 0: one empty combination, if the statement allows it. Usually the target is positive and the empty combination is not an answer. Read it. N-Queens for n = 1 is one solution. N = 2 and n = 3 are zero.

## Interview notes

Write the template on the side, then fill in the choice and the prune. Say "I append, recurse, and pop" so the undo is a commitment. Estimate the number of leaves before you claim the runtime. If the estimate is 2 to the 40, stop and look for dynamic programming or meet-in-the-middle. Dry-run subsets of two elements, including the pop. If the problem asks for a count, ask yourself whether the state can be compressed. If it asks for the listings, do not force a table. Mention the bit mask twin for subsets. It is a good sign you know the shape of the space.

## Practice problems

1. [Subsets](/practice/subsets) and [Subsets II](/practice/subsets-ii).
2. [Permutations](/practice/permutations) and [Permutations II](/practice/permutations-ii).
3. [Combination Sum](/practice/combination-sum) and [Combination Sum II](/practice/combination-sum-ii).
4. [Generate Parentheses](/practice/generate-parentheses).
5. [Word Search](/practice/word-search) and [N-Queens II](/practice/n-queens-ii).
6. [Letter Combinations of a Phone Number](/practice/letter-combinations-of-a-phone-number) and [Restore IP Addresses](/practice/restore-ip-addresses).
7. [Palindrome Partitioning](/practice/palindrome-partitioning).

## Summary and cheat sheet

- Backtracking is depth-first search that undoes. Apply, recurse, undo.
- Copy the path when you record it. Pop what you appended.
- Combinations use a start index. Permutations use a used-set or swaps.
- Prune duplicates after sorting, and prune illegal parentheses with counts.
- Grid search marks and unmarks. N-Queens tracks columns and both diagonals.
- Time follows the number of partial solutions you actually visit.
- Listing subsets is n times 2 to the n. If you only need a count with numeric structure, look for a table.

## Further reading

- [Wikipedia — Backtracking](https://en.wikipedia.org/wiki/Backtracking)
- [Wikipedia — Eight queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle)
- [CP-Algorithms, permutations](https://cp-algorithms.com/combinatorics/permutations.html)
'''

emit(
    "06-recursion-backtracking",
    "01-recursion.mdx",
    title="Recursion and the Call Stack",
    slug="recursion",
    summary="Base cases, linear versus tree recursion, and why overlapping Fibonacci becomes a loop.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["expression-evaluation"],
    tags=["recursion", "call-stack"],
    order=1,
    body=REC,
)
emit(
    "06-recursion-backtracking",
    "02-backtracking.mdx",
    title="Backtracking",
    slug="backtracking",
    summary="The choose, explore, and undo template for subsets, permutations, grids, and N-Queens.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["recursion"],
    tags=["backtracking", "dfs", "search"],
    order=2,
    body=BACK,
)
