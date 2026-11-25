from fastapi import APIRouter, Query

from app.models.schemas import SearchResponse
from app.services import content

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, max_length=200),
    limit: int = Query(default=20, ge=1, le=50),
) -> SearchResponse:
    hits = content.search(q, limit=limit)
    return SearchResponse(query=q, total=len(hits), hits=hits)
