from pydantic import BaseModel, Field
from pydantic import EmailStr


class UserCreate(BaseModel):
    username: str = Field(description="Username")
    email: EmailStr = Field(description="User email")
    password: str = Field(description="User password", min_length=4)


class ShowUser(BaseModel):
    username: str = Field(description="Username")
    email: EmailStr = Field(description="User email")
    is_active: bool = Field(default=True)

    class Config:
        orm_mode = True
