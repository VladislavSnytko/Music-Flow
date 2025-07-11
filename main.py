import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import (HTMLResponse)
from dotenv import load_dotenv

# Импорт роутеров
from routes import auth, rooms, tracks, websocket

load_dotenv()

app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost", "http://localhost", os.getenv("DOMAIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(tracks.router)
app.include_router(websocket.router)

# Инициализация шаблонов
templates = Jinja2Templates(directory="templates")

# Middleware для CSP
@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "media-src 'self' https://*.trycloudflare.com http://localhost:8000 "
        "https://fs-ag-cage-hold.trycloudflare.com; "
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws://* wss://*"
    )
    return response

<<<<<<< HEAD
# Базовый эндпоинт
@app.get("/", response_class=HTMLResponse)
async def player_page(request: Request):
    cookies = request.cookies
    print(cookies)
    return templates.TemplateResponse("player.html", {"request": request})
=======

@app.get("/", response_class=JSONResponse)
async def player_page():
    # cookies = request.cookies
    # print(cookies)
    return {'status': 'worked'}
    # return templates.TemplateResponse("player.html", {"request": request})
>>>>>>> 86ce224c1c09b459b92e4ba057b3c2cb1d942dd5



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=444,
        port=8000,
        reload=True,  # Автоперезагрузка при изменениях
    )