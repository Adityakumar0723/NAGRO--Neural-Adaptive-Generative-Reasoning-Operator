"""Authentication middleware for NAGRO 4.1."""

from __future__ import annotations
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from nagro.core.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Optional API key authentication middleware."""

    EXEMPT_PATHS = {"/", "/api/v1/health", "/docs", "/openapi.json"}

    async def dispatch(self, request: Request, call_next):
        if not settings.nagro_api_key:
            return await call_next(request)

        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        if request.url.path.startswith(("/css", "/js", "/assets")):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
        if api_key != settings.nagro_api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")

        return await call_next(request)
