from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.interfaces.data import GroupRepositoryInterface
from database.model.setup import get_db
from database.sql.user import GroupRepoImplementation
from gateway.functions.authentication import get_active_user
from schema import user
from schema.user import Group, GroupBase

group_router = APIRouter(prefix="/groups", tags=["groups"])


@group_router.get("/", response_model=List[Group])
def get_groups(current_user: Annotated[user.User, Depends(get_active_user)], db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    r: GroupRepositoryInterface = GroupRepoImplementation()
    groups = r.fetch_all_groups(db)
    return groups


@group_router.post("/", response_model=Group)
def create_group(group: GroupBase, current_user: Annotated[user.User, Depends(get_active_user)], db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    r: GroupRepositoryInterface = GroupRepoImplementation()
    group_exists = r.check_group_name_exist(db, group.name)
    if group_exists:
        raise HTTPException(status_code=400, detail="Group name already exists")

    group = r.create_group(db, group, current_user.id)
    if group is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create group")
    return group


@group_router.get("/search", response_model=List[Group] | None)
def get_group(query: str, db: Session = Depends(get_db)):
    r: GroupRepositoryInterface = GroupRepoImplementation()
    groups = r.fetch_groups_by_name(db, query)
    return groups
