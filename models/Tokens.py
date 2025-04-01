import uuid
from sqlalchemy import Column, String, ARRAY, UUID
from dataclasses import dataclass


from db.base import Base

# Модель User
@dataclass
class Tokens(Base):
    __tablename__: str = "tokens"

    user_id: str = Column(String)
    token: str = Column(String, unique=True)
