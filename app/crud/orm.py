from app.models.models import Base, CharactersOrm, UsersOrm, SpeciesOrm
from app.db.database import sync_engine, async_engine, sync_session_factory, async_session_factory
from sqlalchemy import select


class SyncOrm:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def sync_insert_char():
        with sync_session_factory() as session:
            tmp_chars = [
                CharactersOrm(first_name="Ivan", last_name="Ivanov"),
                CharactersOrm(first_name="Petr", last_name="Petrov")
            ]
            session.add_all(tmp_chars)
            session.commit()

    @staticmethod
    def sync_insert_defaults():
        default_species = [
            SpeciesOrm(title="human", icon="", is_default=True),
            SpeciesOrm(title="alien", icon="", is_default=False),
            SpeciesOrm(title="vampire", icon="", is_default=False),
        ]
        with sync_session_factory() as session:
            session.add_all(default_species)
            session.commit()

    @staticmethod
    def sync_insert_user():
        with sync_session_factory() as session:
            tmp_users = [
                UsersOrm(username="Ivan"),
                UsersOrm(username="Petr"),
            ]
            session.add_all(tmp_users)
            session.commit()

    @staticmethod
    def sync_get_user():
        with sync_session_factory() as session:
            # user = session.get(UsersOrm, 1)  # 1 объект
            query = select(UsersOrm)
            result = session.execute(query).scalars().all()
            print(f"{result=}")

    @staticmethod
    def sync_update_user(user_id: int = 1, new_username: str = "Michael"):
        with sync_session_factory() as session:
            user = session.get(UsersOrm, user_id)
            user.username = new_username
            session.commit()


class AsyncOrm:
    @staticmethod
    async def setup_database():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def async_insert_char():
        async with async_session_factory() as session:
            tmp_chars = [
                CharactersOrm(first_name="Ivan", last_name="Ivanov"),
                CharactersOrm(first_name="Petr", last_name="Petrov")
            ]
            session.add_all(tmp_chars)
            await session.commit()
