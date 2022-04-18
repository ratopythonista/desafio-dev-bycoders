from sqlalchemy.orm import Session
from cnab_parser.models.store import StoreModel

from cnab_parser.models.type import TypeModel
from cnab_parser.models.transaction import TransactionModel


class TransactionCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_store(self, store_id: str) -> TransactionModel:
        transaction_model_list = self.db.query(
            TransactionModel.time,
            TransactionModel.value,
            TransactionModel.cpf,
            TransactionModel.card,
            TransactionModel.type, 
            TypeModel.nature,
            TypeModel.signal,
            TypeModel.description,
            StoreModel.name,
            StoreModel.owner
        ).join(
            TypeModel, TypeModel.type_id == TransactionModel.type
        ).join(
            StoreModel, StoreModel.store_id == TransactionModel.store
        ).filter(
            TransactionModel.store == store_id
        ).order_by(TransactionModel.time.asc()).all()
        
        transaction_list, balance = list(), 0
        for transaction_model in transaction_model_list:
            if transaction_model.signal == "-":
                balance -= transaction_model.value
            else:
                balance += transaction_model.value
            transaction_list.append(dict(transaction_model))

        return transaction_list, balance