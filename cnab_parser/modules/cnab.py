from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from cnab_parser.modules.store import StoreCRUD
from cnab_parser.models.transaction import TransactionModel


class CNAB:
    def __init__(self, db: Session, content: str) -> None:
        self.db = db
        self.content_lines = content.strip().split('\n')

    def parser(self):
        self.transactions = 0
        for transaction in self.content_lines:
            self.date = transaction[1:9]
            self.time = transaction[42:48]
            store_name=transaction[62:81].strip()
            store_crud = StoreCRUD(self.db)
            store_model = store_crud.get_by_name(store_name)
            if not store_model:
                store_owner=transaction[48:62].strip()
                store_model = store_crud.insert(store_name, store_owner)
            transaction_model = TransactionModel(
                type = transaction[0:1],
                value = int(transaction[9:19]) / 100.0,
                cpf = transaction[19:30],
                card = transaction[30:42],
                time = datetime.strptime(f'{self.date} {self.time}', "%Y%m%d %H%M%S"),
                store = store_model.store_id
            )
            self.db.add(transaction_model)
            self.db.commit()
            self.db.refresh(transaction_model)
            self.transactions += 1
        return self