from typing import List, Union

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import schemas
import models
from crud.base_crud import BaseCRUD
from models import User
from service.auth_service import AuthService


class UserCRUD(BaseCRUD):
    def __init__(self, db: AsyncSession):
        self.model = User
        super().__init__(db, self.model)

    async def get_users(self) -> List[models.User]:
        return await self._get_all_objects()

    async def get_user(self, username: str) -> models.User:
        return await self._get_object_by_field(field="username", data=username)

    async def __check_existing_user(self, email: str, username: str):
        query = await self.db.execute(
            select(self.model).where(
                or_(self.model.email == email, self.model.username == username)
            )
        )
        return query.scalars().one_or_none()

    async def create_user(self, user: schemas.UserCreate) -> Union[models.User, None]:
        if await self.__check_existing_user(user.email, user.username):
            return None

        user.password = await AuthService().get_password_hash(user.password)
        return await self._create(user.dict())
