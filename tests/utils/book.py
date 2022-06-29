from models.book import Book


def create_book(db_session) -> Book:
    book = {
        "title": "CREATE TEST BOOK",
        "publisher": "O'Reilly Media",
        "author": "Mark Lutz",
        "pages": "1",
        "tags": ["Python", "Development", "Learning", 2009]
    }
    db_book = Book(**book)
    db_session.add(db_book)
    db_session.commit()
    db_session.refresh(db_book)
    return db_book
