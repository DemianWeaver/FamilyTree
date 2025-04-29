from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, text, TIMESTAMP, Enum
from datetime import datetime, UTC
import enum

created_datetime = text("TIMEZONE('utc', now())")

metadata_obj = MetaData()

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("created_at", TIMESTAMP, server_default=created_datetime)

)

trees_table = Table(
    "trees",
    metadata_obj,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("title", String),
    Column("description", String, nullable=True),
    Column("created_at", TIMESTAMP, server_default=created_datetime),
    Column("updated_at", TIMESTAMP, server_default=created_datetime, onupdate=datetime.now(UTC)),
)


class CharacterType(enum.Enum):
    human = "human"
    alien = "alien"
    vampire = "vampire"


characters_table = Table(
    "characters",
    metadata_obj,
    Column("first_name", String),
    Column("last_name", String),
    Column("character_type", Enum(CharacterType))
)

