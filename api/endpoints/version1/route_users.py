from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from sqlalchemy.orm import Session

import schemas
import service
from db.session import get_db
from api.deps import get_token
from utils.service_result import handle_result

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/", response_model=list[schemas.ShowUser])
def get_users(db: Session = Depends(get_db), token: str = Depends(get_token)):
    return handle_result(result=service.UserService(db).get_users())


@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return handle_result(result=service.UserService(db).create_user(user))


@router.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return handle_result(
        result=service.UserService(db).authenticate_user(
            form_data.username, form_data.password
        )
    )
