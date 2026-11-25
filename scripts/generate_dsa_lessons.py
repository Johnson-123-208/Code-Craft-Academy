#!/usr/bin/env python3
"""Generate complete DSA MDX lessons for CodeCraft Academy (all modules).

Preserves content/dsa/01-foundations/01-big-o-and-complexity.mdx.
MDX-safe: curly braces neutralized outside fenced code blocks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DSA = ROOT / "content" / "dsa"

SKIP = {("01-foundations", "01-big-o-and-complexity.mdx")}


def neutralize_outside_fences(text: str) -> str:
    """Replace { } outside ``` fences so MDX does not parse JSX."""
    parts: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.startswith("```"):
            in_fence = not in_fence
            parts.append(line)
            continue
        if in_fence:
            parts.append(line)
        else:
            parts.append(line.replace("{", "(").replace("}", ")"))
    return "".join(parts)


def frontmatter(meta: dict[str, Any]) -> str:
    tags = ", ".join(f'"{t}"' for t in meta["tags"])
    prereq = ", ".join(f'"{p}"' for p in meta["prerequisites"])
    return (
        "---\n"
        f'title: "{meta["title"]}"\n'
        f'slug: "{meta["slug"]}"\n'
        f'summary: "{meta["summary"]}"\n'
        f'duration: {meta["duration"]}\n'
        f'difficulty: "{meta["difficulty"]}"\n'
        f"prerequisites: [{prereq}]\n"
        f"tags: [{tags}]\n"
        f'order: {meta["order"]}\n'
        "---\n"
    )


def build_mdx(meta: dict[str, Any], body: dict[str, str]) -> str:
    raw = (
        frontmatter(meta)
        + f"""
## Why this matters

{body["why"]}

## Intuition

{body["intuition"]}

## Core concept in depth

{body["core"]}

## Diagram / flowchart

```mermaid
{body["mermaid"].strip()}
```

### Dry-run

{body["dry_run"]}

## Code

```python
{body["code"].strip()}
```

## Complexity analysis

{body["complexity"]}

## Tricks, tips and patterns

{body["tricks"]}

## Common mistakes and edge cases

{body["mistakes"]}

## Interview notes

{body["interview"]}

## Practice problems

{body["practice"]}

## Summary / cheat sheet

{body["summary"]}

## Further reading

{body["further"]}
"""
    )
    return neutralize_outside_fences(raw.lstrip("\n") if raw.startswith("\n") else raw)


# ---------------------------------------------------------------------------
# Catalog: (module, filename, meta, body)
# ---------------------------------------------------------------------------

CatalogEntry = tuple[str, str, dict[str, Any], dict[str, str]]
CATALOG: list[CatalogEntry] = []


def lesson(
    module: str,
    filename: str,
    *,
    title: str,
    slug: str,
    summary: str,
    duration: int,
    difficulty: str,
    prerequisites: list[str],
    tags: list[str],
    order: int,
    why: str,
    intuition: str,
    core: str,
    mermaid: str,
    dry_run: str,
    code: str,
    complexity: str,
    tricks: str,
    mistakes: str,
    interview: str,
    practice: str,
    cheat: str,
    further: str,
) -> None:
    meta = {
        "title": title,
        "slug": slug,
        "summary": summary,
        "duration": duration,
        "difficulty": difficulty,
        "prerequisites": prerequisites,
        "tags": tags,
        "order": order,
    }
    body = {
        "why": why,
        "intuition": intuition,
        "core": core,
        "mermaid": mermaid,
        "dry_run": dry_run,
        "code": code,
        "complexity": complexity,
        "tricks": tricks,
        "mistakes": mistakes,
        "interview": interview,
        "practice": practice,
        "summary": cheat,
        "further": further,
    }
    CATALOG.append((module, filename, meta, body))


# ========================= 01 FOUNDATIONS =========================

lesson(
    "01-foundations",
    "02-amortized-analysis.mdx",
    title="Amortized Analysis",
    slug="amortized-analysis",
    summary="Aggregate, accounting, and potential methods for dynamic arrays and union-find.",
    duration=30,
    difficulty="intermediate",
    prerequisites=["big-o-and-complexity"],
    tags=["amortized", "complexity", "foundations"],
    order=2,
    why="Interviewers ask why vector append is O(1) amortized when resizing is O(n). Amortized analysis is the precise answer and reappears in union-find and splay trees.",
    intuition="A coffee punch card makes most cups cost one stamp and the tenth free. Per-cup cost varies, but the long-run average is stable. Amortized analysis studies that average over a worst-case sequence.",
    core="""### Three methods

1. **Aggregate** — bound total cost T(n) of n ops; amortized cost is T(n)/n.
2. **Accounting** — overcharge cheap ops, bank credit, spend on expensive ones.
3. **Potential** — define Φ(state); amortized = actual + Φ_after − Φ_before.

### Dynamic array

Capacity doubles when full. One append may copy n elements, but across n appends from empty, copies sum to less than 2n → amortized O(1).

### Union-Find

Path compression + union by rank yields nearly O(1) amortized per op (inverse Ackermann α(n)).""",
    mermaid="""flowchart TD
    A[n operations] --> B{Method}
    B -->|Aggregate| C[T(n)/n]
    B -->|Accounting| D[Credit tokens]
    B -->|Potential| E[Φ state]
    C --> F[Amortized bound]
    D --> F
    E --> F""",
    dry_run="""Appending with doubling from empty: resizes at sizes 1,2,4,8,… copy costs 1+2+4+…+n/2 less than n. Total actual work O(n) for n appends → amortized O(1) each.""",
    code='''from __future__ import annotations


class DynamicArray:
    def __init__(self) -> None:
        self._data: list[int | None] = [None]
        self._size = 0
        self._cap = 1

    def append(self, value: int) -> None:
        if self._size == self._cap:
            self._resize(self._cap * 2)
        self._data[self._size] = value
        self._size += 1

    def _resize(self, new_cap: int) -> None:
        new_data: list[int | None] = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._cap = new_cap
''',
    complexity="""| Op | Worst single | Amortized |
| --- | --- | --- |
| Dynamic array append | O(n) | O(1) |
| Union-Find find (PC+rank) | uncommon spikes | ≈ O(α(n)) |

Doubling forms a geometric series bounded by 2n.""",
    tricks="""- Say amortized O(1), not average O(1) — average implies randomness.
- Potential Φ should stay non-negative (or bounded below).
- Shrink capacity only at 1/4 full to avoid thrashing.""",
    mistakes="""- Claiming every append is worst-case O(1).
- Shrinking at capacity/2 → O(n²) push/pop thrashing.
- Forgetting amortized bounds assume a known starting state.""",
    interview="""State: worst single append O(n) on resize; any sequence of n appends totals O(n), so amortized O(1). Offer the geometric-series proof in 30 seconds.""",
    practice="""1. Amortized cost of binary counter increments (easy)
2. Two-stack queue amortized O(1) (medium)
3. Multipop stack aggregate analysis (medium)""",
    cheat="""- Amortized = worst-case sequence average, not random average.
- Aggregate / accounting / potential are interchangeable toolkits.
- Dynamic arrays and union-find are the classic examples.""",
    further="""- [Wikipedia — Amortized analysis](https://en.wikipedia.org/wiki/Amortized_analysis)
- [CLRS — Amortized Analysis](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)""",
)

