from datetime import timedelta

import crud
import utils
import schemas
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token


class UserService(utils.AppService):
    def get_users(self) -> utils.ServiceResult:
        users = crud.UserCRUD(self.db).get_users()
        return utils.ServiceResult(users)

    def create_user(self, user: schemas.UserCreate) -> utils.ServiceResult:
        if not (user := crud.UserCRUD(self.db).create_user(user)):
            return utils.ServiceResult(utils.AppException.UserCreate())
        return utils.ServiceResult(user)

    def authenticate_user(self, username: str, password: str) -> utils.ServiceResult:
        if not (user := crud.UserCRUD(self.db).get_user(username)):
            return utils.ServiceResult(utils.AppException.UserGet())
        if not Hasher.verify_password(password, user.hashed_password):
            return utils.ServiceResult(
                utils.AppException.UserUnauthorized(
                    context={"message": "Incorrect password or username"}
                )
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return utils.ServiceResult(
            {"access_token": access_token, "token_type": "bearer"}
        )
