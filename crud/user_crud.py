from core.hashing import Hasher
from models.user import User

import utils
import schemas


class UserCRUD(utils.AppCRUD):
    def get_users(self):
        return self.db.query(User).all()

    def get_user(self, username: str):
        return self.db.query(User).where(User.username == username).one_or_none()

    def create_user(self, user: schemas.UserCreate):
        user = User(
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
