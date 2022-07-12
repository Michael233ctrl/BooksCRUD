from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.version1.route_login import get_token
from crud import crud_tags
from db.session import get_db
from schemas.book import TagRequestBody

router = APIRouter(dependencies=[Depends(get_token)])


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_tags(
    request_body: TagRequestBody, book_id: int, db: Session = Depends(get_db)
):
    book_tag = crud_tags.delete_tag_for_book(db, book_id, request_body.tagId)
    if book_tag is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
