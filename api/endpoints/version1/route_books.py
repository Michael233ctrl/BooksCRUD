from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.deps import get_db, get_current_user
from schemas.book import BookSchema, BookCreate, BookUpdate
from service import BookService


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=List[BookSchema], status_code=status.HTTP_200_OK)
async def read_books(db: AsyncSession = Depends(get_db)):
    return await BookService(db).get_books()


@router.get("/{book_id}", response_model=BookSchema, status_code=status.HTTP_200_OK)
async def read_books_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    return await BookService(db).get_book_by_id(book_id)


@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def create_books(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await BookService(db).create_book(book)


@router.put("/{book_id}", response_model=BookSchema, status_code=status.HTTP_200_OK)
async def update_books(
    book: BookUpdate, book_id: int, db: AsyncSession = Depends(get_db)
):
    return await BookService(db).update_book(book_id, book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_books(book_id: int, db: AsyncSession = Depends(get_db)):
    return await BookService(db).delete_book(book_id)


# @router.delete("/{book_id}/tags/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book_tags(
#     request_body: TagRequestBody, book_id: int, db: AsyncSession = Depends(get_db)
# ):
#     return await BookService(db).delete_book_tags(book_id, request_body.tagId)
