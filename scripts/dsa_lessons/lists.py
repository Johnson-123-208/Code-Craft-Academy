"""Linked-list fundamentals and the classic pointer patterns."""

from emit import emit

FUND = r'''
## Why this matters

Linked lists are where pointer manipulation stops being a metaphor. Arrays give you indexes and contiguous memory. A list gives you a node, a next reference, and no way to jump to the middle. Interviewers use that constraint to see whether you can rewire links without losing the rest of the chain, whether you remember a dummy head, and whether you can reverse a list both iteratively and recursively. The same node shape returns inside LRU caches, graph adjacency lists, and separate chaining. If the pointer code is shaky, those designs are shaky too.

## Intuition

A list is a treasure hunt. Each slip of paper holds a value and the location of the next slip. You cannot look ahead two slips without following the first. If you overwrite a location before you have saved it, the rest of the hunt is gone. Every correct list algorithm is a discipline about which references you save before you overwrite. A dummy node before the head is a fixed slip that you planted yourself, so the first real node can be inserted or deleted with the same code as any other node.

## Core concept in depth

A singly linked node stores a value and a next pointer. The next pointer of the last node is null. The head is the first node. A tail pointer, if you keep one, is the last node and makes append constant time. Without a tail, append is linear because you must walk. A doubly linked node also stores prev. That extra word lets you delete a node in constant time when you already hold it, which is why LRU caches use doubly linked lists. A circular list points the last node at the first. Traversal then needs an explicit stop, usually "back to the start," or it loops forever.

Traversal is a loop: start at the head, and while the node is not null, visit it and step to next. The recursive form visits the node and then calls itself on next, with null as the base case. Both are Theta(n) time. The loop uses constant extra memory. The recursion uses Theta(n) stack. Prefer the loop unless the recursive shape matches the problem, as it does for a reverse that processes the tail first.

Insertion after a known node is constant time: the new node's next becomes the known node's next, then the known node's next becomes the new node. The order of those two assignments matters. Doing them backwards loses the rest of the list. Deletion of the successor of a known node is also constant time: point the known node at its successor's successor. Deletion of a node given only that node, in a singly linked list, is not a true deletion. The usual trick copies the successor's value forward and deletes the successor, which fails on the last node and corrupts any external pointer to the successor. Say that limitation if the prompt asks for it.

A dummy head's next pointer is the real head. Algorithms that might delete or replace the first node write their answer into dummy.next and return that at the end. Merge, reverse-between, and remove-nth-from-end all get simpler with a dummy, because the head stops being a special case.

Iterative reverse uses three pointers: previous, current, and next. previous starts null. While current exists, save current.next, point current.next at previous, then step both previous and current forward. When current becomes null, previous is the new head. The invariant: previous is the head of the reversed prefix, current is the head of the untouched suffix, and those two chains are disjoint. Recursive reverse asks the tail to reverse itself and return the new head, then points the successor back at the current node and clears the current node's next so it becomes the new tail. The recursive call happens before the rewiring. The base case is a null or a single node, which is already reversed. The recursive version is elegant and uses linear stack. The iterative version is the one you want in production and the one you should write first in an interview.

Reversing only a sublist uses the same three-pointer loop for a fixed number of steps, after a dummy has walked you to the node before the sublist. You must reconnect the node before the sublist to the new sublist head, and reconnect the original sublist head, which is now the tail, to the node that followed the sublist. That is four links, and it is the entire problem.

Running time of a walk is proportional to the number of nodes you touch. Random access is linear, unlike an array. Extra memory is the storage of the nodes themselves, which is Theta(n), plus whatever pointers your algorithm adds. In problems in this course the public input is often an array of values, and the reference solution builds nodes so the rewiring is real. You should still talk about pointers, not about swapping values in an array, when the prompt says to reorder the list.

## Diagram and dry run

```mermaid
flowchart LR
    P[previous] --> C[current]
    C --> N[saved next]
    N --> R[rest of the list]
    C -.->|rewire next| P
```

Reverse 1, 2, 3. previous starts null. current starts at 1.

| Step | previous | current | saved next | List shape after the rewire |
| --- | --- | --- | --- | --- |
| 1 | null | 1 | 2 | 1 points at null. 2 still points at 3 |
| 2 | 1 | 2 | 3 | 2 points at 1. 1 points at null |
| 3 | 2 | 3 | null | 3 points at 2. The chain is 3, 2, 1 |
| 4 | 3 | null |  | previous is the new head |

The recursive reverse on the same list reverses 2, 3 first into 3, 2, then points 2 back at 1 and clears 1's next. The new head, 3, is returned all the way up.

## Runnable Python

Both reverses are here. The iterative function is the interview default. The recursive function returns the new head and rewires on the way back. A tiny Node class makes the code runnable without a framework.

```python
class Node:
    def __init__(self, value: int, nxt: "Node | None" = None) -> None:
        self.value = value
        self.nxt = nxt


def reverse_iter(head: Node | None) -> Node | None:
    prev = None
    cur = head
    while cur is not None:
        nxt = cur.nxt
        cur.nxt = prev
        prev = cur
        cur = nxt
    return prev


def reverse_rec(head: Node | None) -> Node | None:
    if head is None or head.nxt is None:
        return head
    new_head = reverse_rec(head.nxt)
    head.nxt.nxt = head
    head.nxt = None
    return new_head
```

Build 1 to 2 to 3, reverse it either way, and walk the result. You should visit 3, then 2, then 1, and then null. If you see a cycle, the recursive version failed to clear head.nxt, or the iterative version pointed a node at itself.

## Complexity and trade-offs

| Operation | Singly linked, no extra index | Array |
| --- | --- | --- |
| Index the i-th element | Theta(i) | Theta(1) |
| Insert or delete after a known node | Theta(1) | Theta(n) to shift |
| Append with a tail pointer | Theta(1) | Amortized Theta(1) |
| Reverse | Theta(n) time, Theta(1) extra if iterative | Theta(n) time, Theta(1) extra |
| Recursive reverse stack | Theta(n) | not applicable |

Use a list when you have the node and you need splices, or when the problem forces you to. Use an array when you need random access or cache locality. A doubly linked list spends another pointer per node and gains constant-time deletion given the node. That trade is correct for an LRU and wasteful for a simple stack of numbers.

## Tricks, tips, and patterns

Save next before you overwrite it. Plant a dummy when the head might change. Draw three boxes and label previous, current, and next before you reverse. For a sublist reverse, identify the four endpoints by name: the node before the range, the original start, the original end, and the node after the range. After the inner reverse, the original start is the tail. Test a one-node list, a two-node list, and a reverse of the entire list. Those three catch most pointer bugs.

## Common mistakes and edge cases

Losing the rest of the list by overwriting next too early. Returning the old head after a reverse. Forgetting that a recursive reverse must set the original head's next to null, so the new tail does not point into the reversed chain and form a cycle. Off-by-one when reversing between positions that are 1-based in the statement and 0-based in your head. A dummy that you forget to skip when you return the answer. Null head. Single node. Deleting the last node with the "copy the successor" trick. Comparing nodes by value when the problem identity is the node itself, which matters for cycles and intersection.

## Interview notes

Talk in pointers. "I save next, point current at previous, and advance." Offer both the loop and the recursion, and say the stack cost of the recursion without being asked. If the input on the platform is an array, say "I will build nodes so the algorithm rewires next, then read the values back." Do not reverse by swapping values unless the prompt explicitly allows it. Dry-run three nodes. Mention the dummy for any problem that deletes the head.

## Practice problems

1. [Reverse Linked List](/practice/reverse-linked-list) — write both versions.
2. [Reverse Linked List II](/practice/reverse-linked-list-ii) — a bounded reverse.
3. [Remove Nth From End](/practice/remove-nth-node-from-end) — a dummy plus a gap of n.
4. [Middle of the Linked List](/practice/middle-of-the-linked-list) — the slow and fast pointers return in the next lesson.
5. [Merge Two Sorted Lists](/practice/merge-two-sorted-lists).

## Summary and cheat sheet

- A node is a value plus next. The last next is null. Doubly linked nodes also store prev.
- Save a pointer before you overwrite it.
- A dummy head removes the special case at the front.
- Iterative reverse uses previous, current, and a saved next. The new head is previous.
- Recursive reverse rewires on the way back and must clear the new tail's next.
- Random access is linear. Splices, given the node, are constant time.
- Recursive walks use linear stack. Loops do not.

## Further reading

- [Wikipedia — Linked list](https://en.wikipedia.org/wiki/Linked_list)
- [Wikipedia — Doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list)
- [CLRS, elementary data structures](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
'''

