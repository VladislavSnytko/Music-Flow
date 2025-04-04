# websocket_manager.py
from typing import Dict, List
import uuid
from datetime import datetime
from fastapi import WebSocket
from sqlalchemy import select
from models.Rooms import Rooms
from db.base import Database

class ConnectionManager:
    def __init__(self, db: Database):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.db = db

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    async def disconnect(self, room_id: str, user_id: str):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message: Dict, exclude_user: str = None):
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                if user_id != exclude_user:
                    try:
                        await connection.send_json(message)
                    except:
                        await self.disconnect(room_id, user_id)

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

    async def update_room_state(self, room_id: str, update_data: Dict):
        async with self.db.session_factory() as session:
            room = await session.get(Rooms, uuid.UUID(room_id))
            for key, value in update_data.items():
                setattr(room, key, value)
            await session.commit()
            return room