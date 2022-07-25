from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


async def get_token(token: str = Depends(oauth2_scheme)):
    if not token:
        return utils.ServiceResult(utils.AppException.UserUnauthorized())