lesson(
    "01-foundations",
    "03-recurrence-master-theorem.mdx",
    title="Recurrence Relations and the Master Theorem",
    slug="recurrence-master-theorem",
    summary="Solve divide-and-conquer recurrences with trees, substitution, and the Master theorem.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["big-o-and-complexity"],
    tags=["recurrence", "master-theorem", "divide-and-conquer"],
    order=3,
    why="Merge sort, binary search, and many D&C algorithms are defined by recurrences. You must go from T(n)=2T(n/2)+O(n) to Θ(n log n) cleanly.",
    intuition="A recurrence is a recursive bill: pay f(n) now, then pay the same style of bill on smaller pieces. The Master theorem is a lookup table for common bills.",
    core="""### Form

T(n) = a·T(n/b) + f(n), T(1)=Θ(1).

- a ≥ 1 subproblems, b > 1 shrink factor, f(n) non-recursive work.

### Master cases

Compare f(n) to n^(log_b a):

1. f polynomially smaller → T = Θ(n^(log_b a))
2. f same order (possibly times log^k n) → root/levels share cost → usually Θ(n^(log_b a) log n)
3. f polynomially larger + regularity → T = Θ(f(n))

Also use recursion trees and induction (substitution).""",
    mermaid="""flowchart TD
    R["T(n)=a T(n/b)+f(n)"] --> C{f vs n^log_b a}
    C -->|smaller| C1[Case 1 leaves dominate? no — root]
    C -->|similar| C2[Case 2 all levels]
    C -->|larger| C3[Case 3 leaves/work dominates]""",
    dry_run="""Merge sort: a=2,b=2,f=Θ(n) → log_b a=1 → Case 2 → Θ(n log n). Binary search: a=1,b=2,f=Θ(1) → Θ(log n). Fibonacci recurrence is not Master form — use DP.""",
    code='''from __future__ import annotations
import math

def master_case(a: float, b: float, f_exp: float, eps: float = 1e-9) -> str:
    crit = math.log(a) / math.log(b)
    if f_exp < crit - eps:
        return f"Case 1: Θ(n^{crit:.4g})"
    if abs(f_exp - crit) <= eps:
        return f"Case 2: Θ(n^{crit:.4g} log n)"
    return f"Case 3: Θ(n^{f_exp})"
''',
    complexity="""| Recurrence | Bound |
| --- | --- |
| 2T(n/2)+Θ(n) | Θ(n log n) |
| T(n/2)+Θ(1) | Θ(log n) |
| 2T(n/2)+Θ(1) | Θ(n) |
| T(n−1)+Θ(n) | Θ(n²) (sum, not Master) |""",
    tricks="""- Always compute log_b a first.
- Draw a 3-level tree in interviews — it sells the bound.
- Uneven splits → Akra–Bazzi or tree summation.""",
    mistakes="""- Applying Master to overlapping Fibonacci recursion.
- Swapping a and b.
- Ignoring that floors/ceilings rarely change asymptotics.""",
    interview="""Write recurrence → identify a,b,f → state case → give Θ. If unsure, sum a geometric series on a recursion tree.""",
    practice="""1. T(n)=4T(n/2)+n (easy)
2. T(n)=2T(n/2)+n log n (medium)
3. Compare Strassen vs classic multiply (medium)""",
    cheat="""- Master covers a·T(n/b)+f(n).
- Compare f to n^(log_b a).
- Overlapping subproblems → DP, not Master.""",
    further="""- [Wikipedia — Master theorem](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms))
- [CLRS Chapter 4](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)""",
)

lesson(
    "01-foundations",
    "04-how-to-approach-problems.mdx",
    title="How to Approach Any DSA Problem",
    slug="how-to-approach-problems",
    summary="Clarify, examples, brute force, optimize, code, test, analyze — a repeatable interview loop.",
    duration=25,
    difficulty="beginner",
    prerequisites=["big-o-and-complexity"],
    tags=["problem-solving", "interview", "framework"],
    order=4,
    why="Knowing algorithms is not enough. Top candidates convert ambiguous prompts into correct analyzed code under time pressure with a disciplined process.",
    intuition="Treat each problem like debugging: reproduce with examples, hypothesize a pattern, ship the simplest correct fix, then optimize with evidence.",
    core="""### Seven steps

1. Clarify inputs/outputs and edge rules
2. Read constraints → pick target complexity
3. Walk a happy-path example + one edge
4. State a correct brute force
5. Name a pattern and invariant
6. Code cleanly
7. Dry-run and state time/space

### Cue → pattern

Sorted → binary search / two pointers. Faster lookups → hash. Optimal substructure + overlap → DP. All configs → backtracking. Unweighted shortest path → BFS.""",
    mermaid="""flowchart TD
    A[Prompt] --> B[Clarify + constraints]
    B --> C[Examples]
    C --> D[Brute force]
    D --> E[Pattern]
    E --> F[Code]
    F --> G[Dry-run + complexity]""",
    dry_run="""Two Sum: clarify indices + unique pair. n≤10^4 → prefer O(n). Brute nested loops. Optimize with hash complement. Test [2,7,11,15],9 → [0,1]. O(n) time O(n) space.""",
    code='''from __future__ import annotations
from typing import Callable

def solve_with_framework(clarify, brute, optimize, verify):
    clarify()
    slow = brute()
    assert verify(slow)
    fast = optimize()
    assert verify(fast)
    return fast
''',
    complexity="""| n | Typical target |
| --- | --- |
| ≤ 20 | O(2^n) OK |
| ≤ 10^3 | O(n²) OK |
| ≤ 10^5 | O(n log n) / O(n) |
| ≥ 10^6 | careful O(n) |""",
    tricks="""- Speak constraints aloud — they pick the algorithm.
- If stuck 5 minutes, return to brute force and ask what work repeats.
- Keep one invariant sentence while coding.""",
    mistakes="""- Coding before an example.
- Optimizing an incorrect brute force.
- Hidden O(n) copies that blow the complexity story.""",
    interview="""Open with: I'll clarify, give brute force, then optimize. Process marks matter as much as the final code.""",
    practice="""1. Framework on Valid Anagram (easy)
2. Framework on longest unique substring (medium)
3. 25-minute timed medium mock""",
    cheat="""- Clarify → examples → brute → pattern → code → test → analyze.
- Constraints dictate complexity budget.
- Patterns are hypotheses verified by dry-runs.""",
    further="""- [Tech Interview Handbook](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/)
- [NeetCode roadmap](https://neetcode.io/roadmap)""",
)

