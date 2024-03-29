from crud.tag_crud import TagCRUD
from models.book import Book
from schemas import TagCreate, BookCreate


def create_book(db_session) -> Book:
    book = BookCreate(
        title="CREATE TEST BOOK",
        publisher="O'Reilly Media",
        author="Mark Lutz",
        pages="500",
        tags=[TagCreate(name="python")],
    )
    tags = [TagCRUD(db_session).get_or_create_tag(tag.name) for tag in book.tags]
    db_book = Book(
        title=book.title,
        publisher=book.publisher,
        author=book.author,
        pages=book.pages,
        tags=tags,
    )
    db_session.add(db_book)
    db_session.commit()
    db_session.refresh(db_book)
    return db_book
