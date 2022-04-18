import uuid
from typing import List

from sqlalchemy.orm import Session

from cnab_parser.models.type import TypeModel

class TypeCrud:
    def __init__(self, db: Session) -> None:
        self.db = db

    def populate(self):
        """Populate database"""
        transaction_types = [
            TypeModel(type_id=1, description="Débito", nature="Entrada", signal="+"),
            TypeModel(type_id=2, description="Boleto", nature="Saída", signal="-"),
            TypeModel(type_id=3, description="Financiamento", nature="Saída", signal="-"),
            TypeModel(type_id=4, description="Recebimento Empréstimo", nature="Entrada", signal="+"),
            TypeModel(type_id=5, description="Crédito", nature="Entrada", signal="+"),
            TypeModel(type_id=6, description="Vendas", nature="Entrada", signal="+"),
            TypeModel(type_id=7, description="Recebimento TED", nature="Entrada", signal="+"),
            TypeModel(type_id=8, description="Recebimento DOC", nature="Entrada", signal="+"),
            TypeModel(type_id=9, description="Aluguel", nature="Saída", signal="-")
            
        ]
        self.db.bulk_save_objects(transaction_types)
        self.db.commit()

