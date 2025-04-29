from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, text, UUID, String
import enum
from typing import Annotated, TypeAlias
from datetime import datetime, UTC


intpk = Annotated[int, mapped_column(primary_key=True)]
uuidpk = Annotated[UUID, mapped_column(primary_key=True)]

created_datetime = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_datetime = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now(UTC))]  # todo: попробовать через триггеры субд

ALLOWED_STRING_LENGTHS = {256}  # добавлять новые ограничения для строк


def str_n(n: int) -> TypeAlias:
    """ Вспомогательная функция для создания аннотаций ограничения строк """
    if n not in ALLOWED_STRING_LENGTHS:
        raise ValueError(f"str_n({n}) не разрешён. Разрешённые длины: {sorted(ALLOWED_STRING_LENGTHS)}")
    return Annotated[str, n]


class Base(DeclarativeBase):
    type_annotation_map = {str_n: String(length) for length in ALLOWED_STRING_LENGTHS}


class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    username: Mapped[str]
    created_at: Mapped[created_datetime]


class TreesOrm(Base):
    __tablename__ = "trees"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None]
    created_at: Mapped[created_datetime]
    updated_at: Mapped[updated_datetime]


class CharacterType(enum.Enum):
    human = "human"
    alien = "alien"
    vampire = "vampire"


class CharactersOrm(Base):
    __tablename__ = "characters"
    id: Mapped[intpk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    character_type: Mapped[CharacterType]
