import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.crud.orm import AsyncOrm
from app.routes.auth_routes import auth_router
from app.routes.user_routes import user_router

app = FastAPI()  # uvicorn app.main:app --reload
app.include_router(auth_router)
app.include_router(user_router)


@app.post("/reload_db", tags=["Reload"], summary="Пересоздать базу данных")
async def reload_db():
    await AsyncOrm.setup_database()
    return {"success": True}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
