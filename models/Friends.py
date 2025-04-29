import uuid
from sqlalchemy import Column, String, ARRAY, UUID, ForeignKey
from dataclasses import dataclass


from db.base import Base

# Модель User
@dataclass
class Friends(Base):
    __tablename__: str = "friends"
    
    user_id: str = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    friends_user: list = Column(ARRAY(String))
