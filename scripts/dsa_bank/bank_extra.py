"""Flagship problems that finish the 250-problem set."""

from __future__ import annotations

from collections import OrderedDict, deque

from lib import cases, define


@define(
    slug="rotate-image",
    title="Rotate Image",
    difficulty="medium",
    topics=["arrays", "matrix"],
    statement="Rotate an n by n matrix 90 degrees clockwise and return it. Rotate in place in the algorithm.",
    constraints=["1 <= n <= 20", "-1000 <= matrix[i][j] <= 1000"],
    signature="from typing import List\n\ndef rotate(matrix: List[List[int]]) -> List[List[int]]:",
    function_name="rotate",
    hints=[
        "Transpose the matrix, then reverse every row.",
        "The transpose swaps matrix[i][j] with matrix[j][i] only for j greater than i, so each pair swaps once.",
        "Reversing each row turns the transpose into a clockwise rotation.",
    ],
    approaches=[
        ("Allocate a new matrix", "O(n^2)", "O(n^2)", "The cell at (i, j) moves to (j, n - 1 - i)."),
        ("Transpose and reverse", "O(n^2)", "O(1)", "The in-place rotation."),
    ],
    editorial=(
        "A clockwise rotation sends (i, j) to (j, n - 1 - i). "
        "Transposing sends (i, j) to (j, i), and reversing the row then sends that cell to (j, n - 1 - i). "
        "Doing the swap only above the diagonal keeps the transform in place."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Adobe"],
)
def rotate(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix


def _oracle_rotate(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix[::-1])]


cases(
    "rotate-image",
    _oracle_rotate,
    [
        ("classic", {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, True, "The first row becomes the last column."),
        ("two", {"matrix": [[1, 2], [3, 4]]}, True, "A 2 by 2 clockwise turn."),
        ("one", {"matrix": [[5]]}, False, None),
        ("four", {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]}, False, None),
        ("neg", {"matrix": [[-1, 0], [2, -3]]}, False, None),
    ],
)


@define(
    slug="find-the-duplicate-number",
    title="Find the Duplicate Number",
    difficulty="medium",
    topics=["arrays", "binary-search", "two-pointers"],
    statement=(
        "`nums` contains n + 1 integers, each in 1..n, and exactly one value is repeated. "
        "Return the repeated value. The array is treated as a linked list of indexes: the next node after i is nums[i]. Floyd's cycle finding locates the duplicate without modifying the array."
    ),
    constraints=["1 <= n <= 10^5", "nums.length == n + 1", "1 <= nums[i] <= n", "Exactly one duplicate"],
    signature="from typing import List\n\ndef find_duplicate(nums: List[int]) -> int:",
    function_name="find_duplicate",
    hints=[
        "Because every value is in 1..n and there are n + 1 entries, following nums[i] as a next pointer must cycle.",
        "The duplicate is the entrance of the cycle. Floyd's tortoise and hare finds a meeting point inside the cycle.",
        "Reset one pointer to nums[0] and move both one step at a time. They meet at the cycle entrance.",
    ],
    approaches=[
        ("Sort or count", "O(n log n) or O(n)", "O(n)", "Easy, and it uses extra memory or mutates the array."),
        ("Floyd cycle detection", "O(n)", "O(1)", "The index-linked-list interpretation."),
    ],
    editorial=(
        "The values are legal indexes into the array, except that index 0 is only a starting point. "
        "A repeated value means two indexes point at the same next node, which is the cycle entrance. "
        "The first loop finds any point on the cycle. The second loop walks from the start and from that meeting point at the same speed, and the first repeated node is the duplicate."
    ),
    companies=["Amazon", "Microsoft", "Google", "Adobe"],
)
def find_duplicate(nums: list[int]) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


def _oracle_find_duplicate(nums: list[int]) -> int:
    seen: set[int] = set()
    for value in nums:
        if value in seen:
            return value
        seen.add(value)
    return -1


cases(
    "find-the-duplicate-number",
    _oracle_find_duplicate,
    [
        ("classic", {"nums": [1, 3, 4, 2, 2]}, True, "2 is the repeated value."),
        ("three", {"nums": [3, 1, 3, 4, 2]}, True, "3 is repeated."),
        ("pair", {"nums": [1, 1]}, False, None),
        ("end", {"nums": [2, 5, 1, 1, 4, 3]}, False, None),
        ("high", {"nums": [4, 3, 1, 4, 2]}, False, None),
    ],
)


@define(
    slug="reverse-nodes-in-k-group",
    title="Reverse Nodes in k-Group",
    difficulty="hard",
    topics=["linked-lists"],
    statement=(
        "The list is given as values. Reverse every group of `k` nodes and return the new sequence. "
        "A leftover tail shorter than k stays in its original order. Rewire next pointers."
    ),
    constraints=["0 <= length <= 5000", "1 <= k <= length when the list is nonempty"],
    signature="from typing import List\n\ndef reverse_k_group(head: List[int], k: int) -> List[int]:",
    function_name="reverse_k_group",
    hints=[
        "A dummy node before the head makes the first group look like every other group.",
        "Walk k steps from the node before the group. If you fall off the list, stop.",
        "Reverse the k nodes by pointing each one at its predecessor, then attach the reversed block and move the group cursor to the new tail.",
    ],
    approaches=[
        ("Reverse value slices", "O(n)", "O(n)", "Correct output, but it does not practice pointer rewiring."),
        ("Pointer reversal per group", "O(n)", "O(1)", "Each node is rewired once."),
    ],
    editorial=(
        "Count k successors from the node that precedes the current group. "
        "If they exist, reverse that segment with the usual three-pointer loop, using the node after the segment as the initial previous pointer so the tail of the reversed group stays connected. "
        "The old head of the group becomes the tail, and the next iteration starts there."
    ),
    companies=["Amazon", "Microsoft", "Google", "Adobe"],
)
def reverse_k_group(head: list[int], k: int) -> list[int]:
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt

    dummy = Node(0)
    tail = dummy
    for value in head:
        tail.nxt = Node(value)
        tail = tail.nxt
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.nxt
            if kth is None:
                node = dummy.nxt
                out = []
                while node:
                    out.append(node.value)
                    node = node.nxt
                return out
        group_next = kth.nxt
        prev, cur = group_next, group_prev.nxt
        for _ in range(k):
            nxt = cur.nxt
            cur.nxt = prev
            prev = cur
            cur = nxt
        new_tail = group_prev.nxt
        group_prev.nxt = prev
        group_prev = new_tail


def _oracle_reverse_k_group(head: list[int], k: int) -> list[int]:
    out = []
    for i in range(0, len(head), k):
        block = head[i : i + k]
        out.extend(reversed(block) if len(block) == k else block)
    return out


cases(
    "reverse-nodes-in-k-group",
    _oracle_reverse_k_group,
    [
        ("classic", {"head": [1, 2, 3, 4, 5], "k": 2}, True, "Pairs reverse and the last node stays."),
        ("three", {"head": [1, 2, 3, 4, 5], "k": 3}, True, "The first three reverse. The tail stays."),
        ("whole", {"head": [1, 2, 3], "k": 3}, False, None),
        ("one", {"head": [1, 2, 3], "k": 1}, False, None),
        ("empty", {"head": [], "k": 1}, False, None),
    ],
)


@define(
    slug="reorder-list",
    title="Reorder List",
    difficulty="medium",
    topics=["linked-lists", "two-pointers"],
    statement=(
        "Reorder the list, given as values, from L0, L1, ..., Ln into L0, Ln, L1, Ln-1, L2, ... "
        "Find the middle, reverse the second half, and merge the halves by rewiring pointers."
    ),
    constraints=["0 <= length <= 5 * 10^4"],
    signature="from typing import List\n\ndef reorder_list(head: List[int]) -> List[int]:",
    function_name="reorder_list",
    hints=[
        "The slow and fast pointers find the start of the second half. Fast moves two steps, slow moves one.",
        "Reverse the second half in place.",
        "Merge by alternating one node from the first half and one node from the reversed second half.",
    ],
    approaches=[
        ("Array of nodes", "O(n)", "O(n)", "Index the ends toward the middle."),
        ("Middle, reverse, merge", "O(n)", "O(1)", "The classic in-place reorder."),
    ],
    editorial=(
        "Split after the middle so the first half is at least as long as the second. "
        "Reverse the second half, then weave: each step takes the next first-half node and the next second-half node. "
        "The weave ends when the second half is exhausted. A middle node of an odd-length list remains at the end of the first half."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Adobe"],
)
def reorder_list(head: list[int]) -> list[int]:
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt

    if len(head) < 2:
        return head[:]
    dummy = Node(0)
    tail = dummy
    for value in head:
        tail.nxt = Node(value)
        tail = tail.nxt
    slow, fast = dummy.nxt, dummy.nxt
    while fast and fast.nxt:
        slow = slow.nxt
        fast = fast.nxt.nxt
    prev = None
    cur = slow
    while cur:
        nxt = cur.nxt
        cur.nxt = prev
        prev = cur
        cur = nxt
    first = dummy.nxt
    second = prev
    while second.nxt:
        nxt1, nxt2 = first.nxt, second.nxt
        first.nxt = second
        second.nxt = nxt1
        first, second = nxt1, nxt2
    out = []
    node = dummy.nxt
    while node:
        out.append(node.value)
        node = node.nxt
    return out


def _oracle_reorder_list(head: list[int]) -> list[int]:
    out = []
    i, j = 0, len(head) - 1
    while i <= j:
        out.append(head[i])
        if i != j:
            out.append(head[j])
        i += 1
        j -= 1
    return out


cases(
    "reorder-list",
    _oracle_reorder_list,
    [
        ("classic", {"head": [1, 2, 3, 4]}, True, "The order becomes 1, 4, 2, 3."),
        ("odd", {"head": [1, 2, 3, 4, 5]}, True, "The order becomes 1, 5, 2, 4, 3."),
        ("empty", {"head": []}, False, None),
        ("one", {"head": [1]}, False, None),
        ("two", {"head": [1, 2]}, False, None),
    ],
)


@define(
    slug="copy-list-with-random-pointer",
    title="Copy List with Random Pointer",
    difficulty="medium",
    topics=["linked-lists", "hashing"],
    statement=(
        "Each node is [value, random_index]. random_index is -1 when the random pointer is null, otherwise the index of the target node. "
        "Deep-copy the list, including random pointers, and return [value, random_value] for each node in order. random_value is null when the pointer is null. Values in the tests are unique, so the random value identifies the target."
    ),
    constraints=["0 <= n <= 1000", "-10000 <= value <= 10000"],
    signature="from typing import List, Optional\n\ndef copy_random_list(nodes: List[List[int]]) -> List[List[Optional[int]]]:",
    function_name="copy_random_list",
    hints=[
        "The hashmap solution clones every node, then assigns next and random by looking up the originals.",
        "The constant-extra-space solution weaves each clone immediately after its original.",
        "After the weave, original.random.next is the clone of the random target. Then unweave the two lists.",
    ],
    approaches=[
        ("Hash map from original to clone", "O(n)", "O(n)", "Two passes."),
        ("Interleaved clones", "O(n)", "O(1) extra", "Weave, assign random, unweave."),
    ],
    editorial=(
        "Build the original list, then insert a clone after every node. "
        "The clone's random pointer is the next node of the original's random pointer, which is that target's clone. "
        "A final pass separates the two lists. The returned pairs read the clone values and the clone random values."
    ),
    companies=["Amazon", "Microsoft", "Facebook", "Bloomberg"],
)
def copy_random_list(nodes: list[list[int]]) -> list[list[int | None]]:
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt
            self.rnd = None

    if not nodes:
        return []
    built: list[Node] = []
    prev = None
    for value, _random_index in nodes:
        node = Node(value)
        built.append(node)
        if prev:
            prev.nxt = node
        prev = node
    for index, node in enumerate(built):
        target = nodes[index][1]
        if target >= 0:
            node.rnd = built[target]
    for node in built:
        clone = Node(node.value, node.nxt)
        node.nxt = clone
    for node in built:
        if node.rnd:
            node.nxt.rnd = node.rnd.nxt
    out: list[list[int | None]] = []
    for node in built:
        clone = node.nxt
        node.nxt = clone.nxt
        if clone.nxt:
            clone.nxt = clone.nxt.nxt
        out.append([clone.value, clone.rnd.value if clone.rnd else None])
    return out


def _oracle_copy_random_list(nodes: list[list[int]]) -> list[list[int | None]]:
    values = [value for value, _index in nodes]
    out = []
    for value, index in nodes:
        out.append([value, None if index < 0 else values[index]])
    return out


cases(
    "copy-list-with-random-pointer",
    _oracle_copy_random_list,
    [
        ("classic", {"nodes": [[7, -1], [13, 0], [11, 4], [10, 2], [1, 0]]}, True, "Random targets become the values of those nodes."),
        ("self", {"nodes": [[1, 1], [2, 1]]}, True, "The second node points at itself."),
        ("empty", {"nodes": []}, False, None),
        ("nulls", {"nodes": [[3, -1], [4, -1]]}, False, None),
        ("cycle-random", {"nodes": [[1, 1], [2, 0]]}, False, None),
    ],
)


@define(
    slug="critical-connections",
    title="Critical Connections in a Network",
    difficulty="hard",
    topics=["graphs", "tarjan", "bridges"],
    statement=(
        "There are `n` servers labeled 0..n-1 and undirected connections. "
        "A critical connection is a bridge: an edge whose removal increases the number of connected components. "
        "Return every bridge as [u, v] with u less than v, sorted lexicographically."
    ),
    constraints=["1 <= n <= 10^5", "0 <= connections.length <= 10^5", "No repeated edges"],
    signature="from typing import List\n\ndef critical_connections(n: int, connections: List[List[int]]) -> List[List[int]]:",
    function_name="critical_connections",
    hints=[
        "A DFS discovery time and a low-link value are enough. low[v] is the smallest discovery time reachable from v without using the parent edge.",
        "The edge u-v, with u the parent, is a bridge when low[v] is strictly greater than disc[u]. The child cannot reach the parent or anything above it.",
        "Ignore the edge back to the parent, but do use other back edges to lower the low-link value.",
    ],
    approaches=[
        ("Remove each edge and recheck connectivity", "O(E * (V + E))", "O(V + E)", "Fine for tiny graphs and a useful oracle."),
        ("Tarjan bridge DFS", "O(V + E)", "O(V + E)", "One depth-first search."),
    ],
    editorial=(
        "Assign increasing discovery times as DFS enters each node. "
        "A child's low-link is the minimum of its own discovery time, the low-links of its children, and the discovery times of back edges. "
        "If after exploring a child its low-link stays above the parent's discovery time, the tree edge is the only connection and it is a bridge."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    disc = [-1] * n
    low = [0] * n
    time = 0
    bridges: list[list[int]] = []

    def dfs(node: int, parent: int) -> None:
        nonlocal time
        disc[node] = low[node] = time
        time += 1
        for nxt in graph[node]:
            if nxt == parent:
                continue
            if disc[nxt] == -1:
                dfs(nxt, node)
                low[node] = min(low[node], low[nxt])
                if low[nxt] > disc[node]:
                    bridges.append(sorted([node, nxt]))
            else:
                low[node] = min(low[node], disc[nxt])

    for node in range(n):
        if disc[node] == -1:
            dfs(node, -1)
    bridges.sort()
    return bridges


def _oracle_critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    def components(skip: tuple[int, int] | None) -> int:
        graph: list[list[int]] = [[] for _ in range(n)]
        for u, v in connections:
            if skip and {u, v} == set(skip):
                continue
            graph[u].append(v)
            graph[v].append(u)
        seen = [False] * n
        count = 0
        for start in range(n):
            if seen[start]:
                continue
            count += 1
            stack = [start]
            seen[start] = True
            while stack:
                node = stack.pop()
                for nxt in graph[node]:
                    if not seen[nxt]:
                        seen[nxt] = True
                        stack.append(nxt)
        return count

    base = components(None)
    bridges = []
    for u, v in connections:
        if components((u, v)) > base:
            bridges.append(sorted([u, v]))
    bridges.sort()
    return bridges


cases(
    "critical-connections",
    _oracle_critical_connections,
    [
        ("classic", {"n": 4, "connections": [[0, 1], [1, 2], [2, 0], [1, 3]]}, True, "The edge from 1 to 3 is the only bridge."),
        ("line", {"n": 3, "connections": [[0, 1], [1, 2]]}, True, "Both edges are bridges."),
        ("cycle", {"n": 3, "connections": [[0, 1], [1, 2], [2, 0]]}, False, None),
        ("one", {"n": 1, "connections": []}, False, None),
        ("two", {"n": 2, "connections": [[0, 1]]}, False, None),
    ],
)


@define(
    slug="longest-increasing-path-in-a-matrix",
    title="Longest Increasing Path in a Matrix",
    difficulty="hard",
    topics=["graphs", "dynamic-programming", "matrix"],
    statement="Return the length of the longest strictly increasing path in the matrix. Moves are 4-directional.",
    constraints=["1 <= m, n <= 200", "0 <= matrix[i][j] <= 2^31 - 1"],
    signature="from typing import List\n\ndef longest_increasing_path(matrix: List[List[int]]) -> int:",
    function_name="longest_increasing_path",
    hints=[
        "From each cell, the answer is 1 plus the best answer among strictly greater neighbors.",
        "Memoize by cell. Each cell is solved once because the increasing constraint makes the dependency graph a DAG.",
        "The global answer is the maximum over every starting cell.",
    ],
    approaches=[
        ("DFS from every cell", "exponential", "O(mn)", "Overlapping subpaths are recomputed."),
        ("Memoized DFS", "O(mn)", "O(mn)", "Each cell and each edge is processed once."),
    ],
    editorial=(
        "The state is the cell, not the path, because every increasing path that reaches a cell can be extended by the same best continuation. "
        "That is why memoization is correct. "
        "A cell with no greater neighbor has length 1."
    ),
    companies=["Google", "Amazon", "Facebook", "Microsoft"],
)
def longest_increasing_path(matrix: list[list[int]]) -> int:
    rows, cols = len(matrix), len(matrix[0])
    memo = [[0] * cols for _ in range(rows)]

    def dfs(r: int, c: int) -> int:
        if memo[r][c]:
            return memo[r][c]
        best = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[r][c] = best
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))


def _oracle_longest_increasing_path(matrix: list[list[int]]) -> int:
    rows, cols = len(matrix), len(matrix[0])

    def dfs(r: int, c: int, prev: int) -> int:
        if not (0 <= r < rows and 0 <= c < cols) or matrix[r][c] <= prev:
            return 0
        return 1 + max(
            dfs(r + dr, c + dc, matrix[r][c]) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
        )

    return max(dfs(r, c, -1) for r in range(rows) for c in range(cols))


cases(
    "longest-increasing-path-in-a-matrix",
    _oracle_longest_increasing_path,
    [
        ("classic", {"matrix": [[9, 9, 4], [6, 6, 8], [2, 1, 1]]}, True, "The path 1, 2, 6, 9 has length 4."),
        ("three", {"matrix": [[3, 4, 5], [3, 2, 6], [2, 2, 1]]}, True, "The longest path has length 4."),
        ("one", {"matrix": [[1]]}, False, None),
        ("flat", {"matrix": [[7, 7], [7, 7]]}, False, None),
        ("row", {"matrix": [[1, 2, 3]]}, False, None),
    ],
)


@define(
    slug="dungeon-game",
    title="Dungeon Game",
    difficulty="hard",
    topics=["dynamic-programming", "matrix"],
    statement=(
        "The knight starts at the top-left of the dungeon and must reach the bottom-right, moving only right or down. "
        "dungeon[i][j] is the health change of that room. Health must stay at least 1 at every moment, including after the final room. "
        "Return the minimum starting health that makes the rescue possible."
    ),
    constraints=["1 <= m, n <= 200", "-1000 <= dungeon[i][j] <= 1000"],
    signature="from typing import List\n\ndef calculate_minimum_hp(dungeon: List[List[int]]) -> int:",
    function_name="calculate_minimum_hp",
    hints=[
        "Work backward. The future requirement is easier to express than the past.",
        "After the last room the knight needs health 1. Before entering a room, the knight needs enough health to absorb that room and still meet the cheaper child's requirement.",
        "The need is max(1, min(need_right, need_down) - dungeon[i][j]). A positive room can reduce the requirement, but never below 1.",
    ],
    approaches=[
        ("Forward search of starting health", "O(mn log H)", "O(mn)", "Binary search the start and simulate."),
        ("Backward DP", "O(mn)", "O(mn)", "Each room stores the health required on entry."),
    ],
    editorial=(
        "Let dp[i][j] be the minimum health required when entering room (i, j). "
        "The princess room requires max(1, 1 - dungeon[m-1][n-1]). "
        "Every earlier room takes the cheaper of the two legal exits, subtracts its own health change, and clamps the result to at least 1. The top-left value is the answer."
    ),
    companies=["Amazon", "Google", "Microsoft", "Adobe"],
)
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    rows, cols = len(dungeon), len(dungeon[0])
    need = [[10**9] * (cols + 1) for _ in range(rows + 1)]
    need[rows][cols - 1] = need[rows - 1][cols] = 1
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            need[r][c] = max(1, min(need[r + 1][c], need[r][c + 1]) - dungeon[r][c])
    return need[0][0]


def _oracle_calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    rows, cols = len(dungeon), len(dungeon[0])
    memo: dict[tuple[int, int], int] = {}

    def enter(r: int, c: int) -> int:
        if (r, c) in memo:
            return memo[(r, c)]
        if r == rows - 1 and c == cols - 1:
            answer = max(1, 1 - dungeon[r][c])
        else:
            options = []
            if r + 1 < rows:
                options.append(enter(r + 1, c))
            if c + 1 < cols:
                options.append(enter(r, c + 1))
            answer = max(1, min(options) - dungeon[r][c])
        memo[(r, c)] = answer
        return answer

    return enter(0, 0)


cases(
    "dungeon-game",
    _oracle_calculate_minimum_hp,
    [
        ("classic", {"dungeon": [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]}, True, "The knight needs 7 health at the start."),
        ("one-negative", {"dungeon": [[-5]]}, True, "Start at 6 so the room leaves the knight at 1."),
        ("one-positive", {"dungeon": [[5]]}, False, None),
        ("row", {"dungeon": [[0, -3]]}, False, None),
        ("gain", {"dungeon": [[2, -1], [-1, -1]]}, False, None),
    ],
)


@define(
    slug="regular-expression-matching",
    title="Regular Expression Matching",
    difficulty="hard",
    topics=["dynamic-programming", "strings"],
    statement=(
        "Implement matching where '.' matches any single character and '*' matches zero or more of the preceding element. "
        "The match must cover the entire string. Return true when `s` matches the pattern `p`."
    ),
    constraints=["0 <= s.length <= 20", "0 <= p.length <= 30", "p is a valid pattern"],
    signature="def is_match(s: str, p: str) -> bool:",
    function_name="is_match",
    hints=[
        "A star applies to the character before it, and it is a choice: use none of them, or use one and keep the star available.",
        "dp[i][j] means s[:i] matches p[:j].",
        "If p[j-1] is a star, the cell is true when the star matches empty (dp[i][j-2]) or when the current character matches the starred element and dp[i-1][j] is true.",
    ],
    approaches=[
        ("Backtracking", "exponential", "O(n + m)", "Try both branches of every star."),
        ("Boolean DP", "O(n * m)", "O(n * m)", "Each pair of prefixes is decided once."),
    ],
    editorial=(
        "The empty pattern matches only the empty string. "
        "A pattern that begins with a star-capable pair can match empty text when the star consumes nothing, which fills the first row. "
        "Every other cell either consumes one character, or handles a star by choosing empty or one-or-more. The bottom-right cell is the full match."
    ),
    companies=["Google", "Facebook", "Uber", "Amazon"],
)
def is_match(s: str, p: str) -> bool:
    rows, cols = len(s) + 1, len(p) + 1
    dp = [[False] * cols for _ in range(rows)]
    dp[0][0] = True
    for j in range(2, cols):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]
    for i in range(1, rows):
        for j in range(1, cols):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2] or (
                    dp[i - 1][j] and p[j - 2] in {s[i - 1], "."}
                )
            elif p[j - 1] in {s[i - 1], "."}:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[-1][-1]


