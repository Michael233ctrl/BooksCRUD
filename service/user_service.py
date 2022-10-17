from sqlalchemy.ext.asyncio import AsyncSession

import crud
import utils
import schemas
from service.auth_service import AuthService


class UserService(utils.AppService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.user_crud = crud.UserCRUD(db)

    async def get_users(self):
        return await self.user_crud.get_users()

    async def get_user(self, username: str):
        if not (user := await self.user_crud.get_user(username)):
            raise utils.AppException.UserGet(context={"message": "User not found"})
        return user

    async def create_user(self, user: schemas.UserCreate):
        if not (user := await self.user_crud.create_user(user)):
            raise utils.AppException.UserCreate(
                context={"message": "User with this data already exists"}
            )
        return user

    async def authenticate_user(self, username: str, password: str):
        auth_service = AuthService()
        if not (user := await self.user_crud.get_user(username)):
            raise utils.AppException.UserGet(
                context={"message": f"User with username: {username} doesn't exist"}
            )
        await auth_service.verify_password(password, user.password)
        return await auth_service.create_token(username)
