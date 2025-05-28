from uuid import UUID
from sqlalchemy import select
from fastapi import Security, HTTPException

from app.db.database import AsyncSessionDep
from app.models.models import UsersOrm, TreesOrm
from app.services.auth import get_current_user


async def get_tree_by_uuid(tree_uuid: UUID, session: AsyncSessionDep, cur_user: UsersOrm = Security(get_current_user)):
    query = select(TreesOrm).where(TreesOrm.id == tree_uuid)
    cur_tree = (await session.execute(query)).scalar_one_or_none()

    if cur_tree is None:
        raise HTTPException(status_code=404, detail="Дерево не найдено")

    if cur_tree.user_id != cur_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому дереву")

    return cur_tree  # todo: привязать к pydantic схеме
