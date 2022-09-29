from typing import Union

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update, and_

import models
import schemas
import utils
from .tag_crud import TagCRUD


class BookCRUD(utils.AppCRUD):
    async def get_books(self):
        query = await self.db.execute(
            select(models.Book).options(selectinload(models.Book.tags))
        )
        return query.scalars().all()

    async def get_book_by_field(self, field: str, data: Union[str, int]):
        if hasattr(models.Book, field):
            book = await self.db.execute(
                select(models.Book).where(getattr(models.Book, field) == data)
            )
            return book.scalars().one_or_none()
        else:
            raise AttributeError(f"Book model has no attribute {field}")

    async def create_book(self, book: schemas.BookCreate):
        if await self.get_book_by_field(field="title", data=book.title):
            return None

        tag_service = TagCRUD(self.db)
        tags = [await tag_service.get_or_create_tag(tag.name) for tag in book.tags]
        book.tags = tags
        db_book = models.Book(**book.dict())
        self.db.add(db_book)
        await self.db.commit()
        await self.db.refresh(db_book)
        return db_book

    def update_book(self, book_id: int, book: schemas.BookCreate):
        self.db.execute(
            update(models.Book)
            .where(models.Book.id == book_id)
            .values(
                title=book.title,
                publisher=book.publisher,
                author=book.author,
                pages=book.pages,
            )
        )
        tags = [TagCRUD(self.db).get_or_create_tag(tag.name) for tag in book.tags]
        db_book = self.get_book_by_id(book_id)
        db_book.tags.extend(tags)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id):
        db_book = self.get_book_by_id(book_id)
        if db_book is None:
            return True
        self.db.delete(db_book)
        self.db.commit()

    def delete_book_tags(self, book_id: int, tag_id: int):
        query = (
            self.db.query(models.BookTags)
            .where(
                and_(
                    models.BookTags.book_id == book_id, models.BookTags.tag_id == tag_id
                )
            )
            .one_or_none()
        )
        if query is None:
            return True
        self.db.delete(query)
        self.db.commit()
