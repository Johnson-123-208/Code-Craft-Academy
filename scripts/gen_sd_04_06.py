#!/usr/bin/env python3
"""Generate modules 04-communication, 05-reliability, 06-security."""
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


def gen_communication() -> None:
    specs = [
        (
            "01-rest.mdx",
            "REST APIs and Resource Design",
            "rest",
            "Design resource-oriented HTTP APIs with status codes, idempotency, pagination, and versioning.",
            1,
            """REST uses resources, URLs, and HTTP verbs. Favor nouns, correct status codes, pagination (cursor preferred), optimistic concurrency with ETags, and explicit versioning strategy.""",
            """```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as DB
    C->>A: GET /orders/42
    A->>D: load
    D-->>A: row
    A-->>C: 200 JSON
    C->>A: POST /orders
    A->>D: insert
    A-->>C: 201 Location
```""",
        ),
        (
            "02-grpc.mdx",
            "gRPC and Protobuf Services",
            "grpc",
            "Use HTTP/2 + Protobuf for efficient service-to-service RPCs with streaming and strong contracts.",
            2,
            """gRPC pairs Protobuf schemas with HTTP/2. Benefits: compact payloads, codegen stubs, streaming. Challenges: browser support (grpc-web), load balancer visibility, human debuggability vs JSON.""",
            """```mermaid
flowchart LR
    SvcA[Service A] -->|HTTP/2 gRPC| SvcB[Service B]
    SvcA -->|protobuf| SvcB
```""",
        ),
        (
            "03-graphql.mdx",
            "GraphQL APIs and Schema Design",
            "graphql",
            "Query graphs flexibly while controlling N+1, authz, and caching challenges unique to GraphQL.",
            3,
            """Clients specify fields; one endpoint serves many views. Great for BFFs. Risks: unbounded queries, N+1 resolvers, harder CDN caching. Mitigate with depth/cost limits, DataLoader, persisted queries.""",
            """```mermaid
flowchart TB
    Client -->|query| GW[GraphQL gateway]
    GW --> Users
    GW --> Orders
    GW --> Inventory
```""",
        ),
        (
            "04-websockets.mdx",
            "WebSockets and Real-Time Channels",
            "websockets",
            "Maintain bidirectional channels for chat, presence, and live updates — with fan-out and reconnect design.",
            4,
            """WebSockets upgrade HTTP to a persistent duplex channel. Need sticky LB or pub/sub fan-out across nodes, heartbeats, backoff reconnect, and auth on connect + periodic refresh.""",
            """```mermaid
flowchart LR
    Browser <-->|WebSocket| GS[Gateway servers]
    GS <--> Redis[(Pub/Sub)]
    GS --> App[App services]
```""",
        ),
        (
            "05-service-discovery.mdx",
            "Service Discovery and Service Registry",
            "service-discovery",
            "Locate healthy instances via DNS, registries, or mesh endpoints as fleets change.",
            5,
            """Clients or proxies resolve service names to instance sets. Patterns: client-side (Consul/Eureka), server-side (DNS/LB), service mesh control plane. Health and readiness must drive membership.""",
            """```mermaid
flowchart TB
    Svc[Service instance] -->|register| Reg[Registry]
    Client --> Proxy[Sidecar / LB]
    Proxy -->|discover| Reg
    Proxy --> Svc
```""",
        ),
        (
            "06-circuit-breakers.mdx",
            "Circuit Breakers and Bulkheads",
            "circuit-breakers",
            "Fail fast when dependencies degrade using closed/open/half-open states and isolation bulkheads.",
            6,
            """Circuit breaker trips after error/latency thresholds, short-circuits calls, then probes half-open. Bulkheads isolate thread/connection pools so one dependency cannot exhaust the process.""",
            """```mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: failures exceed threshold
    Open --> HalfOpen: cooldown elapsed
    HalfOpen --> Closed: probe success
    HalfOpen --> Open: probe failure
```""",
        ),
        (
            "07-retries.mdx",
            "Retries, Timeouts and Backoff",
            "retries",
            "Combine deadlines, jittered exponential backoff, and budgets so retries heal blips without amplifying outages.",
            7,
            """Every call needs a timeout. Retries help transient faults only on idempotent ops. Use exponential backoff + jitter, retry budgets, and honor `Retry-After`. Propagate deadlines across the call chain.""",
            """```mermaid
sequenceDiagram
    participant A as Caller
    participant B as Dependency
    A->>B: attempt 1
    B-->>A: timeout
    Note over A: backoff + jitter
    A->>B: attempt 2
    B-->>A: 200
```""",
        ),
        (
            "08-idempotency.mdx",
            "Idempotency Keys and Safe Retries",
            "idempotency",
            "Make mutating APIs safely retriable with idempotency keys, dedupe stores, and exactly-once effects where needed.",
            8,
            """Idempotent operations produce the same effect when retried. Use client idempotency keys stored with request hash and response; expire keys carefully. Critical for payments and order creation.""",
            """```mermaid
flowchart TD
    Client -->|Idempotency-Key| API
    API --> Store[(Key store)]
    Store -->|seen| Replay[Return saved response]
    Store -->|new| Exec[Execute once + save]
```""",
        ),
        (
            "09-sagas.mdx",
            "Sagas and Distributed Transactions",
            "sagas",
            "Coordinate multi-service workflows with choreography or orchestration and compensating actions.",
            9,
            """When 2PC is too costly, sagas sequence local transactions with compensations on failure. Orchestration: central coordinator. Choreography: events trigger next steps. Need idempotency and clarity on partial states.""",
            """```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant Ord as Orders
    participant Pay as Payments
    participant Inv as Inventory
    O->>Ord: create
    O->>Pay: charge
    O->>Inv: reserve
    alt payment fails
        O->>Ord: cancel compensate
    end
```""",
        ),
    ]

    for filename, title, slug, summary, order, core_extra, diagram in specs:
        write(
            "04-communication",
            filename,
            lesson(
                title=title,
                slug=slug,
                summary=summary,
                duration=35,
                difficulty="advanced",
                tags=["system-design", "communication", slug],
                order=order,
                why=f"Distributed systems live or die by how services talk. Mastering {title} prevents brittle integrations, retry storms, and inconsistent state across boundaries.",
                intuition=f"Picture teams exchanging work orders. Protocols define the form; reliability patterns define what happens when a messenger is late or duplicates a message. {title} is one essential pattern in that toolkit.",
                core=f"### Core ideas\n\n{core_extra}\n\n### Design checklist\n\nDefine success/failure semantics, timeouts, payload schemas, auth, and versioning. Write down what clients should do on 429/503 and partial failure.",
                diagram=diagram,
                dry_run=f"Trace one happy path and one failure path involving {slug}. Note duplicates, ordering, and user-visible state.",
                code="""```python
def should_retry(status: int, method: str, attempts: int, max_attempts: int = 3) -> bool:
    if attempts >= max_attempts:
        return False
    if method.upper() not in {"GET", "HEAD", "PUT", "DELETE"} and status != 409:
        # POST only if caller uses idempotency keys
        return False
    return status in {408, 425, 429, 500, 502, 503, 504}


if __name__ == "__main__":
    print(should_retry(503, "GET", 1))
```""",
                complexity="""Extra hops and payloads cost latency. Strong contracts (protobuf/graphql schemas) reduce coupling bugs but need ownership. Reliability wrappers add state (breaker, keys).",
                tricks="""- Propagate trace/deadline headers.
- Prefer cursor pagination over offset.
- Make write APIs idempotent when clients retry.""",
                mistakes="""- Infinite retries without jitter.
- Chatty sync call graphs between microservices.
- Ignoring poison messages and schema evolution.""",
                interview=f"Explain where {slug} sits in the design, failure behavior, and one alternative. Tie to concrete requirements (latency, fan-out, consistency).",
                practice=f"1. Summarize {slug} in two sentences (easy)\n2. Failure-mode design for this pattern (medium)\n3. Compare to a close alternative (medium)",
                summary_sheet=f"- Know when to use {slug}.\n- Define timeouts and failure semantics.\n- Version contracts deliberately.\n- Observe every hop.",
                further="""- [Microsoft REST API guidelines](https://github.com/microsoft/api-guidelines)
- [gRPC docs](https://grpc.io/docs/)
- [Microservices patterns — Saga](https://microservices.io/patterns/data/saga.html)""",
            ),
        )


def gen_reliability() -> None:
    items = [
        (
            "01-observability.mdx",
            "Observability: Logs, Metrics and Traces",
            "observability",
            "Build the three pillars plus continuous profiling so you can ask new questions of production without redeploying.",
            1,
            """Logs (events), metrics (aggregates), traces (request graphs). Add exemplars linking metrics to traces. Structure logs; use RED/USE methods; sample traces thoughtfully.""",
            """```mermaid
flowchart LR
    App --> Logs
    App --> Metrics
    App --> Traces
    Logs --> Backend[OTel / ELK]
    Metrics --> Prom[Prometheus]
    Traces --> Jaeger[Jaeger / Tempo]
```""",
        ),
        (
            "02-slo-sli-sla.mdx",
            "SLIs, SLOs, SLAs and Error Budgets",
            "slo-sli-sla",
            "Quantify reliability with indicators, objectives, agreements, and error budgets that guide release velocity.",
            2,
            """SLI: measured indicator (availability, latency). SLO: target (99.9% monthly). SLA: customer contract with consequences. Error budget = 1 − SLO; freeze risky changes when exhausted.""",
            """```mermaid
flowchart TD
    SLI[SLI measurements] --> SLO[SLO targets]
    SLO --> Budget[Error budget]
    Budget --> Release[Release decisions]
    SLO --> SLA[External SLA]
```""",
        ),
        (
            "03-chaos-engineering.mdx",
            "Chaos Engineering and Failure Injection",
            "chaos-engineering",
            "Scientifically inject faults to validate hypotheses about resilience before real outages do.",
            3,
            """Start with a steady-state hypothesis, inject latency/kill pods/partition networks in controlled blast radius, observe SLOs, automate in CI/staging then production carefully. Chaos without observability is vandalism.""",
            """```mermaid
flowchart LR
    Hyp[Hypothesis] --> Inject[Inject fault]
    Inject --> Observe[Observe SLOs]
    Observe --> Learn[Learn / fix]
    Learn --> Hyp
```""",
        ),
        (
            "04-disaster-recovery.mdx",
            "Disaster Recovery: RPO, RTO and Multi-Region",
            "disaster-recovery",
            "Plan backups, failover, and multi-region strategies against RPO/RTO targets that leadership understands.",
            4,
            """RPO: how much data you may lose. RTO: how fast you restore service. Patterns: backup/restore, pilot light, warm standby, active-active. Test restores — untested backups are fiction.""",
            """```mermaid
flowchart TB
    Users --> Primary[Primary region]
    Primary -->|async/sync repl| Secondary[DR region]
    Primary --> Backups[(Backups)]
    Secondary -->|failover| Users
```""",
        ),
    ]

    for filename, title, slug, summary, order, core_extra, diagram in items:
        write(
            "05-reliability",
            filename,
            lesson(
                title=title,
                slug=slug,
                summary=summary,
                duration=35,
                difficulty="advanced",
                tags=["system-design", "reliability", slug],
                order=order,
                why=f"Reliability work is only as good as your ability to measure, target, test, and recover. {title} is a core practice for production systems and senior interviews.",
                intuition=f"Think of a hospital: monitors (observability), vital thresholds (SLOs), fire drills (chaos), and evacuation plans (DR). {title} maps to one of those disciplines.",
                core=f"### Deep dive\n\n{core_extra}\n\n### Operating model\n\nTie alerts to user pain (SLO burn), runbooks to actions, and game days to muscle memory.",
                diagram=diagram,
                dry_run=f"Pick a checkout API. Define one SLI, inject one fault relevant to {slug}, and state the expected user impact and rollback.",
                code="""```python
def error_budget_remaining(slo: float, good: int, total: int) -> float:
    \"\"\"Return remaining budget ratio for the window (1.0 = full).\"\"\"
    if total <= 0:
        return 1.0
    allowed_bad = (1.0 - slo) * total
    bad = total - good
    if allowed_bad <= 0:
        return 0.0
    return max(0.0, 1.0 - bad / allowed_bad)


if __name__ == "__main__":
    print(round(error_budget_remaining(0.999, 998_500, 1_000_000), 3))
```""",
                complexity="""More regions and richer telemetry cost money and attention. Over-alerting creates pager fatigue; under-instrumentation creates flying blind. Balance cardinality.",
                tricks="""- Alert on burn rate, not raw CPU.
- Practice failover quarterly.
- Keep runbooks next to dashboards.""",
                mistakes="""- SLAs tighter than measured SLOs.
- Chaos in prod without blast radius limits.
- Backups never restored.""",
                interview=f"Define user journeys, pick SLIs/SLOs, then explain how {slug} validates or restores them. Use RPO/RTO numbers when DR appears.",
                practice=f"1. Define SLI for a read API (easy)\n2. Apply {slug} to a multi-region chat app (medium)\n3. Write a failure hypothesis and test (medium)",
                summary_sheet=f"- Measure user-centric SLIs.\n- Budget errors deliberately.\n- Practice {slug} before incidents.\n- Test restores and failovers.",
                further="""- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Principles of Chaos Engineering](https://principlesofchaos.org/)""",
            ),
        )


def gen_security() -> None:
    items = [
        (
            "01-authn-authz.mdx",
            "Authentication and Authorization",
            "authn-authz",
            "Separate proving identity from granting permissions with sessions, RBAC, ABAC, and least privilege.",
            1,
            """Authn verifies who; authz decides what. Patterns: session cookies, tokens, mTLS between services. Models: RBAC, ABAC, ReBAC. Enforce authz in every service — edge checks are not enough.""",
            """```mermaid
flowchart LR
    User --> Login[Authn]
    Login --> Token[Session / token]
    Token --> API
    API --> Authz{Authorized?}
    Authz -->|yes| Resource
    Authz -->|no| Deny[403]
```""",
        ),
        (
            "02-oauth2.mdx",
            "OAuth 2.0 and OpenID Connect",
            "oauth2",
            "Delegate access with authorization codes, PKCE, refresh tokens, and OIDC identity layers — safely.",
            2,
            """OAuth 2.0 delegates authorization; OIDC adds identity (ID token). Prefer auth code + PKCE for public clients. Avoid implicit flow. Scopes limit access; rotate refresh tokens; use exact redirect URI match.""",
            """```mermaid
sequenceDiagram
    participant U as User
    participant App as Client app
    participant AS as Auth server
    participant API as Resource API
    U->>App: login
    App->>AS: authorize + PKCE
    AS->>U: consent
    AS-->>App: auth code
    App->>AS: code + verifier
    AS-->>App: access + refresh
    App->>API: Bearer access token
```""",
        ),
        (
            "03-jwt.mdx",
            "JWTs: Claims, Validation and Pitfalls",
            "jwt",
            "Use signed JWTs for stateless claims while avoiding alg=none, oversized tokens, and revocation traps.",
            3,
            """JWT = header.payload.signature. Validate iss, aud, exp, signature (JWKS). Prefer short TTL + refresh. Revocation needs blocklists or versioned sessions. Do not store secrets in payloads — they are readable.""",
            """```mermaid
flowchart TD
    Client -->|Bearer JWT| API
    API --> V{Validate sig + claims}
    V -->|ok| Handler
    V -->|fail| Unauthorized[401]
    API --> JWKS[JWKS cache]
```""",
        ),
        (
            "04-encryption.mdx",
            "Encryption in Transit and at Rest",
            "encryption",
            "Apply TLS everywhere, manage keys with KMS/HSM, and understand envelope encryption for data at rest.",
            4,
            """TLS protects data in transit; disk/DB encryption and field-level crypto protect at rest. Envelope encryption: DEK encrypts data, KEK in KMS wraps DEKs. Mind key rotation, nonce reuse, and client-side vs server-side encryption trade-offs.""",
            """```mermaid
flowchart LR
    App --> DEK[Data key]
    DEK --> Cipher[(Encrypted data)]
    DEK --> KMS[KMS wrap]
    KMS --> Wrapped[(Wrapped DEK)]
```""",
        ),
        (
            "05-owasp.mdx",
            "OWASP Top Risks for Backend Engineers",
            "owasp",
            "Defend against injection, broken auth, SSRF, misconfig, and other OWASP risks in modern APIs.",
            5,
            """Focus: injection (SQL/NoSQL/cmd), broken authn, SSRF, insecure design, misconfiguration, vulnerable components, integrity failures, logging gaps, and access control flaws. Secure defaults, parameterized queries, allowlists, and dependency scanning.""",
            """```mermaid
flowchart TB
    Threats[OWASP risks] --> Controls
    Controls --> Param[Parameterized queries]
    Controls --> Auth[Strong authn/authz]
    Controls --> Allow[URL allowlists]
    Controls --> Patch[Dependency patching]
```""",
        ),
    ]

    for filename, title, slug, summary, order, core_extra, diagram in items:
        write(
            "06-security",
            filename,
            lesson(
                title=title,
                slug=slug,
                summary=summary,
                duration=35,
                difficulty="advanced",
                tags=["system-design", "security", slug],
                order=order,
                why=f"Security failures are system design failures. {title} shows up in every public API and case study — interviewers expect concrete controls, not slogans.",
                intuition=f"Security is layered doors and keys. {title} is one door mechanism; attackers walk around missing layers. Design defense-in-depth.",
                core=f"### Essentials\n\n{core_extra}\n\n### Engineering habits\n\nThreat-model new features, least privilege IAM, secrets in a vault, and continuous dependency updates.",
                diagram=diagram,
                dry_run=f"Threat-model a password-reset flow with focus on {slug}: list two attacks and two mitigations.",
                code="""```python
import hmac
import hashlib


def constant_time_equals(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode(), b.encode())


def hash_password(password: str, salt: bytes, iterations: int = 120_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)


if __name__ == "__main__":
    assert constant_time_equals("abc", "abc")
```""",
                complexity="""Crypto and auth add latency and ops (key rotation, JWKS caches). Overly complex custom crypto is worse than standard TLS + KMS.""",
                tricks="""- Short-lived tokens; rotate refresh tokens.
- Parameterize every query.
- Deny by default in authz.""",
                mistakes="""- Rolling your own crypto.
- Long-lived JWTs with no revocation plan.
- Trusting client-side checks only.""",
                interview=f"Place {slug} in the architecture diagram, state trust boundaries, and mention one hard failure mode (theft, SSRF, alg confusion).",
                practice=f"1. Authn vs authz difference (easy)\n2. Harden an endpoint related to {slug} (medium)\n3. Design secret rotation (medium)",
                summary_sheet=f"- Apply {slug} at trust boundaries.\n- Least privilege everywhere.\n- Standards beat custom crypto.\n- Log security events.""",
                further="""- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OAuth 2.1 draft / best practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [JWT best practices](https://datatracker.ietf.org/doc/html/rfc8725)""",
            ),
        )


if __name__ == "__main__":
    gen_communication()
    gen_reliability()
    gen_security()
    print("04-06 done")
