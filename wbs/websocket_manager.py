import asyncio
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy import select
from models.Rooms import Rooms
from db.base import Database

class ConnectionManager:
    def __init__(self, db: Database):
        self.active_connections = {}
        self.db = db

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket
        await self.update_participants(room_id)

    async def disconnect(self, room_id: str, user_id: str):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
            else:
                await self.update_participants(room_id)

    async def broadcast(self, room_id: str, message: dict, exclude_user: str = None):
        if room_id not in self.active_connections:
            return

        to_remove = []
        for user_id, connection in list(self.active_connections[room_id].items()):
            if user_id == exclude_user:
                continue
            try:
                await connection.send_json(message)
            except Exception:
                to_remove.append(user_id)

        for user_id in to_remove:
            await self.disconnect(room_id, user_id)

    async def update_participants(self, room_id: str):
        participants = list(self.active_connections[room_id].keys()) if room_id in self.active_connections else []
        await self.update_room_state(room_id, {"list_of_participants": participants})
        await self.broadcast(room_id, {"type": "participants_update", "participants": participants})

    async def get_room_state(self, room_id: str):
        async with self.db.session_factory() as session:
            result = await session.execute(select(Rooms).where(Rooms.id == uuid.UUID(room_id)))
            room = result.scalar_one()
            return {
                "list_track": room.list_track,
                "index_track": room.index_track,
                "status_track": room.status_track,
                "time_moment": room.time_moment,
                "list_of_participants": room.list_of_participants
            }

    async def update_room_state(self, room_id: str, update_data: dict):
        async with self.db.session_factory() as session:
            room = await session.get(Rooms, uuid.UUID(room_id))
            if not room:
                raise ValueError(f"Room {room_id} not found in DB")  # <-- Явная ошибка!

            for key, value in update_data.items():
                setattr(room, key, value)

            await session.commit()
            return room

    async def get_current_playback_time(self, room_id: str, user_id: str = None):
        if room_id not in self.active_connections:
            return None

        responses = []
        
        # Отправляем запрос всем участникам комнаты (кроме user_id, если указан)
        for uid, connection in self.active_connections[room_id].items():
            if uid == user_id:
                continue  # Пропускаем себя, если exclude_user задан
            
            try:
                await connection.send_json({"type": "request_current_time"})
            except Exception as e:
                print(f"Failed to send time request to {uid}: {e}")
                continue

        # Ждём ответа в основном цикле обработки сообщений (через _handle_message)
        # Здесь просто возвращаем 0.0, а реальное время будем получать через callback
        return 0.0

    async def _get_time_from_connection(self, connection: WebSocket):
        try:
            await connection.send_json({"type": "request_current_time"})
            response = await asyncio.wait_for(connection.receive_json(), timeout=2.0)
            
            if response.get("type") == "current_time":
                return response.get("position")
        except Exception as e:
            print('ERROR FROM _get_time_from_connection:', e)
            return None
