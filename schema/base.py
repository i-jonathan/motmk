from datetime import datetime
from pydantic import BaseModel


class Base(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
