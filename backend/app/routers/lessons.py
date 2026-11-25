from fastapi import APIRouter, HTTPException

from app.models.schemas import LessonDetail
from app.services import content

router = APIRouter(prefix="/api", tags=["lessons"])


@router.get("/lessons/{slug}", response_model=LessonDetail)
def get_lesson(slug: str) -> LessonDetail:
    lesson = content.get_lesson(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {slug}")
    return lesson
