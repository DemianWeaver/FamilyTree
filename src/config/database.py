from sqlalchemy import create_engine, text
from src.config import settings


engine = create_engine(
    url=settings.db_url_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)


with engine.connect() as conn:
    result = conn.execute(text("select version()"))
    print(f"{result=}")
