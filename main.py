import asyncio
from fastapi import FastAPI, HTTPException, Request, Depends, WebSocket, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from yandex_music import Client
from dotenv import load_dotenv
from functools import lru_cache
from aiocache import cached

import requests
import json
import os
import sqlalchemy

from services.rooms_services import RoomsServices
from services.users_services import UserServices
from services.tokens_services import TokenServices

from models.Users import Users
from models.Rooms import Rooms

from db.base import Database
from wbs.websocket_manager import ConnectionManager
from wbs.websocket_routes import WebSocketRoutes
# from db.base import Database


load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cradle-viewpicture-carl-lady.trycloudflare.com"],  # Или конкретный домен, например ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = Database()
manager = ConnectionManager(db)
templates = Jinja2Templates(directory="templates")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
# REDIRECT_URI = "http://localhost:8000/callback"
REDIRECT_URI = "https://fjxp38df-8000.euw.devtunnels.ms/callback"
# DOMAIN = "developmental-educators-allergy-civilization.trycloudflare.com"
# client = Client(OAUTH_TOKEN).init()
DOMAIN = "localhost"
YANDEX_API = "https://api.music.yandex.net"
# Инициализация клиента Яндекс.Музыки
# client = Client(OAUTH_TOKEN).init()

ws_routes = WebSocketRoutes(manager)


@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await ws_routes.handle_websocket(websocket, room_id, user_id)


@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "media-src 'self' https://*.trycloudflare.com http://localhost:8000 "
        "https://bottle-deaths-guestbook-kernel.trycloudflare.com; "
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws://* wss://*"
    )
    return response


@app.get("/", response_class=HTMLResponse)
async def player_page(request: Request):
    cookies = request.cookies
    print(cookies)
    return templates.TemplateResponse("player.html", {"request": request})


@app.get("/join-room")
async def join_room(room_id: str, request: Request):
    return RedirectResponse(f"/room/{room_id}")


@app.websocket("/room/{room_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str
):
    print(room_id, user_id)
    # print('hui rez')
    if not user_id:
        await websocket.close(code=4001, reason="User ID cookie required")
        return
    
    await ws_routes.handle_websocket(websocket, room_id, user_id)

@app.get("/room/{room_id}", response_class=HTMLResponse)
async def get_room_page(request: Request, room_id: str):
    # Проверяем существование комнаты
    async with db.session_factory() as session:

        room = await session.get(Rooms, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
    cookies = request.cookies
    # print(f'Cookie in room: {cookies}')
    return templates.TemplateResponse("room.html", {
        "request": request,
        "room_id": room_id
    })



@app.get("/get_cookie")
async def get_cookie(request: Request):
    try:
        cookies = request.cookies
        # print(f'after join: {cookies}')
        return Response(
        content=json.dumps(cookies),
        status_code=200
    )
    except Exception as e:
        return Response(
        content=json.dumps({'error': str(e)}),
        status_code=500
    )

# @app.get("/check_token")
# async def check_token(token: str, request: Request):
#     return Response(
#         content=json.dumps({'token': token, 'ok': True, "status": "authenticated", "success": True}),
#         status_code=200)
@app.get("/check_token")
async def check_token(code: str, db: Database = Depends(Database)):
    try:
        # 1. Проверяем токен в БД
        user_services = UserServices(db)
        token = await get_access_token(code)
        print('TOKEN:', token)
        existing_user = await user_services.check_yandex_token(token)
        print(existing_user)
        if existing_user:
            print("SEND success")
            response_data = {
                "status": "authenticated",
                "user_id": str(existing_user.id),
                "username": existing_user.username,
                "action": "login",
                "success": True,
            }
            return JSONResponse(
                content=response_data,
                headers={
                    "Access-Control-Allow-Origin": "https://cradle-viewpicture-carl-lady.trycloudflare.com",  # или "*" (но не с credentials)
                }
            )

        try:
            profile = await user_services.get_yandex_profile(token)
            login = profile.get("login")
            email = profile.get("default_email", "None")
            birthday = profile.get("birthday", "None")
            # Проверки на пустые поля
            email = email if email else None
            login = login if login else None
            birthday = birthday if birthday else None
            if not login:
                raise HTTPException(
                    status_code=400, detail="Не удалось получить логин Яндекса"
                )

            
            new_user = await user_services.create_new_user(
                email=email,
                hashed_password='12345',
                username=login,
                birthday=birthday,
                yandex_token=token,
                rooms_list=[],
            )

            return JSONResponse(
                {
                    "status": "registered",
                    "user_id": str(new_user['user_id']),
                    "username": login,
                    "action": "register",
                    "success": True,
                }
            )
        except Exception as e:
            print(str(e))

        # except UnauthorizedError as e:
        #     logger.error(f"Ошибка авторизации Яндекс: {str(e)}")
        #     raise HTTPException(
        #         status_code=401, detail=f"Неверный токен Яндекс.Музыки: {str(e)}"
        #     )
        # except NetworkError as e:
        #     logger.error(f"Ошибка сети Яндекс API: {str(e)}")
        #     raise HTTPException(
        #         status_code=503, detail="Сервис Яндекс.Музыки временно недоступен"
        #     )
        # except Exception as e:
        #     logger.error(f"Ошибка Яндекс API: {str(e)}")
        #     raise HTTPException(
        #         status_code=400, detail=f"Ошибка при работе с Яндекс API: {str(e)}"
        #     )

    except HTTPException:
        raise  # Пробрасываем уже обработанные ошибки
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/auth/current-user")
async def get_current_user(user_id: str = Cookie(None)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    async with db.session_factory() as session:
        user = await session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "username": user.username
        }


async def get_access_token(code: str):
    """
    Обмен кода авторизации на токен доступа.
    """
    token_url = "https://oauth.yandex.ru/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Ошибка при получении токена")
    print(response.json())
    return response.json().get("access_token")


