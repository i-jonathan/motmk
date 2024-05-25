from typing import Type

from sqlalchemy.exc import SQLAlchemyError

from database.interfaces.data import UserRepositoryInterface, GroupRepositoryInterface
from sqlalchemy.orm import Session
from schema.user import UserCreate, GroupBase
from database.model.user_data import User, Group, UserGroups


class UserRepoImplementation(UserRepositoryInterface):
    @classmethod
    def create_user(cls, db: Session, user: UserCreate) -> User | None:
        try:
            db_user = User(email=user.email, password=user.password, name=user.name)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            return None

    @classmethod
    def fetch_user_by_email(cls, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()


class GroupRepoImplementation(GroupRepositoryInterface):
    @classmethod
    def create_group(cls, db: Session, group: GroupBase, owner_id: int) -> Group | None:
        try:
            db_group = Group(name=group.name, owner_id=owner_id, description=group.description)
            db.add(db_group)
            db.commit()
            db.refresh(db_group)
            user_group = UserGroups(user_id=owner_id, group_id=db_group.id)
            db.add(user_group)
            db.commit()
            db.refresh(user_group)
            return db_group
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            return None

    @classmethod
    def fetch_groups_by_name(cls, db: Session, name: str) -> list[Type[Group]]:
        result = db.query(Group).filter(Group.name.contains(name)).all()
        return result

    @classmethod
    def fetch_all_groups(cls, db: Session) -> list[Type[Group]]:
        return db.query(Group).all()

    @classmethod
    def check_group_name_exist(cls, db: Session, name: str) -> bool:
        resp = db.query(Group).filter(Group.name == name).all()
        return len(resp) > 0
