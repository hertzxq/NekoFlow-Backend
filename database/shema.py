from pydantic import BaseModel


class UsersShema(BaseModel):
    username: str
    password: str