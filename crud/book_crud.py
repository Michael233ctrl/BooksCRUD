from sqlalchemy.orm import joinedload
from sqlalchemy import update

import models
import schemas
import utils
from .tag_crud import TagCRUD


class BookCRUD(utils.AppCRUD):
    def get_books(self):
        return self.db.query(models.Book).options(joinedload(models.Book.tags)).all()

    def get_book_by_id(self, book_id: int):
        return (
            self.db.query(models.Book)
            .where(models.Book.id == book_id)
            .options(joinedload(models.Book.tags))
            .one_or_none()
        )

    def get_book_by_title(self, title: str):
        return self.db.query(models.Book).where(models.Book.title == title).first()

    def create_book(self, book):
        tags = [TagCRUD(self.db).get_or_create_tag(tag.name) for tag in book.tags]
        db_book = models.Book(
            title=book.title,
            publisher=book.publisher,
            author=book.author,
            pages=book.pages,
            tags=tags,
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def update_book(self, book_id: int, book: schemas.BookCreate):
        self.db.execute(
            update(models.Book)
            .where(models.Book.id == book_id)
            .values(
                title=book.title,
                publisher=book.publisher,
                author=book.author,
                pages=book.pages,
            )
        )
        tags = [TagCRUD(self.db).get_or_create_tag(tag.name) for tag in book.tags]
        db_book = self.get_book_by_id(book_id)
        db_book.tags.extend(tags)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id):
        db_book = self.get_book_by_id(book_id)
        if db_book is None:
            return True
        self.db.delete(db_book)
        self.db.commit()
