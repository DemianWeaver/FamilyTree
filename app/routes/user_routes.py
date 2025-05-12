from fastapi import APIRouter, Depends

from app.models.models import UsersOrm
from app.models.schemas import UserSchema
from app.services.auth import get_current_user

user_router = APIRouter()
user_tag = "User"


@user_router.get("/profile", response_model=UserSchema, tags=[user_tag], summary="Профиль пользователя")
async def get_profile(cur_user: UsersOrm = Depends(get_current_user)):
    return cur_user
