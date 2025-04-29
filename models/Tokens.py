import uuid
from sqlalchemy import Column, String, ARRAY, UUID
from dataclasses import dataclass


from db.base import Base

# Модель User
@dataclass
class Tokens(Base):
    __tablename__: str = "tokens"
    id: str = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    user_id: str = Column(String)
    token: str = Column(String, unique=True)
