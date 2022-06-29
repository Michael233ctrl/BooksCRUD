from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from api.version1.route_login import get_token
from crud import crud_books
from db.session import get_db
import schemas

router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/", response_model=list[schemas.Book], status_code=status.HTTP_200_OK)
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_books.get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=schemas.Book, status_code=status.HTTP_200_OK)
def read_books_by_id(book_id: int, db: Session = Depends(get_db)):
    return crud_books.get_book_by_id(db, book_id)


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud_books.create_book(db, book)


@router.put("/{book_id}", response_model=schemas.Book, status_code=status.HTTP_200_OK)
def update_books(book_data: schemas.BookCreate, book_id: int, db: Session = Depends(get_db)):
    return crud_books.update_book(db, book_id=book_id, book=book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(book_id: int, db: Session = Depends(get_db)):
    return crud_books.delete_book(db, book_id=book_id)
