import jwt
from datetime import timezone, timedelta, datetime

from pwdlib import PasswordHash

from src.config import settings
from src.exeptions import UsersPasswordNotExistException, IncorrectPasswordException, IncorrectTokenException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthServices(BaseService):
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException


    # регистрация пользователя
    async def users_register(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_data_user = UserAdd(email=data.email, hashed_password=hashed_password)
        await self.db.users.add(new_data_user)
        await self.db.commit()


    async def user_login(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UsersPasswordNotExistException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})  # из  pydentic схемы
        return access_token

    async def get_one_or_none(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)

