from pydantic import BaseModel


class UsersCheckSchema(BaseModel):
    users: list
