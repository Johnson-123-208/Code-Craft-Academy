"""Pydantic v2 API schemas."""

from typing import Any, Literal

from pydantic import BaseModel, Field


Difficulty = Literal["beginner", "intermediate", "advanced", "easy", "medium", "hard"]


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str = "0.1.0"


class LessonSummary(BaseModel):
    slug: str
    title: str
    summary: str
    duration: int = Field(description="Estimated minutes")
    difficulty: str
    order: int
    tags: list[str] = []
    module: str
    course: str


class LessonDetail(LessonSummary):
    prerequisites: list[str] = []
    content: str
    previous_slug: str | None = None
    next_slug: str | None = None


class ModuleSummary(BaseModel):
    slug: str
    title: str
    order: int
    lessons: list[LessonSummary]


class CourseSummary(BaseModel):
    slug: str
    title: str
    summary: str
    category: str
    difficulty: str
    duration_hours: float
    lesson_count: int
    tags: list[str] = []
    thumbnail: str | None = None


class CourseDetail(CourseSummary):
    prerequisites: list[str] = []
    learning_outcomes: list[str] = []
    modules: list[ModuleSummary]
    description: str


class ProblemSummary(BaseModel):
    slug: str
    title: str
    difficulty: str
    topics: list[str] = []
    company_tags: list[str] = []


class ProblemExample(BaseModel):
    input: str
    output: str
    explanation: str | None = None


class ProblemDetail(ProblemSummary):
    statement: str
    constraints: list[str] = []
    examples: list[ProblemExample] = []
    starter_code: str
    hints: list[str] = []
    # Solutions and hidden tests are never exposed in list/detail for submit flow;
    # editorial is available after the client opts in via a separate flag in Phase 2+.
    editorial: str | None = None
    approaches: list[dict[str, Any]] = []


class RunRequest(BaseModel):
    code: str = Field(..., max_length=100_000)
    stdin: str = ""
    language: Literal["python"] = "python"


class RunResponse(BaseModel):
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    timed_out: bool = False
    execution_time_ms: float = 0
    images: list[str] = Field(
        default_factory=list,
        description="Base64-encoded plot images when matplotlib is used",
    )
    truncated: bool = False


class SubmitRequest(BaseModel):
    problem_slug: str
    code: str = Field(..., max_length=100_000)
    language: Literal["python"] = "python"


class TestResult(BaseModel):
    name: str
    passed: bool
    visible: bool = True
    runtime_ms: float = 0
    expected: str | None = None
    actual: str | None = None
    error: str | None = None


class SubmitResponse(BaseModel):
    passed: bool
    results: list[TestResult]
    total: int
    passed_count: int


class SearchHit(BaseModel):
    type: Literal["lesson", "problem", "course"]
    slug: str
    title: str
    summary: str
    course: str | None = None
    difficulty: str | None = None
    score: float = 0


class SearchResponse(BaseModel):
    query: str
    total: int
    hits: list[SearchHit]
