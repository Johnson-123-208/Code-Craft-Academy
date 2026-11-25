#!/usr/bin/env python3
"""Generate CodeCraft Academy System Design MDX lessons."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "system-design"


def fm(
    title: str,
    slug: str,
    summary: str,
    duration: int,
    difficulty: str,
    tags: list[str],
    order: int,
    prereqs: list[str] | None = None,
) -> str:
    pr = prereqs or []
    tags_s = ", ".join(f'"{t}"' for t in tags)
    pr_s = ", ".join(f'"{p}"' for p in pr)
    return f"""---
title: "{title}"
slug: "{slug}"
summary: "{summary}"
duration: {duration}
difficulty: "{difficulty}"
prerequisites: [{pr_s}]
tags: [{tags_s}]
order: {order}
---
"""


def lesson(
    title: str,
    slug: str,
    summary: str,
    duration: int,
    difficulty: str,
    tags: list[str],
    order: int,
    why: str,
    intuition: str,
    core: str,
    diagram: str,
    dry_run: str,
    code: str,
    complexity: str,
    tricks: str,
    mistakes: str,
    interview: str,
    practice: str,
    summary_sheet: str,
    further: str,
    prereqs: list[str] | None = None,
) -> str:
    return (
        fm(title, slug, summary, duration, difficulty, tags, order, prereqs)
        + f"""
## Why this matters

{why}

## Intuition

{intuition}

## Core concept in depth

{core}

## Diagram / flowchart

{diagram}

### Dry-run

{dry_run}

## Code

{code}

## Complexity analysis

{complexity}

## Tricks, tips and patterns

{tricks}

## Common mistakes and edge cases

{mistakes}

## Interview notes

{interview}

## Practice problems

{practice}

## Summary / cheat sheet

{summary_sheet}

## Further reading

{further}
"""
    )


def write(module: str, filename: str, body: str) -> Path:
    path = ROOT / module / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.lstrip("\n") if body.startswith("\n") else body, encoding="utf-8")
    # Ensure frontmatter starts at top
    if not path.read_text(encoding="utf-8").startswith("---"):
        path.write_text(body.lstrip(), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT.parent.parent)}")
    return path


# ---------------------------------------------------------------------------
# 01-fundamentals (skip 01 — already exists)
# ---------------------------------------------------------------------------

def gen_fundamentals() -> None:
    write(
        "01-fundamentals",
        "02-latency-throughput.mdx",
        lesson(
            title="Latency, Throughput and Percentile Thinking",
            slug="latency-throughput",
            summary="Measure and reason about latency percentiles, throughput ceilings, Little's Law, and how batching, concurrency, and queues reshape both.",
            duration=35,
            difficulty="intermediate",
            tags=["system-design", "latency", "throughput", "percentiles"],
            order=2,
            prereqs=["scalability-availability-reliability"],
            why="Users feel latency; operators pay for throughput. A design that looks fine on average RPS can fail hard when p99 spikes or when queues grow without bound. Interviewers and production postmortems both hinge on separating these two metrics and connecting them with queueing theory.",
            intuition="Think of a highway. Throughput is cars per hour that finish the trip. Latency is how long one car takes. Adding lanes raises throughput; a traffic jam raises latency even if total cars/hour later recovers. Batching cars into convoys can raise throughput but makes each car wait to form a batch.",
            core="""### Latency

Time from request start to useful response. Report **p50 / p95 / p99 / p999**, not only the mean. Tail latency often comes from GC pauses, lock contention, cold caches, retries, or noisy neighbors.

### Throughput

Completed work per unit time: RPS, QPS, messages/sec, MB/sec. Limited by the slowest saturated resource (CPU, disk IOPS, network, lock).

### Little's Law

In a stable system: **L = λ × W** — average concurrency (in-flight work) equals arrival rate times average latency. If you want lower latency at the same arrival rate, you must reduce in-flight work (faster handlers, less queueing).

### Relationships

| Lever | Latency | Throughput |
| --- | --- | --- |
| Vertical CPU upgrade | Often down | Often up |
| More replicas | Down if queue waits | Up |
| Batching | Often up | Up |
| Synchronous fan-out | Up | May down |
| Caching hot keys | Down | Up until invalidation cost |

### Saturation curves

