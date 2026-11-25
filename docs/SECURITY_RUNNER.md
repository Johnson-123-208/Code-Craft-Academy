# Code execution security

## Threat model

`/api/run` and `/api/submit` execute **untrusted** Python. Attackers may attempt:

- Infinite loops / CPU exhaustion
- Memory bombs
- Fork bombs / process exhaustion
- Filesystem reads/writes outside the workspace
- Network exfiltration
- Escape to the host via Docker misconfiguration

## Controls (Docker mode)

| Control | Setting |
| --- | --- |
| No network | `--network none` / `network_mode=none` |
| Memory | `SANDBOX_MEMORY_MB` (default 256) |
| PIDs | `SANDBOX_PIDS_LIMIT` (default 64) |
| CPU | 1 nano_cpu equivalent |
| Wall clock | `SANDBOX_TIMEOUT_SECONDS` (default 5) |
| Output cap | `SANDBOX_OUTPUT_LIMIT_BYTES` (64KB) |
| Filesystem | read-only root + small `/tmp` tmpfs |
| User | UID 1000 non-root |
| Image | minimal `codecraft-sandbox` with allowlisted scientific libs |

## Controls (always)

- Per-IP rate limits via slowapi
- Request size limits
- Structured logging of run metadata (not full secrets)

## Pyodide fallback

When `NEXT_PUBLIC_USE_PYODIDE=true`, code runs in the **learner's browser** (WebAssembly). This is appropriate for demos and hosts without Docker. Hidden tests should still be evaluated server-side when a secure sandbox exists; visible tests may run client-side.

## Subprocess fallback (`SANDBOX_DISABLED=true`)

Intended for **local CI and trusted development only**. It is **not** multi-tenant safe.

## Operational guidance

- Do not mount the Docker socket into an internet-exposed backend unless you fully understand the escape risk.
- Prefer ECS task isolation or gVisor/Firecracker for production multi-tenant runners.
- Monitor rate-limit hits and kill rates; ban abusive IPs at the edge (WAF / ALB).
