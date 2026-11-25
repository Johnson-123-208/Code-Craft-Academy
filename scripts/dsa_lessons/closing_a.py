"""Greedy, bits, and number theory."""

from emit import emit

GREEDY = r'''
## Why this matters

A greedy algorithm locks in a choice and never reconsiders it. When the choice is safe, the algorithm is short and fast. When it is not, the algorithm is a confident wrong answer. The skill is the proof, not the loop. Interval scheduling, jump game, gas stations, and Huffman coding are safe. Coin systems that are not canonical are not. Interviewers ask "why is this safe?" because they have seen the coin bug. You should answer with an exchange argument or a stay-ahead argument, in words, before you code.

## Intuition

An exchange argument says: take any optimal solution that disagrees with your first choice. Swap your choice in and something else out, and show the result is still optimal. Then there exists an optimal solution that agrees with you, and you repeat. A stay-ahead argument says: after each step, your partial solution is at least as good as any other partial solution, under a measure you name. If you cannot finish either argument, try dynamic programming or admit the choice is a heuristic.

## Core concept in depth

Activity selection, also the non-overlapping interval problem, sorts by finishing time and keeps an activity when it starts after the last kept finish. The exchange argument: among the activities that fit in the remaining suffix, the one that finishes first leaves the largest possible suffix. Any optimal solution that picked something else can swap in the early finisher without losing feasibility or count. Sorting by start time does not have this argument. A counterexample is a long activity that starts first and blocks three short ones.

Jump game asks whether you can reach the last index, where nums[i] is the farthest jump from i. Walk left to right and track the furthest index you can reach. If your scan index ever passes that furthest index, you are stuck. If the furthest index reaches the end, you can. This is greedy because extending the frontier never requires revisiting an earlier jump: any path that reached a later index already implies the frontier is at least that far. Jump game II asks for the minimum number of jumps. The same frontier, counted in layers like a BFS on the implicit jump graph, is linear. A DP of "minimum jumps to i" is correct and quadratic. The layer scan is the one that fits large n.

Gas station gives gas[i] and cost[i] for a circular route. The total gas must be at least the total cost, or the trip is impossible. If it is possible, the start is the index just after the lowest prefix of gas minus cost, equivalently the station after the longest stretch where the running tank would have gone negative. One pass computes the total and the candidate start: whenever the tank goes negative, the next station becomes the new candidate and the tank resets. The proof: if a start fails at some station, every station in between fails too, because they began with no more fuel than the failed start had when it passed them. So you never need to retry the skipped region.

Huffman coding builds an optimal prefix code by repeatedly merging the two lightest nodes. A prefix code means no codeword is a prefix of another, so the encoded bitstream is unambiguous. The exchange argument is that the two least frequent symbols can sit as siblings at the deepest level. A heap implements the merges in n log n. Interviewers may only want the argument and the tree shape, not a full bit-encoder.

When greedy fails. The coin system 1, 3, 4 and the amount 6: greedy takes 4 and then two 1s, three coins, while two 3s use two coins. Canonical coin systems, including standard US denominations, happen to make the greedy choice optimal. A general coin system needs the unbounded knapsack DP. If you cannot prove the exchange, do not ship the greedy code as a correct algorithm. You may still use it as a heuristic and say so.

Other safe patterns you have already met. Dijkstra is greedy on non-negative weights, with the settlement proof instead of a scheduling proof. Kruskal and Prim are greedy on cuts. A stack that removes a larger digit when a smaller digit follows, in remove-k-digits, is greedy with an exchange argument about the leftmost place where the number can be smaller. Task scheduler with cooldown has a formula based on the most frequent task, and a heap simulation. The formula is greedy: you must separate the most frequent tasks by the cooldown, and the idle slots are filled by other tasks or left empty.

Matroids are the textbook setting where greedy is optimal for a weight function. You do not need the axioms in a coding interview. You need one exchange argument per problem. If the interviewer says "prove it," give the swap. If you cannot, switch families.

## Diagram and dry run

```mermaid
flowchart TD
    A[Sort or scan in the greedy order] --> B[Take the local choice]
    B --> C{Can you swap it into any optimal solution?}
    C -->|Yes| D[Lock it in and reduce the problem]
    C -->|No| E[This is not a correct greedy algorithm]
    D --> F[Repeat until the instance is empty]
```

Activities as half-open intervals of finish-then-start. Activities (1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9). Sorted by finish: (1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9).

| Considered | Last finish | Decision |
| --- | --- | --- |
| 1 to 4 | none | keep. Finish becomes 4 |
| 3 to 5 | 4 | starts before 4, skip |
| 0 to 6 | 4 | skip |
| 5 to 7 | 4 | keep. Finish becomes 7 |
| 8 to 9 | 7 | keep |
| 5 to 9 | 9 | skip |

Three activities. The long one from 0 to 6 was the trap for a start-time sort.

Gas 1, 2, 3, 4, 5 and cost 3, 4, 5, 1, 2. Differences -2, -2, -2, 3, 3. The tank goes negative through the first three stations. The candidate becomes index 3. The total of differences is 0, so a trip exists, and index 3 works: the surplus at the end of the array covers the deficit at the beginning.

## Runnable Python

Jump reachability and the gas-station start are both one pass. The recursive formulation of jump, "try every jump," is the exponential specification. It is included only as the thing the greedy replaces. Do not ship it for large n.

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, jump in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + jump)
    return True


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = 0
    start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        total += g - c
        tank += g - c
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1
```

`can_jump` on 2, 3, 1, 1, 4 returns true. On 3, 2, 1, 0, 4 it returns false because index 3 is a zero and the reach dies there before the last index. `can_complete_circuit` on the gas example returns 3. If every difference is negative in total, it returns -1 even if a local tank looked fine.

## Complexity and trade-offs

| Problem | Greedy | If you refuse to prove it |
| --- | --- | --- |
| Activity selection | Theta(n log n) sort, then linear | interval DP is slower |
| Jump I and II | Theta(n) | quadratic DP |
| Gas station | Theta(n) | try every start, quadratic |
| Huffman | Theta(n log n) | exponential code search |
| General coins | not greedy | unbounded knapsack |
| Non-negative shortest paths | Dijkstra | Bellman-Ford still correct, slower |

Greedy is not a complexity class. It is a proof style. A linear greedy and a linear DP can solve different problems. Compare proofs, not slogans.

## Tricks, tips, and patterns

Sort by the endpoint the exchange argument names. Finish time for scheduling. End coordinate for bursting balloons. Leftmost digit for the smallest number after deletions. Track a frontier for jumps. Track a tank and a candidate start for gas. If the total resource is insufficient, fail before you trust the candidate. When a counterexample exists, switch to DP and keep the greedy as a comment about what does not work.

## Common mistakes and edge cases

Sorting activities by start. Jump game that returns true because the first jump is large, without scanning the hole in the middle. Gas station that returns 0 whenever the total is enough, even if station 0 cannot complete. An off-by-one that starts at `start` equal to n, which is index 0 on a circle only if you modulo. If the total is enough, the algorithm's start is at most n - 1, because the last reset still leaves a non-negative suffix and the total covers the prefix. Huffman that merges the two heaviest symbols. Greedy coins on a non-canonical system. A single activity. An empty schedule. A jump array of one element, which is already at the end, reach 0, and the loop index 0 is not past reach.

## Interview notes

State the choice and the exchange in two sentences, then code. If the interviewer asks "are you sure?", walk the swap on their example rather than repeating "it's greedy." For jumps, say "the furthest reach is a BFS layer boundary." For gas, say "a failed start condemns every index it passed." Mention the coin counterexample if they ask whether greedy always works. It does not.

## Practice problems

1. [Jump Game](/practice/jump-game) and [Jump Game II](/practice/jump-game-ii).
2. [Gas Station](/practice/gas-station).
3. [Non-overlapping Intervals](/practice/non-overlapping-intervals) and [Minimum Number of Arrows](/practice/minimum-number-of-arrows-to-burst-balloons).
4. [Partition Labels](/practice/partition-labels).
5. [Task Scheduler](/practice/task-scheduler).

## Summary and cheat sheet

- Greedy locks a choice. Prove it with an exchange or a stay-ahead argument.
- Schedule by earliest finish. Jumps track the furthest reach. Gas tracks the tank and resets the start after a deficit.
- A sufficient total plus the reset start solves the circular gas station in one pass.
- Huffman merges the two lightest nodes.
- Non-canonical coins break greedy. Use DP.
- Dijkstra, Kruskal, and Prim are greedy algorithms whose proofs you already have.

## Further reading

- [Wikipedia — Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm)
- [Wikipedia — Activity selection problem](https://en.wikipedia.org/wiki/Activity_selection_problem)
- [Wikipedia — Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)
'''

