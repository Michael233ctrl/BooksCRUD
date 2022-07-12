from fastapi import APIRouter
from fastapi import Depends
from starlette import status
from sqlalchemy.orm import Session

from api.version1.route_login import get_token
from db.session import get_db
from crud import crud_user
from schemas.user import ShowUser, UserCreate

router = APIRouter()


@router.get("/", response_model=list[ShowUser])
def get_user(db: Session = Depends(get_db), token: str = Depends(get_token)):
    return crud_user.get_users(db=db)


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_new_user(user=user, db=db)
