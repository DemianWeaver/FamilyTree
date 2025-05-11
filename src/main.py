from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config.database import get_async_session
from src.queries.orm import AsyncOrm
from src.config.schemas import NewUserSchema, UserSchema
from src.config.models import UsersOrm

app = FastAPI()  # uvicorn src.main:app --reload
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@app.post("/setup")
async def setup_db():
    await AsyncOrm.setup_database()
    return {"success": True}


@app.post("/users")
async def add_user(data: NewUserSchema, session: SessionDep):
    new_user = UsersOrm(username=data.username, password=data.password)
    session.add(new_user)
    await session.commit()
    return {"success": True}


@app.get("/users")
async def get_users(session: SessionDep):
    query = select(UsersOrm)
    return (await session.execute(query)).scalars().all()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
