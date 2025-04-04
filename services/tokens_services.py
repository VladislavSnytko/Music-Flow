import asyncio

import sqlalchemy
from sqlalchemy import select

from models.Users import Users  # Импорт всех моделей
from models.Tokens import Tokens

from db.base import Database, Base
# from db.base import engine, Base, AsyncSession

from pydantic import EmailStr

import jwt
import secrets

from hashlib import sha256


class TokenServices:
    def __init__(self, db: Database):
        self.db = db

    async def create_token(self, obj):
        secret_key = secrets.token_urlsafe(20)

        token = jwt.encode(obj, secret_key, algorithm='HS256')
        return token 

    async def check_token(self, token: str):
        async with self.db.session_factory() as session:
            result = await session.execute(select(Tokens).where(Tokens.token == token))
            token_bd = result.scalar_one()
            if token_bd:
                return {'status': 'Successfully', 'user_id': token_bd.user_id}
            return {'status': 'Error', 'message': 'Токен не найден'}
    
    async def new_token(self, user_id: str, obj: dict):
        try:
            async with self.db.session_factory() as session:
                token = await self.create_token(obj)
                new_token = Tokens(user_id=str(user_id), token=token)
                print(f'user: {str(user_id)}\ntoken: {token}')
                session.add(new_token)
                await session.commit()
            return token
        except Exception as e:
            print(e)
            return {'status': 'error', 'message': e}
        

if __name__ == '__main__':
    d = Database()
    b = TokenServices(d)
    asyncio.run(b.create_token({'s': 'w'}))