@app.post("/create_room")
async def create_room(request: Request, name_rooms: str = None, db: Database = Depends(Database)):
    if not(name_rooms):
        return Response(
        content=json.dumps({'Status': 'Error', 'Message': 'Введите название комнаты'}),
        status_code=500
    )
    cookies = request.cookies
    # print(cookies)
    if 'user_id' not in cookies and not(cookies['user_id']):
        # print(1)
        return Response(
        content=json.dumps({'Status': 'Error', 'Message': 'Авторизуйтесь'}),
        status_code=500
    )
    resp = RoomsServices(db)
    user_model = UserServices(db)
    # print(name_rooms)
    try:
        done = await resp.create_room(name_rooms, cookies['user_id'])
        op = await user_model.add_room(str(done['id']), cookies['user_id'])
        # print(type(done))
    except sqlalchemy.exc.IntegrityError as e:
        return Response(
        content=json.dumps({'Status': 'Error', 'Message': str(e)}),
        status_code=500
    )
    done = await resp.get_all()
    # print(done)
    return Response(
        content=json.dumps(done),
        status_code=200
    )


@app.get('/auth/sign-in')
async def auth_login(request: Request, response: Response, nickname: str, hashed_password: str, db: Database = Depends(Database)):
    try:
        # obj = await request.json()
        obj = {'nickname': nickname,
               'hashed_password': hashed_password}

        user_model = UserServices(db)

        user = await user_model.logging(obj)

        if user:
            # token = await token_model.new_token(obj=obj, user_id=user.id)
            usr_id = user.id
            response = JSONResponse(
                content=json.dumps({'status': 'Successfully hui', 'user_id': str(usr_id)}),
                status_code=200
            )
            response.set_cookie(
                key="user_id",
                value=str(usr_id),
                httponly=True,
                secure=False,
                samesite="lax",
                domain=DOMAIN,  # Явное указание домена
                path="/"
            )
            return response
        return {'status': 'error', 'message': 'Неправильный логин или пароль'}
    except Exception as e:
        print(e)
        return {'message': str(e)}
    

@app.get("/callback")
async def callback(code: str, access_token: str):
    # print(f'code: {code}')
    """
    Обработка перенаправления от Yandex и получение токена доступа.
    """
    # global access_token
    # access_token = await get_access_token(code)
    print('access_token', access_token)
    return {"message": "Авторизация успешна", "access_token": access_token}


@app.get("/track_info")
async def get_track_info(url: str, user_id: str, request: Request):
    try:
        user_model = UserServices(db)
        
        yan_tok = await user_model.get_yandex_token_by_user_id(user_id=user_id)
        print(yan_tok)
        client = Client(yan_tok).init()
        
        # track_id = url.split('track/')[1].split('/')[0]
        track_id = '138186678'
        
        track = client.tracks(track_id)[0]
        print('url:', url, 'user:', user_id, 'track_id:', track_id)
        return {
            "title": track.title,
            "artist": track.artists[0].name,
            "cover": f"https://{track.cover_uri.replace('%%', '400x400')}"
        }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

@cached(ttl=60)
async def get_cached_track_info(track_id: str, user_id: str):
    user_model = UserServices(db)
    yan_tok = await user_model.get_yandex_token_by_user_id(user_id=user_id)
    client = Client(OAUTH_TOKEN).init()
    return client.tracks(track_id)[0]
    

