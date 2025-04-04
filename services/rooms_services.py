import asyncio

import sqlalchemy
# from db.base import engine, Base, AsyncSession
from models.Rooms import Rooms  # Импорт всех моделей
from models.Users import Users
from models.Friends import Friends
from models.Tokens import Tokens
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
        
    async def create_room(self, name_room: str):
        async with self.db.session_factory() as session:
            new_room = Rooms(
                name_room=name_room, 
                list_track=[], 
                index_track=0, 
                list_of_participants=[],
                list_users={'test': []},
                users_index={'test': 0},
                status_track=False,
                time_moment=0
            )
            session.add(new_room)
            await session.commit()
            return {'Status': 'Successfully'}

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