import enum
from datetime import datetime, UTC
from typing import Annotated, TypeAlias
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, text, String
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]
uuidpk = Annotated[UUID, mapped_column(UUID_PG(as_uuid=True), primary_key=True, default=uuid4)]

created_datetime = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_datetime = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now(UTC))]  # todo: попробовать через триггеры субд

ALLOWED_STRING_LENGTHS = {8, 16, 256}  # добавлять новые ограничения для строк


def str_n(n: int) -> TypeAlias:
    """ Вспомогательная функция для создания аннотаций ограничения строк """
    if n not in ALLOWED_STRING_LENGTHS:
        raise ValueError(f"str_n({n}) не разрешён. Разрешённые длины: {sorted(ALLOWED_STRING_LENGTHS)}")
    return Annotated[str, n]


class Base(DeclarativeBase):
    type_annotation_map = {str_n: String(length) for length in ALLOWED_STRING_LENGTHS}


class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[uuidpk]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[created_datetime]

    trees: Mapped[list["TreesOrm"]] = relationship(back_populates="user")


class TreesOrm(Base):
    __tablename__ = "trees"
    id: Mapped[uuidpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str_n(16)]
    description: Mapped[str | None]  # todo: указать максимальный размер
    created_at: Mapped[created_datetime]
    updated_at: Mapped[updated_datetime]

    user: Mapped["UsersOrm"] = relationship(back_populates="trees")


class SpeciesOrm(Base):
    __tablename__ = "species"
    id: Mapped[intpk]
    title: Mapped[str_n(8)]
    icon: Mapped[str]  # todo: заменить на нужный тип
    is_default: Mapped[bool] = mapped_column(default=False, server_default=text("FALSE"))


class CharactersOrm(Base):
    __tablename__ = "characters"
    id: Mapped[uuidpk]
    tree_id: Mapped[int] = mapped_column(ForeignKey("trees.id", ondelete="CASCADE"))
    first_name: Mapped[str_n(16)]
    last_name: Mapped[str_n(16)]
    biography: Mapped[str | None]  # todo: указать максимальный размер
    image: Mapped[str | None]  # todo: заменить на нужный тип
    # перед добавлением персонажа, если species_id=null поместить элемент с is_default=True
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))


class GamesEnum(enum.Enum):
    sims3 = "The Sims 3"
    sims4 = "The Sims 4"


class TraitsOrm(Base):
    __tablename__ = "traits"
    id: Mapped[intpk]
    title: Mapped[str_n(8)]
    icon: Mapped[str]  # todo: заменить на нужный тип
    description: Mapped[str]  # todo: указать максимальный размер
    game: Mapped[GamesEnum]


class RelationshipTypesEnum(enum.Enum):
    peer = "peer"
    up = "up"
    down = "down"


class RelationshipsOrm(Base):
    __tablename__ = "relationships"
    id: Mapped[intpk]
    inverse_relationship_id: Mapped[int | None] = mapped_column(ForeignKey("relationships.id"))
    title: Mapped[str_n(8)]
    type: Mapped[RelationshipTypesEnum]


class CharacterRelationships(Base):
    __tablename__ = "character_relationships"
    id: Mapped[intpk]
    char_id: Mapped[UUID] = mapped_column(ForeignKey("characters.id"))
    related_char_id: Mapped[UUID] = mapped_column(ForeignKey("characters.id"))
    relationship_id: Mapped[int] = mapped_column(ForeignKey("relationships.id"))

