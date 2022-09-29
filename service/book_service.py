from sqlalchemy.ext.asyncio import AsyncSession

import schemas
import utils
import crud


class BookService(utils.AppService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.book_service = crud.BookCRUD(db)

    async def get_books(self):
        return await self.book_service.get_books()

    async def get_book_by_id(self, book_id: int):
        if not (
            book_db := await self.book_service.get_book_by_field(
                field="id", data=book_id
            )
        ):
            raise utils.AppException.BookGet(context={"id": book_id})
        return book_db

    async def create_book(self, book: schemas.BookCreate):
        if not (book_db := await self.book_service.create_book(book)):
            raise utils.AppException.BookAlreadyExists(context={"title": book.title})
        return book_db

    # def update_book(
    #     self, book_id: int, book: schemas.BookCreate
    # ) -> utils.ServiceResult:
    #     book_by_id = crud.BookCRUD(self.db).get_book_by_id(book_id)
    #     book_by_title = crud.BookCRUD(self.db).get_book_by_title(book.title)
    #     if not book_by_id:
    #         return self.create_book(book)
    #     if book_by_title is not None and book_by_id.id != book_by_title.id:
    #         return utils.ServiceResult(
    #             utils.AppException.BookUpdate(
    #                 context={
    #                     "message": f"Id mismatch! Book with title: "
    #                     f"{book_by_title.title} has id: {book_by_title.id}, not {book_id}"
    #                 }
    #             )
    #         )
    #     if not (book_db := crud.BookCRUD(self.db).update_book(book_id, book)):
    #         return utils.ServiceResult(utils.AppException.BookUpdate())
    #     return utils.ServiceResult(book_db)
    #
    # def delete_book(self, book_id: int) -> utils.ServiceResult:
    #     if crud.BookCRUD(self.db).delete_book(book_id):
    #         return utils.ServiceResult(
    #             utils.AppException.BookGet(context={"id": book_id})
    #         )
    #     return utils.ServiceResult("Success!")
    #
    # def delete_book_tags(self, book_id: int, tag_id: int) -> utils.ServiceResult:
    #     if crud.BookCRUD(self.db).delete_book_tags(book_id, tag_id):
    #         return utils.ServiceResult(utils.AppException.BookTagDoesNotExist())
    #     return utils.ServiceResult("Success!")
