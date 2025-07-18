from pydantic import BaseModel, EmailStr


class UsersShema(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginShema(BaseModel):
    username: str
    password: str