lesson(
    "01-foundations",
    "05-how-to-learn-dsa.mdx",
    title="How to Learn DSA Effectively",
    slug="how-to-learn-dsa",
    summary="Spaced repetition, active recall, pattern notebooks, and a progressive practice plan.",
    duration=20,
    difficulty="beginner",
    prerequisites=["how-to-approach-problems"],
    tags=["learning", "study-plan", "foundations"],
    order=5,
    why="Volume without retention fails interviews. Deliberate practice turns lessons and problems into durable pattern recognition.",
    intuition="Musicians slow hard passages and revisit them on a schedule. DSA is the same sport for working memory.",
    core="""### Principles

Active recall, spaced repetition (1d/3d/7d/21d), a pattern notebook (trigger + template + pitfalls), interleaving topics, and depth over binge counts.

### Ladder

Lesson → guided problems → mixed review → mock interview → schedule revisits.

### Log fields

Pattern, minutes to AC, mistakes, confidence for cold re-solve.""",
    mermaid="""flowchart LR
    L[Lesson] --> G[Guided]
    G --> R[Spaced review]
    R --> M[Mock]
    M --> L""",
    dry_run="""Day 1: sliding window lesson + 3 easies. Day 2: two mediums + notes. Day 4: re-solve Day 1 cold. Day 8: timed mixed set including one window problem.""",
    code='''from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class ProblemLog:
    slug: str
    pattern: str
    minutes: int
    confident: bool
    next_review: date = field(default_factory=date.today)

    def schedule(self) -> None:
        self.next_review = date.today() + timedelta(days=1 if not self.confident else 7)
''',
    complexity="""Human-time complexity: 8–12 weeks at 1–2 hours/day covering core patterns beats memorizing hundreds of solutions.""",
    tricks="""- Re-type from memory; never copy-paste editorials into muscle memory.
- Rubber-duck explanations expose gaps.
- After AC, write a 3-line pattern trigger.""",
    mistakes="""- Only reading solutions.
- 50 array problems then zero graphs.
- Skipping review because you already solved it once.""",
    interview="""If asked how you prepared, briefly describe your spaced system — it signals maturity. Then focus on clear thinking.""",
    practice="""1. 14-day arrays+hashing plan (easy)
2. Pattern pages for two pointers and BFS (medium)
3. 45-minute mock with failure log (medium)""",
    cheat="""- Active recall + spacing beat binge grinding.
- Pattern notebook with triggers.
- Interleave and track confidence.""",
    further="""- [Retrieval practice](https://www.retrievalpractice.org/)
- [Anki](https://apps.ankiweb.net/)""",
)

# ========================= 02 ARRAYS / STRINGS =========================

def _std_further(*urls: str) -> str:
    return "\n".join(f"- {u}" for u in urls)


lesson(
    "02-arrays-strings",
    "01-arrays-and-strings-overview.mdx",
    title="Arrays and Strings Overview",
    slug="arrays-and-strings-overview",
    summary="Memory layout, indexing, mutability, and when arrays beat linked structures.",
    duration=25,
    difficulty="beginner",
    prerequisites=["how-to-approach-problems"],
    tags=["arrays", "strings", "overview"],
    order=1,
    why="Most interview problems start as arrays or strings. Understanding contiguous memory, indexing costs, and Python list vs str semantics prevents silent O(n²) bugs.",
    intuition="An array is a numbered row of lockers: jump to locker i in O(1). A string is often an immutable array of characters — editing means building a new row.",
    core="""### Properties

- Random access O(1)
- Append amortized O(1) in dynamic arrays; insert/delete in middle O(n)
- Cache-friendly contiguous layout

### Python notes

list is a dynamic array. str is immutable — repeated += in a loop is O(n²); use join. bytearray when you need mutable bytes.

### Patterns preview

Two pointers, sliding window, prefix sums, in-place partitioning.""",
    mermaid="""flowchart LR
    A[Array/String problem] --> B{Need?}
    B -->|Subarray/substring| W[Window / prefix]
    B -->|Pair ends| T[Two pointers]
    B -->|Reorder| P[Partition / sort]""",
    dry_run="""Building s = '' then s += c for n chars copies 1+2+…+n = Θ(n²). Using parts.append(c); ''.join(parts) is Θ(n).""",
    code='''from __future__ import annotations

def reverse_inplace(a: list[int]) -> None:
    i, j = 0, len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
''',
    complexity="""| Op | list | str |
| --- | --- | --- |
| index | O(1) | O(1) |
| append / += char | amort O(1) | O(n) new string |
| insert mid | O(n) | O(n) |""",
    tricks="""- Prefer indices over slicing when you need O(1) views of ranges (slices copy).
- For immutable strings, gather chunks then join once.""",
    mistakes="""- s += in a loop.
- Assuming list.pop(0) is O(1) — it is O(n); use collections.deque.""",
    interview="""Mention cache locality when comparing arrays to linked lists — shows systems awareness.""",
    practice="""1. Reverse string in-place (easy)
2. Merge sorted arrays (easy)
3. Product of array except self (medium)""",
    cheat="""- Arrays: O(1) index, O(n) mid insert.
- Strings immutable in Python — join chunks.
- Most patterns build on index manipulation.""",
    further=_std_further(
        "[Python Time Complexity](https://wiki.python.org/moin/TimeComplexity)",
        "[Arrays — CP Algorithms](https://cp-algorithms.com/)",
    ),
)

lesson(
    "02-arrays-strings",
    "02-two-pointers.mdx",
    title="Two Pointers",
    slug="two-pointers",
    summary="Opposite ends and same-direction pointers for pairs, palindromes, and partitions.",
    duration=30,
    difficulty="beginner",
    prerequisites=["arrays-and-strings-overview"],
    tags=["two-pointers", "arrays"],
    order=2,
    why="Two pointers turn many O(n²) pair searches on sorted data into O(n), and they enable elegant in-place rewrites.",
    intuition="Two fingers walking a page: sometimes toward each other to find a pair summing to target, sometimes one leads and one follows to strip duplicates.",
    core="""### Styles

1. **Opposite ends** — sorted two-sum, container with most water, palindrome check
2. **Same direction (fast/slow)** — remove duplicates, move zeros, cycle ideas on arrays
3. **Partition** — Dutch national flag style

### Invariant examples

- All indices less than lo are less than pivot
- Characters outside [L,R] are already decided""",
    mermaid="""flowchart LR
    A[Sorted array] --> B[L=0 R=n-1]
    B --> C{sum vs target}
    C -->|too small| D[L++]
    C -->|too big| E[R--]
    C -->|equal| F[Found]""",
    dry_run="""Two-sum sorted [1,2,4,6,8] target 10: L=0,R=4 → 9 too small → L=1 → 10 done (2,8).""",
    code='''from __future__ import annotations

def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return []
''',
    complexity="""Time O(n) after sort O(n log n) if needed. Space O(1) extra for opposite-ends patterns.""",
    tricks="""- Sorting destroys original indices — keep (value,index) pairs when indices matter.
- For strings, skip non-alphanumeric in palindrome checks.""",
    mistakes="""- Off-by-one when lo and hi meet.
- Using two pointers on unsorted data for two-sum without sorting or hashing.""",
    interview="""State the invariant before coding. Interviewers listen for why L++ or R-- is safe.""",
    practice="""1. Valid palindrome (easy)
2. Container with most water (medium)
3. 3Sum (medium)""",
    cheat="""- Opposite ends for sorted pair problems.
- Fast/slow for in-place filtering.
- Always announce the invariant.""",
    further=_std_further("[Two pointers pattern — NeetCode](https://neetcode.io/)"),
)

