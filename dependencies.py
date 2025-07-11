from db.base import Database
from wbs.websocket_manager import ConnectionManager
from wbs.websocket_routes import WebSocketRoutes

def get_db():
    db = Database()
    try:
        yield db
    finally:
        pass  # Можно добавить закрытие соединения при необходимости

# Инициализация менеджера WebSocket
db = Database()
manager = ConnectionManager(db)
ws_routes = WebSocketRoutes(manager)