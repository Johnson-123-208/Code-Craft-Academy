"""AVL, red-black trees, segment trees, Fenwick trees, and tries."""

from emit import emit

BAL = r'''
## Why this matters

A binary search tree that is a chain is an expensive linked list. Balanced trees promise that the height stays logarithmic after every insert and delete, so search, insert, delete, successor, and rank stay logarithmic in the worst case. AVL trees keep that promise with a height rule you can check by hand. Red-black trees keep a looser promise that is cheaper to maintain, which is why they show up in library maps such as C++ `std::map` and Java's `TreeMap`. Interviewers at this level rarely ask you to code a full red-black insertion from a blank page. They do ask what "balanced" means, what a rotation is, and why the height bound holds. Those answers are this lesson.

## Intuition

A rotation is a way to pull a node up and push its parent down without changing the inorder sequence. The keys stay in the same sorted order. Only the shape changes, the way you can rehang a mobile so it sits level. AVL trees rehang as soon as some node's two subtrees differ in height by more than one. Red-black trees paint nodes red or black and rehang, or recolor, when a red node sits next to another red node or when the black-height of the paths would disagree. Both schemes stop a chain from forming. AVL stays shorter. Red-black does fewer rotations on an insert.

## Core concept in depth

The height of a null tree is -1 or 0, depending on the convention. Pick one and keep it. This lesson uses height of a null child as 0 and height of a leaf as 1, which matches the binary-tree lesson. The balance factor of a node is the height of the left subtree minus the height of the right subtree. An AVL tree requires every balance factor to be -1, 0, or 1. That local rule implies a global height bound. The shortest AVL tree of height h is built from the shortest trees of height h - 1 and h - 2, which is a Fibonacci recurrence. The height is therefore at most about 1.44 log2(n), a constant times log n. Search is O(log n) in the worst case, with a smaller leading constant than a red-black tree.

A rotation repairs a local imbalance. A right rotation on node y, whose left child is x, makes x the parent. y becomes x's right child. x's old right subtree becomes y's left subtree. A left rotation is the mirror. The inorder sequence is unchanged because the subtree that moves stays between x and y in sorted order. There are four imbalance shapes, named by the side of the heavy child and the heavy grandchild. Left-left means the left child is taller and its left child is taller still: one right rotation at the node. Right-right is one left rotation. Left-right means the left child is taller but its right child is the heavy one: left-rotate the left child, then right-rotate the node. Right-left is the mirror. After the rotation, recompute heights on the way up. Insert walks down, attaches the leaf, and rotates at most once on the way back, at the deepest unbalanced node. Delete may rotate at every level on the way back, still O(log n) rotations.

Red-black trees use color. Every node is red or black. The root is black. Null children are black. A red node has only black children, so there is no red-red edge. Every path from a node to a null descendant contains the same number of black nodes. That last rule is the black-height. It implies the bound. The shortest path is all black. The longest path alternates and is at most twice the black-height. The black-height is at most log2(n + 1). Therefore the height is at most 2 log2(n + 1). Search is O(log n). The tree is less rigidly balanced than AVL, which is the point: insert fixup is a small case analysis of recoloring and at most two rotations.

Insert a red node, which preserves black-height and may create a red-red edge with the parent. If the uncle is red, recolor the parent and uncle black and the grandparent red, and continue at the grandparent. If the uncle is black and the node is an inner grandchild, rotate it to become an outer grandchild. If the uncle is black and the node is an outer grandchild, rotate the grandparent and recolor so the new parent is black and the old parent is red. Delete is the longer case analysis, built from a "double black" deficit that walks up the tree. You should be able to describe insert. You should be able to say that delete exists, restores the same invariants, and is still O(log n). Coding delete from memory under time pressure is how candidates lose the round. Describe it, and code AVL rotations if they want code.

Neither structure replaces a hash table for exact-key expected constant time. They win when you need ordered iteration, successor, predecessor, or rank. A treap uses a random priority and heap order on the priority, with BST order on the key. Rotations restore the heap property. With random priorities the expected height is logarithmic. Skip lists are another randomized ordered map. Mention them as the "expected balance without a painful delete." The advanced module returns to randomized structures briefly.

## Diagram and dry run

```mermaid
flowchart TD
    A[Insert a key and update heights on the way up] --> B{A node has balance outside -1, 0, 1?}
    B -->|Left heavy, left child left heavy| C[Right rotation]
    B -->|Left heavy, left child right heavy| D[Left rotation on the child, then right rotation]
    B -->|Right heavy mirrors| E[Left rotation, or right-then-left]
    B -->|All legal| F[Done]
```

Keys arrive 3, 2, 1 into an empty AVL tree. Insert 3. Insert 2 as the left child. Balance factors are fine. Insert 1 as the left child of 2. Node 3 has balance factor 2. The heavy side is left, and the left child 2 is left-heavy. One right rotation on 3 makes 2 the root, with left child 1 and right child 3. Heights are 2, 1, and 1. Every balance factor is 0 or 1. The inorder sequence is still 1, 2, 3.

A left-right case: keys 3, 1, 2. 2 is the right child of 1, and 3 is left-heavy. Left-rotate 1 first, so 2 becomes the left child of 3 and 1 becomes the left child of 2. Then right-rotate 3. The root is 2. Same sorted order, height two instead of a chain of three.

## Runnable Python

Rotations are the code to have in your fingers. The AVL insert below handles the left-heavy cases and mirrors them for the right-heavy cases. Heights are stored on the node. This is iterative in spirit at each node and recursive along the path, which is the natural shape. A fully iterative AVL insert exists and is harder to read.

```python
class Node:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 1


def height(node: Node | None) -> int:
    return 0 if node is None else node.height


def refresh(node: Node) -> None:
    node.height = 1 + max(height(node.left), height(node.right))


def rotate_right(y: Node) -> Node:
    x = y.left
    assert x is not None
    y.left = x.right
    x.right = y
    refresh(y)
    refresh(x)
    return x


def rotate_left(x: Node) -> Node:
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    refresh(x)
    refresh(y)
    return y


def insert(node: Node | None, key: int) -> Node:
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)
    refresh(node)
    balance = height(node.left) - height(node.right)
    if balance > 1 and key < node.left.key:
        return rotate_right(node)
    if balance > 1 and key > node.left.key:
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if balance < -1 and key > node.right.key:
        return rotate_left(node)
    if balance < -1 and key < node.right.key:
        node.right = rotate_right(node.right)
        return rotate_left(node)
    return node
```

Inserting 3, then 2, then 1 returns a tree whose root key is 2. Inserting 3, then 1, then 2 also returns root 2. The comparisons against `node.left.key` assume the child exists, which it does when the balance factor says that side is heavy. Duplicates are sent right. If your problem forbids duplicates, return the node unchanged when the key is present.

## Complexity and trade-offs

| Structure | Height | Insert rotations | Ordered iteration | Exact lookup |
| --- | --- | --- | --- | --- |
| Plain BST | n in the worst case | none | Theta(n) | Theta(height) |
| AVL | at most about 1.44 log2 n | at most one on insert | Theta(n) | Theta(log n) worst case |
| Red-black | at most 2 log2(n + 1) | O(1) rotations, O(log n) recolors | Theta(n) | Theta(log n) worst case |
| Hash table | not a tree | none | no useful order | Theta(1) expected |
| Treap | expected log n | expected O(log n) | Theta(n) | expected Theta(log n) |

Choose AVL when lookups dominate and you want the tighter height. Choose red-black when inserts and deletes dominate library use and a slightly taller tree is acceptable. Choose a hash table when there is no order. Say the height constant if someone claims all balanced trees are identical.

## Tricks, tips, and patterns

Draw the four shapes before you memorize letters. Left-left is one rotation. Left-right is two. The first rotation turns left-right into left-left. Recompute height at the nodes you moved, bottom first. For red-black, remember "red uncle means recolor, black uncle means rotate." Nulls are black, so a missing uncle is a black uncle. Never claim a plain BST is logarithmic without a balance argument or a random-insertion assumption.

## Common mistakes and edge cases

Forgetting to refresh heights after a rotation, so the next balance factor is stale. Rotating the wrong node. Updating the parent's child pointer and dropping the new subtree root, which is why insert must return the new root of the subtree. Allowing a red-red edge and calling the tree red-black. Forgetting that nulls count as black, and then computing a black-height that ignores leaves. Duplicate keys that bounce between left and right and never settle. An empty tree. A single node, which is a balanced black root. Deleting from an AVL tree and only rotating once, when the deficit can propagate. If you did not study delete, say so and talk about the propagation instead of inventing a rotation.

## Interview notes

Define the balance factor. State the Fibonacci height bound in words: the smallest AVL tree grows like Fibonacci, so the height is logarithmic. Draw a right rotation and name the subtree that changes parent. For red-black, list the four invariants and the 2 log n height. Sketch the red-uncle and black-uncle insert cases. Do not volunteer to code red-black delete. Do code a rotation if asked. Compare with hashing in one sentence so the interviewer knows you would not reach for a tree to solve Two Sum.

## Practice problems

1. [Validate Binary Search Tree](/practice/validate-binary-search-tree) — the property rotations must preserve.
2. [Balanced Binary Tree](/practice/balanced-binary-tree) — the AVL predicate on a plain binary tree, checked once rather than maintained.
3. [Kth Smallest Element in a BST](/practice/kth-smallest-element-in-a-bst) — logarithmic only if the height is logarithmic or you stop early.

## Summary and cheat sheet

- AVL: every balance factor is -1, 0, or 1. Height is under about 1.44 log2 n.
- Left-left: rotate right. Left-right: rotate left on the child, then right on the node. Mirrors for the right side.
- A rotation changes shape and preserves inorder.
- Red-black: root black, nulls black, no red-red edge, equal black-height. Height at most 2 log2(n + 1).
- Insert fixup: red uncle recolors, black uncle rotates.
- Both give worst-case logarithmic search. Hashing is faster for exact keys and gives no order.

## Further reading

- [Wikipedia — AVL tree](https://en.wikipedia.org/wiki/AVL_tree)
- [Wikipedia — Red-black tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
- [Wikipedia — Tree rotation](https://en.wikipedia.org/wiki/Tree_rotation)
- [CLRS, chapters on AVL and red-black trees](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
'''

