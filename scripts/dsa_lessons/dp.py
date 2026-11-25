"""DP framework, classic families, and advanced state shapes."""

from emit import emit

FRAME = r'''
## Why this matters

Dynamic programming is what you do after you have written a correct recursion and noticed that it solves the same subproblem many times. The recursion is the specification. The table, or the memo, is the implementation that makes the specification fast enough. Climbing stairs, house robber, coin change, and edit distance are not four unrelated tricks. They are four states. Interviewers listen for the state in a sentence, the transition in a second sentence, and the complexity that follows from the size of the table. If you cannot say the state, you are guessing indices.

## Intuition

A city grid of tolls, where the toll to reach an intersection depends only on how you entered it and not on the whole history of the trip, can forget the history. The cheapest way to be at this intersection is the cheapest way to be at a legal previous intersection, plus the last step. That is optimal substructure: an optimal solution contains optimal solutions of subproblems. Overlapping subproblems means those smaller intersections are reused by many routes. If the routes never share intersections, you have divide and conquer, not dynamic programming. If the best route depends on the entire history, the state is too small and the answers will be wrong.

## Core concept in depth

Design the state first. A state is the smallest bundle of facts that lets you make the next decision. For climbing stairs, the fact is the stair index you are standing on. For house robber, it is the house index and whether you are still allowed to rob, which collapses to "the best profit from this house onward" because the adjacency rule is local. For a knapsack, it is the item index and the remaining capacity. If two histories leave you with the same bundle, they are the same state and you store one answer.

Write the transition as a recurrence. Climbing stairs: ways(n) = ways(n - 1) + ways(n - 2), with ways(0) = 1 and ways(1) = 1, or the equivalent base cases you choose and then test. House robber: rob(i) = max(value[i] + rob(i + 2), rob(i + 1)). Coin change: the minimum coins for amount a is one plus the minimum over coins c of the answer for a - c, when c is at most a. The recurrence is the algorithm. Everything else is an evaluation order.

Top-down evaluation is the recursive function plus a memo table keyed by the state. Check the memo before you recur. Store the answer before you return. This evaluates only the states you reach. It uses stack depth equal to the longest chain of dependencies. Bottom-up evaluation orders the states so that when you compute one, its dependencies are already stored. Climbing stairs fills an array from 2 to n. Knapsack fills items one by one and capacities from high to low if you are rolling the array. Bottom-up uses no recursion and makes the loops the proof of order. Prefer it when the dependency order is obvious and the stack might be deep. Prefer top-down when the state space is large but sparse, or when the recurrence is easier to trust than the loop bounds.

The time is the number of states times the work inside one transition. Climbing stairs is n states and O(1) work, so Theta(n). A 0/1 knapsack is n times capacity states and O(1) work per state, so Theta(n W). If the transition tries every coin, multiply by the number of coins. Space is the table, unless you notice that each layer reads only the previous layer or the previous two cells. Climbing stairs keeps two integers. House robber keeps two integers. A knapsack that processes items one at a time can keep one array of size W, iterating the capacity downward so a cell is not reused inside the same item. Iterating upward on that array turns 0/1 into unbounded, which is a real algorithm for the other problem and a bug for this one.

Base cases are part of the specification. ways(0) = 1 means there is one way to stand still. The minimum coins for amount 0 is 0. The minimum coins for an unreachable amount must be an infinity you recognize, not a 0 that looks like success. Off-by-one base cases are the bugs that survive a single example and fail the empty input.

Reconstruction, when the problem asks for the choices and not only the value, stores a predecessor or replays the recurrence from the stored answers. Do not store every full subset in the cell. Store the decision, and walk it at the end. That keeps the space equal to the number of states rather than the number of states times the solution size.

A problem is not dynamic programming just because it has a maximum in it. Greedy problems have a local choice you can prove without trying all of them. DP is what remains when several choices could be optimal and only the subproblem answers can tell them apart. If the constraints show n up to 10 to the 5th and your state is n squared, the state is too big. Look for a greedy, a heap, or a tighter state.

## Diagram and dry run

```mermaid
flowchart TD
    A[Name the state] --> B[Write the recurrence]
    B --> C[Write the base cases]
    C --> D{Sparse state space or deep chain?}
    D -->|Sparse| E[Top-down memo]
    D -->|Dense and ordered| F[Bottom-up loops]
    E --> G[Complexity is states times transition work]
    F --> G
```

Climbing stairs, n = 5. ways(0) = 1, ways(1) = 1.

| Stair | Recurrence | Value |
| --- | --- | --- |
| 2 | 1 + 1 | 2 |
| 3 | 2 + 1 | 3 |
| 4 | 3 + 2 | 5 |
| 5 | 5 + 3 | 8 |

House robber on values 2, 7, 9, 3, 1. Let best_skip be the best answer not using the current house's predecessor, and best_take the best that did. Walking left to right, the answer at each house is the max of skipping it (previous answer) and taking it (value plus the answer from two houses ago). The numbers are 2, then max(2, 7) = 7, then max(7, 9 + 2) = 11, then max(11, 3 + 7) = 11, then max(11, 1 + 11) = 12. The optimal robbery is 2, 9, 1 or 7 and 3 and... 7 + 3 + 1 = 11, and 2 + 9 + 1 = 12. The table found 12.

## Runnable Python

The memoized recursion and the rolling loop for climbing stairs are the same recurrence. House robber is the loop you should generalize. Both bottom-up versions are iterative. The memoized version is the recursive form.

```python
def climb_memo(n: int) -> int:
    memo = [-1] * (n + 1)

    def ways(k: int) -> int:
        if k <= 1:
            return 1
        if memo[k] == -1:
            memo[k] = ways(k - 1) + ways(k - 2)
        return memo[k]

    return ways(n)


def climb_loop(n: int) -> int:
    if n <= 1:
        return 1
    prev, cur = 1, 1
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur


def rob(nums: list[int]) -> int:
    prev, cur = 0, 0
    for value in nums:
        prev, cur = cur, max(cur, prev + value)
    return cur
```

`climb_loop(5)` is 8. `rob` on 2, 7, 9, 3, 1 is 12. The robber's `prev` is the best up to but not including the previous house, which is exactly "two houses ago" after the rotation in the assignment. Write the assignment as a tuple swap so you do not overwrite cur before prev reads it.

## Complexity and trade-offs

| Problem | States | Transition | Time | Space |
| --- | --- | --- | --- | --- |
| Climbing stairs, rolling | n | O(1) | Theta(n) | Theta(1) |
| Climbing stairs, naive recursion | n, recomputed | two calls | Theta(phi to the n) | Theta(n) stack |
| House robber | n | O(1) | Theta(n) | Theta(1) |
| 0/1 knapsack | n times W | O(1) | Theta(n W) | Theta(W) rolled |
| Coin change, amount A, c coins | A | O(c) | Theta(A c) | Theta(A) |

Top-down and bottom-up share the state complexity. They differ in constants, in stack risk, and in whether unused states are allocated. A hash map memo saves memory on sparse states and costs more per lookup than an array. Use an array when the state is a dense integer range.

## Tricks, tips, and patterns

Say the state out loud before you declare an array. If you cannot finish the sentence "the answer for this state is the min or max of ...", you do not have a recurrence. Match the loop direction to the dependency. Upward loops for prefixes. Downward loops for a rolling 0/1 knapsack. Initialize unreachable states to infinity for minima and to a neutral 0 or negative infinity for maxima, and do not let infinity plus a number overflow. Test n = 0, n = 1, and a case where the optimal choice skips a tempting early value.

## Common mistakes and edge cases

A memo that is checked after the recursive calls, which does nothing. An array of size n indexed at n. Base case ways(0) = 0, so every answer collapses. Using the rolling knapsack in the wrong direction and counting an item twice. Storing the full path in every cell. Calling a greedy coin choice "DP" when the coin system is not canonical. Forgetting that house robber on a circle is two linear problems, not one, because the first and last houses conflict. That variant is in the next lesson. Integer answers that exceed 32 bits in other languages. In Python they do not. Empty input returns the base case, usually 0.

## Interview notes

Use four sentences. State: "best from this index onward." Transition: "take it and skip the next, or skip it." Base: "past the end is 0." Complexity: "n states, constant work, linear time, constant space with two variables." Then code the loop. If you get stuck, write the naive recursion, point at a duplicated call on a small n, and add a memo. That path is slower to type and easier to justify. Dry-run the robber array above. It is the example where taking the first house wins, so a greedy "always take the larger neighbor" story fails.

## Practice problems

1. [Climbing Stairs](/practice/climbing-stairs) and [Fibonacci Number](/practice/fibonacci-number).
2. [House Robber](/practice/house-robber) and [House Robber II](/practice/house-robber-ii).
3. [Min Cost Climbing Stairs](/practice/min-cost-climbing-stairs).
4. [Coin Change](/practice/coin-change) — the minimum-coins recurrence.

## Summary and cheat sheet

- State, transition, base case, evaluation order. That is the whole method.
- Overlapping subproblems plus optimal substructure. No overlap means you should not memoize for speed.
- Time is states times transition work. Space is the table, or the layers you actually reread.
- Top-down is recursion plus memo. Bottom-up is loops in dependency order.
- Roll the array when a layer only needs the previous layer. Reverse the loop when a layer must not reuse a cell.
- Naive Fibonacci-style recursion is the specification, not the answer, when n is large.

## Further reading

- [Wikipedia — Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)
- [Wikipedia — Memoization](https://en.wikipedia.org/wiki/Memoization)
- [CP-Algorithms, introduction to DP](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)
'''

