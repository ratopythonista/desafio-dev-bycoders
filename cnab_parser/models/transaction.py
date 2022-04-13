from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

from cnab_parser.models import Base


class TransactionModel(Base):
    __tablename__ = "transaction"
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    time = Column(DateTime, index=False, nullable=False)
    value = Column(Float, index=False, nullable=False)
    cpf = Column(String(length=11), index=True, nullable=False)
    card = Column(String(length=12), index=True, nullable=False)
    type = Column(Integer, ForeignKey('type.type_id'), index=True, nullable=False)
    store = Column(UUID(as_uuid=True), ForeignKey('store.store_id'))


    type_relationship = relationship("TypeModel")
    store_relationship = relationship("StoreModel")