lesson(
    "02-arrays-strings",
    "03-sliding-window.mdx",
    title="Sliding Window",
    slug="sliding-window",
    summary="Fixed and variable windows for subarray/substring optima in O(n).",
    duration=35,
    difficulty="intermediate",
    prerequisites=["two-pointers"],
    tags=["sliding-window", "arrays", "strings"],
    order=3,
    why="Subarray problems with contiguous constraints explode into O(n²) if you restart every left bound. Sliding window reuses work as the window crawls.",
    intuition="A train window moving along cars: add the new car on the right, drop cars on the left when the view breaks a rule (too many unique chars, sum too large, …).",
    core="""### Templates

**Fixed size k** — maintain sum/state of nums[i−k+1..i].

**Variable** — expand right; while invalid, shrink left; track best.

### Typical state

Counts map, number of zeros, running sum, last-seen index.""",
    mermaid="""flowchart TD
    R[Expand right] --> V{Window valid?}
    V -->|yes| T[Update answer]
    V -->|no| L[Shrink left]
    L --> V
    T --> R""",
    dry_run="""Longest substring without repeat: s=abcab. Grow to abc (best=3), add a → shrink until one a remains → cab (best=3), …""",
    code='''from __future__ import annotations

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
''',
    complexity="""O(n) time when each index enters/leaves at most once. Space O(Σ) for alphabet/map.""",
    tricks="""- Prefer while-invalid shrink over restarting left at 0.
- For at most K distinct, count how many keys are live.""",
    mistakes="""- Updating answer before shrinking when constraint is violated.
- Forgetting to move left past previous duplicate index.""",
    interview="""Name fixed vs variable. Sketch expand/shrink. Confirm each pointer moves ≤ n times.""",
    practice="""1. Max sum subarray of size k (easy)
2. Longest substring without repeating (medium)
3. Minimum window substring (hard)""",
    cheat="""- Contiguous + constraint → sliding window.
- Expand right, shrink left, track best.
- O(n) if amortized one pass each pointer.""",
    further=_std_further("[Sliding window — Educative patterns](https://www.educative.io/)"),
)

lesson(
    "02-arrays-strings",
    "04-prefix-sums.mdx",
    title="Prefix Sums",
    slug="prefix-sums",
    summary="Precompute running sums for O(1) range queries and subarray-sum counting.",
    duration=30,
    difficulty="beginner",
    prerequisites=["arrays-and-strings-overview"],
    tags=["prefix-sums", "arrays"],
    order=4,
    why="Range sum queries and 'subarray sum equals k' become trivial once you store prefix[i] = sum of first i elements.",
    intuition="Mileage markers on a highway: distance between exits i and j is marker[j] − marker[i].",
    core="""### Definition

prefix[0]=0; prefix[i]=nums[0]+…+nums[i−1].
Range sum [L,R] inclusive = prefix[R+1]−prefix[L].

### Subarray sum equals k

Count frequencies of prefix values; for each prefix[j], add count of prefix[j]−k.

### 2D prefix

Inclusion-exclusion on corners for matrix regions.""",
    mermaid="""flowchart LR
    A[nums] --> B[prefix]
    B --> C["sum(L..R)=P[R+1]-P[L]"]""",
    dry_run="""nums=[1,2,3], prefix=[0,1,3,6]. Sum index 1..2 = 6−1=5.""",
    code='''from __future__ import annotations
from collections import defaultdict

def subarray_sum(nums: list[int], k: int) -> int:
    count = defaultdict(int)
    count[0] = 1
    pref = 0
    ans = 0
    for x in nums:
        pref += x
        ans += count[pref - k]
        count[pref] += 1
    return ans
''',
    complexity="""Build O(n), query O(1). Subarray sum equals k: O(n) time O(n) space.""",
    tricks="""- Include prefix 0 → 1 so subarrays from index 0 count.
- For modulo problems, store prefix % m carefully with negatives.""",
    mistakes="""- Off-by-one between inclusive/exclusive prefix conventions.
- Mutating nums in place without documenting the scheme.""",
    interview="""Draw the prefix array once. Mention hash map extension for equals-k.""",
    practice="""1. Range sum query immutable (easy)
2. Subarray sum equals k (medium)
3. Contiguous array 0/1 (medium)""",
    cheat="""- prefix[R+1]−prefix[L] = range sum.
- Hash prefixes for count of target sums.
- 2D uses inclusion-exclusion.""",
    further=_std_further("[Prefix sums — CP Algorithms](https://cp-algorithms.com/spaces/prefix_sums.html)"),
)

lesson(
    "02-arrays-strings",
    "05-kadane-maximum-subarray.mdx",
    title="Kadane's Algorithm — Maximum Subarray",
    slug="kadane-maximum-subarray",
    summary="Find the contiguous subarray with maximum sum in linear time.",
    duration=25,
    difficulty="intermediate",
    prerequisites=["prefix-sums"],
    tags=["kadane", "arrays", "dp"],
    order=5,
    why="Maximum subarray is a classic DP that collapses to a few variables — Kadane's algorithm — and appears in stock and signal problems.",
    intuition="At each index decide: extend the previous running sum, or start fresh here if the previous run is poison (negative).",
    core="""### Recurrence

best_ending_here = max(x, best_ending_here_prev + x)
global_best = max(global_best, best_ending_here)

### Variants

- Also return bounds (track start index)
- Circular maximum subarray
- 2D maximum subrectangle via Kadane on temp columns""",
    mermaid="""flowchart TD
    X[x_i] --> D{prev>0?}
    D -->|yes| E[extend]
    D -->|no| S[start new]
    E --> U[update global]
    S --> U""",
    dry_run="""[-2,1,-3,4,-1,2,1,-5,4]: running evolves; best becomes 6 from [4,-1,2,1].""",
    code='''from __future__ import annotations

def max_subarray(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
''',
    complexity="""Time O(n), space O(1). Divide-and-conquer alternative O(n log n).""",
    tricks="""- Initialize with nums[0], not 0 — handles all-negative arrays.
- For indices, reset start when starting fresh.""",
    mistakes="""- Initializing best=0 and returning 0 on all-negative input.
- Mixing empty-subarray-allowed rules without clarifying.""",
    interview="""Call it DP: optimal substructure on ending index. Mention empty-subarray policy.""",
    practice="""1. Maximum subarray (easy/medium)
2. Maximum circular subarray (medium)
3. Best time to buy/sell stock (easy)""",
    cheat="""- cur = max(x, cur+x); best = max(best, cur).
- Careful with all-negative.
- O(n)/O(1).""",
    further=_std_further("[Kadane — Wikipedia](https://en.wikipedia.org/wiki/Maximum_subarray_problem)"),
)

