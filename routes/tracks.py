import json
import os
import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import (JSONResponse, StreamingResponse)
from yandex_music import Client
from aiocache import cached
from services.users_services import UserServices
from db.base import Database
from dotenv import load_dotenv


db = Database()
load_dotenv()
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")

router = APIRouter(prefix="/tracks")


@cached(ttl=60)
async def get_cached_track_info(track_id: str, user_id: str):
    user_model = UserServices(db)
    yan_tok = await user_model.get_yandex_token_by_user_id(user_id=user_id)
    client = Client(OAUTH_TOKEN).init()
    return client.tracks(track_id)[0]


@router.get("/track_info")
async def get_track_info(url: str, user_id: str, request: Request):
    try:
        user_model = UserServices(db)

        yan_tok = await user_model.get_yandex_token_by_user_id(user_id=user_id)
        print(yan_tok)
        client = Client(yan_tok).init()
        
        track_id = url.split('track/')[1].split('/')[0] if 'track/' in url else url
        track = client.tracks(track_id)[0]

        print("url:", url, "user:", user_id, "track_id:", track_id)
        return {
            "title": track.title,
            "artist": ", ".join(artist.name for artist in track.artists),
            "cover": f"https://{track.cover_uri.replace('%%', '400x400')}",
        }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/track_and_stream")
async def track_and_stream(url: str, user_id: str):
    try:
        clean_url = url.split("?")[0]
        print(f"{url} - {user_id}")
        track_id = clean_url.split("track/")[1].split("/")[0]

        track = await get_cached_track_info(track_id, user_id)
        download_info = track.get_download_info(get_direct_links=True)[0]
        
        stream_url = download_info.get_direct_link()

        track_info = {
            "title": track.title,
            "artist": ", ".join(artist.name for artist in track.artists),
            "cover": f"https://{track.cover_uri.replace('%%', '400x400')}",
            "stream_url": f"/stream?url={url}&user_id={user_id}",
        }

        return JSONResponse(track_info)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/stream")
async def stream_audio(url: str, request: Request, user_id: str):
    try:
        if "music.yandex.ru" not in url or "track/" not in url:
            raise HTTPException(status_code=400, detail="Invalid track URL. Must be a Yandex Music track URL")

        clean_url = url.split("?")[0]
        track_id = clean_url.split("track/")[1].split("/")[0]

        # Получаем метаданные трека
        track = await get_cached_track_info(track_id, user_id)
        download_info = track.get_download_info(get_direct_links=True)[0]
        stream_url = download_info.get_direct_link()

        # Определяем MIME-тип по кодека
        mime_type = {
            "mp3": "audio/mpeg",
            "aac": "audio/aac",
            "flac": "audio/flac",
        }.get(download_info.codec, "audio/mpeg")

        # Получаем длительность трека в секундах
        duration_sec = track.duration_ms / 1000 if track.duration_ms else None

        # Получаем Content-Length (если возможно)
        content_length = None
        async with httpx.AsyncClient() as client:
            try:
                head_response = await client.head(stream_url, follow_redirects=True)
                content_length = head_response.headers.get("content-length")
            except Exception as e:
                print(f"Error getting content length: {e}")

        # Если не удалось получить Content-Length, используем примерный расчет
        if not content_length and duration_sec:
            # Примерный расчет для MP3 ~128kbps
            content_length = str(int(duration_sec * 16000))  # 16KB/сек

        track_info = {
            "title": track.title,
            "artist": ", ".join(artist.name for artist in track.artists),
            "cover": f"https://{track.cover_uri.replace('%%', '400x400')}",
            "duration": duration_sec,
        }

        # Основные заголовки для предотвращения скачивания
        response_headers = {
            "Content-Type": mime_type,
            "Content-Disposition": "inline",  # Предотвращает скачивание
            "X-Content-Type-Options": "nosniff",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "Track-Info, Content-Duration",
            "Track-Info": json.dumps(track_info),
            "Content-Duration": str(duration_sec) if duration_sec else "0",
            "Cache-Control": "no-cache",  # Для потоковой передачи
            "Accept-Ranges": "bytes",
        }

        # Добавляем Content-Length, если он известен
        if content_length:
            response_headers["Content-Length"] = content_length

        # Асинхронный генератор для потоковой передачи
        async def generate():
            async with httpx.AsyncClient(timeout=None, follow_redirects=True) as client:
                async with client.stream("GET", stream_url) as response:
                    if response.status_code != 200:
                        raise HTTPException(
                            status_code=502,
                            detail=f"Upstream error: {response.status_code}"
                        )
                    
                    # Используем оптимальный размер чанка
                    async for chunk in response.aiter_bytes(chunk_size=320 * 1024):
                        if await request.is_disconnected():
                            break
                        yield chunk

        return StreamingResponse(
            generate(),
            media_type=mime_type,
            headers=response_headers
        )

    except Exception as e:
        print(f"Stream error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")