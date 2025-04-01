import uuid
from sqlalchemy import Column, Integer, String, ARRAY, UUID, JSON, BOOLEAN
from dataclasses import dataclass

from db.base import Base

# Модель Rooms
@dataclass
class Rooms(Base):
    __tablename__: str = "rooms"
    id: str = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name_room: str = Column(String, nullable=False)
    list_track: list = Column(ARRAY(String))
    index_track: int = Column(Integer)
    list_of_participants: list = Column(ARRAY(String))
    list_users: dict = Column(JSON)
    users_index: dict = Column(JSON)
    status_track: bool = Column(BOOLEAN)
    time_moment: int = Column(Integer)