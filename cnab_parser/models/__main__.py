from loguru import logger
from sqlalchemy.exc import IntegrityError

from cnab_parser.models import Base, engine, get_db
from cnab_parser.models.type import TypeModel
from cnab_parser.modules.type import TypeCrud
from cnab_parser.models.store import StoreModel
from cnab_parser.models.transaction import TransactionModel


Base.metadata.create_all(bind=engine)
database = next(get_db())

try:
    TypeCrud(database).populate()
except IntegrityError:
    logger.info("ALREADY POPULATED") 