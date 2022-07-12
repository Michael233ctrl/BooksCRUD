from core.hashing import Hasher
from errors.app_error import UserNotFoundError, UserUnauthorizedError
from models.user import User
from schemas.user import UserCreate
from sqlalchemy.orm import Session


def get_users(db: Session):
    return db.query(User).all()


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundError()
    return user


def authenticate_user(username: str, password: str, db: Session):
    try:
        user = get_user(username=username, db=db)
    except UserNotFoundError:
        raise UserUnauthorizedError()
    if not Hasher.verify_password(password, user.hashed_password):
        raise UserUnauthorizedError()
    return user


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
