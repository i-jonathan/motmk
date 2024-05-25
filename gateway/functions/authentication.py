from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from typing import Any, Annotated
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy.orm import Session

from config.config import setting
from database.model.setup import get_db
from schema.user import TokenData
from database.sql.user import UserRepoImplementation
from database.model.user_data import User


password_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    return password_context.verify(plain_pass, hashed_pass)


def create_access_token(data: dict[str, Any], duration: timedelta | None = None) -> str:
    if duration is None:
        duration = timedelta(minutes=20)

    expiry_time = datetime.now(timezone.utc) + duration
    jwt_data = data.copy()
    jwt_data.update({"exp": expiry_time})
    return jwt.encode(jwt_data, setting.JWTSecret, setting.JWTAlgo)


async def get_active_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User | None:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, setting.JWTSecret, algorithms=[setting.JWTAlgo])
        email: str = payload.get("sub")
        if email is None:
            raise exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise exception

    user = UserRepoImplementation.fetch_user_by_email(db, token_data.email)
    if user is None:
        raise exception
    return user
