from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


class NewUserSchema(BaseModel):
    username: str
    password: str = Field(min_length=8)


class UserSchema(NewUserSchema):
    id: str  # todo: переделать на uuid если нужно
    created_at: datetime


# class UserSchema(BaseModel):
#     email: EmailStr
#     password: str = Field(min_length=8)
#     username: str
#     age: int = Field(ge=0, le=130)

    # model_config = ConfigDict(extra="forbid")  # запретить получать доп параметры
