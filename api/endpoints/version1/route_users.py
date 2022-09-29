from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas import ShowUser, UserCreate, Token
from service import UserService
from api.deps import get_token, get_db
from utils.service_result import handle_result

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/", response_model=list[ShowUser], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db), _: str = Depends(get_token)):
    return handle_result(result=await UserService(db).get_users())


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return handle_result(result=await UserService(db).create_user(user))


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return handle_result(
        result=await UserService(db).authenticate_user(
            form_data.username, form_data.password
        )
    )
