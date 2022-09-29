from typing import Optional, Union

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description="Token access")
    refresh_token: str = Field(description="Token refresh")
    token_type: str = Field(description="Token type")


class TokenPayload(BaseModel):
    sub: Optional[Union[str, int]]
