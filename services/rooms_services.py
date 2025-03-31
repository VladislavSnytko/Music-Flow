import asyncio
# from db.base import engine, Base, AsyncSession
from models.Rooms import Rooms  # Импорт всех моделей
from sqlalchemy import select
from db.base import Database

# FastAPI Dependency
class RoomsServices:
    def __init__(self, db: Database):
        self.db = db

    async def get_all(self):
        async with self.db.session_factory() as session:
            print(session)
            result = await session.execute(select(Rooms))
            # print(result.scalars().one())
            return result.scalars().all()
        
if __name__ == '__main__':
    d = Database()
    b = RoomsServices(d)
    asyncio.run(b.get_all())