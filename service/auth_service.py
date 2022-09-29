from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

import schemas
import utils
from core.config import settings


class AuthService:
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = settings.SECRET_KEY
    algorithm = settings.ALGORITHM

    async def verify_password(self, plain_password, hashed_password):
        if not self.hasher.verify(plain_password, hashed_password):
            return utils.ServiceResult(
                utils.AppException.UserUnauthorized(
                    context={"message": "Incorrect password or username"}
                )
            )

    async def get_password_hash(self, password):
        return self.hasher.hash(password)

    async def encode_token(
        self,
        username: str,
        scope: str,
        expires_delta: Optional[timedelta],
    ):
        payload = {
            "exp": datetime.utcnow() + expires_delta,
            "iat": datetime.utcnow(),
            "scope": scope,
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    async def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return schemas.TokenPayload(**payload)
        except (JWTError, ValidationError):
            return utils.ServiceResult(
                utils.AppException.TokenExpiredError(
                    context={"message": "Could not validate credentials"}
                )
            )

    async def create_token(self, username: str):
        access_token = await self.encode_token(
            username=username,
            scope="access_token",
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = await self.encode_token(
            username=username,
            scope="refresh_token",
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
