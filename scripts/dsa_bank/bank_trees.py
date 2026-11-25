"""Binary tree and BST problems. Trees are level-order lists; null is JSON null."""

from __future__ import annotations

from lib import cases, define


class _N:
    def __init__(self, value: int, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def _build(values: list) -> _N | None:
    if not values or values[0] is None:
        return None
    root = _N(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = _N(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = _N(values[i])
            queue.append(node.right)
        i += 1
    return root


def _dump(root: _N | None) -> list:
    if root is None:
        return []
    queue = [root]
    out: list = []
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.value)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


@define(
    slug="invert-binary-tree",
    title="Invert Binary Tree",
    difficulty="easy",
    topics=["trees", "recursion"],
    statement="Invert a binary tree given in level order and return the inverted tree in level order, omitting trailing nulls.",
    constraints=["0 <= number of nodes <= 100", "-100 <= Node.val <= 100"],
    signature="from typing import List, Optional\n\ndef invert_tree(root: List[Optional[int]]) -> List[Optional[int]]:",
    function_name="invert_tree",
    hints=[
        "Swap the two children of every node.",
        "Recursion does the swap after, or before, inverting the subtrees. The order of the swap and the recursive calls does not matter.",
        "An empty tree inverts to an empty tree.",
    ],
    approaches=[
        ("BFS swap", "O(n)", "O(n)", "A queue visits every node and swaps its children."),
        ("DFS swap", "O(n)", "O(h)", "The call stack is the height."),
    ],
    editorial=(
        "Inversion is a homomorphism: invert(node) swaps left and right and inverts both sides. "
        "The base case is a null child. Level-order serialization is only the input and output format. The algorithm itself walks nodes."
    ),
    companies=["Google", "Amazon", "Adobe", "Microsoft"],
)
def invert_tree(root: list) -> list:
    node = _build(root)

    def walk(current):
        if current is None:
            return None
        current.left, current.right = walk(current.right), walk(current.left)
        return current

    return _dump(walk(node))


def _oracle_invert_tree(root: list) -> list:
    node = _build(root)

    def walk(current):
        if current is None:
            return
        current.left, current.right = current.right, current.left
        walk(current.left)
        walk(current.right)

    walk(node)
    return _dump(node)


cases(
    "invert-binary-tree",
    _oracle_invert_tree,
    [
        ("classic", {"root": [4, 2, 7, 1, 3, 6, 9]}, True, "Every left and right child swaps."),
        ("empty", {"root": []}, True, "The empty tree stays empty."),
        ("single", {"root": [1]}, False, None),
        ("skew", {"root": [1, 2, None, 3]}, False, None),
        ("two", {"root": [1, 2, 3]}, False, None),
    ],
)


@define(
    slug="maximum-depth-of-binary-tree",
    title="Maximum Depth of Binary Tree",
    difficulty="easy",
    topics=["trees", "recursion"],
    statement="Return the number of nodes on the longest root-to-leaf path. An empty tree has depth 0.",
    constraints=["0 <= number of nodes <= 10^4"],
    signature="from typing import List, Optional\n\ndef max_depth(root: List[Optional[int]]) -> int:",
    function_name="max_depth",
    hints=[
        "The depth of a node is 1 plus the deeper child.",
        "A null child has depth 0.",
        "BFS counts layers and returns the number of layers.",
    ],
    approaches=[
        ("BFS layers", "O(n)", "O(n)", "The last layer index is the depth."),
        ("DFS", "O(n)", "O(h)", "One recursive definition."),
    ],
    editorial=(
        "max_depth(null) = 0 and max_depth(node) = 1 + max(max_depth(left), max_depth(right)). "
        "That is the whole algorithm. It is also the template for height-based tree DP."
    ),
    companies=["Amazon", "Microsoft", "Apple", "Google"],
)
def max_depth(root: list) -> int:
    def walk(node) -> int:
        if node is None:
            return 0
        return 1 + max(walk(node.left), walk(node.right))

    return walk(_build(root))


def _oracle_max_depth(root: list) -> int:
    node = _build(root)
    best = 0
    stack = [(node, 1)]
    while stack:
        current, depth = stack.pop()
        if current is None:
            continue
        best = max(best, depth)
        stack.append((current.left, depth + 1))
        stack.append((current.right, depth + 1))
    return best


cases(
    "maximum-depth-of-binary-tree",
    _oracle_max_depth,
    [
        ("classic", {"root": [3, 9, 20, None, None, 15, 7]}, True, "The longest path has three nodes."),
        ("empty", {"root": []}, True, "Depth is 0."),
        ("skew", {"root": [1, 2, None, 3]}, False, None),
        ("single", {"root": [1]}, False, None),
        ("full", {"root": [1, 2, 3]}, False, None),
    ],
)


@define(
    slug="same-tree",
    title="Same Tree",
    difficulty="easy",
    topics=["trees"],
    statement="Return true when two binary trees are structurally identical and have the same node values.",
    constraints=["0 <= number of nodes <= 100"],
    signature="from typing import List, Optional\n\ndef is_same_tree(p: List[Optional[int]], q: List[Optional[int]]) -> bool:",
    function_name="is_same_tree",
    hints=[
        "Both nodes null means this position matches.",
        "Exactly one null, or two different values, means the trees differ.",
        "Otherwise both subtrees must match.",
    ],
    approaches=[
        ("Serialize and compare", "O(n)", "O(n)", "Level order including internal nulls."),
        ("Paired DFS", "O(n)", "O(h)", "Walk both trees with the same recursion."),
    ],
    editorial=(
        "Equality is recursive. Compare the current values, then the left children, then the right children. "
        "Short-circuit on the first mismatch. The null cases are what make structure part of the comparison rather than values alone."
    ),
    companies=["Amazon", "Bloomberg", "Adobe", "Google"],
)
def is_same_tree(p: list, q: list) -> bool:
    def walk(a, b) -> bool:
        if a is None or b is None:
            return a is b
        return a.value == b.value and walk(a.left, b.left) and walk(a.right, b.right)

    return walk(_build(p), _build(q))


def _oracle_is_same_tree(p: list, q: list) -> bool:
    def full(values: list) -> list:
        node = _build(values)
        if node is None:
            return []
        queue = [node]
        out: list = []
        while any(item is not None for item in queue):
            current = queue.pop(0)
            if current is None:
                out.append(None)
                queue.append(None)
                queue.append(None)
            else:
                out.append(current.value)
                queue.append(current.left)
                queue.append(current.right)
        return out

    return full(p) == full(q)


cases(
    "same-tree",
    _oracle_is_same_tree,
    [
        ("yes", {"p": [1, 2, 3], "q": [1, 2, 3]}, True, "The trees match."),
        ("no-value", {"p": [1, 2], "q": [1, None, 2]}, True, "The child is on the other side."),
        ("empty", {"p": [], "q": []}, False, None),
        ("shape", {"p": [1, 2, 3], "q": [1, 2, 4]}, False, None),
        ("single", {"p": [1], "q": [1]}, False, None),
    ],
)


@define(
    slug="symmetric-tree",
    title="Symmetric Tree",
    difficulty="easy",
    topics=["trees"],
    statement="Return true when the binary tree is a mirror of itself around its center.",
    constraints=["1 <= number of nodes <= 1000"],
    signature="from typing import List, Optional\n\ndef is_symmetric(root: List[Optional[int]]) -> bool:",
    function_name="is_symmetric",
    hints=[
        "The tree is symmetric when the left subtree is a mirror of the right subtree.",
        "Two trees are mirrors when their roots match and each left child mirrors the other right child.",
        "A null pair matches. One null does not.",
    ],
    approaches=[
        ("Recursive mirror check", "O(n)", "O(h)", "Compare outside children and inside children."),
        ("BFS pairs", "O(n)", "O(n)", "Enqueue children in mirror order."),
    ],
    editorial=(
        "Call a helper on (left, right). It returns true when both are null, false when one is null or the values differ, "
        "and otherwise checks mirror(left.left, right.right) and mirror(left.right, right.left). "
        "The root itself has no partner. Its two children do."
    ),
    companies=["Amazon", "Microsoft", "Facebook", "LinkedIn"],
)
def is_symmetric(root: list) -> bool:
    node = _build(root)

    def mirror(a, b) -> bool:
        if a is None or b is None:
            return a is b
        return a.value == b.value and mirror(a.left, b.right) and mirror(a.right, b.left)

    return node is None or mirror(node.left, node.right)


def _oracle_is_symmetric(root: list) -> bool:
    node = _build(root)
    if node is None:
        return True
    stack = [(node.left, node.right)]
    while stack:
        a, b = stack.pop()
        if a is None and b is None:
            continue
        if a is None or b is None or a.value != b.value:
            return False
        stack.append((a.left, b.right))
        stack.append((a.right, b.left))
    return True


cases(
    "symmetric-tree",
    _oracle_is_symmetric,
    [
        ("yes", {"root": [1, 2, 2, 3, 4, 4, 3]}, True, "The tree is a mirror."),
        ("no", {"root": [1, 2, 2, None, 3, None, 3]}, True, "The inner children are not mirrored."),
        ("single", {"root": [1]}, False, None),
        ("two", {"root": [1, 2, 2]}, False, None),
        ("values", {"root": [1, 2, 3]}, False, None),
    ],
)


@define(
    slug="binary-tree-level-order-traversal",
    title="Binary Tree Level Order Traversal",
    difficulty="medium",
    topics=["trees", "bfs"],
    statement="Return the level-order traversal as a list of levels, from left to right, top to bottom.",
    constraints=["0 <= number of nodes <= 2000"],
    signature="from typing import List, Optional\n\ndef level_order(root: List[Optional[int]]) -> List[List[int]]:",
    function_name="level_order",
    hints=[
        "BFS with a queue is the definition of level order.",
        "Snapshot the queue length at the start of each layer so you know when the layer ends.",
        "Append node values for that many pops, and push the children.",
    ],
    approaches=[
        ("DFS with depth index", "O(n)", "O(h)", "Append to levels[depth]."),
        ("BFS by layer", "O(n)", "O(n)", "The queue holds one layer plus the next."),
    ],
    editorial=(
        "The queue invariant is that it contains exactly the next layer, left to right. "
        "Record its length, drain that many nodes, and enqueue their children. "
        "Each iteration of the outer loop is one level of the answer."
    ),
    companies=["Amazon", "Microsoft", "Bloomberg", "Facebook"],
)
def level_order(root: list) -> list[list[int]]:
    node = _build(root)
    if node is None:
        return []
    out: list[list[int]] = []
    queue = [node]
    while queue:
        layer: list[int] = []
        nxt = []
        for current in queue:
            layer.append(current.value)
            if current.left:
                nxt.append(current.left)
            if current.right:
                nxt.append(current.right)
        out.append(layer)
        queue = nxt
    return out


def _oracle_level_order(root: list) -> list[list[int]]:
    node = _build(root)
    levels: list[list[int]] = []

    def walk(current, depth: int) -> None:
        if current is None:
            return
        if depth == len(levels):
            levels.append([])
        levels[depth].append(current.value)
        walk(current.left, depth + 1)
        walk(current.right, depth + 1)

    walk(node, 0)
    return levels


cases(
    "binary-tree-level-order-traversal",
    _oracle_level_order,
    [
        ("classic", {"root": [3, 9, 20, None, None, 15, 7]}, True, "Levels are [3], [9, 20], [15, 7]."),
        ("empty", {"root": []}, True, "No levels."),
        ("single", {"root": [1]}, False, None),
        ("skew", {"root": [1, 2, None, 3]}, False, None),
        ("full", {"root": [1, 2, 3, 4, 5, 6, 7]}, False, None),
    ],
)


@define(
    slug="binary-tree-right-side-view",
    title="Binary Tree Right Side View",
    difficulty="medium",
    topics=["trees", "bfs"],
    statement="Imagine standing on the right side of the tree. Return the values of the nodes you can see, from top to bottom.",
    constraints=["0 <= number of nodes <= 100"],
    signature="from typing import List, Optional\n\ndef right_side_view(root: List[Optional[int]]) -> List[int]:",
    function_name="right_side_view",
    hints=[
        "The visible node on a level is the last node of that level in a left-to-right BFS.",
        "A DFS that visits the right child before the left child records the first node seen at each depth.",
        "Both answers are the same list.",
    ],
    approaches=[
        ("BFS last node", "O(n)", "O(n)", "Take the last value of every layer."),
        ("Right-first DFS", "O(n)", "O(h)", "Append when depth equals the answer length."),
    ],
    editorial=(
        "Level order already groups the nodes a viewer would scan. The rightmost node of each group is visible. "
        "The DFS version relies on visit order: the first time a depth is reached from the right, that node hides everything to its left on the same depth."
    ),
    companies=["Amazon", "Facebook", "Bloomberg", "Adobe"],
)
def right_side_view(root: list) -> list[int]:
    levels = level_order(root)
    return [layer[-1] for layer in levels]


def _oracle_right_side_view(root: list) -> list[int]:
    node = _build(root)
    out: list[int] = []

    def walk(current, depth: int) -> None:
        if current is None:
            return
        if depth == len(out):
            out.append(current.value)
        walk(current.right, depth + 1)
        walk(current.left, depth + 1)

    walk(node, 0)
    return out


cases(
    "binary-tree-right-side-view",
    _oracle_right_side_view,
    [
        ("classic", {"root": [1, 2, 3, None, 5, None, 4]}, True, "The right side is 1, 3, 4."),
        ("left-only", {"root": [1, 2, None, 3]}, True, "A left child is visible when nothing is to its right."),
        ("empty", {"root": []}, False, None),
        ("single", {"root": [1]}, False, None),
        ("full", {"root": [1, 2, 3, 4]}, False, None),
    ],
)


@define(
    slug="validate-binary-search-tree",
    title="Validate Binary Search Tree",
    difficulty="medium",
    topics=["trees", "bst"],
    statement=(
        "Return true when the tree is a valid BST. The left subtree of every node contains only smaller keys, "
        "and the right subtree contains only larger keys. Comparing a node with its parent is not enough."
    ),
    constraints=["1 <= number of nodes <= 10^4", "Node values fit in a 32-bit signed integer"],
    signature="from typing import List, Optional\n\ndef is_valid_bst(root: List[Optional[int]]) -> bool:",
    function_name="is_valid_bst",
    hints=[
        "An inorder traversal of a BST is strictly increasing.",
        "Alternatively, carry an exclusive lower and upper bound into each subtree.",
        "The bounds start as negative and positive infinity. A left child tightens the upper bound. A right child tightens the lower bound.",
    ],
    approaches=[
        ("Inorder list", "O(n)", "O(n)", "Check that the sequence is strictly sorted."),
        ("Bound propagation", "O(n)", "O(h)", "Every node is checked against the range inherited from its ancestors."),
    ],
    editorial=(
        "The bug in 'greater than parent' is a node deep in the left subtree that is still larger than the root. "
        "Bounds fix that: every ancestor contributes a constraint. "
        "Inorder works for the same reason: the BST definition is exactly that inorder is sorted."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "Bloomberg"],
)
def is_valid_bst(root: list) -> bool:
    def walk(node, low, high) -> bool:
        if node is None:
            return True
        if not low < node.value < high:
            return False
        return walk(node.left, low, node.value) and walk(node.right, node.value, high)

    return walk(_build(root), float("-inf"), float("inf"))


def _oracle_is_valid_bst(root: list) -> bool:
    values: list[int] = []

    def inorder(node) -> None:
        if node is None:
            return
        inorder(node.left)
        values.append(node.value)
        inorder(node.right)

    inorder(_build(root))
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


cases(
    "validate-binary-search-tree",
    _oracle_is_valid_bst,
    [
        ("yes", {"root": [2, 1, 3]}, True, "A three-node BST."),
        ("no", {"root": [5, 1, 4, None, None, 3, 6]}, True, "3 is in the right subtree of 5 but is smaller than 5."),
        ("single", {"root": [1]}, False, None),
        ("equal", {"root": [2, 2, 2]}, False, None),
        ("deeper", {"root": [5, 4, 6, None, None, 3, 7]}, False, None),
    ],
)


@define(
    slug="kth-smallest-element-in-a-bst",
    title="Kth Smallest Element in a BST",
    difficulty="medium",
    topics=["trees", "bst"],
    statement="Return the kth smallest value in the BST. k is 1-based and always valid.",
    constraints=["1 <= k <= number of nodes <= 10^4"],
    signature="from typing import List, Optional\n\ndef kth_smallest(root: List[Optional[int]], k: int) -> int:",
    function_name="kth_smallest",
    hints=[
        "Inorder visits BST keys in sorted order.",
        "Stop the walk after k nodes. You do not need the whole list.",
        "An iterative stack makes the early exit obvious: pop a node, decrement k, and return when k hits zero.",
    ],
    approaches=[
        ("Collect inorder", "O(n)", "O(n)", "Return the element at index k - 1."),
        ("Early-exit inorder", "O(h + k)", "O(h)", "Stop after the kth visit. A balanced tree makes this O(log n + k)."),
    ],
    editorial=(
        "The inorder successor sequence is the sorted order of a BST. "
        "Walk left, visit, walk right, and count visits. The kth visit is the answer. "
        "Augmenting each node with subtree size would answer later queries in O(h), which is the follow-up interviewers ask."
    ),
    companies=["Amazon", "Google", "Facebook", "Uber"],
)
def kth_smallest(root: list, k: int) -> int:
    stack = []
    node = _build(root)
    while True:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.value
        node = node.right


def _oracle_kth_smallest(root: list, k: int) -> int:
    values: list[int] = []

    def inorder(node) -> None:
        if node:
            inorder(node.left)
            values.append(node.value)
            inorder(node.right)

    inorder(_build(root))
    return values[k - 1]


cases(
    "kth-smallest-element-in-a-bst",
    _oracle_kth_smallest,
    [
        ("classic", {"root": [3, 1, 4, None, 2], "k": 1}, True, "The smallest value is 1."),
        ("second", {"root": [5, 3, 6, 2, 4, None, None, 1], "k": 3}, True, "The sorted order starts 1, 2, 3."),
        ("root", {"root": [2, 1, 3], "k": 2}, False, None),
        ("last", {"root": [2, 1, 3], "k": 3}, False, None),
        ("single", {"root": [1], "k": 1}, False, None),
    ],
)


@define(
    slug="lowest-common-ancestor-of-a-binary-tree",
    title="Lowest Common Ancestor of a Binary Tree",
    difficulty="medium",
    topics=["trees"],
    statement=(
        "Values in the tree are unique. `p` and `q` are values that exist in the tree. "
        "Return the value of their lowest common ancestor. A node may be an ancestor of itself."
    ),
    constraints=["2 <= number of nodes <= 10^5", "All values are unique"],
    signature="from typing import List, Optional\n\ndef lowest_common_ancestor(root: List[Optional[int]], p: int, q: int) -> int:",
    function_name="lowest_common_ancestor",
    hints=[
        "If the current node is p or q, it is a candidate even before you look at the children.",
        "Ask both subtrees. If both return a node, the current node is the LCA.",
        "If only one side returns a node, that node is the LCA of the pair, or the pair lives entirely on that side.",
    ],
    approaches=[
        ("Parent map plus ancestor set", "O(n)", "O(n)", "Walk from p to the root and see where q's path hits that set."),
        ("Single DFS", "O(n)", "O(h)", "The three-way return described above."),
    ],
    editorial=(
        "The DFS returns the LCA if both targets are in the subtree, the target itself if exactly one is in the subtree, and null otherwise. "
        "When left and right are both non-null, the current node is the first place the two targets meet. "
        "When the current node is a target, returning it immediately is correct because the other target is either here or below, and a node is an ancestor of itself."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "LinkedIn"],
)
def lowest_common_ancestor(root: list, p: int, q: int) -> int:
    def walk(node):
        if node is None or node.value in (p, q):
            return node
        left = walk(node.left)
        right = walk(node.right)
        if left and right:
            return node
        return left or right

    return walk(_build(root)).value


def _oracle_lowest_common_ancestor(root: list, p: int, q: int) -> int:
    parent = {}
    node = _build(root)
    stack = [node]
    parent[node] = None
    while stack:
        current = stack.pop()
        for child in (current.left, current.right):
            if child is not None:
                parent[child] = current
                stack.append(child)
    seen = set()
    current = next(item for item in parent if item.value == p)
    while current is not None:
        seen.add(current)
        current = parent[current]
    current = next(item for item in parent if item.value == q)
    while current not in seen:
        current = parent[current]
    return current.value


cases(
    "lowest-common-ancestor-of-a-binary-tree",
    _oracle_lowest_common_ancestor,
    [
        ("classic", {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 1}, True, "The LCA is the root, 3."),
        ("deeper", {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 4}, True, "5 is an ancestor of 4."),
        ("leaves", {"root": [1, 2, 3], "p": 2, "q": 3}, False, None),
        ("self", {"root": [1, 2], "p": 2, "q": 2}, False, None),
        ("chain", {"root": [1, 2, None, 3], "p": 3, "q": 2}, False, None),
    ],
)


@define(
    slug="lowest-common-ancestor-of-a-bst",
    title="Lowest Common Ancestor of a Binary Search Tree",
    difficulty="medium",
    topics=["trees", "bst"],
    statement="Return the LCA of values `p` and `q` in a BST. Both values exist, and all values are unique.",
    constraints=["2 <= number of nodes <= 10^5"],
    signature="from typing import List, Optional\n\ndef lowest_common_ancestor_bst(root: List[Optional[int]], p: int, q: int) -> int:",
    function_name="lowest_common_ancestor_bst",
    hints=[
        "The general binary-tree LCA is correct and does not use the BST property.",
        "If both targets are smaller than the node, the LCA is in the left subtree.",
        "If both are larger, go right. Otherwise the current node splits them and is the LCA.",
    ],
    approaches=[
        ("General tree LCA", "O(n)", "O(h)", "Ignores ordering."),
        ("BST descent", "O(h)", "O(1)", "One path, no recursion required."),
    ],
    editorial=(
        "Assume p <= q by swapping if needed. Walk from the root. "
        "A node smaller than p is too far left, so go right. A node larger than q is too far right, so go left. "
        "The first node that lies between them, inclusive, is the LCA, because one target is in each subtree or the node is a target."
    ),
    companies=["Amazon", "Facebook", "Microsoft", "LinkedIn"],
)
def lowest_common_ancestor_bst(root: list, p: int, q: int) -> int:
    if p > q:
        p, q = q, p
    node = _build(root)
    while node is not None:
        if node.value < p:
            node = node.right
        elif node.value > q:
            node = node.left
        else:
            return node.value
    raise ValueError("missing")


def _oracle_lowest_common_ancestor_bst(root: list, p: int, q: int) -> int:
    return lowest_common_ancestor(root, p, q)


cases(
    "lowest-common-ancestor-of-a-bst",
    _oracle_lowest_common_ancestor_bst,
    [
        ("classic", {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 8}, True, "6 splits 2 and 8."),
        ("descendant", {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 4}, True, "2 is the ancestor of 4."),
        ("leaves", {"root": [2, 1, 3], "p": 1, "q": 3}, False, None),
        ("same", {"root": [2, 1], "p": 1, "q": 1}, False, None),
        ("deep", {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 3, "q": 5}, False, None),
    ],
)


@define(
    slug="diameter-of-binary-tree",
    title="Diameter of Binary Tree",
    difficulty="easy",
    topics=["trees"],
    statement="The diameter is the length of the longest path between any two nodes, measured in edges. The path does not have to pass through the root. Return that length.",
    constraints=["1 <= number of nodes <= 10^4"],
    signature="from typing import List, Optional\n\ndef diameter_of_binary_tree(root: List[Optional[int]]) -> int:",
    function_name="diameter_of_binary_tree",
    hints=[
        "The longest path through a node is the height of the left subtree plus the height of the right subtree, in edges.",
        "The diameter of the tree is the maximum of that quantity over every node.",
        "A height DFS can update a global best on the way back up. Height in edges from a node to its deepest leaf is what you return.",
    ],
    approaches=[
        ("Two DFS passes per node", "O(n^2)", "O(h)", "Recompute heights."),
        ("One DFS", "O(n)", "O(h)", "Height and diameter are computed together."),
    ],
    editorial=(
        "Return the height of a subtree to the parent, and as a side effect record left_height + right_height. "
        "Use edges: a null child contributes height 0, and a leaf returns 1 to its parent if you count nodes, or you can count edges explicitly. "
        "The standard edge formulation returns 1 + max(left, right) as the height in edges from the parent link, and adds the two child heights."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def diameter_of_binary_tree(root: list) -> int:
    best = 0

    def height(node) -> int:
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(_build(root))
    return best


def _oracle_diameter_of_binary_tree(root: list) -> int:
    node = _build(root)
    nodes = []
    stack = [node]
    while stack:
        current = stack.pop()
        if current is None:
            continue
        nodes.append(current)
        stack.append(current.left)
        stack.append(current.right)

    def depth(current) -> int:
        if current is None:
            return 0
        return 1 + max(depth(current.left), depth(current.right))

    best = 0
    for current in nodes:
        left = depth(current.left)
        right = depth(current.right)
        best = max(best, left + right)
    return best


cases(
    "diameter-of-binary-tree",
    _oracle_diameter_of_binary_tree,
    [
        ("classic", {"root": [1, 2, 3, 4, 5]}, True, "The path 4-2-5 or 4-2-1-3 has length 3."),
        ("skew", {"root": [1, 2, None, 3]}, True, "A single path of two edges."),
        ("single", {"root": [1]}, False, None),
        ("two", {"root": [1, 2]}, False, None),
        ("bush", {"root": [1, 2, 3, 4, None, None, 5]}, False, None),
    ],
)


@define(
    slug="balanced-binary-tree",
    title="Balanced Binary Tree",
    difficulty="easy",
    topics=["trees"],
    statement="Return true when the tree is height-balanced. A tree is height-balanced when the depths of the two subtrees of every node differ by at most 1.",
    constraints=["0 <= number of nodes <= 5000"],
    signature="from typing import List, Optional\n\ndef is_balanced(root: List[Optional[int]]) -> bool:",
    function_name="is_balanced",
    hints=[
        "A naive check recomputes height at every node and is quadratic.",
        "Return the height, and use a sentinel such as -1 when a subtree is already unbalanced.",
        "A node is balanced when both children are balanced and their heights differ by at most 1.",
    ],
    approaches=[
        ("Height at every node", "O(n^2)", "O(h)", "Simple and easy to overshoot the time limit."),
        ("Postorder with a sentinel", "O(n)", "O(h)", "One walk returns both facts."),
    ],
    editorial=(
        "If either child returns -1, propagate -1. "
        "If the absolute difference of the two heights exceeds 1, return -1. "
        "Otherwise return 1 + the larger height. The tree is balanced when the root's call does not return -1."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def is_balanced(root: list) -> bool:
    def height(node) -> int:
        if node is None:
            return 0
        left = height(node.left)
        if left < 0:
            return -1
        right = height(node.right)
        if right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(_build(root)) >= 0


def _oracle_is_balanced(root: list) -> bool:
    def check(node):
        if node is None:
            return True, 0
        lok, lh = check(node.left)
        rok, rh = check(node.right)
        ok = lok and rok and abs(lh - rh) <= 1
        return ok, 1 + max(lh, rh)

    return check(_build(root))[0]


cases(
    "balanced-binary-tree",
    _oracle_is_balanced,
    [
        ("yes", {"root": [3, 9, 20, None, None, 15, 7]}, True, "Every node is balanced."),
        ("no", {"root": [1, 2, 2, 3, 3, None, None, 4, 4]}, True, "The left spine is too deep."),
        ("empty", {"root": []}, False, None),
        ("single", {"root": [1]}, False, None),
        ("skew", {"root": [1, 2, None, 3]}, False, None),
    ],
)


@define(
    slug="path-sum",
    title="Path Sum",
    difficulty="easy",
    topics=["trees", "recursion"],
    statement="Return true when the tree has a root-to-leaf path whose values sum to `target_sum`.",
    constraints=["0 <= number of nodes <= 5000"],
    signature="from typing import List, Optional\n\ndef has_path_sum(root: List[Optional[int]], target_sum: int) -> bool:",
    function_name="has_path_sum",
    hints=[
        "Subtract the current value from the target as you descend.",
        "A leaf matches when the remaining target equals the leaf value.",
        "A null node is not a successful path. An empty tree is false.",
    ],
    approaches=[
        ("DFS with remaining sum", "O(n)", "O(h)", "One boolean per subtree."),
        ("BFS with remaining sum", "O(n)", "O(n)", "Carry the remainder in the queue."),
    ],
    editorial=(
        "has_path_sum(null, _) is false. "
        "A leaf returns whether its value equals the remaining target. "
        "An internal node returns true when either child can finish the remainder after subtracting the node value."
    ),
    companies=["Amazon", "Microsoft", "Adobe", "Google"],
)
def has_path_sum(root: list, target_sum: int) -> bool:
    def walk(node, remain: int) -> bool:
        if node is None:
            return False
        remain -= node.value
        if node.left is None and node.right is None:
            return remain == 0
        return walk(node.left, remain) or walk(node.right, remain)

    return walk(_build(root), target_sum)


def _oracle_has_path_sum(root: list, target_sum: int) -> bool:
    node = _build(root)
    stack = [(node, target_sum)]
    while stack:
        current, remain = stack.pop()
        if current is None:
            continue
        remain -= current.value
        if current.left is None and current.right is None and remain == 0:
            return True
        stack.append((current.left, remain))
        stack.append((current.right, remain))
    return False


cases(
    "path-sum",
    _oracle_has_path_sum,
    [
        ("yes", {"root": [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], "target_sum": 22}, True, "5-4-11-2 sums to 22."),
        ("no", {"root": [1, 2, 3], "target_sum": 5}, True, "No root-to-leaf path sums to 5."),
        ("empty", {"root": [], "target_sum": 0}, False, None),
        ("leaf", {"root": [1], "target_sum": 1}, False, None),
        ("neg", {"root": [1, -2, -3, 1, 3, -2, None, -1], "target_sum": -1}, False, None),
    ],
)


@define(
    slug="binary-tree-maximum-path-sum",
    title="Binary Tree Maximum Path Sum",
    difficulty="hard",
    topics=["trees", "dynamic-programming"],
    statement=(
        "A path is any sequence of nodes connected by edges, with no repeated node. It does not have to pass through the root or end at a leaf. "
        "Return the maximum path sum. Node values may be negative."
    ),
    constraints=["1 <= number of nodes <= 3 * 10^4", "-1000 <= Node.val <= 1000"],
    signature="from typing import List, Optional\n\ndef max_path_sum(root: List[Optional[int]]) -> int:",
    function_name="max_path_sum",
    hints=[
        "Split the path at its highest node. That node has a left gain and a right gain.",
        "A gain is max(0, value + best child gain). A negative gain is discarded.",
        "The answer at that node is value + left gain + right gain. The value returned to the parent is value + the better single gain, because a parent path cannot use both children.",
    ],
    approaches=[
        ("All pairs of nodes", "O(n^2)", "O(n)", "Compute the unique path between every pair."),
        ("Tree DP gain", "O(n)", "O(h)", "One postorder computes both the gain and the global best."),
    ],
    editorial=(
        "The function returns the best downward gain starting at this node. "
        "Before returning, it considers the path that bends through the node, which is the only place both children can be used. "
        "Initialize the global best to the root value, not zero, so an all-negative tree returns the largest value."
    ),
    companies=["Amazon", "Google", "Facebook", "Microsoft"],
)
def max_path_sum(root: list) -> int:
    best = [float("-inf")]

    def gain(node) -> int:
        if node is None:
            return 0
        left = max(0, gain(node.left))
        right = max(0, gain(node.right))
        best[0] = max(best[0], node.value + left + right)
        return node.value + max(left, right)

    gain(_build(root))
    return int(best[0])


def _oracle_max_path_sum(root: list) -> int:
    # Independent postorder with explicit negative rejection.
    answer = [None]

    def walk(node):
        if node is None:
            return 0
        left = max(walk(node.left), 0)
        right = max(walk(node.right), 0)
        answer[0] = node.value + left + right if answer[0] is None else max(answer[0], node.value + left + right)
        return node.value + max(left, right)

    walk(_build(root))
    return answer[0]


cases(
    "binary-tree-maximum-path-sum",
    _oracle_max_path_sum,
    [
        ("classic", {"root": [1, 2, 3]}, True, "The path 2-1-3 sums to 6."),
        ("negative", {"root": [-10, 9, 20, None, None, 15, 7]}, True, "The path 15-20-7 sums to 42."),
        ("single", {"root": [-3]}, False, None),
        ("line", {"root": [2, -1]}, False, None),
        ("mixed", {"root": [5, 4, 8, 11, None, 13, 4]}, False, None),
    ],
)


@define(
    slug="house-robber-iii",
    title="House Robber III",
    difficulty="medium",
    topics=["trees", "dynamic-programming"],
    statement=(
        "Houses form a binary tree. Adjacent houses, meaning a parent and its child, cannot both be robbed. "
        "Return the maximum amount you can rob. Every node value is the money in that house."
    ),
    constraints=["1 <= number of nodes <= 10^4", "0 <= Node.val <= 10^4"],
    signature="from typing import List, Optional\n\ndef rob(root: List[Optional[int]]) -> int:",
    function_name="rob",
    hints=[
        "For each subtree, compute two numbers: the best if you rob the root, and the best if you do not.",
        "Robbing the root adds its value to the 'do not rob' results of both children.",
        "Skipping the root takes the better of rob or skip from each child.",
    ],
    approaches=[
        ("Recursion with memo on nodes", "O(n)", "O(n)", "Two states per node."),
        ("Return a pair", "O(n)", "O(h)", "The pair is (rob this node, skip this node)."),
    ],
    editorial=(
        "Let rob_this = value + skip_left + skip_right. "
        "Let skip_this = max(rob_left, skip_left) + max(rob_right, skip_right). "
        "The answer for the subtree is the max of those two. The answer for the tree is that value at the root. "
        "This is the standard tree DP with a binary state."
    ),
    companies=["Amazon", "Google", "Microsoft", "Uber"],
)
def rob(root: list) -> int:
    def walk(node):
        if node is None:
            return 0, 0
        left = walk(node.left)
        right = walk(node.right)
        take = node.value + left[1] + right[1]
        skip = max(left) + max(right)
        return take, skip

    return max(walk(_build(root)))


def _oracle_rob(root: list) -> int:
    def walk(node):
        if node is None:
            return 0, 0
        lt, ls = walk(node.left)
        rt, rs = walk(node.right)
        return node.value + ls + rs, max(lt, ls) + max(rt, rs)

    return max(walk(_build(root)))


cases(
    "house-robber-iii",
    _oracle_rob,
    [
        ("classic", {"root": [3, 2, 3, None, 3, None, 1]}, True, "Rob 3, 3, and 1 for a total of 7."),
        ("other", {"root": [3, 4, 5, 1, 3, None, 1]}, True, "The best total is 9."),
        ("single", {"root": [4]}, False, None),
        ("line", {"root": [2, 1, None, 3]}, False, None),
        ("zeros", {"root": [0, 0, 0]}, False, None),
    ],
)


@define(
    slug="implement-trie",
    title="Implement Trie (Prefix Tree)",
    difficulty="medium",
    topics=["trie", "design"],
    statement=(
        "Simulate a trie of lowercase words. `operations` contains insert, search, and startsWith. "
        "`arguments[i]` is the word or prefix for that call. "
        "insert returns null. search returns whether the word was inserted. startsWith returns whether any inserted word has that prefix."
    ),
    constraints=["1 <= operations.length <= 10^4", "1 <= word.length <= 200", "words are lowercase"],
    signature="from typing import List, Optional\n\ndef trie_ops(operations: List[str], arguments: List[str]) -> List[Optional[bool]]:",
    function_name="trie_ops",
    hints=[
        "Each node owns a map from character to child, plus a boolean that says a word ends here.",
        "insert walks or creates a child for every character and marks the last node.",
        "search requires the end mark. startsWith only requires that the walk succeeds.",
    ],
    approaches=[
        ("Hash set of words plus a prefix scan", "O(total length) worst case per prefix", "O(total length)", "Correct, and slow when many words share prefixes."),
        ("Trie", "O(length) per call", "O(total characters)", "Shared prefixes share nodes."),
    ],
    editorial=(
        "A trie is a deterministic automaton for the inserted strings. "
        "The end mark is separate from the existence of children, because a prefix of an inserted word is not itself inserted unless insert was called on it. "
        "startsWith stops at the last character of the prefix and ignores the end mark."
    ),
    companies=["Amazon", "Google", "Microsoft", "Twitter"],
)
def trie_ops(operations: list[str], arguments: list[str]) -> list[bool | None]:
    root: dict = {}
    out: list[bool | None] = []
    for op, word in zip(operations, arguments):
        node = root
        if op == "insert":
            for ch in word:
                node = node.setdefault(ch, {})
            node["#"] = True
            out.append(None)
        else:
            missing = False
            for ch in word:
                if ch not in node:
                    missing = True
                    break
                node = node[ch]
            if op == "search":
                out.append((not missing) and bool(node.get("#")))
            else:
                out.append(not missing)
    return out


def _oracle_trie_ops(operations: list[str], arguments: list[str]) -> list[bool | None]:
    words: set[str] = set()
    out: list[bool | None] = []
    for op, word in zip(operations, arguments):
        if op == "insert":
            words.add(word)
            out.append(None)
        elif op == "search":
            out.append(word in words)
        else:
            out.append(any(item.startswith(word) for item in words))
    return out


cases(
    "implement-trie",
    _oracle_trie_ops,
    [
        (
            "classic",
            {
                "operations": ["insert", "search", "search", "startsWith", "insert", "search"],
                "arguments": ["apple", "apple", "app", "app", "app", "app"],
            },
            True,
            "app is a prefix before it is inserted, and a word afterward.",
        ),
        (
            "miss",
            {"operations": ["search", "startsWith"], "arguments": ["a", "a"]},
            True,
            "An empty trie rejects both queries.",
        ),
        (
            "prefix-only",
            {"operations": ["insert", "startsWith", "search"], "arguments": ["banana", "ban", "ban"]},
            False,
            None,
        ),
        (
            "two",
            {"operations": ["insert", "insert", "search", "startsWith"], "arguments": ["cat", "car", "car", "ca"]},
            False,
            None,
        ),
    ],
)
