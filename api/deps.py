from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

import models
import utils
from db.session import async_session
from service import UserService, AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


async def get_db():
    async with async_session() as session:
        yield session


async def get_token(token: str = Depends(oauth2_scheme)):
    if not token:
        return utils.ServiceResult(utils.AppException.UserUnauthorized())


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> models.User:
    token_data = await AuthService().decode_token(token)
    return await UserService(db).get_user(token_data.sub)
