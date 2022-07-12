from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from crud.crud_tags import get_or_create_tag
from models.book import Book
from schemas.book import BookCreate


def get_books(db: Session):
    return db.query(Book).options(joinedload(Book.tags)).all()


def get_book_by_id(db: Session, book_id: int):
    return (
        db.query(Book)
        .options(joinedload(Book.tags))
        .where(Book.id == book_id)
        .one_or_none()
    )


def get_book_by_title(db: Session, title: str):
    return db.query(Book).where(Book.title == title).first()


def create_book(db: Session, book: BookCreate):
    check_book = get_book_by_title(db, book.title)
    if check_book is not None:
        return None

    tags = [get_or_create_tag(db, tag.name) for tag in book.tags]
    db_book = Book(
        title=book.title,
        publisher=book.publisher,
        author=book.author,
        pages=book.pages,
        tags=tags,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookCreate):
    db_book = get_book_by_id(db, book_id)

    if db_book is None:
        return create_book(db, book)

    db.execute(
        update(Book)
        .where(Book.id == db_book.id)
        .values(
            title=book.title,
            publisher=book.publisher,
            author=book.author,
            pages=book.pages,
        )
    )
    tags = [get_or_create_tag(db, tag.name) for tag in book.tags]
    db_book.tags.extend(tags)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if db_book is None:
        return None
    db.delete(db_book)
    db.commit()
    return "Deleted!"
