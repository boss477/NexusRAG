import logging
import socket
import uuid

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings
from app.logging_config import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)
app = FastAPI(title=settings.app_name, version="0.1.0")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "%s %s -> %s",
            request.method,
            request.url.path,
            response.status_code,
            extra={"request_id": request_id},
        )
        return response


app.add_middleware(RequestContextMiddleware)


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {"name": settings.app_name, "status": "running"}


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready", tags=["system"])
async def readiness() -> dict[str, object]:
    """Report whether required infrastructure endpoints are configured and resolvable."""
    checks = {
        "qdrant": _host_is_resolvable(settings.qdrant_url),
        "redis": _host_is_resolvable(settings.redis_url),
    }
    ready = all(checks.values())
    return {"status": "ready" if ready else "not_ready", "checks": checks}


def _host_is_resolvable(url: str) -> bool:
    host = url.split("://", 1)[-1].split("/", 1)[0].split(":", 1)[0]
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return False
    return True

