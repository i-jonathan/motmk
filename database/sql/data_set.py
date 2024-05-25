from sqlalchemy.exc import SQLAlchemyError

from database.interfaces.data import DataSetInterface
from sqlalchemy.orm import Session
from schema.data_set import DataSetInternal
from database.model.data_set import DataSet


class DataSetImplementation(DataSetInterface):
    @classmethod
    def create_dataset(cls, db: Session, data_set: DataSetInternal, owner_id: int) -> DataSet | None:
        try:
            db_data = DataSet(name=data_set.name, type=data_set.type.value, created_by_id=owner_id, path=data_set.path)
            db.add(db_data)
            db.commit()
            db.refresh(db_data)
            return db_data
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            return None

    @classmethod
    def fetch_dataset_by_id(cls, db: Session, dataset_id: int) -> DataSet | None:
        try:
            resp = db.query(DataSet).filter(DataSet.id == dataset_id).one()
            return resp
        except SQLAlchemyError as e:
            print(e)
            return None

    @classmethod
    def update_dataset(cls, db: Session, data_set: DataSetInternal, data_id: int) -> DataSet | None:
        resp = cls.fetch_dataset_by_id(db, data_id)
        if resp is None:
            return None
        try:
            resp.name = data_set.name
            resp.type = data_set.type
            resp.path = data_set.path
            db.commit()
            db.refresh(resp)
            return resp
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            return None

    @classmethod
    def delete_dataset(cls, db: Session, dataset_id: int) -> bool:
        db.query(DataSet).filter(DataSet.id == dataset_id).delete()
        db.commit()
        return True
