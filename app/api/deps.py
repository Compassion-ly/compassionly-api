from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import FastAPI, Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, select


from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

reusable_oauth2 = HTTPBearer(
    scheme_name="Bearer",
    auto_error=False
)

# security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
# TokenDep = Annotated[str, Depends(reusable_oauth2)]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(reusable_oauth2)]



def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        # Extract token string from HTTPAuthorizationCredentials
        token_str = token.credentials
        payload = security.decode_token(token_str)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials: {str(e)}")

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    uid = payload.get("sub")
    if not uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user ID in token")

    user = session.exec(select(User).where(User.uid == uid)).first()
    if not user:
        raise HTTPException(status_code=404, detail=uid)
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user



CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