As utilization approaches 100%, queue wait explodes. Aim for headroom (often 50–70% peak utilization on critical paths) so p99 stays sane.""",
            diagram="""```mermaid
flowchart LR
    Clients -->|arrival rate λ| Q[Request Queue]
    Q --> W[Workers]
    W -->|completions| Out[Responses]
    W --> M[Metrics: p50 p95 p99]
    Q --> D[Depth L]
```""",
            dry_run="""Service handles λ = 2,000 RPS. Mean latency W = 50 ms = 0.05 s.

| Quantity | Value |
| --- | --- |
| In-flight L = λ × W | 2,000 × 0.05 = 100 requests |
| If p99 = 200 ms | Need enough concurrency / capacity for the tail |
| If queue depth grows unboundedly | System is unstable — arrival exceeds service rate |""",
            code="""```python
def littles_law_inflight(rps: float, latency_ms: float) -> float:
    \"\"\"Average in-flight requests from rate and mean latency.\"\"\"
    return rps * (latency_ms / 1000.0)


def percentile(sorted_samples: list[float], p: float) -> float:
    if not sorted_samples:
        raise ValueError("empty")
    if not 0 < p <= 100:
        raise ValueError("p must be in (0, 100]")
    idx = int(round((p / 100) * (len(sorted_samples) - 1)))
    return sorted_samples[idx]


if __name__ == "__main__":
    samples = sorted([12, 15, 18, 20, 22, 25, 40, 80, 120, 200])
    print("inflight", littles_law_inflight(2000, 50))
    print("p50", percentile(samples, 50), "p99", percentile(samples, 99))
```""",
            complexity="""| Concern | Typical cost |
| --- | --- |
| Measuring high-cardinality latency | Storage and CPU for histograms |
| Raising throughput via replicas | Coordination + data fan-out |
| Cutting p99 via sync calls | Often hurts availability under dependency failure |
| Aggressive batching | Higher end-to-end latency, memory spikes |""",
            tricks="""- Instrument histograms, not just averages.
- Separate client-perceived latency from server processing time.
- Use timeouts shorter than upstream SLOs; budget the whole chain.
- Prefer shedding load over unlimited queues.
- Coalesce identical in-flight reads (singleflight) to protect caches.""",
            mistakes="""- Optimizing mean while p99 is 20× worse.
