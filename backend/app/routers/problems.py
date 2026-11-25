from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import ProblemDetail, ProblemSummary
from app.services import content

router = APIRouter(prefix="/api", tags=["problems"])


@router.get("/problems", response_model=list[ProblemSummary])
def list_problems(
    topic: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    company: str | None = Query(default=None),
) -> list[ProblemSummary]:
    return content.list_problems(topic=topic, difficulty=difficulty, company=company)


@router.get("/problems/{slug}", response_model=ProblemDetail)
def get_problem(slug: str) -> ProblemDetail:
    problem = content.get_problem(slug)
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Problem not found: {slug}")
    return problem