FAMILIES = r'''
## Why this matters

After the framework, the interviews repeat a handful of families. Knapsack and coins are decisions on a capacity. Longest common subsequence and edit distance are decisions on two strings. Longest increasing subsequence is a decision on a sequence, with a patient sorting trick that improves the bound. Grid paths are knapsacks on two indexes. Interval DP, including burst balloons, decides a last cut inside a span. If you can name the family, you can usually write the state. If you invent a new state for each title, you will run out of time.

## Intuition

A knapsack packs items into a weight budget, each item used once or many times. A string DP walks two cursors and pays for a match, a skip, or a substitution. A grid DP walks only right and down, so each cell has two predecessors. An interval DP says: I do not know the first cut, but I know the last action inside this span, and the two sides of that action are smaller intervals. The families are different shapes of the same sentence. The last decision reduces the state to something already solved.

## Core concept in depth

0/1 knapsack. Items have weight and value. State dp[i][w] is the best value using the first i items with capacity w. Transition: skip the item, or take it when the weight fits, adding its value to dp[i - 1][w - weight]. The rolled array iterates items forward and capacity backward. Unbounded knapsack, where each item may be used any number of times, iterates capacity forward so the same item can be picked again inside the layer. Coin change for the minimum number of coins is an unbounded knapsack on the amount, with value replaced by one coin of cost. Coin change II, the number of combinations, is the same loop with sums instead of minima, and the loop order decides whether you count combinations or permutations. Iterating coins outside and amount inside counts combinations. Iterating amount outside counts permutations, because order of coins becomes distinct. Read the problem. Combinations and permutations are different numbers.

Longest common subsequence. dp[i][j] is the LCS length of the first i characters of s and the first j of t. If the characters match, the answer is 1 plus dp[i - 1][j - 1]. Otherwise it is the max of dropping a character from either string. Time and space are Theta of the product of the lengths. A rolling row drops the space to Theta of the shorter length if you only need the length. Reconstruction walks from the end and emits a character when the match transition was used.

Edit distance allows insert, delete, and replace, each of cost 1. The match case costs 0 plus the diagonal. Insert and delete are the two neighbors. Replace is the diagonal plus 1. The base cases are the first row and column: turning a string into empty takes a deletion per character. This is the Levenshtein distance. The state is the same shape as LCS. Do not mix their transitions.

Longest increasing subsequence. The quadratic DP sets dp[i] to the longest increasing subsequence that ends at i, which is 1 plus the maximum dp[j] for j less than i and nums[j] less than nums[i]. The n log n method maintains the smallest possible tail of all increasing subsequences of each length. For each value, binary-search the leftmost tail that is at least the value and replace it, or append if the value extends every tail. The array length is the answer. The array is not the subsequence. Reconstruction needs extra parent pointers. Patience sorting is this algorithm. Use the quadratic DP when n is a few thousand. Use the tails when n is 10 to the 5th.

Grid paths. Unique paths on a grid moving only right and down: dp[r][c] = dp[r - 1][c] + dp[r][c - 1], with the first row and column equal to 1 if those cells are open. Obstacles zero a cell and block the sum. Minimum path sum replaces the sum with a min and adds the cell cost. The space rolls to one row. A grid that also allows up and left is not acyclic, and this DP is invalid. That problem is a graph search.

Interval DP. Burst balloons and matrix-chain multiplication share a span. Let dp[l][r] be the best score for bursting every balloon strictly between l and r, with l and r already the boundaries. The last balloon k you burst between them scores nums[l] times nums[k] times nums[r], plus the two subspans. Try every k. Fill by increasing span length so the subspans are ready. Time is Theta(n cubed). The same loop multiplies matrices: the last multiplication splits the chain. If you see "last cut of an interval" or "burst this one last," write this state. A recursion on the first burst is correct and much harder to memoize, because the neighbors change.

House robber II is a circle: run the linear robber on the range that excludes the first house, and on the range that excludes the last, and take the max. The empty and single-house cases are the overlap of those ranges. Do not double-count a one-house village.

## Diagram and dry run

```mermaid
flowchart TD
    A[Two string indexes i and j] --> B{Characters equal?}
    B -->|Yes| C[Diagonal plus one, for LCS]
    B -->|No| D[Max of the cell above and the cell to the left]
```

LCS of "ace" and "abcde". Rows are ace, columns are abcde. The match of a, then no match on b, match of c against c, match of e against e. The length is 3, and one subsequence is a, c, e.

Coin change. Coins 1 and 3, amount 4. Combinations, coins outer.

| Amount | After coin 1 | After coin 3 |
| --- | --- | --- |
| 0 | 1 way, take nothing | 1 |
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 1 | 2, namely 1+1+1 and 3 |
| 4 | 1 | 2, namely four 1s, and 3+1 |

If the loops were swapped you would also count 1+3 as different from 3+1. Minimum coins for 4 is 2, using 1 and 3, from the other recurrence.

## Runnable Python

Unbounded coin change for the minimum count, and the quadratic LIS. The coin function is iterative. LIS is iterative. A recursive memo of LIS is natural and risks a deep stack. The loops are the interview versions.

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1
    dp = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


def lis_length(nums: list[int]) -> int:
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
```

`coin_change` on coins 1, 3 and amount 4 returns 2. An amount that cannot be made, such as coins 2 and 4 with amount 3, returns -1 because the cell stays above the amount. `lis_length` on 10, 9, 2, 5, 3, 7, 101, 18 returns 4. The tails array is not the subsequence 2, 3, 7, 18. It is a sequence of best tails. Do not print it as the answer unless you stored parents.

## Complexity and trade-offs

| Family | Time | Space | Watch |
| --- | --- | --- | --- |
| 0/1 knapsack | Theta(n W) | Theta(W) | loop capacity downward |
| Unbounded coins, minimum | Theta(amount times coins) | Theta(amount) | infinity for impossible |
| Combinations of coins | same | same | coin loop outside |
| LCS or edit distance | Theta(n m) | Theta(min(n, m)) rolled | different transitions |
| LIS quadratic | Theta(n squared) | Theta(n) | easy to reconstruct |
| LIS tails | Theta(n log n) | Theta(n) | the array is not the subsequence |
| Interval DP | Theta(n cubed) | Theta(n squared) | fill by span length |

If W is 10 to the 9th, the knapsack table does not fit. Look for a meet-in-the-middle split, a greedy exchange, or a feasibility binary search. If both strings have length 10 to the 5th, the LCS table does not fit either. The interview constraints are part of the family choice.

## Tricks, tips, and patterns

Draw the LCS cell and its three neighbors before you fill anything. For knapsacks, write "0/1 means backward, unbounded means forward" on the paper. For LIS tails, the binary search is a lower bound. For interval DP, include the sentinel boundaries, the way burst balloons adds balloons of value 1 at both ends, so the formula has neighbors. For a circular house row, solve two linear ranges. For grid DP, set the obstacle cell to 0 before the neighbors add into it.

## Common mistakes and edge cases

Counting permutations when the problem asks for combinations. A coin of value 0, which loops forever if you are not careful. It should be excluded. Edit distance that charges 1 for a match. LIS that uses a non-strict comparison when the sequence must be strictly increasing. Interval DP that indexes the last burst outside the open interval and double-counts the boundary. House robber II that runs one linear pass and also allows both ends. Empty coins, amount 0, which is 0 coins. Empty string LCS, which is 0. A grid with an obstacle on the start cell, which has 0 paths.

## Interview notes

Name the family, then the state, then the loop direction. For coins, ask "combinations or permutations?" if the statement is ambiguous, and point at the loop order as your interpretation. For LIS, give the quadratic answer first if n is small, and mention n log n if n is large. For edit distance, write the three operations in the cell diagram. Dry-run a 3 by 5 LCS or a four-dollar coin change. Those fit on a corner of the board. Interval DP is the one to bring up only when the problem says last burst, last cut, or matrix chain. Do not force it onto a linear house robber.

## Practice problems

1. [Coin Change](/practice/coin-change) and [Coin Change II](/practice/coin-change-ii).
2. [Knapsack](/practice/knapsack) and [Partition Equal Subset Sum](/practice/partition-equal-subset-sum).
3. [Longest Common Subsequence](/practice/longest-common-subsequence) and [Edit Distance](/practice/edit-distance).
4. [Longest Increasing Subsequence](/practice/longest-increasing-subsequence).
5. [Unique Paths](/practice/unique-paths) and [Minimum Path Sum](/practice/minimum-path-sum).
6. [Burst Balloons](/practice/burst-balloons) and [Rod Cutting](/practice/rod-cutting).

## Summary and cheat sheet

- 0/1 knapsack loops capacity downward. Unbounded loops forward. Coin combinations keep the coin loop outside.
- LCS match is the diagonal plus one. Otherwise the max of dropping either side.
- Edit distance adds insert, delete, and replace to that picture, and a match is free.
- LIS is n squared with an end-at-i state, or n log n with binary search on tails.
- Grid DP needs an acyclic move set. Right and down is the usual one.
- Interval DP tries the last cut and fills short spans first. Time is n cubed.
- A circle is two linear subproblems when the first and last choices conflict.

## Further reading

- [Wikipedia — Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)
- [Wikipedia — Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence)
- [Wikipedia — Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
- [CP-Algorithms, longest increasing subsequence](https://cp-algorithms.com/sequences/longest_increasing_subsequence.html)
'''