lesson(
    "02-arrays-strings",
    "06-dutch-national-flag.mdx",
    title="Dutch National Flag Partitioning",
    slug="dutch-national-flag",
    summary="Three-way partition for sort colors and pivot partitioning in-place.",
    duration=25,
    difficulty="intermediate",
    prerequisites=["two-pointers"],
    tags=["dutch-flag", "partition", "arrays"],
    order=6,
    why="Sort Colors and quicksort's three-way partition need a linear in-place rearrange into low / mid / high regions.",
    intuition="Three buckets painted as you walk: everything left of lo is red, right of hi is blue, and mid scans the unknown middle.",
    core="""### Invariant

- [0, lo) = 0
- [lo, mid) = 1
- [mid, hi] = unknown
- (hi, n−1] = 2

Advance mid; swap with lo or hi depending on value.""",
    mermaid="""flowchart LR
    A["0s | 1s | unknown | 2s"] --> B[mid scans unknown]""",
    dry_run="""[2,0,2,1,1,0]: swaps pull 0s left and 2s right until mid>hi → [0,0,1,1,2,2].""",
    code='''from __future__ import annotations

def sort_colors(nums: list[int]) -> None:
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
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1
''',
    complexity="""O(n) time, O(1) extra space — one pass.""",
    tricks="""- Do not mid++ when swapping a 2 in — the swapped-in value is unknown.
- Generalizes to pivot three-way partition.""",
    mistakes="""- mid++ after swapping with hi.
- Using a sort library when interview asks for one-pass partition.""",
    interview="""Draw the four regions. Emphasize why mid stays after a 2-swap.""",
    practice="""1. Sort colors (medium)
2. Move zeros (easy)
3. Quicksort three-way sketch (medium)""",
    cheat="""- lo/mid/hi three-way partition.
- mid stays after hi swap.
- O(n)/O(1).""",
    further=_std_further("[Dutch national flag — Dijkstra](https://en.wikipedia.org/wiki/Dutch_national_flag_problem)"),
)

lesson(
    "02-arrays-strings",
    "07-boyer-moore-voting.mdx",
    title="Boyer-Moore Voting Algorithm",
    slug="boyer-moore-voting",
    summary="Find majority elements in linear time and constant space.",
    duration=25,
    difficulty="intermediate",
    prerequisites=["arrays-and-strings-overview"],
    tags=["boyer-moore", "majority", "arrays"],
    order=7,
    why="Majority element (appears more than n/2 times) can be found without hashing by cancellation — a favorite interview follow-up on space.",
    intuition="Pairwise cancel different votes. The majority value survives because it outnumbers all others combined.",
    core="""### Algorithm

Track candidate and count. Same as candidate → count++. Different → count−−. When count hits 0, adopt new candidate. Optional second pass verifies.

### n/3 variant

Maintain up to two candidates with similar cancellation (Misra–Gries).""",
    mermaid="""flowchart TD
    X[x] --> C{count==0?}
    C -->|yes| Set[candidate=x]
    C --> Cmp{x==candidate?}
    Set --> Inc[count=1]
    Cmp -->|yes| Inc2[count++]
    Cmp -->|no| Dec[count--]""",
    dry_run="""[2,2,1,1,1,2,2]: candidate settles on 2 with positive count; verify count>n/2.""",
    code='''from __future__ import annotations

def majority_element(nums: list[int]) -> int:
    cand = None
    count = 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand  # assume majority exists
''',
    complexity="""O(n) time, O(1) space. Verification pass O(n) if majority not guaranteed.""",
    tricks="""- Always verify when problem does not guarantee a majority.
- For n/3, two candidates + final count pass.""",
    mistakes="""- Returning candidate without verification when required.
- Confusing Boyer-Moore voting with Boyer-Moore string search.""",
    interview="""Explain cancellation intuition. Mention verification. Contrast with hash counting O(n) space.""",
    practice="""1. Majority element (easy)
2. Majority element II (medium)
3. Design with stream constraints (medium)""",
    cheat="""- Cancel pairs of different values.
- Candidate + count; optional verify.
- O(n)/O(1).""",
    further=_std_further("[Boyer–Moore majority](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm)"),
)

lesson(
    "02-arrays-strings",
    "08-intervals.mdx",
    title="Interval Problems",
    slug="intervals",
    summary="Merge, insert, and schedule intervals by sorting endpoints.",
    duration=30,
    difficulty="intermediate",
    prerequisites=["arrays-and-strings-overview"],
    tags=["intervals", "sorting", "greedy"],
    order=8,
    why="Calendars, resource booking, and coverage queries reduce to sorting intervals and scanning with a running end bound.",
    intuition="Lay meeting blocks on a timeline. Sort by start. If the next block overlaps the current end, merge; else start a new block.",
    core="""### Toolkit

1. Sort by start (sometimes by end for greedy selection)
2. Merge overlapping
3. Insert new interval into merged list
4. Min meeting rooms = max concurrent → sort starts/ends or sweep line
5. Can attend all = no overlaps after sort""",
    mermaid="""flowchart TD
    S[Sort by start] --> M{overlaps current?}
    M -->|yes| U[Extend end]
    M -->|no| A[Push current; replace]""",
    dry_run="""Merge [[1,3],[2,6],[8,10]] → [[1,6],[8,10]].""",
    code='''from __future__ import annotations

def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    out: list[list[int]] = []
    for s, e in intervals:
        if not out or out[-1][1] < s:
            out.append([s, e])
        else:
            out[-1][1] = max(out[-1][1], e)
    return out
''',
    complexity="""O(n log n) from sort; scan O(n). Space O(n) for output.""",
    tricks="""- Clarify inclusive/exclusive ends.
- Meeting rooms: track active count with sweep of +1/−1 events.""",
    mistakes="""- Forgetting to sort.
- Using less-or-equal incorrectly for touching intervals (problem-dependent).""",
    interview="""Ask whether touching intervals merge. Sort first. For rooms, explain sweep line.""",
    practice="""1. Merge intervals (medium)
2. Insert interval (medium)
3. Meeting rooms II (medium)""",
    cheat="""- Sort by start to merge.
- Sort by end to pick max non-overlap.
- Sweep for concurrency.""",
    further=_std_further("[Sweep line ideas — CP Algorithms](https://cp-algorithms.com/)"),
)

