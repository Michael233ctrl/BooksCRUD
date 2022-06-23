from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import schemas
from api.version1.route_login import get_token
from crud import crud_books
from db.session import get_db

router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_books.get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=schemas.Book)
def read_books_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud_books.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/", response_model=schemas.Book, status_code=201)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud_books.create_book(db, book)


@router.put("/{book_id}", response_model=schemas.Book)
def update_books(book_data: schemas.BookCreate, book_id: int, db: Session = Depends(get_db)):
    db_book = crud_books.get_book_by_id(db, book_id)
    if db_book is None:
        return create_books(book=book_data, db=db)
    return crud_books.update_book(db, db_book=db_book, book=book_data)


@router.delete("/{book_id}")
def delete_books(book_id: int, db: Session = Depends(get_db)):
    db_book = crud_books.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud_books.delete_book(db, db_book=db_book)
    return {"message": "OK"}
