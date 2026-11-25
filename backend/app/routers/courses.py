from fastapi import APIRouter, HTTPException

from app.models.schemas import CourseDetail, CourseSummary
from app.services import content

router = APIRouter(prefix="/api", tags=["courses"])


@router.get("/courses", response_model=list[CourseSummary])
def list_courses() -> list[CourseSummary]:
    return content.list_courses()


@router.get("/courses/{slug}", response_model=CourseDetail)
def get_course(slug: str) -> CourseDetail:
    course = content.get_course(slug)
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course not found: {slug}")
    return course
