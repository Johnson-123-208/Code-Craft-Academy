"""Shortest paths, MSTs, union-find, and bridges."""

from emit import emit

PATHS = r'''
## Why this matters

BFS dies as soon as edges have different costs. The shortest path is no longer the one with the fewest edges. Dijkstra's algorithm repairs that for non-negative weights by growing a settled region. Bellman-Ford allows negative weights and detects negative cycles, at a slower cost. Floyd-Warshall computes every pair on a dense graph with a tiny piece of code and a cubic cost. Network delay, cheapest flights with a hop limit, and "is there a negative cycle" are these three algorithms. Using the wrong one is not a style issue. Dijkstra is incorrect on negative edges, and Bellman-Ford is too slow when the graph is large and the weights are safe.

## Intuition

Dijkstra is BFS with a priority queue. You always expand the unsettled node whose current distance is smallest. With non-negative weights, the first time you pop a node you can never find a cheaper path later, because any path that leaves the settled region has to pay a non-negative toll. Bellman-Ford does not trust that argument. It relaxes every edge, and it repeats that pass enough times for a simple path to have been considered, which is n - 1 passes. A cheaper update on pass n means a negative cycle. Floyd-Warshall asks, for each possible waypoint k, whether going via k improves the best path between i and j. Adding waypoints one at a time is dynamic programming on the set of allowed intermediate nodes.

## Core concept in depth

A relaxation of an edge u to v with weight w asks whether dist[v] is greater than dist[u] + w. If it is, write the smaller value and remember u as the predecessor. Every shortest-path algorithm in this lesson is a schedule for relaxations, plus a reason the schedule is enough.

Dijkstra. Set the source distance to 0 and every other distance to infinity. Push (0, source) into a min-heap. While the heap is not empty, pop the smallest distance. If it is worse than the stored distance, it is a stale copy and you skip it. Otherwise the node is settled. Relax each outgoing edge and push the neighbor with the new distance. The first time a node is settled, its distance is final, provided every weight is non-negative. Time with a binary heap is Theta((n + m) log n) when you allow duplicate entries. A Fibonacci heap is Theta(m + n log n) and is not worth coding here. If you need the path, follow predecessors back to the source and reverse them.

Negative weights break the settlement argument. A later edge could pay you to enter a node you already popped. Do not run Dijkstra. Bellman-Ford initializes distances the same way and then loops n - 1 times over all edges, relaxing each. After that, every simple-path distance is correct if no negative cycle is reachable. One more pass that still relaxes an edge proves a negative cycle reachable from the source. To detect a cycle anywhere, add a dummy source with a zero-cost edge to every node, or start the extra pass from a distance array of zeros if the problem asks "does this graph have a negative cycle" rather than "reachable from s." Time is Theta(n m). On a dense graph that is Theta(n cubed), the same order as Floyd-Warshall, with a worse constant for all-pairs.

Cheapest flights within k stops is Bellman-Ford limited to k + 1 relaxations, and you must relax from a copy of the previous pass. If you relax in place, a single pass can chain many hops and violate the stop limit. That bug is the whole problem.

Floyd-Warshall uses a matrix. dist[i][i] = 0. dist[i][j] is the edge weight or infinity. For k from 0 to n - 1, for every pair i, j, relax dist[i][j] with dist[i][k] + dist[k][j]. The k loop is outside. Swapping it inside is wrong, because you would use waypoints you have not finished computing in the right order. The algorithm handles negative weights and can detect a negative cycle when some dist[i][i] becomes negative. Time is Theta(n cubed). Space is Theta(n squared). Use it when n is a few hundred and you need every pair. Use Dijkstra from each source when the graph is sparse and weights are non-negative: that is n times (n + m) log n, which wins on sparse graphs.

Path reconstruction for Floyd stores next[i][j], the first hop, updated whenever the relaxation improves. For Dijkstra and Bellman-Ford, store the parent. A distance without a parent is enough when the problem asks only for the cost.

Unweighted graphs should stay on BFS. A heap makes them slower. 0-1 weights can use the deque version from the BFS lesson. Non-negative arbitrary weights use Dijkstra. Negative weights use Bellman-Ford or Floyd. A negative cycle on the path makes the shortest-path question undefined, because looping decreases the cost forever. Return the problem's failure value.

## Diagram and dry run

```mermaid
flowchart TD
    A[Weights non-negative?] -->|Yes| B[Dijkstra with a min-heap]
    A -->|No| C{Need all pairs and n is small?}
    C -->|Yes| D[Floyd-Warshall]
    C -->|No| E[Bellman-Ford from the source]
    E --> F{Extra pass still relaxes?}
    F -->|Yes| G[Negative cycle]
    F -->|No| H[Distances are shortest simple paths]
```

Directed edges: 0 to 1 weight 4, 0 to 2 weight 1, 2 to 1 weight 2, 1 to 3 weight 1. Dijkstra from 0.

| Pop | Settled distance | Heap idea | Distances of 0, 1, 2, 3 |
| --- | --- | --- | --- |
| start |  | (0, 0) | 0, inf, inf, inf |
| 0 | 0 | (4, 1), (1, 2) | 0, 4, 1, inf |
| 2 | 1 | (3, 1), (4, 1) | 0, 3, 1, inf |
| 1 | 3 | (4, 3) and a stale (4, 1) | 0, 3, 1, 4 |
| 3 | 4 |  | 0, 3, 1, 4 |

The stale pair for node 1 with distance 4 is ignored because 3 is already stored. The shortest path to 1 is 0, 2, 1 with cost 3, not the direct edge.

Change the edge 2 to 1 into weight -5. Dijkstra might settle 1 too early at 4 and never repair it. Bellman-Ford will. If you also add a cycle that returns to 2 with total negative weight, the extra pass reports it and the distance to nodes on that cycle is undefined.

## Runnable Python

Dijkstra with stale entries, and one Bellman-Ford that returns null on a negative cycle reachable from the source. Both are iterative. Floyd is a triple loop you can write from the recurrence without a helper.

```python
def dijkstra(graph: list[list[tuple[int, int]]], source: int) -> list[float]:
    import heapq
    n = len(graph)
    dist = [float("inf")] * n
    dist[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        cost, node = heapq.heappop(heap)
        if cost != dist[node]:
            continue
        for nxt, weight in graph[node]:
            cand = cost + weight
            if cand < dist[nxt]:
                dist[nxt] = cand
                heapq.heappush(heap, (cand, nxt))
    return dist


def bellman_ford(n: int, edges: list[tuple[int, int, int]], source: int) -> list[int] | None:
    dist = [10**18] * n
    dist[source] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None
    return dist
```

On the non-negative example, `dijkstra` reports 0, 3, 1, 4. `bellman_ford` on the same edges does too. If a negative cycle is reachable, `bellman_ford` returns null. Compare floats only when you stored floats. Prefer integers for integer weights so the stale check `cost != dist[node]` is exact. The code above uses floats because infinity is convenient. An integer sentinel works if you guard the addition against overflow of the sentinel.

## Complexity and trade-offs

| Algorithm | Weights | Time | Space | Returns |
| --- | --- | --- | --- | --- |
| BFS | unit | Theta(n + m) | Theta(n) | one source |
| Dijkstra, binary heap | non-negative | Theta((n + m) log n) | Theta(n + m) | one source |
| Bellman-Ford | any, detects negative cycles | Theta(n m) | Theta(n) | one source |
| Floyd-Warshall | any, detects negative cycles on the diagonal | Theta(n cubed) | Theta(n squared) | all pairs |
| DAG relaxation in topological order | any, no cycles by promise | Theta(n + m) | Theta(n) | one source |

On a DAG, even with negative weights, one relaxation in topological order is enough and there is no negative cycle to worry about unless the promise is false. That is the fastest shortest path you will ever get. Use it when the graph is known to be acyclic.

## Tricks, tips, and patterns

Skip stale heap entries. Copy the distance array between Bellman-Ford passes when a hop limit exists. Keep the k loop outermost in Floyd-Warshall. Initialize the source to 0 and everything else to a real infinity, not to 0. A 0 initialization makes every node look reachable at cost 0. Store parents if the path is required. For "impossible," the problem usually wants -1 when the distance stays infinite. Translate that at the end, not inside the relaxations, or you will treat -1 as a tiny weight.

## Common mistakes and edge cases

Dijkstra on a negative edge. In-place Bellman-Ford when hops are limited. Floyd with the loops nested in the wrong order. Overflow when infinity plus a weight wraps in a fixed-width integer. Using a visited set in Dijkstra that refuses to update a node before it is settled, which is actually correct only if you mark settled on pop, not on push. Marking on push is the BFS habit and it is wrong for Dijkstra, because the first push may not be the best distance. The stale-entry style marks settled on pop by the equality check. A disconnected node stays infinite. A source with a negative self-loop is a negative cycle. An empty edge list leaves only the source at 0. k = 0 in the flight problem means no flight, so only the source is reachable unless you define zero-hop carefully. Read the stop count.

## Interview notes

Ask about signs of weights and about whether you need one source or all pairs. Then name the algorithm and its bound before you code. Say the settlement sentence for Dijkstra: "non-negative weights, so the first pop is final." Say the extra pass for Bellman-Ford. Dry-run the four-node example, including the stale pair, so the interviewer sees why you do not use a visited-on-push set. If the graph is a DAG, say you will relax in topological order in linear time.

## Practice problems

1. [Network Delay Time](/practice/network-delay-time) — Dijkstra. The answer is the maximum finite distance, or the failure value if some node is unreachable.
2. [Cheapest Flights Within K Stops](/practice/cheapest-flights-within-k-stops) — Bellman-Ford with a pass limit and a copied distance array.
3. [Path With Minimum Effort and similar threshold searches can be Dijkstra or binary search plus BFS. Network delay is the clean Dijkstra drill.](/practice/network-delay-time)

## Summary and cheat sheet

- Relaxation: if dist[u] + w is smaller, update dist[v].
- Dijkstra: min-heap, non-negative weights, first pop is final, skip stale pairs. Time (n + m) log n.
- Bellman-Ford: n - 1 full passes. A successful nth pass means a negative cycle. Time n m.
- Hop limits require relaxing from the previous pass only.
- Floyd-Warshall: k outside, then i, j. Time n cubed. Negative diagonal means a negative cycle.
- DAGs: one pass in topological order, even if weights are negative.
- Unit weights: go back to BFS.

## Further reading

- [Wikipedia — Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Wikipedia — Bellman-Ford algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm)
- [Wikipedia — Floyd-Warshall algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)
- [CP-Algorithms, Dijkstra](https://cp-algorithms.com/graph/dijkstra.html)
'''

