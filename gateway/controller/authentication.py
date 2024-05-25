from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Annotated

from gateway.functions.authentication import hash_password, verify_password, create_access_token, get_active_user
from gateway.functions.validate import validate_password
from schema import user
from database.model.setup import get_db
from database.sql.user import UserRepoImplementation
from database.interfaces.data import UserRepositoryInterface

auth_router = APIRouter()


@auth_router.post("/user", response_model=user.User)
def create_user(u: user.UserCreate, db: Session = Depends(get_db)):
    r: UserRepositoryInterface = UserRepoImplementation()
    db_user = r.fetch_user_by_email(db, u.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # check whatever password restrictions
    ok, msg = validate_password(u.password)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    u.password = hash_password(u.password)
    return r.create_user(db, u)


@auth_router.post("/login")
def login(email: Annotated[str, Body()], password: Annotated[str, Body()], db: Session = Depends(get_db)):
    r: UserRepositoryInterface = UserRepoImplementation()
    db_user = r.fetch_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email not registered")

    correct = verify_password(password, db_user.password)
    if not correct:
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": db_user.email})
    return user.Token(access_token=token, token_type="Bearer")


@auth_router.get("/restricted", response_model=user.User)
def test(current_user: Annotated[user.User, Depends(get_active_user)]):
    return current_user
