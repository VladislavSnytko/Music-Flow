# websocket_routes.py
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json
from .websocket_manager import ConnectionManager

class WebSocketRoutes:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def handle_websocket(self, websocket: WebSocket, room_id: str, user_id: str):
        # Проверяем существование комнаты
        try:
            room_state = await self.manager.get_room_state(room_id)
        except:
            await websocket.close(code=1008, reason="Room not found")
            return

        await self.manager.connect(websocket, room_id, user_id)
        room_state = await self.manager.get_room_state(room_id)
        
        try:
            # Отправляем текущее состояние комнаты новому участнику
            await websocket.send_json({
                "type": "init",
                "room": room_state,
                'user_id': user_id
            })
            if room_state["list_track"] and len(room_state["list_track"]) > 0:
                await self.handle_play(room_id, user_id, {
                    "position": room_state["time_moment"] or 0
                })
        
            while True:
                data = await websocket.receive_json()
                # print(data)
                if data["type"] == "play":
                    await self.handle_play(room_id, user_id, data)
                elif data["type"] == "pause":
                    await self.handle_pause(room_id, user_id, data)
                elif data["type"] == "change_track":
                    await self.handle_change_track(room_id, user_id, data)
                elif data["type"] == "seek":
                    await self.handle_seek(room_id, user_id, data)
                elif data["type"] == "add_participant":
                    await self.handle_add_participant(room_id, user_id)
                elif data["type"] == "get_participants":
                    await websocket.send_json({
                "type": "participants_update",
                "participants": list(self.manager.active_connections[room_id].keys())
                })
                elif data["type"] == "load":
                    await websocket.send_json({
                "type": "load_track",
                "url": list(self.manager.active_connections[room_id].keys())
                })
                    # print(1, list(self.manager.active_connections[room_id].keys()))

                
        except WebSocketDisconnect:
            await self.handle_disconnect(room_id, user_id)

    async def handle_play(self, room_id: str, user_id: str, data: dict):
        await self.manager.update_room_state(room_id, {
            "status_track": True,
            "time_moment": data.get("position", 0)
        })
        
        await self.manager.broadcast(room_id, {
            "type": "play",
            "position": data.get("position", 0),
            "timestamp": datetime.now().timestamp()
        }, exclude_user=user_id)

    async def handle_pause(self, room_id: str, user_id: str, data: dict):
        await self.manager.update_room_state(room_id, {
            "status_track": False,
            "time_moment": data.get("position", 0)
        })
        
        await self.manager.broadcast(room_id, {
            "type": "pause",
            "position": data.get("position", 0),
            "timestamp": datetime.now().timestamp()
        }, exclude_user=user_id)

    async def handle_change_track(self, room_id: str, user_id: str, data: dict):
        await self.manager.update_room_state(room_id, {
            "list_track": data["tracks"],
            "index_track": data["index"],
            "status_track": False,
            "time_moment": 0
        })
        print('hui zdes')
        await self.manager.broadcast(room_id, {
            "type": "load_track",  # Было "load"
            'url': data["tracks"][data["index"]]
        })
        
        # await self.manager.broadcast(room_id, {
        #     "type": "change_track",
        #     "tracks": data["tracks"],
        #     "index": data["index"],
        #     "timestamp": datetime.now().timestamp()
        # }, exclude_user=user_id)

    async def handle_seek(self, room_id: str, user_id: str, data: dict):
        await self.manager.update_room_state(room_id, {
            "time_moment": data["position"]
        })
        
        await self.manager.broadcast(room_id, {
            "type": "seek",
            "position": data["position"],
            "timestamp": datetime.now().timestamp()
        }, exclude_user=user_id)

    async def handle_add_participant(self, room_id: str, user_id: str):
        room_state = await self.manager.get_room_state(room_id)
        if user_id not in room_state["list_of_participants"]:
            await self.manager.update_room_state(room_id, {
                "list_of_participants": [*room_state["list_of_participants"], user_id]
            })
            
            await self.manager.broadcast(room_id, {
                "type": "participants_update",
                "participants": [*room_state["list_of_participants"], user_id]
            })

    async def handle_disconnect(self, room_id: str, user_id: str):
        await self.manager.disconnect(room_id, user_id)
        room_state = await self.manager.get_room_state(room_id)
        if user_id in room_state["list_of_participants"]:
            await self.manager.update_room_state(room_id, {
                "list_of_participants": [
                    uid for uid in room_state["list_of_participants"] 
                    if uid != user_id
                ]
            })
            
            await self.manager.broadcast(room_id, {
                "type": "participants_update",
                "participants": [
                    uid for uid in room_state["list_of_participants"] 
                    if uid != user_id
                ]
            })