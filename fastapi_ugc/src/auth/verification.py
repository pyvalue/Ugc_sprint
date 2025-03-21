from typing import Set, Tuple

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from starlette.status import HTTP_403_FORBIDDEN

from settings import settings
from src.auth.bearer import HTTPBearer
from src.auth.user_schema import User, HTTPAuthorizationCredentials

security = HTTPBearer()


def decode_token(token: str) -> User:
    """Токен декодируется."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str('Could not validate credentials'),
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return User.parse_obj(payload)


def get_user(request: Request) -> User:
    """Внедряется в ручку как dependency, чтобы работать с каждой ролью отдельно."""
    return request.state.user


class Access:
    def __init__(self, roles: Set[str]):
        """Список ролей, которым разрешен доступ."""
        self.roles = roles

    def __call__(self, request_user: Tuple[Request, HTTPAuthorizationCredentials] = Depends(security)) -> None:
        """Токен декодируется, в нем проверяются роли."""
        exc = HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Not authenticated',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        request, token = request_user
        user = decode_token(token.token)
        if self.roles not in user.roles and user.is_admin is False:
            raise exc
        request.state.user = user
