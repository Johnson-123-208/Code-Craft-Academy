"""Graph traversal, topological sort, and shortest-path problems."""

from __future__ import annotations

import heapq
from collections import deque

from lib import cases, define


@define(
    slug="number-of-islands",
    title="Number of Islands",
    difficulty="medium",
    topics=["graphs", "dfs", "bfs", "grid"],
    statement="A grid of '1' (land) and '0' (water) is given as a list of strings. Return the number of islands. An island is a 4-directionally connected group of land cells.",
    constraints=["1 <= m, n <= 300", "grid[i][j] is '0' or '1'"],
    signature="from typing import List\n\ndef num_islands(grid: List[str]) -> int:",
    function_name="num_islands",
    hints=[
        "Every unvisited land cell starts a new island.",
        "DFS or BFS floods the whole island and marks it visited so it is not counted again.",
        "Mutating the grid to water is a valid visited mark when the caller does not need the original grid.",
    ],
    approaches=[
        ("BFS flood", "O(mn)", "O(mn)", "A queue expands each island."),
        ("DFS flood", "O(mn)", "O(mn)", "The recursion or an explicit stack marks the component."),
    ],
    editorial=(
        "Scan every cell. When you see land, increment the island count and flood-fill every land cell reachable in four directions. "
        "Mark visited cells as water so later scans skip them. Each cell is entered a constant number of times, so the algorithm is linear in the number of cells."
    ),
    companies=["Amazon", "Google", "Microsoft", "Bloomberg"],
)
def num_islands(grid: list[str]) -> int:
    board = [list(row) for row in grid]
    rows, cols = len(board), len(board[0])

    def flood(r: int, c: int) -> None:
        stack = [(r, c)]
        board[r][c] = "0"
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] == "1":
                    board[nx][ny] = "0"
                    stack.append((nx, ny))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "1":
                count += 1
                flood(r, c)
    return count


def _oracle_num_islands(grid: list[str]) -> int:
    board = [list(row) for row in grid]
    rows, cols = len(board), len(board[0])
    seen = [[False] * cols for _ in range(rows)]

    def bfs(r: int, c: int) -> None:
        queue = deque([(r, c)])
        seen[r][c] = True
        while queue:
            x, y = queue.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and board[nx][ny] == "1":
                    seen[nx][ny] = True
                    queue.append((nx, ny))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "1" and not seen[r][c]:
                count += 1
                bfs(r, c)
    return count


cases(
    "number-of-islands",
    _oracle_num_islands,
    [
        ("classic", {"grid": ["11110", "11010", "11000", "00000"]}, True, "One island."),
        ("three", {"grid": ["11000", "11000", "00100", "00011"]}, True, "Three islands."),
        ("water", {"grid": ["000", "000"]}, False, None),
        ("single", {"grid": ["1"]}, False, None),
        ("diag", {"grid": ["10", "01"]}, False, None),
    ],
)


