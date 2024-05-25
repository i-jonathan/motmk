from enum import Enum

from pydantic import BaseModel

from schema.base import Base
from schema.user import User


class DataType(str, Enum):
    Default = "Default"
    Audio = "Audio"
    Image = "Image"
    File = "File"


class DataSetCreate(BaseModel):
    name: str


class DataSetInternal(DataSetCreate):
    type: DataType = DataType.Default
    path: str


class DataSet(Base, DataSetInternal):
    created_by: User

    class Config:
        from_attributes = True
