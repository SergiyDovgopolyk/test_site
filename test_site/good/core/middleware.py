from fastapi import Request, Response, HTTPException
from fastapi.responses import RedirectResponse

from test_site.good.routers.routers import templates

CANONICAL_URL = "http://127.0.0.1:8000/"

async def redirect_to_canonical_good(request: Request, call_next):
    full_url = str(request.url)
    if (
        full_url.startswith("http://127.0.0.1:8000//")
        or "www." in full_url
        or request.url.path in [
            "/index.php", "/home.php", "/index.html", "/home.html", "/index.htm", "/home.htm", "/home"
        ]
    ):
        return RedirectResponse(CANONICAL_URL, status_code=301)
    return await call_next(request)


# Возвращаем 404 для несуществующих страниц
async def error_404_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "og_title": "Page 404 - Not Found",
            "og_description": "The page you are looking for does not exist.",
            "og_image": "/static/images/404_image.avif",
            "canonical_url": None,
        }, status_code=404)
    return exc