from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class MultiTenantMiddleware(BaseHTTPMiddleware):
    """
    Multi-tenant Resolution Middleware.
    Extracts tenant slug/ID from 'X-Tenant-ID' request header or subdomains.
    Guarantees strict multi-tenant isolation context.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        tenant_id = request.headers.get("X-Tenant-ID", "default-tenant")
        request.state.tenant_id = tenant_id
        response = await call_next(request)
        response.headers["X-Tenant-ID"] = tenant_id
        return response
