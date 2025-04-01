import uuid
from sqlalchemy import Column, String, ARRAY, UUID
from dataclasses import dataclass


from db.base import Base

# Модель User
@dataclass
class Friends(Base):
    __tablename__: str = "friends"
    
    user_id: str = Column(String)
    friends_user: list = Column(ARRAY(String))
