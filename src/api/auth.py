from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def users_register(data: UserRequestAdd):
    try:
        hashed_password = AuthServices().hash_password(data.password)
        new_data_user = UserAdd(email=data.email, hashed_password=hashed_password)
        async with async_session_maker() as session:
            await UsersRepositories(session).add(new_data_user)
            await session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Пользователь с таким Email уже существует")
    return {"status": "ok"}


@router.post("/login")
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


@router.get("/me")
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_one_or_none(id=user_id)
    return user

@router.post("/logout")
async def user_logout(
        response: Response
):
    response.delete_cookie("access_token")
    return {"status": "ok"}



