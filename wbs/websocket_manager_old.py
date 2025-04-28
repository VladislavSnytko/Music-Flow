# websocket_manager.py
import asyncio
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
    
    # Добавляем подключение
        self.active_connections[room_id][user_id] = websocket
    
    # Обновляем список участников в БД
        participants = list(self.active_connections[room_id].keys())
        # print(participants)
        await self.update_room_state(room_id, {
            "list_of_participants": participants
        })
        await self.broadcast(room_id, {
        "type": "participants_update",
        "participants": participants
        })

    async def disconnect(self, room_id: str, user_id: str):
        if room_id not in self.active_connections:
            return
        if user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            participants = list(self.active_connections[room_id].keys()) if room_id in self.active_connections else []
            if room_id in self.active_connections:  # Проверяем, что комната еще существует
                await self.update_room_state(room_id, {
                    "list_of_participants": participants
                })
                await self.broadcast(room_id, {
                    "type": "participants_update",
                    "participants": participants
                })
            if room_id in self.active_connections and not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message: Dict, exclude_user: str = None):
        # print(message)
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
        
    async def get_current_playback_time(self, room_id: str):
        if room_id not in self.active_connections:
            return None
            
        # Создаем список задач для получения времени от всех участников
        tasks = []
        for user_id, connection in self.active_connections[room_id].items():
            try:
                # Создаем задачу для каждого подключения
                tasks.append(self._get_time_from_connection(connection))
            except:
                continue
        
        # Ждем первый успешный ответ
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                if result is not None:
                    return result
            except:
                continue
        
        return None
    
    async def _get_time_from_connection(self, connection: WebSocket):
        try:
            await connection.send_json({
                "type": "request_current_time"
            })
            # Устанавливаем таймаут для ожидания ответа
            response = await asyncio.wait_for(connection.receive_json(), timeout=2.0)
            print(f'RESPONSE TYPE: {response}')
            if response.get("type") == "current_time":
                return response.get("position")
        except (asyncio.TimeoutError, Exception):
            return None