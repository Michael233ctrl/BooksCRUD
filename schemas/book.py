from typing import List, Optional

from pydantic import BaseModel, Field
from datetime import datetime


class BookBase(BaseModel):
    id: int = Field(description="Book id")
    title: str = Field(description="Book title")
    publisher: str = Field(description="Book publisher")
    author: str = Field(description="Book author")
    pages: Optional[str] = Field(description="Book pages")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    id: int
    name: str = Field(description="Tag title")

    class Config:
        orm_mode = True


class TagRequestBody(BaseModel):
    tagId: int


class BookSchema(BookBase):
    tags: List[TagBase]


class TagSchema(TagBase):
    books: List[BookBase]


class TagCreate(BaseModel):
    name: str = Field(description="Tag title")

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str = Field(description="Book title")
    publisher: str = Field(description="Book publisher")
    author: str = Field(description="Book author")
    pages: Optional[str] = Field(description="Book pages")
    tags: Optional[List[TagCreate]]

    class Config:
        orm_mode = True
