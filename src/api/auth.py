from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.exeptions import ObjectAlreadyExistException, EmailAlreadyExistException, EmailAlreadyExistHTTPException, \
    ObjectAlreadyExistHTTPException
from src.repositories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd
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
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Пользователь с таким паролем не зарегистрирован')
        if not AuthServices().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Пароль не верный')
        access_token = AuthServices().create_access_token({"user_id": user.id})  # из  pydentic схемы
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me", summary="Получение текущего пользователя")
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_one_or_none(id=user_id)
    return user

@router.post("/logout", summary="Выход пользователя")
async def user_logout(
        response: Response
):
    response.delete_cookie("access_token")
    return {"status": "ok"}



