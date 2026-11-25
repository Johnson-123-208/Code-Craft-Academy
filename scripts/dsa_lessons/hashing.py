"""Hash maps, sets, LRU, and LFU."""

from emit import emit

MAPS = r'''
## Why this matters

A hash map turns a repeated linear search into an expected constant-time lookup. That single trade, linear memory for a faster question, is the difference between an accepted solution and a timeout on a large fraction of array and string problems. Two Sum, anagrams, subarray sums, longest consecutive runs, and the first unique character are the same idea wearing different masks: store what you have already seen, in a form that answers the next question immediately. You also need the honesty that comes with the structure. Expected constant time is not worst-case constant time. Interviewers listen for that word.

## Intuition

A hash function assigns each key a bucket, like a postal code. Keys that share a postal code sit together in a short list, or they probe for another slot. If the function scatters keys evenly and the table is not overcrowded, the list in a bucket is short, usually a handful of items, and finding a key does not depend on how many keys exist in total. The moment every key lands in one bucket, the structure is just a list and the lookup is linear. Good libraries rehash and resize to avoid that on ordinary data. Adversarial keys can still force collisions if the hash is predictable. Python randomizes its string hash per process for that reason.

## Core concept in depth

A hash table stores pairs of key and value. The hash code of the key selects a bucket index, typically by reducing an integer modulo the number of buckets. A collision is two keys that reduce to the same bucket. Chaining keeps a list or a tree in each bucket. Open addressing keeps one item per slot and searches a probe sequence, such as linear probing or double hashing, until it finds the key or an empty slot. Deletion under open addressing cannot simply empty a slot, or later probes will stop too early. It leaves a tombstone. Chaining deletes from the list and has no tombstone problem. Python's dict is a compact open-addressing table with a perturbation probe, and it remembers insertion order. For interviews you may treat dict and set operations as expected constant time, and you should say "expected."

The load factor is the number of keys divided by the number of buckets. When it passes a threshold, the table allocates a larger bucket array and reinserts every key. One insertion can therefore be linear. A sequence of n insertions, with geometric growth, is amortized linear, by the same credit argument as a doubling array. That is why building a map of n keys is expected linear overall, not expected quadratic. The worst case of one insertion remains linear. Mention both if the interviewer is pushing.

Equality and hashing must agree. If two keys compare equal, they must have the same hash. If you define equality on a custom object and forget the hash, the object is unusable as a key. Mutable keys are a bug: if the hash changes after insertion, the table looks in the wrong bucket. Use tuples, strings, numbers, or other immutable keys. A list is not a key. A tuple of the list's items is.

The interview patterns are small. A frequency map counts items. A set answers membership. An index map answers "where did I see this key?" Grouping anagrams uses the sorted tuple of characters, or a count tuple of length 26, as the key, and appends the original word to that bucket. Longest consecutive sequence inserts every value into a set, then starts a run only at a value whose predecessor is absent, and walks forward. Each value is the start of at most one run and is visited at most once inside a run, so the scan is linear even though there is a nested walk. Four Sum II counts pair sums of the first two arrays and asks, for every pair from the last two, how many stored sums hit the negation. That is the hash version of splitting a 4-sum.

Subarray sum equals k, from the prefix lesson, is a hash map from prefix sum to frequency. Isomorphic strings and word patterns are two maps, or one map and a set, enforcing a bijection: if a maps to b, a must not later map to c, and b must not be the image of a different letter. A single map is not enough, because two letters can collide on one image.

Hash sets do not store values, only keys. Use a set when the payload would only be true. Use a map when you need a count, an index, or a list. Iteration order of a set is not a contract you should depend on, even if a particular Python version looks stable. If the problem wants a sorted answer, sort at the end. If it wants the first index, store the index, do not hope that iteration order matches insertion in a set you rebuilt.

## Diagram and dry run

```mermaid
flowchart LR
    A[Key] --> B[Hash function]
    B --> C[Bucket index]
    C --> D{Key already in this bucket?}
    D -->|Yes| E[Update the value]
    D -->|No| F[Insert the pair]
    F --> G{Load factor too high?}
    G -->|Yes| H[Allocate more buckets and reinsert]
    G -->|No| I[Done]
    H --> I
```

Group the words eat, tea, tan, ate, nat, bat by anagram. The key is the sorted spelling.

| Word | Key | Bucket after insertion |
| --- | --- | --- |
| eat | aet | aet holds eat |
| tea | aet | aet holds eat, tea |
| tan | ant | ant holds tan |
| ate | aet | aet holds eat, tea, ate |
| nat | ant | ant holds tan, nat |
| bat | abt | abt holds bat |

The values of the map, sorted by key if the contract wants a canonical order, are the groups. Building the keys is n times k log k for word length k, which dominates the hashing when words are long. A count tuple of 26 letters avoids the sort and costs n times k.

## Runnable Python

The anagram grouper is iterative. The recursive counter below is a teaching version of a frequency map over a list. It is not faster. It shows that a fold and a loop compute the same map.

```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    buckets: dict[tuple[str, ...], list[str]] = {}
    for word in words:
        key = tuple(sorted(word))
        buckets.setdefault(key, []).append(word)
    return [sorted(group) for group in sorted(buckets.values(), key=lambda group: group[0])]


def frequencies(nums: list[int]) -> dict[int, int]:
    def go(i: int, acc: dict[int, int]) -> dict[int, int]:
        if i == len(nums):
            return acc
        acc[nums[i]] = acc.get(nums[i], 0) + 1
        return go(i + 1, acc)
    return go(0, {})
```

The recursive frequency function uses Theta(n) stack and mutates one dictionary. The loop version is the same body without the call. Prefer the loop. The anagram function returns groups in a deterministic order so tests can compare them. If the statement accepts any order, you can skip the sorts and say so.

## Complexity and trade-offs

| Operation | Expected time | Worst time | Notes |
| --- | --- | --- | --- |
| Lookup, insert, delete | Theta(1) | Theta(n) | Worst case is one long chain or one probe cluster |
| Build a map of n keys | Theta(n) | Theta(n squared) | Expected includes amortized resizing |
| Sort, then scan | Theta(n log n) worst case | Theta(n log n) | No hash, less memory traffic, worse asymptotic average |
| Balanced tree map | Theta(log n) | Theta(log n) | Use when you need order or a hard worst case |

Anagram grouping is Theta of total characters times log of the longest word if you sort each word, or linear in the total number of characters with a 26-count key. Longest consecutive sequence is expected linear. A sort-based consecutive scan is n log n and needs no hashing. Offer it when the interviewer wants a worst-case bound.

## Tricks, tips, and patterns

Store the answer to the question you are about to ask, not a vague "seen" flag, when the question needs an index or a count. Update the map after the query when the current element must not match itself. Use a tuple as a composite key. Normalize anagrams the same way for every word. For a fixed alphabet, a count tuple is a good key and does not require sorting. Remember that expected linear means a good hash and a controlled load factor. If you need keys in sorted order, use a balanced tree or sort the keys at the end. Do not sort on every insertion unless the interview is specifically about that cost.

## Common mistakes and edge cases

Using a list as a key. Forgetting that equal keys share a hash. Looking up a complement after inserting the current value, so one element pairs with itself. Counting an anagram key from the original word and then sorting the word in place, so later logic sees the sorted spelling. Assuming set iteration order is the order of first insertion. A worst-case story told as if it were expected, or the other way around. Integer keys are easy. For the divisible-subarray problem, the key is the prefix modulo m, and negative prefixes need a non-negative residue. Empty input returns an empty group list or a zero count. Duplicate words are separate elements if the statement says they are. Read it.

## Interview notes

Say "hash map, expected linear time, linear memory" as one phrase so you do not have to be corrected. Name the key in a sentence: "the key is the sorted word" or "the key is the complement." Dry-run three insertions and one collision in words even if you do not draw buckets. If the interviewer asks how a hash map works, give chaining, the load factor, and resizing. You do not need to reimplement Python's probe sequence. If they ask for a worst-case guarantee, switch to a balanced tree and accept the log factor, or sort. Do not pretend hashing has one.

## Practice problems

1. [Two Sum](/practice/two-sum) and [4Sum II](/practice/4sum-ii).
2. [Group Anagrams](/practice/group-anagrams) and [Valid Anagram](/practice/valid-anagram).
3. [Top K Frequent Elements](/practice/top-k-frequent-elements) — the map, then a heap or a bucket array.
4. [Longest Consecutive Sequence](/practice/longest-consecutive-sequence).
5. [Isomorphic Strings](/practice/isomorphic-strings) and [Word Pattern](/practice/word-pattern).
6. [Ransom Note](/practice/ransom-note) and [First Unique Character](/practice/first-unique-character).

## Summary and cheat sheet

- A hash table is buckets plus a hash function. Collisions are chaining or probing.
- Expected constant time per operation. Worst case linear. Resizing is amortized.
- Keys must be immutable, and equal keys must share a hash.
- Maps store payloads. Sets store membership. Do not rely on set order.
- The pattern is: choose the key that makes the next question a lookup.
- Query before insert when the current item must not see itself.
- A count tuple is a sort-free anagram key for a fixed alphabet.

## Further reading

- [Wikipedia — Hash table](https://en.wikipedia.org/wiki/Hash_table)
- [Wikipedia — Hash function](https://en.wikipedia.org/wiki/Hash_function)
- [Python TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity)
- [CPython dict implementation notes](https://github.com/python/cpython/blob/main/Objects/dictobject.c)
'''

