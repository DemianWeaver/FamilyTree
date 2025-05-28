from fastapi import APIRouter, HTTPException, Security, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.schemas.tree_schemas import NewTreeSchema
from app.models.models import TreesOrm, UsersOrm
from app.db.database import AsyncSessionDep
from app.services.auth import get_current_user
from app.services.trees import get_tree_by_uuid

tree_router = APIRouter()
tree_tag = "Tree 🌳"


@tree_router.post("/trees", tags=[tree_tag], summary="Добавить дерево")
async def add_tree(tree_data: NewTreeSchema, session: AsyncSessionDep, cur_user: UsersOrm = Security(get_current_user)):
    new_tree = TreesOrm(
        user_id=cur_user.id,
        title=tree_data.title,
        description=tree_data.description
    )
    session.add(new_tree)
    try:
        await session.flush()
        tree_uuid = new_tree.id
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Ошибка при создании дерева")

    return {"success": True, "treeID": tree_uuid}


@tree_router.get("/trees", tags=[tree_tag], summary="Показать все деревья текущего пользователя")
async def get_trees(session: AsyncSessionDep, cur_user: UsersOrm = Security(get_current_user)):
    query = select(TreesOrm).where(TreesOrm.user_id == cur_user.id)
    trees = (await session.execute(query)).scalars().all()
    return trees


@tree_router.get("/trees/{tree_id}", tags=[tree_tag], summary="Показать выбранное дерево")
async def get_tree(tree: TreesOrm = Depends(get_tree_by_uuid)):
    return tree
