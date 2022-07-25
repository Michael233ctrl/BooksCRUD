from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from api.deps import get_token
from db.session import get_db
from schemas.book import TagRequestBody
from service import TagService
from utils.service_result import handle_result

router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/")
def read_tags(db: Session = Depends(get_db)):
    return handle_result(result=TagService(db).get_tags())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_tags(
    request_body: TagRequestBody, book_id: int, db: Session = Depends(get_db)
):
    return handle_result(
        result=TagService(db).delete_tag_for_book(book_id, request_body.tagId)
    )
