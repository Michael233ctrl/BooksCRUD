import crud
import utils
import schemas
from service.auth_service import AuthService


class UserService(utils.AppService):
    async def get_users(self):
        return await crud.UserCRUD(self.db).get_users()

    async def get_user(self, username: str):
        if not (
            user := await crud.UserCRUD(self.db).get_user_by_field(
                field="username", data=username
            )
        ):
            raise utils.AppException.UserGet(context={"message": "User not found"})
        return user

    async def create_user(self, user: schemas.UserCreate):
        if not (user := await crud.UserCRUD(self.db).create_user(user)):
            raise utils.AppException.UserCreate(
                context={"message": "User with this data already exists"}
            )
        return user

    async def authenticate_user(self, username: str, password: str):
        auth_service = AuthService()
        if not (
            user := await crud.UserCRUD(self.db).get_user_by_field(
                field="username", data=username
            )
        ):
            raise utils.AppException.UserGet(
                context={"message": f"User with username: {username} doesn't exist"}
            )

        await auth_service.verify_password(password, user.hashed_password)
        return await auth_service.create_token(username)
