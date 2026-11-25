#!/usr/bin/env python3
"""Generate modules 02-building-blocks and 03-architecture-styles."""
from __future__ import annotations

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "gen_sd_course", Path(__file__).with_name("gen_sd_course.py")
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)
lesson, write = mod.lesson, mod.write


def gen_building_blocks() -> None:
    write(
        "02-building-blocks",
        "01-load-balancers.mdx",
        lesson(
            title="Load Balancers: L4, L7 and Traffic Distribution",
            slug="load-balancers",
            summary="Design traffic entry with L4 vs L7 load balancers, algorithms, health checks, sticky sessions, and multi-tier LB topologies.",
            duration=35,
            difficulty="intermediate",
            tags=["system-design", "load-balancer", "networking"],
            order=1,
            why="Almost every scaled system puts a load balancer between clients and app fleets. Wrong tier (L4 vs L7), bad health checks, or sticky-session abuse create hotspots and silent outages. Interviews expect you to place LBs correctly and explain failover.",
            intuition="A restaurant host seats guests across tables. L4 is seating by party size without reading the menu order; L7 reads the order (HTTP path, headers) and sends vegans to a special station. If a table is dirty (unhealthy), the host stops seating there.",
            core="""### Layers

- **L4 (transport)**: TCP/UDP, fast, cheap, little app awareness. Good for TLS passthrough or non-HTTP.
- **L7 (application)**: HTTP/gRPC routing by path, host, headers; can terminate TLS, retry idempotent GETs carefully, WAF integration.

### Algorithms

Round-robin, least-connections, weighted, power-of-two-choices, consistent hashing for cache-friendly affinity.

### Health and connection management

Active/passive health checks, connection draining, slow-start for new backends, PROXY protocol / X-Forwarded-For for client IP.

### Topology

DNS → anycast / global LB → regional L7 → service mesh or internal L4. Separate public edge from internal east-west balancing.""",
            diagram="""```mermaid
flowchart TB
    Users --> DNS
    DNS --> GLB[Global Load Balancer]
    GLB --> R1[Regional L7 LB]
    GLB --> R2[Regional L7 LB]
    R1 --> A1[App]
    R1 --> A2[App]
    R2 --> A3[App]
    R2 --> A4[App]
```""",
            dry_run="""10 backends, round-robin, one backend fails health checks.

| Step | Result |
| --- | --- |
| Health check fails 3 times | Backend removed from pool |
| In-flight connections | Drained or reset per policy |
| New requests | Spread across 9 healthy nodes |""",
            code="""```python
from itertools import cycle


class RoundRobin:
    def __init__(self, backends: list[str]):
        self._healthy = list(backends)
        self._cycle = cycle(self._healthy)

    def mark_down(self, backend: str) -> None:
        self._healthy = [b for b in self._healthy if b != backend]
        self._cycle = cycle(self._healthy) if self._healthy else cycle([])

    def next(self) -> str | None:
        if not self._healthy:
            return None
        return next(self._cycle)


if __name__ == "__main__":
    rr = RoundRobin(["a", "b", "c"])
    print([rr.next() for _ in range(4)])
    rr.mark_down("b")
    print([rr.next() for _ in range(4)])
```""",
            complexity="""| Choice | Benefit | Cost |
| --- | --- | --- |
| L4 | Low latency overhead | Weak routing features |
| L7 | Smart routing, auth at edge | CPU for TLS/HTTP parse |
| Sticky sessions | Simple stateful apps | Uneven load, painful deploys |""",
            tricks="""- Prefer stateless apps; use sticky only as a bridge.
- Health checks should hit a cheap dependency-aware endpoint.
- Drain on deploy; never cut all connections at once.
- Put TLS termination where cert ops and mTLS fit your threat model.""",
            mistakes="""- Health check that always returns 200 while DB is down.
- Single LB VM as SPOF without HA pair / cloud LB.
- Using source-IP hash through CGNAT (everyone sticky to one node).
- Infinite retries at LB amplifying outages.""",
            interview="""Draw clients → DNS → LB → N stateless apps → DB. Justify L7 if you need path routing. Mention health checks and no sticky sessions unless required.",
            practice="""1. When would you choose L4 over L7? (easy)
2. Design LB config for blue/green deploy with draining (medium)
3. Explain power-of-two-choices vs round-robin under skew (medium)""",
            summary_sheet="""- L4 = fast packets; L7 = HTTP-aware.
- Health checks + draining are mandatory.
- Avoid stickiness; scale stateless.
- Multi-tier: global then regional.""",
            further="""- [AWS ELB docs](https://docs.aws.amazon.com/elasticloadbalancing/)
- [NGINX load balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/)""",
        ),
    )

    write(
        "02-building-blocks",
        "02-reverse-proxies.mdx",
        lesson(
            title="Reverse Proxies and Edge Gateways",
            slug="reverse-proxies",
            summary="Use reverse proxies for TLS termination, compression, static serving, request buffering, and protecting origin servers.",
            duration=30,
            difficulty="intermediate",
            tags=["system-design", "proxy", "nginx"],
            order=2,
            prereqs=["load-balancers"],
            why="Reverse proxies sit in front of app servers to terminate TLS, cache, compress, rate-limit, and hide internal topology. Confusing them with forward proxies or skipping them leads to duplicated cross-cutting concerns in every service.",
            intuition="A hotel concierge takes guest requests, speaks many languages (protocols), filters spam callers, and only bothers the kitchen (origin) when needed. Guests never walk into the kitchen directly.",
            core="""### Reverse vs forward

- **Forward proxy**: client-side agent to reach the internet.
- **Reverse proxy**: server-side agent that clients think is the origin.

### Common duties

TLS termination, HTTP/2–HTTP/1.1 translation, gzip/brotli, static file serving, request/response buffering, header sanitization, basic authn hooks, canary routing.

### Placement

Edge reverse proxy / API gateway → app. Often the same process family as L7 LB (Envoy, NGINX, HAProxy, Caddy).""",
            diagram="""```mermaid
flowchart LR
    Client -->|HTTPS| RP[Reverse Proxy]
    RP -->|HTTP| App1[App]
    RP --> App2[App]
    RP --> Static[Static files / cache]
```""",
            dry_run="""Client uploads a large body. Proxy buffers to disk, origin sees a complete request only after buffer finishes — or streams if configured. Mis-sized buffers cause 413 or memory pressure.",
            code="""```python
# Conceptual middleware-style reverse proxy hop

def reverse_proxy_headers(incoming: dict[str, str], client_ip: str) -> dict[str, str]:
    out = dict(incoming)
    out["X-Forwarded-For"] = client_ip
    out["X-Forwarded-Proto"] = "https"
    out.pop("X-Powered-By", None)
    return out


if __name__ == "__main__":
    print(reverse_proxy_headers({"Host": "api.example.com"}, "203.0.113.10"))
```""",
            complexity="""Proxies add a network hop (usually sub-ms in-DC) but save origin CPU via TLS offload and caching. Misconfiguration can double timeouts or hide real client IPs.",
            tricks="""- Standardize forwarded headers; trust only the edge hop.
- Keep proxy timeouts aligned with app deadlines.
- Serve hashed static assets at the proxy/CDN, not the app.""",
            mistakes="""- Trusting X-Forwarded-For from the open internet.
- Tiny proxy timeouts causing retry storms.
- Logging bodies with secrets at the proxy.""",
            interview="""Mention reverse proxy for TLS, compression, and shielding origins. Distinguish from LB algorithms and from API gateways (policy layer).",
            practice="""1. Difference between forward and reverse proxy (easy)
2. Design header trust model with two proxy hops (medium)
3. When buffering hurts streaming APIs (medium)""",
            summary_sheet="""- Reverse proxy fronts origins.
- TLS, cache, compress, sanitize.
- Trust hop-by-hop forwarded headers carefully.""",
            further="""- [NGINX Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Envoy Proxy](https://www.envoyproxy.io/)""",
        ),
    )

    write(
        "02-building-blocks",
        "03-cdns.mdx",
        lesson(
            title="CDNs: Caching Content at the Edge",
            slug="cdns",
            summary="Push static and cacheable dynamic content to PoPs worldwide — cache keys, TTLs, purge, origin shield, and signed URLs.",
            duration=30,
            difficulty="intermediate",
            tags=["system-design", "cdn", "caching"],
            order=3,
            why="CDNs cut latency and origin load for images, video segments, JS/CSS, and even API GETs. Without cache-key discipline you leak personalized content or thrash origins. Most consumer-scale designs assume a CDN on the read path.",
            intuition="Instead of every reader flying to your warehouse (origin), you stock popular items in neighborhood lockers (PoPs). Popular items stay stocked (high TTL / hit ratio); rare items still come from the warehouse.",
            core="""### What to cache

Immutable hashed assets (long TTL), images, HLS/DASH segments, public API responses with careful Vary headers. Rarely: personalized HTML (risk).

### Cache keys and freshness

Key = scheme + host + path + selected query + selected headers. Use Cache-Control, ETag, stale-while-revalidate. Purge/ban on deploy.

### Origin protection

Origin shield (collapse mid-tier), request coalescing, signed URLs/cookies for private content, geographic restrictions.""",
            diagram="""```mermaid
flowchart LR
    User --> PoP[CDN PoP]
    PoP -->|HIT| User
    PoP -->|MISS| Shield[Origin Shield]
    Shield --> Origin[Origin Storage / App]
```""",
            dry_run="""Asset `/app.a1b2.js` with `Cache-Control: public, max-age=31536000, immutable`.

| Event | Behavior |
| --- | --- |
| First Tokyo user | MISS → fetch origin → cache |
| Second Tokyo user | HIT at PoP |
| New deploy `app.c3d4.js` | New URL; old entry expires naturally |""",
            code="""```python
def cache_control_for_asset(immutable: bool, ttl_sec: int) -> str:
    if immutable:
        return f"public, max-age={ttl_sec}, immutable"
    return f"public, max-age={ttl_sec}, stale-while-revalidate=60"


if __name__ == "__main__":
    print(cache_control_for_asset(True, 31_536_000))
```""",
            complexity="""CDN shifts bytes and latency cost to the edge provider. Purge fan-out can be slow globally — prefer URL fingerprinting over emergency purge storms.",
            tricks="""- Fingerprint filenames instead of short TTL for static bundles.
- Collapse query-string noise in cache keys.
- Use signed URLs for downloads; never put secrets in query strings without expiry.""",
            mistakes="""- Caching `Set-Cookie` personalized pages at the edge.
- Ignoring `Vary: Accept-Encoding` duplicates.
- Origin without shield thundering during cold start.""",
            interview="""Put CDN in front of object storage for media; long-TTL hashed assets; signed URLs for private files; estimate hit ratio impact on origin.",
            practice="""1. Why fingerprint JS bundles? (easy)
2. Design private video delivery with CDN (medium)
3. Mitigate origin surge after global purge (medium)""",
            summary_sheet="""- PoPs cache by key + TTL.
- Prefer immutable URLs over purge.
- Shield and coalesce protect origin.""",
            further="""- [CDN overview](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)
- [RFC 9111 HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)""",
        ),
    )

    write(
        "02-building-blocks",
        "04-caching.mdx",
        lesson(
            title="Caching Strategies and Invalidation",
            slug="caching",
            summary="Apply cache-aside, read/write-through, TTLs, eviction, stampede control, and multi-layer caching from browser to Redis to CDN.",
            duration=40,
            difficulty="intermediate",
            tags=["system-design", "cache", "redis"],
            order=4,
            why="Caching is the highest-leverage performance tool — and the top source of consistency bugs. Interview designs almost always include a cache layer; production incidents often start with stampede or stale reads after deploys.",
            intuition="A sticky note of a phone number saves a directory lookup until the number changes. The hard part is knowing when the sticky note lies. Strategies differ mainly in who updates the note and when it is thrown away.",
            core="""### Patterns

- **Cache-aside (lazy)**: app reads cache; on miss, load DB, populate cache.
- **Read-through**: cache library loads on miss.
- **Write-through**: write cache + DB together.
- **Write-behind**: write cache, async DB — fast, riskier.
- **Refresh-ahead**: proactively refresh hot keys.

### Eviction and TTL

LRU/LFU/ARC; TTL as safety net; explicit delete on write for correctness-sensitive keys.

### Stampedes

Soft TTL + singleflight/locking; probabilistic early expiration; serve stale while revalidate.""",
            diagram="""```mermaid
sequenceDiagram
    participant C as Client
    participant A as App
    participant R as Redis
    participant D as DB
    C->>A: GET item
    A->>R: GET key
    alt hit
        R-->>A: value
    else miss
        R-->>A: nil
        A->>D: SELECT
        D-->>A: row
        A->>R: SET key TTL
    end
    A-->>C: response
```""",
            dry_run="""Hot key expires; 1,000 concurrent misses without coalescing → 1,000 identical DB queries. With singleflight → 1 DB query, others wait.""",
            code="""```python
import time
from threading import Lock


class CacheAside:
    def __init__(self):
        self.store: dict[str, tuple[str, float]] = {}
        self.locks: dict[str, Lock] = {}

    def get(self, key: str, loader, ttl: float) -> str:
        now = time.time()
        hit = self.store.get(key)
        if hit and hit[1] > now:
            return hit[0]
        lock = self.locks.setdefault(key, Lock())
        with lock:
            hit = self.store.get(key)
            if hit and hit[1] > now:
                return hit[0]
            value = loader(key)
            self.store[key] = (value, now + ttl)
            return value


if __name__ == "__main__":
    c = CacheAside()
    print(c.get("x", lambda k: "v1", 60))
```""",
            complexity="""| Pattern | Read latency | Consistency risk |
| --- | --- | --- |
| Cache-aside | Low on hit | Stale until TTL/delete |
| Write-through | Higher writes | Better alignment |
| Write-behind | Fast writes | Durability risk |""",
            tricks="""- Cache entities by ID; be careful caching query lists.
- Add jitter to TTLs.
- Track hit ratio and eviction causes.
- Negative caching for misses with short TTL.""",
            mistakes="""- Caching without invalidation plan.
- Giant values blowing memory.
- Using cache as source of truth.
- Thundering herd on expiry.""",
            interview="""Default to cache-aside + Redis + TTL + delete-on-write for entities. Mention stampede control and what may go stale.",
            practice="""1. Sketch cache-aside for user profiles (easy)
2. Prevent stampede on a celebrity key (medium)
3. Compare write-through vs delete-on-write (medium)""",
            summary_sheet="""- Cache-aside is the default.
- Invalidate or TTL — never neither.
- Collapse stampedes; jitter TTLs.
- Multi-layer: browser → CDN → app → Redis.""",
            further="""- [Caching strategies](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
- [Redis docs](https://redis.io/docs/)""",
        ),
    )

    write(
        "02-building-blocks",
        "05-sql-vs-nosql.mdx",
        lesson(
            title="SQL vs NoSQL: Choosing a Data Store",
            slug="sql-vs-nosql",
            summary="Compare relational and non-relational stores on schema, queries, transactions, scaling model, and when polyglot persistence wins.",
            duration=35,
            difficulty="intermediate",
            tags=["system-design", "sql", "nosql", "databases"],
            order=5,
            why="Picking the wrong database creates years of pain: missing transactions, painful joins, or a mega-table that cannot shard. System design interviews test whether you match access patterns to storage engines — not brand loyalty.",
            intuition="Spreadsheets with enforced columns and cross-sheet formulas are SQL-like. Stacks of labeled sticky notes you can toss on different desks are document/KV-like. Use the spreadsheet when relationships and constraints matter; sticky notes when you need flexible shape and easy horizontal spread.",
            core="""### Relational (SQL)

Strong schema, rich queries, joins, mature ACID transactions. Scale-up first; scale-out via sharding/Postgres-Citus/Vitess/Spanner-like systems.

### NoSQL families

- **KV / wide-column**: Redis, DynamoDB, Cassandra — primary key access, high write ingest.
- **Document**: MongoDB, Couchbase — JSON documents, secondary indexes.
- **Search**: Elasticsearch — inverted index, not system of record.
- **Graph**: Neo4j — relationship traversal.

### Decision drivers

Access pattern (key lookup vs ad-hoc query), transaction boundary, latency, team expertise, multi-record invariants, analytics needs.""",
            diagram="""```mermaid
flowchart TD
    Q[Access pattern?] -->|Multi-row ACID + joins| SQL[(SQL)]
    Q -->|Key lookup huge scale| KV[(KV / wide-column)]
    Q -->|Flexible docs| Doc[(Document)]
    Q -->|Full-text / facets| Search[(Search index)]
    Q -->|Deep relationships| Graph[(Graph)]
```""",
            dry_run="""Orders need inventory decrement + payment record atomically → SQL or transactional store. Product catalog mostly get-by-id at massive scale → KV/document with care for inventory separately.""",
            code="""```python
def choose_store(needs_acid_multirow: bool, primary_key_only: bool) -> str:
    if needs_acid_multirow:
        return "relational_or_transactional"
    if primary_key_only:
        return "kv_or_wide_column"
    return "document_or_sql_with_indexes"


if __name__ == "__main__":
    print(choose_store(True, False))
    print(choose_store(False, True))
```""",
            complexity="""SQL joins explode if you shard poorly. NoSQL pushes join/aggregation into the app. Operational complexity of distributed SQL can exceed a well-sharded monolith DB for mid scale.",
            tricks="""- Start SQL unless scale/access patterns demand otherwise.
- Use search/analytics as derived stores, not sources of truth.
- Model transactions first, then scale.""",
            mistakes="""- MongoDB for multi-document money transfers without transactions.
- Cassandra for heavy ad-hoc joins.
- One DB for OLTP and heavy OLAP.""",
            interview="""State entities, queries, and invariants. Pick primary store, then optional cache/search. Explain what you give up.",
            practice="""1. Store for banking ledger? (easy)
2. Design polyglot for social network (medium)
3. When to prefer DynamoDB over Postgres (medium)""",
            summary_sheet="""- Match access patterns + invariants.
- SQL default for relational ACID.
- NoSQL for scale/flex of simple keys.
- Polyglot: OLTP + search + cache.""",
            further="""- [AWS purpose-built databases](https://aws.amazon.com/products/databases/)
- [Designing Data-Intensive Applications](https://dataintensive.net/)""",
        ),
    )

    write(
        "02-building-blocks",
        "06-indexing-sharding-replication.mdx",
        lesson(
            title="Indexing, Sharding and Replication",
            slug="indexing-sharding-replication",
            summary="Speed reads with indexes, spread data with shards, and survive faults with replication — including hot keys and rebalancing.",
            duration=45,
            difficulty="advanced",
            tags=["system-design", "sharding", "replication", "indexing"],
            order=6,
            prereqs=["sql-vs-nosql"],
            why="These three knobs appear in every large data design. Bad indexes slow writes; bad shard keys create hotspots; weak replication loses data. You must reason about all three together.",
            intuition="An index is a book index. Sharding is splitting an encyclopedia across volumes by letter. Replication is photocopies of each volume in another library. Wrong letter split (everything under S) makes one volume huge.",
            core="""### Indexing

B+ tree for range, hash for equality, inverted for text, composite order matters (`WHERE a=? AND b=?` loves `(a,b)`). Each index costs write amplification and storage.

### Replication

- **Leader-follower (primary-replica)**: simple reads scale; failover needed.
- **Multi-leader / leaderless**: higher write availability; conflict risk.
- Sync vs async: durability/latency trade-off.

### Sharding

Partition by hash(key), range, or directory. Choose key for even load and query locality. Plan resharding (consistent hashing, dual writes).""",
            diagram="""```mermaid
flowchart TB
    App --> Router[Shard router]
    Router --> S1[(Shard 1 primary)]
    Router --> S2[(Shard 2 primary)]
    S1 --> R1[(Replica)]
    S2 --> R2[(Replica)]
```""",
            dry_run="""User_id hash mod 4. Celebrity user_id gets 30% traffic → one shard hot. Fix: cache celebrity, or split by (user_id, bucket), or isolate hot key.""",
            code="""```python
import hashlib


def shard_for(key: str, n: int) -> int:
    h = hashlib.sha256(key.encode()).hexdigest()
    return int(h, 16) % n


if __name__ == "__main__":
    print([shard_for(f"user-{i}", 4) for i in range(8)])
```""",
            complexity="""| Technique | Read benefit | Write / ops cost |
| --- | --- | --- |
| Extra indexes | Faster filters | Slower writes |
| Async replicas | More read QPS | Stale reads |
| More shards | Parallelism | Cross-shard queries hard |""",
            tricks="""- Shard by tenancy or entity id that matches queries.
- Avoid auto-increment global IDs as shard keys for write hotspots.
- Index only proven slow queries.""",
            mistakes="""- Cross-shard joins in the hot path.
- Single replica async = data loss on primary death.
- Range shard on timestamp → all writes to newest shard.""",
            interview="""Pick primary key/shard key from access patterns, add replicas for HA/reads, indexes for filters, call out hot keys and cross-shard limits.",
            practice="""1. Index for `WHERE user_id=? ORDER BY created_at DESC` (easy)
2. Reshard plan from 4 to 8 shards (medium)
3. Hot-key mitigation for a viral post (medium)""",
            summary_sheet="""- Indexes accelerate reads; tax writes.
- Replication = HA + read scale.
- Shard key decides load balance.
- Plan hotspots and rebalancing early.""",
            further="""- [Vitess sharding](https://vitess.io/docs/overview/what-is-vitess/)
- [Postgres indexing](https://www.postgresql.org/docs/current/indexes.html)""",
        ),
    )

    write(
        "02-building-blocks",
        "07-queues-kafka-pubsub.mdx",
        lesson(
            title="Message Queues, Kafka and Pub/Sub",
            slug="queues-kafka-pubsub",
            summary="Decouple producers and consumers with queues and logs — at-least-once delivery, consumer groups, ordering, and backpressure.",
            duration=40,
            difficulty="advanced",
            tags=["system-design", "kafka", "pubsub", "queues"],
            order=7,
            why="Async messaging absorbs spikes, isolates failures, and enables event-driven architectures. Mixing queue vs log semantics incorrectly causes duplicate processing or lost ordering. Interviews expect delivery guarantees and idempotent consumers.",
            intuition="A ticket counter queue: one customer per clerk, work disappears when done. A library ledger (log): many readers can replay history from an offset. Kafka is the ledger; classic SQS is the ticket counter.",
            core="""### Models

- **Queue / competing consumers**: each message to one worker.
- **Pub/Sub**: fan-out to many subscriptions.
- **Log (Kafka)**: durable partitioned append log; consumer groups share partitions.

### Delivery

At-most-once, at-least-once (common), exactly-once (end-to-end hard; often idempotent processing + dedupe).

### Ordering

Per-partition / per-key ordering in Kafka. Global order kills scale.""",
            diagram="""```mermaid
flowchart LR
    P[Producers] --> T[Kafka topic partitions]
    T --> CG1[Consumer group A]
    T --> CG2[Consumer group B]
    CG1 --> W1[Workers]
    CG2 --> W2[Analytics]
```""",
            dry_run="""Topic with 6 partitions, consumer group with 3 workers → each gets 2 partitions. Add 4th worker idle until rebalance / more partitions.""",
            code="""```python
from collections import deque


class InMemoryQueue:
    def __init__(self):
        self._q: deque[str] = deque()

    def publish(self, msg: str) -> None:
        self._q.append(msg)

    def consume(self) -> str | None:
        return self._q.popleft() if self._q else None


if __name__ == "__main__":
    q = InMemoryQueue()
    q.publish("job-1")
    print(q.consume())
```""",
            complexity="""Brokers add ops cost. Lag is the key SLI. Large fan-out multiplies downstream cost. Retention multiplies storage.",
            tricks="""- Key messages for ordering; size partitions for parallelism.
- Make consumers idempotent; use dedupe keys.
- Alert on lag and DLQ depth.""",
            mistakes="""- Using Kafka as an RPC replacement without timeouts.
- One giant partition for all users.
- Ignoring poison messages (no DLQ).""",
            interview="""Use queue for async jobs; Kafka when multiple consumers need the same stream or replay. State at-least-once + idempotency.",
            practice="""1. Queue vs pub/sub for email sending (easy)
2. Design consumer lag alerting (medium)
3. Preserve per-user order at scale (medium)""",
            summary_sheet="""- Queue = work distribution; log = replayable stream.
- At-least-once → idempotent consumers.
- Order per key/partition, not globally.
- Watch lag and DLQs.""",
            further="""- [Kafka docs](https://kafka.apache.org/documentation/)
- [AWS SQS](https://docs.aws.amazon.com/sqs/)""",
        ),
    )

    write(
        "02-building-blocks",
        "08-api-gateways.mdx",
        lesson(
            title="API Gateways and Edge Policy",
            slug="api-gateways",
            summary="Centralize auth, rate limits, routing, and request shaping at an API gateway without turning it into a god service.",
            duration=30,
            difficulty="intermediate",
            tags=["system-design", "api-gateway", "edge"],
            order=8,
            prereqs=["reverse-proxies"],
            why="Microservices need a single external front door for TLS, authentication, throttling, and versioned routing. Overloading the gateway with business logic recreates a monolith at the worst place — the edge.",
            intuition="An airport security and check-in hall: verify tickets (auth), limit line jumpers (rate limit), direct travelers to gates (routing). The hall should not cook the meals (business logic).",
            core="""### Responsibilities that fit

Authn/authz hooks, rate limiting, request validation, protocol translation, canary routing, request IDs, basic aggregation sparingly.

### Anti-responsibilities

Core domain workflows, multi-step transactions, heavy transformation that changes often with products.

### Patterns

BFF (backend-for-frontend) per client type; gateway + service mesh split (north-south vs east-west).""",
            diagram="""```mermaid
flowchart TB
    Mobile --> GW[API Gateway]
    Web --> GW
    GW --> Auth[Auth service]
    GW --> Orders[Orders]
    GW --> Users[Users]
```""",
            dry_run="""Client calls `GET /v1/me/orders`. Gateway validates JWT, applies per-user rate limit, routes to Orders. Business filtering stays in Orders service.""",
            code="""```python
def gateway_allow(path: str, has_valid_token: bool, rps_used: int, limit: int) -> str:
    if not has_valid_token:
        return "401"
    if rps_used >= limit:
        return "429"
    if not path.startswith("/v1/"):
        return "404"
    return "route"


if __name__ == "__main__":
    print(gateway_allow("/v1/orders", True, 10, 100))
```""",
            complexity="""Gateway is on every request path — keep it lean. Central policy updates are powerful and risky (blast radius).",
            tricks="""- Push JWT validation locally with cached JWKS.
- Version APIs at the gateway.
- Separate admin APIs from public APIs.""",
            mistakes="""- God-gateway with dozens of inline scripts.
- No timeout budgets to backends.
- Dual authorization only at gateway — backends must still enforce.""",
            interview="""Place gateway at edge for cross-cutting concerns; services own domain authz. Mention rate limits and JWT validation.",
            practice="""1. List 5 gateway duties (easy)
2. Design BFF vs single gateway trade-off (medium)
3. Zero-trust: gateway + service auth (medium)""",
            summary_sheet="""- Gateway = policy + routing.
- Keep business logic in services.
- Enforce authz again downstream.
- Guard latency and blast radius.""",
            further="""- [Kong](https://docs.konghq.com/)
- [Envoy Gateway](https://gateway.envoyproxy.io/)""",
        ),
    )

    write(
        "02-building-blocks",
        "09-rate-limiting.mdx",
        lesson(
            title="Rate Limiting Algorithms and Placement",
            slug="rate-limiting",
            summary="Protect systems with token bucket, leaky bucket, fixed/sliding windows, and distributed counters — plus UX for 429s.",
            duration=35,
            difficulty="intermediate",
            tags=["system-design", "rate-limiting", "token-bucket"],
            order=9,
            why="Without rate limits, one noisy client or bot melts your DB. Limits also enforce product tiers. Interview case studies (API gateways, public APIs) almost always include a limiter design.",
            intuition="An hourglass lets sand through at a fixed rate (leaky bucket). A ticket roll that refills over time (token bucket) allows short bursts. Fixed windows are like punch cards that reset at noon — easy but bursty at boundaries.",
            core="""### Algorithms

- **Token bucket**: allows bursts up to bucket size; steady refill.
- **Leaky bucket**: smooth egress rate; queues or drops excess.
- **Fixed window**: count per interval — simple, boundary bursts.
- **Sliding window log / counter**: smoother approximation.

### Placement

Edge/gateway per IP, per API key, per user; service-local limits; downstream bulkheads.

### Distributed

Redis INCR + TTL, or sorted sets for sliding logs; sticky limiter; eventually consistent counts acceptable if slightly soft.""",
            diagram="""```mermaid
flowchart LR
    Client --> GW[Gateway]
    GW --> RL{Rate limiter}
    RL -->|allow| API[API service]
    RL -->|deny 429| Client
    RL --> Redis[(Redis counters)]
```""",
            dry_run="""Limit 100 req/min, token bucket capacity 20. Idle user accrues 20 tokens → can burst 20, then sustained ~1.67 rps.""",
            code="""```python
import time


class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.updated = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


if __name__ == "__main__":
    b = TokenBucket(rate=5, capacity=10)
    print(sum(1 for _ in range(12) if b.allow()))
```""",
            complexity="""Distributed limits add Redis RTT. Overly tight limits hurt UX; overly loose fail open under attack. Exact global limits are expensive — prefer slightly soft limits.",
            tricks="""- Return `Retry-After` and remaining quota headers.
- Separate anonymous vs authenticated buckets.
- Load-shed critical vs non-critical routes differently.""",
            mistakes="""- Fixed window only → double burst at edges.
- Limiting only by IP behind NAT.
- Fail-closed Redis outage taking all traffic down without policy.""",
            interview="""Propose token bucket at gateway, Redis-backed per user id, 429 + Retry-After, mention burst vs sustained and fail-open/closed choice.",
            practice="""1. Implement mental model of token bucket (easy)
2. Design tiered API limits (medium)
3. Avoid fixed-window boundary burst (medium)""",
            summary_sheet="""- Token bucket = bursts + sustained rate.
- Place at edge and deep in stack.
- Soft distributed counts OK.
- Speak HTTP 429 clearly.""",
            further="""- [Stripe rate limiting](https://stripe.com/blog/rate-limiters)
- [Cloudflare rate limiting](https://www.cloudflare.com/learning/bots/what-is-rate-limiting/)""",
        ),
    )

    write(
        "02-building-blocks",
        "10-consistent-hashing.mdx",
        lesson(
            title="Consistent Hashing and Request Affinity",
            slug="consistent-hashing",
            summary="Minimize remapping when nodes join or leave using hash rings, virtual nodes, and keyed affinity for caches and shards.",
            duration=35,
            difficulty="advanced",
            tags=["system-design", "consistent-hashing", "sharding"],
            order=10,
            prereqs=["indexing-sharding-replication"],
            why="Mod-N hashing reshuffles almost all keys when N changes. Consistent hashing remaps only ~1/N keys, enabling elastic caches, DHT-style stores, and sticky routing with less pain.",
            intuition="Imagine a circle clock. Nodes sit at random minute marks; keys walk clockwise to the next node. Add a node: only keys that previously mapped to its clockwise neighbor move. Virtual nodes are multiple marks per server for balance.",
            core="""### Ring mechanics

Hash nodes and keys onto a ring; owner = first node clockwise from key. Replication: next R distinct nodes.

### Virtual nodes

Each physical node gets many ring points → better balance and smoother scaling.

### Use cases

Distributed caches, partitioners, load balancers with affinity, Dynamo-style stores.""",
            diagram="""```mermaid
flowchart LR
    K[key hash] --> Ring[Hash ring]
    Ring --> N1[Node A]
    Ring --> N2[Node B]
    Ring --> N3[Node C]
```""",
            dry_run="""3 nodes, add 4th. Expected remapped fraction ≈ 1/4 of keys. Mod-N would remap ≈ majority.""",
            code="""```python
import hashlib
import bisect


class ConsistentHash:
    def __init__(self, nodes: list[str], vnodes: int = 100):
        self.vnodes = vnodes
        self.ring: list[int] = []
        self.map: dict[int, str] = {}
        for n in nodes:
            self.add(n)

    def _h(self, key: str) -> int:
        return int(hashlib.sha256(key.encode()).hexdigest(), 16)

    def add(self, node: str) -> None:
        for i in range(self.vnodes):
            hv = self._h(f"{node}#{i}")
            bisect.insort(self.ring, hv)
            self.map[hv] = node

    def get(self, key: str) -> str:
        hv = self._h(key)
        idx = bisect.bisect_left(self.ring, hv) % len(self.ring)
        return self.map[self.ring[idx]]


if __name__ == "__main__":
    ch = ConsistentHash(["a", "b", "c"])
    print(ch.get("user-42"))
```""",
            complexity="""O(log N) lookup with binary search on ring. Memory grows with virtual nodes. Without vnodes, imbalance is common.",
            tricks="""- Use many vnodes (hundreds) per physical node.
- Pair with bounded loads to avoid hot nodes.
- For caches: accept remaps as misses, not disasters.""",
            mistakes="""- Too few vnodes → skew.
- Forgetting replica placement diversity (same rack).
- Using consistent hashing when a directory service is simpler at small N.""",
            interview="""Explain mod-N problem, draw ring, mention virtual nodes, apply to cache cluster membership changes.",
            practice="""1. Why virtual nodes? (easy)
2. Estimate remapped keys when doubling cluster (medium)
3. Design cache pool with consistent hashing (medium)""",
            summary_sheet="""- Ring + clockwise ownership.
- ~1/N keys move on membership change.
- Virtual nodes balance load.
- Great for caches and DHTs.""",
            further="""- [Consistent hashing](https://en.wikipedia.org/wiki/Consistent_hashing)
- [Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)""",
        ),
    )

    write(
        "02-building-blocks",
        "11-bloom-filters.mdx",
        lesson(
            title="Bloom Filters and Probabilistic Membership",
            slug="bloom-filters",
            summary="Use Bloom filters to cheaply test set membership with false positives but no false negatives — plus Counting and Cuckoo variants.",
            duration=30,
            difficulty="advanced",
            tags=["system-design", "bloom-filter", "probabilistic"],
            order=11,
            why="At large scale you often need to ask may this key exist? before hitting disk or a remote store. Bloom filters answer in bits with tunable false-positive rates, saving enormous I/O for caches, databases, and URL crawlers.",
            intuition="A set of checkboxes. Adding an item flips several boxes based on hashes. To test membership, check those boxes — if any is off, the item was never added. If all are on, it might be the item or a collision (false positive).",
            core="""### Properties

- **No false negatives** (for standard Bloom without deletes).
- **False positives** possible; rate ≈ (1 − e^(−kn/m))^k for m bits, n items, k hashes.
- Cannot list items; cannot reliably delete (use Counting Bloom / Cuckoo).

### Applications

Cassandra/RocksDB SSTable skips, CDN cache admission, malicious URL sets, username-taken cheap checks before DB.""",
            diagram="""```mermaid
flowchart LR
    Key --> H1[hash1]
    Key --> H2[hash2]
    Key --> H3[hash3]
    H1 --> Bitset[(Bit array)]
    H2 --> Bitset
    H3 --> Bitset
    Bitset --> Decision{All bits set?}
    Decision -->|No| Absent[Definitely not present]
    Decision -->|Yes| Maybe[Probably present]
```""",
            dry_run="""m=32 bits, k=2, insert "apple" sets bits 3 and 17. Query "apple" → maybe/yes. Query "pear" hashes to 3 and 9 → bit 9 clear → definitely no.""",
            code="""```python
import hashlib


class BloomFilter:
    def __init__(self, size: int = 1024, hashes: int = 3):
        self.size = size
        self.hashes = hashes
        self.bits = 0  # simple int bitset for demo

    def _indexes(self, key: str) -> list[int]:
        out = []
        for i in range(self.hashes):
            dig = hashlib.sha256(f"{i}:{key}".encode()).hexdigest()
            out.append(int(dig, 16) % self.size)
        return out

    def add(self, key: str) -> None:
        for idx in self._indexes(key):
            self.bits |= 1 << idx

    def might_contain(self, key: str) -> bool:
        return all(self.bits & (1 << idx) for idx in self._indexes(key))


if __name__ == "__main__":
    b = BloomFilter()
    b.add("apple")
    print(b.might_contain("apple"), b.might_contain("pear"))
```""",
            complexity="""Space is O(m) bits independent of item size. Optimal k ≈ (m/n) ln 2. Too full → FP rate explodes; resize/rebuild needed.",
            tricks="""- Size for expected n and target FP (e.g., 1%).
- Keep Bloom ahead of expensive checks.
- For deletes, prefer Cuckoo filters.""",
            mistakes="""- Treating positive as certain membership.
- Using standard Bloom with frequent deletes.
- Undersizing until FP ≈ random.""",
            interview="""Define FP vs FN, give RocksDB/cache example, sketch bitset + k hashes, mention sizing.",
            practice="""1. Can Bloom have false negatives? (easy)
2. Size filter for 10M URLs at 1% FP (medium)
3. Where to place Bloom in a cache miss path (medium)""",
            summary_sheet="""- Probabilistic set membership.
- No FN; possible FP.
- Great before disk/network.
- Count/Cuckoo when deletes matter.""",
            further="""- [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter)
- [Cuckoo filter](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)""",
        ),
    )


def gen_architecture() -> None:
    items = [
        (
            "01-monolith.mdx",
            "Monolith Architecture",
            "monolith",
            "When a modular monolith is the right default — deployment simplicity, in-process calls, and honest modularity before microservices.",
            1,
            "monolith",
            """A monolith packages UI/API/domain/data access as one deployable unit (often modularized). Prefer it until team size, scale, or release independence force split.""",
            """```mermaid
flowchart TB
    Client --> App[Modular Monolith]
    App --> ModA[Orders module]
    App --> ModB[Users module]
    App --> DB[(Single primary DB)]
```""",
        ),
        (
            "02-microservices.mdx",
            "Microservices Architecture",
            "microservices",
            "Split independently deployable services with clear boundaries, data ownership, and operational overhead you must afford.",
            2,
            "microservices",
            """Microservices: independently deployable services owning their data. Gains: scaling and team autonomy. Costs: distributed transactions, observability, platform maturity.""",
            """```mermaid
flowchart LR
    GW[API Gateway] --> Orders
    GW --> Users
    GW --> Inventory
    Orders --> ODB[(Orders DB)]
    Users --> UDB[(Users DB)]
    Inventory --> IDB[(Inventory DB)]
```""",
        ),
        (
            "03-event-driven.mdx",
            "Event-Driven Architecture",
            "event-driven",
            "React to domain events via brokers for decoupling, fan-out, and temporal flexibility — with idempotency and schema discipline.",
            3,
            "event-driven",
            """Producers emit immutable events; consumers react asynchronously. Excellent for fan-out and decoupling; harder for synchronous user flows and debugging.""",
            """```mermaid
flowchart LR
    Orders --> Bus[Event bus]
    Bus --> Email
    Bus --> Analytics
    Bus --> SearchIndexer
```""",
        ),
        (
            "04-serverless.mdx",
            "Serverless and FaaS Patterns",
            "serverless",
            "Use functions-as-a-service for spiky workloads and managed scale — mindful of cold starts, timeouts, and vendor constraints.",
            4,
            "serverless",
            """FaaS runs handlers without managing servers. Great for bursty, parallelizable work. Limits: cold starts, max duration, stateful workflows need step functions/queues.""",
            """```mermaid
flowchart LR
    API[API Gateway] --> Fn[Functions]
    Fn --> Q[Queue]
    Q --> Fn2[Workers]
    Fn --> DB[(Managed DB)]
```""",
        ),
        (
            "05-cqrs.mdx",
            "CQRS — Command Query Responsibility Segregation",
            "cqrs",
            "Separate write models from read models when query shapes diverge and scale differently from transactional commands.",
            5,
            "cqrs",
            """Commands mutate a write model; queries hit optimized read models updated via events or projections. Adds complexity — use when read/write asymmetry is real.""",
            """```mermaid
flowchart TB
    Client -->|commands| Write[Write API]
    Client -->|queries| Read[Read API]
    Write --> WDB[(Write store)]
    Write --> Events[Events]
    Events --> Proj[Projections]
    Proj --> RDB[(Read store)]
    Read --> RDB
```""",
        ),
        (
            "06-event-sourcing.mdx",
            "Event Sourcing",
            "event-sourcing",
            "Persist state as an append-only stream of events and rebuild projections — auditability with replay complexity.",
            6,
            "event-sourcing",
            """Source of truth is the event log; current state is a fold over events. Superb audit/replay; requires versioning, snapshots, and careful GDPR story.""",
            """```mermaid
flowchart LR
    Cmd[Command] --> Agg[Aggregate]
    Agg --> Log[(Event log)]
    Log --> Snap[Snapshots]
    Log --> View[Read projections]
```""",
        ),
        (
            "07-hexagonal.mdx",
            "Hexagonal Architecture Ports and Adapters",
            "hexagonal",
            "Isolate domain logic behind ports with adapters for HTTP, DB, and messaging so the core stays testable.",
            7,
            "hexagonal",
            """Domain sits in the center; inbound/outbound ports define interfaces; adapters implement frameworks. Keeps business rules free of Express/Django/ORM details.""",
            """```mermaid
flowchart TB
    HTTP[HTTP adapter] --> InPort[Inbound port]
    InPort --> Domain[Domain core]
    Domain --> OutPort[Outbound port]
    OutPort --> SQL[SQL adapter]
    OutPort --> MQ[Queue adapter]
```""",
        ),
        (
            "08-ddd.mdx",
            "Domain-Driven Design Essentials",
            "ddd",
            "Use bounded contexts, ubiquitous language, aggregates, and context maps to carve services and modules that match the business.",
            8,
            "ddd",
            """DDD aligns software with business domains. Bounded contexts prevent one giant model. Aggregates enforce invariants transactionally. Context maps show integration patterns.""",
            """```mermaid
flowchart LR
    Sales[Sales context] -->|ACL| Billing[Billing context]
    Sales -->|shared kernel| Catalog[Catalog context]
```""",
        ),
    ]

    for filename, title, slug, summary, order, tag, core_extra, diagram in items:
        write(
            "03-architecture-styles",
            filename,
            lesson(
                title=title,
                slug=slug,
                summary=summary,
                duration=35,
                difficulty="advanced",
                tags=["system-design", "architecture", tag],
                order=order,
                why=f"Architecture style choices lock in team topology, failure modes, and delivery speed. Understanding {title} helps you pick intentionally instead of copying buzzwords.",
                intuition=f"Treat {title} as a tool with a clear sweet spot. The right style makes change cheap in the places your business changes most; the wrong one multiplies coordination cost.",
                core=f"### Essence\n\n{core_extra}\n\n### When it fits\n\nChoose this style when its benefits match your scale, team boundaries, and consistency needs — and you can pay its operational or conceptual cost.\n\n### Trade-offs\n\nDocument what becomes harder: transactions, debugging, onboarding, or infra. Pair with modularity and testing strategy.",
                diagram=diagram,
                dry_run=f"Walk a single user request through a {slug} deployment: note hop count, data ownership, and failure points. Compare to a simple modular monolith baseline.",
                code="""```python
def style_fit(team_count: int, need_independent_deploys: bool) -> str:
    if team_count <= 2 and not need_independent_deploys:
        return "modular_monolith_first"
    if need_independent_deploys:
        return "consider_microservices_with_platform"
    return "modular_monolith_or_modular_distributed"


if __name__ == "__main__":
    print(style_fit(1, False))
```""",
                complexity="""Complexity shifts from code to operations as you distribute. Measure deploy frequency, change fail rate, and cognitive load — not only request latency.""",
                tricks="""- Start from domain boundaries, not fashion.
- Keep a modular monolith until pain is measured.
- Invest in platform/observability before many services.""",
                mistakes="""- Distributed monolith: many services, one shared DB, chatty sync calls.
- Event soup without schema ownership.
- Overusing CQRS/event sourcing for CRUD apps.""",
                interview=f"Define requirements, propose a simple shape, then say when you would evolve toward {slug}. Emphasize trade-offs and migration path.",
                practice=f"1. Name two pros and cons of {slug} (easy)\n2. Sketch a migration from monolith toward this style (medium)\n3. Identify a bad fit use case (medium)",
                summary_sheet=f"- Know the sweet spot of {slug}.\n- Boundaries and data ownership matter most.\n- Complexity must be justified by scale or teams.\n- Prefer evolutionary architecture.",
                further="""- [Martin Fowler — Architecture](https://martinfowler.com/architecture/)
- [DDD Reference](https://www.domainlanguage.com/ddd/)""",
            ),
        )


if __name__ == "__main__":
    gen_building_blocks()
    gen_architecture()
    print("02+03 done")