def _oracle_is_match(s: str, p: str) -> bool:
    def match(i: int, j: int) -> bool:
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in {s[i], "."}
        if j + 1 < len(p) and p[j + 1] == "*":
            return match(i, j + 2) or (first and match(i + 1, j))
        return first and match(i + 1, j + 1)

    return match(0, 0)


cases(
    "regular-expression-matching",
    _oracle_is_match,
    [
        ("star", {"s": "aa", "p": "a*"}, True, "The star consumes both a's."),
        ("dot-star", {"s": "ab", "p": ".*"}, True, "Dot-star consumes any string."),
        ("mixed", {"s": "aab", "p": "c*a*b"}, False, None),
        ("miss", {"s": "mississippi", "p": "mis*is*p*."}, False, None),
        ("empty", {"s": "", "p": "a*"}, False, None),
    ],
)


@define(
    slug="burst-balloons",
    title="Burst Balloons",
    difficulty="hard",
    topics=["dynamic-programming", "divide-and-conquer"],
    statement=(
        "Balloons are numbered by `nums`. Bursting balloon i earns nums[left] * nums[i] * nums[right], where left and right are the nearest balloons that have not been burst. "
        "Add a balloon of value 1 at each end. Return the maximum coins you can collect."
    ),
    constraints=["1 <= nums.length <= 300", "0 <= nums[i] <= 100"],
    signature="from typing import List\n\ndef max_coins(nums: List[int]) -> int:",
    function_name="max_coins",
    hints=[
        "Choosing the first balloon to burst is awkward because the neighbors change. Choose the last balloon to burst in an interval instead.",
        "If k is the last balloon burst between left and right, the coins are nums[left] * nums[k] * nums[right] plus the two subintervals.",
        "Add the boundary ones, then fill intervals by increasing length.",
    ],
    approaches=[
        ("Try every burst order", "O(n!)", "O(n)", "Only for tiny n."),
        ("Interval DP", "O(n^3)", "O(n^2)", "The last-burst choice."),
    ],
    editorial=(
        "Pad the array with ones. dp[left][right] is the best score for bursting every balloon strictly between those bounds. "
        "The last balloon k between them sees the two bounds as neighbors, so its score does not depend on the order inside the subintervals. "
        "Those subintervals are shorter and already solved. The answer is dp[0][len-1]."
    ),
    companies=["Google", "Amazon", "Snap", "Microsoft"],
)
def max_coins(nums: list[int]) -> int:
    arr = [1, *nums, 1]
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for span in range(2, n):
        for left in range(n - span):
            right = left + span
            for k in range(left + 1, right):
                coins = arr[left] * arr[k] * arr[right] + dp[left][k] + dp[k][right]
                dp[left][right] = max(dp[left][right], coins)
    return dp[0][n - 1]