# ========================= Modules 03–17 via rich specs =========================


def Q(
    module: str,
    num: int,
    slug: str,
    title: str,
    summary: str,
    *,
    difficulty: str = "intermediate",
    duration: int = 30,
    prereq: list[str] | None = None,
    tags: list[str] | None = None,
    why: str,
    intuition: str,
    bullets: list[str],
    mermaid: str,
    dry: str,
    code: str,
    complexity: str,
    tricks: list[str],
    mistakes: list[str],
    interview: str,
    practice: list[str],
    cheat: list[str],
    links: list[str],
    order: int | None = None,
) -> None:
    core = "\n".join(f"- {b}" for b in bullets)
    lesson(
        module,
        f"{num:02d}-{slug}.mdx",
        title=title,
        slug=slug,
        summary=summary,
        duration=duration,
        difficulty=difficulty,
        prerequisites=prereq or [],
        tags=tags or [slug.split("-")[0]],
        order=order if order is not None else num,
        why=why,
        intuition=intuition,
        core=core,
        mermaid=mermaid,
        dry_run=dry,
        code=code,
        complexity=complexity,
        tricks="\n".join(f"- {t}" for t in tricks),
        mistakes="\n".join(f"- {m}" for m in mistakes),
        interview=interview,
        practice="\n".join(f"{i}. {p}" for i, p in enumerate(practice, 1)),
        cheat="\n".join(f"- {c}" for c in cheat),
        further="\n".join(f"- {u}" for u in links),
    )


# ----- 03 Hashing -----
Q(
    "03-hashing", 1, "hash-maps-and-sets", "Hash Maps and Hash Sets",
    "Average O(1) lookups, frequency maps, and set algebra for interview problems.",
    difficulty="beginner",
    prereq=["how-to-approach-problems"],
    tags=["hashing", "hashmap", "hashset"],
    why="Hash tables turn many O(n²) searches into expected O(n). Two Sum, anagrams, and duplicates all start here.",
    intuition="A coat-check: hash the coat to a hook number; average grab is instant, though a crowded hook needs a short walk.",
    bullets=[
        "Map: key → value; Set: key membership only",
        "Python dict/set are hash tables with open addressing",
        "Patterns: frequency count, complement search, seen-before, grouping by signature",
        "Keys must be hashable (immutable) in Python",
    ],
    mermaid="""flowchart LR
    K[Key] --> H[Hash]
    H --> B[Bucket]
    B --> V[Value / membership]""",
    dry="Two Sum [2,7,11,15] target 9: see 2 store idx 0; at 7 find 2 in map → [0,1].",
    code='''from __future__ import annotations
from collections import Counter

def is_anagram(a: str, b: str) -> bool:
    return Counter(a) == Counter(b)
''',
    complexity="Average O(1) per op; worst O(n) on collisions. Space O(n) for stored keys.",
    tricks=["Use Counter for frequencies", "Store index not just bool when positions matter", "frozenset for set-of-sets keys"],
    mistakes=["Assuming worst-case O(1)", "Using mutable list as dict key", "Forgetting complement already consumed"],
    interview="State expected O(1) and mention pathological worst case briefly.",
    practice=["Two Sum (easy)", "Valid Anagram (easy)", "Group Anagrams (medium)"],
    cheat=["Hash for lookups/counts", "Complement pattern", "Expected O(1), space O(n)"],
    links=["[Python dict](https://docs.python.org/3/library/stdtypes.html#dict)"],
)
Q(
    "03-hashing", 2, "collisions-and-hash-design", "Collisions and Hash Design",
    "Chaining vs open addressing, load factor, and designing hash keys for problems.",
    prereq=["hash-maps-and-sets"],
    tags=["hashing", "collisions"],
    why="Understanding collisions explains performance cliffs and helps you design signatures for grouping problems.",
    intuition="Many coats mapping to one hook: either hang a chain of coats (chaining) or probe nearby hooks (open addressing).",
    bullets=[
        "Load factor α = n / buckets; resize when α high",
        "Chaining: linked lists/trees per bucket",
        "Open addressing: linear/quadratic probing, Robin Hood",
        "Problem hashes: sorted string, tuple of counts, (row,col) keys",
    ],
    mermaid="""flowchart TD
    C[Collision] --> Ch[Chaining]
    C --> OA[Open addressing]""",
    dry="Group anagrams: hash key = tuple(sorted(s)) or 26-count tuple; bucket words together.",
    code='''from __future__ import annotations
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    buckets: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - 97] += 1
        buckets[tuple(counts)].append(s)
    return list(buckets.values())
''',
    complexity="Expected O(n·L) for n strings length L with count signature.",
    tricks=["Prefer count tuple over sorting when alphabet small", "Custom __hash__/__eq__ rarely needed in interviews"],
    mistakes=["Using str(Counter) as key — unstable", "Ignoring unicode/case constraints"],
    interview="Explain load factor and why average stays O(1) with resizing.",
    practice=["Group Anagrams (medium)", "Design HashMap (medium)", "Longest consecutive sequence (medium)"],
    cheat=["Collisions inevitable; resize keeps α low", "Signature keys group equivalents", "Know chaining vs probing"],
    links=["[Hash table — Wikipedia](https://en.wikipedia.org/wiki/Hash_table)"],
)
Q(
    "03-hashing", 3, "lru-cache", "LRU Cache",
    "Ordered dict / HashMap + doubly linked list for O(1) get and put with eviction.",
    prereq=["hash-maps-and-sets"],
    tags=["lru", "design", "hashing"],
    why="LRU Cache is the canonical system-design-lite coding problem: combine hashing with a linked list for recency.",
    intuition="A backpack that kicks out the item you touched least recently when full. Dict finds items; a queue-like list tracks order.",
    bullets=[
        "HashMap key → node; DLL maintains recency (head=MRU, tail=LRU)",
        "get: move node to head; put: insert/update head, evict tail if over capacity",
        "Python: collections.OrderedDict or functools.lru_cache for comparison",
    ],
    mermaid="""flowchart LR
    H[MRU] --> N1 --> N2 --> T[LRU]
    M[HashMap] --> N1
    M --> N2""",
    dry="capacity 2: put 1, put 2, get 1, put 3 → evicts 2; cache holds 1 and 3.",
    code='''from __future__ import annotations
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.od: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)
''',
    complexity="get/put O(1) average with hashmap + DLL (or OrderedDict).",
    tricks=["Dummy head/tail nodes simplify edge links", "Interviewers may forbid OrderedDict — implement DLL"],
    mistakes=["Forgetting to update recency on get", "Evicting MRU instead of LRU"],
    interview="Draw map + list. Narrate get and put including eviction.",
    practice=["LRU Cache (medium)", "Design browser history (medium)"],
    cheat=["Map + DLL (or OrderedDict)", "Touch → move to front", "Evict tail when over capacity"],
    links=["[LRU — Wikipedia](https://en.wikipedia.org/wiki/Cache_replacement_policies)"],
)
Q(
    "03-hashing", 4, "lfu-cache", "LFU Cache",
    "Least frequently used eviction with frequency lists for O(1) operations.",
    prereq=["lru-cache"],
    tags=["lfu", "design", "hashing"],
    why="LFU adds frequency to eviction policy. It tests multi-index design: key→node, freq→DLL of keys, track min frequency.",
    intuition="Prefer kicking out what you barely use — but ties break toward least recent within that frequency bucket.",
    bullets=[
        "Structures: key→(val,freq), freq→OrderedDict of keys, min_freq",
        "On get/put: bump freq, move key to new bucket, update min_freq",
        "Evict from min_freq bucket's least-recent key",
    ],
    mermaid="""flowchart TD
    K[key] --> F[freq map]
    F --> B[freq buckets DLL]""",
    dry="capacity 2: put 1, put 2, get 1 (freq1=2), put 3 → evict 2 (freq 1).",
    code='''from __future__ import annotations
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.val: dict[int, int] = {}
        self.freq: dict[int, int] = {}
        self.buckets: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.minf = 0

    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if f == self.minf and not self.buckets[f]:
            self.minf += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.val:
            self.val[key] = value
            self._touch(key)
            return
        if len(self.val) >= self.cap:
            old, _ = self.buckets[self.minf].popitem(last=False)
            del self.val[old]
            del self.freq[old]
        self.val[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.minf = 1
''',
    complexity="O(1) per get/put with hash maps + ordered freq buckets.",
    tricks=["Track min_freq to find eviction victim fast", "capacity 0 is a real edge case"],
    mistakes=["Not advancing min_freq when a bucket empties", "Evicting from wrong frequency"],
    interview="Contrast LRU vs LFU policy. Diagram the three maps.",
    practice=["LFU Cache (hard)", "Compare LRU vs LFU verbally (medium)"],
    cheat=["Multi-index: key, freq, buckets", "Bump freq on access", "Evict min_freq LRU"],
    links=["[LFU — Wikipedia](https://en.wikipedia.org/wiki/Least_frequently_used)"],
)