PATTERNS = r'''
## Why this matters

Once you can reverse a list, the interview problems are compositions: find the middle, reverse one half, merge, detect a cycle, copy a node that has a second random pointer. Each composition has a famous pointer trick. Fast and slow pointers find the middle and detect cycles. A fixed gap between two pointers finds the nth node from the end. Merging is a dummy plus the smaller head. Copying a list with random pointers is either a hash map from old node to new node, or an interleaved weave that uses no extra map. You should be able to implement the linear ones and explain Floyd's meeting point without hand-waving.

## Intuition

Two walkers on a circular track, one moving twice as fast as the other, will meet if there is a loop and will never meet if the track is a straight line that ends. That is Floyd's cycle test. The same speed difference finds the middle of a straight list: when the fast walker falls off the end, the slow walker is about halfway. A gap of n between two walkers who then move in lockstep leaves the slow walker n steps from the end when the fast walker finishes. None of these need indexes. They need the discipline of moving the fast walker first, so it has somewhere to go, and of stopping when a next pointer is null.

## Core concept in depth

The middle of a list: slow and fast both start at the head. While fast and fast.next both exist, step slow once and fast twice. When the loop ends, slow is the middle. On an even-length list this version returns the second of the two middle nodes, because fast starts on the head and the loop continues while a pair of steps remains. Starting fast one node ahead returns the first middle. Know which one you need. Reorder List wants the start of the second half, which is the node after the first middle, so it uses the "fast starts ahead" split and then cuts the list.

Cycle detection: slow and fast start at the head. Move slow once and fast twice. If fast reaches null, there is no cycle. If slow and fast land on the same node, there is a cycle. Correctness: inside a cycle of length c, the fast walker gains one step per iteration on the slow walker, so it catches up. If there is no cycle, fast hits the end.

The start of the cycle is the subtle part. Let the head-to-cycle distance be a, and let the meeting point be b steps into the cycle. When the walkers meet, the fast walker has traveled twice as far as the slow walker, and the extra distance is a whole number of loops. A short derivation shows that a equals some number of full loops minus b, which means: if you put one walker back at the head and leave the other at the meeting point, and you move both one step at a time, they meet at the cycle entrance. Implement that second phase. It is the whole of Linked List Cycle II. The proof is worth re-deriving once so you are not reciting a ritual.

Remove nth from the end: plant a dummy. Move a fast pointer n steps ahead of the dummy. Then move fast and a slow pointer together until fast's next is null. Slow is the node before the one to delete. Point slow at slow.next.next. The dummy makes deleting the head ordinary. The gap is n plus the dummy's head start, which is why you count carefully on a two-node example.

Merge two sorted lists: dummy, and a tail that starts at the dummy. While both lists remain, append the smaller head to the tail and advance that list. Append whichever list remains. Return dummy.next. Merge k lists uses a heap of the current heads, keyed by value, or it merges them like merge sort in pairs. The heap is Theta(n log k) for n total nodes. The pairwise merge is the same bound. A linear scan of k heads per output node is Theta(n k) and loses.

Palindrome list: find the middle, reverse the second half, compare the two halves in lockstep, and optionally reverse the second half back so the list is unchanged. The comparison fails fast on a mismatch. The extra memory is constant. Copying the values into an array is correct and uses linear memory. Say which one you are doing.

Reorder list: split at the middle, reverse the second half, then weave one node from each half. The weave saves both next pointers before it rewires. Stop when the second half is exhausted. An odd-length list leaves the middle node at the end of the first half.

Copy with random pointers. The map version creates every clone, stores old-to-new, then assigns each clone's next and random by lookup. Two passes, linear extra memory. The weave version inserts each clone immediately after its original, assigns random by jumping original.random.next, which is the clone of the random target, then unweaves the two lists. Linear time, constant extra memory beyond the output. The weave is easy to get wrong at the unweave step. Test a random pointer that is null, one that points at the node itself, and one that points backward.

Add Two Numbers is a merge with a carry. Dummy, walk both lists, add the two digits and the carry, append the units digit, and keep the tens digit as the next carry. Do not stop while a carry remains even if both lists have ended.

Odd-even list rewires nodes so odd positions precede even positions, preserving relative order. Two tails, one for each parity, and a saved head of the even chain, are enough. Attach the even head after the odd tail at the end.

Swap in pairs is a reverse of every group of two. Reverse Nodes in k-Group is the general version: count k nodes, reverse that group with the iterative reverse, reconnect, and leave a short tail alone. A dummy makes the first group normal. The inner reverse must know the node after the group so the reversed tail stays connected.

## Diagram and dry run

```mermaid
flowchart TD
    A[Fast and slow at the head] --> B{Fast can take two steps?}
    B -->|Yes| C[Slow takes one. Fast takes two]
    C --> D{They occupy the same node?}
    D -->|Yes| E[Cycle. Reset one walker to the head]
    D -->|No| B
    B -->|No| F[No cycle. Slow is at the middle of a finite list]
    E --> G[Move both one step until they meet. That node starts the cycle]
```

Cycle example. Nodes 1 to 2 to 3 to 4, and 4 points at 2. The entrance is 2.

| Phase | Slow | Fast | Note |
| --- | --- | --- | --- |
| Start | 1 | 1 | |
| Move | 2 | 3 | |
| Move | 3 | 2 | 4 goes to 2 |
| Move | 4 | 4 | They meet at 4 |
| Reset | 1 | 4, the meeting node | Second phase, one step each |
| Move | 2 | 2 | They meet at the entrance |

A list with no cycle, 1 to 2 to 3, ends when fast cannot move, and slow sits on 2, the middle.

## Runnable Python

Floyd's second phase is the piece to implement carefully. The merge is the other workhorse. Both are iterative. A recursive merge exists and is a one-liner on the smaller head, with linear stack. It is included so you can compare.

```python
class Node:
    def __init__(self, value: int, nxt: "Node | None" = None) -> None:
        self.value = value
        self.nxt = nxt


def cycle_start(head: Node | None) -> Node | None:
    slow = fast = head
    while fast is not None and fast.nxt is not None:
        slow = slow.nxt
        fast = fast.nxt.nxt
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.nxt
                fast = fast.nxt
            return slow
    return None


def merge(a: Node | None, b: Node | None) -> Node | None:
    if a is None or b is None:
        return a or b
    if a.value <= b.value:
        a.nxt = merge(a.nxt, b)
        return a
    b.nxt = merge(a, b.nxt)
    return b
```

The recursive merge is correct and uses stack proportional to the total length. An interview can ask you to rewrite it with a dummy and a loop. Do that rewrite if they ask for constant extra memory. `cycle_start` returns the entrance node, or null when the walk reaches the end. Identity is `is`, not value equality. Two nodes can hold the same number and still be different objects.

## Complexity and trade-offs

| Pattern | Time | Extra space |
| --- | --- | --- |
| Middle, fast and slow | Theta(n) | Theta(1) |
| Cycle test and entrance | Theta(n) | Theta(1) |
| Nth from end | Theta(n) | Theta(1) |
| Merge two lists, iterative | Theta(n) | Theta(1) |
| Merge two lists, recursive | Theta(n) | Theta(n) stack |
| Merge k lists with a heap | Theta(n log k) | Theta(k) |
| Palindrome by reversing the half | Theta(n) | Theta(1) |
| Copy random, hash map | Theta(n) | Theta(n) |
| Copy random, weave | Theta(n) | Theta(1) extra |

The array-copy versions are easier and use linear memory. Offer the constant-space version when the prompt or the interviewer asks for it. Do not sacrifice correctness for the weave if you cannot finish the unweave. A correct map solution beats a broken clever one.

## Tricks, tips, and patterns

Move fast first in your mind: the loop condition must look at fast.next before you touch fast.next.next. For the entrance proof, remember the reset. One phase only tells you that a cycle exists. For k-group reverse, count k with a scout pointer before you reverse, and abort the reverse when the scout falls off, so a short tail stays put. For the weave copy, the clone of a node is node.next after the interleave, and the clone of node.random is node.random.next. Write those two sentences on the board. Restore a palindrome list if the caller still needs the original order. Say so.

## Common mistakes and edge cases

Comparing nodes by value inside a cycle test. Fast and slow meeting at the entrance by luck on one example and failing on another, because you skipped the reset phase. Off-by-one on the middle of an even list, which shifts the entire reorder. Losing a next pointer during the weave. A k-group that reverses a short tail. Forgetting the final carry in Add Two Numbers. A random pointer to self, which the weave handles only if you assign random after every clone has been inserted. Null head. A cycle that starts at the head, where a is 0, and the reset phase must still work. Two lists that merge, in the intersection problem, which is a different "meet" and is solved by equalizing lengths or by the cycle trick of connecting one tail to the other head. Do not confuse that problem with Floyd.

## Interview notes

Name the pattern, then the invariant, then the code. "Fast moves twice as fast, so the meeting point encodes the head distance. I reset one pointer to the head and walk in lockstep." Dry-run the four-node cycle above. It is short and it uses both phases. For merge, mention the dummy and the leftover list. For k lists, give the heap bound. If you only have time for one clever algorithm, make it Floyd, and do the ordinary merges with a dummy. Interviewers forgive a simple merge. They do not forgive a cycle test that loops forever.

## Practice problems

1. [Linked List Cycle](/practice/linked-list-cycle) and [Linked List Cycle II](/practice/linked-list-cycle-ii).
2. [Reorder List](/practice/reorder-list) and [Palindrome Linked List](/practice/palindrome-linked-list).
3. [Copy List with Random Pointer](/practice/copy-list-with-random-pointer).
4. [Swap Nodes in Pairs](/practice/swap-nodes-in-pairs) and [Reverse Nodes in k-Group](/practice/reverse-nodes-in-k-group).
5. [Odd Even Linked List](/practice/odd-even-linked-list) and [Add Two Numbers](/practice/add-two-numbers).
6. [Merge K Sorted Lists](/practice/merge-k-sorted-lists).

## Summary and cheat sheet

- Fast and slow find the middle and detect cycles. The entrance needs a second phase with one walker reset to the head.
- A gap of n finds the node before the nth from the end. Use a dummy if the head might disappear.
- Merge with a dummy. Merge k lists with a heap in n log k.
- Palindrome and reorder are split, reverse the second half, then compare or weave.
- Copy random pointers with a map, or weave clones and use original.random.next.
- k-group reverse counts k nodes before it reverses, and it leaves a short tail.
- Pointer identity is object identity, not value equality.

## Further reading

- [Wikipedia — Cycle detection](https://en.wikipedia.org/wiki/Cycle_detection)
- [Wikipedia — Floyd's tortoise and hare, inside cycle detection](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)
- [CLRS, elementary data structures](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
'''

emit(
    "04-linked-lists",
    "01-linked-list-fundamentals.mdx",
    title="Linked List Fundamentals",
    slug="linked-list-fundamentals",
    summary="Nodes, dummy heads, and reversal by pointer rewiring, both as a loop and as a recursion.",
    duration=35,
    difficulty="intermediate",
    prerequisites=["lru-and-lfu"],
    tags=["linked-lists", "pointers"],
    order=1,
    body=FUND,
)
emit(
    "04-linked-lists",
    "02-linked-list-patterns.mdx",
    title="Linked List Patterns",
    slug="linked-list-patterns",
    summary="Fast and slow pointers, Floyd's cycle entrance, merges, k-group reverse, and random-pointer copies.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["linked-list-fundamentals"],
    tags=["linked-lists", "two-pointers", "floyd"],
    order=2,
    body=PATTERNS,
)
