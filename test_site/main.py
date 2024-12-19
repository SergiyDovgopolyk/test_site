from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from good.routers.routers import router as first_app_router
from bad.routers.routers import router as second_app_router
from fastapi.templating import Jinja2Templates
import uvicorn
import os

# Общие настройки
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Инициализация шаблонов
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def create_app(title, description, version, router):
    app = FastAPI(title=title, description=description, version=version)
    app.include_router(router)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return app


# Создаем приложения
first_app = create_app(
    title="First Application",
    description="This is the first FastAPI application",
    version="1.0.0",
    router=first_app_router,
)

second_app = create_app(
    title="Second Application",
    description="This is the second FastAPI application",
    version="1.0.0",
    router=second_app_router,
)


if __name__ == "__main__":
    import multiprocessing

    def run_first_app():
        uvicorn.run(first_app, host="0.0.0.0", port=8000)

    def run_second_app():
        uvicorn.run(second_app, host="0.0.0.0", port=7000)

    p1 = multiprocessing.Process(target=run_first_app)
    p2 = multiprocessing.Process(target=run_second_app)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
