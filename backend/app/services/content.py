"""Load courses, lessons, and problems from the content directory."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import frontmatter
import structlog
import yaml

from app.config import get_settings
from app.models.schemas import (
    CourseDetail,
    CourseSummary,
    LessonDetail,
    LessonSummary,
    ModuleSummary,
    ProblemDetail,
    ProblemExample,
    ProblemSummary,
    SearchHit,
)

logger = structlog.get_logger(__name__)

COURSE_META: dict[str, dict[str, Any]] = {
    "python": {
        "title": "Python from Zero to Advanced",
        "summary": (
            "A complete Python curriculum from first REPL session to packaging, "
            "concurrency, testing, and production APIs."
        ),
        "category": "Programming",
        "difficulty": "beginner",
        "tags": ["python", "oop", "asyncio", "testing"],
        "thumbnail": "/images/courses/python.svg",
        "prerequisites": ["None — start from absolute zero"],
        "learning_outcomes": [
            "Write idiomatic, production-quality Python",
            "Master OOP, generators, decorators, and concurrency",
            "Test, package, and ship Python applications",
        ],
        "description": (
            "This course takes you from installing Python to writing clean, typed, "
            "tested code. Every lesson pairs deep explanation with runnable examples "
            "you can edit in the in-browser playground."
        ),
    },
    "dsa": {
        "title": "Data Structures and Algorithms",
        "summary": (
            "Master Big-O, classic data structures, and problem-solving patterns "
            "with dry-runs, diagrams, and hundreds of practice problems."
        ),
        "category": "Algorithms",
        "difficulty": "intermediate",
        "tags": ["dsa", "algorithms", "interview", "big-o"],
        "thumbnail": "/images/courses/dsa.svg",
        "prerequisites": ["Comfortable with basic Python syntax"],
        "learning_outcomes": [
            "Analyze time and space complexity rigorously",
            "Implement and apply core data structures",
            "Recognize and apply the major problem-solving patterns",
        ],
        "description": (
            "A mastery track for interviews and real engineering: arrays to graphs, "
            "DP frameworks, string algorithms, and a pattern cheat sheet."
        ),
    },
    "system-design": {
        "title": "System Design and Software Architecture",
        "summary": (
            "Scalability, building blocks, architecture styles, and full case "
            "studies from URL shorteners to ML inference platforms."
        ),
        "category": "Architecture",
        "difficulty": "advanced",
        "tags": ["system-design", "distributed-systems", "architecture"],
        "thumbnail": "/images/courses/system-design.svg",
        "prerequisites": ["1+ years of backend experience recommended"],
        "learning_outcomes": [
            "Estimate capacity and choose the right building blocks",
            "Design for availability, consistency, and latency trade-offs",
            "Produce interview-ready architecture diagrams and designs",
        ],
        "description": (
            "From CAP and PACELC to Kafka, caching, and end-to-end case studies "
            "with Mermaid architecture diagrams."
        ),
    },
    "cloud-devops": {
        "title": "Cloud, DevOps, CI/CD and Deployment",
        "summary": (
            "AWS core services, Terraform, Docker, Kubernetes, CI/CD pipelines, "
            "observability, and hands-on deployment of this very platform."
        ),
        "category": "Cloud & DevOps",
        "difficulty": "intermediate",
        "tags": ["aws", "docker", "kubernetes", "terraform", "cicd"],
        "thumbnail": "/images/courses/cloud-devops.svg",
        "prerequisites": ["Basic Linux and networking familiarity"],
        "learning_outcomes": [
            "Provision and operate workloads on AWS",
            "Containerize apps and orchestrate with Kubernetes",
            "Build secure CI/CD pipelines and monitor production",
        ],
        "description": (
            "A practical DevOps path covering cloud fundamentals through "
            "GitOps, with architecture diagrams for deploying CodeCraft Academy."
        ),
    },
    "ai-ml": {
        "title": "AI / ML / Data Science",
        "summary": (
            "Math foundations, classical ML from scratch, deep learning, NLP/LLMs, "
            "MLOps, and AWS SageMaker end to end."
        ),
        "category": "AI & Machine Learning",
        "difficulty": "advanced",
        "tags": ["machine-learning", "deep-learning", "sagemaker", "nlp"],
        "thumbnail": "/images/courses/ai-ml.svg",
        "prerequisites": ["Python fluency", "High-school math (refreshers included)"],
        "learning_outcomes": [
            "Derive and implement core ML algorithms from scratch",
            "Train, evaluate, and serve models with modern tooling",
            "Operate ML systems with MLOps and SageMaker",
        ],
        "description": (
            "Deep coverage from linear algebra intuition to Transformers, RAG, "
            "and production SageMaker pipelines — all with runnable Python."
        ),
    },
}

MODULE_TITLES: dict[str, str] = {
    "01-getting-started": "Getting Started",
    "01-foundations": "Foundations: Complexity and Approach",
    "01-fundamentals": "Fundamentals",
    "01-cloud-fundamentals": "Cloud Fundamentals",
    "02-aws-core": "AWS Core Services",
    "03-terraform": "Terraform",
    "04-docker": "Docker",
    "05-kubernetes": "Kubernetes",
    "06-cicd": "CI/CD",
    "07-linux-networking": "Linux and Networking",
    "08-monitoring-cost": "Monitoring and Cost",
    "09-deploy-codecraft": "Deploy CodeCraft",
    "01-math-foundations": "Math Foundations",
    "02-python-data": "Python for Data",
    "03-ml-fundamentals": "ML Fundamentals",
    "04-classical-ml": "Classical Machine Learning",
    "05-deep-learning": "Deep Learning",
    "06-nlp-llms": "NLP and Large Language Models",
    "07-cv-timeseries-xai": "Vision, Time Series, and Explainability",
    "08-mlops": "MLOps",
    "09-sagemaker": "AWS SageMaker",
    "10-capstones": "Capstone Projects",
    "02-arrays-strings": "Arrays and Strings",
    "03-hashing": "Hashing",
    "04-linked-lists": "Linked Lists",
    "05-stacks-queues": "Stacks and Queues",
    "06-recursion-backtracking": "Recursion and Backtracking",
    "07-searching-sorting": "Searching and Sorting",
    "08-trees": "Trees",
    "09-heaps": "Heaps",
    "10-graphs": "Graphs",
    "11-dp": "Dynamic Programming",
    "12-greedy": "Greedy Algorithms",
    "13-bit-manipulation": "Bit Manipulation",
    "14-math-number-theory": "Math and Number Theory",
    "15-string-algorithms": "String Algorithms",
    "16-advanced": "Advanced Techniques",
    "17-patterns-interview": "Patterns and Interview Strategy",
}


def _content_root() -> Path:
    return get_settings().content_path


def _slugify_filename(name: str) -> str:
    return name.removesuffix(".mdx").removesuffix(".md")


def _parse_lesson(path: Path, course: str, module: str) -> LessonSummary:
    post = frontmatter.load(path)
    meta = post.metadata
    slug = meta.get("slug") or _slugify_filename(path.name)
    return LessonSummary(
        slug=slug,
        title=str(meta.get("title", slug)),
        summary=str(meta.get("summary", "")),
        duration=int(meta.get("duration", 15)),
        difficulty=str(meta.get("difficulty", "beginner")),
        order=int(meta.get("order", 0)),
        tags=list(meta.get("tags", [])),
        module=module,
        course=course,
    )


def _iter_lesson_files(course: str | None = None) -> list[tuple[str, str, Path]]:
    root = _content_root()
    results: list[tuple[str, str, Path]] = []
    courses = [course] if course else list(COURSE_META.keys())
    for c in courses:
        course_dir = root / c
        if not course_dir.is_dir():
            continue
        for module_dir in sorted(p for p in course_dir.iterdir() if p.is_dir()):
            for lesson_file in sorted(module_dir.glob("*.mdx")):
                results.append((c, module_dir.name, lesson_file))
    return results


def list_courses() -> list[CourseSummary]:
    root = _content_root()
    courses: list[CourseSummary] = []
    for slug, meta in COURSE_META.items():
        lessons = _iter_lesson_files(slug)
        total_minutes = 0
        for c, module, path in lessons:
            summary = _parse_lesson(path, c, module)
            total_minutes += summary.duration
        courses.append(
            CourseSummary(
                slug=slug,
                title=meta["title"],
                summary=meta["summary"],
                category=meta["category"],
                difficulty=meta["difficulty"],
                duration_hours=round(total_minutes / 60, 1) if total_minutes else 0,
                lesson_count=len(lessons),
                tags=meta["tags"],
                thumbnail=meta.get("thumbnail"),
            )
        )
    return courses


def get_course(slug: str) -> CourseDetail | None:
    meta = COURSE_META.get(slug)
    if meta is None:
        return None

    lesson_files = _iter_lesson_files(slug)
    modules_map: dict[str, list[LessonSummary]] = {}
    for course, module, path in lesson_files:
        lesson = _parse_lesson(path, course, module)
        modules_map.setdefault(module, []).append(lesson)

    modules: list[ModuleSummary] = []
    for idx, (module_slug, lessons) in enumerate(sorted(modules_map.items())):
        lessons_sorted = sorted(lessons, key=lambda x: x.order)
        title = MODULE_TITLES.get(
            module_slug,
            module_slug.replace("-", " ").title(),
        )
        # Prefer title from first lesson's module frontmatter if present later
        modules.append(
            ModuleSummary(
                slug=module_slug,
                title=title,
                order=idx + 1,
                lessons=lessons_sorted,
            )
        )

    summary = next((c for c in list_courses() if c.slug == slug), None)
    if summary is None:
        return None

    return CourseDetail(
        **summary.model_dump(),
        prerequisites=meta.get("prerequisites", []),
        learning_outcomes=meta.get("learning_outcomes", []),
        modules=modules,
        description=meta.get("description", ""),
    )


def _all_lessons_ordered(course: str) -> list[LessonSummary]:
    files = _iter_lesson_files(course)
    lessons = [_parse_lesson(path, c, m) for c, m, path in files]
    # Sort by module name then order
    return sorted(lessons, key=lambda L: (L.module, L.order))


def get_lesson(slug: str) -> LessonDetail | None:
    for course, module, path in _iter_lesson_files():
        post = frontmatter.load(path)
        meta = post.metadata
        lesson_slug = meta.get("slug") or _slugify_filename(path.name)
        if lesson_slug != slug:
            continue

        ordered = _all_lessons_ordered(course)
        idx = next((i for i, L in enumerate(ordered) if L.slug == slug), None)
        prev_slug = ordered[idx - 1].slug if idx is not None and idx > 0 else None
        next_slug = (
            ordered[idx + 1].slug
            if idx is not None and idx < len(ordered) - 1
            else None
        )

        return LessonDetail(
            slug=lesson_slug,
            title=str(meta.get("title", slug)),
            summary=str(meta.get("summary", "")),
            duration=int(meta.get("duration", 15)),
            difficulty=str(meta.get("difficulty", "beginner")),
            order=int(meta.get("order", 0)),
            tags=list(meta.get("tags", [])),
            module=module,
            course=course,
            prerequisites=list(meta.get("prerequisites", [])),
            content=post.content,
            previous_slug=prev_slug,
            next_slug=next_slug,
        )
    return None


def _problems_dir() -> Path:
    return _content_root() / "problems"


def _load_problem_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Problem file must be an object: {path}")
    return data


def list_problems(
    topic: str | None = None,
    difficulty: str | None = None,
    company: str | None = None,
) -> list[ProblemSummary]:
    root = _problems_dir()
    if not root.is_dir():
        return []

    problems: list[ProblemSummary] = []
    for path in sorted(root.glob("*.*")):
        if path.suffix not in {".json", ".yaml", ".yml"}:
            continue
        try:
            data = _load_problem_file(path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("problem_load_failed", path=str(path), error=str(exc))
            continue

        topics = list(data.get("topics", []))
        company_tags = list(data.get("company_tags", []))
        diff = str(data.get("difficulty", "easy"))

        if topic and topic.lower() not in [t.lower() for t in topics]:
            continue
        if difficulty and difficulty.lower() != diff.lower():
            continue
        if company and company.lower() not in [c.lower() for c in company_tags]:
            continue

        problems.append(
            ProblemSummary(
                slug=str(data.get("slug", path.stem)),
                title=str(data.get("title", path.stem)),
                difficulty=diff,
                topics=topics,
                company_tags=company_tags,
            )
        )
    return problems


def get_problem(slug: str, include_editorial: bool = True) -> ProblemDetail | None:
    root = _problems_dir()
    for path in root.glob("*.*"):
        if path.suffix not in {".json", ".yaml", ".yml"}:
            continue
        data = _load_problem_file(path)
        if str(data.get("slug", path.stem)) != slug:
            continue

        examples = [
            ProblemExample(
                input=str(ex.get("input", "")),
                output=str(ex.get("output", "")),
                explanation=ex.get("explanation"),
            )
            for ex in data.get("examples", [])
        ]

        return ProblemDetail(
            slug=slug,
            title=str(data.get("title", slug)),
            difficulty=str(data.get("difficulty", "easy")),
            topics=list(data.get("topics", [])),
            company_tags=list(data.get("company_tags", [])),
            statement=str(data.get("statement", "")),
            constraints=list(data.get("constraints", [])),
            examples=examples,
            starter_code=str(data.get("starter_code", "")),
            hints=list(data.get("hints", [])),
            editorial=str(data.get("editorial", "")) if include_editorial else None,
            approaches=list(data.get("approaches", [])),
        )
    return None


def get_problem_raw(slug: str) -> dict[str, Any] | None:
    """Return full problem dict including hidden tests (for submit harness)."""
    root = _problems_dir()
    for path in root.glob("*.*"):
        if path.suffix not in {".json", ".yaml", ".yml"}:
            continue
        data = _load_problem_file(path)
        if str(data.get("slug", path.stem)) == slug:
            return data
    return None


def search(query: str, limit: int = 20) -> list[SearchHit]:
    q = query.strip().lower()
    if not q:
        return []

    tokens = [t for t in re.split(r"\s+", q) if t]
    hits: list[SearchHit] = []

    def score_text(*parts: str) -> float:
        blob = " ".join(parts).lower()
        score = 0.0
        for token in tokens:
            if token in blob:
                score += 1.0
                if any(p.lower().startswith(token) for p in parts if p):
                    score += 0.5
        return score

    for course in list_courses():
        s = score_text(course.title, course.summary, " ".join(course.tags))
        if s > 0:
            hits.append(
                SearchHit(
                    type="course",
                    slug=course.slug,
                    title=course.title,
                    summary=course.summary,
                    difficulty=course.difficulty,
                    score=s,
                )
            )

    for course, module, path in _iter_lesson_files():
        lesson = _parse_lesson(path, course, module)
        s = score_text(lesson.title, lesson.summary, " ".join(lesson.tags), module)
        if s > 0:
            hits.append(
                SearchHit(
                    type="lesson",
                    slug=lesson.slug,
                    title=lesson.title,
                    summary=lesson.summary,
                    course=course,
                    difficulty=lesson.difficulty,
                    score=s,
                )
            )

    for problem in list_problems():
        s = score_text(
            problem.title,
            " ".join(problem.topics),
            " ".join(problem.company_tags),
        )
        if s > 0:
            hits.append(
                SearchHit(
                    type="problem",
                    slug=problem.slug,
                    title=problem.title,
                    summary=", ".join(problem.topics),
                    difficulty=problem.difficulty,
                    score=s,
                )
            )

    hits.sort(key=lambda h: (-h.score, h.title))
    return hits[:limit]


@lru_cache
def warm_content_cache() -> int:
    """Touch content once at startup; returns lesson count."""
    return len(_iter_lesson_files())
