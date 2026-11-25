#!/usr/bin/env python3
"""Generate substantial MDX lessons from a structured curriculum outline.

Skips files that already exist unless --force. Stdlib only.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

# course -> module -> list of (order, slug, title, summary, difficulty, tags, focus_bullets)
CURRICULUM: dict[str, dict[str, list[tuple]]] = {
    "python": {
        "02-syntax-and-types": [
            (2, "python-io-and-fstrings", "I/O and f-strings", "Reading input, writing output, and formatting strings idiomatically.", "beginner", ["python", "io", "strings"], ["input/print", "f-strings", "format specs", "encoding basics"]),
            (3, "python-operators-expressions", "Expressions and Operator Precedence", "How Python evaluates expressions and the pitfalls of chained comparisons.", "beginner", ["python", "operators"], ["precedence", "chained comparisons", "short-circuit", "walrus operator"]),
        ],
        "03-control-flow": [
            (1, "python-conditionals", "Conditionals and Branching", "if/elif/else, truthiness, and structuring clear decision logic.", "beginner", ["python", "control-flow"], ["if/elif/else", "ternary", "match/case intro", "guard clauses"]),
            (2, "python-loops", "Loops: for, while, and Control", "Iteration patterns, else on loops, break/continue, and when not to loop.", "beginner", ["python", "loops"], ["for/while", "enumerate/zip", "break/continue", "else on loops"]),
            (3, "python-comprehensions", "Comprehensions", "List/set/dict comprehensions and generator expressions for expressive data transforms.", "beginner", ["python", "comprehensions"], ["list/set/dict comps", "filtering", "nested comps", "genexps"]),
        ],
        "04-functions": [
            (2, "python-closures-decorators", "Closures and Decorators", "Capture enclosing state and wrap callables with reusable cross-cutting behavior.", "intermediate", ["python", "decorators"], ["closures", "decorator factories", "functools.wraps", "timing/auth examples"]),
            (3, "python-generators-recursion", "Generators, Lambda, and Recursion", "Lazy sequences, anonymous functions, and recursive thinking with base cases.", "intermediate", ["python", "generators", "recursion"], ["yield", "lambda limits", "recursion depth", "tail patterns"]),
        ],
        "05-data-structures": [
            (1, "python-lists-tuples", "Lists and Tuples in Depth", "Sequence operations, slicing, and when immutability buys safety.", "beginner", ["python", "list", "tuple"], ["slicing", "methods", "sorting", "tuple packing"]),
            (2, "python-sets-dicts", "Sets and Dictionaries", "Hash-based collections for membership, counting, and keyed access.", "beginner", ["python", "set", "dict"], ["hashing intuition", "dict views", "set algebra", "insertion order"]),
            (3, "python-collections-heapq", "collections and heapq", "Counter, defaultdict, deque, OrderedDict patterns, and heap queues.", "intermediate", ["python", "collections", "heapq"], ["Counter", "defaultdict", "deque", "heapq"]),
            (4, "python-mutability-memory", "Mutability and the Memory Model", "Object identity, copying, and how references explain surprising bugs.", "intermediate", ["python", "memory"], ["id/is", "shallow vs deep copy", "interning", "refcount GC intro"]),
        ],
        "06-strings-files": [
            (1, "python-strings-regex", "Strings and Regular Expressions", "Text processing with str methods and the re module.", "intermediate", ["python", "regex"], ["str methods", "re patterns", "groups", "flags"]),
            (2, "python-file-io-pathlib", "File I/O, JSON/CSV, and pathlib", "Reliable file handling with context managers and modern paths.", "beginner", ["python", "files", "json"], ["open modes", "pathlib", "json/csv", "encoding"]),
        ],
        "07-errors-logging": [
            (1, "python-exceptions-context-managers", "Exceptions and Context Managers", "Raise, catch, and design clean resource lifetimes with with.", "intermediate", ["python", "exceptions"], ["try/except/else/finally", "custom exceptions", "contextlib", "with"]),
            (2, "python-logging", "Logging like a Professional", "Replace print debugging with structured, leveled logging.", "intermediate", ["python", "logging"], ["levels", "handlers", "formatters", "best practices"]),
        ],
        "08-oop": [
            (1, "python-classes-objects", "Classes and Objects", "Define types, construct instances, and separate state from behavior.", "intermediate", ["python", "oop"], ["class/instance", "__init__", "self", "attrs"]),
            (2, "python-methods-inheritance-mro", "Methods, Inheritance, and MRO", "Instance/class/static methods, inheritance trees, and C3 MRO.", "intermediate", ["python", "inheritance"], ["classmethod", "staticmethod", "super", "MRO"]),
            (3, "python-encapsulation-abc-dunders", "Encapsulation, ABCs, and Dunders", "Privacy conventions, abstract base classes, and the data model hooks.", "intermediate", ["python", "abc", "dunder"], ["_ vs __", "ABC", "dunders", "protocols"]),
            (4, "python-dataclasses-composition-solid", "Dataclasses, Composition, and SOLID", "Model data cleanly and apply SOLID with Pythonic composition.", "advanced", ["python", "solid", "dataclasses"], ["dataclass", "composition", "SOLID", "trade-offs"]),
            (5, "python-design-patterns", "Design Patterns in Python", "Singleton, Factory, Observer, Strategy, Decorator — idiomatic forms.", "advanced", ["python", "patterns"], ["strategy", "factory", "observer", "decorator pattern"]),
        ],
        "09-modules-packages": [
            (1, "python-modules-packages-imports", "Modules, Packages, and Imports", "Structure projects, control imports, and avoid circular dependency pain.", "intermediate", ["python", "modules"], ["import system", "packages", "__init__", "relative imports"]),
        ],
        "10-itertools-functools": [
            (1, "python-itertools-functools", "itertools and functools", "Composable iteration tools and higher-order function utilities.", "intermediate", ["python", "itertools", "functools"], ["islice/chain", "groupby", "lru_cache", "partial"]),
        ],
        "11-typing": [
            (1, "python-type-hints-mypy-pydantic", "Type Hints, mypy, and Pydantic", "Gradual typing for readability and runtime validation at boundaries.", "intermediate", ["python", "typing", "pydantic"], ["annotations", "mypy", "Optional/Union", "Pydantic models"]),
        ],
        "12-concurrency": [
            (1, "python-threading-multiprocessing-gil", "Threading, Multiprocessing, and the GIL", "Choose concurrency models with eyes open about the GIL.", "advanced", ["python", "concurrency", "gil"], ["threads", "processes", "GIL", "queues"]),
            (2, "python-asyncio", "asyncio and async/await", "Cooperative concurrency for I/O-bound workloads.", "advanced", ["python", "asyncio"], ["event loop", "await", "tasks", "async with"]),
        ],
        "13-testing": [
            (1, "python-unittest-pytest-tdd", "unittest, pytest, Mocking, and TDD", "Build confidence with automated tests and a red-green-refactor loop.", "intermediate", ["python", "pytest", "tdd"], ["pytest", "fixtures", "mocking", "TDD"]),
        ],
        "14-performance": [
            (1, "python-profiling-performance", "Profiling and Performance Awareness", "Measure before optimizing; know Big-O costs of common Python ops.", "intermediate", ["python", "performance"], ["cProfile", "timeit", "complexity", "numpy awareness"]),
        ],
        "15-web-apis": [
            (1, "python-requests-fastapi-rest", "requests, FastAPI Basics, and REST", "Consume and build HTTP APIs with clear resource design.", "intermediate", ["python", "fastapi", "rest"], ["requests", "REST verbs", "FastAPI routes", "status codes"]),
        ],
        "16-databases": [
            (1, "python-sql-sqlite-sqlalchemy", "SQL, SQLite, and SQLAlchemy", "Persist data with SQL fundamentals and an ORM path.", "intermediate", ["python", "sql", "sqlalchemy"], ["SQL CRUD", "SQLite", "ORM vs SQL", "migrations intro"]),
        ],
        "17-packaging-quality": [
            (1, "python-packaging-git-quality", "Packaging, Git, and Code Quality", "Ship installable packages with clean VCS and linting habits.", "intermediate", ["python", "packaging", "git"], ["pyproject.toml", "git basics", "ruff/black", "idioms"]),
        ],
    },
    "dsa": {
        "02-arrays-strings": [
            (1, "dsa-arrays-strings-basics", "Arrays and Strings Foundations", "Contiguous memory mental model, Python list costs, and string immutability.", "intermediate", ["arrays", "strings"], ["indexing", "amortized append", "immutability", "patterns overview"]),
            (2, "dsa-two-pointers-sliding-window", "Two Pointers and Sliding Window", "Shrink/grow ranges to turn O(n^2) scans into O(n) passes.", "intermediate", ["two-pointers", "sliding-window"], ["opposite pointers", "fast-slow", "fixed/variable window", "templates"]),
            (3, "dsa-prefix-sums-kadane", "Prefix Sums and Kadane", "Precompute ranges and find maximum subarrays with linear DP.", "intermediate", ["prefix-sums", "kadane"], ["prefix arrays", "range sums", "Kadane", "variants"]),
            (4, "dsa-dutch-flag-boyer-moore-intervals", "Dutch Flag, Boyer-Moore, and Intervals", "Partition arrays, majority votes, and merge/schedule intervals.", "intermediate", ["arrays", "intervals"], ["3-way partition", "majority vote", "merge intervals", "sweep line intro"]),
        ],
        "03-hashing": [
            (1, "dsa-hash-maps-sets", "Hash Maps and Sets", "Average O(1) membership and counting with collision awareness.", "intermediate", ["hashing"], ["hash functions", "collisions", "dict/set", "design problems"]),
            (2, "dsa-lru-lfu-cache", "LRU and LFU Cache Design", "Combine hashing with linked structures for eviction policies.", "advanced", ["lru", "lfu", "design"], ["OrderedDict", "DLL+map", "LFU frequency lists", "complexity"]),
        ],
        "04-linked-lists": [
            (1, "dsa-linked-lists", "Linked Lists Mastery", "Singly/doubly/circular lists, reversal, merge, and cycle detection.", "intermediate", ["linked-lists"], ["node structure", "fast-slow", "reverse", "merge"]),
        ],
        "05-stacks-queues": [
            (1, "dsa-stacks-queues-monotonic", "Stacks, Queues, and Monotonic Structures", "LIFO/FIFO patterns plus monotonic stack/queue templates.", "intermediate", ["stacks", "queues"], ["expression eval", "monotonic stack", "deque", "next greater"]),
        ],
        "06-recursion-backtracking": [
            (1, "dsa-recursion-backtracking", "Recursion and Backtracking", "Explore decision trees for subsets, permutations, N-Queens, and Sudoku.", "intermediate", ["backtracking", "recursion"], ["state/choice/undo", "subsets", "perms", "constraint pruning"]),
        ],
        "07-searching-sorting": [
            (1, "dsa-binary-search-variants", "Binary Search and Variants", "Search on indices and on answer space with correct boundary handling.", "intermediate", ["binary-search"], ["lo/hi invariants", "lower/upper bound", "search on answer", "templates"]),
            (2, "dsa-sorting-algorithms", "Sorting Algorithms Deep Dive", "From quadratic sorts to n log n classics, stability, and Timsort.", "intermediate", ["sorting"], ["merge/quick/heap", "counting/radix", "stability", "Timsort"]),
        ],
        "08-trees": [
            (1, "dsa-binary-trees-bst", "Binary Trees and BSTs", "Traversals, BST invariants, LCA, diameter, and serialization.", "intermediate", ["trees", "bst"], ["DFS/BFS", "Morris", "LCA", "serialize"]),
            (2, "dsa-balanced-trees-fenwick-trie", "Balanced Trees, Fenwick, Segment Tree, Trie", "Self-balancing concepts and advanced tree structures for ranges and prefixes.", "advanced", ["avl", "segment-tree", "trie"], ["AVL/RB concepts", "Fenwick", "segment tree", "Trie"]),
        ],
        "09-heaps": [
            (1, "dsa-heaps-priority-queues", "Heaps and Priority Queues", "Top-K, merge K lists, running median, and scheduling.", "intermediate", ["heaps"], ["binary heap", "top-K", "median stream", "heapq"]),
        ],
        "10-graphs": [
            (1, "dsa-graphs-bfs-dfs", "Graph Representations, BFS, and DFS", "Build graphs and traverse for connectivity, bipartite checks, and components.", "intermediate", ["graphs", "bfs", "dfs"], ["adj list", "BFS/DFS", "components", "bipartite"]),
            (2, "dsa-graphs-topo-shortest-mst", "Topo Sort, Shortest Paths, MST, and DSU", "Ordering, distances, spanning trees, and Union-Find.", "advanced", ["graphs", "dijkstra", "mst", "dsu"], ["Kahn/DFS topo", "Dijkstra/BF/FW", "Prim/Kruskal", "DSU"]),
            (3, "dsa-graphs-advanced-bridges-scc", "Bridges, Articulation Points, and SCC", "Tarjan-style insights for critical edges/nodes and strongly connected components.", "advanced", ["graphs", "tarjan"], ["discovery times", "bridges", "articulation", "SCC"]),
        ],
        "11-dynamic-programming": [
            (1, "dsa-dp-framework", "Dynamic Programming Framework", "Derive states, transitions, and bases — memoization vs tabulation.", "advanced", ["dynamic-programming"], ["state design", "memo/tab", "space opt", "checklist"]),
            (2, "dsa-dp-classic-families", "Classic DP Families", "Knapsack, LIS/LCS, edit distance, coin change, grids, and partitions.", "advanced", ["dynamic-programming"], ["knapsack", "LCS/LIS", "edit distance", "grid DP"]),
            (3, "dsa-dp-advanced", "Advanced DP", "Trees, bitmasks, digits, and state-machine DP.", "advanced", ["dynamic-programming"], ["tree DP", "bitmask", "digit DP", "state machine"]),
        ],
        "12-greedy": [
            (1, "dsa-greedy-algorithms", "Greedy Algorithms and Proofs", "Exchange arguments, interval scheduling, and Huffman coding intuition.", "intermediate", ["greedy"], ["proof ideas", "intervals", "scheduling", "Huffman"]),
        ],
        "13-bit-manipulation": [
            (1, "dsa-bit-manipulation", "Bit Manipulation Tricks", "Masks, flips, and interview bit idioms.", "intermediate", ["bit-manipulation"], ["masks", "xor tricks", "lowest set bit", "bit DP intro"]),
        ],
        "14-math-number-theory": [
            (1, "dsa-math-number-theory", "Math and Number Theory for Interviews", "GCD, sieve, modular arithmetic, fast exponentiation, combinatorics.", "intermediate", ["math", "number-theory"], ["Euclid", "sieve", "modpow", "nCr"]),
        ],
        "15-string-algorithms": [
            (1, "dsa-string-algorithms", "String Algorithms", "KMP, Rabin-Karp, Z-algorithm, Manacher, and suffix arrays intro.", "advanced", ["strings", "kmp"], ["prefix function", "rolling hash", "Z-array", "Manacher"]),
        ],
        "16-advanced": [
            (1, "dsa-advanced-techniques", "Advanced Techniques", "Divide and conquer opts, sqrt decomposition, meet in the middle, randomized algorithms.", "advanced", ["divide-conquer", "randomized"], ["D&C opt", "sqrt decomp", "meet in middle", "randomized"]),
        ],
        "17-patterns-interview": [
            (1, "dsa-patterns-cheat-sheet", "Problem-Solving Patterns Cheat Sheet", "The ~20 patterns and how to recognize which one fits.", "intermediate", ["patterns", "interview"], ["pattern catalog", "identification", "templates", "examples"]),
            (2, "dsa-mock-interview-strategy", "Mock Interview Strategy and Revision", "Communication, timeboxing, and a sustainable revision plan.", "intermediate", ["interview", "career"], ["communication", "time management", "revision", "scorecard"]),
        ],
    },
}


def render_lesson(
    course: str,
    module: str,
    order: int,
    slug: str,
    title: str,
    summary: str,
    difficulty: str,
    tags: list[str],
    focus: list[str],
) -> str:
    focus_md = "\n".join(f"- **{item}**" for item in focus)
    tags_yaml = json_dumps(tags)
    mermaid = dedent(
        f"""\
        ```mermaid
        flowchart TD
            A[Motivation] --> B[Build intuition]
            B --> C[Formalize core ideas]
            C --> D[Dry-run + code]
            D --> E[Analyze complexity]
            E --> F[Practice + interview notes]
        ```"""
    )
    code = dedent(
        f"""\
        ```python
        def demo_{slug.replace('-', '_')}() -> None:
            \"\"\"Runnable sketch for: {title}\"\"\"
            topics = {tags!r}
            print("Course:", {course!r})
            print("Lesson:", {title!r})
            for i, t in enumerate(topics, 1):
                print(f"{{i}}. {{t}}")


        if __name__ == "__main__":
            demo_{slug.replace('-', '_')}()
        ```"""
    )
    return dedent(
        f"""\
        ---
        title: "{title}"
        slug: "{slug}"
        summary: "{summary}"
        duration: 30
        difficulty: "{difficulty}"
        prerequisites: []
        tags: {tags_yaml}
        order: {order}
        ---

        ## Why this matters

        {summary} In real systems and interviews, weak fundamentals here cascade into slower debugging, fragile designs, and missed edge cases. This lesson builds a durable mental model you will reuse across later modules in the **{course}** path.

        Engineers who internalize these ideas communicate trade-offs clearly, spot bugs earlier, and choose simpler solutions under time pressure. Treat this as a craft skill, not trivia.

        ## Intuition

        Before symbols and APIs, picture the problem in the physical world: inputs arrive, state changes, and outputs must remain consistent. The ideas in this lesson — {", ".join(focus)} — are different lenses on that same story.

        If you can explain the idea to a teammate with zero jargon, you are ready for the formal section. If you cannot, keep refining the analogy until it clicks.

        ## Core concept in depth

        This lesson focuses on:

        {focus_md}

        Work through each idea with an invariant in mind: what must remain true before and after every step? Write that invariant down. Algorithms and APIs become easier once the invariant is explicit.

        Definitions matter. Name the objects, the operations allowed on them, and the complexity you expect. Then connect the definition to a small example you can execute by hand.

        ### Step-by-step method

        1. Restate the goal and constraints in your own words.
        2. Identify inputs/outputs and failing edge cases.
        3. Choose a representation that makes the invariant obvious.
        4. Implement the smallest correct version.
        5. Only then optimize with measurements or clear asymptotic wins.

        ## Diagram / flowchart

        {mermaid}

        ### Dry-run table

        | Step | Action | State / notes |
        | --- | --- | --- |
        | 1 | Clarify goal | Success criteria written |
        | 2 | Pick representation | Data structure chosen |
        | 3 | Apply core operation | Invariant checked |
        | 4 | Handle edge case | Empty / single-element covered |
        | 5 | Confirm complexity | Time and space stated |

        ## Code

        {code}

        ## Complexity analysis

        | Approach | Time | Space | Notes |
        | --- | --- | --- | --- |
        | Naive | Often polynomial | Low to moderate | Good for validating tests |
        | Improved | Better asymptotic class | May trade memory | Prefer when constraints grow |
        | Idiomatic Python | Constants matter | Interpreter overhead | Profile before micro-optimizing |

        Justify every bound from loops, recursion depth, and allocated structures — not vibes.

        ## Tricks, tips and patterns

        - Name the pattern out loud before coding (it unlocks templates).
        - Keep a personal snippet library for this topic's standard shapes.
        - Prefer clarity first; compress only when the solution is correct.
        - Cross-link related lessons when the same invariant appears elsewhere.
        - For interviews, narrate the invariant and complexity as you write.

        ## Common mistakes and edge cases

        - Off-by-one errors at boundaries.
        - Forgetting empty inputs or single-element collections.
        - Mutating shared state unintentionally.
        - Claiming an asymptotic bound without accounting for hidden loops.
        - Overengineering before a correct baseline exists.

        ## Interview notes

        Interviewers listen for structured thinking: clarifying questions, an initial approach, complexity, then code. For **{title}**, expect follow-ups that tweak constraints (larger n, streaming input, or stricter memory).

        Practice explaining a wrong approach and how you would detect it with a counterexample — that signal is often stronger than a silent perfect solution.

        ## Practice problems

        1. Warm-up implementing the core operation on a tiny input (easy)
        2. Variant that changes one constraint (medium)
        3. Adversarial edge-case battery (medium)
        4. Related pattern transfer problem (hard)

        Use the Practice panel to run your solution against visible tests, then submit for hidden cases when the API sandbox is available.

        ## Summary / cheat sheet

        - {summary}
        - Focus points: {", ".join(focus)}
        - Always state invariants + complexity.
        - Dry-run before you optimize.
        - Connect the idea to at least one interview prompt.

        ## Further reading

        - Official documentation and primary references for this topic
        - A reputable textbook chapter covering the same idea
        - One high-quality visual or interactive explainer
        - The next lesson in this module — continue while the context is fresh
        """
    )


def json_dumps(values: list[str]) -> str:
    inner = ", ".join(f'"{v}"' for v in values)
    return f"[{inner}]"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--course", choices=sorted(CURRICULUM.keys()) + ["all"], default="all")
    args = parser.parse_args()

    courses = CURRICULUM.keys() if args.course == "all" else [args.course]
    written = 0
    for course in courses:
        for module, lessons in CURRICULUM[course].items():
            mod_dir = CONTENT / course / module
            mod_dir.mkdir(parents=True, exist_ok=True)
            for order, slug, title, summary, difficulty, tags, focus in lessons:
                path = mod_dir / f"{order:02d}-{slug}.mdx"
                if path.exists() and not args.force:
                    continue
                path.write_text(
                    render_lesson(course, module, order, slug, title, summary, difficulty, tags, focus),
                    encoding="utf-8",
                )
                written += 1
                print("wrote", path.relative_to(ROOT))
    print(f"Done. Wrote {written} lessons.")


if __name__ == "__main__":
    main()