def _oracle_max_coins(nums: list[int]) -> int:
    arr = [1, *nums, 1]
    memo: dict[tuple[int, int], int] = {}

    def best(left: int, right: int) -> int:
        if right - left < 2:
            return 0
        if (left, right) in memo:
            return memo[(left, right)]
        memo[(left, right)] = max(
            arr[left] * arr[k] * arr[right] + best(left, k) + best(k, right)
            for k in range(left + 1, right)
        )
        return memo[(left, right)]

    return best(0, len(arr) - 1)


cases(
    "burst-balloons",
    _oracle_max_coins,
    [
        ("classic", {"nums": [3, 1, 5, 8]}, True, "The best order collects 167 coins."),
        ("one", {"nums": [5]}, True, "The only balloon is worth 1 * 5 * 1."),
        ("two", {"nums": [1, 5]}, False, None),
        ("zeros", {"nums": [0, 0]}, False, None),
        ("three", {"nums": [2, 3, 4]}, False, None),
    ],
)


@define(
    slug="single-number-ii",
    title="Single Number II",
    difficulty="medium",
    topics=["bit-manipulation"],
    statement="Every element appears three times except one element, which appears once. Return the single element. The values in these tests are non-negative.",
    constraints=["1 <= nums.length <= 3 * 10^4", "0 <= nums[i] <= 2^31 - 1"],
    signature="from typing import List\n\ndef single_number_ii(nums: List[int]) -> int:",
    function_name="single_number_ii",
    hints=[
        "Count each bit modulo 3. The bits whose count is not divisible by 3 belong to the single number.",
        "Two variables, ones and twos, are a finite-state machine for the count of each bit.",
        "ones holds bits seen 1 mod 3. twos holds bits seen 2 mod 3. Seeing a bit the third time clears both.",
    ],
    approaches=[
        ("Hash count", "O(n)", "O(n)", "Return the key whose count is 1."),
        ("Bit state machine", "O(n)", "O(1)", "Constant memory, one pass."),
    ],
    editorial=(
        "For every number, XOR it into ones and then clear any bit that is also in twos. "
        "Then XOR it into twos and clear any bit that is also in ones. "
        "The order matters: a bit moves from ones to twos to gone. After the whole array, ones holds the unique value."
    ),
    companies=["Amazon", "Google", "Adobe", "Microsoft"],
)
def single_number_ii(nums: list[int]) -> int:
    ones = twos = 0
    for value in nums:
        ones = (ones ^ value) & ~twos
        twos = (twos ^ value) & ~ones
    return ones


