from fastapi import Query, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated

from src.database import async_session_maker
from src.services.auth import AuthServices
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, lt=40)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен")
    return token

def get_current_user_id(token: str = Depends(get_token)):
    data = AuthServices().decode_jwt(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]