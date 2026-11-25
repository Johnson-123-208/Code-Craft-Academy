"""Foundations lessons: complexity, amortization, Master theorem, approach."""

from emit import emit

BIG_O = r'''
## Why this matters

Complexity is the language interviewers use to decide whether a solution will survive real input sizes. A service that is fine on a demo of a few hundred rows can time out when the same code meets a few million. At the 15 to 20 LPA bar, stating a correct bound is not a footnote you add after the code. It is part of the design. You are expected to compare a brute force idea with an improved one, name the bottleneck, and say what you would pay in memory to remove it.

The same skill shows up after the interview. Capacity planning, choosing an index, and deciding whether a nightly job can be a nested loop are all complexity arguments. If you can only say "this looks fast," you cannot defend the choice when the data grows. Big-O, Big-Omega, and Big-Theta give you a way to talk about growth without arguing about a laptop's clock speed.

## Intuition

Picture a stadium emptying after a match. If each person walks to the nearest gate without waiting on anyone else, the time grows with the number of people. Double the crowd and the exit takes about twice as long. That is linear growth. If every person must shake hands with every other person before leaving, doubling the crowd roughly quadruples the handshakes. That is quadratic growth. Binary search is the opposite kind of story: each question throws away half of the remaining possibilities, so a huge sorted list still takes only a handful of comparisons.

Asymptotic notation deliberately ignores the exact number of seconds. It answers a different question: if the input size n grows without bound, which term dominates? A program that does 3n + 100 additions and a program that does n additions are in the same class, because the 3 and the 100 stop mattering next to the growth of n. Constants still matter when you tune a hot loop in production. They do not matter when you are choosing between a linear scan and a quadratic scan for large n. The doubling test is the practical version of this idea. If doubling n doubles the time, think linear. If it multiplies the time by about four, think quadratic. If the time barely moves, think logarithmic or constant.

## Core concept in depth

Fix a function T(n) that counts the primitive steps of an algorithm on an input of size n. We say T(n) is O(f(n)) when there exist constants c greater than 0 and n0 such that for every n at least n0, T(n) is at most c times f(n). This is an upper bound. It says the cost does not grow faster than f, up to a constant factor, once n is large enough. It does not say the bound is tight. A linear scan is O(n), and it is also O(n squared), because a looser upper bound is still a true upper bound. Interviewers usually want the tightest simple bound you can justify.

T(n) is Omega(f(n)) when there exist constants c greater than 0 and n0 such that for every n at least n0, T(n) is at least c times f(n). This is a lower bound. It says the algorithm must do at least this much work on the inputs you are considering. T(n) is Theta(f(n)) when it is both O(f(n)) and Omega(f(n)). Theta is the tight bound. When you say "merge sort is Theta of n log n," you mean the leading term really is n log n, not merely that n log n is some safe overestimate.

You must also say which inputs the bound talks about. Best case is the cheapest input of size n. Worst case is the most expensive. Average case is the expectation over a stated distribution, often uniform random inputs or random pivots. Quicksort is the classic reminder: with a good pivot it is Theta of n log n on average, and with consistently terrible pivots it is Theta of n squared in the worst case. A hash table lookup is expected constant time under a good hash, and linear in the worst case when every key collides. If you say "hash maps are O(1)" without the word expected, a strong interviewer will ask you to repair the sentence.

The model behind these counts is a random-access machine: reading an array slot, adding two words, comparing two words, and following a pointer are constant-time primitives, as long as the words fit in a machine word. A loop that runs n times around a constant body is Theta(n). Two sequential loops add. Two nested loops over the same n multiply. A loop that halves a range each iteration, such as low to high in binary search, runs Theta(log n) iterations. Recursion needs a recurrence. A function that does linear work and then solves two halves has the shape T(n) = 2 T(n/2) + Theta(n). The Master theorem, treated in its own lesson, solves that to Theta(n log n).

Space complexity counts extra memory, not the input itself, unless the problem asks you to count the whole footprint. An in-place partition uses Theta(1) extra words. A hash set of the input uses Theta(n) extra words. Recursion uses stack frames. A recursive depth-first traversal of a skewed tree can use Theta(n) stack space even when the algorithm looks "in place." Output size counts when you materialize it: returning every pair of an array is Theta(n squared) space no matter how clever the loop is.

Little-o and little-omega are strict versions. T(n) is o(f(n)) when T(n) / f(n) goes to 0. You will rarely need the little forms in an interview, but they explain why we drop lower-order terms: n is o(n log n), and n log n is o(n squared).

## Diagram and dry run

```mermaid
flowchart TD
    A[Count primitive steps T of n] --> B{Which bound?}
    B -->|Upper| C[Big-O: T stays under c times f]
    B -->|Lower| D[Big-Omega: T stays above c times f]
    B -->|Both| E[Big-Theta: the bound is tight]
    E --> F{Which inputs?}
    F --> G[Best case]
    F --> H[Worst case]
    F --> I[Average case under a stated distribution]
```

The next table counts additions in a double loop, `s += 1` inside `for i in range(n)` and `for j in range(n)`, and compares that with a loop that only runs to i. For n = 4 the full square does 16 additions. The triangular loop does 0 + 1 + 2 + 3 = 6 additions, which is n(n-1)/2 and still Theta(n squared).

| n | Full n by n additions | Triangular additions | Binary-search comparisons on a sorted array of n, worst case |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 4 | 1 | 2 |
| 4 | 16 | 6 | 3 |
| 8 | 64 | 28 | 4 |
| 16 | 256 | 120 | 5 |

Doubling n multiplies the square by four and adds only one comparison to the binary search. That single picture is worth more than a memorized formula.

## Runnable Python

The first routine is the iterative search you should be able to write without hesitation. The second is the same algorithm in recursive form. Both return the index or -1. The comparison counter makes the logarithmic bound visible.

```python
def binary_search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_rec(nums: list[int], target: int, lo: int, hi: int) -> int:
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        return binary_search_rec(nums, target, mid + 1, hi)
    return binary_search_rec(nums, target, lo, mid - 1)
```

On a sorted array of a million elements the loop body runs at most twenty times, because 2 to the 20th is about a million. The recursive version does the same work and also uses Theta(log n) stack frames. Prefer the loop unless the recursive shape makes the invariant clearer.

## Complexity and trade-offs

| Procedure | Best time | Worst time | Extra space |
| --- | --- | --- | --- |
| Scan an unsorted array | Theta(1) if the target is first | Theta(n) | Theta(1) |
| Iterative binary search | Theta(1) if the middle hits | Theta(log n) | Theta(1) |
| Recursive binary search | Theta(1) | Theta(log n) | Theta(log n) stack |
| Double loop over the array | Theta(n squared) | Theta(n squared) | Theta(1) |
| Build a hash set, then scan | Theta(n) expected | Theta(n squared) if every hash collides | Theta(n) |

The hash-set row is the trade you will make constantly. Two Sum is quadratic if you try every pair, and expected linear if you store values you have already seen. You pay linear memory for that speed. Say so. Also say that Python's sort is Theta(n log n) worst case, so sorting in order to binary search is Theta(n log n), not Theta(log n). The sort dominates.

## Tricks, tips, and patterns

Drop constant factors and lower-order terms when you name the class: 5n + n log n + 40 is Theta(n log n). Add sequential independent loops and multiply nested loops that each run with the full size. A loop whose counter doubles, or whose range halves, is logarithmic. Recursion depth is space. Early returns improve the best case and usually do not improve the worst case, so do not advertise the early return as the complexity of the algorithm. When a library call sits inside a loop, expand it. `in` on a list is linear. `in` on a set is expected constant time. `sorted` is linearithmic. String concatenation in a loop can be quadratic if each addition copies the whole string. Collect pieces and join them once.

The doubling question is a good sanity check when you are unsure: "If n becomes 2n, what happens to the number of inner-loop executions?" If you cannot answer, you do not have a bound yet.

## Common mistakes and edge cases

The most common mistake is hiding a linear scan inside another linear scan and still calling the result linear. Another is claiming that sorting is free. A third is quoting the average case of quicksort or of hashing as if it were a worst-case guarantee. A fourth is forgetting the output. Generating all subsets is Theta(n times 2 to the n) time simply because there are that many subsets to write down. A fifth is using the best case as the answer to "what is the complexity?" Interviewers mean worst case unless they say otherwise.

Empty inputs are Theta(1) for most scans, and they are a good test that your bound's n0 story still has a defined algorithm at n = 0. Overflow of the midpoint in languages with fixed-width integers is not a complexity issue, but it is the usual companion bug of binary search. In Python the midpoint arithmetic is safe. The infinite loop from updating lo or hi incorrectly is not safe in any language, and a wrong update can turn a logarithmic algorithm into a non-terminating one. Complexity statements assume termination.

## Interview notes

Lead with the bound you will actually defend, then the reason. A clean sentence is: "The outer loop runs n times and the inner two-pointer scan together moves each endpoint at most n times, so the total is Theta(n squared) time and Theta(1) extra memory." If you improved a quadratic brute force, say what the brute force was and which observation removed a factor of n. Mention average versus worst when the structure is a hash table, a balanced tree, or quicksort. Mention stack space when the elegant solution is recursive. If the interviewer asks you to go faster, the honest answers are a tighter bound you missed, a data-structure trade, or a statement that the problem has a known lower bound, such as comparison sorting requiring Omega(n log n) comparisons in the worst case.

Do not invent a linear sort for arbitrary comparable objects. Do not say "O of n log n or better" as a way to avoid choosing. Pick the bound, then discuss constant factors only if two algorithms share a class.

## Practice problems

Use these as complexity drills. Write the brute force, name its bound, then write the improved solution and name the new bound and the extra memory.

1. [Two Sum](/practice/two-sum) — pairs versus a hash map.
2. [Contains Duplicate](/practice/contains-duplicate) — sort, or a set.
3. [Maximum Subarray](/practice/maximum-subarray) — every subarray versus Kadane's one pass.
4. [Climbing Stairs](/practice/climbing-stairs) — the exponential recursion versus the linear recurrence.
5. [Binary Search](/practice/binary-search) — write both the loop and the recurrence T(n) = T(n/2) + Theta(1).

## Summary and cheat sheet

- Big-O is an upper bound, Big-Omega is a lower bound, and Big-Theta means both.
- Always attach the bound to best, worst, or average case. Average case needs a distribution.
- Nested full passes multiply. Sequential passes add. Halving is logarithmic.
- Space includes auxiliary structures and the call stack, and output size when you build it.
- Hashing is expected constant time, not a worst-case promise.
- Sorting arbitrary comparable items is Theta(n log n) in the worst case for comparison sorts.
- Drop constants when naming the class. Keep them when you are tuning inside one class.

## Further reading

- [Wikipedia — Big O notation](https://en.wikipedia.org/wiki/Big_O_notation)
- [Wikipedia — Best, worst and average case](https://en.wikipedia.org/wiki/Best,_worst_and_average_case)
- [Python TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity)
- [CLRS, Introduction to Algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
'''

