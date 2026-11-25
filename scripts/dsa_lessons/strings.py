"""KMP, rolling hashes, Z, Manacher, and suffix arrays."""

from emit import emit

MATCHING = r'''
## Why this matters

A nested loop that checks the pattern at every text offset is correct and easy to explain. It is also the wrong final answer when the strings are long. Interviewers use "find the first occurrence," "longest prefix that is also a suffix," and "does this string repeat" to see whether you know the linear string algorithms, or at least the border idea those algorithms share. Knuth-Morris-Pratt, Rabin-Karp, and the Z-algorithm all answer pattern search. They do not memorize the same table. KMP stores how far a partial match can fall back. Rabin-Karp hashes a window and slides it. The Z-algorithm stores how far each position matches the prefix. You should be able to build each table by hand on a short string and say which one a problem is actually asking for.

## Intuition

After a mismatch, you already know a chunk of characters. Throwing that chunk away and restarting at the next text character repeats work. A border of a string is a proper prefix that is also a suffix. If the pattern's matched part has a border of length k, the next comparison can resume at pattern index k, because those k characters are already known to match the text. KMP precomputes, for every prefix of the pattern, the longest border. Rabin-Karp does not use borders. It treats the window as a number in a large base, updates that number in constant time when the window slides by one, and checks the real characters only when the numbers agree. The Z-array answers a different question that happens to solve search: for each index, how long is the substring starting there that copies the beginning of the whole string.

## Core concept in depth

A string here is a finite sequence of characters. Indexing starts at 0. A prefix of s is s from the start through some index. A suffix is s from some index through the end. Proper means the piece is not the whole string. The longest proper prefix that is also a suffix is the border. For "aabaa" the borders are "a" and "aa", and the longest has length 2. The prefix function, also called the longest-prefix-suffix array or LPS, stores that length for every prefix. lps[i] is the border length of the prefix that ends at i, which is the slice s[0] through s[i].

Building the prefix function is itself a KMP scan of the pattern against itself. Keep a variable length, the border you are currently trying to extend. Walk i from 1 to the end. If pattern[i] equals pattern[length], extend the border, store it, and move i. If not, and length is positive, set length to lps[length - 1] and try again without moving i. That fallback is safe because a border of a border is a border. If length is already 0, the prefix has no border, store 0, and move i. The whole build is linear: i only moves forward, and length only moves forward when i does or falls back along previously stored borders, so the total fallback is at most the number of successful extensions.

Searching with that table uses two indices, i in the text and j in the pattern. On a match, advance both. When j reaches the pattern length, you have an occurrence ending at i, so the start is i - j. To find the next one, set j to lps[j - 1] and continue, because the occurrence itself has a border. On a mismatch, if j is positive, set j to lps[j - 1] and do not advance i. If j is 0, advance i. Each text character is examined a constant number of times in aggregate, so the search is linear in the text length plus the pattern length. The naive double loop is linear only in the average case for random strings. Its worst case is the product of the lengths, on a pattern of many identical characters and a text of the same character.

Rabin-Karp picks a base and a modulus. The hash of a window of length m is the polynomial base to the m - 1 times the first character, plus base to the m - 2 times the next, and so on, all modulo the modulus. When the window slides, subtract the outgoing character times base to the m - 1, multiply by the base, and add the incoming character, reducing modulo the modulus at each step. That is a rolling hash. A hit is not a proof. Different windows can share a hash. On a hit, compare the characters, or use a second modulus and accept only a double hit if the problem allows a tiny error probability. With one large prime modulus the error is rare for interview constraints and still not zero. Choose a base larger than the alphabet, often 26 or 256, and a prime modulus such as 10 to the 9 plus 7. In Python the modulus is optional because integers do not overflow, but a bounded hash is what the algorithm is. Reduce the subtraction with an added modulus so it does not go negative.

The Z-array of a string s has Z[0] = 0 by convention, and Z[i] equal to the greatest k such that the slice starting at i of length k equals the prefix of length k. The algorithm maintains a Z-box, the rightmost segment [left, right] that is known to match a prefix. If i lies past that box, compare characters from scratch and, if you match at least one, set the box to the new segment. If i lies inside the box, the mirror position i - left already has a Z value, and the box promises that the text around i copies the text around the mirror. So Z[i] starts at the minimum of Z[i - left] and the distance from i to the end of the box. Then extend by explicit comparisons past the box. Each character is copied into a successful comparison at most once, because the right endpoint only moves forward, so the algorithm is linear.

Search by Z is concatenation. Build the Z-array of pattern, plus a separator that appears in neither string, plus the text. An index whose Z value equals the pattern length, and that sits inside the text portion, is a match. The separator stops a match from crossing the boundary. The same prefix function answers "longest happy prefix": the border of the entire string is lps of the last index, and the string itself is excluded because borders are proper. Repeated substring pattern is the border test: a string repeats a block when it has a border whose length makes the period divide the length. If n is positive and lps[n - 1] is positive and n modulo (n - lps[n - 1]) is 0, the string is made of a repeated block. "abcabcabc" has period 3. "abab" has period 2. "aba" does not.

The naive specification is still worth writing, because it is the oracle. Recurse on a candidate alignment: if the pattern is exhausted, you matched; if the text is exhausted or the characters differ, that alignment fails; otherwise consume one character from both. Try every start iteratively. That recursion is the definition of "occurs at this index." KMP, Rabin-Karp, and Z compute the same answer. They differ in the table and in whether a hash collision can force an extra comparison.

## Diagram and dry run

```mermaid
flowchart TD
    A[Compare text index i with pattern index j] --> B{Characters equal?}
    B -->|Yes| C[Advance both]
    C --> D{Pattern exhausted?}
    D -->|Yes| E[Report a match and fall back by the border]
    D -->|No| A
    B -->|No| F{j is positive?}
    F -->|Yes| G[Set j to the border of the matched prefix]
    F -->|No| H[Advance i only]
    G --> A
    H --> A
```

Prefix function of "ababaca".

| i | character | length after the step | lps so far, written through i |
| --- | --- | --- | --- |
| 0 | a | 0 | 0 |
| 1 | b | mismatch at 0 | 0, 0 |
| 2 | a | extends to 1 | 0, 0, 1 |
| 3 | b | extends to 2 | 0, 0, 1, 2 |
| 4 | a | extends to 3 | 0, 0, 1, 2, 3 |
| 5 | c | falls from 3 to 1 to 0, then stores 0 | 0, 0, 1, 2, 3, 0 |
| 6 | a | extends to 1 | 0, 0, 1, 2, 3, 0, 1 |

At i = 5 the character c does not match pattern[3], which is b. The border of the prefix of length 3 is lps[2] = 1, and c does not match pattern[1], which is b. The border of that shorter prefix is lps[0] = 0, and c does not match pattern[0]. Store 0.

Z-array of "aabaab". Z[0] is 0. Index 1 matches one a and then stops, so Z[1] is 1 and the box is the single character at index 1. Index 2 is b against a, so Z[2] is 0. Index 3 matches a, a, b, three characters, and the box becomes indices 3 through 5. Index 4 copies the mirror Z[1], which is 1, and cannot extend. Index 5 copies Z[2], which is 0. The array is 0, 1, 0, 3, 1, 0.

A rolling window on text "abcd" and pattern "bcd", base 10, no modulus, characters as their alphabet rank a=1. The pattern hash is 2 * 100 + 3 * 10 + 4 = 234. The first window "abc" hashes to 123. Slide: drop 1, multiply 23 by 10, add 4, get 234. The hashes agree, and the characters agree.

## Runnable Python

The prefix function and the search are iterative. The recursive helper is the naive alignment check, the specification KMP replaces. Use KMP when you need a guaranteed linear scan. Use the recursive checker only on short strings or as an oracle.

```python
def build_lps(pattern: str) -> list[int]:
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return -1


def naive_search(text: str, pattern: str) -> int:
    def match_at(i: int, j: int) -> bool:
        if j == len(pattern):
            return True
        if i == len(text) or text[i] != pattern[j]:
            return False
        return match_at(i + 1, j + 1)

    if pattern == "":
        return 0
    last = len(text) - len(pattern)
    for start in range(last + 1):
        if match_at(start, 0):
            return start
    return -1
```

`build_lps("ababaca")` returns 0, 0, 1, 2, 3, 0, 1. `kmp_search("abababaca", "ababaca")` returns 2. `naive_search` returns the same index. An empty pattern returns 0, matching the usual library convention. A pattern longer than the text returns -1 because the start loop is empty and the KMP loop never fills j.

## Complexity and trade-offs

| Algorithm | Time | Extra space | Failure mode |
| --- | --- | --- | --- |
| Naive, every alignment | Theta of the product of the lengths, worst case | Theta(1) plus the recursion depth of the pattern if you match recursively | too slow on long repetitive strings |
| KMP | Theta of text length plus pattern length | the prefix array, linear in the pattern | none if the table is right |
| Rabin-Karp, one hash | expected linear, worst case the product if every window collides and you verify | Theta(1) | a collision you forget to verify |
| Z-algorithm | Theta of the concatenated length | the Z-array | a separator that occurs in the data |

KMP and Z are deterministic and linear. Rabin-Karp is the one you want when you have many patterns against one text and you can hash the patterns into a set, or when the interview is about rolling hashes specifically. A second modulus makes a false hit negligible. It does not make it impossible. For a library `find`, a well-implemented hybrid such as the one inside CPython is allowed to be more complicated than KMP. In an interview, name KMP or Z and implement one of them cleanly.

## Tricks, tips, and patterns

The border length lps[n - 1] is the longest happy prefix. The smallest period of a string that is built by repeating a block is n - lps[n - 1], and that period must divide n. When you only need existence of a pattern, you can stop KMP at the first time j reaches the pattern length. When you need all occurrences, fall back with the border and keep scanning, and remember that occurrences may overlap. A rolling hash of every prefix lets you compare two substrings in constant time after linear preprocessing, as long as you accept the collision story or verify. That is the bridge from Rabin-Karp to "are these two slices equal." Do not build the prefix function on the text. Build it on the pattern, or on pattern plus separator plus text when the problem is about the whole concatenation.

## Common mistakes and edge cases

Off-by-one in the fallback: the value to assign to j on a mismatch is lps[j - 1], the border of the matched prefix, not lps[j]. Forgetting that borders are proper, and returning the whole string as its own happy prefix. An empty pattern, an empty text, or a pattern longer than the text. Using a separator that appears in the text, so a Z match crosses the join. A rolling hash that goes negative after the subtraction, or that overflows a 32-bit integer in other languages before the modulus. Treating a hash hit as a match. Rebuilding the prefix function from scratch inside the search loop. Assuming the naive algorithm is always quadratic. It is quadratic in the worst case and often fine on short interview inputs. Say which bound you are claiming.

## Interview notes

State the definition of lps[i] before you write the loop. Dry-run "ababaca" or "aabaab". If the interviewer asks why the fallback does not miss a match, say that every shorter border is already stored, because a border of a border is a border, and the text characters you skip were compared on the way in. For Rabin-Karp, say "expected linear, verify collisions." For the repeated-string problem, derive the period from the border instead of inventing a new scan. Mention Z if you are more fluent with the box than with the prefix function. They are the same family.

## Practice problems

1. [Find the Index of the First Occurrence](/practice/find-the-index-of-the-first-occurrence) — implement KMP or a verified rolling hash.
2. [Longest Happy Prefix](/practice/longest-happy-prefix) — the last entry of the prefix function.
3. [Repeated Substring Pattern](/practice/repeated-substring-pattern) — the period test.
4. [Rabin-Karp Search](/practice/rabin-karp-search) and [Z-Algorithm Search](/practice/z-algorithm-search).

## Summary and cheat sheet

- A border is a proper prefix that is also a suffix. lps[i] is the longest border of the prefix ending at i.
- On a mismatch, resume the pattern at lps[j - 1]. Do not rewind the text.
- KMP build and search are both linear.
- Rabin-Karp slides a polynomial hash in constant time and verifies character equality on a hit.
- Z[i] is the longest prefix match starting at i. A Z-box copies mirror values and only extends the right edge forward.
- Search with Z by scanning pattern, a fresh separator, and the text.
- A string is a repeated block when n - lps[n - 1] divides n and the border is non-empty.

## Further reading

- [Wikipedia — Knuth-Morris-Pratt algorithm](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
- [CP-Algorithms — Prefix function](https://cp-algorithms.com/string/prefix-function.html)
- [CP-Algorithms — Rabin-Karp](https://cp-algorithms.com/string/rabin-karp.html)
- [CP-Algorithms — Z-function](https://cp-algorithms.com/string/z-function.html)
'''

