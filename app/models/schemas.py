from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    """ Для аутентификации пользователя """
    email: EmailStr
    password: str = Field(min_length=8)


class NewUserSchema(UserLoginSchema):
    username: str


class UserSchema(NewUserSchema):
    id: UUID
    created_at: datetime




# class UserSchema(BaseModel):
#     email: EmailStr
#     password: str = Field(min_length=8)
#     username: str
#     age: int = Field(ge=0, le=130)

    # model_config = ConfigDict(extra="forbid")  # запретить получать доп параметры
