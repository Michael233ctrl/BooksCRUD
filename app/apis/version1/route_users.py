from apis.version1.route_login import get_token
from crud import crud_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
import schemas
from schemas.user import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=list[schemas.ShowUser])
def create_user(db: Session = Depends(get_db), token: str = Depends(get_token)):
    return crud_user.get_users(db=db)


@router.post("/", response_model=schemas.ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_new_user(user=user, db=db)
