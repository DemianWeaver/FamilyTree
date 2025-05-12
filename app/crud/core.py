from sqlalchemy import select, insert, update
from app.db.database import sync_engine
from app.models.tables import metadata_obj, users_table


class SyncCore:
    @staticmethod
    def create_tables():
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)

    @staticmethod
    def sync_insert_users():
        tmp_users = [
                    {"username": "Ivan"},
                    {"username": "Petr"},
        ]
        with sync_engine.connect() as conn:
            smtm = insert(users_table).values(tmp_users)
            conn.execute(smtm)
            conn.commit()

    @staticmethod
    def sync_get_users():
        with sync_engine.connect() as conn:
            query = select(users_table)
            result = conn.execute(query).all()
            print(f"{result=}")

    @staticmethod
    def sync_update_user(user_id: int = 1, new_username: str = "Michael"):
        with sync_engine.connect() as conn:
            # сырым запросом
            # stmt = text("update users set username=:name where id=:id")
            # stmt = stmt.bindparams(name=new_username, id=user_id)
            stmt = (
                update(users_table)
                .values(username=new_username)
                .filter_by(id=user_id)
            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:
    pass