RANGE = r'''
## Why this matters

Prefix sums answer static range sums. They do not survive updates. A segment tree and a Fenwick tree, also called a binary indexed tree, answer point updates and range sums in logarithmic time. A trie, or prefix tree, stores strings so that a prefix query is proportional to the prefix length rather than to the number of words. These three structures cover a different interview tier than binary search trees: the segment tree and the Fenwick tree are about ranges of an array, and the trie is about shared prefixes. You should be able to implement a Fenwick tree from memory, derive a segment tree from the "split the range in half" idea, and implement trie insert and search without notes.

## Intuition

A segment tree is a tournament bracket. Each internal node stores the winner, or the sum, of a range. The root stores the whole array. The leaves store single elements. A query that covers a node completely takes that node's answer. A query that covers only part of a node asks both children and combines. An update changes a leaf and walks back to the root, recomputing O(log n) nodes. A Fenwick tree stores the same idea in the binary representation of the index. The lowest set bit of an index tells you how far that slot's responsibility extends. There is no explicit tree, only an array and two while-loops. A trie is a tree of characters. Words that share a prefix share the nodes. Lookup fails as soon as a character is missing.

## Core concept in depth

Build a segment tree on a range that you pad to a power of two if that makes the indexing easier, or keep the length general and pass left and right bounds into recursive functions. The recursive build on a segment `[L, R]` creates a leaf when L equals R, and otherwise splits at mid, builds both children, and stores the sum of the children. Query(qL, qR) on a node that covers `[L, R]` returns 0 when the ranges miss, returns the stored sum when the node is completely inside the query, and otherwise returns the sum of the two recursive queries. Update changes the leaf and adds the delta, or sets the leaf and recomputes, on the way back. Each query and update visits O(log n) nodes because the range splits in half and a query touches at most two nodes per level. Memory is about 4n nodes in the recursive layout, or 2n on a padded power of two. Store the tree in an array: the children of index i are 2i and 2i + 1 if you use 1-based indexing.

The same shape stores other associative combinations. Minimum, maximum, gcd, and sum all work, because combining two halves does not depend on order of combination beyond associativity. Assignment updates and range-add updates need lazy propagation: a node remembers a pending update for its whole range and pushes that pending update to its children only when a query or a later update needs to go deeper. Lazy propagation is the technique that makes range-update plus range-query logarithmic. Without it, a range update is a loop of point updates and can be linearithmic or worse. For the first interview, point update and range query are enough. Mention lazy as the next step.

A Fenwick tree keeps an array bit[1..n], 1-based. The responsibility of index i is the range ending at i whose length is the lowest set bit of i. Adding at i walks upward: add the lowest set bit to i, and add the delta to each slot, until i passes n. A prefix sum through i walks downward: add bit[i], then clear the lowest set bit, until i is 0. The lowest set bit of i is `i & -i` in two's complement. A range sum from l to r is prefix(r) - prefix(l - 1). Point update and prefix query are both O(log n). The tree uses n words and a tighter constant than a segment tree, and it is harder to adapt to minimum queries because minimum does not invert: you cannot subtract prefixes. Sum is the Fenwick tree's home. If you need minimum, use a segment tree.

Build a Fenwick tree from an existing array by calling add for each element, which is O(n log n), or by a linear specialized build that you do not need to memorize. The operation problem in this course starts from zeros and applies adds, which matches the loops above.

A trie node is a map from character to child, plus a boolean that says a word ends here. Insert walks the word, creating missing children, and marks the last node. Search walks the word and requires the end mark, so a proper prefix of an inserted word is not a false hit. Starts-with walks the prefix and ignores the end mark. Time is proportional to the word length, with a factor for the map lookup. An array of 26 children makes the lookup a true constant and spends memory on absent letters. A hash map spends memory only on letters that occur. Delete is optional and must not remove nodes that other words still need. Count words through a node if you need delete to be correct, or simply unmark the end bit if leaving dead branches is acceptable.

Word search II is a board backtracking guided by a trie of the dictionary. You prune a path when the trie has no child for the next letter. Without the trie you search the board once per word. With the trie you search the board once for the whole dictionary. The trie lesson and the backtracking lesson meet there.

Bitwise trie of integers, with a child for bit 0 and bit 1, answers maximum XOR pair questions by walking the opposite bit when it exists. It is the same prefix tree on a fixed alphabet of size 2. Mention it as an application, and implement the character trie first.

## Diagram and dry run

```mermaid
flowchart TD
    A["Root covers 0..7, sum of all"] --> B["Left covers 0..3"]
    A --> C["Right covers 4..7"]
    B --> D["Leaves and partial sums"]
    C --> D
    Q[Query 2..5] --> B
    Q --> C
```

Array 1, 3, 5, 7. Build pair sums. Leaves 1, 3, 5, 7. Parents 4 and 12. Root 16. Query from index 1 through 2 is the leaf 3 plus the leaf 5, total 8. The root is not fully covered, the left parent covers indexes 0 and 1 and is not fully covered, the right parent is not fully covered. The query touches both relevant leaves. Update index 2 by adding 10. The leaf 5 becomes 15, its parent becomes 22, the root becomes 26. Two or three nodes change, not the whole array.

Fenwick on the same values, 1-based adds of 1 at index 1, 3 at index 2, 5 at index 3, 7 at index 4. Prefix through 3 is 1 + 3 + 5 = 9. The downward walk uses the lowest set bit rather than visiting every leaf. Check the implementation against this prefix before you trust it.

Trie insert of "cat" and "car". The root grows a child c, then a, then t with an end mark. Inserting "car" reuses c and a, and adds r with an end mark. Search "ca" fails because a is not an end. Starts-with "ca" succeeds. Search "cat" succeeds.

## Runnable Python

The Fenwick tree is the one to reproduce under pressure. The trie insert and search are the other. The segment tree is recursive and clear. All three are iterative at the operation level except the segment tree, whose recursion is the range split and is logarithmic so the stack is safe.

```python
class Fenwick:
    def __init__(self, n: int) -> None:
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index: int, delta: int) -> None:
        index += 1
        while index <= self.n:
            self.bit[index] += delta
            index += index & -index

    def prefix(self, index: int) -> int:
        index += 1
        total = 0
        while index > 0:
            total += self.bit[index]
            index -= index & -index
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix(right) - (self.prefix(left - 1) if left else 0)


class Trie:
    def __init__(self) -> None:
        self.children: dict[str, Trie] = {}
        self.end = False

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.end = True

    def search(self, word: str) -> bool:
        node = self
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.end

    def starts_with(self, prefix: str) -> bool:
        node = self
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

Mark `end` only after the loop. If you mark it on every character, a proper prefix looks like a stored word. After `insert("cat")`, `search("ca")` is false and `search("cat")` is true. Fenwick `add(0, 1)`, `add(1, 3)`, `add(2, 5)` makes `range_sum(0, 2)` equal 9.

## Complexity and trade-offs

| Structure | Point update | Range sum | Memory | Best at |
| --- | --- | --- | --- | --- |
| Prefix array | Theta(n) rebuild | Theta(1) | Theta(n) | Static arrays |
| Fenwick | Theta(log n) | Theta(log n) | Theta(n) | Sums |
| Segment tree | Theta(log n) | Theta(log n) | Theta(n) | Sum, min, max, lazy range updates |
| Trie | insert Theta(length) | prefix Theta(length) | proportional to the number of distinct prefixes | Strings and bit prefixes |

A segment tree can do what a Fenwick tree can do for sums, with more code and more memory. A Fenwick tree cannot do lazy range assignment cleanly without extra technique. Start with Fenwick for sums. Move to a segment tree when the combine is not an invertible sum or when updates cover a range. A hash set of the inserted words answers search and does not answer "is this prefix a prefix of any word?" without scanning. That scan is why the trie exists.

## Tricks, tips, and patterns

Fenwick indexes in the loops are 1-based even if the problem is 0-based. Convert at the boundary. `i & -i` is the lowest set bit. Range sum subtracts the prefix before the left endpoint. Segment-tree queries return early on a total miss and a total cover. Do not walk to the leaves when the node is fully inside the query. Trie end marks belong on the last character only. Share nodes across words. For a board search, unmark visited cells and also decide whether a word may be used twice. Store a set of found words so a word is emitted once.

## Common mistakes and edge cases

The broken end-mark bug above. Off-by-one in Fenwick conversion so index 0 updates bit slot 0, which the downward loop never reads, and the update vanishes. Using `index &= index - 1` and `index += index & -index` on a mix of languages where negative numbers are not two's complement. Python's negative integers still satisfy `i & -i` for the lowest set bit of a positive i. Do not call it on 0. Query ranges where left is 0 must not call prefix(-1). The code above special-cases that. Segment trees that forget the "completely outside" case and add a child's sum anyway. Lazy flags that are pushed twice or never pushed before a read. Empty trie search of the empty string: define it. Usually the empty string is stored only if it was inserted, and the root's end mark says so. A single-element Fenwick. Updates that set a value rather than add a delta: set is "add the difference from the old value," so you must remember the old value.

## Interview notes

For sums with updates, say Fenwick and write the two loops. Explain the lowest set bit in one sentence even if you do not prove the coverage. For minima or for range updates, say segment tree, draw one split, and write the query's three cases: miss, cover, partial. For strings, draw "cat" and "car" sharing two nodes and mark the ends. Mention the false end-mark bug as something you are careful about. If the problem is Word Search II, say the trie prunes the board search. Give complexities in log n or in word length, not in a vague "tree so log."

## Practice problems

1. [Fenwick Range Sum](/practice/fenwick-range-sum) — the two loops, tested against a plain array.
2. [Implement Trie](/practice/implement-trie) — insert, search, and prefix.
3. [Word Search](/practice/word-search) — the board half of the trie search. The dictionary half is the trie.
4. [Subarray Sum Equals K](/practice/subarray-sum-equals-k) — the static cousin, a prefix hash, so you can say why you did not build a tree.

## Summary and cheat sheet

- Segment tree: each node is a range. Query uses miss, full cover, or both children. Update recomputes a path of length log n.
- Lazy propagation pushes pending range updates down. Use it when updates are ranges.
- Fenwick: add walks up by the lowest set bit, prefix walks down by clearing it. Range sum is a difference of prefixes. Sums, not minima.
- Trie: one node per character, shared prefixes, an end mark only on the last character.
- Insert and search cost the word length. Prefix tests do not require the end mark.
- Prefix arrays win when the array is static. Hash sets win when the question is exact membership of a whole word.

## Further reading

- [Wikipedia — Segment tree](https://en.wikipedia.org/wiki/Segment_tree)
- [Wikipedia — Fenwick tree](https://en.wikipedia.org/wiki/Fenwick_tree)
- [Wikipedia — Trie](https://en.wikipedia.org/wiki/Trie)
- [CP-Algorithms, Fenwick tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CP-Algorithms, segment tree](https://cp-algorithms.com/data_structures/segment_tree.html)
'''

emit(
    "08-trees",
    "03-avl-and-red-black.mdx",
    title="AVL and Red-Black Trees",
    slug="avl-and-red-black",
    summary="Balance factors, the four rotations, and the color invariants that keep a search tree logarithmic.",
    duration=40,
    difficulty="advanced",
    prerequisites=["bst-lca-and-serialization"],
    tags=["avl", "red-black", "trees"],
    order=3,
    body=BAL,
)
emit(
    "08-trees",
    "04-segment-fenwick-and-tries.mdx",
    title="Segment Trees, Fenwick Trees, and Tries",
    slug="segment-fenwick-and-tries",
    summary="Logarithmic range sums, the lowest-set-bit tree, and prefix trees for strings.",
    duration=45,
    difficulty="advanced",
    prerequisites=["avl-and-red-black"],
    tags=["segment-tree", "fenwick", "trie"],
    order=4,
    body=RANGE,
)