BITS = r'''
## Why this matters

Bit tricks show up as their own problems and as the inner loop of masks, hashes, and Fenwick indexes. You are expected to set, clear, toggle, and test a bit without a sermon, to use XOR as a toggle that cancels pairs, and to know why `n & (n - 1)` drops the lowest set bit. Single number, missing number, power of two, and the count of set bits are the drills. The advanced DP lesson uses the same masks as state. This lesson is the arithmetic.

## Intuition

A non-negative integer is a row of switches. AND keeps a switch on only if both inputs have it on. OR turns a switch on if either input has it on. XOR turns it on if the inputs disagree. Shifting left is multiplying by a power of two. Shifting right is dividing by a power of two, toward zero or with sign extension depending on the operator and the language. A mask is an integer you build so that AND isolates the switches you care about. XOR of a value with itself is zero, and XOR of a value with zero is the value. Those two identities are why pairs disappear.

## Core concept in depth

Number the bits from the right, starting at 0. Bit k has weight 2 to the k. The mask with only that bit set is `1 << k`. Test with `n & (1 << k)`. Set with `n | (1 << k)`. Clear with `n & ~(1 << k)`. Toggle with `n ^ (1 << k)`. In Python, integers are unbounded and `~n` is the bitwise complement in an infinite two's-complement sense, equal to `-n - 1`. Clearing a bit with `~` still works. Printing `~n` surprises people who expected a 32-bit pattern. If the problem wants a 32-bit answer, mask with `0xFFFFFFFF` at the end.

XOR properties you will use. XOR is associative and commutative. `a ^ a` is 0. `a ^ 0` is a. Therefore the XOR of an array in which every value appears twice except one is the single value. The pairs cancel. If every value appears three times except one, XOR is not enough, because three copies do not cancel in a two-state toggle. Count each bit modulo 3, or use the two-variable state machine from the single-number-II problem: ones and twos track the count of each bit modulo 3. Sum of two integers without `+` is XOR for the sum bits and a left-shifted AND for the carry, repeated until the carry is 0. That is the adder.

`n & (n - 1)` clears the lowest set bit. Loop until n is 0 and count the iterations to get the popcount. That is Brian Kernighan's trick, and it runs in time proportional to the number of set bits, not to the word width. A power of two has exactly one set bit, so `n > 0 and n & (n - 1) == 0`. Zero is not a power of two. `n & -n` isolates the lowest set bit. Fenwick trees use that. Python's negative numbers are two's complement in the bitwise operators, so `n & -n` works for positive n. Do not call it on zero.

Missing number, given 0 through n with one missing, is the XOR of all indices and all values, or the formula `n(n+1)/2` minus the sum. XOR avoids overflow in languages with fixed-width integers. The formula is clearer. Both are linear. Reverse bits of a 32-bit word swaps bit k with bit 31 - k. Do it with a loop, or with the well-known parallel swap of bit fields. A loop is the right interview code. Bitwise AND of numbers in a range has a closed form: the AND of a range is the common binary prefix of the endpoints. Shift both numbers right until they are equal, counting the shifts, then shift the common value back. The differing suffix becomes zeros.

Shifts. `n << k` multiplies by 2 to the k. `n >> k` in Python is a floor division by 2 to the k for positive n, and it sign-extends for negative n because there is no unsigned type. A logical right shift of a 32-bit pattern is `(n & 0xFFFFFFFF) >> k`. Know which one the problem wants.

Masks as sets. The empty set is 0. Add element i with OR. Remove it with AND of the complement of the bit. Membership is AND. Iterate the set bits by repeatedly isolating the lowest bit and clearing it. Submasks of a mask iterate by `sub = (sub - 1) & mask`. That loop is the bridge to bitmask DP. You do not need it for the single-number problems.

## Diagram and dry run

```mermaid
flowchart LR
    A[Value n] --> B[AND with a one-bit mask to test]
    A --> C[OR the mask to set]
    A --> D[AND the complement to clear]
    A --> E[XOR the mask to toggle]
    F[n AND n minus 1] --> G[Lowest set bit falls off]
```

Array 4, 1, 2, 1, 2. XOR running total:

| Value | Running XOR |
| --- | --- |
| 4 | 4 |
| 1 | 5, which is 4 xor 1 |
| 2 | 7 |
| 1 | 6, the second 1 cancels |
| 2 | 4, the second 2 cancels |

The survivor is 4.

Number 12 is 1100 in binary. 12 AND 11 is 1100 AND 1011, which is 1000, clearing the lowest set bit. One more step yields 0. Two set bits. 8 AND 7 is 0, and 8 is positive, so 8 is a power of two. 6 AND 5 is 4, not 0, so 6 is not.

## Runnable Python

The pair-cancel XOR, the popcount loop, and the carry adder. All three are iterative. The recursive popcount is the same idea with a call per set bit, included so the recurrence `pop(n) = 1 + pop(n & (n - 1))` is visible. Prefer the loop.

```python
def single_number(nums: list[int]) -> int:
    acc = 0
    for value in nums:
        acc ^= value
    return acc


def popcount(n: int) -> int:
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def popcount_rec(n: int) -> int:
    if n == 0:
        return 0
    return 1 + popcount_rec(n & (n - 1))


def add_without_plus(a: int, b: int) -> int:
    while b:
        a, b = a ^ b, (a & b) << 1
    return a
```

`single_number` on 4, 1, 2, 1, 2 returns 4. `popcount(12)` is 2. `add_without_plus(5, 7)` is 12. The adder as written is for non-negative integers. A fixed-width signed adder masks every step and interprets the sign bit at the end. Say that if the interviewer asks about negatives.

## Complexity and trade-offs

| Operation | Time | Notes |
| --- | --- | --- |
| Test, set, clear, toggle one bit | Theta(1) | a shift and a boolean op |
| XOR of an array | Theta(n) | constant space |
| Popcount by Kernighan | Theta(number of set bits) | better than 32 when the word is sparse |
| Popcount by scanning the width | Theta(word size) | simpler, fine for 32 or 64 |
| Range AND by common prefix | Theta(word size) | shifts until the endpoints match |
| Bitmask DP transition | depends on the mask | the arithmetic is still constant per edge |

A hash set also finds the single number and uses linear memory. XOR uses constant memory and needs the pair promise. If the promise is false, XOR returns some mixture and you will not notice. State the promise.

## Tricks, tips, and patterns

Write the four operations once on the whiteboard at the start of a bit round. Remember `n & (n - 1)` and `n & -n`. XOR cancels pairs. Modulo-3 counts need bits or the ones/twos machine, not a single XOR. Mask to 32 bits when the problem says 32-bit and you are in Python. For subsets, integer order enumerates masks, and clearing a bit yields a smaller integer, which is why a DP loop from 0 to `1 << n` sees submasks first if the transition clears bits.

## Common mistakes and edge cases

Using `~` and expecting a positive 32-bit mask. Treating 0 as a power of two. Sign issues in `>>` on negative numbers. XOR for triples. Off-by-one in the shift amount, so you set bit k + 1. A missing number problem whose array contains 0, which is a legal value and must not be used as an "empty" sentinel in the same way as a null. Overflow of `1 << 31` in 32-bit signed languages. In Python `1 << k` is fine for large k and then becomes a slow bigint. The adder that does not terminate if you mask incorrectly and the carry walks off into an infinite Python integer... with non-negative inputs and no mask, the carry walks left and ends. Do not OR the carry back into a confused sign bit.

## Interview notes

Start from the identity you need, not from a list of operators. "Pairs cancel under XOR, so one pass is the answer." "A power of two has one bit, so AND with n - 1 is zero." Dry-run 12 and 11, or the array 4, 1, 2, 1, 2. Mention Kernighan if they ask for popcount. Mention the 32-bit mask if the language is Python and the output is a bit pattern. Connect masks to the DP lesson only if the problem is a subset state. Otherwise solve the bit problem and stop.

## Practice problems

1. [Single Number](/practice/single-number) and [Single Number II](/practice/single-number-ii).
2. [Missing Number](/practice/missing-number) and [Number of 1 Bits](/practice/number-of-1-bits).
3. [Power of Two](/practice/power-of-two) and [Counting Bits](/practice/counting-bits).
4. [Sum of Two Integers](/practice/sum-of-two-integers) and [Reverse Bits](/practice/reverse-bits).
5. [Bitwise AND of Numbers Range](/practice/bitwise-and-of-numbers-range).

## Summary and cheat sheet

- Test, set, clear, toggle: AND, OR, AND-complement, XOR, each with `1 << k`.
- `a ^ a` is 0 and `a ^ 0` is a. Pairs cancel. Triples do not.
- `n & (n - 1)` clears the lowest set bit. `n & -n` isolates it.
- A positive n is a power of two when `n & (n - 1)` is 0.
- Addition is XOR plus a shifted AND carry, repeated.
- In Python, mask to 32 bits when the problem's universe is 32 bits.
- Range AND is the common prefix of the two endpoints.

## Further reading

- [Wikipedia — Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation)
- [Wikipedia — Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)
- [Python bitwise operators](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations)
'''

