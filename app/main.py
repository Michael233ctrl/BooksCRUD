from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud import crud
from db.session import engine, SessionLocal
from db.base import Base

Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_books_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_books(book_data: schemas.BookCreate, book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db, db_book=db_book, book=book_data)


@app.delete("/books/{book_id}")
def delete_books(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, db_book=db_book)
    return {"message": "OK"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
