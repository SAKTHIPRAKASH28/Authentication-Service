from pydantic import BaseModel, Field, validator
import regex as re
import datetime


class UserModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    password: str = Field(...)

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', value):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValueError(
                "Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise ValueError(
                "Password must contain at least one special character")
        return value


class TokenPayload(BaseModel):
    username: str
    exp: datetime.datetime
