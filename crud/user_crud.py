from core.hashing import Hasher

import utils
import schemas
import models


class UserCRUD(utils.AppCRUD):
    def get_users(self):
        return self.db.query(models.User).all()

    def get_user(self, username: str):
        return (
            self.db.query(models.User)
            .where(models.User.username == username)
            .one_or_none()
        )

    def create_user(self, user: schemas.UserCreate):
        user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            is_active=True,
            is_superuser=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