MST = r'''
## Why this matters

A minimum spanning tree connects every node at the smallest total edge weight, without cycles. Network design, clustering, and "cheapest way to link these points" are that problem. Kruskal's algorithm sorts edges and adds one when it joins different components. Prim's algorithm grows one component by the cheapest edge that leaves it. Both need a reason to believe the greedy choice is safe, and Kruskal needs a union-find structure to recognize components in nearly constant time. The same union-find answers redundant connections and whether an undirected graph is a tree. Bridges, the edges whose removal disconnects the graph, are a different question: Tarjan's depth-first search computes them in linear time. Critical connections are that algorithm.

## Intuition

Kruskal looks at the globally cheapest edge that does not close a cycle, and trusts that some optimal tree can include it. The exchange argument says: if an optimal tree avoided that edge, adding it would create a cycle, and deleting the heaviest edge on that cycle cannot increase the cost, so you can force the cheap edge in. Prim trusts the cheapest edge leaving the grown set, for the same exchange reason: an optimal tree must cross the cut somewhere, and you can swap in the cheapest crossing edge. Union-find is the accountant. Each node starts in its own family. Find walks to the family representative. Union marries two families. A proposed edge is a cycle exactly when its ends already share a representative.

## Core concept in depth

A spanning tree of a connected undirected graph is a subset of n - 1 edges that connects every node. It is acyclic by the edge count plus connectivity, or by construction. A minimum spanning tree minimizes the sum of edge weights. If weights are distinct, the MST is unique. If not, several trees can share the minimum sum.

Union-find, or disjoint set union, stores a parent pointer. Find follows parents to the root. Path compression points every node on that walk directly at the root, or at least halfway up. Union by rank or by size attaches the shorter tree under the taller one, so the trees stay shallow. Together, any sequence of m operations on n elements costs nearly O(m + n), more precisely O(m alpha(n)) where alpha is the inverse Ackermann function, which is at most 4 for any n you will ever store. In interviews you may say "effectively constant per operation." Without compression and without rank, a union-find can degenerate into a list and become linear per find.

Kruskal sorts the edges by weight, lightest first. For each edge, if find of the two ends differs, union them and keep the edge. Stop at n - 1 edges, or scan them all if you also want to know whether the graph was disconnected. If you finish with fewer than n - 1 unions, no spanning tree exists. Time is the sort, Theta(m log m), plus the nearly linear union-find. Correctness is the cut or the exchange argument above, applied to the lightest edge that still joins two components.

Prim grows a set S, starting from any node. A min-heap stores the cheapest known edge that enters each node outside S. When you pop a node, if it is already in S you skip it. Otherwise you add it and relax its edges, decreasing the best entry cost of its neighbors. This is Dijkstra with a different relaxation: the priority is the edge weight into the node, not the path sum from the root. Time is Theta((n + m) log n) with a binary heap. On a dense graph, an array scan for the next minimum is Theta(n squared) and can be faster. Prim needs the graph to be connected or it grows only one component. Loop from unvisited starts if you need a minimum spanning forest.

A graph is a tree when it has n - 1 edges and is connected, which union-find checks: every edge unions two different roots, and you perform exactly n - 1 unions. An extra edge that joins the same root is a cycle. Redundant connection asks for that extra edge, often the last one in the input order. Run the unions in order and return the first edge whose ends share a root.

Bridges are edges that are not on any cycle. Tarjan's bridge algorithm is a DFS that records discovery time and low-link value. low[v] is the smallest discovery time reachable from v by tree edges downward and at most one back edge. When you return from a child v to a parent u, if low[v] is strictly greater than disc[u], the tree edge u-v is a bridge: the child cannot climb back to u or above u. Back edges update low with the neighbor's discovery time, and you must ignore the edge to the parent so you do not treat the tree edge as a back edge. The algorithm is linear. Articulation points, nodes whose removal disconnects the graph, use a similar low-link test: a non-root node is an articulation point when some child cannot climb to an ancestor of the node, and the root is one when it has two or more DFS children. Critical connections asks for the bridges, not the articulation points. Return them in the order the statement demands, usually sorted endpoints.

These structures assume an undirected graph for MSTs and bridges. A directed "minimum spanning tree" is a branching and is a different algorithm. Do not run Kruskal on directed edges and call it an arborescence.

## Diagram and dry run

```mermaid
flowchart TD
    A[Sort edges by weight] --> B{Next edge joins two components?}
    B -->|Yes| C[Union the ends and keep the edge]
    B -->|No| D[Skip. It would close a cycle]
    C --> E{n minus 1 edges kept?}
    D --> E
    E -->|No| B
    E -->|Yes| F[Those edges are an MST]
```

Nodes 0, 1, 2, 3. Edges 0-1 weight 1, 1-2 weight 2, 0-2 weight 3, 2-3 weight 4.

| Edge | Roots before | Decision |
| --- | --- | --- |
| 0-1 weight 1 | all separate | keep. Union 0 and 1 |
| 1-2 weight 2 | 2 is alone | keep. Union into the 0-1 component |
| 0-2 weight 3 | same component | skip |
| 2-3 weight 4 | 3 is alone | keep |

The tree weight is 1 + 2 + 4 = 7. The edge of weight 3 is the one that would cycle.

A bridge example. A triangle 0-1-2 plus a pendant 1-3. DFS from 0 discovers the triangle and can climb back via a back edge, so none of the triangle edges is a bridge. The child 3 has low-link equal to its own discovery time, which is greater than the discovery time of 1, so 1-3 is a bridge.

## Runnable Python

Union-find with path compression and union by rank, plus Kruskal. The bridge finder is the other routine to have nearby when the question is critical connections. Both are iterative at the operation level. The bridge search is recursive DFS. Convert it to an explicit stack if the component can be deeper than the interpreter allows.

```python
class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    dsu = DSU(n)
    chosen: list[tuple[int, int, int]] = []
    for weight, u, v in sorted((w, u, v) for u, v, w in edges):
        if dsu.union(u, v):
            chosen.append((u, v, weight))
            if len(chosen) == n - 1:
                break
    return chosen
```

On the four-node example, `kruskal` returns the three edges of weights 1, 2, and 4. `union` returns false on the weight-3 edge. Path compression is the inner assignment `parent[x] = parent[parent[x]]`. Full compression, pointing every node at the root in one pass, is also fine. Rank stops a long chain when compression has not yet run.

## Complexity and trade-offs

| Algorithm | Time | Space | Needs |
| --- | --- | --- | --- |
| Kruskal | Theta(m log m) | Theta(n) | undirected, union-find |
| Prim, binary heap | Theta((n + m) log n) | Theta(n + m) | undirected, connected for one tree |
| DSU, m operations | Theta(m alpha(n)) | Theta(n) | the accountant, not a tree by itself |
| Tarjan bridges | Theta(n + m) | Theta(n) | undirected DFS |
| Redundant connection | Theta(n alpha(n)) | Theta(n) | exactly one extra edge in the usual problem |

Kruskal is simpler when the edges are already a list. Prim is natural when the graph is an adjacency list and you think in cuts. On points in the plane, Prim or Kruskal on the complete graph is quadratic in the number of points, which the constraints sometimes allow. A Delaunay triangulation would thin the edges. You will not build that in an interview. Say the complete graph is m = n squared.

## Tricks, tips, and patterns

Sort a copy of the edges so you do not surprise the caller. Union returns a boolean so Kruskal and redundant-connection share code. Stop Kruskal at n - 1 edges. For bridges, write disc and low, and skip the parent. Discovery time increases by one per visited node. Compare low of the child with disc of the parent, strictly greater. Equal means a back edge climbed exactly to the parent, so the edge is not a bridge. For articulation points, do not use the bridge test unchanged. A node can be an articulation point without any bridge, in a figure-eight of two cycles sharing a vertex.

## Common mistakes and edge cases

Running MST algorithms on directed graphs. Forgetting the reverse edge when you built an undirected adjacency list, so Prim never sees the way back. Union without compression and rank, then calling it nearly constant. Kruskal that adds an edge before checking find, creating a cycle in the "tree." A disconnected graph: Kruskal returns too few edges, and you must not pretend the sum of a forest is a spanning tree unless the problem asked for a forest. Self-loops. Duplicate edges: the lighter one is considered first and the heavier one is skipped if the ends are already joined. Bridges on a disconnected graph: run DFS from every unvisited node. The parent of a root is a sentinel, and the root's missing parent must not look like a back edge. Integer weights can be zero or negative. MSTs still make sense. "Minimum" with negative weights prefers the negative edges, and Kruskal handles that because it sorts.

## Interview notes

Say "lightest edge that does not cycle" for Kruskal and "lightest edge across the cut" for Prim, then give the exchange sentence in plain language. Mention union-find's two optimizations by name. If the question is only "does this edge close a cycle," you may not need a full MST. For bridges, say low-link and the strict inequality, and offer to dry-run the pendant edge. Confirm undirected. Confirm whether the graph is connected. Return the problem's failure value when a spanning tree does not exist.

## Practice problems

1. [Min Cost to Connect All Points](/practice/min-cost-to-connect-all-points) — Prim or Kruskal on a complete graph of points. The weight is the Manhattan distance.
2. [Redundant Connection](/practice/redundant-connection) — the first edge that union refuses.
3. [Graph Valid Tree](/practice/graph-valid-tree) — n - 1 successful unions.
4. [Critical Connections](/practice/critical-connections) — Tarjan bridges.
5. [Accounts Merge](/practice/accounts-merge) — union-find on emails, not on an MST.
6. [Number of Provinces](/practice/number-of-provinces) — components, by DFS or by union-find.

## Summary and cheat sheet

- An MST is n - 1 edges, connected, minimum total weight.
- Kruskal sorts edges and unions ends that lie in different components.
- Prim grows one component by the cheapest outgoing edge. The priority is the edge, not a path sum.
- Union-find: path compression and union by rank. Effectively constant time. find tells you the component.
- A tree check is n - 1 successful unions, or n - 1 edges plus one connected component.
- A bridge is a DFS tree edge whose child cannot climb to the parent or above: low[child] greater than disc[parent].
- These algorithms are for undirected graphs.

## Further reading

- [Wikipedia — Minimum spanning tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree)
- [Wikipedia — Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)
- [Wikipedia — Bridge (graph theory)](https://en.wikipedia.org/wiki/Bridge_(graph_theory))
- [CP-Algorithms, Kruskal and bridges](https://cp-algorithms.com/graph/bridge-searching.html)
'''

emit(
    "10-graphs",
    "03-shortest-paths.mdx",
    title="Shortest Paths",
    slug="shortest-paths",
    summary="Dijkstra, Bellman-Ford, and Floyd-Warshall, and the weight conditions that make each one valid.",
    duration=40,
    difficulty="advanced",
    prerequisites=["topological-sort"],
    tags=["graphs", "dijkstra", "shortest-paths"],
    order=3,
    body=PATHS,
)
emit(
    "10-graphs",
    "04-mst-dsu-and-bridges.mdx",
    title="Spanning Trees, Union-Find, and Bridges",
    slug="mst-dsu-and-bridges",
    summary="Kruskal, Prim, disjoint sets, and Tarjan's low-link search for bridges.",
    duration=40,
    difficulty="advanced",
    prerequisites=["shortest-paths"],
    tags=["graphs", "mst", "union-find", "bridges"],
    order=4,
    body=MST,
)