# ----- 04 Linked lists -----
Q(
    "04-linked-lists", 1, "singly-linked-lists", "Singly Linked Lists",
    "Nodes, traversal, insertion/deletion, and dummy-head technique.",
    difficulty="beginner",
    prereq=["arrays-and-strings-overview"],
    tags=["linked-list", "pointers"],
    why="Linked lists train pointer manipulation used in graphs, skip lists, and interview classics like reverse and merge.",
    intuition="A scavenger hunt: each clue points to the next. Cheap insert at known node; expensive random access.",
    bullets=[
        "Node: value + next",
        "Dummy head simplifies insert/delete at front",
        "Always save next before rewiring",
        "Prefer iterative patterns in interviews unless recursion is cleaner",
    ],
    mermaid="""flowchart LR
    D[dummy] --> A --> B --> C --> N[None]""",
    dry="Delete value 2 from 1→2→3: prev=1, skip node 2 → 1→3.",
    code='''from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class ListNode:
    val: int = 0
    next: Optional["ListNode"] = None

def list_length(head: Optional[ListNode]) -> int:
    n = 0
    while head:
        n += 1
        head = head.next
    return n
''',
    complexity="Access k-th O(n); insert/delete at known node O(1); space O(1) extra typical.",
    tricks=["Dummy head", "Draw before/after pointers", "Return dummy.next"],
    mistakes=["Losing reference to next", "Off-by-one on 1-indexed problems", "Forgetting empty list"],
    interview="Draw nodes. Narrate each pointer assignment. Use dummy when head may change.",
    practice=["Design linked list (medium)", "Delete node (easy)", "Remove nth from end (medium)"],
    cheat=["Pointer rewiring with saved next", "Dummy head", "O(n) scan O(1) splice"],
    links=["[Linked list — Wikipedia](https://en.wikipedia.org/wiki/Linked_list)"],
)
Q(
    "04-linked-lists", 2, "doubly-and-circular", "Doubly and Circular Lists",
    "prev links, circular structures, and when they help (LRU, round-robin).",
    prereq=["singly-linked-lists"],
    tags=["doubly-linked-list", "circular"],
    why="DLL enables O(1) removal given a node — the backbone of LRU. Circular lists model round-robin schedulers.",
    intuition="Scavenger hunt with arrows both ways, or a loop of clues with no end.",
    bullets=[
        "DLL node: prev + next; update four links carefully on splice",
        "Circular: last.next = first; watch infinite loops — track start node",
        "Sentinel nodes common in production list implementations",
    ],
    mermaid="""flowchart LR
    A <--> B <--> C
    C --> A""",
    dry="Remove B from A↔B↔C: A.next=C, C.prev=A.",
    code='''from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class DNode:
    val: int = 0
    prev: Optional["DNode"] = None
    next: Optional["DNode"] = None

def splice_out(node: DNode) -> None:
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev
''',
    complexity="Splice O(1) given node; search still O(n).",
    tricks=["Sentinels remove null checks", "In circular traversal break when back at start"],
    mistakes=["Not updating both prev and next", "Infinite loop on circular print"],
    interview="Relate DLL to LRU design. Mention circular for Josephus.",
    practice=["LRU with explicit DLL (medium)", "Josephus circular (medium)"],
    cheat=["DLL: O(1) unlink", "Circular: remember start", "Sentinels help"],
    links=["[Doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list)"],
)
Q(
    "04-linked-lists", 3, "fast-and-slow-pointers", "Fast and Slow Pointers",
    "Midpoint, cycle detection, and palindrome checks with tortoise and hare.",
    prereq=["singly-linked-lists"],
    tags=["fast-slow", "linked-list"],
    why="Floyd's cycle detection and midpoint finding need only O(1) space — interview favorites.",
    intuition="Two runners on a track: if there's a loop, the fast one laps the slow. For midpoint, when fast finishes, slow is halfway.",
    bullets=[
        "Mid: fast moves 2, slow moves 1; handle even/odd carefully",
        "Cycle detect: meet ⇒ cycle; null ⇒ no cycle",
        "Cycle start: after meet, reset one to head; advance both by 1",
        "Palindrome: reverse second half from mid, compare",
    ],
    mermaid="""flowchart TD
    S[slow] --> M[mid / meet]
    F[fast x2] --> M""",
    dry="1→2→3→4→5: fast at 5, slow at 3 (mid). Cycle 3→2: eventually meet inside loop.",
    code='''from __future__ import annotations
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # type: ignore
        fast = fast.next.next
        if slow is fast:
            return True
    return False
''',
    complexity="O(n) time O(1) space for detect/mid.",
    tricks=["Draw even-length mid convention", "Prove cycle entry with equal steps after reset"],
    mistakes=["Not checking fast.next before fast.next.next", "Losing mid's previous for split"],
    interview="Name Floyd. Explain why meeting implies a cycle; optional math for entry point.",
    practice=["Linked list cycle (easy)", "Middle of list (easy)", "Palindrome list (easy/medium)"],
    cheat=["fast×2 slow×1", "Meet ⇒ cycle", "Reset for entry"],
    links=["[Floyd cycle detection](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)"],
)
Q(
    "04-linked-lists", 4, "reverse-linked-list", "Reverse a Linked List",
    "Iterative and recursive reversal; reverse sublists between bounds.",
    prereq=["singly-linked-lists"],
    tags=["reverse", "linked-list"],
    why="Reversal is the atomic surgery behind palindrome checks, k-group reverse, and many pointer drills.",
    intuition="Flip arrows one by one: remember previous, point current back, slide forward.",
    bullets=[
        "Iterative: prev=None, cur=head; while cur: nxt=cur.next; cur.next=prev; prev=cur; cur=nxt",
        "Recursive: reverse rest, then head.next.next=head; head.next=None",
        "Sublist reverse: find bounds, reverse segment, reconnect",
    ],
    mermaid="""flowchart LR
    A --> B --> C
    A2[A] <-- B2[B] <-- C2[C]""",
    dry="1→2→3: steps yield 1←2←3 with prev=3 as new head.",
    code='''from __future__ import annotations
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
''',
    complexity="O(n) time O(1) iterative; recursive O(n) stack.",
    tricks=["Prefer iterative in interviews for O(1) space", "Save nxt before rewiring"],
    mistakes=["Returning head instead of prev", "Breaking the list by losing nxt"],
    interview="Code iterative first; mention recursive trade-off.",
    practice=["Reverse list (easy)", "Reverse between L and R (medium)", "Reverse k-group (hard)"],
    cheat=["prev/cur/nxt waltz", "Return prev", "Reconnect for partial reverse"],
    links=["[Reverse linked list patterns](https://neetcode.io/)"],
)
Q(
    "04-linked-lists", 5, "merge-lists", "Merge Linked Lists",
    "Merge two sorted lists and merge k lists with heap or divide-and-conquer.",
    prereq=["singly-linked-lists"],
    tags=["merge", "linked-list", "heap"],
    why="Merging sorted lists mirrors merge-sort's combine step and scales to k-way merge — a top interview problem.",
    intuition="Two sorted lines at a ticket counter: always take the smaller front, attach to the result tail.",
    bullets=[
        "Two-list merge with dummy tail pointer",
        "k lists: min-heap of heads O(N log k), or pairwise D&C merge",
        "In-place merge by rewiring next pointers — no new nodes required",
    ],
    mermaid="""flowchart TD
    A[list A] --> T[tail pick min]
    B[list B] --> T
    T --> R[result]""",
    dry="1→4→5 and 1→2→3 → 1→1→2→3→4→5.",
    code='''from __future__ import annotations
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

def merge_two(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode()
    t = dummy
    while a and b:
        if a.val <= b.val:
            t.next, a = a, a.next
        else:
            t.next, b = b, b.next
        t = t.next
    t.next = a or b
    return dummy.next
''',
    complexity="Two lists O(n+m). k lists heap O(N log k).",
    tricks=["Dummy + tail", "Heap stores (val, tie, node) because nodes are incomparable"],
    mistakes=["Mutating without dummy", "Comparing ListNode in heap without tie-breaker"],
    interview="Start with two-list. Escalate to heap k-way and complexity.",
    practice=["Merge two sorted lists (easy)", "Merge k sorted lists (hard)"],
    cheat=["Dummy tail merge", "Heap for k-way", "O(N log k)"],
    links=["[Merge k lists](https://leetcode.com/problems/merge-k-sorted-lists/)"],
)
Q(
    "04-linked-lists", 6, "linked-list-cycles-and-intersection", "Cycles and Intersection",
    "Detect cycles, find cycle entrance, and intersecting list nodes.",
    prereq=["fast-and-slow-pointers"],
    tags=["cycle", "intersection", "linked-list"],
    why="Cycle entrance and intersection problems test pointer math and careful edge handling without extra memory.",
    intuition="Two paths that share a tunnel: equalize lengths or use Floyd meeting + reset to find the junction.",
    bullets=[
        "Entrance: Floyd meet, then head and meet advance → entrance",
        "Intersection: length diff align, or A+B path equalization trick",
        "Hashing nodes works but uses O(n) space — mention as baseline",
    ],
    mermaid="""flowchart LR
    H[head] --> M[meet]
    M --> E[entrance]
    H2[head reset] --> E""",
    dry="Intersection at node 8: align lengths or dual traversal A then B.",
    code='''from __future__ import annotations
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

def get_intersection(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    p, q = a, b
    while p is not q:
        p = p.next if p else b
        q = q.next if q else a
    return p
''',
    complexity="O(n) time O(1) space for Floyd and dual-pointer intersection.",
    tricks=["Equalize paths A+B", "After meet, same steps to entrance as head"],
    mistakes=["Comparing values instead of node identity", "Infinite loop if both null handling wrong"],
    interview="Prefer O(1) space solutions; mention hash as backup.",
    practice=["Linked list cycle II (medium)", "Intersection of two lists (easy)"],
    cheat=["Floyd + reset", "Path equalization", "Compare nodes not values"],
    links=["[Floyd](https://en.wikipedia.org/wiki/Cycle_detection)"],
)

# Continue importing remaining modules from companion file executed below
from generate_dsa_lessons_rest import register as register_rest  # type: ignore

register_rest(Q)

# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------


def main() -> None:
    written = 0
    skipped = 0
    for module, filename, meta, body in CATALOG:
        if (module, filename) in SKIP:
            skipped += 1
            continue
        out_dir = DSA / module
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / filename
        if module == "01-foundations" and filename == "01-big-o-and-complexity.mdx":
            skipped += 1
            continue
        path.write_text(build_mdx(meta, body), encoding="utf-8")
        written += 1
    # Ensure existing big-O remains untouched
    big_o = DSA / "01-foundations" / "01-big-o-and-complexity.mdx"
    print(f"Wrote {written} lessons; skipped {skipped}; big-O exists={big_o.is_file()}")
    print(f"Total catalog entries: {len(CATALOG)}")


if __name__ == "__main__":
    main()
