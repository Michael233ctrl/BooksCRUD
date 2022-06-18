from pydantic import BaseModel
from datetime import datetime


class BookBase(BaseModel):
    title: str
    publisher: str
    author: str
    pages: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
