# websocket_routes.py
import asyncio
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json
from .websocket_manager import ConnectionManager

# class WebSocketRoutes:
#     def __init__(self, manager: ConnectionManager):
#         self.manager = manager

#     async def handle_websocket(self, websocket: WebSocket, room_id: str, user_id: str):
#         # Проверяем существование комнаты
#         try:
#             room_state = await self.manager.get_room_state(room_id)
#         except:
#             await websocket.close(code=1008, reason="Room not found")
#             return

#         await self.manager.connect(websocket, room_id, user_id)
#         current_position = await self.manager.get_current_playback_time(room_id)
#         if current_position is not None and int(current_position) > 0 and current_position != room_state["time_moment"]:
#             # Обновляем время в базе данных
#             await self.manager.update_room_state(room_id, {
#                 "time_moment": current_position
#             })
#             room_state["time_moment"] = current_position
#         room_state = await self.manager.get_room_state(room_id)
        
#         try:
#             # Отправляем текущее состояние комнаты новому участнику
#             await websocket.send_json({
#                 "type": "init",
#                 "room": room_state,
#                 'user_id': user_id,
#                 'current_time': room_state["time_moment"] or 0,  # Добавляем текущее время
#                 'is_playing': room_state["status_track"]         # Добавляем статус воспроизведения
#             })
#             if room_state["list_track"] and len(room_state["list_track"]) > 0:
#                 await websocket.send_json({
#                     "type": "track_state",
#                     "url": room_state["list_track"][room_state["index_track"]],
#                     "position": room_state["time_moment"] or 0,
#                     "is_playing": room_state["status_track"]
#                 })
        