def _oracle_single_number_ii(nums: list[int]) -> int:
    from collections import Counter

    return next(value for value, count in Counter(nums).items() if count == 1)


cases(
    "single-number-ii",
    _oracle_single_number_ii,
    [
        ("classic", {"nums": [2, 2, 3, 2]}, True, "3 appears once."),
        ("zero", {"nums": [0, 1, 0, 1, 0, 1, 99]}, True, "99 appears once."),
        ("single", {"nums": [7]}, False, None),
        ("high", {"nums": [4, 4, 4, 8]}, False, None),
        ("mixed", {"nums": [5, 6, 5, 6, 5, 6, 1]}, False, None),
    ],
)


@define(
    slug="sum-of-two-integers",
    title="Sum of Two Integers",
    difficulty="medium",
    topics=["bit-manipulation", "math"],
    statement="Return the sum of two non-negative integers without using the addition or subtraction operators.",
    constraints=["0 <= a, b <= 1000"],
    signature="def get_sum(a: int, b: int) -> int:",
    function_name="get_sum",
    hints=[
        "XOR writes the sum bits where the bits differ, which is addition without carry.",
        "AND, shifted left by one, is the carry.",
        "Repeat until the carry is zero.",
    ],
    approaches=[
        ("Built-in addition", "O(1)", "O(1)", "Not the point of the problem."),
        ("XOR and carry", "O(1)", "O(1)", "Each step pushes the carry one position higher."),
    ],
    editorial=(
        "On paper, a column with two 1s writes 0 and carries 1. XOR writes the 0, and the shifted AND is the carry into the next column. "
        "Columns with a single 1 are finished by the XOR. "
        "When the carry becomes zero, every column is finished and the XOR is the sum."
    ),
    companies=["Facebook", "Amazon", "Adobe", "Microsoft"],
)
def get_sum(a: int, b: int) -> int:
    while b:
        a, b = a ^ b, (a & b) << 1
    return a


def _oracle_get_sum(a: int, b: int) -> int:
    return a + b


cases(
    "sum-of-two-integers",
    _oracle_get_sum,
    [
        ("classic", {"a": 1, "b": 2}, True, "The sum is 3."),
        ("carry", {"a": 5, "b": 7}, True, "The sum is 12."),
        ("zero", {"a": 0, "b": 0}, False, None),
        ("one-side", {"a": 20, "b": 0}, False, None),
        ("same", {"a": 8, "b": 8}, False, None),
    ],
)


