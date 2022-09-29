from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas import ShowUser, UserCreate, Token, TokenRefresh
from service import UserService, AuthService
from api.deps import get_current_user, get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.get("/", response_model=list[ShowUser], status_code=status.HTTP_200_OK)
async def get_users(
    db: AsyncSession = Depends(get_db), _: str = Depends(get_current_user)
):
    return await UserService(db).get_users()


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService(db).create_user(user)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await UserService(db).authenticate_user(
        form_data.username, form_data.password
    )


@router.post("/refresh-token", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(token: TokenRefresh):
    return await AuthService().refresh_token(token)
