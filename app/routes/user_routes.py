from fastapi import APIRouter, Security

from app.models.models import UsersOrm
from app.schemas.user_schemas import PublicUserSchema
from app.services.auth import get_current_user

user_router = APIRouter()
user_tag = "User 👤"


@user_router.get("/profile", response_model=PublicUserSchema, tags=[user_tag], summary="Профиль пользователя")
async def get_profile(cur_user: UsersOrm = Security(get_current_user)):
    return cur_user
