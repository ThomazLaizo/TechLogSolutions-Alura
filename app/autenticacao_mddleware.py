from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationToken(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_path = request.url.path
        rotas_publicas = ("/login", "/registro", "/static")

        if request_path.startswith(rotas_publicas):
            return await call_next(request)
        
        token = request.cookies.get("session_token")

        if token != "token-senha":
            return RedirectResponse(url = "/login", status_code = 303)

        return await call_next(request)