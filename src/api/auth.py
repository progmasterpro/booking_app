from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exeptions import ObjectAlreadyExistException, EmailAlreadyExistException, EmailAlreadyExistHTTPException, \
    ObjectAlreadyExistHTTPException, UsersPasswordNotExistException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def users_register(
    data: UserRequestAdd,
    db: DBDep
):
    try:
        await AuthServices(db).users_register(data)
    except EmailAlreadyExistException:
        raise EmailAlreadyExistHTTPException
    except ObjectAlreadyExistException:
        raise ObjectAlreadyExistHTTPException
    return {"status": "ok"}


@router.post("/login", summary="Логин")
async def user_login(
        db: DBDep,
        data: UserRequestAdd,
        response: Response,
):
    try:
        access_token = await AuthServices(db).user_login(data)
    except UsersPasswordNotExistException:
        raise UsersPasswordNotExistException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получение текущего пользователя")
async def get_me(
        db: DBDep,
        user_id: UserIdDep,
):
    return await AuthServices(db).get_one_or_none(user_id)


@router.post("/logout", summary="Выход пользователя")
async def user_logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}