@define(
    slug="max-area-of-island",
    title="Max Area of Island",
    difficulty="medium",
    topics=["graphs", "dfs", "grid"],
    statement="Return the area of the largest 4-connected island of 1s in a grid of 0s and 1s. An all-water grid has area 0.",
    constraints=["1 <= m, n <= 50", "grid[i][j] is 0 or 1"],
    signature="from typing import List\n\ndef max_area_of_island(grid: List[List[int]]) -> int:",
    function_name="max_area_of_island",
    hints=[
        "This is number of islands, except you return the size of the component instead of 1.",
        "Count cells as you mark them visited.",
        "Track the maximum count. Zero islands means the answer is 0.",
    ],
    approaches=[
        ("DFS size", "O(mn)", "O(mn)", "Return the number of cells flooded."),
        ("BFS size", "O(mn)", "O(mn)", "Same component, counted with a queue."),
    ],
    editorial=(
        "Flood each unvisited land cell and add one to the area for every cell you mark. "
        "The answer is the maximum area encountered. Marking visited is mandatory, otherwise a cell would be counted by every neighbor."
    ),
    companies=["Amazon", "Google", "Facebook", "Uber"],
)
def max_area_of_island(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    def area(r: int, c: int) -> int:
        stack = [(r, c)]
        seen[r][c] = True
        size = 0
        while stack:
            x, y = stack.pop()
            size += 1
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == 1:
                    seen[nx][ny] = True
                    stack.append((nx, ny))
        return size

    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                best = max(best, area(r, c))
    return best


def _oracle_max_area_of_island(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    def dfs(r: int, c: int) -> int:
        if not (0 <= r < rows and 0 <= c < cols) or seen[r][c] or grid[r][c] == 0:
            return 0
        seen[r][c] = True
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

    return max((dfs(r, c) for r in range(rows) for c in range(cols)), default=0)


cases(
    "max-area-of-island",
    _oracle_max_area_of_island,
    [
        (
            "classic",
            {"grid": [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]},
            True,
            "The largest island has area 6.",
        ),
        ("none", {"grid": [[0, 0, 0], [0, 0, 0]]}, True, "No land."),
        ("one", {"grid": [[1]]}, False, None),
        ("all", {"grid": [[1, 1], [1, 1]]}, False, None),
        ("split", {"grid": [[1, 0, 1], [0, 0, 1]]}, False, None),
    ],
)


@define(
    slug="flood-fill",
    title="Flood Fill",
    difficulty="easy",
    topics=["graphs", "dfs", "grid"],
    statement="Re-color the 4-connected component that contains `(sr, sc)` with `color`. Return the image. If the starting pixel already has that color, return the image unchanged.",
    constraints=["1 <= m, n <= 50", "0 <= image[i][j], color < 2^16"],
    signature="from typing import List\n\ndef flood_fill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:",
    function_name="flood_fill",
    hints=[
        "Remember the original color. Only pixels of that color are recolored.",
        "If the original color equals the new color, stop immediately or you will loop forever.",
        "DFS or BFS from the start pixel is the fill.",
    ],
    approaches=[
        ("DFS", "O(mn)", "O(mn)", "Recolor as you walk."),
        ("BFS", "O(mn)", "O(mn)", "Same component, explicit queue."),
    ],
    editorial=(
        "Capture the starting color. If it already equals the replacement, return. "
        "Otherwise walk every 4-neighbor that still has the starting color and paint it. "
        "Painting before enqueueing prevents a cell from being queued twice."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Apple"],
)
def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    original = image[sr][sc]
    if original == color:
        return image
    rows, cols = len(image), len(image[0])
    stack = [(sr, sc)]
    image[sr][sc] = color
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original:
                image[nr][nc] = color
                stack.append((nr, nc))
    return image


def _oracle_flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    image = [row[:] for row in image]
    original = image[sr][sc]
    if original == color:
        return image
    rows, cols = len(image), len(image[0])
    queue = deque([(sr, sc)])
    image[sr][sc] = color
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original:
                image[nr][nc] = color
                queue.append((nr, nc))
    return image


cases(
    "flood-fill",
    _oracle_flood_fill,
    [
        ("classic", {"image": [[1, 1, 1], [1, 1, 0], [1, 0, 1]], "sr": 1, "sc": 1, "color": 2}, True, "The connected 1s become 2. The corner 1 stays."),
        ("same", {"image": [[0, 0], [0, 0]], "sr": 0, "sc": 0, "color": 0}, True, "The color is unchanged."),
        ("single", {"image": [[1]], "sr": 0, "sc": 0, "color": 9}, False, None),
        ("corner", {"image": [[1, 0], [0, 1]], "sr": 0, "sc": 1, "color": 3}, False, None),
        ("row", {"image": [[2, 2, 2]], "sr": 0, "sc": 1, "color": 1}, False, None),
    ],
)


@define(
    slug="rotting-oranges",
    title="Rotting Oranges",
    difficulty="medium",
    topics=["graphs", "bfs", "grid"],
    statement=(
        "0 is empty, 1 is a fresh orange, and 2 is a rotten orange. Every minute, a rotten orange rots its 4-directional fresh neighbors. "
        "Return the minutes until no fresh orange remains, or -1 if some fresh orange can never rot."
    ),
    constraints=["1 <= m, n <= 10", "grid[i][j] is 0, 1, or 2"],
    signature="from typing import List\n\ndef oranges_rotting(grid: List[List[int]]) -> int:",
    function_name="oranges_rotting",
    hints=[
        "Multi-source BFS: every initially rotten orange is a source at minute 0.",
        "The minute of a cell is one more than the minute of the rotten neighbor that reached it.",
        "If a fresh orange is never reached, return -1. The answer is the maximum minute written on a rotten cell.",
    ],
    approaches=[
        ("Simulate minute by minute", "O(mn * minutes)", "O(mn)", "Scan the whole grid each minute."),
        ("Multi-source BFS", "O(mn)", "O(mn)", "Each cell is enqueued at most once."),
    ],
    editorial=(
        "Enqueue every rotten cell with time 0 and count the fresh cells. "
        "When you rot a fresh neighbor, decrement the fresh count and enqueue it with time + 1. "
        "If fresh remains, return -1. Otherwise return the last time you wrote, which is 0 when there was nothing to rot."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def oranges_rotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, minutes = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, minutes + 1))
    return -1 if fresh else minutes


def _oracle_oranges_rotting(grid: list[list[int]]) -> int:
    grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])
    for minute in range(rows * cols + 1):
        if not any(cell == 1 for row in grid for cell in row):
            return minute
        rot = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            rot.append((nr, nc))
        if not rot:
            return -1
        for r, c in rot:
            grid[r][c] = 2
    return -1


cases(
    "rotting-oranges",
    _oracle_oranges_rotting,
    [
        ("classic", {"grid": [[2, 1, 1], [1, 1, 0], [0, 1, 1]]}, True, "Every fresh orange rots in 4 minutes."),
        ("blocked", {"grid": [[2, 1, 1], [0, 1, 1], [1, 0, 1]]}, True, "The bottom-left orange is isolated."),
        ("none", {"grid": [[0, 2]]}, False, None),
        ("already", {"grid": [[1], [2]]}, False, None),
        ("empty-fresh", {"grid": [[0]]}, False, None),
    ],
)


@define(
    slug="course-schedule",
    title="Course Schedule",
    difficulty="medium",
    topics=["graphs", "topological-sort"],
    statement=(
        "There are `num_courses` courses labeled 0..n-1. `prerequisites[i] = [a, b]` means course b must be taken before course a. "
        "Return true when you can finish every course, which is exactly the statement that the directed graph has no cycle."
    ),
    constraints=["1 <= num_courses <= 2000", "0 <= prerequisites.length <= 5000"],
    signature="from typing import List\n\ndef can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:",
    function_name="can_finish",
    hints=[
        "Model an edge b -> a, meaning b unlocks a. The indegree of a increases.",
        "Kahn's algorithm repeatedly takes a node of indegree 0.",
        "If you process fewer than num_courses nodes, a cycle held the rest at positive indegree.",
    ],
    approaches=[
        ("DFS colors", "O(V + E)", "O(V + E)", "White, gray, and black detect a back edge."),
        ("Kahn indegree", "O(V + E)", "O(V + E)", "A queue of unlocked courses."),
    ],
    editorial=(
        "Build the adjacency list and indegree array. Seed a queue with every course of indegree 0. "
        "Pop a course, count it, and decrement its neighbors. A neighbor that hits 0 is unlocked. "
        "The schedule exists exactly when the count equals the number of courses."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = [i for i in range(num_courses) if indegree[i] == 0]
    seen = 0
    while queue:
        node = queue.pop()
        seen += 1
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return seen == num_courses


def _oracle_can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph = [[] for _ in range(num_courses)]
    for course, pre in prerequisites:
        graph[pre].append(course)
    color = [0] * num_courses

    def dfs(node: int) -> bool:
        if color[node] == 1:
            return False
        if color[node] == 2:
            return True
        color[node] = 1
        if not all(dfs(nxt) for nxt in graph[node]):
            return False
        color[node] = 2
        return True

    return all(dfs(node) for node in range(num_courses))


cases(
    "course-schedule",
    _oracle_can_finish,
    [
        ("yes", {"num_courses": 2, "prerequisites": [[1, 0]]}, True, "Take 0, then 1."),
        ("cycle", {"num_courses": 2, "prerequisites": [[1, 0], [0, 1]]}, True, "The two courses depend on each other."),
        ("none", {"num_courses": 3, "prerequisites": []}, False, None),
        ("chain", {"num_courses": 4, "prerequisites": [[1, 0], [2, 1], [3, 2]]}, False, None),
        ("self", {"num_courses": 1, "prerequisites": [[0, 0]]}, False, None),
    ],
)


@define(
    slug="course-schedule-ii",
    title="Course Schedule II",
    difficulty="medium",
    topics=["graphs", "topological-sort"],
    statement=(
        "Return one valid order in which you can finish every course, using the same prerequisite encoding as Course Schedule. "
        "If several orders exist, return the lexicographically smallest one. If it is impossible, return an empty list."
    ),
    constraints=["1 <= num_courses <= 2000"],
    signature="from typing import List\n\ndef find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:",
    function_name="find_order",
    hints=[
        "Kahn's algorithm produces a topological order if you record nodes as you pop them.",
        "A min-heap, or a sorted list, of indegree-zero nodes makes the order unique.",
        "If the recorded order is shorter than num_courses, return an empty list.",
    ],
    approaches=[
        ("DFS postorder", "O(V + E)", "O(V + E)", "Append a node after its neighbors and reverse the list."),
        ("Kahn with a sorted frontier", "O((V + E) log V)", "O(V + E)", "Always unlock the smallest available course next."),
    ],
    editorial=(
        "The lexicographically smallest topological order is Kahn's algorithm with a min-heap frontier. "
        "Pop the smallest unlocked course, append it, and unlock neighbors whose indegree hits zero. "
        "A cycle leaves some course unprocessed, and the function returns an empty list instead of a partial order."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    ready = [i for i in range(num_courses) if indegree[i] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(ready, nxt)
    return order if len(order) == num_courses else []


def _oracle_find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    ready = sorted(i for i in range(num_courses) if indegree[i] == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        changed = False
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
                changed = True
        if changed:
            ready.sort()
    return order if len(order) == num_courses else []


cases(
    "course-schedule-ii",
    _oracle_find_order,
    [
        ("chain", {"num_courses": 2, "prerequisites": [[1, 0]]}, True, "The only order is 0 then 1."),
        ("free", {"num_courses": 4, "prerequisites": [[1, 0], [2, 0], [3, 1], [3, 2]]}, True, "The smallest order is 0, 1, 2, 3."),
        ("cycle", {"num_courses": 2, "prerequisites": [[0, 1], [1, 0]]}, False, None),
        ("empty", {"num_courses": 3, "prerequisites": []}, False, None),
        ("one", {"num_courses": 1, "prerequisites": []}, False, None),
    ],
)


@define(
    slug="number-of-provinces",
    title="Number of Provinces",
    difficulty="medium",
    topics=["graphs", "dfs", "union-find"],
    statement="`is_connected` is an n by n adjacency matrix of an undirected graph. Return the number of connected components, called provinces.",
    constraints=["1 <= n <= 200", "is_connected[i][i] == 1", "The matrix is symmetric"],
    signature="from typing import List\n\ndef find_circle_num(is_connected: List[List[int]]) -> int:",
    function_name="find_circle_num",
    hints=[
        "DFS or BFS from every unvisited city counts a component.",
        "Union-find unions cities that share an edge and then counts roots.",
        "Skip the diagonal. It is a self-loop, not a new edge.",
    ],
    approaches=[
        ("DFS on the matrix", "O(n^2)", "O(n)", "Each pair is inspected once."),
        ("Disjoint set", "O(n^2)", "O(n)", "Union every edge, then count parents that point at themselves."),
    ],
    editorial=(
        "A province is a connected component. "
        "The DFS version marks a city visited and recurses through every neighbor whose matrix entry is 1. "
        "The number of times you start a search is the number of provinces."
    ),
    companies=["Amazon", "Microsoft", "Google", "Facebook"],
)
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    seen = [False] * n

    def dfs(city: int) -> None:
        seen[city] = True
        for other in range(n):
            if is_connected[city][other] and not seen[other]:
                dfs(other)

    count = 0
    for city in range(n):
        if not seen[city]:
            count += 1
            dfs(city)
    return count


def _oracle_find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                ri, rj = find(i), find(j)
                parent[ri] = rj
    return len({find(i) for i in range(n)})


cases(
    "number-of-provinces",
    _oracle_find_circle_num,
    [
        ("two", {"is_connected": [[1, 1, 0], [1, 1, 0], [0, 0, 1]]}, True, "Cities 0 and 1 are connected. City 2 is alone."),
        ("three", {"is_connected": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}, True, "Three isolated cities."),
        ("one", {"is_connected": [[1]]}, False, None),
        ("all", {"is_connected": [[1, 1], [1, 1]]}, False, None),
        ("chain", {"is_connected": [[1, 1, 0], [1, 1, 1], [0, 1, 1]]}, False, None),
    ],
)


@define(
    slug="redundant-connection",
    title="Redundant Connection",
    difficulty="medium",
    topics=["graphs", "union-find"],
    statement=(
        "An undirected graph started as a tree and then gained one extra edge. "
        "`edges` lists the edges in the order they were added, as pairs of 1-based node ids. "
        "Return the edge that can be removed to restore a tree. If several answers exist, return the one that appears latest in the input."
    ),
    constraints=["3 <= n <= 1000", "edges.length == n", "There is exactly one extra edge"],
    signature="from typing import List\n\ndef find_redundant_connection(edges: List[List[int]]) -> List[int]:",
    function_name="find_redundant_connection",
    hints=[
        "A tree on n nodes has n - 1 edges and no cycle. The extra edge is the one that closes a cycle.",
        "Union-find detects that moment: union fails when both endpoints are already in the same component.",
        "Because you scan in input order, the last failing edge is the one the problem wants.",
    ],
    approaches=[
        ("DFS cycle after each insertion", "O(n^2)", "O(n)", "Rebuild and search."),
        ("Disjoint set", "O(n)", "O(n)", "Nearly constant-time finds with path compression and union by rank."),
    ],
    editorial=(
        "Process edges in order. If find(u) equals find(v), this edge connects two nodes that are already connected, so it is redundant. "
        "Otherwise union them. The problem guarantees exactly one such edge, and the scan order makes it the latest one."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    parent = list(range(len(edges) + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
    raise ValueError("no cycle")


def _oracle_find_redundant_connection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    graph = [[] for _ in range(n + 1)]

    def connected(a: int, b: int) -> bool:
        seen = {a}
        stack = [a]
        while stack:
            node = stack.pop()
            if node == b:
                return True
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return False

    answer = edges[-1]
    for u, v in edges:
        if connected(u, v):
            answer = [u, v]
        else:
            graph[u].append(v)
            graph[v].append(u)
    return answer


cases(
    "redundant-connection",
    _oracle_find_redundant_connection,
    [
        ("classic", {"edges": [[1, 2], [1, 3], [2, 3]]}, True, "The last edge closes the triangle."),
        ("later", {"edges": [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]}, True, "[1, 4] closes the cycle. [1, 5] is a tree edge."),
        ("square", {"edges": [[1, 2], [2, 3], [3, 1]]}, False, None),
        ("tail", {"edges": [[1, 2], [1, 3], [3, 4], [2, 4]]}, False, None),
        ("small", {"edges": [[2, 1], [3, 1], [4, 2], [1, 4]]}, False, None),
    ],
)


@define(
    slug="is-graph-bipartite",
    title="Is Graph Bipartite",
    difficulty="medium",
    topics=["graphs", "bfs"],
    statement=(
        "`graph` is an adjacency list of an undirected graph. Return true when the nodes can be colored with two colors so every edge joins different colors. "
        "The graph may be disconnected."
    ),
    constraints=["1 <= n <= 100", "0 <= graph[u].length < n", "No self-loops or parallel edges"],
    signature="from typing import List\n\ndef is_bipartite(graph: List[List[int]]) -> bool:",
    function_name="is_bipartite",
    hints=[
        "A graph is bipartite exactly when it has no odd cycle.",
        "BFS coloring: color a node 0 and every neighbor 1, then alternate.",
        "A neighbor that already has your color means a conflict. Restart BFS from every uncolored node because the graph may be disconnected.",
    ],
    approaches=[
        ("DFS two-color", "O(V + E)", "O(V)", "The recursion carries the next color."),
        ("BFS two-color", "O(V + E)", "O(V)", "A queue carries the color."),
    ],
    editorial=(
        "Store colors as -1 for uncolored and 0 or 1 for the two sides. "
        "When you first see a node, color it 0 and BFS. Each neighbor must accept the opposite color. "
        "If it already has the opposite color, the edge is fine. If it has the same color, return false."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def is_bipartite(graph: list[list[int]]) -> bool:
    n = len(graph)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if color[nxt] == -1:
                    color[nxt] = color[node] ^ 1
                    queue.append(nxt)
                elif color[nxt] == color[node]:
                    return False
    return True


def _oracle_is_bipartite(graph: list[list[int]]) -> bool:
    n = len(graph)
    color = [-1] * n

    def dfs(node: int, paint: int) -> bool:
        color[node] = paint
        for nxt in graph[node]:
            if color[nxt] == -1:
                if not dfs(nxt, paint ^ 1):
                    return False
            elif color[nxt] == paint:
                return False
        return True

    return all(color[node] != -1 or dfs(node, 0) for node in range(n))


cases(
    "is-graph-bipartite",
    _oracle_is_bipartite,
    [
        ("yes", {"graph": [[1, 3], [0, 2], [1, 3], [0, 2]]}, True, "A square is bipartite."),
        ("no", {"graph": [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]}, True, "A triangle is not bipartite."),
        ("single", {"graph": [[]]}, False, None),
        ("edge", {"graph": [[1], [0]]}, False, None),
        ("odd", {"graph": [[1, 2], [0, 2], [0, 1]]}, False, None),
    ],
)


@define(
    slug="keys-and-rooms",
    title="Keys and Rooms",
    difficulty="medium",
    topics=["graphs", "dfs"],
    statement="`rooms[i]` is the list of keys found in room i. You start in room 0. Return true when you can visit every room.",
    constraints=["1 <= n <= 1000", "0 <= rooms[i][j] < n"],
    signature="from typing import List\n\ndef can_visit_all_rooms(rooms: List[List[int]]) -> bool:",
    function_name="can_visit_all_rooms",
    hints=[
        "This is reachability from node 0 in a directed graph.",
        "A key lets you traverse an edge. Finding the key again does not matter.",
        "Visit a room at most once. Compare the visited count with n.",
    ],
    approaches=[
        ("DFS", "O(n + keys)", "O(n)", "Mark rooms as you enter them."),
        ("BFS", "O(n + keys)", "O(n)", "A queue of newly opened rooms."),
    ],
    editorial=(
        "Start at room 0 with it marked visited. For every key inside a visited room, if that room is new, visit it. "
        "The search ends when no new keys lead anywhere. Success is visiting n rooms."
    ),
    companies=["Amazon", "Google", "Adobe", "Uber"],
)
def can_visit_all_rooms(rooms: list[list[int]]) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if key not in seen:
                seen.add(key)
                stack.append(key)
    return len(seen) == len(rooms)


def _oracle_can_visit_all_rooms(rooms: list[list[int]]) -> bool:
    seen = [False] * len(rooms)

    def dfs(room: int) -> None:
        seen[room] = True
        for key in rooms[room]:
            if not seen[key]:
                dfs(key)

    dfs(0)
    return all(seen)


cases(
    "keys-and-rooms",
    _oracle_can_visit_all_rooms,
    [
        ("yes", {"rooms": [[1], [2], [3], []]}, True, "The keys form a chain."),
        ("no", {"rooms": [[1, 3], [3, 0, 1], [2], [0]]}, True, "Room 2 is locked from the outside and holds its own key."),
        ("one", {"rooms": [[]]}, False, None),
        ("loop", {"rooms": [[1, 2], [2], [1]]}, False, None),
        ("split", {"rooms": [[1], [], [0]]}, False, None),
    ],
)


@define(
    slug="network-delay-time",
    title="Network Delay Time",
    difficulty="medium",
    topics=["graphs", "dijkstra", "shortest-paths"],
    statement=(
        "`times[i] = [u, v, w]` is a directed edge from u to v with travel time w. Nodes are labeled 1..n. "
        "A signal starts at node `k`. Return the time until every node has received it, or -1 if some node is unreachable."
    ),
    constraints=["1 <= n <= 100", "1 <= times.length <= 6000", "1 <= w <= 100"],
    signature="from typing import List\n\ndef network_delay_time(times: List[List[int]], n: int, k: int) -> int:",
    function_name="network_delay_time",
    hints=[
        "This is single-source shortest paths on a graph with positive weights.",
        "Dijkstra with a binary heap computes those distances.",
        "The answer is the maximum finite distance. An infinite distance means return -1.",
    ],
    approaches=[
        ("Bellman-Ford", "O(n * edges)", "O(n)", "Relax every edge n - 1 times. No negative weights, so it is correct."),
        ("Dijkstra", "O((n + edges) log n)", "O(n + edges)", "The right tool for nonnegative weights."),
    ],
    editorial=(
        "Build the adjacency list and a distance array initialized to infinity, with dist[k] = 0. "
        "Pop the closest unsettled node and relax its outgoing edges. A stale heap entry, whose distance does not match the array, is ignored. "
        "The delay is the max distance. If any node is still infinite, the signal never arrives."
    ),
    companies=["Google", "Amazon", "Microsoft", "Akamai"],
)
def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))
    dist = [10**18] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d != dist[node]:
            continue
        for nxt, w in graph[node]:
            if d + w < dist[nxt]:
                dist[nxt] = d + w
                heapq.heappush(heap, (dist[nxt], nxt))
    answer = max(dist[1:])
    return -1 if answer >= 10**18 else answer


def _oracle_network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    dist = [10**18] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    answer = max(dist[1:])
    return -1 if answer >= 10**18 else answer


cases(
    "network-delay-time",
    _oracle_network_delay_time,
    [
        ("classic", {"times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]], "n": 4, "k": 2}, True, "Every node receives the signal by time 2."),
        ("unreachable", {"times": [[1, 2, 1]], "n": 2, "k": 2}, True, "Node 1 never receives a signal that starts at 2."),
        ("direct", {"times": [[1, 2, 5]], "n": 2, "k": 1}, False, None),
        ("choice", {"times": [[1, 2, 1], [1, 3, 4], [2, 3, 1]], "n": 3, "k": 1}, False, None),
        ("single", {"times": [], "n": 1, "k": 1}, False, None),
    ],
)


@define(
    slug="cheapest-flights-within-k-stops",
    title="Cheapest Flights Within K Stops",
    difficulty="medium",
    topics=["graphs", "bellman-ford", "shortest-paths"],
    statement=(
        "`flights[i] = [from, to, price]` is a directed flight. "
        "Return the cheapest price from `src` to `dst` using at most `k` stops. A stop is an intermediate city, so you may use at most k + 1 flights. Return -1 if no such route exists."
    ),
    constraints=["1 <= n <= 100", "0 <= k < n", "1 <= price <= 10^4"],
    signature="from typing import List\n\ndef find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:",
    function_name="find_cheapest_price",
    hints=[
        "Plain Dijkstra by price can take a cheap path with too many stops and then miss a legal path.",
        "Bellman-Ford relaxed for exactly one more edge per round respects the stop limit.",
        "Copy the distance array before a round so a path cannot use more than one new edge in that round.",
    ],
    approaches=[
        ("DFS with pruning", "exponential", "O(k)", "Try every walk of length at most k + 1."),
        ("Bounded Bellman-Ford", "O(k * flights)", "O(n)", "k + 1 rounds of relaxation."),
    ],
    editorial=(
        "Let dist[v] be the cheapest price to reach v with the flights used so far. "
        "Perform k + 1 rounds. In each round, relax every flight against a snapshot of the previous round, so one round adds one flight. "
        "If dst is still infinite, return -1."
    ),
    companies=["Amazon", "Google", "Expedia", "Uber"],
)
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    dist = [10**18] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] >= 10**18 else dist[dst]


def _oracle_find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    graph = [[] for _ in range(n)]
    for u, v, w in flights:
        graph[u].append((v, w))
    best = 10**18
    stack = [(src, 0, 0)]
    while stack:
        node, cost, stops = stack.pop()
        if node == dst:
            best = min(best, cost)
            continue
        if stops > k or cost >= best:
            continue
        for nxt, w in graph[node]:
            stack.append((nxt, cost + w, stops + 1))
    return -1 if best >= 10**18 else best


cases(
    "cheapest-flights-within-k-stops",
    _oracle_find_cheapest_price,
    [
        ("classic", {"n": 4, "flights": [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], "src": 0, "dst": 3, "k": 1}, True, "One stop allows 0-1-3 for 700. The cheaper 0-1-2-3 uses two stops."),
        ("none", {"n": 3, "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]], "src": 0, "dst": 2, "k": 1}, True, "Both the direct flight and the one-stop flight are legal. 200 is cheaper."),
        ("direct", {"n": 2, "flights": [[0, 1, 10]], "src": 0, "dst": 1, "k": 0}, False, None),
        ("blocked", {"n": 3, "flights": [[0, 1, 2]], "src": 0, "dst": 2, "k": 1}, False, None),
        ("zero-stop", {"n": 3, "flights": [[0, 1, 2], [1, 2, 3], [0, 2, 10]], "src": 0, "dst": 2, "k": 0}, False, None),
    ],
)


@define(
    slug="min-cost-to-connect-all-points",
    title="Min Cost to Connect All Points",
    difficulty="medium",
    topics=["graphs", "mst", "prim"],
    statement=(
        "Points are given as [x, y] on the plane. The cost of connecting two points is the Manhattan distance. "
        "Return the minimum cost to connect every point, which is the weight of a minimum spanning tree."
    ),
    constraints=["1 <= points.length <= 1000 on the full problem", "These tests use small n", "-1000 <= x, y <= 1000"],
    signature="from typing import List\n\ndef min_cost_connect_points(points: List[List[int]]) -> int:",
    function_name="min_cost_connect_points",
    hints=[
        "The complete graph is implicit. You do not need to store every edge for Prim.",
        "Prim grows one component. The next edge is the cheapest edge from the component to an outside point.",
        "Manhattan distance is abs(x1 - x2) + abs(y1 - y2).",
    ],
    approaches=[
        ("Kruskal on all pairs", "O(n^2 log n)", "O(n^2)", "Sort every edge and union until one component remains."),
        ("Prim", "O(n^2)", "O(n)", "Dense Prim scans all outside points each step and is optimal for a complete graph."),
    ],
    editorial=(
        "Start from point 0. Keep the cheapest known connection from the tree to every outside point. "
        "Add the outside point with the smallest connection, then update the other outside points with the distance to the newly added point. "
        "The sum of the chosen connections is the MST cost. A single point costs 0."
    ),
    companies=["Amazon", "Google", "Microsoft", "Facebook"],
)
def min_cost_connect_points(points: list[list[int]]) -> int:
    n = len(points)
    in_tree = [False] * n
    best = [10**18] * n
    best[0] = 0
    total = 0
    for _ in range(n):
        u = min((best[i], i) for i in range(n) if not in_tree[i])[1]
        in_tree[u] = True
        total += best[u]
        x, y = points[u]
        for v in range(n):
            if not in_tree[v]:
                dist = abs(points[v][0] - x) + abs(points[v][1] - y)
                best[v] = min(best[v], dist)
    return total


def _oracle_min_cost_connect_points(points: list[list[int]]) -> int:
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((dist, i, j))
    edges.sort()
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = used = 0
    for dist, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += dist
            used += 1
            if used == n - 1:
                break
    return total


cases(
    "min-cost-to-connect-all-points",
    _oracle_min_cost_connect_points,
    [
        ("classic", {"points": [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]}, True, "The MST costs 20."),
        ("line", {"points": [[3, 12], [-2, 5], [-4, 1]]}, True, "The MST costs 18."),
        ("one", {"points": [[0, 0]]}, False, None),
        ("two", {"points": [[0, 0], [1, 2]]}, False, None),
        ("square", {"points": [[0, 0], [0, 1], [1, 0], [1, 1]]}, False, None),
    ],
)


@define(
    slug="shortest-path-in-binary-matrix",
    title="Shortest Path in Binary Matrix",
    difficulty="medium",
    topics=["graphs", "bfs", "grid"],
    statement=(
        "In an n by n binary grid, 0 is open and 1 is blocked. "
        "Return the length of the shortest clear path from (0, 0) to (n - 1, n - 1). You may move to any of the eight neighbors. Return -1 if the path does not exist. A path length counts cells, including both ends."
    ),
    constraints=["1 <= n <= 100", "grid[i][j] is 0 or 1"],
    signature="from typing import List\n\ndef shortest_path_binary_matrix(grid: List[List[int]]) -> int:",
    function_name="shortest_path_binary_matrix",
    hints=[
        "Unweighted grid movement is BFS, not Dijkstra.",
        "Eight directions include the diagonals.",
        "If either corner is blocked, return -1 before searching. Mark cells visited when you enqueue them.",
    ],
    approaches=[
        ("DFS", "exponential without memo", "O(n^2)", "DFS does not give the shortest path in an unweighted graph unless you explore every walk."),
        ("BFS", "O(n^2)", "O(n^2)", "The first time you reach the corner is optimal."),
    ],
    editorial=(
        "BFS layers are distances in an unweighted graph. "
        "Start at the top-left with distance 1 if it is open. Expand all eight neighbors that are open and unvisited. "
        "The distance stored when you first reach the bottom-right is the answer."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    queue = deque([(0, 0, 1)])
    grid[0][0] = 1
    while queue:
        r, c, dist = queue.popleft()
        if r == n - 1 and c == n - 1:
            return dist
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    queue.append((nr, nc, dist + 1))
    return -1


def _oracle_shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] or grid[-1][-1]:
        return -1
    seen = {(0, 0)}
    queue = deque([(0, 0, 1)])
    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == (n - 1, n - 1):
            return dist
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    return -1


cases(
    "shortest-path-in-binary-matrix",
    _oracle_shortest_path_binary_matrix,
    [
        ("classic", {"grid": [[0, 1], [1, 0]]}, True, "The diagonal path has length 2."),
        ("blocked", {"grid": [[0, 0, 0], [1, 1, 0], [1, 1, 0]]}, True, "The clear path has length 4."),
        ("start-blocked", {"grid": [[1, 0], [0, 0]]}, False, None),
        ("one", {"grid": [[0]]}, False, None),
        ("none", {"grid": [[0, 1], [1, 1]]}, False, None),
    ],
)


@define(
    slug="01-matrix",
    title="01 Matrix",
    difficulty="medium",
    topics=["graphs", "bfs", "grid"],
    statement="Given a binary matrix, return a matrix of the same size where each cell is the distance to the nearest 0. Distance is 4-directional.",
    constraints=["1 <= m, n <= 10^4 cells total", "There is at least one 0"],
    signature="from typing import List\n\ndef update_matrix(mat: List[List[int]]) -> List[List[int]]:",
    function_name="update_matrix",
    hints=[
        "Searching outward from every 1 repeats work.",
        "Multi-source BFS from every 0 assigns distances in increasing order.",
        "Initialize 0-cells to distance 0 and 1-cells to infinity, then relax neighbors.",
    ],
    approaches=[
        ("BFS from each 1", "O((mn)^2)", "O(mn)", "Too slow when the matrix is large."),
        ("Multi-source BFS", "O(mn)", "O(mn)", "Each cell is dequeued once."),
    ],
    editorial=(
        "Enqueue every 0 with distance 0. A 1 starts at infinity and is not a source. "
        "When you dequeue a cell, each in-bounds neighbor whose stored distance is larger than yours plus one gets updated and enqueued. "
        "Because edges have length 1, the first time a cell is set is its final distance."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    rows, cols = len(mat), len(mat[0])
    dist = [[10**9] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] > dist[r][c] + 1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


def _oracle_update_matrix(mat: list[list[int]]) -> list[list[int]]:
    rows, cols = len(mat), len(mat[0])
    zeros = [(r, c) for r in range(rows) for c in range(cols) if mat[r][c] == 0]
    return [[min(abs(r - zr) + abs(c - zc) for zr, zc in zeros) for c in range(cols)] for r in range(rows)]


cases(
    "01-matrix",
    _oracle_update_matrix,
    [
        ("classic", {"mat": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]}, True, "The center is distance 1 from a zero."),
        ("row", {"mat": [[0, 0, 0], [0, 1, 0], [1, 1, 1]]}, True, "Distances grow away from the zeros."),
        ("one", {"mat": [[0]]}, False, None),
        ("column", {"mat": [[0], [1], [1]]}, False, None),
        ("corners", {"mat": [[1, 0], [0, 1]]}, False, None),
    ],
)


@define(
    slug="all-paths-from-source-to-target",
    title="All Paths From Source to Target",
    difficulty="medium",
    topics=["graphs", "backtracking", "dfs"],
    statement=(
        "`graph` is a directed acyclic graph as an adjacency list. Nodes are 0..n-1. "
        "Return every path from 0 to n - 1, sorted lexicographically."
    ),
    constraints=["2 <= n <= 15", "The graph is a DAG"],
    signature="from typing import List\n\ndef all_paths_source_target(graph: List[List[int]]) -> List[List[int]]:",
    function_name="all_paths_source_target",
    hints=[
        "DFS from 0, carrying the path.",
        "When you reach n - 1, copy the path into the answer.",
        "Backtrack by popping the node so sibling edges can reuse the prefix. A DAG needs no visited set.",
    ],
    approaches=[
        ("BFS storing full paths", "O(2^n * n)", "O(2^n * n)", "Each path is a queue item."),
        ("DFS backtracking", "O(2^n * n)", "O(n)", "The output size dominates. The recursion depth is n."),
    ],
    editorial=(
        "The absence of cycles means a walk never repeats a node, so you do not need a seen set. "
        "Append the current node, recurse to each neighbor, and pop. "
        "Record a copy when the current node is the target. Sort the collected paths so the answer is unique."
    ),
    companies=["Amazon", "Google", "Facebook", "Bloomberg"],
)
def all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    target = len(graph) - 1
    out: list[list[int]] = []
    path = [0]

    def dfs(node: int) -> None:
        if node == target:
            out.append(path[:])
            return
        for nxt in graph[node]:
            path.append(nxt)
            dfs(nxt)
            path.pop()

    dfs(0)
    out.sort()
    return out


def _oracle_all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    target = len(graph) - 1
    out: list[list[int]] = []
    stack = [(0, [0])]
    while stack:
        node, path = stack.pop()
        if node == target:
            out.append(path)
            continue
        for nxt in reversed(graph[node]):
            stack.append((nxt, path + [nxt]))
    out.sort()
    return out


cases(
    "all-paths-from-source-to-target",
    _oracle_all_paths_source_target,
    [
        ("classic", {"graph": [[1, 2], [3], [3], []]}, True, "The two paths are 0-1-3 and 0-2-3."),
        ("chain", {"graph": [[1], [2], []]}, True, "One path."),
        ("branch", {"graph": [[4, 3, 1], [3, 2, 4], [3], [4], []]}, False, None),
        ("direct", {"graph": [[1], []]}, False, None),
        ("two-step", {"graph": [[1, 2], [2], []]}, False, None),
    ],
)


@define(
    slug="pacific-atlantic-water-flow",
    title="Pacific Atlantic Water Flow",
    difficulty="medium",
    topics=["graphs", "dfs", "grid"],
    statement=(
        "Heights is an m by n grid. Water flows from a cell to a neighbor of equal or lower height. "
        "The Pacific touches the top and left borders. The Atlantic touches the bottom and right borders. "
        "Return every cell that can flow to both oceans, sorted by row and then column, as [row, col] pairs."
    ),
    constraints=["1 <= m, n <= 200", "0 <= heights[r][c] <= 10^5"],
    signature="from typing import List\n\ndef pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:",
    function_name="pacific_atlantic",
    hints=[
        "Flowing downhill from every cell is a search per cell.",
        "Reverse the edges: start at the ocean border and walk uphill, to cells of equal or greater height.",
        "A cell reachable by both uphill searches can reach both oceans.",
    ],
    approaches=[
        ("DFS from each cell", "O((mn)^2)", "O(mn)", "Stop at a border of each ocean."),
        ("Two reverse floods", "O(mn)", "O(mn)", "One flood from Pacific borders, one from Atlantic borders."),
    ],
    editorial=(
        "Mark Pacific-reachable cells by DFS from the first row and first column, moving only to neighbors whose height is at least the current height. "
        "Do the same for the Atlantic from the last row and last column. "
        "The intersection, read in row-major order, is the answer."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    rows, cols = len(heights), len(heights[0])
    pacific = [[False] * cols for _ in range(rows)]
    atlantic = [[False] * cols for _ in range(rows)]

    def flood(r: int, c: int, seen: list[list[bool]]) -> None:
        seen[r][c] = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and heights[nr][nc] >= heights[r][c]:
                flood(nr, nc, seen)

    for r in range(rows):
        flood(r, 0, pacific)
        flood(r, cols - 1, atlantic)
    for c in range(cols):
        flood(0, c, pacific)
        flood(rows - 1, c, atlantic)
    return [[r, c] for r in range(rows) for c in range(cols) if pacific[r][c] and atlantic[r][c]]


def _oracle_pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    rows, cols = len(heights), len(heights[0])

    def reaches(r: int, c: int) -> tuple[bool, bool]:
        seen = {(r, c)}
        stack = [(r, c)]
        pacific = atlantic = False
        while stack:
            x, y = stack.pop()
            if x == 0 or y == 0:
                pacific = True
            if x == rows - 1 or y == cols - 1:
                atlantic = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dr, y + dc
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in seen and heights[nx][ny] <= heights[x][y]:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        return pacific, atlantic

    return [[r, c] for r in range(rows) for c in range(cols) if all(reaches(r, c))]


cases(
    "pacific-atlantic-water-flow",
    _oracle_pacific_atlantic,
    [
        (
            "classic",
            {"heights": [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]},
            True,
            "Seven cells reach both oceans.",
        ),
        ("one", {"heights": [[1]]}, True, "A single cell touches both oceans."),
        ("row", {"heights": [[1, 2, 3]]}, False, None),
        ("flat", {"heights": [[2, 2], [2, 2]]}, False, None),
        ("col", {"heights": [[1], [2], [3]]}, False, None),
    ],
)


@define(
    slug="surrounded-regions",
    title="Surrounded Regions",
    difficulty="medium",
    topics=["graphs", "dfs", "grid"],
    statement=(
        "A board of 'X' and 'O' is given as a list of strings. Capture every region of 'O' that is 4-connected and completely surrounded by 'X'. "
        "A region that touches the border is not captured. Return the board as a list of strings."
    ),
    constraints=["1 <= m, n <= 200"],
    signature="from typing import List\n\ndef solve(board: List[str]) -> List[str]:",
    function_name="solve",
    hints=[
        "Do not search for surrounded regions directly. Search for the regions that escape.",
        "Any 'O' on the border, and anything connected to it, survives.",
        "Mark those cells, flip every unmarked 'O' to 'X', and restore the marks to 'O'.",
    ],
    approaches=[
        ("DFS from every O", "O((mn)^2)", "O(mn)", "Check whether the component touches the border."),
        ("Border flood", "O(mn)", "O(mn)", "One flood from the border, then one rewrite pass."),
    ],
    editorial=(
        "Flood from every border O and mark the reachable O cells as temporary safe cells. "
        "Then scan the board: an O becomes X, and a safe mark becomes O again. "
        "X cells never change. This captures exactly the components with no border cell."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def solve(board: list[str]) -> list[str]:
    grid = [list(row) for row in board]
    rows, cols = len(grid), len(grid[0])

    def flood(r: int, c: int) -> None:
        stack = [(r, c)]
        grid[r][c] = "S"
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "O":
                    grid[nx][ny] = "S"
                    stack.append((nx, ny))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "O" and (r in (0, rows - 1) or c in (0, cols - 1)):
                flood(r, c)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "O":
                grid[r][c] = "X"
            elif grid[r][c] == "S":
                grid[r][c] = "O"
    return ["".join(row) for row in grid]


def _oracle_solve(board: list[str]) -> list[str]:
    grid = [list(row) for row in board]
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    def component(r: int, c: int):
        cells = []
        stack = [(r, c)]
        seen[r][c] = True
        border = False
        while stack:
            x, y = stack.pop()
            cells.append((x, y))
            border = border or x in (0, rows - 1) or y in (0, cols - 1)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == "O":
                    seen[nx][ny] = True
                    stack.append((nx, ny))
        return cells, border

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "O" and not seen[r][c]:
                cells, border = component(r, c)
                if not border:
                    for x, y in cells:
                        grid[x][y] = "X"
    return ["".join(row) for row in grid]


cases(
    "surrounded-regions",
    _oracle_solve,
    [
        ("classic", {"board": ["XXXX", "XOOX", "XXOX", "XOXX"]}, True, "The center region is captured. The border O survives."),
        ("none", {"board": ["X"]}, True, "A single X stays."),
        ("border", {"board": ["OO", "OO"]}, False, None),
        ("inside", {"board": ["XXX", "XOX", "XXX"]}, False, None),
        ("row", {"board": ["XOX"]}, False, None),
    ],
)


@define(
    slug="word-ladder",
    title="Word Ladder",
    difficulty="hard",
    topics=["graphs", "bfs"],
    statement=(
        "Begin at `begin_word` and change one letter at a time. Every intermediate word must be in `word_list`. "
        "Return the number of words in the shortest transformation to `end_word`, counting both ends. Return 0 when no sequence exists."
    ),
    constraints=["1 <= beginWord.length <= 10", "1 <= wordList.length <= 5000", "All words share that length"],
    signature="from typing import List\n\ndef ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:",
    function_name="ladder_length",
    hints=[
        "This is an unweighted graph. An edge joins words at Hamming distance 1. BFS gives the shortest path.",
        "If the end word is not in the list, return 0.",
        "Generating all one-letter neighbors from the alphabet is faster than comparing every pair when the list is long. For short tests either method is fine.",
    ],
    approaches=[
        ("Compare every pair", "O(n^2 * word length)", "O(n)", "Build the graph explicitly, then BFS."),
        ("Wildcard buckets or alphabet expansion", "O(n * length * alphabet)", "O(n * length)", "BFS without a quadratic graph build."),
    ],
    editorial=(
        "Put the word list in a set. BFS from the begin word with distance 1. "
        "For each word, try changing every position to every letter. If the new word is in the set, enqueue it with distance + 1 and delete it so it is not visited twice. "
        "The first time you generate the end word, return that distance."
    ),
    companies=["Amazon", "Google", "Facebook", "LinkedIn"],
)
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    queue = deque([(begin_word, 1)])
    words.discard(begin_word)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    while queue:
        word, dist = queue.popleft()
        for i in range(len(word)):
            for ch in alphabet:
                nxt = word[:i] + ch + word[i + 1 :]
                if nxt == end_word:
                    return dist + 1
                if nxt in words:
                    words.remove(nxt)
                    queue.append((nxt, dist + 1))
    return 0


def _oracle_ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    queue = deque([(begin_word, 1)])
    seen = {begin_word}
    while queue:
        word, dist = queue.popleft()
        if word == end_word:
            return dist
        for other in list(words):
            if other not in seen and sum(a != b for a, b in zip(word, other)) == 1:
                seen.add(other)
                queue.append((other, dist + 1))
    return 0


cases(
    "word-ladder",
    _oracle_ladder_length,
    [
        ("classic", {"begin_word": "hit", "end_word": "cog", "word_list": ["hot", "dot", "dog", "lot", "log", "cog"]}, True, "hit-hot-dot-dog-cog has length 5."),
        ("missing", {"begin_word": "hit", "end_word": "cog", "word_list": ["hot", "dot", "dog", "lot", "log"]}, True, "cog is not in the list."),
        ("same", {"begin_word": "a", "end_word": "c", "word_list": ["a", "b", "c"]}, False, None),
        ("direct", {"begin_word": "hot", "end_word": "dot", "word_list": ["dot"]}, False, None),
        ("none", {"begin_word": "ab", "end_word": "cd", "word_list": ["cd"]}, False, None),
    ],
)