@define(
    slug="integer-to-roman",
    title="Integer to Roman",
    difficulty="medium",
    topics=["math", "strings", "greedy"],
    statement="Convert an integer in the range 1..3999 to its Roman numeral. Use the standard subtractive pairs: CM, CD, XC, XL, IX, and IV.",
    constraints=["1 <= num <= 3999"],
    signature="def int_to_roman(num: int) -> str:",
    function_name="int_to_roman",
    hints=[
        "List the symbols from largest to smallest, including the six subtractive pairs.",
        "Greedily take as many of the current symbol as fit.",
        "Because the list is sorted and includes the subtractive forms, the greedy choice is the standard numeral.",
    ],
    approaches=[
        ("Digit place tables", "O(1)", "O(1)", "Four arrays for thousands, hundreds, tens, and ones."),
        ("Greedy symbol list", "O(1)", "O(1)", "Thirteen symbols cover every value."),
    ],
    editorial=(
        "Walk the value-symbol pairs from 1000 down to 1. "
        "While the remaining number is at least the current value, append the symbol and subtract. "
        "The subtractive pairs sit between the plain symbols, so 4, 9, 40, 90, 400, and 900 are taken before three or four copies of a smaller symbol."
    ),
    companies=["Amazon", "Adobe", "Microsoft", "Apple"],
)
def int_to_roman(num: int) -> str:
    pairs = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )
    parts: list[str] = []
    for value, symbol in pairs:
        while num >= value:
            parts.append(symbol)
            num -= value
    return "".join(parts)


def _oracle_int_to_roman(num: int) -> str:
    thousands = ["", "M", "MM", "MMM"]
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return thousands[num // 1000] + hundreds[(num % 1000) // 100] + tens[(num % 100) // 10] + ones[num % 10]


cases(
    "integer-to-roman",
    _oracle_int_to_roman,
    [
        ("three", {"num": 3}, True, "III."),
        ("fifty-eight", {"num": 58}, True, "LVIII."),
        ("year", {"num": 1994}, False, None),
        ("four", {"num": 4}, False, None),
        ("nine-hundred", {"num": 900}, False, None),
    ],
)


@define(
    slug="online-stock-span",
    title="Online Stock Span",
    difficulty="medium",
    topics=["stacks", "monotonic-stack"],
    statement=(
        "The span of a price is the number of consecutive days, ending today, on which the price was less than or equal to today's price. "
        "`prices[i]` arrives on day i. Return the span of every day."
    ),
    constraints=["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^5"],
    signature="from typing import List\n\ndef stock_spans(prices: List[int]) -> List[int]:",
    function_name="stock_spans",
    hints=[
        "A decreasing stack stores prices that are still candidates to stop a future span.",
        "Before pushing today, pop every price that is less than or equal to today. Those days are covered by today's span.",
        "Store the span with the price so a pop can add that whole span in constant time instead of walking day by day.",
    ],
    approaches=[
        ("Scan backward each day", "O(n^2)", "O(1)", "Stop at the first strictly greater price."),
        ("Monotonic stack", "O(n)", "O(n)", "Each day is pushed and popped once."),
    ],
    editorial=(
        "The span is one plus the spans of the consecutive previous days that are not strictly greater. "
        "Those days sit on the stack in decreasing order. Popping them accumulates their spans, and the first strictly greater price stays on the stack as the new blocker. "
        "Today is then pushed with its total span."
    ),
    companies=["Amazon", "Bloomberg", "Adobe", "Microsoft"],
)
def stock_spans(prices: list[int]) -> list[int]:
    stack: list[tuple[int, int]] = []
    spans: list[int] = []
    for price in prices:
        span = 1
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]
        stack.append((price, span))
        spans.append(span)
    return spans


def _oracle_stock_spans(prices: list[int]) -> list[int]:
    spans = []
    for i, price in enumerate(prices):
        span = 1
        j = i - 1
        while j >= 0 and prices[j] <= price:
            span += 1
            j -= 1
        spans.append(span)
    return spans


cases(
    "online-stock-span",
    _oracle_stock_spans,
    [
        ("classic", {"prices": [100, 80, 60, 70, 60, 75, 85]}, True, "The spans are 1, 1, 1, 2, 1, 4, 6."),
        ("rising", {"prices": [1, 2, 3]}, True, "Each day covers every earlier day."),
        ("falling", {"prices": [3, 2, 1]}, False, None),
        ("flat", {"prices": [5, 5, 5]}, False, None),
        ("one", {"prices": [10]}, False, None),
    ],
)


