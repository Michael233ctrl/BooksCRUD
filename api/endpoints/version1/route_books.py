from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from api.deps import get_token
from db.session import get_db
from schemas.book import BookSchema, BookCreate, TagRequestBody
from service import BookService
from utils.service_result import handle_result


router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/", response_model=list[BookSchema], status_code=status.HTTP_200_OK)
def read_books(db: Session = Depends(get_db)):
    return handle_result(result=BookService(db).get_books())


@router.get("/{book_id}", response_model=BookSchema, status_code=status.HTTP_200_OK)
def read_books_by_id(book_id: int, db: Session = Depends(get_db)):
    return handle_result(result=BookService(db).get_book_by_id(book_id))


@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_books(book: BookCreate, db: Session = Depends(get_db)):
    return handle_result(result=BookService(db).create_book(book))


@router.put("/{book_id}", response_model=BookSchema, status_code=status.HTTP_200_OK)
def update_books(book: BookCreate, book_id: int, db: Session = Depends(get_db)):
    return handle_result(result=BookService(db).update_book(book_id, book))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(book_id: int, db: Session = Depends(get_db)):
    return handle_result(result=BookService(db).delete_book(book_id))


@router.delete("/{book_id}/tags/", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_tags(
    request_body: TagRequestBody, book_id: int, db: Session = Depends(get_db)
):
    return handle_result(
        result=BookService(db).delete_book_tags(book_id, request_body.tagId)
    )