AMORTIZED = r'''
## Why this matters

Some operations are usually cheap and occasionally expensive. A dynamic array append is the everyday example: most appends write one slot, and every so often the array allocates a bigger buffer and copies everything. If you quote only the expensive copy, append looks linear and unusable. If you quote only the cheap write, you are hiding the copy. Amortized analysis is the third answer. Across a long sequence of operations, the expensive ones are rare enough that the average cost per operation is constant. Interviewers ask about this whenever a resizable array, a hash table resize, a splay tree, or a two-stack queue shows up. It is also the right way to talk about the cost of n appends in Python's list.

## Intuition

Suppose a coffee shop gives you a stamp card. Nine coffees are a quick swipe, and the tenth is free but the cashier spends a long time resetting the card. Looking only at the tenth customer, service looks slow. Looking at ten customers together, the reset is one extra piece of work spread over ten sales. Amortized cost is that long-run average. It is not the same as average-case complexity. Average-case talks about random inputs. Amortized analysis talks about a worst-case sequence of operations. The adversary can force the resize to happen. The adversary cannot force every single append to resize, because a geometric resize pays for itself with the cheap appends that follow.

## Core concept in depth

There are three standard methods, and they prove the same style of statement.

Aggregate analysis sums the total cost of a sequence of n operations and divides by n. If the total is at most c n, each operation has amortized cost c. For a dynamic array that doubles when it is full, the copies of an element happen at sizes 1, 2, 4, and so on. An element is copied O(log n) times if you look at one element over the whole life of the array, but the aggregate argument is cleaner: the total number of element-copies across n appends is at most 1 + 2 + 4 + ... + n, which is less than 2n. Plus n writes into empty slots, the whole sequence costs less than 3n element moves. Divide by n and each append is amortized Theta(1), even though some individual append is Theta(n).

The accounting method assigns a charge that may differ from the actual cost. Cheap operations pay a little extra, and that extra is stored as credit on the data structure. Expensive operations spend the credit. For doubling arrays, charge 3 units for each append. One unit pays for writing the new element. Two units are saved as credit on that element. When a resize copies the element into a new buffer, the copy spends one unit of its credit, and the other unit remains so the element can be copied again after the next doubling, or you can retune the charge. The usual textbook charge is: each append pays 3, the write uses 1, and 2 are deposited. A resize of k live elements finds 2k credits because those elements were inserted after the previous resize, and the copy costs k, so the credits cover it. No operation's bank balance goes negative, therefore the sum of charges is an upper bound on the sum of actual costs. The amortized cost is the charge, which is 3, a constant.

The potential method stores the credit in a function of the whole structure instead of on individual objects. Let Phi be the potential. Define the amortized cost of an operation as its actual cost plus the change in potential. Summing over a sequence, the potentials telescope: the sum of amortized costs equals the sum of actual costs plus Phi at the end minus Phi at the start. If Phi ends at least as high as it started, the amortized sum upper-bounds the actual sum. For a doubling array, a good potential is twice the number of occupied slots minus the capacity, or zero when that quantity is negative. An ordinary append increases the potential by 2 and does 1 unit of real work, so its amortized cost is 3. A doubling append copies n elements, the capacity jumps, and the potential drops enough to cancel the copy. You do not need to memorize one magic formula. You need to know that potential is a Lyapunov function for credit: it rises on cheap steps and falls on expensive steps, and it never has to go below its starting value.

A binary counter that starts at zero and is incremented n times is the other classic aggregate proof. Incrementing flips a trailing run of ones to zeros and flips one zero to one. Across n increments, bit 0 flips every step, bit 1 flips every second step, bit 2 every fourth step. The total flips are at most n + n/2 + n/4 + ... which is less than 2n. Each increment is amortized Theta(1) bit flips even though one increment can flip Theta(log n) bits.

A queue built from two stacks has the same shape. Push onto the inbox is Theta(1). Pop either pops the outbox or pours the entire inbox onto the outbox and then pops. Each element is pushed once, moved once, and popped once, so n operations move each element O(1) times. Any single pop can be linear. The sequence is amortized linear in n, which is amortized constant per operation.

## Diagram and dry run

```mermaid
flowchart LR
    A[Append into a dynamic array] --> B{Room in the buffer?}
    B -->|Yes| C[Write one slot. Actual cost 1]
    B -->|No| D[Allocate double capacity and copy]
    D --> E[Credit from earlier appends pays for the copy]
    C --> F[Amortized cost stays constant]
    E --> F
```

Start with capacity 1. Append the letters A, B, C, D, E. A resize copies every currently live element into the new buffer.

| Append | Value | Capacity before write | Elements copied on this append | Actual element moves | Credit deposited if we charge 3 |
| --- | --- | --- | --- | --- | --- |
| 1 | A | 1, already full, grow to 1 | 0, then write A | 1 | 3 |
| 2 | B | 1, grow to 2, copy A | 1 | 2 | 3 |
| 3 | C | 2, room | 0 | 1 | 3 |
| 4 | D | 2, grow to 4, copy A B C | 3 | 4 | 3 |
| 5 | E | 4, room | 0 | 1 | 3 |

Total actual moves: 1 + 2 + 1 + 4 + 1 = 9. Total charges: 15. The charges dominate the actual cost, which is what an upper bound must do. The copies are 0, 1, and 3, a geometric series, not five full copies.

## Runnable Python

This instrumented list doubles by hand so you can see the copy count. The recursive function is not a natural fit for amortization, so the second routine is the two-stack queue, whose pop is the occasionally expensive operation. Both are worth implementing until the credit story feels mechanical.

```python
class DoublingArray:
    def __init__(self) -> None:
        self._data = [None]
        self._size = 0
        self.copies = 0

    def append(self, value: object) -> None:
        if self._size == len(self._data):
            grown = [None] * (len(self._data) * 2)
            for i in range(self._size):
                grown[i] = self._data[i]
                self.copies += 1
            self._data = grown
        self._data[self._size] = value
        self._size += 1


class TwoStackQueue:
    def __init__(self) -> None:
        self._inbox: list[object] = []
        self._outbox: list[object] = []

    def push(self, value: object) -> None:
        self._inbox.append(value)

    def pop(self) -> object:
        if not self._outbox:
            while self._inbox:
                self._outbox.append(self._inbox.pop())
        return self._outbox.pop()
```

After n appends on the doubling array, `copies` stays below n. After n pushes and n pops on the queue, each element moves from the inbox to the outbox at most once.

## Complexity and trade-offs

| Structure | Worst single operation | Amortized cost over n operations | Extra space |
| --- | --- | --- | --- |
| Doubling dynamic array append | Theta(n) on resize | Theta(1) | Theta(n) for the buffer |
| Increment a binary counter | Theta(number of bits) | Theta(1) | Theta(log n) bits |
| Two-stack queue push | Theta(1) | Theta(1) | Theta(n) |
| Two-stack queue pop | Theta(n) when the outbox is empty | Theta(1) | Theta(n) |
| Hash table insert with doubling | Theta(n) on rehash | Theta(1) expected, before hashing collisions | Theta(n) |

Growing by a constant amount, such as adding 10 slots each time, destroys the argument. The copies become n/10 + 2n/10 + ... which sums to Theta(n squared) for n appends, so each append is amortized linear. The growth factor must be a constant strictly greater than 1. Doubling is the usual choice. Growing by 1.5 also works and copies less aggressively. Shrinking has a matching trap: if you shrink as soon as the array is half empty and double as soon as it is full, an adversary can oscillate around the boundary and force a copy every operation. Shrink only when the array is about a quarter full, so that a grow and a shrink cannot chase each other.

Amortized bounds are not worst-case latency bounds. A real-time system that cannot accept a linear pause should use a structure with a strict worst-case constant, or it should spread the copy over later operations. That technique is called incremental resizing. It is more code, and it is the right follow-up if an interviewer says the pause is unacceptable.

## Tricks, tips, and patterns

If the expensive event happens every time the size doubles, sum a geometric series. The sum of 1 + 2 + 4 + ... + n is less than 2n, so the total is linear and the average is constant. If you are asked to prove it cleanly, pick aggregate analysis first and mention accounting or potential as the method you would use to assign the cost to individual operations. Multipop on a stack, where one call may pop several items but each item is popped at most once, is the same aggregate idea. A token you place on an object when it is inserted, and remove when it is deleted or moved, is an accounting proof in physical form.

## Common mistakes and edge cases

Do not say "append is O(1) worst case" for a dynamic array. Say amortized. Do not confuse amortized with average-case. The doubling proof does not require random data. Do not grow by a fixed number of slots and expect a constant amortized cost. Do not shrink at the same threshold where you grow. Do not forget that a sequence of n amortized-constant operations is Theta(n) total, which is usually what a caller needs. An empty pop on the two-stack queue is an error, not an amortized event. State the precondition.

Python's list follows this doubling strategy. Appending n items is Theta(n) total. Inserting at the front of a list is Theta(n) each time, because every later item shifts, and amortization does not save you. Use a deque when both ends must be cheap.

## Interview notes

A strong answer to "what does amortized mean?" is one sentence plus one example. The sentence: across any sequence of operations, the average cost is bounded, even if a particular operation is expensive. The example: doubling array, total copies less than 2n, therefore append is amortized constant. If they ask for a proof method, name aggregate, accounting, and potential, and walk aggregate on the board. If they ask about worst-case latency, acknowledge that amortized constant is not worst-case constant, and mention incremental growth as the remedy. The two-stack queue is a common follow-up. Implement it, then explain why each element crosses at most once.

## Practice problems

1. [Min Stack](/practice/min-stack) — a second stack keeps the minimum, and every push and pop is worst-case constant, which is stronger than amortized.
2. [LRU Cache](/practice/lru-cache) — ordered dictionary operations are amortized constant in Python. Be ready to say that.
3. [LFU Cache](/practice/lfu-cache) — frequency buckets need the same constant-time move story.
4. [Sliding Window Maximum](/practice/sliding-window-maximum) — each index enters and leaves the deque once, an aggregate argument.
5. [Online Stock Span](/practice/online-stock-span) — each day is pushed and popped at most once.

## Summary and cheat sheet

- Amortized cost is the average over a worst-case sequence, not a random-input average.
- Aggregate: sum the costs, divide by n.
- Accounting: charge extra on cheap steps and spend it on expensive steps.
- Potential: store the credit in a function that telescopes.
- Doubling arrays, binary counters, and two-stack queues are amortized constant per operation.
- Grow by a constant factor. Do not shrink at the grow threshold.
- Amortized constant does not promise a constant pause.

## Further reading

- [Wikipedia — Amortized analysis](https://en.wikipedia.org/wiki/Amortized_analysis)
- [Wikipedia — Dynamic array](https://en.wikipedia.org/wiki/Dynamic_array)
- [Python TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity)
- [CLRS, Introduction to Algorithms, amortization chapter](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
'''

emit(
    "01-foundations",
    "01-big-o-and-complexity.mdx",
    title="Big-O, Theta, Omega, and How to Think About Complexity",
    slug="big-o-and-complexity",
    summary="Formal upper, lower, and tight bounds, best versus worst versus average case, and the loop rules interviewers expect.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["python-intro-and-setup"],
    tags=["big-o", "complexity", "foundations"],
    order=1,
    body=BIG_O,
)
emit(
    "01-foundations",
    "02-amortized-analysis.mdx",
    title="Amortized Analysis",
    slug="amortized-analysis",
    summary="Aggregate, accounting, and potential methods, with doubling arrays, binary counters, and two-stack queues.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["big-o-and-complexity"],
    tags=["amortized", "complexity", "foundations"],
    order=2,
    body=AMORTIZED,
)
