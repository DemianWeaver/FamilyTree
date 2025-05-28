import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.crud.orm import AsyncOrm
from app.routes import routes

app = FastAPI()  # uvicorn app.main:app --reload
for router in routes:
    app.include_router(router)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.post("/reload_db", tags=["Reload 🔄"], summary="Пересоздать базу данных")
async def reload_db():
    await AsyncOrm.setup_database()
    return {"success": True}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
