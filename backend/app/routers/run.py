from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings
from app.models.schemas import RunRequest, RunResponse, SubmitRequest, SubmitResponse
from app.services import runner

router = APIRouter(prefix="/api", tags=["execution"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/run", response_model=RunResponse)
@limiter.limit("30/minute")
def run_code(request: Request, body: RunRequest) -> RunResponse:
    settings = get_settings()
    if len(body.code.encode("utf-8")) > settings.max_request_size_bytes:
        return RunResponse(
            stderr="Code exceeds maximum allowed size.",
            exit_code=1,
        )
    return runner.run_code(body)


@router.post("/submit", response_model=SubmitResponse)
@limiter.limit("30/minute")
def submit_code(request: Request, body: SubmitRequest) -> SubmitResponse:
    settings = get_settings()
    if len(body.code.encode("utf-8")) > settings.max_request_size_bytes:
        return SubmitResponse(
            passed=False,
            results=[],
            total=0,
            passed_count=0,
        )
    return runner.submit_code(body)
