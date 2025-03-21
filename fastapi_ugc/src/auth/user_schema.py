from typing import List

from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    exp: int
    is_admin: bool
    login: str
    roles: List[str]


class HTTPAuthorizationCredentials(BaseModel):
    token: str