PALINDROME = r'''
## Why this matters

Palindromes are a string topic of their own because the center of the answer can sit on a character or between two characters, and because the naive expansion repeats work that a radius array can reuse. Longest palindromic substring and the count of palindromic substrings are on the standard interview list. Manacher's algorithm solves the longest one in linear time. You should also know the quadratic expand-around-centers solution, which is what most interviews actually want written down, and you should know that the longest palindromic subsequence is a different problem and a dynamic program. The second half of this lesson is the suffix array, the sorted list of every suffix. You will not be asked to code a linear construction in a 45-minute round. You will be asked what the structure is, what the LCP array adds, and which questions become binary search plus a longest-common-prefix check once the suffixes are sorted.

## Intuition

A palindrome reads the same forward and backward, so it is determined by a center and a radius. Expand every center while the wings match. That is correct. Manacher notices that once you have expanded a long palindrome, the radii inside its right half mirror the radii inside its left half, until they hit the boundary of the long one. The suffix array is a different intuition: sorting the suffixes puts equal prefixes next to each other. The longest repeated substring is then the maximum longest-common-prefix of two adjacent suffixes. Pattern search is a binary search over that sorted list.

## Core concept in depth

A palindrome is a string equal to its reverse. The empty string and every single character are palindromes. A substring is a contiguous slice. A subsequence is not required to be contiguous. Those two words are the usual trap. Longest palindromic substring asks for a contiguous slice. Longest palindromic subsequence asks for a not-necessarily-contiguous sequence, and it is the longest common subsequence of the string with its reverse, or a direct interval DP. Do not run Manacher on a subsequence problem.

Expand around centers. There are 2n - 1 centers in a string of length n: n characters and n - 1 gaps between characters. For each center, walk outward while the indices stay inside the string and the characters match. Track the best slice. Each expansion can walk the whole string, and there are linearly many centers, so the time is quadratic and the extra space is constant if you only keep the best endpoints. Counting palindromic substrings is the same walk, incrementing a counter on every successful radius, including the single-character palindromes. A substring is counted once per center. That is the right count, because each palindromic substring has one center.

Manacher's algorithm makes the center story uniform and then adds the mirror. Insert a separator, conventionally a hash, between characters and at both ends. "abba" becomes "#a#b#b#a#". Every palindrome in the original string, odd or even, becomes an odd-length palindrome in the transformed string, centered on a character or on a separator. Let p[i] be the radius in the transformed string, the largest number such that the transformed characters i - p[i] and i + p[i] are inside and the slice between them is a palindrome. The corresponding original length is p[i], because the separators account for half the transformed width. Maintain the center and the right edge of the palindrome that currently reaches farthest right. When i is strictly inside that right edge, the mirror index is 2 * center - i, and p[i] starts at the minimum of p[mirror] and the distance from i to the right edge. Then try to expand past that guess by comparing characters. If i plus the new radius passes the old right edge, this center becomes the new owner of the right edge. The right edge only moves forward, and every expansion step that increases it charges a character, so the total expansion work is linear. The transform itself is linear. The answer is the maximum p[i], mapped back to a slice of the original string. If the center index in the transformed string is i and the radius is r, the original start is (i - r) // 2 and the original length is r.

The simple expansion is the algorithm to code under time pressure. Manacher is the algorithm to name when they ask for linear time, and to code if you have already practiced the radius table. Both return a real slice. If several slices tie, either is acceptable unless the problem asks for the earliest one. Take the one you find first and say so.

A suffix of s is a slice from some index through the end. The suffix array is the permutation of starting indices sorted by the suffixes those indices name. For "banana" the suffixes are banana, anana, nana, ana, na, a. Sorted in dictionary order they are a, ana, anana, banana, na, nana, so the suffix array is 5, 3, 1, 0, 4, 2. Sorting with ordinary string comparison costs an extra linear factor in the string length per comparison, so this construction is fine for teaching and too slow for a long string. Linear constructions exist. The DC3 algorithm, also called skew, and the prefix-doubling algorithm that sorts by the first 1, 2, 4, 8 characters, are the ones textbooks name. Prefix doubling runs in n log squared n with a standard sort, or n log n with a radix sort. You should be able to describe doubling: each suffix is a pair of ranks of its two halves, and after a sort the pairs become the new ranks. You are not expected to debug DC3 on a whiteboard.

The LCP array stores, between each pair of adjacent entries in the suffix array, the length of their longest common prefix. For "banana" the adjacent LCP values are 1 (a against ana), 3 (ana against anana), 0 (anana against banana), 0 (banana against na), and 2 (na against nana). A direct comparison computes this in quadratic time. Kasai's algorithm computes it in linear time from the string and the suffix array, using one inequality: if the LCP of the suffix starting at i with its neighbor in suffix-array order is h, then the LCP of the suffix starting at i + 1 with its own neighbor is at least h - 1. You can drop the first character and the rest of the common prefix still matches, except that the neighbor might change. Mention Kasai. Implement the direct comparison unless you have the linear version solid.

What the pair of arrays gives you. The longest repeated substring is the maximum LCP, and the substring is the prefix of either adjacent suffix of that length. The number of distinct substrings is n(n + 1) / 2 minus the sum of the LCP array, because every substring is a prefix of some suffix, and adjacent suffixes share LCP prefixes that would otherwise be counted twice along the sorted order. Pattern search is binary search on the suffix array: compare the pattern with the suffix at the middle index, and walk left or right. With an LCP structure that answers range minimum queries, the binary search compares only the characters it has not already deduced, but a plain binary search that compares the pattern from scratch is already n log n character inspections in the worst case and is the right interview description. A suffix automaton and a suffix tree represent the same family of facts with different shapes. The tree is the compacted trie of all suffixes. The array is the more common competitive-programming tool. For this course the array plus the LCP definition is the required intro.

## Diagram and dry run

```mermaid
flowchart TD
    A[Transformed string with separators] --> B[Walk centers left to right]
    B --> C{Inside the current right edge?}
    C -->|Yes| D[Copy the mirror radius, clipped to the edge]
    C -->|No| E[Start from radius 0]
    D --> F[Expand while the wings match]
    E --> F
    F --> G[If this palindrome sets a new right edge, keep it]
```

Expand-around-centers on "abba". Centers and the slice they produce:

| Center | Expansion | Slice |
| --- | --- | --- |
| on a at 0 | single character | a |
| between 0 and 1 | a against b, stop | empty gap |
| on b at 1 | single b, wings a and b differ | b |
| between the two b characters | b matches b, then a matches a | abba |
| on b at 2 | single b | b |
| between 2 and 3 | b against a, stop | empty gap |
| on a at 3 | single a | a |

The best slice is "abba".

Manacher on the same string. The transformed characters are hash, a, hash, b, hash, b, hash, a, hash, at indexes 0 through 8. Radii grow as follows. Index 0 cannot expand. Index 1 expands to radius 1, and the right edge becomes 2. Index 2 does not expand. Index 3 expands to radius 1, and the right edge becomes 4. Index 4, the middle hash, expands through both b characters and both a characters out to the ends, radius 4, and the right edge becomes 8. Radius 4 is the whole original string. Later centers sit inside that edge and only copy mirrors. The original start is (4 - 4) / 2 = 0 and the length is 4.

Suffix array of "banana":

| Suffix array index | Start | Suffix | LCP with the next row |
| --- | --- | --- | --- |
| 5 | 5 | a | 1 |
| 3 | 3 | ana | 3 |
| 1 | 1 | anana | 0 |
| 0 | 0 | banana | 0 |
| 4 | 4 | na | 2 |
| 2 | 2 | nana | none |

The longest repeated substring is "ana", from the LCP of 3.

## Runnable Python

Center expansion is a pair of loops, one iterative scan of centers and one iterative expansion. The recursive formulation expands one wing and returns the endpoints. It is the same algorithm with the call stack holding the radius. Prefer the loops. The suffix-array helpers sort and then compare adjacent suffixes. They are the introductory construction, not DC3.

```python
def longest_palindrome(s: str) -> str:
    if s == "":
        return ""
    best_l, best_r = 0, 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for i in range(len(s)):
        for left, right in (expand(i, i), expand(i, i + 1)):
            if right - left > best_r - best_l:
                best_l, best_r = left, right
    return s[best_l:best_r + 1]


def expand_rec(s: str, left: int, right: int) -> tuple[int, int]:
    if left < 0 or right >= len(s) or s[left] != s[right]:
        return left + 1, right - 1
    return expand_rec(s, left - 1, right + 1)


def suffix_array(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])


def lcp_adjacent(s: str, sa: list[int]) -> list[int]:
    values = []
    for a, b in zip(sa, sa[1:]):
        k = 0
        while a + k < len(s) and b + k < len(s) and s[a + k] == s[b + k]:
            k += 1
        values.append(k)
    return values
```

`longest_palindrome("abba")` returns "abba". `longest_palindrome("aba")` returns "aba". `expand_rec("abba", 1, 2)` starts between the two b characters and returns the endpoints 0 and 3. `suffix_array("banana")` returns 5, 3, 1, 0, 4, 2. `lcp_adjacent` of that array returns 1, 3, 0, 0, 2. The maximum entry is the length of the longest repeated substring.

## Complexity and trade-offs

| Tool | Time | Space | What you get |
| --- | --- | --- | --- |
| Expand around centers | Theta(n squared) | Theta(1) extra | one palindromic substring, or a count |
| Manacher | Theta(n) | Theta(n) for the transform and the radii | the same substring, linear |
| Interval DP for the subsequence | Theta(n squared) | Theta(n squared), rollable | a subsequence, not a slice |
| Suffix array by sorting suffixes | Theta(n squared log n) character work | Theta(n) | the order of suffixes |
| Prefix doubling | Theta(n log squared n) or better with radix sort | Theta(n) | the same order, the practical construction |
| Kasai LCP | Theta(n) after the suffix array | Theta(n) | adjacent LCP values |
| Direct adjacent LCP | Theta(n squared) worst case | Theta(1) extra | fine for a short demo |

Manacher is not a replacement for the subsequence DP. The suffix array is not a replacement for KMP when you have one pattern and one text and no other queries. Build the heavier structure when you have many queries, repeated-substring questions, or a reason to binary-search suffixes.

## Tricks, tips, and patterns

Write 2n - 1 centers on the board so you do not forget even lengths. In the transform, the original length equals the radius, and the original start is (i - r) // 2. Guard the empty string before you divide. For counts, every radius step is one palindromic substring, and the single letters must be included. If the problem allows any longest slice, keep the first maximum and do not sort the candidates. For suffix arrays, draw "banana" from memory. It is the example every reader of the structure has seen, which makes your LCP numbers easy to check. When you need the longest common substring of two strings, concatenate them with a separator and take the maximum LCP among adjacent suffixes that come from different sides. That is the standard application, and it is still an introduction, not a second data structure.

## Common mistakes and edge cases

Returning a subsequence from an expansion, or a substring from the subsequence DP. Forgetting even centers, so "aa" becomes "a". An infinite expansion because the bounds are checked after the character access. Manacher radii copied from the mirror without clipping to the right edge, which invents characters past the known palindrome. Mapping the transformed index back to the original string with the wrong formula and slicing off a separator. An empty string. A string of one character. Suffix sorting that compares only the first character. LCP computed against the original index order instead of the suffix-array order. Claiming a linear suffix array and then coding `sorted` on the slices. Those are different algorithms. Say which one you wrote.

## Interview notes

Start with expand-around-centers unless they asked for linear time. Dry-run "abba" or "cbbd". Name Manacher and the mirror idea in two sentences if they push on complexity. If the word subsequence appears, stop and switch to the DP from the classic families lesson. For suffix arrays, define the array, sort "banana", define LCP, and name one query: longest repeated substring, or pattern search by binary search. Mention Kasai and prefix doubling as the efficient constructions. Do not start DC3 unless you can finish it.

## Practice problems

1. [Longest Palindromic Substring](/practice/longest-palindromic-substring) — expand, or Manacher if you want the linear pass.
2. [Palindromic Substrings](/practice/palindromic-substrings) — count every center you can expand.
3. [Longest Palindromic Subsequence](/practice/longest-palindromic-subsequence) — the DP, not Manacher.
4. [Valid Palindrome](/practice/valid-palindrome) — a two-pointer check, useful as a warmup before radii.
5. [Palindrome Partitioning](/practice/palindrome-partitioning) — backtracking over palindromic cuts.

## Summary and cheat sheet

- A palindromic substring has a center and a radius. There are 2n - 1 centers.
- Expand-around-centers is quadratic and is the usual interview code.
- Manacher inserts separators, copies mirror radii inside the current right edge, and runs in linear time.
- Map a transformed center i and radius r back with start (i - r) // 2 and length r.
- A palindromic subsequence is a different problem. Use DP.
- The suffix array is the starts of all suffixes in sorted order. Sorting slices is the teaching construction.
- The LCP array stores adjacent shared-prefix lengths. Its maximum is the longest repeated substring.
- Kasai builds LCP in linear time. Prefix doubling builds the suffix array efficiently. Pattern search is binary search on the suffix array.

## Further reading

- [Wikipedia — Longest palindromic substring](https://en.wikipedia.org/wiki/Longest_palindromic_substring)
- [CP-Algorithms — Manacher](https://cp-algorithms.com/string/manacher.html)
- [Wikipedia — Suffix array](https://en.wikipedia.org/wiki/Suffix_array)
- [CP-Algorithms — Suffix array](https://cp-algorithms.com/string/suffix-array.html)
- [Wikipedia — LCP array](https://en.wikipedia.org/wiki/LCP_array)
'''

emit(
    "15-string-algorithms",
    "01-kmp-rabin-karp-z.mdx",
    title="KMP, Rabin-Karp, and the Z-Algorithm",
    slug="kmp-rabin-karp-z",
    summary="Borders, the prefix function, rolling hashes, and the Z-box, all used for linear pattern search.",
    duration=45,
    difficulty="advanced",
    prerequisites=["number-theory"],
    tags=["strings", "kmp"],
    order=1,
    body=MATCHING,
)
emit(
    "15-string-algorithms",
    "02-manacher-and-suffix-arrays.mdx",
    title="Manacher and Suffix Arrays",
    slug="manacher-and-suffix-arrays",
    summary="Palindromic radii, Manacher's mirror, and the suffix array with its LCP array.",
    duration=45,
    difficulty="advanced",
    prerequisites=["kmp-rabin-karp-z"],
    tags=["strings", "suffix-array"],
    order=2,
    body=PALINDROME,
)
