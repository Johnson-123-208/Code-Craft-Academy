"""BFS, DFS, grids, and topological sort."""

from emit import emit

BFS = r'''
## Why this matters

Graphs are how you model anything whose parts touch: cities and roads, courses and prerequisites, pixels and their neighbors, accounts and shared emails. Depth-first search and breadth-first search are the two walks that every later algorithm specializes. BFS finds shortest paths when every edge has the same cost. DFS finds connectivity, cycles, and finishing times. On a grid, the "graph" is implicit: a cell has up to four neighbors and you must not allocate an adjacency list unless you want to. Island counts, flood fill, rotting oranges, and walls-and-gates are BFS or DFS with a visited mark. If the mark is missing, the search never ends.

## Intuition

DFS is a person in a maze who walks as far as possible down one corridor before backtracking. The call stack, or an explicit stack, remembers the corridors not yet taken. BFS is a ripple. Everyone who is one step away is processed before anyone who is two steps away. A queue enforces that order. On an unweighted graph the ripple reaches a node by a shortest path, because a shorter path would have been a smaller ripple that arrived earlier. On a weighted graph that argument dies, and you need Dijkstra or Bellman-Ford.

## Core concept in depth

Represent a graph as an adjacency list: a vector of vectors, or a dictionary from node to neighbors. An undirected edge is stored twice. A directed edge is stored once. A grid does not need that list. The neighbors of a cell are the four, or eight, coordinate offsets that stay inside the board.

DFS from a start node marks the node visited, then explores each unvisited neighbor. The recursive version is the specification. The iterative version pushes the start, and when it pops a node it pushes the unvisited neighbors. Marking on push avoids putting the same node on the stack many times. Marking on pop matches the recursive timing more closely and can still explode the stack with duplicates if you are not careful. Prefer mark-on-push for iterative DFS. Time is Theta(n + m) for n nodes and m edges, because each node is expanded once and each edge is looked at once. Space is Theta(n) for the visited set and the stack. In a recursion, the call stack can be depth n. Python will hit the recursion limit on a long chain. Use the explicit stack when the problem constraints allow a chain of 10 to the 5th nodes.

BFS pushes the start with distance 0 and marks it visited immediately, not when it is dequeued. That mark-on-enqueue rule is the difference between linear time and a queue that contains the same node once per path. While the queue is not empty, pop the front, and enqueue each unvisited neighbor with distance plus one, marking it as you enqueue. The first time a node is enqueued is the shortest unweighted distance. Multi-source BFS puts every source in the queue at distance 0 before the loop. Rotting oranges is multi-source: every rotten orange is a source, and the answer is the maximum distance at which a fresh orange becomes rotten, or a failure if a fresh orange was never reached. 0-1 BFS is the variant where edges cost 0 or 1. Use a deque. A 0-cost edge pushes to the front and a 1-cost edge pushes to the back. The first time you pop a node, its distance is final. It is a special case of Dijkstra that does not need a heap.

Connected components in an undirected graph are the nodes reached by one DFS or BFS. Loop over every node, and start a search when it is unvisited. The number of starts is the number of components. On a grid, an island is a component of land cells. Count the starts, and let the search mark the whole island so it is not counted again. Flood fill is the same search that writes a new color instead of only marking. Max area is the same search that returns a size. Surrounded regions and enclaves are a search that starts from the border, marks everything that can escape, and then treats the unmarked land as trapped.

Bipartite checking is a BFS or DFS that colors a node 0 and its neighbors 1, and fails when a neighbor is already the same color. A graph is bipartite exactly when it has no odd cycle. Disconnected graphs need a start from every unvisited node. A single node is bipartite.

Cycle detection differs by directed and undirected. Undirected: DFS with a parent. A visited neighbor that is not the parent is a back edge to an ancestor or a cross edge inside the component, and in an undirected graph that means a cycle. Directed: three colors. White is unseen, gray is on the current recursion stack, black is finished. A gray neighbor is a back edge and a cycle. A black neighbor is a cross edge or a forward edge and is not, by itself, a cycle. Forgetting the parent in the undirected case reports every edge as a cycle, because the search walks back to the node it just came from.

Iterative and recursive DFS compute the same reachability. They do not always visit neighbors in the same order, and an iterative version that pushes neighbors left to right will pop them right to left. If the problem wants a specific order, sort the neighbors or use recursion and document the order. BFS order is fixed once the neighbor order is fixed: increasing distance, and within a distance the enqueue order.

## Diagram and dry run

```mermaid
flowchart TD
    A[Enqueue the source and mark it] --> B{Queue empty?}
    B -->|No| C[Dequeue v]
    C --> D[Enqueue unmarked neighbors and mark them]
    D --> B
    B -->|Yes| E[Distances are shortest in hops]
```

Undirected graph. Nodes 0, 1, 2, 3. Edges 0-1, 0-2, 1-3. BFS from 0.

| Dequeue | Queue after enqueueing new nodes | Distances |
| --- | --- | --- |
| start | 0 | 0 is 0 |
| 0 | 1, 2 | 1 is 1, 2 is 1 |
| 1 | 2, 3 | 3 is 2 |
| 2 | 3 | no new node |
| 3 | empty | done |

The shortest path from 0 to 3 has length 2. DFS from 0 might visit 0, 1, 3, 2 if it walks the 1 edge first. Both see the whole component. Only BFS reports the hop distance.

A grid island example. Three land cells in a corner and one isolated land cell. The first land cell you meet starts a search that marks three cells. The isolated cell starts a second search. The answer is 2. If you forget to mark, the first search oscillates between two adjacent land cells forever.

## Runnable Python

Recursive DFS and iterative BFS are the pair to keep. The grid island counter uses BFS so the recursion limit is irrelevant. Neighbors are four-directional.

```python
def dfs(graph: list[list[int]], start: int) -> list[int]:
    seen = [False] * len(graph)
    order: list[int] = []

    def visit(node: int) -> None:
        seen[node] = True
        order.append(node)
        for nxt in graph[node]:
            if not seen[nxt]:
                visit(nxt)

    visit(start)
    return order


def bfs(graph: list[list[int]], start: int) -> list[int]:
    from collections import deque
    seen = [False] * len(graph)
    seen[start] = True
    queue = deque([start])
    dist = [-1] * len(graph)
    dist[start] = 0
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if not seen[nxt]:
                seen[nxt] = True
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist


def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    def flood(r: int, c: int) -> None:
        stack = [(r, c)]
        seen[r][c] = True
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == "1":
                    seen[nx][ny] = True
                    stack.append((nx, ny))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not seen[r][c]:
                flood(r, c)
                count += 1
    return count
```

`bfs` returns hop distances, with -1 for unreachable nodes. `num_islands` treats the character 1 as land. Marking when you push, including the start, is what keeps the stack linear in the size of the island rather than exponential in the number of paths.

## Complexity and trade-offs

| Search | Time | Extra space | Shortest paths |
| --- | --- | --- | --- |
| Recursive DFS | Theta(n + m) | Theta(n) stack in the worst case | no |
| Iterative DFS | Theta(n + m) | Theta(n) | no |
| BFS | Theta(n + m) | Theta(n) queue | yes, unweighted |
| 0-1 BFS | Theta(n + m) | Theta(n) | yes, weights 0 and 1 |
| Multi-source BFS | Theta(n + m) | Theta(n) | yes, distance to the nearest source |

DFS uses less memory than BFS on a long thin path if you count only the recursion depth against a wide BFS frontier, and the opposite on a balanced graph where the frontier is wide and the depth is small. For correctness of shortest paths, use BFS. For topological finishing times and directed cycles, use DFS colors. For grids, either search is fine for connectivity. BFS is required when the answer is a distance.

## Tricks, tips, and patterns

Mark on the way in, not on the way out. For BFS, mark when you enqueue. For undirected cycles, remember the parent. For directed cycles, gray means on the stack. For grids, check bounds before you read the cell. For multi-source problems, enqueue every source first. For "minimum steps to a target" on an unweighted implicit graph, BFS and stop when you dequeue the target. The open-the-lock puzzle is that graph: 10000 nodes, eight edges each, and deadends removed. Do not build the adjacency list in advance. Generate neighbors from the current state.

## Common mistakes and edge cases

Forgetting the parent and reporting a cycle on every undirected edge. Marking a grid cell only after exploring it, so two paths enqueue it twice and the distance is still correct but the time is not linear. Using DFS distances as shortest paths. Using BFS on weighted edges. Eight-directional versus four-directional neighbors. A grid of all water has zero islands. A one-cell island counts. Disconnected graphs: a search from node 0 does not cover node 5. Loop over all starts. Directed reachability is not symmetric. A self-loop is a cycle. An empty graph has zero components or one component per the problem's definition of n. Read n. Python recursion on a snake-shaped island of length 10 to the 5th. Use a stack.

## Interview notes

Say which search and why in one sentence. "Unweighted distance, so BFS, mark on enqueue." Or "connectivity, DFS, and I will use a stack because the island can be long." Name the graph. For a grid, say the nodes are cells and the edges are the four steps. Dry-run a four-node graph or a 2 by 2 grid. Mention the n + m bound. If the interviewer adds weights, stop and switch algorithms. Do not quietly keep the BFS.

## Practice problems

1. [Number of Islands](/practice/number-of-islands), [Max Area of Island](/practice/max-area-of-island), and [Flood Fill](/practice/flood-fill).
2. [Rotting Oranges](/practice/rotting-oranges) — multi-source BFS.
3. [01 Matrix](/practice/01-matrix) and [Shortest Path in a Binary Matrix](/practice/shortest-path-in-binary-matrix).
4. [Number of Enclaves](/practice/number-of-enclaves) and [Pacific Atlantic Water Flow](/practice/pacific-atlantic-water-flow) — searches from the border.
5. [Is Graph Bipartite](/practice/is-graph-bipartite) and [Keys and Rooms](/practice/keys-and-rooms).
6. [Open the Lock](/practice/open-the-lock) — BFS on an implicit graph.

## Summary and cheat sheet

- DFS goes deep. BFS goes level by level. Both are linear in nodes plus edges.
- BFS gives shortest paths only when every edge has the same positive cost, usually 1.
- Mark when you push. In BFS that is when you enqueue.
- Undirected cycles: a visited neighbor that is not the parent. Directed cycles: a gray node.
- Grids are implicit graphs. Check bounds. Choose four or eight neighbors on purpose.
- Multi-source BFS enqueues every source at distance 0.
- 0-1 BFS uses a deque. Real weights need Dijkstra.

## Further reading

- [Wikipedia — Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Wikipedia — Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
- [CP-Algorithms, BFS](https://cp-algorithms.com/graph/breadth-first-search.html)
- [CP-Algorithms, DFS](https://cp-algorithms.com/graph/depth-first-search.html)
'''

