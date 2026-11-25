"""Tree traversals, Morris, BST, LCA, diameter, and serialization."""

from emit import emit

TRAV = r'''
## Why this matters

Trees are the first structure where the shape of the recursion is the shape of the data. Directory listings, expression trees, the DOM, and compiler ASTs are all trees. Interview problems on binary trees ask you to walk every node with a stated order, to compute a value that depends on both children, and to do it without wasting space. The recursive walks are the specification. The explicit-stack walks are how you dodge the recursion limit. Morris traversal is the specialist answer when the interviewer asks for constant extra memory and will let you temporarily rewrite pointers. You should know all three, and you should know which one you are offering.

## Intuition

A binary tree is a node with a left child, a right child, or neither. There is one root and no cycles. Preorder visits a node before its children, which is "say the name, then explore." Inorder visits the left subtree, then the node, then the right subtree, which on a binary search tree yields sorted order. Postorder visits the children before the node, which is "finish the pieces, then combine." Level order visits row by row, which is a queue rather than a stack. Morris is inorder without a stack: you thread a pointer from the predecessor back to the node, so you can return to it after the left subtree, and then you erase the thread.

## Core concept in depth

The recursive preorder is: if the node is null, return; visit; recurse left; recurse right. Inorder swaps the visit to the middle. Postorder visits after both calls. The base case is the null node, not the leaf. Treating a leaf as the base case and then forgetting null children is how you crash. Time is Theta(n) because each node is visited once. The extra space is the recursion depth, Theta(h), where h is the height. A balanced tree has logarithmic height. A chain has linear height. State both.

The iterative preorder uses an explicit stack. Push the root. While the stack is not empty, pop, visit, and push the right child then the left child, so the left is popped first. The iterative inorder walks left as far as possible, pushing nodes, then pops and visits, then steps to the right. The iterative postorder is the awkward one. Two common versions: visit in preorder but node-right-left and reverse the output at the end, or keep a pointer to the previously visited node so you know whether you are returning from the left or the right child. The reverse trick is shorter. Say that the output list is reversed, so the extra memory is still linear in the output, which you needed anyway if the caller wants the list.

Level order uses a queue. Push the root. While the queue is not empty, record the size, and pop exactly that many nodes, enqueueing their children. Each iteration of the size loop is one level. Right-side view is the last node of each level. Zigzag is the same walk with alternating append directions, or a reverse of every other level. The queue holds at most one level. On a balanced tree that is about n/2 nodes. Time is Theta(n). Do not recurse per level unless you also pass the depth and fill buckets. That recursive version is a depth-first search that happens to group by depth, and its stack is the height, not the width.

Morris inorder uses the predecessor, the rightmost node of the left subtree. If there is no left child, visit the node and go right. If there is a left child, find the predecessor. If its right pointer is null, thread it to the current node and go left. If its right pointer is already the current node, you have finished the left subtree: erase the thread, visit the current node, and go right. Every edge is followed a constant number of times, so the time is Theta(n). The extra memory is Theta(1) besides the output, because the stack is gone and the threads occupy existing pointers. The tree is restored when the algorithm ends. It is temporarily mutated. Do not use Morris on a shared tree unless you can prove no other reader observes the threads. It also does not generalize as cleanly to postorder, though a Morris postorder exists and is harder to get right. For interviews, Morris inorder is the one to know.

Diameter is the longest path between any two nodes, measured in edges or in nodes. The statement must say which. The standard node-count version is computed with a postorder: the height of a null child is 0, the height of a node is 1 plus the taller child, and the best path through this node is the left height plus the right height. The answer is the maximum of that sum over all nodes. You return the height and carry the best in a closure or a return pair. This is postorder because you need both children before you can score the node.

A tree is height-balanced when every node's subtrees differ in height by at most one. The same postorder returns the height, or a failure flag if a subtree is already unbalanced or the heights differ by more than one. Short-circuiting avoids extra work. Maximum depth is the height walk without the balance check. Same tree and symmetric tree are simultaneous walks. Symmetric compares the left of one side with the right of the other.

Path sum asks whether a root-to-leaf path adds to a target. Subtract as you go, and succeed only at a leaf. Maximum path sum allows a path that does not pass through the root and does not need to be root-to-leaf. At each node the best path that can be extended upward is the node plus at most one child contribution, and only if that contribution is positive. The best path that bends through the node, using both children, is a candidate for the global answer and is not returned upward, because a parent cannot use both. Negative children are dropped. This is the tree version of Kadane.

## Diagram and dry run

```mermaid
flowchart TD
    N[Node] --> L[Left subtree]
    N --> R[Right subtree]
    L --> I[Inorder visits left, then node, then right]
```

Tree with root 1, left child 2, right child 3, and 2's left child 4.

| Order | Visit sequence | Why |
| --- | --- | --- |
| Preorder | 1, 2, 4, 3 | node before children |
| Inorder | 4, 2, 1, 3 | left, node, right |
| Postorder | 4, 2, 3, 1 | children before node |
| Level order | 1, then 2 3, then 4 | queue, one width at a time |

Morris on this tree threads 4's right pointer, which is null, up to 2, then later to 1 when 2 is the predecessor of 1. After visiting 1 the thread is removed. The visit order is still 4, 2, 1, 3. Heights: 4 has height 1, 2 has height 2, 3 has height 1, 1 has height 3. The diameter through 1 is 2 + 1 = 3 nodes if you count nodes on the path 4-2-1-3, which is 3 edges. Say the unit before you quote a number.

## Runnable Python

Recursive and iterative inorder are the pair to memorize. Diameter is the postorder pattern. Node objects are small on purpose.

```python
class Node:
    def __init__(self, value: int, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def inorder(root: Node | None) -> list[int]:
    if root is None:
        return []
    return inorder(root.left) + [root.value] + inorder(root.right)


def inorder_iter(root: Node | None) -> list[int]:
    out: list[int] = []
    stack: list[Node] = []
    cur = root
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.value)
        cur = cur.right
    return out


def diameter(root: Node | None) -> int:
    best = 0

    def height(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best
```

The recursive inorder builds lists on the way back. That is correct and spends extra linear work on concatenations in a skewed tree, which can become quadratic. The iterative version, or a recursive helper that appends into one shared list, is Theta(n). Use the shared list in an interview. `diameter` on the example returns 3, counting edges, because left + right at the root is 2 + 1 = 3. Check that number against the statement's unit.

## Complexity and trade-offs

| Walk | Time | Extra space |
| --- | --- | --- |
| Recursive preorder, inorder, postorder | Theta(n) | Theta(h) stack |
| Iterative with an explicit stack | Theta(n) | Theta(h) |
| Level order | Theta(n) | Theta(width) |
| Morris inorder | Theta(n) | Theta(1) extra, mutates temporarily |
| Recursive inorder that concatenates new lists | Theta(n) to Theta(n squared) | Theta(n) output plus intermediates |

Morris is the constant-space answer. It is harder to debug and it writes to the tree. The explicit stack is the practical answer. Level order is mandatory when the problem talks about depth, rows, or the rightmost node. Do not simulate a queue with recursion.

## Tricks, tips, and patterns

Null is the base case. Return a pair when one walk must compute two things, such as height and diameter, or height and balance. For maximum path sum, clamp child contributions at zero. For level order, snapshot the queue length. For Morris, the predecessor is the rightmost node of the left subtree, stopping if you meet a thread that already points at the current node. Restore every thread. If you need parent pointers or a previous-node pointer, say so, because a plain binary tree does not have them and you must not pretend it does.

## Common mistakes and edge cases

Concatenating lists and timing out on a chain. Forgetting to push right before left in iterative preorder, which swaps the children. Morris threads left in place, so a later algorithm sees a cycle. Diameter counted in nodes when the tests count edges, or the reverse. A null root: diameter 0, traversals empty, height 0. A single node: diameter 0 edges. Path sum on a non-leaf that happens to equal the target is not a success in the root-to-leaf problem. Maximum path sum with all negative nodes must return the largest node, not zero. Balance that only checks the root and not every subtree. Symmetric tree that compares left with left.

## Interview notes

Say the order and the base case, then code the recursive form. Offer the iterative form if they ask about stack limits. Mention Morris only when they ask for constant extra space, and say that it temporarily rewrites pointers. For diameter and path sum, say "postorder, I need both children." Dry-run the four-node example. Agree on edges versus nodes before you compute a number.

## Practice problems

1. [Binary Tree Level Order Traversal](/practice/binary-tree-level-order-traversal) and [Binary Tree Right Side View](/practice/binary-tree-right-side-view).
2. [Maximum Depth of Binary Tree](/practice/maximum-depth-of-binary-tree) and [Balanced Binary Tree](/practice/balanced-binary-tree).
3. [Diameter of Binary Tree](/practice/diameter-of-binary-tree).
4. [Path Sum](/practice/path-sum) and [Binary Tree Maximum Path Sum](/practice/binary-tree-maximum-path-sum).
5. [Same Tree](/practice/same-tree) and [Symmetric Tree](/practice/symmetric-tree).
6. [Invert Binary Tree](/practice/invert-binary-tree) — swap children, preorder or postorder.

## Summary and cheat sheet

- Preorder: node, left, right. Inorder: left, node, right. Postorder: left, right, node.
- Null is the base case. Time is linear. Stack space is the height.
- Level order is a queue. Snapshot the size to separate rows.
- Morris inorder threads the predecessor, visits, then unthreads. Constant extra space, temporary mutation.
- Diameter and balance and maximum path sum are postorder reductions.
- A path extended to a parent uses at most one child. A path that bends is only a global candidate.
- Do not concatenate fresh lists on every return if n can be large.

## Further reading

- [Wikipedia — Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal)
- [Wikipedia — Binary tree](https://en.wikipedia.org/wiki/Binary_tree)
- [CP-Algorithms, depth-first search is the graph form of the same walk](https://cp-algorithms.com/graph/depth-first-search.html)
'''