CACHES = r'''
## Why this matters

Caches are the design question that sits on top of hashing. An LRU cache evicts the item that has been idle the longest. An LFU cache evicts the item that has been used the least, and breaks ties by recency. Both must answer get and put in constant time, which means a hash map for the key and a second structure that can move or delete an arbitrary item without scanning. The interview is not "import a cache." It is the two structures and the invariant that keeps them honest. Ordered dictionaries in Python make the LRU short. You should still be able to describe the doubly linked list, and you should be able to explain LFU's frequency buckets.

## Intuition

An LRU is a line of people at a counter. The person who just spoke moves to the front. When the room is full and someone new arrives, the person at the back leaves. Finding a person by name is the hash map. Moving them, without walking the line, requires that each person know their neighbors, which is a doubly linked list, or a structure such as OrderedDict that offers the same moves. An LFU is a set of such lines, one per frequency. Using an item moves it from the line for count f to the line for count f + 1. The person to evict is the back of the lowest non-empty line. You keep that lowest frequency in a variable so you do not scan the lines.

## Core concept in depth

LRU operations. get(key) returns -1 when the key is absent. When it is present, the node moves to the most-recent position and the value is returned. put(key, value) updates the value and moves the node to the most-recent position when the key exists. When the key is new and the cache is at capacity, it evicts the least-recent node, then inserts the new node as the most recent. Capacity zero stores nothing. A clean implementation uses sentinel head and tail nodes so the real list is never empty of sentinels. The most recent sits next to the head. The least recent sits next to the tail. Unlinking a node is four pointer assignments, or two if you write a helper that knows the neighbors. The map points from key to node, so the unlink does not search.

The invariant: the map's keys are exactly the nodes between the sentinels, the list order is most recent toward least recent, and the size equals the number of keys. Every get and put restores the invariant. Eviction deletes the node before the tail from both the list and the map. Because both deletions are constant time, get and put are constant time. There is no amortization hiding in the list operations themselves. If the map resizes, a particular put can be linear, and a sequence of puts is amortized constant in the map. For interviews, "constant time aside from hash-table resizing" is the precise sentence.

OrderedDict implements this policy. move_to_end(key) on access, and popitem(last=False) to evict the oldest. Python's OrderedDict is a dict plus a linked list, which is the design above. Using it is acceptable when the interviewer allows the standard library and still asks you to explain the complexity. If they say "do not use OrderedDict," draw the sentinels.

LFU adds frequencies. Each key stores its value and its frequency. Each frequency maps to an ordered dictionary or a linked list of keys with that frequency, in most-recent order. A variable min_freq is the smallest frequency that currently has at least one key. get on a hit increases the frequency by one: remove the key from the old bucket, insert it at the recent end of the new bucket, and if the old bucket was the minimum and is now empty, increment min_freq. The new frequency is exactly old plus one, so the minimum cannot jump further than that. put of an existing key updates the value and performs the same frequency bump. put of a new key, when full, evicts the least-recent key in the min_freq bucket, then inserts the new key at frequency 1. The new minimum is 1, because a brand-new key has been used once. Capacity zero rejects puts.

The LFU invariant: every key appears in the bucket of its stored frequency, buckets contain no empty holes that min_freq would point at, and within a bucket the order is recency. Eviction then takes the oldest key of the least frequently used bucket, which is exactly the statement of the policy. A wrong min_freq, off by one after a bump, evicts a frequent item or crashes on an empty bucket. That variable is the part to dry-run.

Neither cache is thread-safe in this design. A production cache also decides what to do with a single-flight miss, expiry, and memory measured in bytes rather than in entry count. Those are system-design follow-ups. The data-structure round ends when get and put are correct and constant time.

## Diagram and dry run

```mermaid
flowchart TD
    A[put a new key] --> B{At capacity?}
    B -->|Yes| C[Evict least recent of the minimum frequency]
    B -->|No| D[Insert at frequency 1]
    C --> D
    E[get a present key] --> F[Move it from frequency f to f plus 1]
    F --> G{Old bucket empty and it was the minimum?}
    G -->|Yes| H[Minimum becomes f plus 1]
    G -->|No| I[Minimum unchanged]
```

LRU capacity 2. Operations put(1, 1), put(2, 2), get(1), put(3, 3), get(2).

| Operation | Most recent to least recent | Return |
| --- | --- | --- |
| put 1 | 1 | null |
| put 2 | 2, 1 | null |
| get 1 | 1, 2 | 1 |
| put 3 | 3, 1 | null, and 2 is evicted |
| get 2 | 3, 1 | -1 |

LFU capacity 2 on the classic sequence put 1, put 2, get 1, put 3. After get 1, key 1 has frequency 2 and key 2 has frequency 1. The next put evicts 2, the only key at the minimum frequency. A later get(2) returns -1. If both keys had the same frequency, the least recently used of them would leave.

## Runnable Python

This LRU uses OrderedDict so the file stays short enough to type in a round, and the methods match the policy above. The LFU sketch in the comments of a real round should become frequency buckets. The second function is the operation runner you can test without a class wrapper. A recursive cache does not make sense. The iterative structure is the algorithm.

```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self._data:
            return -1
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self._data:
            self._data.move_to_end(key)
            self._data[key] = value
            return
        if len(self._data) >= self.capacity:
            self._data.popitem(last=False)
        self._data[key] = value


def lru_ops(capacity: int, ops: list[tuple[str, list[int]]]) -> list[int | None]:
    cache = LRUCache(capacity)
    out: list[int | None] = []
    for name, args in ops:
        if name == "get":
            out.append(cache.get(args[0]))
        else:
            cache.put(args[0], args[1])
            out.append(None)
    return out
```

The dry-run sequence, encoded as operations, returns null, null, 1, null, -1. If you implement the sentinel list instead, the same sequence is the test. Draw the four links of an unlink once so your hands remember them: the neighbor's next and prev, then the node's own pointers if you care about leaving it detached.

## Complexity and trade-offs

| Cache | get hit | get miss | put | Eviction choice |
| --- | --- | --- | --- | --- |
| LRU, list plus map | Theta(1) | Theta(1) | Theta(1) | Least recently used |
| LRU, scan a list | Theta(n) | Theta(n) | Theta(n) | Correct and too slow |
| LFU, buckets plus maps | Theta(1) | Theta(1) | Theta(1) | Least frequent, then least recent |
| LFU, scan frequencies | Theta(n) | Theta(1) | Theta(n) | Easier to write, fails the bound |

A heap of timestamps does not give constant time, because updating a key's timestamp is not a constant-time heap operation unless you also lazy-delete, and lazy deletion can leave the heap linear in the number of updates. The linked list or the ordered bucket is the right tool. Say that if someone proposes a heap.

## Tricks, tips, and patterns

Sentinels remove the empty-list special case. One helper to detach a node and one helper to insert it after the head are the whole list API. In LFU, a new key always lands at frequency 1, and that resets the minimum. A frequency bump moves a key by exactly one bucket. If the old bucket empties and it was the minimum, the new minimum is the new frequency, not an unknown larger number, because this key is now at old plus one and nothing else was at a frequency between them that this operation created. Other keys might still sit at the old frequency. Only the empty check increments the minimum. Test capacity 0, capacity 1, an update of an existing key while full, and a tie of frequencies.

## Common mistakes and edge cases

Evicting the most recent end because popitem was called with the default. Forgetting to move a key to the recent end on get, so a frequently read key still looks old. Updating a value without counting the update as a use. In LFU, evicting before checking that the key already exists, so an update of a present key at full capacity throws away some other key. Leaving min_freq on an empty bucket. Using a queue instead of a doubly linked structure and then being unable to delete a middle node on a get. Capacity zero. Negative capacity should be rejected or treated as zero. Keys that are equal must update, not duplicate. The return of put is null in the usual operation-list contract. get of a missing key is -1, not null, in the usual contract. Read the prompt. The two sentinels are not entries and must not be counted toward capacity.

## Interview notes

Draw the map and the list, label most recent and least recent, and then implement. Say the invariant once. For LFU, draw two buckets and the min_freq arrow, and dry-run the classic capacity-2 sequence before you write the general case. If time is short, implement LRU completely and describe LFU's buckets in sentences the interviewer can believe. Do not claim constant time for a solution that scans. Mention that resizing the hash map is amortized, if you want to be exact. Discuss thread safety only if the interviewer leaves the data-structure problem and asks about production. Otherwise finish the invariant.

## Practice problems

1. [LRU Cache](/practice/lru-cache) — implement the operation sequence.
2. [LFU Cache](/practice/lfu-cache) — frequency buckets and a recency tie break.
3. [Implement Trie](/practice/implement-trie) — another design that is a map of maps. The trie lesson goes deeper.

## Summary and cheat sheet

- LRU: hash map plus a recency list. Most recent at one end, evict the other end. Move on every use.
- Sentinels make insert and delete uniform.
- OrderedDict is that design in the standard library. Explain it if you use it.
- LFU: a list per frequency, plus the current minimum frequency.
- A hit moves a key from frequency f to f + 1. An empty minimum bucket increments the minimum.
- A new key evicts first when full, then enters at frequency 1, and the minimum becomes 1.
- get and put are constant time only if arbitrary nodes can be removed without a scan.

## Further reading

- [Wikipedia — Cache replacement policies](https://en.wikipedia.org/wiki/Cache_replacement_policies)
- [Wikipedia — Doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list)
- [Python OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
'''

emit(
    "03-hashing",
    "01-hash-maps-and-sets.mdx",
    title="Hash Maps and Sets",
    slug="hash-maps-and-sets",
    summary="Buckets, collisions, load factor, and the key-design patterns behind the classic hashing problems.",
    duration=40,
    difficulty="intermediate",
    prerequisites=["partitions-majority-and-intervals"],
    tags=["hashing", "hash-map", "sets"],
    order=1,
    body=MAPS,
)
emit(
    "03-hashing",
    "02-lru-and-lfu.mdx",
    title="LRU and LFU Caches",
    slug="lru-and-lfu",
    summary="Constant-time caches: a recency list for LRU, and frequency buckets with a recency tie-break for LFU.",
    duration=40,
    difficulty="advanced",
    prerequisites=["hash-maps-and-sets"],
    tags=["lru", "lfu", "design", "hashing"],
    order=2,
    body=CACHES,
)
