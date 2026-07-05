from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersModel
from src.repositories.base import BaseRepositories
from src.repositories.mappers.mappers import UsersDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepositories(BaseRepositories):
    model = UsersModel
    mapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)