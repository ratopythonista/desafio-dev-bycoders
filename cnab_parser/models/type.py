from sqlalchemy import Column, Integer, String

from cnab_parser.models import Base


class TypeModel(Base):
    __tablename__ = "type"
    type_id = Column(Integer, primary_key=True)
    description = Column(String, index=True, nullable=False)
    nature = Column(String, index=True, nullable=False)
    signal = Column(String(length=1), index=False, nullable=False)