MATH = r'''
## Why this matters

A slice of interview problems is number theory in work clothes: gcd, primes, modular exponentiation, trailing zeros of a factorial, and combinatorics under a modulus. The algorithms are old and short. The bugs are overflow, the wrong modulus identity, and sieves that start marking at the wrong multiple. You should be able to write Euclid's algorithm both ways, the Sieve of Eratosthenes, and fast exponentiation, and you should know why `n!` has as many trailing zeros as the number of times 5 divides it.

## Intuition

The greatest common divisor of a and b also divides any integer combination of them, in particular a - b and, more usefully, a mod b. That is Euclid: gcd(a, b) = gcd(b, a mod b), and gcd(a, 0) = a. The primes up to n are what remain after you cross out multiples. Fast exponentiation squares the base and halves the exponent, so a power that looks linear in the exponent becomes logarithmic. Trailing zeros are factors of 10, and 10 is 2 times 5, and there are always extra 2s, so you count 5s.

## Core concept in depth

Euclid's algorithm. Assume a and b are non-negative and a is at least b. If b is 0, return a. Otherwise return gcd(b, a mod b). The recursive form is the proof. The iterative form replaces the pair until b is 0. The number of steps is logarithmic in the larger input. Worst cases track the Fibonacci numbers, which is why the bound is tight up to a constant and still logarithmic. The least common multiple is a times b divided by the gcd, computed as `a // gcd * b` so you divide before you multiply and reduce overflow in fixed-width languages. In Python the order is about clarity. GCD of more than two numbers folds the two-argument function. Extended Euclid also returns integers x and y with a x + b y = gcd. You need it for modular inverses when the modulus is not prime. For a prime modulus, Fermat's little theorem gives the inverse of a as a to the power p - 2 modulo p, via fast exponentiation.

The Sieve of Eratosthenes. A boolean array from 0 to n, initially "maybe prime," with 0 and 1 set to not prime. For each i from 2 up to sqrt(n), if i is still prime, mark multiples from i times i up to n, stepping by i. Multiples below i times i were marked by smaller primes. Time is O(n log log n). Space is O(n). The smallest prime factor sieve is the upgrade that also factorizes every number up to n in similar time: when you mark a multiple, store i as its smallest prime factor if it does not have one. Trial division of a single number up to sqrt(n) is enough when you have one query and n is large. A sieve is the right tool when you have many queries or you need all primes up to n.

Modular arithmetic. (a + b) mod m is (a mod m + b mod m) mod m. Same for subtraction, adding m if the difference goes negative. Multiplication is (a mod m) times (b mod m) mod m. Division is multiplication by the modular inverse, and the inverse exists only when gcd(a, m) is 1. Fast exponentiation computes a to the n modulo m by scanning the bits of n. If the bit is set, multiply the result by the current base. Square the base every step. Both operations are modulo m. The time is Theta(log n) multiplications. Python's built-in `pow(base, exp, mod)` does this and is the thing you should call unless the question is the algorithm. Recursive fast pow squares `pow(n // 2)` and multiplies an extra base when n is odd. Iterative and recursive forms match. A negative exponent is an inverse, not this function, unless you define it.

Combinations. n choose k equals n choose n - k, and it satisfies Pascal's identity: C(n, k) = C(n - 1, k) + C(n - 1, k - 1). A DP table of those values is Theta(n k) and fine for n up to a few thousand. The multiplicative formula computes the product of k terms, dividing as you go so the intermediate stays integral: multiply by (n - i) and divide by (i + 1) for i from 0 to k - 1. Under a prime modulus, replace the division by multiplication with the modular inverse. Under a non-prime modulus, inverses may not exist and you should keep the Pascal DP modulo m, which only uses addition.

Trailing zeros of n! . Each factor of 10 is a 2 and a 5. The number of 5s in n! is floor(n/5) + floor(n/25) + floor(n/125) + ... until the power exceeds n. The number of 2s is larger, so the zeros equal the number of 5s. Extra factors of 10 from other sources do not appear. This is not "divide n by 10." 25! has six trailing zeros, not two, because 25 and 20 and 15 and 10 and 5 contribute, and 25 contributes two.

Primality of a single large integer, beyond trial division, uses Miller-Rabin, a randomized test. For interview sizes, trial division up to sqrt(n) is the expected answer. Mention Miller-Rabin only as the production test. Do not invent a deterministic polynomial you cannot prove.

## Diagram and dry run

```mermaid
flowchart TD
    A[gcd of a and b] --> B{b is 0?}
    B -->|Yes| C[Return a]
    B -->|No| D[Replace the pair by b and a mod b]
    D --> A
```

gcd(48, 18). 48 mod 18 is 12. gcd(18, 12). 18 mod 12 is 6. gcd(12, 6). 12 mod 6 is 0. gcd(6, 0) is 6. Three remainders. lcm(48, 18) is 48 / 6 * 18 = 144.

Sieve up to 20. After crossing multiples of 2, 3, and then stopping because the next i exceeds sqrt(20), the primes are 2, 3, 5, 7, 11, 13, 17, 19. 1 is not in the list. 9 was crossed by 3. 4, 6, 8, 10 were crossed by 2.

Trailing zeros of 25!. Powers of 5: floor(25/5) = 5, floor(25/25) = 1, total 6.

Fast pow of 2 to the 10, modulo 1000. Exponent 10 is 1010 in binary. Square 2 five times would be the wrong count. The iterative algorithm starts result 1, base 2. Bit 1 of 10 is set? 10 is even, square base to 4, exponent 5. Odd, result 4, base 16, exponent 2. Even, base 256, exponent 1. Odd, result 4 * 256 = 1024, then modulo 1000 is 24. And 2 to the 10 is 1024. Correct.

## Runnable Python

Iterative Euclid, the sieve, and iterative modular exponentiation. The recursive Euclid is three lines and is the form to recite. Call the iterative one when you want constant stack, which matters only for a pathological but still logarithmic depth you will not hit.

```python
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def gcd_rec(a: int, b: int) -> int:
    if b == 0:
        return abs(a)
    return gcd_rec(b, a % b)


def sieve(n: int) -> list[int]:
    prime = [True] * (n + 1)
    if n >= 0:
        prime[0] = False
    if n >= 1:
        prime[1] = False
    p = 2
    while p * p <= n:
        if prime[p]:
            for multiple in range(p * p, n + 1, p):
                prime[multiple] = False
        p += 1
    return [i for i in range(n + 1) if prime[i]]


def mod_pow(base: int, exp: int, mod: int) -> int:
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result
```

`gcd(48, 18)` is 6. `sieve(20)` returns the eight primes listed above. `mod_pow(2, 10, 1000)` is 24. `pow(2, 10, 1000)` in the standard library agrees. Use the library in application code. Use the loop when the interview asks how exponentiation is logarithmic.

## Complexity and trade-offs

| Algorithm | Time | Space |
| --- | --- | --- |
| Euclid | Theta(log min(a, b)) steps | Theta(1) iterative |
| Sieve up to n | Theta(n log log n) | Theta(n) |
| Trial division of one n | Theta(sqrt(n)) | Theta(1) |
| Fast pow | Theta(log exponent) multiplications | Theta(1) iterative |
| Pascal triangle modulo m | Theta(n k) | Theta(k) rolled |
| Trailing zeros | Theta(log n) divisions by 5 | Theta(1) |

A prime sieve of 10 to the 8th fits in a boolean array if you pack bits, and it does not fit as a Python list of a hundred million integers without thought. For one primality test of a 12-digit number, trial division up to the square root is a million operations and is fine. For all primes up to a million, sieve.

## Tricks, tips, and patterns

Divide before multiplying when computing lcm in a fixed-width language. Count fives for trailing zeros, and include 25, 125, and so on. Start sieve marking at i times i. Skip even numbers after 2 if you want a smaller sieve. Fast pow reduces the base modulo m at the start. Combinations under a prime modulus use inverses. Range counts use f(R) - f(L - 1) once f is a prefix count. GCD of negatives: take absolute values, because divisors do not care about sign. Define gcd(0, 0) only if you must. Mathematically it is often left undefined or 0 by the same loop. Say what you return.

## Common mistakes and edge cases

Marking sieve multiples from 2i instead of i squared, which is correct and slower, not a bug. Marking 1 as prime. Forgetting that 2 is prime. Integer division of lcm that overflows before the gcd division. Modular multiplication that overflows before the modulus in other languages. Python will not overflow, and then a slow bigint can hide inside a "logarithmic" pow if you forget the modulus. Trailing zeros that stop after one division by 5. n choose k with k greater than n, which is 0. k = 0, which is 1. A negative exponent in mod_pow, which the loop does not handle. Primality of 1.

## Interview notes

Write Euclid, say the remainder shrinks, and give the Fibonacci worst-case remark if you remember it. For primes, choose sieve or trial division based on how many queries and how large n is. For powers, write the bit loop and mention `pow(base, exp, mod)`. For trailing zeros, say "count fives, there are extra twos" and write the loop. Dry-run gcd(48, 18) or the zeros of 25!. Those two are small enough to finish.

## Practice problems

1. [Count Primes](/practice/count-primes) — the sieve, returning a count.
2. [Pow(x, n)](/practice/powx-n) — fast exponentiation. Mind a negative n, which becomes a reciprocal. The integer version in the bank uses a non-negative exponent.
3. [Factorial Trailing Zeroes](/practice/factorial-trailing-zeroes).
4. [Excel Sheet Column Number](/practice/excel-sheet-column-number) — base 26, a cousin of the digit loops above.

## Summary and cheat sheet

- gcd(a, b) = gcd(b, a mod b). lcm is the product divided by the gcd.
- Sieve: cross out multiples from i squared. Time n log log n. 0 and 1 are not prime.
- Fast pow squares the base and halves the exponent. Include the modulus at every multiply.
- Inverses modulo a prime are pow(a, p - 2, p).
- n choose k multiplies k terms and divides as it goes, or uses Pascal's identity.
- Trailing zeros of n! equal the number of fives in the factorization, counting higher powers.
- Trial-divide one number. Sieve a range.

## Further reading

- [Wikipedia — Euclidean algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm)
- [Wikipedia — Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
- [Wikipedia — Modular exponentiation](https://en.wikipedia.org/wiki/Modular_exponentiation)
- [CP-Algorithms, binary exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
'''

emit(
    "12-greedy",
    "01-greedy-algorithms.mdx",
    title="Greedy Algorithms and Exchange Arguments",
    slug="greedy-algorithms",
    summary="When a locked-in choice is safe: scheduling, jumps, gas stations, and the coin counterexample.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["advanced-dp"],
    tags=["greedy"],
    order=1,
    body=GREEDY,
)
emit(
    "13-bit-manipulation",
    "01-bit-manipulation.mdx",
    title="Bit Manipulation",
    slug="bit-manipulation",
    summary="Masks, XOR cancellation, the lowest set bit, and the arithmetic behind bitmask DP.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["greedy-algorithms"],
    tags=["bits"],
    order=1,
    body=BITS,
)
emit(
    "14-math-number-theory",
    "01-number-theory.mdx",
    title="Number Theory for Interviews",
    slug="number-theory",
    summary="Euclid, sieves, modular exponentiation, combinations, and trailing zeros.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["bit-manipulation"],
    tags=["math", "number-theory"],
    order=1,
    body=MATH,
)
