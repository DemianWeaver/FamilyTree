from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select

from app.core.config import settings
from app.db.database import AsyncSessionDep
from app.models.models import UsersOrm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign_in/swagger")


async def get_current_user(session: AsyncSessionDep, token: str | None = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials")

    if token is None:
        raise credentials_exception

    try:  # верификация токена todo: вынести в отдельную функцию
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    query = select(UsersOrm).where(UsersOrm.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