- Infinite queues that hide overload until OOM.
- Comparing RPS across endpoints with different payload sizes.
- Ignoring retry amplification that multiplies effective load.""",
            interview="""State the workload (read/write, payload size), quote target percentiles, estimate RPS, then show capacity with headroom. Mention Little's Law when discussing concurrency and thread/connection pools.",
            practice="""1. Given 5,000 RPS and 30 ms mean latency, estimate average in-flight requests (easy)
2. Explain why p99 can rise when average RPS is flat (medium)
3. Design a load-shedding policy for a read API under flash traffic (medium)""",
            summary_sheet="""- Latency = time per request; throughput = work per time.
- Report percentiles; design for the tail.
- Little's Law: L = λ × W.
- Headroom beats 100% utilization for stable p99.""",
            further="""- [Little's Law](https://en.wikipedia.org/wiki/Little%27s_law)
- [Google SRE — Latency and Availability](https://sre.google/sre-book/embracing-risk/)
- [The Tail at Scale (Dean & Barroso)](https://research.google/pubs/pub40801/)""",
        ),
    )

    write(
        "01-fundamentals",
        "03-cap-pacelc.mdx",
        lesson(
            title="CAP Theorem and PACELC in Practice",
            slug="cap-pacelc",
            summary="Apply CAP and PACELC correctly: what a partition really is, why CA is not a free lunch, and how real systems pick CP, AP, or tunable consistency.",
            duration=35,
            difficulty="advanced",
            tags=["system-design", "cap", "pacelc", "distributed-systems"],
            order=3,
            prereqs=["scalability-availability-reliability"],
            why="CAP is the most misquoted idea in system design interviews. Used well, it forces a clear stance when the network splits. PACELC adds the everyday case: even without partitions, you still trade latency against consistency. Product requirements (payments vs likes) map directly onto these choices.",
            intuition="Two bank branches lose the phone line. If both keep approving withdrawals (availability), balances can disagree (consistency suffers). If both freeze withdrawals until the line returns (consistency), customers cannot get cash (availability suffers). When the line works, you still choose: sync to the other branch every time (higher latency, stronger consistency) or sync later (faster, risk of stale views).",
            core="""### CAP (during a Partition)

You cannot simultaneously guarantee perfect Consistency and perfect Availability for all clients. Systems lean **CP** (refuse or block conflicting ops) or **AP** (serve possibly stale/ divergent answers).

Important: CAP Consistency means **linearizability** (one global order), not SQL ACID isolation in general. Availability means every non-failing node eventually returns a response — not "99.99% uptime marketing."

### PACELC

**If Partition → trade Availability vs Consistency; Else → trade Latency vs Consistency.**

Examples:

| System style | Partition stance | Else stance |
| --- | --- | --- |
| Consensus primary (etcd-like) | CP | Prefer C over L |
| Dynamo-style quorum / hinted handoff | AP-leaning | Often L over C |
| Tunable Cassandra/DynamoDB | Configurable | Configurable |

### Practical mapping

- **Ledger / inventory reservation**: prefer CP or strongly consistent single-region primary.
- **Social counters / presence**: often AP + eventual merge.
- **Multi-region active-active**: expect PACELC latency/consistency tension even when healthy.""",
            diagram="""```mermaid
flowchart TD
    Start[Distributed data store] --> P{Partition?}
    P -->|Yes| Cap{Choose}
    Cap -->|C| CP[Block or refuse unsafe ops]
    Cap -->|A| AP[Serve local / stale answers]
    P -->|No| Else{PACELC Else}
    Else -->|C| Strong[Sync replication / quorum]
    Else -->|L| Fast[Async / local reads]
```""",
            dry_run="""Scenario: 3 replicas, write quorum W=2, read quorum R=2.

| Case | Outcome |
| --- | --- |
| Healthy cluster | Stronger reads if R+W > N |
| One replica isolated | Writes needing W=2 may fail on minority side (CP flavor) |
| W=1, R=1 | Higher availability, stale reads possible |""",
            code="""```python
def quorum_ok(n: int, r: int, w: int) -> dict:
    \"\"\"Classic quorum rules of thumb for N replicas.\"\"\"
    return {
        "intersects": r + w > n,
        "write_tolerates_failures": n - w,
        "read_tolerates_failures": n - r,
    }


if __name__ == "__main__":
    print(quorum_ok(3, 2, 2))
    print(quorum_ok(3, 1, 1))
```""",
            complexity="""| Choice | Benefit | Cost |
| --- | --- | --- |
| CP / sync commit | Safer invariants | Higher write latency, outages on majority loss |
| AP / async | Stay writable | Conflict resolution, stale reads |
| Cross-region sync | Global C | Tens to hundreds of ms RTT |""",
            tricks="""- Ask: what is wrong if two clients see different values for 5 seconds?
- Prefer single-region strong consistency + async analytics replicas when possible.
- Use idempotency keys and version vectors when choosing AP writes.
- Document the client-visible consistency model explicitly.""",
            mistakes="""- Claiming a system is CA under partitions (hand-waving).
- Confusing high availability SLOs with CAP Availability.
- Treating eventual consistency as no consistency at all.
- Forcing global sync replication for data that does not need it.""",
            interview="""Name the business invariant, pick CP vs AP for partitions, then state the healthy-path latency vs consistency choice (PACELC). Give one concrete failure scenario and the user-visible behavior.",
            practice="""1. Classify a shopping-cart service and a payment capture service under CAP (easy)
2. Design quorum R/W for N=5 aiming for intersection (medium)
3. Explain PACELC for a multi-region session store (medium)""",
            summary_sheet="""- CAP applies when partitioned: pick C or A.
- PACELC: else also pick latency vs consistency.
- Quorums: R+W > N helps intersection.
- Match invariants to the model — not buzzwords.""",
            further="""- [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)
- [PACELC](https://en.wikipedia.org/wiki/PACELC_theorem)
- [Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)""",
        ),
    )

    write(
        "01-fundamentals",
        "04-consistency-models.mdx",
        lesson(
            title="Consistency Models from Strong to Eventual",
            slug="consistency-models",
            summary="Navigate linearizability, sequential and causal consistency, read-your-writes, monotonic reads, and eventual consistency with client-centric guarantees.",
            duration=40,
            difficulty="advanced",
            tags=["system-design", "consistency", "replication"],
            order=4,
            prereqs=["cap-pacelc"],
            why="Saying eventual consistency is not a design — it is a spectrum. Clients notice anomalies: reading stale profiles, losing cart items, or seeing comments out of order. Choosing and communicating the right consistency model prevents silent correctness bugs and over-engineered consensus everywhere.",
            intuition="A shared Google Doc with live cursors aims for strong, immediate agreement. A likes counter that lags by a second is fine. A chat app needs causal order: you should not see the reply before the message it answers. Consistency models are contracts about which reorderings and stales are allowed.",
            core="""### Strong models

- **Linearizability**: each operation appears instantaneously in a single global order consistent with real-time. Hardest; typical of consensus-backed KV and single-leader sync commits.
- **Sequential consistency**: one global order, but not necessarily real-time aligned.

### Causal and session models

- **Causal consistency**: respects happened-before (writes that causally relate stay ordered).
- **Read-your-writes**: a client sees its own writes.
- **Monotonic reads**: once you saw version v, you never go backward.
- **Monotonic writes**: a client's writes apply in order.

### Eventual consistency

Replicas converge if writes stop. Without extras, clients can see any intermediate state. Pair with conflict resolution: LWW, CRDTs, merge functions, or human workflows.

### Read/write paths

| Pattern | Typical guarantee |
| --- | --- |
| Sync primary + read primary | Strong for that key |
| Async replicas for reads | Eventual / bounded stale |
| Quorum R/W with intersection | Tunable strength |
| Client sticky sessions | Helps read-your-writes |""",
            diagram="""```mermaid
flowchart TB
    subgraph strong [Stronger]
      L[Linearizable]
      S[Sequential]
      C[Causal]
    end
    subgraph session [Client-centric]
      RYW[Read-your-writes]
      MR[Monotonic reads]
    end
    subgraph weak [Weaker]
      E[Eventual]
    end
    L --> S --> C --> E
    C --> RYW
    RYW --> MR
```""",
            dry_run="""Timeline: Client A writes x=1 at t1. Replica R2 is behind. Client B reads x from R2.

| Model | Allowed? |
| --- | --- |
| Linearizable after t1 completes | B must see x=1 (or op not yet complete) |
| Eventual | B may see old x |
| Read-your-writes for A | A must see x=1 on next read |""",
            code="""```python
from dataclasses import dataclass, field


@dataclass
class VersionedValue:
    value: str
    version: int


@dataclass
class Session:
    last_seen: dict[str, int] = field(default_factory=dict)

    def read_ok(self, key: str, vv: VersionedValue) -> bool:
        \"\"\"Monotonic reads: never go backward for this session.\"\"\"
        prev = self.last_seen.get(key, 0)
        if vv.version < prev:
            return False
        self.last_seen[key] = vv.version
        return True


if __name__ == "__main__":
    s = Session()
    assert s.read_ok("user", VersionedValue("a", 1))
    assert not s.read_ok("user", VersionedValue("old", 0))
```""",
            complexity="""| Model | Coordination cost | Anomaly risk |
| --- | --- | --- |
| Linearizable | High | Low |
| Causal | Medium (dependency tracking) | Medium |
| Eventual + LWW | Low | High without care |""",
            tricks="""- Push strong consistency to small critical sets (balances, unique usernames).
- Use session guarantees via sticky routing or version tokens in APIs.
- Bounded staleness (e.g., max 5s) is often enough for feeds.
- CRDTs shine for collaborative counters and sets.""",
            mistakes="""- Serving reads from async replicas for check-then-act writes.
- Assuming TTL cache equals a consistency model.
- Ignoring clock skew when using LWW timestamps.
- Exposing merge conflicts to users without UX.""",
            interview="""List user-visible anomalies you refuse to accept, pick the weakest model that forbids them, then describe the replication mechanism that implements it.",
            practice="""1. Which model prevents seeing a reply before its parent message? (easy)
2. Design read-your-writes for a multi-region profile service (medium)
3. Compare LWW vs CRDT for a shared shopping list (medium)""",
            summary_sheet="""- Linearizability ⊂ sequential ⊂ causal ⊂ eventual (roughly).
- Session guarantees fix many UX bugs cheaply.
- Match model to anomaly budget, not fashion.
- Tokens / sticky sessions help client-centric guarantees.""",
            further="""- [Consistency models](https://en.wikipedia.org/wiki/Consistency_model)
- [Bailis — Highly Available Transactions](http://www.bailis.org/papers/hat-vldb2014.pdf)
- [CRDTs](https://crdt.tech/)""",
        ),
    )

    write(
        "01-fundamentals",
        "05-back-of-envelope.mdx",
        lesson(
            title="Back-of-the-Envelope Estimation for System Design",
            slug="back-of-envelope",
            summary="Estimate QPS, storage, bandwidth, and servers using powers of two, latency numbers every programmer should know, and clear peak-factor assumptions.",
            duration=40,
            difficulty="intermediate",
            tags=["system-design", "estimation", "capacity"],
            order=5,
            prereqs=["latency-throughput"],
            why="Interviews and capacity reviews reward Fermi estimates within an order of magnitude. Without numbers you cannot size caches, shards, or egress cost. With a repeatable method you expose bottlenecks before drawing boxes.",
            intuition="You do not need a spreadsheet model on day one. You need: users × actions × size × peak factor, then convert to RPS, GB/day, and machines. Think like packing a moving truck: count boxes, volume, and trips — not perfect inventory.",
            core="""### Numbers to memorize (approx.)

| Resource | Ballpark |
| --- | --- |
| L1 cache ref | ~1 ns |
| Main memory ref | ~100 ns |
| SSD random read | ~100 µs |
| HDD seek | ~10 ms |
| Same-DC RTT | ~0.5 ms |
| Cross-coast RTT | ~50–80 ms |
| Disk sequential | hundreds MB/s |
| 1 day | ~10^5 seconds (86,400) |

Powers of two: 2^10 ≈ 10^3, 2^20 ≈ 10^6, 2^30 ≈ 10^9.

### Method

1. Clarify DAU/MAU, read/write ratio, object sizes, retention.
2. Daily volume → average RPS → peak RPS (3–10×).
3. Storage = objects × size × replicas × growth × retention.
4. Bandwidth = write path + fan-out reads + replication.
5. Servers = peak_RPS / RPS_per_instance with headroom.

### Sanity checks

Compare to known systems; check if network or disk saturates first; round aggressively.""",
            diagram="""```mermaid
flowchart TD
    Req[Requirements] --> U[Users and actions]
    U --> R[Avg and peak RPS]
    U --> S[Storage growth]
    U --> B[Bandwidth]
    R --> Cap[Capacity plan]
    S --> Cap
    B --> Cap
    Cap --> Design[Architecture choices]
```""",
            dry_run="""URL shortener: 100M new URLs/month, 10:1 read:write, 500 byte metadata/URL, keep forever, peak 5×.

| Step | Calc |
| --- | --- |
| Writes/sec avg | 100e6 / (30×86400) ≈ 40 WPS |
| Peak writes | ~200 WPS |
| Peak reads | ~2,000 RPS |
| Year storage | 1.2e9 × 500 B ≈ 600 GB (+ indexes/replicas) |""",
            code="""```python
SECONDS_DAY = 86_400


def peak_rps(daily_events: float, peak_factor: float = 5.0) -> float:
    return (daily_events / SECONDS_DAY) * peak_factor


def storage_gb(objects: float, bytes_each: float, replicas: int = 3) -> float:
    return objects * bytes_each * replicas / (1024 ** 3)


if __name__ == "__main__":
    monthly = 100_000_000
    daily_writes = monthly / 30
    print("peak writes", round(peak_rps(daily_writes), 1))
    print("peak reads", round(peak_rps(daily_writes * 10), 1))
    print("1y storage GiB", round(storage_gb(monthly * 12, 500), 1))
```""",
            complexity="""Estimation error of 2–5× is normal early; designs should tolerate that. Over-precision wastes interview time. Under-estimating egress and indexes is the usual miss.""",
            tricks="""- State assumptions out loud; invite correction.
- Estimate write amplification (indexes, replicas, WAL).
- Convert everything to per-second and per-year.
- Carry units in every line.""",
            mistakes="""- Using average RPS as capacity target.
- Forgetting replicas and backups in storage.
- Ignoring fan-out (one write → many reads downstream).
- Mixing GB and GiB without caring at TB scale.""",
            interview="""Spend 3–5 minutes on estimates before deep design. Round to nice numbers, show peak, then size the first bottleneck component.",
            practice="""1. Estimate QPS for 50M DAU posting 2 times/day with 10× peak (easy)
2. Storage for 5 years of 1 KB events at 20k events/sec (medium)
3. Bandwidth for video at 2 Mbps average bitrates for 1M concurrent viewers (medium)""",
            summary_sheet="""- DAU × actions → daily → avg RPS → peak RPS.
- Storage includes replicas, indexes, retention.
- Memorize latency/bandwidth orders of magnitude.
- Order-of-magnitude accuracy beats false precision.""",
            further="""- [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832)
- [System Design Primer — estimates](https://github.com/donnemartin/system-design-primer)""",
        ),
    )


if __name__ == "__main__":
    gen_fundamentals()
    print("fundamentals done")