#             while True:
#                 data = await websocket.receive_json()
#                 # print(data)
#                 if data["type"] == "play":
#                     await self.handle_play(room_id, user_id, data)
#                 elif data["type"] == "current_time":  # Обработка ответа с текущим временем
#                     return
#                 elif data["type"] == "pause":
#                     await self.handle_pause(room_id, user_id, data)
#                 elif data["type"] == "change_track":
#                     await self.handle_change_track(room_id, user_id, data)
#                 elif data["type"] == "seek":
#                     await self.handle_seek(room_id, user_id, data)
#                 elif data["type"] == "add_participant":
#                     await self.handle_add_participant(room_id, user_id)
#                 elif data["type"] == "get_participants":
#                     print(self.manager.active_connections[room_id])
#                     await websocket.send_json({
#                 "type": "participants_update",
#                 "participants": list(self.manager.active_connections[room_id].keys())
#                 })
#                 elif data["type"] == "load":
#                     await websocket.send_json({
#                 "type": "load_track",
#                 "url": list(self.manager.active_connections[room_id].keys())
#                 })
#                     # print(1, list(self.manager.active_connections[room_id].keys()))

                
#         except WebSocketDisconnect:
#             await self.handle_disconnect(room_id, user_id)
class WebSocketRoutes:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self.message_queues = {}

    async def handle_websocket(self, websocket: WebSocket, room_id: str, user_id: str):
        try:
            room_state = await self.manager.get_room_state(room_id)
        except:
            await websocket.close(code=1008, reason="Room not found")
            return

        await self.manager.connect(websocket, room_id, user_id)

        # 1. Запрашиваем текущее время у существующих участников
        current_position = await self._get_consensus_time(room_id, user_id)
        print(current_position)
        # 2. Обновляем состояние комнаты (если время изменилось)
        if current_position != room_state["time_moment"]:
            await self.manager.update_room_state(room_id, {
                "time_moment": current_position,
            })
            room_state["time_moment"] = current_position

        # 3. Отправляем новому участнику начальное состояние
        await self._send_initial_state(websocket, room_state, user_id)

        # 4. Основной цикл обработки сообщений
        try:
            while True:
                data = await websocket.receive_json()
                await self._handle_message(data, room_id, user_id, websocket)
                
        except WebSocketDisconnect:
            await self.manager.disconnect(room_id, user_id)

    # async def _get_consensus_time(self, room_id: str, user_id: str) -> float:
    #     """Получаем актуальное время от других участников с гарантией ответа."""
    #     if room_id not in self.manager.active_connections:
    #         return 0.0

    #     connections = [
    #         conn for uid, conn in self.manager.active_connections[room_id].items()
    #         if uid != user_id
    #     ]

    #     if not connections:
    #         return 0.0

    #     # Создаем уникальный идентификатор запроса
    #     request_id = str(uuid.uuid4())
    #     responses = []

    #     # Отправляем запрос всем участникам
    #     tasks = []
    #     for conn in connections:
    #         task = asyncio.create_task(
    #             self._get_time_from_connection(conn, request_id)
    #         )
    #         tasks.append(task)

    #     try:
    #         # Ждем первый ответ с таймаутом 1 секунда
    #         done, pending = await asyncio.wait(
    #             tasks,
    #             timeout=1.0,
    #             return_when=asyncio.FIRST_COMPLETED
    #         )
            
    #         # Обрабатываем ответы
    #         for task in done:
    #             try:
    #                 response = await task
    #                 if response is not None:
    #                     responses.append(response)
    #             except Exception as e:
    #                 print(f"Error processing time response: {e}")

    #         # Отменяем оставшиеся запросы
    #         for task in pending:
    #             task.cancel()

    #         # Возвращаем медианное значение для надежности
    #         return sorted(responses)[len(responses) // 2] if responses else 0.0

    #     except Exception as e:
    #         print(f"Error in consensus time: {e}")
    #         return 0.0
    async def _get_consensus_time(self, room_id: str, user_id: str) -> float:
        """Полностью переработанный метод с очередями сообщений"""
        if room_id not in self.manager.active_connections:
            return 0.0

        active_connections = [
            (uid, conn) for uid, conn in self.manager.active_connections[room_id].items()
            if uid != user_id
        ]

        if not active_connections:
            return 0.0

        request_id = str(uuid.uuid4())
        response_queue = asyncio.Queue()
        tasks = []

        # Создаем задачи для запросов
        for uid, conn in active_connections:
            task = asyncio.create_task(
                self._safe_time_request(conn, request_id, response_queue)
            )
            tasks.append(task)

        try:
            # Ждем первый ответ с таймаутом 500мс
            try:
                result = await asyncio.wait_for(response_queue.get(), timeout=0.5)
                return result
            except asyncio.TimeoutError:
                return 0.0
        finally:
            # Очищаем все задачи
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_time_request(self, connection: WebSocket, request_id: str, response_queue: asyncio.Queue):
        """Безопасный запрос времени с обработкой очереди сообщений"""
        try:
            # Регистрируем очередь для этого соединения
            if connection not in self.message_queues:
                self.message_queues[connection] = asyncio.Queue()
                asyncio.create_task(self._message_router(connection))

            # Отправляем запрос
            await connection.send_json({
                "type": "request_current_time",
                "request_id": request_id
            })

            # Ждем ответ в очереди
            while True:
                message = await self.message_queues[connection].get()
                print(1)
                if (message.get("type") == "current_time" and 
                    message.get("request_id") == request_id):
                    await response_queue.put(message.get("position", 0.0))
                    return
        except Exception as e:
            print(f"Safe request failed: {e}")

    async def _message_router(self, connection: WebSocket):
        """Маршрутизатор сообщений для одного соединения"""
        try:
            while True:
                message = await connection.receive_json()
                if connection in self.message_queues:
                    await self.message_queues[connection].put(message)
        except:
            if connection in self.message_queues:
                del self.message_queues[connection]
    async def _get_time_from_connection(self, connection: WebSocket, request_id: str):
        """Получаем время от конкретного участника с гарантией ответа."""
        try:
            # Отправляем запрос с уникальным ID
            await connection.send_json({
                "type": "request_current_time",
                "request_id": request_id
            })

            # Ждем ответ с таймаутом 500мс
            response = await asyncio.wait_for(
                connection.receive_json(),
                timeout=0.5
            )

            # Проверяем, что это ответ на наш запрос
            if response.get("type") == "current_time" and response.get("request_id") == request_id:
                return response.get("position")
            
            return None
        except (asyncio.TimeoutError, Exception) as e:
            print(f"Timeout getting time from connection: {e}")
            return None

    async def _send_initial_state(self, websocket: WebSocket, room_state: dict, user_id: str):
        """Отправляет новому участнику текущее состояние комнаты."""
        message = {
            "type": "init",
            "room": room_state,
            "user_id": user_id,
            "current_time": room_state["time_moment"] or 0,
            "is_playing": room_state["status_track"]
        }
        
        if room_state["list_track"] and len(room_state["list_track"]) > 0:
            message.update({
                "track_url": room_state["list_track"][room_state["index_track"]],
                "track_info": {
                    "title": "Загрузка...",  # Можно добавить реальные данные из кэша
                    "artist": "",
                    "cover": ""
                }
            })
    
        await websocket.send_json(message)

    async def _handle_message(self, data: dict, room_id: str, user_id: str, websocket: WebSocket):
        """Обрабатывает входящие WebSocket-сообщения."""
        if data["type"] == "current_time":
            return  # Игнорируем ответы на request_current_time

        elif data["type"] == "play":
            await self.manager.update_room_state(room_id, {
                "status_track": True,
                "time_moment": data.get("position", 0)
            })
            await self.manager.broadcast(room_id, data, exclude_user=user_id)

        elif data["type"] == "pause":
            await self.manager.update_room_state(room_id, {
                "status_track": False,
                "time_moment": data.get("position", 0)
            })
            await self.manager.broadcast(room_id, data, exclude_user=user_id)
        elif data["type"] == "change_track":
            await self.handle_change_track(room_id, user_id, data)
        elif data["type"] == "seek":
            await self.handle_seek(room_id, user_id, data)
        elif data["type"] == "add_participant":
            await self.handle_add_participant(room_id, user_id)
        elif data["type"] == "get_participants":
            # print(self.manager.active_connections[room_id])
            await websocket.send_json({
                "type": "participants_update",
                "participants": list(self.manager.active_connections[room_id].keys())
            })
        elif data["type"] == "load":
            await websocket.send_json({
                "type": "load_track",
                "url": list(self.manager.active_connections[room_id].keys())
            })

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
        # print('hui zdes')
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