TOPO = r'''
## Why this matters

Some graphs are schedules. An edge u to v means u must happen before v: a course before its follow-up, a build step before the binary that links it, a spreadsheet cell before the cell that reads it. A topological order is a linear order that respects every edge. It exists exactly when the directed graph has no cycle. Kahn's algorithm finds one with a queue of indegree-zero nodes, or proves a cycle by failing to output every node. DFS finds one by reversing the finishing times, and the same search's gray edges prove a cycle. Course Schedule is the decision version. Course Schedule II is the order. Eventual safe nodes and alien dictionary are the same idea in a costume.

## Intuition

A node that nobody depends on, or that has no prerequisites left, can go next. Taking it removes its outgoing edges and may free other nodes. If you can keep doing that until the graph is empty, you have a valid order. If you get stuck while nodes remain, those nodes all have a prerequisite still in the stuck set, which means a cycle. DFS says the same thing from the other end. A node finishes when everything it points at is already finished. Listing nodes in reverse finishing order puts dependencies first.

## Core concept in depth

A directed acyclic graph, a DAG, is a directed graph with no directed cycle. A topological order is a permutation of the nodes such that for every edge u to v, u appears before v. A DAG always has at least one. A graph with a directed cycle has none, because the cycle's nodes cannot all precede each other.

Kahn's algorithm computes indegrees. Every node with indegree 0 enters a queue. While the queue is not empty, pop a node, append it to the order, and decrement the indegree of each neighbor. A neighbor that falls to 0 enters the queue. If the order contains n nodes, it is a topological order. If not, the remaining nodes form a cycle. The queue can be a stack or a priority queue. A plain queue gives the order of discovery. A min-heap gives the lexicographically smallest order among topological orders, because you always take the smallest ready node. Time is Theta(n + m). Space is Theta(n) for indegrees and the queue.

DFS topological sort uses the three colors from the cycle lesson. A recursive visit marks the node gray, visits unvisited neighbors, and on the way out marks it black and pushes it onto a finishing stack. If a neighbor is gray, there is a cycle and you abort. After every node has been started, the finishing stack from top to bottom is a topological order: a node is pushed after its descendants, so popping reverses that. Iterative DFS can compute the same finishing times if you record a node when all its edges have been explored, which means the stack frame must remember the next edge index. The recursive form is shorter when the depth is safe. For n up to 10 to the 5th, an explicit stack or Kahn's algorithm is safer in Python.

Both algorithms detect cycles. Kahn's detection is "I could not schedule everyone." DFS detection is "I saw a gray node." Use Kahn when you want the order and the cycle test together with simple code. Use DFS when you are already coloring the graph for another reason, such as strongly connected components. Tarjan's and Kosaraju's algorithms for strongly connected components are the directed-graph refinement of this coloring. A condensation of a directed graph, one node per strongly connected component, is always a DAG, and the topological order of the condensation is the order of components. You do not need to code Tarjan's SCC for a first course-schedule problem. You should know the term if the interviewer asks what remains after you contract cycles.

Course Schedule builds the graph from prerequisite pairs. Be careful which way the edge points. If the pair means "to take a you need b," the edge is b to a, and b has to appear first. Reversing every edge reverses the order and still works if you reverse your reading of the output. Inconsistent direction is a silent wrong answer. Course Schedule II returns any valid order, or a specified one. If any order is accepted, Kahn's queue order is fine. If the smallest lexicographic order is required, use a min-heap of ready nodes.

Eventual safe nodes are nodes from which every path ends at a terminal node, which means no path reaches a cycle. That is a topological question on the reverse graph, or a DFS color: a node is safe when every neighbor is safe. A gray neighbor means this node reaches a cycle and is unsafe. Memoize the answer so each node is decided once.

A graph that is a tree, in the undirected sense, has n - 1 edges and is connected, which you can test with DFS or with a union-find structure. The union-find version belongs with the MST lesson. Topological order is a directed notion. Do not topologically sort an undirected graph. The undirected analogue of "no cycle and connected" is a tree, not a topological order.

## Diagram and dry run

```mermaid
flowchart TD
    A[Compute indegrees] --> B[Queue every node with indegree 0]
    B --> C{Queue empty?}
    C -->|No| D[Pop u into the order]
    D --> E[Decrement neighbors. Enqueue any that hit 0]
    E --> C
    C -->|Yes| F{Order has n nodes?}
    F -->|Yes| G[That is a topological order]
    F -->|No| H[The remainder is a cycle]
```

Edges 0 to 1, 0 to 2, 1 to 3, 2 to 3. Indegrees: 0 is 0, 1 is 1, 2 is 1, 3 is 2.

| Pop | Order | Indegrees of 1, 2, 3 after the pops so far | Queue |
| --- | --- | --- | --- |
| start | empty | 1, 1, 2 | 0 |
| 0 | 0 | 0, 0, 2 | 1, 2 |
| 1 | 0, 1 | 0, 0, 1 | 2 |
| 2 | 0, 1, 2 | 0, 0, 0 | 3 |
| 3 | 0, 1, 2, 3 |  | empty |

The order 0, 1, 2, 3 respects every edge. The order 0, 2, 1, 3 is the other topological order, and it appears if the queue pops 2 before 1. Both are correct when the problem accepts any order.

Add an edge 3 to 1. Indegrees change and the queue never frees the cycle 1, 3. The output length is less than 4. Report a cycle.

## Runnable Python

Kahn's algorithm below returns an empty list when there is a cycle, and one valid order otherwise. The DFS version returns the same kind of answer and uses a color array. Prefer Kahn in Python at large n. The DFS version is the one whose finishing-time story you should be able to tell.

```python
def topo_kahn(graph: list[list[int]]) -> list[int]:
    from collections import deque
    n = len(graph)
    indegree = [0] * n
    for node in range(n):
        for nxt in graph[node]:
            indegree[nxt] += 1
    queue = deque(node for node in range(n) if indegree[node] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else []


def topo_dfs(graph: list[list[int]]) -> list[int]:
    n = len(graph)
    color = [0] * n
    order: list[int] = []

    def visit(node: int) -> bool:
        color[node] = 1
        for nxt in graph[node]:
            if color[nxt] == 1:
                return False
            if color[nxt] == 0 and not visit(nxt):
                return False
        color[node] = 2
        order.append(node)
        return True

    for node in range(n):
        if color[node] == 0 and not visit(node):
            return []
    order.reverse()
    return order
```

On the four-node example, `topo_kahn` returns 0, 1, 2, 3 if neighbor lists are in increasing order and the initial queue is filled from low indexes to high. `topo_dfs` returns a possibly different valid order, reversed from finishing times. Compare either output against the edges, not against one golden permutation, unless the problem demands the lexicographically smallest one.

## Complexity and trade-offs

| Method | Time | Extra space | Cycle test | Which order |
| --- | --- | --- | --- | --- |
| Kahn, queue | Theta(n + m) | Theta(n) | output shorter than n | depends on queue ties |
| Kahn, min-heap | Theta((n + m) log n) | Theta(n) | same | lexicographically smallest |
| DFS finishing times | Theta(n + m) | Theta(n) | gray neighbor | reverse postorder |

A dynamic-programming longest path in a DAG is topological order plus a relaxation, and it is linear. The same problem on a general graph is hard. The moment someone promises a DAG, topological order becomes the iteration order for one-pass DP. Course schedules with an extra "longest chain of prerequisites" are that DP.

## Tricks, tips, and patterns

Build the edge direction from a sentence you write down: "edge from prerequisite to course." Count indegrees in a separate pass so you do not miss nodes that appear only as neighbors. Nodes that are isolated have indegree 0 and belong in the initial queue. If the problem numbers nodes from 1, allocate n + 1 and ignore 0, or translate. For the smallest lexicographic order, push ready nodes into a heap. For alien dictionary, consecutive words of different lengths define edges between the first differing characters, and a longer word that is a prefix of a shorter next word is an immediate impossibility. Then topological-sort the character graph.

## Common mistakes and edge cases

Edges pointing the wrong way, so the order is reversed and still looks plausible on a chain. Treating an undirected edge as a prerequisite. Forgetting isolated nodes. Reporting a cycle when the queue still has nodes but you stopped early. DFS that uses a visited boolean instead of three colors and misses a back edge into the stack, or that treats a finished node as a cycle. Outputting the finishing list without reversing it. A graph with n = 0. A graph with a self-loop, which is a cycle: indegree never falls, or DFS sees gray immediately. Multiple edges that double-count indegree if you naively add them twice and the neighbor list has duplicates. Deduplicate or accept the double count consistently in both the build and the decrement. An empty neighbor list is not a missing node.

## Interview notes

Say "topological order exists if and only if the directed graph is acyclic." Then pick Kahn and explain indegree zero. Mention DFS finishing times as the other construction. Dry-run the four-node graph, and then add the back edge and show the short output. Confirm the edge direction with the interviewer before you build the list. If they want the lexicographically smallest order, say you will replace the queue with a min-heap and accept the extra log. Do not start coding union-find for a directed prerequisite cycle. Union-find is for undirected connectivity.

## Practice problems

1. [Course Schedule](/practice/course-schedule) and [Course Schedule II](/practice/course-schedule-ii).
2. [Find Eventual Safe States](/practice/find-eventual-safe-states).
3. [Graph Valid Tree](/practice/graph-valid-tree) — undirected, so this is a component check plus an edge count, not a topological sort.
4. [Alien dictionary is the same Kahn skeleton on characters. Practice the edge direction on paper if you have not implemented it.](/practice/course-schedule-ii)

## Summary and cheat sheet

- A topological order puts every edge's tail before its head. It exists exactly on DAGs.
- Kahn: queue of indegree 0, decrement neighbors, fail if you cannot place everyone.
- A min-heap instead of a queue yields the lexicographically smallest order.
- DFS: gray means on the stack and proves a cycle. Reverse the finishing order to get the schedule.
- Edge direction is part of the problem statement. Write it down before you build lists.
- Longest paths on DAGs are one relaxation in topological order.

## Further reading

- [Wikipedia — Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting)
- [Wikipedia — Directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
- [CP-Algorithms, topological sort](https://cp-algorithms.com/graph/topological-sort.html)
'''

emit(
    "10-graphs",
    "01-bfs-dfs-and-grids.mdx",
    title="BFS, DFS, and Grid Graphs",
    slug="bfs-dfs-and-grids",
    summary="The two graph walks, hop distances, directed and undirected cycles, and implicit grids.",
    duration=45,
    difficulty="intermediate",
    prerequisites=["binary-heaps"],
    tags=["graphs", "bfs", "dfs"],
    order=1,
    body=BFS,
)
emit(
    "10-graphs",
    "02-topological-sort.mdx",
    title="Topological Sort",
    slug="topological-sort",
    summary="Kahn's indegree queue, DFS finishing times, and the fact that a directed cycle has no schedule.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["bfs-dfs-and-grids"],
    tags=["graphs", "topological-sort", "dag"],
    order=2,
    body=TOPO,
)
