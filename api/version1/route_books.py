from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.version1.route_login import get_token
from crud import crud_books, crud_tags
from db.session import get_db
from errors.app_error import BookNotFoundError, BookAlreadyExistError
from schemas.book import BookSchema, BookCreate, TagRequestBody

router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/", response_model=list[BookSchema], status_code=status.HTTP_200_OK)
def read_books(db: Session = Depends(get_db)):
    return crud_books.get_books(db)


@router.get("/{book_id}", response_model=BookSchema, status_code=status.HTTP_200_OK)
def read_books_by_id(book_id: int, db: Session = Depends(get_db)):
    book = crud_books.get_book_by_id(db, book_id)
    if book is None:
        raise BookNotFoundError()
    return book


@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_books(book: BookCreate, db: Session = Depends(get_db)):
    book = crud_books.create_book(db, book)
    if book is None:
        raise BookAlreadyExistError()
    return book


@router.put("/{book_id}", response_model=BookSchema, status_code=status.HTTP_200_OK)
def update_books(book_data: BookCreate, book_id: int, db: Session = Depends(get_db)):
    book = crud_books.update_book(db, book_id=book_id, book=book_data)
    if book is None:
        raise BookAlreadyExistError()
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(book_id: int, db: Session = Depends(get_db)):
    book = crud_books.delete_book(db, book_id=book_id)
    if book is None:
        raise BookNotFoundError()
    return book