@define(
    slug="lfu-cache",
    title="LFU Cache",
    difficulty="hard",
    topics=["hashing", "design", "linked-lists"],
    statement=(
        "Simulate an LFU cache of the given capacity. "
        "`operations` are get and put. get(key) returns the value or -1 and counts as a use. "
        "put(key, value) inserts or updates. When the cache is full, evict the least frequently used key, breaking ties by least recently used. "
        "put returns null. A capacity of 0 rejects every put."
    ),
    constraints=["0 <= capacity <= 10^4", "0 <= key, value <= 10^5", "At most 2 * 10^5 calls"],
    signature="from typing import List, Optional\n\ndef lfu_ops(capacity: int, operations: List[str], arguments: List[List[int]]) -> List[Optional[int]]:",
    function_name="lfu_ops",
    hints=[
        "A map from key to (value, frequency) answers get in constant time.",
        "A second map from frequency to an ordered dictionary of keys keeps each frequency bucket in LRU order.",
        "Remember the current minimum frequency. Eviction pops the oldest key in that bucket, and a use moves a key into the next bucket.",
    ],
    approaches=[
        ("Scan for the eviction victim", "O(n) per put", "O(capacity)", "Track frequency and a timestamp, then scan."),
        ("Frequency buckets", "O(1) per call", "O(capacity)", "Ordered dictionaries give LRU order inside a frequency."),
    ],
    editorial=(
        "get on a missing key returns -1. get on a present key increments its frequency and moves it to the most-recent end of the new bucket. "
        "If its old bucket becomes empty and it was the minimum frequency, the minimum rises by one. "
        "put of a new key evicts first when at capacity, then inserts the key at frequency 1, which becomes the new minimum."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def lfu_ops(capacity: int, operations: list[str], arguments: list[list[int]]) -> list[int | None]:
    values: dict[int, int] = {}
    freq: dict[int, int] = {}
    buckets: dict[int, OrderedDict] = {}
    minimum = 0

    def touch(key: int) -> None:
        nonlocal minimum
        old = freq[key]
        buckets[old].pop(key)
        if not buckets[old] and minimum == old:
            minimum += 1
        freq[key] = old + 1
        buckets.setdefault(old + 1, OrderedDict())[key] = None

    out: list[int | None] = []
    for op, arg in zip(operations, arguments):
        if op == "get":
            key = arg[0]
            if key not in values:
                out.append(-1)
            else:
                touch(key)
                out.append(values[key])
        else:
            key, value = arg
            if capacity == 0:
                out.append(None)
                continue
            if key in values:
                values[key] = value
                touch(key)
            else:
                if len(values) >= capacity:
                    evict, _marker = buckets[minimum].popitem(last=False)
                    del values[evict]
                    del freq[evict]
                values[key] = value
                freq[key] = 1
                buckets.setdefault(1, OrderedDict())[key] = None
                minimum = 1
            out.append(None)
    return out


def _oracle_lfu_ops(capacity: int, operations: list[str], arguments: list[list[int]]) -> list[int | None]:
    data: dict[int, list[int]] = {}
    clock = 0
    out: list[int | None] = []
    for op, arg in zip(operations, arguments):
        clock += 1
        if op == "get":
            key = arg[0]
            if key not in data:
                out.append(-1)
            else:
                data[key][1] += 1
                data[key][2] = clock
                out.append(data[key][0])
        else:
            key, value = arg
            if capacity == 0:
                out.append(None)
                continue
            if key in data:
                data[key][0] = value
                data[key][1] += 1
                data[key][2] = clock
            else:
                if len(data) >= capacity:
                    victim = min(data, key=lambda item: (data[item][1], data[item][2]))
                    del data[victim]
                data[key] = [value, 1, clock]
            out.append(None)
    return out


cases(
    "lfu-cache",
    _oracle_lfu_ops,
    [
        (
            "classic",
            {
                "capacity": 2,
                "operations": ["put", "put", "get", "put", "get", "get", "put", "get", "get", "get"],
                "arguments": [[1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]],
            },
            True,
            "Frequency, then recency, decides the eviction.",
        ),
        (
            "zero",
            {"capacity": 0, "operations": ["put", "get"], "arguments": [[1, 1], [1]]},
            True,
            "A zero-capacity cache stores nothing.",
        ),
        (
            "update",
            {"capacity": 2, "operations": ["put", "put", "put", "get"], "arguments": [[1, 1], [1, 2], [2, 3], [1]]},
            False,
            None,
        ),
        (
            "tie",
            {"capacity": 2, "operations": ["put", "put", "get", "get", "put", "get", "get"], "arguments": [[1, 1], [2, 2], [1], [2], [3, 3], [1], [2]]},
            False,
            None,
        ),
        (
            "one",
            {"capacity": 1, "operations": ["put", "get", "put", "get", "get"], "arguments": [[2, 1], [2], [3, 2], [2], [3]]},
            False,
            None,
        ),
    ],
)


@define(
    slug="fenwick-range-sum",
    title="Fenwick Tree Range Sum",
    difficulty="medium",
    topics=["trees", "fenwick", "binary-indexed-tree"],
    statement=(
        "An array of `n` zeros is updated with a Fenwick tree, also called a binary indexed tree. "
        "Each operation is [0, index, delta] to add, or [1, left, right] to query. Indexes are 0-based and ranges are inclusive. "
        "Return the result of every query, in order."
    ),
    constraints=["1 <= n <= 10^5", "1 <= operations.length <= 10^5", "0 <= index, left, right < n"],
    signature="from typing import List\n\ndef fenwick_ops(n: int, operations: List[List[int]]) -> List[int]:",
    function_name="fenwick_ops",
    hints=[
        "A Fenwick tree stores partial sums. Index i in the tree, using 1-based indexes, covers the range ending at i whose length is the lowest set bit of i.",
        "add walks upward by adding the lowest set bit. A prefix sum walks downward by clearing the lowest set bit.",
        "A range sum is prefix(right) - prefix(left - 1). Convert 0-based indexes to 1-based indexes at the boundary.",
    ],
    approaches=[
        ("Plain array", "O(n) per query", "O(n)", "Correct and slow when both updates and queries are frequent."),
        ("Fenwick tree", "O(log n) per operation", "O(n)", "The binary indexed tree."),
    ],
    editorial=(
        "Store n + 1 slots and ignore index 0. "
        "To add at a 1-based index, add the delta and jump forward by index & -index. "
        "A prefix sum adds the slot and jumps backward the same way. Subtracting prefix sums answers a range. The point of the structure is that both walks are logarithmic."
    ),
    companies=["Google", "Amazon", "Uber", "Microsoft"],
)
def fenwick_ops(n: int, operations: list[list[int]]) -> list[int]:
    bit = [0] * (n + 1)

    def add(index: int, delta: int) -> None:
        index += 1
        while index <= n:
            bit[index] += delta
            index += index & -index

    def prefix(index: int) -> int:
        index += 1
        total = 0
        while index > 0:
            total += bit[index]
            index -= index & -index
        return total

    out: list[int] = []
    for kind, a, b in operations:
        if kind == 0:
            add(a, b)
        else:
            out.append(prefix(b) - (prefix(a - 1) if a else 0))
    return out


def _oracle_fenwick_ops(n: int, operations: list[list[int]]) -> list[int]:
    arr = [0] * n
    out = []
    for kind, a, b in operations:
        if kind == 0:
            arr[a] += b
        else:
            out.append(sum(arr[a : b + 1]))
    return out


cases(
    "fenwick-range-sum",
    _oracle_fenwick_ops,
    [
        (
            "classic",
            {"n": 5, "operations": [[0, 1, 4], [0, 3, 2], [1, 1, 3], [0, 1, -1], [1, 0, 4]]},
            True,
            "The first query sees 6. The second sees the whole array after the update.",
        ),
        ("empty-query", {"n": 1, "operations": [[1, 0, 0], [0, 0, 5], [1, 0, 0]]}, True, "A zero cell, then an update."),
        ("two", {"n": 3, "operations": [[0, 0, 1], [0, 2, 1], [1, 0, 2], [1, 1, 1]]}, False, None),
        ("overwrite", {"n": 2, "operations": [[0, 0, 3], [0, 0, 4], [1, 0, 0]]}, False, None),
        ("right", {"n": 4, "operations": [[0, 3, 8], [1, 2, 3], [1, 3, 3]]}, False, None),
    ],
)


@define(
    slug="count-subsets-with-sum",
    title="Count Subsets With Sum",
    difficulty="medium",
    topics=["divide-and-conquer", "meet-in-the-middle", "dynamic-programming"],
    statement=(
        "Count the subsets of `nums` whose values add up to `target`. "
        "The empty subset sums to 0. Values are non-negative and the list has at most 20 elements, so meet-in-the-middle splits the list in half, enumerates both halves, and counts complementary sums."
    ),
    constraints=["0 <= nums.length <= 20", "0 <= nums[i] <= 1000", "0 <= target <= 20000"],
    signature="from typing import List\n\ndef count_subsets(nums: List[int], target: int) -> int:",
    function_name="count_subsets",
    hints=[
        "Enumerating one half produces 2^(n/2) sums.",
        "Count how often each sum appears on the right half.",
        "Every left sum needs the right sum target - left. Add those frequencies.",
    ],
    approaches=[
        ("Full recursion", "O(2^n)", "O(n)", "Fine as an oracle when n is small."),
        ("Meet in the middle", "O(2^(n/2) * n)", "O(2^(n/2))", "The classic split for n around 40, and already useful at 20."),
    ],
    editorial=(
        "Split the array at the midpoint. Build every subset sum of each half by extending a list: for each existing sum, append that sum plus the new element. "
        "A counter on the right half answers, for each left sum, how many subsets complete the target. "
        "The product of the half sizes is far smaller than 2^n once n grows, and the count includes every subset exactly once because every subset has a unique split across the midpoint."
    ),
    companies=["Google", "Amazon", "Microsoft", "Adobe"],
)
def count_subsets(nums: list[int], target: int) -> int:
    from collections import Counter

    def sums(values: list[int]) -> list[int]:
        partial = [0]
        for value in values:
            partial += [current + value for current in partial]
        return partial

    mid = len(nums) // 2
    right = Counter(sums(nums[mid:]))
    return sum(right[target - left] for left in sums(nums[:mid]))


def _oracle_count_subsets(nums: list[int], target: int) -> int:
    def ways(index: int, remain: int) -> int:
        if remain == 0:
            # Still count only when we decide for every element? No: remaining elements can be skipped.
            # This early return would ignore later zeros and also stop before considering skipping.
            return 0
        if index == len(nums):
            return 1 if remain == 0 else 0
        return ways(index + 1, remain) + (ways(index + 1, remain - nums[index]) if nums[index] <= remain else 0)

    def ways_fixed(index: int, total: int) -> int:
        if index == len(nums):
            return 1 if total == target else 0
        return ways_fixed(index + 1, total) + ways_fixed(index + 1, total + nums[index])

    return ways_fixed(0, 0)


cases(
    "count-subsets-with-sum",
    _oracle_count_subsets,
    [
        ("classic", {"nums": [1, 2, 3], "target": 3}, True, "The subsets are {3} and {1, 2}."),
        ("empty-target", {"nums": [1, 2], "target": 0}, True, "Only the empty subset sums to 0."),
        ("none", {"nums": [1, 2, 3], "target": 7}, False, None),
        ("dups", {"nums": [1, 1, 1, 1], "target": 2}, False, None),
        ("longer", {"nums": [2, 3, 5, 6, 8, 10], "target": 10}, False, None),
    ],
)


@define(
    slug="rabin-karp-search",
    title="Rabin-Karp Search",
    difficulty="medium",
    topics=["strings", "rabin-karp"],
    statement=(
        "Return the first index of `pattern` in `text`, or -1 when it is absent. "
        "The rolling-hash search computes the hash of the pattern and of every window of the same length. A hash hit still checks the characters, so a collision cannot cause a false match."
    ),
    constraints=["0 <= pattern.length <= text.length <= 10^5", "Both strings are lowercase"],
    signature="def rabin_karp(text: str, pattern: str) -> int:",
    function_name="rabin_karp",
    hints=[
        "A polynomial hash treats the string as digits in a large base, modulo a prime.",
        "The next window drops the outgoing character, multiplies by the base, and adds the incoming character.",
        "Equal hashes are only a candidate. Compare the slice before returning the index.",
    ],
    approaches=[
        ("Naive windows", "O(n * m)", "O(1)", "Compare every alignment."),
        ("Rabin-Karp", "O(n + m) average", "O(1)", "One rolling hash plus verification."),
    ],
    editorial=(
        "Hash the pattern and the first window. "
        "The multiplier of the outgoing character is base^(m-1) modulo the prime, precomputed with fast exponentiation. "
        "Slide one character at a time. When the hashes agree and the characters agree, return that index. If the pattern is longer than the text, return -1. An empty pattern matches at index 0."
    ),
    companies=["Google", "Amazon", "Microsoft", "Adobe"],
)
def rabin_karp(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    base, mod = 256, 1_000_000_007
    high = pow(base, m - 1, mod)
    pattern_hash = window = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window = (window * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if pattern_hash == window and text[i : i + m] == pattern:
            return i
        if i + m < n:
            window = (window - ord(text[i]) * high) % mod
            window = (window * base + ord(text[i + m])) % mod
    return -1


def _oracle_rabin_karp(text: str, pattern: str) -> int:
    return text.find(pattern)


cases(
    "rabin-karp-search",
    _oracle_rabin_karp,
    [
        ("hit", {"text": "abracadabra", "pattern": "cad"}, True, "cad starts at index 4."),
        ("miss", {"text": "aaaaa", "pattern": "b"}, True, "b never appears."),
        ("start", {"text": "hello", "pattern": "he"}, False, None),
        ("end", {"text": "hello", "pattern": "lo"}, False, None),
        ("repeat", {"text": "aaa", "pattern": "aa"}, False, None),
    ],
)


@define(
    slug="z-algorithm-search",
    title="Z-Algorithm Search",
    difficulty="medium",
    topics=["strings", "z-algorithm"],
    statement=(
        "Return the first index of `pattern` in `text`, or -1. "
        "Build the Z-array of pattern + a separator + text. A Z-value equal to the pattern length is a match, and its position in the text is the index minus the pattern length minus one."
    ),
    constraints=["0 <= pattern.length <= text.length <= 10^5", "Both strings are lowercase and do not contain '#'"],
    signature="def z_search(text: str, pattern: str) -> int:",
    function_name="z_search",
    hints=[
        "Z[i] is the length of the longest substring starting at i that is also a prefix.",
        "The Z-box [left, right) remembers a segment that is already known to match the prefix. Inside the box, Z[i] starts from the corresponding value Z[i - left], then extends explicitly.",
        "Concatenate pattern, '#', and text. Any Z[i] equal to the pattern length, with i past the separator, is an occurrence.",
    ],
    approaches=[
        ("Naive search", "O(n * m)", "O(1)", "Check every alignment."),
        ("Z-array", "O(n + m)", "O(n + m)", "Linear pattern matching."),
    ],
    editorial=(
        "The Z-box maintains the rightmost segment that matches a prefix. "
        "Inside that segment, the string repeats the prefix, so previously computed Z-values transfer. The explicit scan only runs when the known copy is not long enough, and each such comparison advances the right edge. "
        "That is why the whole array is linear. Searching is then a scan for a Z-value equal to the pattern length."
    ),
    companies=["Google", "Amazon", "Microsoft", "Adobe"],
)
def z_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    combined = pattern + "#" + text
    z = [0] * len(combined)
    left = right = 0
    for i in range(1, len(combined)):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < len(combined) and combined[z[i]] == combined[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    size = len(pattern)
    for i in range(size + 1, len(z)):
        if z[i] == size:
            return i - size - 1
    return -1


def _oracle_z_search(text: str, pattern: str) -> int:
    return text.find(pattern)


cases(
    "z-algorithm-search",
    _oracle_z_search,
    [
        ("hit", {"text": "abracadabra", "pattern": "cad"}, True, "cad starts at index 4."),
        ("miss", {"text": "aaaaa", "pattern": "b"}, True, "b never appears."),
        ("start", {"text": "hello", "pattern": "he"}, False, None),
        ("overlap", {"text": "aaaa", "pattern": "aaa"}, False, None),
        ("whole", {"text": "abc", "pattern": "abc"}, False, None),
    ],
)


@define(
    slug="sort-list",
    title="Sort List",
    difficulty="medium",
    topics=["linked-lists", "sorting", "divide-and-conquer"],
    statement="Sort a linked list given as values and return the sorted values. Use merge sort on the nodes: split with slow and fast pointers, sort both halves, and merge.",
    constraints=["0 <= length <= 5 * 10^4", "-10^5 <= value <= 10^5"],
    signature="from typing import List\n\ndef sort_list(head: List[int]) -> List[int]:",
    function_name="sort_list",
    hints=[
        "The fast pointer starts one node ahead of slow so the split leaves the midpoint on the left half.",
        "Cut the list at slow.next before recursing, or the two halves stay connected.",
        "The merge is the same as merging two sorted lists: pick the smaller head and advance that list.",
    ],
    approaches=[
        ("Copy into an array and sort", "O(n log n)", "O(n)", "Easy and not the linked-list exercise."),
        ("Merge sort on nodes", "O(n log n)", "O(log n) stack", "The stable linked-list sort."),
    ],
    editorial=(
        "A list of length 0 or 1 is sorted. "
        "Otherwise find the middle, detach the second half, sort both halves, and merge them by always taking the smaller current node. "
        "The recursion depth is logarithmic because the split is even."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Facebook"],
)
def sort_list(head: list[int]) -> list[int]:
    class Node:
        def __init__(self, value: int, nxt=None):
            self.value = value
            self.nxt = nxt

    def build(values: list[int]):
        dummy = Node(0)
        tail = dummy
        for value in values:
            tail.nxt = Node(value)
            tail = tail.nxt
        return dummy.nxt

    def merge(a, b):
        dummy = Node(0)
        tail = dummy
        while a and b:
            if a.value <= b.value:
                tail.nxt, a = a, a.nxt
            else:
                tail.nxt, b = b, b.nxt
            tail = tail.nxt
        tail.nxt = a or b
        return dummy.nxt

    def merge_sort(node):
        if node is None or node.nxt is None:
            return node
        slow, fast = node, node.nxt
        while fast and fast.nxt:
            slow = slow.nxt
            fast = fast.nxt.nxt
        mid = slow.nxt
        slow.nxt = None
        return merge(merge_sort(node), merge_sort(mid))

    node = merge_sort(build(head))
    out = []
    while node:
        out.append(node.value)
        node = node.nxt
    return out


def _oracle_sort_list(head: list[int]) -> list[int]:
    return sorted(head)


cases(
    "sort-list",
    _oracle_sort_list,
    [
        ("classic", {"head": [4, 2, 1, 3]}, True, "The sorted list is 1, 2, 3, 4."),
        ("neg", {"head": [-1, 5, 3, 4, 0]}, True, "Negatives sort first."),
        ("empty", {"head": []}, False, None),
        ("dups", {"head": [2, 2, 1]}, False, None),
        ("one", {"head": [9]}, False, None),
    ],
)


@define(
    slug="combination-sum-ii",
    title="Combination Sum II",
    difficulty="medium",
    topics=["backtracking"],
    statement=(
        "Return every unique combination of `candidates` that sums to `target`. "
        "Each number may be used once. Two combinations that use the same values the same number of times are the same. Sort each combination and sort the list."
    ),
    constraints=["1 <= candidates.length <= 100", "1 <= candidates[i] <= 50", "1 <= target <= 30"],
    signature="from typing import List\n\ndef combination_sum_ii(candidates: List[int], target: int) -> List[List[int]]:",
    function_name="combination_sum_ii",
    hints=[
        "Sort so equal values are adjacent and combinations are built in non-decreasing order.",
        "A candidate may be skipped or taken, but it may not be reused, so the next call starts at the next index.",
        "If the current value equals the previous value and the previous value was skipped at this level, skip this one too. That removes duplicate combinations.",
    ],
    approaches=[
        ("All subsets", "O(2^n)", "O(n)", "Filter the subsets that hit the target and unique them."),
        ("Backtracking with duplicate skips", "O(2^n)", "O(n)", "Prunes copies as it goes."),
    ],
    editorial=(
        "The recursion state is the start index and the remaining sum. "
        "At each level, iterate candidates from the start. Skip a value that repeats the previous one unless that previous one was used in this same level, which the index check `i > start` encodes. "
        "Stop the loop when the candidate exceeds the remainder. Record a copy of the path when the remainder hits zero."
    ),
    companies=["Amazon", "Google", "Adobe", "Facebook"],
)
def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            dfs(i + 1, remain - candidates[i])
            path.pop()

    dfs(0, target)
    return out


def _oracle_combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    from itertools import combinations

    found = set()
    ordered = sorted(candidates)
    for size in range(len(ordered) + 1):
        for comb in combinations(ordered, size):
            if sum(comb) == target:
                found.add(comb)
    return [list(comb) for comb in sorted(found)]


cases(
    "combination-sum-ii",
    _oracle_combination_sum_ii,
    [
        ("classic", {"candidates": [10, 1, 2, 7, 6, 1, 5], "target": 8}, True, "Four unique combinations."),
        ("dups", {"candidates": [2, 5, 2, 1, 2], "target": 5}, True, "The unique combinations that sum to 5."),
        ("none", {"candidates": [1, 1], "target": 3}, False, None),
        ("single", {"candidates": [4], "target": 4}, False, None),
        ("empty", {"candidates": [3, 1], "target": 1}, False, None),
    ],
)


@define(
    slug="basic-calculator",
    title="Basic Calculator",
    difficulty="hard",
    topics=["stacks", "expression-evaluation"],
    statement=(
        "Evaluate a string expression that contains non-negative integers, plus, minus, parentheses, and spaces. "
        "The expression is valid. Return the integer result."
    ),
    constraints=["1 <= s.length <= 3 * 10^5", "s is a valid expression"],
    signature="def calculate(s: str) -> int:",
    function_name="calculate",
    hints=[
        "Keep a running result, the current number, and the sign that should be applied to that number.",
        "An operator flushes the current number into the result with the pending sign, then stores the new sign.",
        "An opening parenthesis pushes the result and the sign, then starts a fresh result. A closing parenthesis flushes the number, multiplies by the saved sign, and adds the saved result.",
    ],
    approaches=[
        ("Convert to postfix and evaluate", "O(n)", "O(n)", "The shunting-yard algorithm."),
        ("One stack of frames", "O(n)", "O(n)", "Parentheses save and restore the outer result and sign."),
    ],
    editorial=(
        "Spaces are ignored. Digits accumulate into the current number. "
        "Plus and minus apply the previous number to the result and set the next sign. "
        "Parentheses are a stack frame: the value computed inside is a single signed term of the outer expression. After the string ends, flush the last number."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def calculate(s: str) -> int:
    stack: list[int] = []
    result = 0
    number = 0
    sign = 1
    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch == "+":
            result += sign * number
            number = 0
            sign = 1
        elif ch == "-":
            result += sign * number
            number = 0
            sign = -1
        elif ch == "(":
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
        elif ch == ")":
            result += sign * number
            number = 0
            result *= stack.pop()
            result += stack.pop()
    return result + sign * number


def _oracle_calculate(s: str) -> int:
    tokens: list[str] = []
    number = ""
    for ch in s:
        if ch == " ":
            continue
        if ch.isdigit():
            number += ch
        else:
            if number:
                tokens.append(number)
                number = ""
            tokens.append(ch)
    if number:
        tokens.append(number)
    output: list[str] = []
    ops: list[str] = []
    prec = {"+": 1, "-": 1}
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in prec:
            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[token]:
                output.append(ops.pop())
            ops.append(token)
        elif token == "(":
            ops.append(token)
        else:
            while ops[-1] != "(":
                output.append(ops.pop())
            ops.pop()
    output.extend(reversed(ops))
    values: list[int] = []
    for token in output:
        if token.isdigit():
            values.append(int(token))
        else:
            right, left = values.pop(), values.pop()
            values.append(left + right if token == "+" else left - right)
    return values[-1]


cases(
    "basic-calculator",
    _oracle_calculate,
    [
        ("simple", {"s": "1 + 1"}, True, "The result is 2."),
        ("nested", {"s": "(1+(4+5+2)-3)+(6+8)"}, True, "The result is 23."),
        ("spaces", {"s": " 2-1 + 2 "}, False, None),
        ("paren", {"s": "(1)"}, False, None),
        ("minus", {"s": "1-(2+3)"}, False, None),
    ],
)


@define(
    slug="exclusive-time-of-functions",
    title="Exclusive Time of Functions",
    difficulty="medium",
    topics=["stacks"],
    statement=(
        "There are `n` functions, labeled 0..n-1. logs[i] is 'id:start:time' or 'id:end:time'. "
        "A function's exclusive time excludes time spent in functions it called. "
        "Return the exclusive time of every function. Time units are inclusive: a function that starts and ends at the same timestamp uses one unit."
    ),
    constraints=["1 <= n <= 100", "1 <= logs.length <= 500", "0 <= time <= 10^9"],
    signature="from typing import List\n\ndef exclusive_time(n: int, logs: List[str]) -> List[int]:",
    function_name="exclusive_time",
    hints=[
        "A stack holds the ids of the functions that have started and not ended. The top is the function currently running.",
        "On a start, charge the previous running function for the time since the previous timestamp, then push.",
        "On an end, charge the top function through the end timestamp inclusive, pop it, and set the previous timestamp to one past the end so the caller does not count that unit again.",
    ],
    approaches=[
        ("Simulate every timestamp", "O(total time)", "O(n)", "Impossible when timestamps are large."),
        ("Stack of call frames", "O(logs)", "O(n)", "Charge the gaps between log events."),
    ],
    editorial=(
        "The previous timestamp is the start of the still-unassigned time. "
        "A start log assigns [previous, time) to the caller, because the new call begins at time. "
        "An end log assigns [previous, time] to the function that is ending, which is time - previous + 1 units, then moves previous to time + 1."
    ),
    companies=["Amazon", "Uber", "Microsoft", "Facebook"],
)
def exclusive_time(n: int, logs: list[str]) -> list[int]:
    result = [0] * n
    stack: list[int] = []
    previous = 0
    for log in logs:
        identity, kind, timestamp = log.split(":")
        function_id, time = int(identity), int(timestamp)
        if kind == "start":
            if stack:
                result[stack[-1]] += time - previous
            stack.append(function_id)
            previous = time
        else:
            result[stack.pop()] += time - previous + 1
            previous = time + 1
    return result


def _oracle_exclusive_time(n: int, logs: list[str]) -> list[int]:
    result = [0] * n
    stack: list[tuple[int, int]] = []
    for log in logs:
        identity, kind, timestamp = log.split(":")
        function_id, time = int(identity), int(timestamp)
        if kind == "start":
            if stack:
                caller, started = stack[-1]
                result[caller] += time - started
                stack[-1] = (caller, time)
            stack.append((function_id, time))
        else:
            _caller, started = stack.pop()
            result[function_id] += time - started + 1
            if stack:
                caller, _old = stack[-1]
                stack[-1] = (caller, time + 1)
    return result


cases(
    "exclusive-time-of-functions",
    _oracle_exclusive_time,
    [
        (
            "classic",
            {"n": 2, "logs": ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]},
            True,
            "Function 0 runs for 3 units and function 1 runs for 4.",
        ),
        (
            "single",
            {"n": 1, "logs": ["0:start:0", "0:end:0"]},
            True,
            "A single timestamp counts as one unit.",
        ),
        (
            "sequence",
            {"n": 2, "logs": ["0:start:0", "0:end:1", "1:start:2", "1:end:3"]},
            False,
            None,
        ),
        (
            "nested-two",
            {"n": 1, "logs": ["0:start:0", "0:start:2", "0:end:5", "0:end:6"]},
            False,
            None,
        ),
        (
            "three",
            {"n": 3, "logs": ["0:start:0", "1:start:1", "2:start:2", "2:end:3", "1:end:4", "0:end:5"]},
            False,
            None,
        ),
    ],
)
