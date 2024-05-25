from database.model.setup import get_base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class UserGroups(get_base()):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)


class User(get_base()):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    name = Column(String)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    groups_in = relationship("Group", secondary=UserGroups.__table__, back_populates="members")

    groups = relationship("Group", back_populates="owner")
    data_sets = relationship("DataSet", back_populates="created_by")


class Group(get_base()):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    members = relationship("User", secondary=UserGroups.__table__, back_populates="groups_in")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="groups")
