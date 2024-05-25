from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.orm import Session
from schema.user import UserCreate, GroupBase
from schema.data_set import DataSetInternal
from database.model.user_data import User, Group
from database.model.data_set import DataSet


class UserRepositoryInterface(ABC):
    @classmethod
    @abstractmethod
    def create_user(cls, db: Session, user: UserCreate) -> User | None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def fetch_user_by_email(cls, db: Session, email: str) -> User | None:
        raise NotImplemented


class GroupRepositoryInterface(ABC):
    @classmethod
    @abstractmethod
    def create_group(cls, db: Session, group: GroupBase, owner_id: int) -> Group:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def fetch_groups_by_name(cls, db: Session, name: str) -> list[Type[Group]] | None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def fetch_all_groups(cls, db: Session) -> list[Type[Group]]:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def check_group_name_exist(cls, db: Session, name: str) -> bool:
        raise NotImplemented


class DataSetInterface(ABC):
    @classmethod
    @abstractmethod
    def create_dataset(cls, db: Session, data_set: DataSetInternal, owner_id: int) -> DataSet | None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def fetch_dataset_by_id(cls, db: Session, dataset_id: int) -> DataSet | None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def update_dataset(cls, db: Session, data_set: DataSetInternal, data_id: int) -> DataSet | None:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def delete_dataset(cls, db:Session, dataset_id: int) -> DataSet | None:
        raise NotImplemented
