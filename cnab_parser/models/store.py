from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from cnab_parser.models import Base


class StoreModel(Base):
    __tablename__ = "store"
    store_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, index=True, nullable=False)