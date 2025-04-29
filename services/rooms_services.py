import asyncio

import sqlalchemy
# from db.base import engine, Base, AsyncSession
from models.Rooms import Rooms  # Импорт всех моделей
from models.Users import Users
from models.Friends import Friends
# from models.Tokens import Tokens
from sqlalchemy import select
from db.base import Database, Base

# FastAPI Dependency
class RoomsServices:
    def __init__(self, db: Database):
        self.db = db

    async def get_all(self):
        async with self.db.session_factory() as session:
            print(session)
            result = await session.execute(select(Rooms))
            result = result.scalars().all()
            # print(result.scalars().one())
            return [{'id': str(i.id), 
                     'name_room': i.name_room, 
                     'list_track': list(i.list_track), 
                     'index_track': i.index_track,
                     'list_of_participants': list(i.list_of_participants),
                     'list_users': dict(i.list_users),
                     'users_index': dict(i.users_index),
                     'status_track': i.status_track,
                     'time_moment': i.time_moment} for i in result]
        
    async def create_room(self, name_room: str, user_id: str):
        async with self.db.session_factory() as session:
            new_room = Rooms(
                name_room=name_room, 
                list_track=[], 
                index_track=0, 
                list_of_participants=[user_id],
                list_users={user_id: []},
                users_index={user_id: 0},
                status_track=False,
                time_moment=0
            )
            session.add(new_room)
            await session.commit()
            print(new_room.id)
            return {'Status': 'Successfully', 'id': new_room.id}
        
    async def update_participants(self, room_id: str, user_id: str):
        async with self.db.session_factory() as session:
            # Получаем комнату
            room = await session.get(Rooms, room_id)
            if not room:
                return {"status": "error", "message": "Комната не найдена"}
            
            # Проверяем, что пользователь еще не в комнате
            if user_id in room.list_of_participants:
                return {"status": "error", "message": "Пользователь уже в комнате"}
            
            # Добавляем пользователя
            room.list_of_participants.append(user_id)
            room.list_users[user_id] = []  # Инициализируем пустой список для пользователя
            room.users_index[user_id] = 0  # Устанавливаем начальный индекс
            
            await session.commit()
            
            return room


    async def create_database(self):
    # Создает все таблицы, определенные в Base.metadata
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы!")
        
if __name__ == '__main__':
    d = Database()
    b = RoomsServices(d)
    asyncio.run(b.create_database())
    # b.create_database()