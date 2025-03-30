# from fastapi import FastAPI, HTTPException
# from fastapi.responses import StreamingResponse
# from yandex_music import Client
# import requests

# app = FastAPI()
# client = Client('ваш_oauth_токен').init()

# @app.get("/stream/{track_id}")
# async def stream_audio(track_id: str):
#     try:
#         track = client.tracks(track_id)[0]
#         download_info = track.get_download_info()[0]
#         stream_url = download_info.get_direct_link()
        
#         # Потоковая передача аудио
#         audio_stream = requests.get(stream_url, stream=True)
        
#         return StreamingResponse(
#             audio_stream.iter_content(chunk_size=1024),
#             media_type="audio/mpeg"
#         )
        
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from yandex_music import Client
from dotenv import load_dotenv
import requests
import json
import os


load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
# Инициализация клиента Яндекс.Музыки
client = Client(OAUTH_TOKEN).init()

@app.get("/", response_class=HTMLResponse)
async def player_page(request: Request):
    return templates.TemplateResponse("player.html", {"request": request})

@app.get("/stream")
async def stream_audio(url: str):
    try:
        # Удаляем лишние параметры из URL
        clean_url = url.split('?')[0]
        track_id = clean_url.split('track/')[1].split('/')[0]
        
        # Получаем трек
        track = client.tracks(track_id)[0]
        download_info = track.get_download_info(get_direct_links=True)[0]
        stream_url = download_info.get_direct_link()
        
        # Проверяем ссылку
        test_request = requests.head(stream_url)
        if test_request.status_code != 200:
            return {"error": "Не удалось получить аудиопоток"}
        response = requests.get(stream_url)
        
        # Потоковая передача
        def generate():
            with requests.get(stream_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=1024*16):  # Увеличенный буфер
                    yield chunk
                    
        return StreamingResponse(
            generate(),
            media_type="audio/mpeg",
            headers={
                "Track-Info": json.dumps({
                    "title": track.title,
                    "artist": track.artists[0].name,
                    "cover": f"https://{track.cover_uri.replace('%%', '400x400')}"
                }),
                "Accept-Ranges": "bytes",
                "Content-Length": str(len(response.content))  # Важно указать размер
            }
        )
        
    except Exception as e:
        return {"error": str(e)}
# @app.get("/stream")
# async def stream_audio(url: str):
#     try:
#         clean_url = url.split('?')[0]
#         track_id = clean_url.split('track/')[1].split('/')[0]
        
#         track = client.tracks(track_id)[0]
#         download_info = track.get_download_info(get_direct_links=True)[0]
#         stream_url = download_info.get_direct_link()
        
#         # Загружаем весь трек за один запрос
#         response = requests.get(stream_url)
#         if response.status_code != 200:
#             return {"error": "Не удалось получить аудиопоток"}
        
#         audio_data = response.content
        
#         # Формируем заголовки
#         headers = {
#             "Track-Info": json.dumps({
#                 "title": track.title,
#                 "artist": track.artists[0].name,
#                 "cover": f"https://{track.cover_uri.replace('%%', '400x400')}"
#             }),
#             "Content-Length": str(len(audio_data))  # Важно указать размер
#         }
        
#         # Отправляем полный файл
#         return Response(
#             content=audio_data,
#             media_type="audio/mpeg",
#             headers=headers
#         )
        
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        port=8001,
        reload=True,      # Автоперезагрузка при изменениях
    )
