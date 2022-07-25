from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from sqlalchemy.orm import Session

from schemas import ShowUser, UserCreate, Token
from service import UserService
from db.session import get_db
from api.deps import get_token
from utils.service_result import handle_result

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/", response_model=list[ShowUser])
def get_users(db: Session = Depends(get_db), token: str = Depends(get_token)):
    return handle_result(result=UserService(db).get_users())


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return handle_result(result=UserService(db).create_user(user))


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return handle_result(
        result=UserService(db).authenticate_user(form_data.username, form_data.password)
    )