ADV = r'''
## Why this matters

Some states are not a single index. A traveling salesman on 15 cities can afford a state that is a subset of visited cities plus the current city, because 2 to the 15 times 15 is half a million. A digit DP walks a number one digit at a time and remembers whether it is still tight against the upper bound. A tree DP roots the tree anywhere and combines children. A stock state machine remembers whether you hold a share and whether you are cooling down. These are the same framework with a richer key. Interviewers use them to see whether "DP" for you means one memorized table or a way to invent a state.

## Intuition

If the future depends on a set, put the set in the state, and hope the set is small enough to bitmask. If the future depends on a prefix of a number and on whether you have already chosen a smaller digit, put that boolean in the state. If the future depends on a subtree, compute the subtree first, which is postorder, and pass a summary to the parent. If the future depends on a mode, such as holding or not holding, the mode is one dimension of the state and the day is the other. You are not learning four algorithms. You are packing the memory of the process into the smallest key that still determines the optimum.

## Core concept in depth

Bitmask DP. Label the objects 0 through n - 1 with n at most about 20. A mask is an integer whose bits say which objects are in the subset. The traveling salesman state is (mask, j): the minimum cost of a path that has visited exactly the cities in the mask and ends at j. The transition comes from a previous city i that is also in the mask: dp[mask][j] is the min of dp[mask without j][i] plus the edge i to j. The start is dp[1 shifted left by the start city][start] = 0. The answer is the min over j of dp[full mask][j] plus the edge back, if the tour must return. Time is Theta(2 to the n times n squared) if every pair is tried, because each state looks at n previous cities. Space is Theta(2 to the n times n). For n = 20 that is about 20 million states, which is the edge of what a tight implementation can do and more than a casual Python loop should promise. For n = 15 it is comfortable. Subset sums of a small set can also be masks. When n is 40, masks do not fit, and meet-in-the-middle splits the set in half. That technique is in the advanced-techniques lesson.

Digit DP counts numbers up to R whose digits satisfy a property, such as "the digit sum is 10" or "no repeated digit." The state is the position in the decimal representation, the running property, and a tight flag. tight is true when every digit chosen so far matches the prefix of R, which means the next digit cannot exceed R's digit at this position. Once you place a smaller digit, tight becomes false and later digits may be anything from 0 to 9. A leading-zero flag is the other boolean people forget, because leading zeros should not count as digits in a "no repeat" constraint. The recurrence tries each legal next digit and calls the next position. Memoize on (position, property, tight, leading). The number of positions is the number of digits, about 18 for a 64-bit integer, so the table is small even when the property is a digit sum up to a few hundred. Count one side of a range by f(R) - f(L - 1), and define f(negative) as 0. This is the standard way to answer "how many integers in a range" without looping over the range.

Tree DP. Root the tree at any node if it is unrooted. A postorder computes a vector of answers for each subtree. House robber III is the example you already trust: each subtree returns two numbers, the best if this node is robbed and the best if it is not. If it is robbed, the children must not be robbed, so you add their "not robbed" answers. If it is not robbed, each child contributes the max of its two answers. The root returns the max of its two numbers. Time is linear. Any tree problem whose choice is local to a node and whose children are independent given that choice is this shape. Diameter was a tree DP that returned a height and updated a global best. You have been doing tree DP since the traversal lesson.

State-machine DP. A stock problem with cooldown has three modes: holding a share, not holding and free to buy, and cooling down after a sale. Each day, holding can stay holding or sell into cooldown. Free can stay free or buy into holding. Cooldown must become free. The transitions are a constant number, so one day is O(1) and n days are linear. You can roll the three variables. Best time to buy and sell with cooldown is exactly this machine. Unlimited transactions without cooldown are a simpler machine with two modes, and there is also a greedy reading: add every upward difference. The greedy is right for that special case and wrong as soon as a fee or a cooldown appears. When the constraints add a fee, subtract it on the sell transition. When they add a limit of k transactions, add k to the state, and the time becomes n times k.

Bitmask and digit and tree and machine states compose. A tree DP can return a bitmask summary when the subtree alphabet is tiny. A digit DP can track a small mask of used digits. Do not compose them until the separate versions are correct. Write one new bit of state, check the base case, then the transition.

## Diagram and dry run

```mermaid
flowchart LR
    A[Day d, free] -->|buy| B[Day d plus 1, holding]
    A -->|rest| A2[Day d plus 1, free]
    B -->|sell| C[Day d plus 1, cooldown]
    B -->|rest| B2[Day d plus 1, holding]
    C -->|must rest| A2
```

Prices 1, 2, 3, 0, 2, with a one-day cooldown after each sale. One optimal policy buys at 1, sells at 3, waits out the cooldown on the 0, and buys... the 0 is the cooldown day if you sold on the 3, so you cannot buy the 0. You can buy the 2, but selling it needs a later day you do not have. The profit of buy 1 and sell 3 is 2. Buying at 0 is impossible under that schedule and unnecessary: buy 1, sell 2, cooldown on 3, buy 0, sell 2. Profit is (2 - 1) + (2 - 0) = 3, and the cooldown day is the 3, which you correctly skipped. The state machine finds 3. A greedy "sell every rise" would try to sell 1 to 2 and 2 to 3 without a cooldown and would be illegal.

Traveling salesman on three cities in a triangle with costs 1, 1, and 3. Starting at 0, the mask that has visited everyone and ends at 1 or 2, plus the return edge, picks the tour that uses the two cheap edges and one expensive edge. The cost is 1 + 1 + 3 = 5, the only Hamiltonian tour up to direction. The DP still tries both directions. On three cities that is the whole table.

## Runnable Python

The stock cooldown machine uses three rolling variables. House robber III is the tree DP. Both are the forms to adapt. The salesman is a bottom-up mask loop for a complete graph given as a matrix. Keep n tiny in tests.

```python
def max_profit_cooldown(prices: list[int]) -> int:
    free = 0
    held = float("-inf")
    cool = 0
    for price in prices:
        free, held, cool = max(free, cool), max(held, free - price), held + price
    return max(free, cool)


class Node:
    def __init__(self, value: int, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def rob_tree(root: Node | None) -> int:
    def dfs(node: Node | None) -> tuple[int, int]:
        if node is None:
            return 0, 0
        left, right = dfs(node.left), dfs(node.right)
        robbed = node.value + left[1] + right[1]
        skipped = max(left) + max(right)
        return robbed, skipped

    return max(dfs(root))
```

The tuple assignment in `max_profit_cooldown` reads the old free, held, and cool on the right-hand side, so the transitions do not see the new values too early. `held` starts at negative infinity because holding nothing and pretending you hold a share would allow a fake sale. After prices 1, 2, 3, 0, 2 the function returns 3. `rob_tree` on a single node returns the node value. On a null root it returns 0.

## Complexity and trade-offs

| Kind | State size | Time | When it fits |
| --- | --- | --- | --- |
| Bitmask TSP | 2 to the n times n | times another n | n up to about 15 in Python, 20 in a tight language |
| Digit DP | digits times property times 2 | times 10 | ranges up to 10 to the 18 |
| Tree DP | n nodes times a small vector | Theta(n) times combine cost | any tree you can traverse |
| Stock machine | n times modes times k | Theta(n k) | k small, or roll the day |
| Plain index DP | n or n squared | the family bound | the previous lesson |

A bitmask on n = 40 is impossible. Say so and switch to meet-in-the-middle or an approximation. A digit DP that loops over the numeric range instead of the digits has abandoned the point. A tree DP that also passes the entire path as a state becomes exponential. Pass a summary.

## Tricks, tips, and patterns

Enumerate submasks, when you need them, by `sub = mask; while sub: ...; sub = (sub - 1) & mask`. That walks submasks in time proportional to the number of submasks, not to 2 to the n per mask, across all masks the total is 3 to the n. You need this for some subset DP, not for the basic salesman. For digit DP, write the tight transition on paper for the number 20, so you see the digit 2 freeze the first position. For stocks, draw the modes and the legal edges before the variables. For trees, return a tuple, not a single number, when the parent needs to know how the subtree optimum was achieved.

## Common mistakes and edge cases

Updating a bitmask state from a mask that has not been computed, because the loop over masks was not increasing. The salesman must iterate masks in increasing order of popcount, or simply in integer order, which already respects "submask before mask" if you only look at masks with the bit removed and that mask is numerically smaller. It is, because clearing a bit decreases the integer. Rely on that. Digit DP off-by-one on the last position, counting the number itself twice or not at all. Forgetting leading zeros. Stock transitions that buy and sell on the same day when the statement forbids it. Cooldown machines that allow a buy on the cooldown day. Tree DP that robs a node and also adds the robbed child value. Negative infinity that leaks into a max with a real profit and wins because you compared wrong. In Python, `max(0, float("-inf"))` is 0, which is what you want for "do nothing." An empty price list returns 0.

## Interview notes

When the constraint on n is 15 or 20 and the problem says visit every city or assign every mask, say bitmask. When the problem says numbers from L to R with a digit property, say digit DP and name the tight flag. When the input is a tree and the choice is rob or not, return two numbers per subtree. When the problem is stocks with a cooldown or a fee, draw three modes. Give the state size as a product you computed from the constraints, so the interviewer sees that the table fits. Do not say "DP" without the key.

## Practice problems

1. [House Robber III](/practice/house-robber-iii) — the tree pair.
2. [Best Time to Buy and Sell Stock with Cooldown](/practice/best-time-to-buy-and-sell-stock-with-cooldown).
3. [Best Time to Buy and Sell Stock II](/practice/best-time-to-buy-and-sell-stock-ii) — the two-mode machine, also solvable by summing rises.
4. [Target Sum](/practice/target-sum) — a knapsack in disguise, or a small mask when the array is tiny.
5. [Partition Equal Subset Sum](/practice/partition-equal-subset-sum).

## Summary and cheat sheet

- Put into the state exactly the memory the future needs.
- Bitmasks fit when n is about 20 or less. TSP is (mask, last city).
- Digit DP walks digits, with a tight flag and usually a leading-zero flag. Answer range queries by subtraction.
- Tree DP is a postorder summary. House robber III returns robbed and skipped.
- Stock problems are small state machines. Cooldown adds a mode. A fee is a cost on the sell edge.
- Time is still states times transition work. If that product does not fit, the state is wrong or the problem is not this DP.

## Further reading

- [Wikipedia — Travelling salesman problem, the Held-Karp section](https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm)
- [Wikipedia — Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)
- [CP-Algorithms, digit DP](https://cp-algorithms.com/dynamic_programming/digit-dp.html)
'''

emit(
    "11-dp",
    "01-dp-framework.mdx",
    title="The Dynamic Programming Framework",
    slug="dp-framework",
    summary="State, transition, base case, and the choice between a memo and a bottom-up loop.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["mst-dsu-and-bridges"],
    tags=["dynamic-programming", "memoization"],
    order=1,
    body=FRAME,
)
emit(
    "11-dp",
    "02-classic-dp-families.mdx",
    title="Classic DP Families",
    slug="classic-dp-families",
    summary="Knapsacks and coins, LCS and edit distance, LIS, grids, and interval DP.",
    duration=45,
    difficulty="intermediate",
    prerequisites=["dp-framework"],
    tags=["dynamic-programming", "knapsack", "lcs"],
    order=2,
    body=FAMILIES,
)
emit(
    "11-dp",
    "03-advanced-dp.mdx",
    title="Bitmask, Digit, Tree, and State-Machine DP",
    slug="advanced-dp",
    summary="Subset masks, tight digit walks, subtree summaries, and stock modes.",
    duration=40,
    difficulty="advanced",
    prerequisites=["classic-dp-families"],
    tags=["bitmask", "digit-dp", "tree-dp"],
    order=3,
    body=ADV,
)
