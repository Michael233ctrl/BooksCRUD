from sqlalchemy.ext.asyncio import AsyncSession

import schemas
import utils
import crud


class BookService(utils.AppService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.book_crud = crud.BookCRUD(db)

    async def get_books(self):
        return await self.book_crud.get_books()

    async def get_book_by_id(self, book_id: int):
        if not (book_db := await self.book_crud.get_book_by_id(book_id)):
            raise utils.AppException.BookGet(context={"id": book_id})
        return book_db

    async def create_book(self, book: schemas.BookCreate):
        if not (book_db := await self.book_crud.create_book(book)):
            raise utils.AppException.BookAlreadyExists(context={"title": book.title})
        return book_db

    async def update_book(self, book_id: int, book: schemas.BookUpdate):
        if not (book_db := await self.book_crud.get_book_by_id(book_id)):
            return await self.create_book(book)
        if not (created_book := await self.book_crud.update_book(book_db, book)):
            raise utils.AppException.BookAlreadyExists(context={"title": book.title})
        return created_book

    async def delete_book(self, book_id: int):
        if await self.book_crud.delete_book(book_id):
            raise utils.AppException.BookGet(context={"id": book_id})

    # async def delete_book_tags(self, book_id: int, tag_id: int):
    #     if await self.book_crud.delete_book_tags(book_id, tag_id):
    #         raise utils.AppException.BookTagDoesNotExist(
    #             context={"book_id": book_id, "tag_id": tag_id}
    #         )
