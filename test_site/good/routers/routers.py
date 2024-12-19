import os

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from good.services.article_service import get_articles
from good.services.hreflang_service import generate_hreflangs


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)



@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    og_title = "Main Page - News Portal"
    og_description = "Latest news and articles from various categories."
    og_image = "/static/images/default_image.webp"
    articles = get_articles(limit=10)
    canonical_url = "/"

    return templates.TemplateResponse("home.html", {
        "request": request,
        "articles": articles[:10],
        "canonical_url": canonical_url,
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image,  # Используем строку напрямую
        "og_image_alt": "Default alt description",  # Устанавливаем alt напрямую
        "hreflangs": generate_hreflangs("/")
    })


@router.get("/category/{category_name}", response_class=HTMLResponse)
async def category(request: Request, category_name: str):
    articles = get_articles(limit=10)
    filtered_articles = [a for a in articles if a["category"].lower() == category_name.lower()]
    canonical_url = f"/category/{category_name}"

    return templates.TemplateResponse("category.html", {
        "request": request,
        "category": category_name,
        "articles": filtered_articles,
        "canonical_url": canonical_url,
        "hreflangs": generate_hreflangs(f"/category/{category_name}"),
        "page_title": f"Category: {category_name}",
        "page_description": f"Explore the latest articles in the {category_name} category."
    })


@router.get("/category/{category_name}/article/{article_id}", response_class=HTMLResponse)
async def get_article(request: Request, category_name: str, article_id: int):
    try:
        articles = get_articles(limit=10)
    except Exception as e:
        articles = []
    article = next((a for a in articles if a["id"] == article_id and a["category"].lower() == category_name.lower()), None)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Основные данные статьи
    og_title = article.get("title", "Article Title not found")
    og_description = article.get("description", "Article description not found")
    og_image = article.get("image", "/static/images/default_image.webp")
    canonical_url = f"/category/{category_name}/article/{article_id}"
    date_published = article.get("date_published")
    author_name = article.get("author_name", "No author specified")

    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": article,
        "category_name": category_name,
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image if isinstance(og_image, str) else og_image.get("url"),
        "og_image_alt": "Default alt description" if isinstance(og_image, str) else og_image.get("alt",
                                                                                                 "Default alt description"),
        "canonical_url": canonical_url,
        "date": date_published,
        "author_name": author_name,
        "hreflangs": generate_hreflangs(f"/category/{category_name}/article/{article_id}")
    })

@router.get("/about-us", response_class=HTMLResponse)
async def about_us(request: Request):
    og_title = "About Us - News Portal"
    og_description = "Learn more about our team and mission."
    canonical_url = f"/about-us"

    return templates.TemplateResponse("about_us.html", {
        "request": request,
        "og_title": og_title,
        "og_description": og_description,
        "hreflangs": generate_hreflangs("/about-us"),
        "canonical_url": canonical_url
    })


@router.get("/contacts", response_class=HTMLResponse)
async def contact(request: Request):
    og_title = "Contact Us - News Portal"
    og_description = "Get in touch with us for inquiries and support."
    canonical_url = f"/contacts"

    return templates.TemplateResponse("contact.html", {
        "request": request,
        "og_title": og_title,
        "og_description": og_description,
        "hreflangs": generate_hreflangs("/contacts"),
        "canonical_url": canonical_url
    })


@router.get("/robots.txt")
async def get_robots_txt():
    file_path = os.path.join(os.getcwd(), "static", "robots.txt")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/sitemap.xml")
async def get_sitemap():
    file_path = os.path.join(os.getcwd(), "static", "sitemap.xml")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")