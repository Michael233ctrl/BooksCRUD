import crud
import utils
import schemas
from service.auth_service import AuthService


class UserService(utils.AppService):
    async def get_users(self) -> utils.ServiceResult:
        users = await crud.UserCRUD(self.db).get_users()
        return utils.ServiceResult(users)

    async def get_user(self, username: str):
        if not (
            user := await crud.UserCRUD(self.db).get_user_by_field(
                field="username", data=username
            )
        ):
            return utils.ServiceResult(
                utils.AppException.UserGet(context={"message": "User not found"})
            )
        return user

    async def create_user(self, user: schemas.UserCreate) -> utils.ServiceResult:
        if not (user := await crud.UserCRUD(self.db).create_user(user)):
            return utils.ServiceResult(
                utils.AppException.UserCreate(
                    context={"message": "User with this data already exists"}
                )
            )
        return utils.ServiceResult(user)

    async def authenticate_user(
        self, username: str, password: str
    ) -> utils.ServiceResult:
        auth_service = AuthService()
        if not (
            user := await crud.UserCRUD(self.db).get_user_by_field(
                field="username", data=username
            )
        ):
            return utils.ServiceResult(
                utils.AppException.UserGet(
                    context={"message": f"User with username: {username} doesn't exist"}
                )
            )
        await auth_service.verify_password(password, user.hashed_password)
        return utils.ServiceResult(await auth_service.create_token(username))