@app.get("/track_and_stream")
async def track_and_stream(url: str, user_id: str):
    try:
        clean_url = url.split('?')[0]
        track_id = clean_url.split('track/')[1].split('/')[0]
        
        track = await get_cached_track_info(track_id, user_id)
        download_info = track.get_download_info(get_direct_links=True)[0]
        stream_url = download_info.get_direct_link()
        
        track_info = {
            "title": track.title,
            "artist": track.artists[0].name,
            "cover": f"https://{track.cover_uri.replace('%%', '400x400')}",
            "stream_url": f"/stream?url={url}&user_id={user_id}"
        }
        
        return JSONResponse(track_info)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))


# @app.get("/stream")
# async def stream_audio(url: str,request: Request, user_id: str):
#     try:
#         # # Удаляем лишние параметры из URL
#         # print(f'TOKEN: {OAUTH_TOKEN}')
#         # x = await request.json()
#         # print(x)
#         # user_id = request.cookies['user_id']
#         user_model = UserServices(db)
#         print('IDDDDDDDDDDDDDDDDDD', user_id)
#         yan_tok = await user_model.get_yandex_token_by_user_id(user_id=user_id)
#         # print(f'Token from bd: {yan_tok}')
        
#         client = Client(OAUTH_TOKEN).init()
        
#         clean_url = url.split('?')[0]
#         track_id = clean_url.split('track/')[1].split('/')[0]
        
#         # Получаем трек
#         track = client.tracks(track_id)[0]
#         download_info = track.get_download_info(get_direct_links=True)[0]
        
#         stream_url = download_info.get_direct_link()
#         print('stream_url:', stream_url)
#         # Проверяем ссылку
#         test_request = requests.head(stream_url)
#         if test_request.status_code != 200:
#             return {"error": "Не удалось получить аудиопоток"}
#         response = requests.get(stream_url)
#         print(f'{user_id} - {yan_tok}')
#         # Потоковая передача
#         def generate():
#             with requests.get(stream_url, stream=True) as r:
#                 for chunk in r.iter_content(chunk_size=1024*16):  # Увеличенный буфер
#                     if chunk:
#                         yield chunk
#                         del chunk
#         track_info = {
#             "title": track.title,
#             "artist": track.artists[0].name,
#             "cover": f"https://{track.cover_uri.replace('%%', '400x400')}"
#         }
#         return StreamingResponse(
#             generate(),
#             media_type="audio/mpeg",
#             headers={
#                 "Content-Security-Policy": "media-src 'self' https://*.trycloudflare.com https://localhost:8000",
#                 "Access-Control-Expose-Headers": "Track-Info",
#                 "Track-Info": json.dumps(track_info),
#                 "Accept-Ranges": "bytes",
#                 "Content-Length": str(len(response.content)),  # Важно указать размер
#                 "Content-Type": "audio/mpeg"
#             }
#         )
        
#     except Exception as e:
#         print(e)
#         return {"error": str(e)}
        
#     except Exception as e:
#         return {"error": str(e)}
@app.get("/stream")
async def stream_audio(url: str, request: Request, user_id: str):
    try:
        # Быстрая проверка URL
        if 'track/' not in url:
            raise HTTPException(status_code=400, detail="Invalid track URL")
            
        clean_url = url.split('?')[0]
        track_id = clean_url.split('track/')[1].split('/')[0]
        
        # Получаем трек из кэша или API
        track = await get_cached_track_info(track_id, user_id)
        download_info = track.get_download_info(get_direct_links=True)[0]
        stream_url = download_info.get_direct_link()
        
        # Проверка доступности потока через HEAD запрос
        test_request = requests.head(stream_url, timeout=5)
        response = requests.get(stream_url)
        if test_request.status_code != 200:
            raise HTTPException(status_code=502, detail="Audio stream unavailable")
        
        # Генератор потока с буферизацией
        async def generate():
            with requests.get(stream_url, stream=True, timeout=10) as r:
                for chunk in r.iter_content(chunk_size=32*1024):  # Увеличенный буфер
                    if chunk:
                        yield chunk
        
        track_info = {
            "title": track.title,
            "artist": track.artists[0].name,
            "cover": f"https://{track.cover_uri.replace('%%', '400x400')}"
        }
        
        return StreamingResponse(
            generate(),
            media_type="audio/mpeg",
            headers={
                "Content-Security-Policy": "media-src 'self' https://*.trycloudflare.com https://localhost:8000",
                "Access-Control-Expose-Headers": "Track-Info",
                "Accept-Ranges": "bytes",
                "Track-Info": json.dumps(track_info),
                "Content-Type": "audio/mpeg",
                "Content-Length": str(len(response.content)),
                "Cache-Control": "public, max-age=3600"  # Кэширование на 1 час
            }
        )
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Stream timeout")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        port=444,
        reload=True,      # Автоперезагрузка при изменениях
    )
