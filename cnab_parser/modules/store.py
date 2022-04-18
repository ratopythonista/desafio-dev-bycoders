from sqlalchemy.orm import Session

from cnab_parser.models.store import StoreModel


class StoreCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_name(self, name: str) -> StoreModel:
        return self.db.query(StoreModel).filter(StoreModel.name == name).one_or_none()

    def get_all(self):
        store_model_list = self.db.query(StoreModel).all()
        return store_model_list

    def insert(self, name: str, owner: str) -> StoreModel:
        store_model = StoreModel(name=name, owner=owner)
        self.db.add(store_model)
        self.db.commit()
        self.db.refresh(store_model)
        return store_model