BST = r'''
## Why this matters

A binary search tree stores keys so that an inorder walk is sorted and a search is a walk down one path. That property is the source of successor queries, kth-smallest, and a cheapest lowest common ancestor. It is also a trap. A tree that merely looks balanced in a drawing can be a chain, and then every "logarithmic" operation is linear. Validation, serialization, and the lowest common ancestor of a general binary tree are the problems that check whether you used the property you were allowed to use, and no property you were not given.

## Intuition

Every node splits the key space. Keys less than the node belong to the left. Keys greater belong to the right. Search is binary search on a tree instead of an array: you throw away a subtree instead of a half-array. The lowest common ancestor in a BST is the first node where the two targets fall on different sides, or the node that is one of the targets. In a general binary tree you do not have sides. You have "did I find the target in this subtree?" and the ancestor is the first node for which the answer is yes on both sides, or the node that is itself a target and found the other target below it.

## Core concept in depth

The search-tree property must hold for the whole subtree, not only for the parent link. A node can be greater than its parent and still smaller than some node in the parent's left subtree, which violates the property even though each edge looks locally fine. The correct validation carries a valid open interval. The root may hold any key. The left child must lie strictly inside (low, node), and the right child strictly inside (node, high). Pass the interval down. An inorder walk that checks for a strictly increasing sequence is an equivalent test and uses the same time. The interval version makes the allowed range obvious. Duplicates: decide whether they go left, right, or are forbidden. The interval test uses strict inequalities when duplicates are forbidden. Match the problem.

Search and insert follow one path. Search returns null when it falls off. Insert attaches the new key at the null where search ended. Both are Theta(h). Delete has three cases: a leaf is removed, a node with one child is replaced by that child, and a node with two children is replaced by its inorder successor or predecessor, which is then deleted from the subtree. The successor is the leftmost node of the right subtree. Deletion is the operation most candidates fumble. Practice it on a node with two children.

Kth smallest is inorder until you have visited k nodes. If the tree is large and you query often, augment each node with the size of its subtree. Then the walk decides in constant time per level whether the kth key is the current node, in the left subtree, or in the right subtree at rank k - size(left) - 1. The augmented search is Theta(h). The augmentation must be maintained on insert and delete. Say that cost if you propose it.

Lowest common ancestor of a binary search tree: if both keys are smaller, go left. If both are larger, go right. Otherwise the current node is the split, and it is the ancestor. This assumes both keys exist. If they might not, search for both first or continue carefully. Lowest common ancestor of a general binary tree: a postorder returns a node if this subtree contains p or q. If the left recursion and the right recursion both return non-null, this node is the ancestor. If one side returns non-null, pass that result up. A node that is p or q returns itself. The first formulation that "returns this node when both sides hit" misses the case where the node itself is p and q is in one subtree. Returning itself immediately, and still combining children only when the node is neither target, is the clean version: if the node is p or q, you can still look at children if you need to know whether the other exists, but the usual problem guarantees both exist, so returning the node when you see a target is correct. The standard code that checks children first also works when both exist: a target returns itself after its children return null. Dry-run a case where the ancestor is one of the targets.

Serialization turns a tree into a string or a list that can be rebuilt. Level-order serialization writes values row by row and writes an explicit null for missing children, then drops trailing nulls if the format allows. Deserialization uses a queue: the front node receives the next two values as children, and non-null children join the queue. Preorder serialization writes the node, then the left subtree, then the right, with null markers. Deserialization is a recursive read that consumes the marker and returns null, or builds a node and reads its left and right from the same cursor. Both formats need the null markers. Without them the shape is ambiguous. Inorder alone is never enough. Inorder plus preorder is enough for a unique binary tree when keys are unique: the preorder root splits the inorder array into the left and right index ranges. That reconstruction is a classic problem. Duplicate keys make it ambiguous unless the statement adds a rule.

A balanced search tree keeps h logarithmic. AVL and red-black trees, in the next lesson, are the usual guarantees. A plain BST does not promise balance. If the interview gives you a static set of keys and you may preprocess, sorting and building the tree from the middle key yields a balanced tree in linear time after the sort. If the keys arrive online, you need rotations or a skip list or a hash table.

## Diagram and dry run

```mermaid
flowchart TD
    R["Root 4, interval all keys"] --> L["Left 2, keys below 4"]
    R --> RT["Right 6, keys above 4"]
    L --> LL["Left 1"]
    L --> LR["Right 3"]
```

Validate 4 with left 2 and right 6, and 2 with children 1 and 3. Every node sits inside its inherited interval. Change 3 to 5 and the interval for the right child of 2 is (2, 4). 5 is outside it, so the tree is illegal even though 5 is greater than 2.

LCA of 1 and 3 in this BST. Both are less than 4, so go left to 2. Then 1 and 3 fall on different sides of 2, so 2 is the ancestor. LCA of 1 and 6: they fall on different sides of 4, so 4 is the ancestor. LCA of 2 and 3: 2 is itself a target, and 3 is in its subtree, so 2 is the ancestor.

Serialize the same tree in preorder with null markers: 4, 2, 1, null, null, 3, null, null, 6, null, null. The recursive reader consumes that stream left to right and rebuilds the edges.

## Runnable Python

Validation carries the interval. The BST lowest ancestor is a walk with no extra memory. The general-tree ancestor is a postorder. All three are recursive. The interval walk has an iterative form with an explicit stack of triples, which you can write if the tree may be a chain of 10 to the 5th nodes.

```python
class Node:
    def __init__(self, value: int, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def is_bst(root: Node | None, low: float = float("-inf"), high: float = float("inf")) -> bool:
    if root is None:
        return True
    if not (low < root.value < high):
        return False
    return is_bst(root.left, low, root.value) and is_bst(root.right, root.value, high)


def lca_bst(root: Node | None, p: int, q: int) -> Node | None:
    cur = root
    while cur is not None:
        if p < cur.value and q < cur.value:
            cur = cur.left
        elif p > cur.value and q > cur.value:
            cur = cur.right
        else:
            return cur
    return None


def lca_tree(root: Node | None, p: Node, q: Node) -> Node | None:
    if root is None or root is p or root is q:
        return root
    left = lca_tree(root.left, p, q)
    right = lca_tree(root.right, p, q)
    if left is not None and right is not None:
        return root
    return left or right
```

`is_bst` rejects a node that sits on the boundary when duplicates are forbidden, because the inequalities are strict. `lca_bst` is iterative and uses constant extra memory. `lca_tree` compares node identity, not value, so duplicate values remain unambiguous. On the example, `lca_bst` of 1 and 3 returns the node 2.

## Complexity and trade-offs

| Operation | Balanced height | Chain | Extra space |
| --- | --- | --- | --- |
| Search, insert | Theta(log n) | Theta(n) | Theta(1) iterative, Theta(h) recursive |
| Delete | Theta(log n) | Theta(n) | Theta(h) to find the successor |
| Validate | Theta(n) | Theta(n) | Theta(h) |
| Kth smallest, plain inorder | Theta(h + k) | Theta(k) | Theta(h) |
| Kth smallest, subtree sizes | Theta(h) | Theta(n) | Theta(1) extra on top of the sizes |
| LCA, BST | Theta(h) | Theta(n) | Theta(1) |
| LCA, general tree | Theta(n) | Theta(n) | Theta(h) |
| Serialize and rebuild | Theta(n) | Theta(n) | Theta(n) for the output |

A hash table is expected constant time for exact membership and does not give you successor, rank, or range queries. A sorted array gives you binary search and rank, and it is expensive to update. A balanced BST is the structure that does all of those in logarithmic time. If the problem is static, sorting once is enough and simpler.

## Tricks, tips, and patterns

Carry an interval, do not only compare with the parent. For BST LCA, the first split is the answer. For general LCA, identity and a postorder. For serialization, null markers are mandatory in a single traversal. For reconstruction from preorder and inorder, the root is the first preorder value and it splits the inorder range. Build a map from value to inorder index so each split is constant time. The total is then linear. For kth smallest without augmentation, iterate the inorder and stop at k. Do not materialize the whole list if k is small and n is large, unless the height is the bigger problem.

## Common mistakes and edge cases

A local parent check that accepts an illegal tree. Duplicates with a strict validator. LCA coded with values on a general tree that contains duplicates. Returning the first target you see in a general tree without looking at the other side, which fails when the two targets are in different branches... actually returning a target immediately is correct if both exist. The bug is returning a target and also requiring both children. Read the code you wrote against the case "ancestor is one of the nodes." Serialization without nulls. Forgetting to enqueue only non-null children while still consuming null markers from the list. An empty tree serializes to an empty list. A single null child must not shift the next level. Successor deletion that fails to copy the successor's key and then deletes the wrong node. Integer keys equal to your sentinel low or high, if you used a real integer instead of infinity. Use a None bound or a real infinity.

## Interview notes

Ask whether the tree is a BST and whether it is balanced. Those two answers change the complexity you are allowed to claim. For validation, describe the interval. For LCA, say which algorithm matches the tree you were given. Do not run the BST split on a general tree. Dry-run the ancestor-is-the-node case. For serialization, include one null in the dry run so the queue indexes stay honest. Mention balance only as a hypothesis unless the problem guarantees it.

## Practice problems

1. [Validate Binary Search Tree](/practice/validate-binary-search-tree).
2. [Kth Smallest Element in a BST](/practice/kth-smallest-element-in-a-bst).
3. [Lowest Common Ancestor of a BST](/practice/lowest-common-ancestor-of-a-bst) and [Lowest Common Ancestor of a Binary Tree](/practice/lowest-common-ancestor-of-a-binary-tree).
4. [Invert Binary Tree](/practice/invert-binary-tree) and [Symmetric Tree](/practice/symmetric-tree).
5. Build the preorder-with-nulls serializer on a whiteboard even though the platform problems here use level-order arrays as input.

## Summary and cheat sheet

- BST: every key in the left subtree is smaller, every key in the right subtree is larger. Validate with an interval.
- Search, insert, and BST LCA are one path, Theta(height).
- General LCA is a postorder on identities. The split node, or a target that contains the other target, is the answer.
- Kth smallest is inorder, or a subtree-size augmentation.
- Serialization needs null markers. Preorder plus inorder rebuilds a unique tree when keys are unique.
- A plain BST can be a chain. Logarithmic claims need balance or a random-insert assumption you must state.

## Further reading

- [Wikipedia — Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree)
- [Wikipedia — Lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor)
- [CLRS, binary search trees](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
'''

emit(
    "08-trees",
    "01-traversals-and-morris.mdx",
    title="Traversals, Diameter, and Morris Inorder",
    slug="traversals-and-morris",
    summary="Preorder, inorder, postorder, level order, and the constant-extra-space Morris walk, plus the postorder reductions.",
    duration=45,
    difficulty="intermediate",
    prerequisites=["timsort"],
    tags=["trees", "traversals", "morris"],
    order=1,
    body=TRAV,
)
emit(
    "08-trees",
    "02-bst-lca-and-serialization.mdx",
    title="BST Property, LCA, and Serialization",
    slug="bst-lca-and-serialization",
    summary="Interval validation, the BST split for ancestors, the general-tree postorder, and why serialization needs nulls.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["traversals-and-morris"],
    tags=["bst", "lca", "trees"],
    order=2,
    body=BST,
)
