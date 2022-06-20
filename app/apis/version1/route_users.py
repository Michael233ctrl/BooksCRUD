from crud.crud_user import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from schemas.user import ShowUser
from schemas.user import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user=user, db=db)

