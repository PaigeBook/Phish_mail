import logging
import time
from collections.abc import Callable

from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """Log request/response with timing and request context.

    Args:
        request: FastAPI request object
        call_next: Next middleware/handler callable

    Returns:
        Response object with logging side effects
    """
    start_time = time.time()
    request_id = request.headers.get("X-Request-ID", "unknown")

    logger.info(
        f"[{request_id}] {request.method} {request.url.path} - START",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        message = (
            f"[{request_id}] {request.method} {request.url.path} - "
            f"{response.status_code} ({duration:.2f}s)"
        )
        logger.info(
            message,
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration": duration,
            },
        )
        return response
    except RuntimeError:
        duration = time.time() - start_time
        logger.error(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"RuntimeError after {duration:.2f}s",
            extra={"request_id": request_id, "duration": duration},
            exc_info=True,
        )
        raise
    except Exception:
        duration = time.time() - start_time
        logger.error(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Unexpected error after {duration:.2f}s",
            extra={"request_id": request_id, "duration": duration},
            exc_info=True,
        )
        raise
