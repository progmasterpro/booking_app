from pydantic import BaseModel, EmailStr, ConfigDict


class UserRequestAdd(BaseModel): # schema route
    email: EmailStr
    password: str


class UserAdd(BaseModel): # add in DB
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)



class UserWithHashedPassword(User):
    hashed_password: str