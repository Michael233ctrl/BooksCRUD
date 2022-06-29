from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from errors.app_error import BookNotFoundError, BookAlreadyExistError
from models.book import Book
import schemas


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise BookNotFoundError()
    return db_book


def create_book(db: Session, book: schemas.BookCreate):
    db_book = Book(**book.dict())
    try:
        db.add(db_book)
        db.commit()
    except IntegrityError:
        raise BookAlreadyExistError()
    else:
        db.refresh(db_book)
        return db_book


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    try:
        db_book = get_book_by_id(db, book_id)
    except BookNotFoundError:
        return create_book(db, book)
    else:
        db.execute(update(Book).where(Book.id == db_book.id).values(**book.dict()))
        db.commit()
        db.refresh(db_book)
        return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    db.delete(db_book)
    db.commit()
