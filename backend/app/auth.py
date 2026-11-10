import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.database import get_active_engine, users
from app.roles import Permission, Role, has_permission
from app.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate the access token and retrieve the active database user."""

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id or not user_id.isdigit():
            raise credentials_error

    except (jwt.InvalidTokenError, AttributeError, TypeError):
        raise credentials_error

    with get_active_engine().connect() as connection:
        user = connection.execute(
            select(users).where(users.c.id == int(user_id))
        ).mappings().first()

    if not user or not user["is_active"]:
        raise credentials_error

    try:
        Role(user["role"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account has an invalid role.",
        )

    return dict(user)


def require_permission(permission: Permission):
    """Create a dependency that enforces a specific permission."""

    def permission_dependency(
        current_user: dict = Depends(get_current_user),
    ):
        if not has_permission(current_user["role"], permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return permission_dependency
