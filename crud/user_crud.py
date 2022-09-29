from typing import List, Union

from sqlalchemy import or_
from sqlalchemy.future import select

from core.hashing import Hasher
import utils
import schemas
import models


class UserCRUD(utils.AppCRUD):
    async def get_users(self) -> List[models.User]:
        users = await self.db.execute(select(models.User))
        return users.scalars().all()

    async def get_user_by_field(self, field: str, data: Union[str, int]) -> models.User:
        if hasattr(models.User, field):
            user = await self.db.execute(
                select(models.User).where(getattr(models.User, field) == data)
            )
            return user.scalars().one_or_none()
        else:
            raise AttributeError(f"User model has no attribute {field}")

    async def _check_existing_user(self, email: str, username: str):
        user = await self.db.execute(
            select(models.User).where(
                or_(models.User.email == email, models.User.username == username)
            )
        )
        return user.scalars().one_or_none()

    async def create_user(self, user: schemas.UserCreate) -> Union[models.User, None]:
        if await self._check_existing_user(user.email, user.username):
            return None

        hashed_password = await Hasher.get_password_hash(user.password)
        user_db = models.User(
            **user.dict(exclude={"password"}), hashed_password=hashed_password
        )
        self.db.add(user_db)
        await self.db.commit()
        await self.db.refresh(user_db)
        return user_db
