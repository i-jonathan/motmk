from database.model.setup import get_base
from sqlalchemy import Column, String, Integer, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class DataSet(get_base()):
    __tablename__ = 'data_set'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    path = Column(String)
    created_at = Column(DateTime, default=func.now())
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_by = relationship('User', back_populates='data_sets')
