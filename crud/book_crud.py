from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import schemas
from models import Book
from .base_crud import BaseCRUD
from .tag_crud import TagCRUD


class BookCRUD(BaseCRUD):
    def __init__(self, db: AsyncSession):
        self.model = Book
        super().__init__(db, self.model)

    async def get_books(self):
        return await self._get_all_objects(self.model.tags)

    async def get_book_by_id(self, book_id: int):
        return await self._get_object_by_field("id", book_id, self.model.tags)

    async def __book_cleaned_data(self, book: schemas.BookCreate):
        if await self._get_object_by_field("title", book.title, self.model.tags):
            return None

        tag_crud = TagCRUD(self.db)
        book.tags = [await tag_crud.get_or_create_tag(tag.name) for tag in book.tags]
        return book.dict(exclude_unset=True)

    async def create_book(self, book: schemas.BookCreate):
        cleaned_data = await self.__book_cleaned_data(book)
        return await self._create(cleaned_data) if cleaned_data else None

    async def update_book(self, book_db, book: schemas.BookUpdate):
        cleaned_data = await self.__book_cleaned_data(book)
        return await self._update(book_db, cleaned_data) if cleaned_data else None

    async def delete_book(self, book_id):
        if not (
            book_db := await self._get_object_by_field("id", book_id, self.model.tags)
        ):
            return True
        await self._delete(book_db)

    # async def delete_book_tags(self, book_id: int, tag_id: int):
    #     query = await self.db.execute(
    #         select(BookTags).where(
    #             and_(BookTags.book_id == book_id, BookTags.tag_id == tag_id)
    #         )
    #     )
    #     if query.scalars().one_or_none():
    #         return True
    #
    #     await self.db.delete(query)
