from typing import Annotated

from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password, create_access_token
from app.db.database import AsyncSessionDep
from app.models.models import UsersOrm
from app.schemas.user_schemas import UserLoginSchema, NewUserSchema

auth_router = APIRouter()
auth_tag = "Auth ✍️️"


@auth_router.post("/sign_up", tags=[auth_tag], summary="Регистрация")
async def sign_up(new_user_data: NewUserSchema, session: AsyncSessionDep):
    new_user = UsersOrm(
        username=new_user_data.username,
        email=new_user_data.email,
        password=hash_password(new_user_data.password),
    )
    session.add(new_user)

    try:
        await session.flush()
        token = create_access_token(data={"sub": str(new_user.id)})
        await session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolationError):
            raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже существует.")
        raise HTTPException(status_code=400, detail="Ошибка при создании пользователя.")

    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/sign_in", tags=[auth_tag], summary="Аутентификация")
async def sign_in(user_data: UserLoginSchema, session: AsyncSessionDep):
    stmt = select(UsersOrm).where(UsersOrm.email == user_data.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/sign_in/swagger", include_in_schema=False)  # скрытая ручка чисто для swagger'а
async def swagger_sign_in(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSessionDep):
    stmt = select(UsersOrm).where(UsersOrm.email == user_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
