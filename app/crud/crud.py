from sqlalchemy import update
from sqlalchemy.orm import Session
from models.book import Book
import schemas


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, db_book: Book, book: schemas.BookCreate):
    db.execute(update(Book).where(Book.id == db_book.id).values(**book.dict()))
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, db_book: Book):
    db.delete(db_book)
    db.commit()
