from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description="Token")
    token_type: str = Field(description="Token type")
