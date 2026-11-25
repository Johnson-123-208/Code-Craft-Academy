# Phase 1 Coverage Checklist

## Infrastructure

| Item | Path |
| --- | --- |
| Env template | `.env.example` |
| Docker Compose | `docker-compose.yml` |
| Makefile | `Makefile` |
| Git ignore | `.gitignore` |
| CI workflow | `.github/workflows/ci.yml` |
| README | `README.md` |
| Sandbox image | `sandbox/Dockerfile` |

## Backend (FastAPI)

| Item | Path |
| --- | --- |
| App entry | `backend/app/main.py` |
| Settings | `backend/app/config.py` |
| Logging | `backend/app/logging_config.py` |
| Schemas | `backend/app/models/schemas.py` |
| Content service | `backend/app/services/content.py` |
| Runner stub | `backend/app/services/runner.py` |
| `GET /health` | `backend/app/routers/health.py` |
| `GET /api/courses` | `backend/app/routers/courses.py` |
| `GET /api/courses/{slug}` | `backend/app/routers/courses.py` |
| `GET /api/lessons/{slug}` | `backend/app/routers/lessons.py` |
| `GET /api/problems` | `backend/app/routers/problems.py` |
| `GET /api/problems/{slug}` | `backend/app/routers/problems.py` |
| `POST /api/run` | `backend/app/routers/run.py` |
| `POST /api/submit` | `backend/app/routers/run.py` |
| `GET /api/search` | `backend/app/routers/search.py` |
| Tests | `backend/tests/test_health.py`, `backend/tests/test_content_api.py` |

## Frontend (Next.js)

| Item | Path |
| --- | --- |
| App shell / theme | `frontend/src/app/layout.tsx`, `globals.css` |
| Home | `frontend/src/app/page.tsx` |
| Catalog | `frontend/src/app/catalog/page.tsx` |
| Course page | `frontend/src/app/courses/[slug]/page.tsx` |
| Lesson page (3-col) | `frontend/src/app/lessons/[slug]/page.tsx` |
| Playground | `frontend/src/app/playground/page.tsx` |
| Practice list | `frontend/src/app/practice/page.tsx` |
| Problem detail | `frontend/src/app/practice/[slug]/page.tsx` |
| Search | `frontend/src/app/search/page.tsx` |
| Header / footer | `frontend/src/components/layout/*` |
| shadcn-style UI | `frontend/src/components/ui/*` |
| MDX + callouts | `frontend/src/components/mdx/*` |
| Mermaid | `frontend/src/components/mdx/mermaid.tsx` |
| Monaco editor | `frontend/src/components/playground/*` |
| Fuse.js search | `frontend/src/lib/search.ts` |
| Content loader | `frontend/src/lib/content.ts` |

## Sample content (pipeline demos; full courses in later phases)

| Topic | File |
| --- | --- |
| Python — Intro & setup | `content/python/01-getting-started/01-intro-and-setup.mdx` |
| DSA — Big-O | `content/dsa/01-foundations/01-big-o-and-complexity.mdx` |
| System Design — Scalability | `content/system-design/01-fundamentals/01-scalability-availability-reliability.mdx` |
| Cloud — AWS overview | `content/cloud-devops/01-cloud-fundamentals/01-cloud-and-aws-overview.mdx` |
| AI/ML — Linear algebra | `content/ai-ml/01-math-foundations/01-linear-algebra-for-ml.mdx` |
| Problem — Two Sum | `content/problems/two-sum.json` |

## Custom MDX components

`Tip`, `Warning`, `Trick`, `InterviewNote`, `Pitfall`, `ComplexityTable`, `Visualizer`, Mermaid fenced blocks (` ```mermaid `).

## Deferred to Phase 2+

- Full Docker sandbox execution + malicious-case test suite
- Pyodide client fallback wiring end-to-end
- Complete course lesson sets and 300+ problems
