import asyncio

import sqlalchemy
from sqlalchemy import select

from models.Users import Users  # Импорт всех моделей
from models.Tokens import Tokens

from db.base import Database
# from db.base import engine, Base, AsyncSession

from pydantic import EmailStr

import jwt
import secrets

from hashlib import sha256


class UserServices:
    def __init__(self, db: Database):
        self.db = db


    async def create_token(self, obj):
        secret_key = secrets.token_urlsafe(20)

        token = jwt.encode(obj, secret_key, algorithm='HS256')
        return token    


    async def hash_password(self, password):
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password

    async def get_all(self):
        async with self.db.session_factory() as session:
            result = await session.execute(select(Users))
            result = result.scalars().all()
            result = [{'id': str(i.id), 
                     'email': i.email, 
                     'hashed_password': i.hashed_password, 
                     'username': i.username,
                     'birthday': i.birthday,
                     'rooms_list': list(i.rooms_list),
                     'yandex_token': i.yandex_token
                    }
                    for i in result]
            print(result)
            return result
        
    async def create_new_user(self, email: EmailStr, password: str, username: str, birthday: str, rooms_list: list = [], yandex_token: str = None):
        async with self.db.session_factory() as session:
            hashed_password =  await self.hash_password(password)
            new_user = Users(
                email=email,
                hashed_password=hashed_password,
                username=username,
                birthday=birthday,
                rooms_list=rooms_list,
                yandex_token=yandex_token
            )
            # new_user_friends = 

        session.add(new_user)
        await session.commit()

        return {'Status': 'Successfully'}
    
    async def logging(self, obj: dict):
        async with self.db.session_factory() as session:
            print(obj)
            if 'yandex_token' in obj:
                result = await session.execute(select(Users).where(Users.yandex_token == obj['yandex_token']))
            else:
                result = await session.execute(select(Users).where((Users.email == obj['nickname'] or Users.username == obj['nickname']) and 
                                                                   Users.hashed_password == obj['hashed_password']))
            user = result.scalar_one()
            print(user)
            if user:
                return user
            return None
        
    async def add_room(self, room_id: str, user_id: str):
        async with self.db.session_factory() as session:
            result = await session.execute(select(Users).where(Users.id == user_id))
            print(type(result))

        
if __name__ == '__main__':
    d = Database()
    b = UserServices(d)
    
    asyncio.run(b.create_new_user(email="artem.com", password="1234567", birthday="12.06.2005", username="1neplay"))
    # asyncio.run(b.get_all())
    # b.create_database()