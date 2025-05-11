import asyncio

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config.config import settings

sync_engine = create_engine(
    url=settings.db_url_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.db_url_asyncpg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_factory() as session:
        yield session
