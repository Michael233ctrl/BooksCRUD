from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from api.deps import get_token
from db.session import get_db
from service import TagService
from utils.service_result import handle_result
from schemas import TagCreate

router = APIRouter(dependencies=[Depends(get_token)])


@router.get("/")
def read_tags(db: Session = Depends(get_db)):
    return handle_result(result=TagService(db).get_tags())


@router.put("/{tag_id}", response_model=TagCreate, status_code=status.HTTP_200_OK)
def update_tags(tag: TagCreate, tag_id: int, db: Session = Depends(get_db)):
    return handle_result(result=TagService(db).update_tag(tag_id, tag))


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tags(tag_id: int, db: Session = Depends(get_db)):
    return handle_result(result=TagService(db).delete_tag(tag_id))
