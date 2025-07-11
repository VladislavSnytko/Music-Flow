import json
import os
import sqlalchemy
from yandex_music import Client
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import (HTMLResponse, RedirectResponse, JSONResponse)
from fastapi.templating import Jinja2Templates
from services.rooms_services import Rooms, RoomsServices
from services.users_services import UserServices
from db.base import Database
from dotenv import load_dotenv


db = Database()
load_dotenv()
templates = Jinja2Templates(directory="templates")


DOMAIN = os.getenv("DOMAIN")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")



router = APIRouter(prefix="/rooms")


@router.get("/{room_id}", response_class=HTMLResponse)
async def get_room_page(request: Request, room_id: str):
    # Проверяем существование комнаты
    async with db.session_factory() as session:

        room = await session.get(Rooms, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
    cookies = request.cookies
    # print(f'Cookie in room: {cookies}')
    return templates.TemplateResponse(
        "room.html", {"request": request, "room_id": room_id}
    )

@router.post("/create")
async def create_room(
    request: Request, name_rooms: str = None, db: Database = Depends(Database)
):
    if not (name_rooms):
        return Response(
            content=json.dumps(
                {"Status": "Error", "Message": "Введите название комнаты"}
            ),
            status_code=500,
        )
    cookies = request.cookies
    # print(cookies)
    if "user_id" not in cookies and not (cookies["user_id"]):
        # print(1)
        return Response(
            content=json.dumps({"Status": "Error", "Message": "Авторизуйтесь"}),
            status_code=500,
        )
    resp = RoomsServices(db)
    user_model = UserServices(db)
    # print(name_rooms)
    try:
        done = await resp.create_room(name_rooms, cookies["user_id"])
        op = await user_model.add_room(str(done["id"]), cookies["user_id"])
        # print(type(done))
    except sqlalchemy.exc.IntegrityError as e:
        return Response(
            content=json.dumps({"Status": "Error", "Message": str(e)}), status_code=500
        )
    done = await resp.get_all()
    # print(done)
    return Response(content=json.dumps(done), status_code=200)

@router.get("/{room_id}/join")
async def join_room(room_id: str, request: Request):
    return RedirectResponse(f"/room/{room_id}")


@router.get("/{room_id}/queue")
async def get_queue_tracks(room_id: str, track_id: str):
    room_model = RoomsServices(db)
    info = await room_model.get_tracks_from_room(room_id)
    tracks = []
    print(info)
    client = Client(OAUTH_TOKEN).init()
    try:
        if track_id:
            
            track = client.tracks(track_id)[0]
            track_info = {
                "title": track.title,
                "artist": ", ".join(artist.name for artist in track.artists),
                "cover": f"https://{track.cover_uri.replace('%%', '50x50')}"
            }
            print(track_info)
            return JSONResponse(content={'new_track': track_info},
                            headers={
                                "Access-Control-Allow-Origin": DOMAIN,
                                "Access-Control-Allow-Credentials": "true",
                            })
        for url in info['list_track']:
            clean_url = url.split("?")[0]
            track_id = clean_url.split("track/")[1].split("/")[0]
            print('type:', type(track_id))
            # track = await get_cached_track_info(track_id, user_id)
            
            track = client.tracks(track_id)[0]
            # download_info = track.get_download_info(get_direct_links=True)[0]
            # stream_url = download_info.get_direct_link()

            track_info = {
                "title": track.title,
                "artist": ", ".join(artist.name for artist in track.artists),
                "cover": f"https://{track.cover_uri.replace('%%', '50x50')}"
            }
            print(track_info)
            tracks.append(track_info)

        return JSONResponse(content={'list_track': tracks, 'index': info['index']},
                            headers={
                                "Access-Control-Allow-Origin": DOMAIN,
                                "Access-Control-Allow-Credentials": "true",
                            })
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))