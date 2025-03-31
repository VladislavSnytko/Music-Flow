from sqlalchemy import Column, Integer, String, ARRAY
from dataclasses import dataclass

from db.base import Base

# Модель Rooms
@dataclass
class Rooms(Base):
    __tablename__: str = "rooms"
    id: str = Column(String, primary_key=True, index=True)
    list_track: list = Column(ARRAY(String))
    index_track: int = Column(Integer)