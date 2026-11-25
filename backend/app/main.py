"""CodeCraft Academy FastAPI application."""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.logging_config import configure_logging
from app.routers import courses, health, lessons, problems, run, search
from app.services import content

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    configure_logging(settings.environment)
    count = content.warm_content_cache()
    logger.info(
        "startup",
        environment=settings.environment,
        content_dir=str(settings.content_path),
        lesson_files=count,
    )
    yield
    logger.info("shutdown")


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="CodeCraft Academy API",
        description="Learning platform API for courses, lessons, problems, and code execution.",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.state.limiter = run.limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_middleware(SlowAPIMiddleware)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(courses.router)
    application.include_router(lessons.router)
    application.include_router(problems.router)
    application.include_router(run.router)
    application.include_router(search.router)

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_error", path=str(request.url.path), error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return application


app = create_app()
