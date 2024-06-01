from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from firebase_admin import auth

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash, decode_token
from app.models import Message, NewPassword, Token, RequestToken, TokenResponse, User, ResponseModel
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)
from pydantic import BaseModel
import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/access-token", response_model=TokenResponse)
async def login_access_token(requestToken: RequestToken, session: SessionDep) -> TokenResponse:
    """
    Firebase verify login token
    """
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(requestToken.token)
        uid = decoded_token['uid']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase ID token")

    # START user check tambahan apabila dibutuhkan

    # create user if not exist
    user_data = {
        "uid": uid,
        "email": decoded_token.get("email"),
        "is_active": True,
    }
    user = crud.get_user_by_email(session=session, email=user_data["email"])
    if not user:
        # create user with session
        user.uid = uid
        user.email = decoded_token.get("email")
        user.is_active = True
        session.add(user)
        # user = crud.create_user(session=session, user_create=user_data)
    else:
        # check if uid is none, if none update uid
        if not user.uid:
            user.uid = uid
            session.add(user)
            session.commit()

    # END user check tambahan apabila dibutuhkan

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(uid, expires_delta=access_token_expires)

    token = Token(access_token=access_token, token_type="bearer", user = user.from_db(user))

    response = TokenResponse(data=token, message="login successfull")

    print(response)

    return response

@router.post("/logout", response_model=ResponseModel)
async def logout(token: str, session: SessionDep) -> ResponseModel:
    """
    Invalidate an access token
    """
    try:
        # Assume decode_token is a function that can parse your JWTs
        payload = decode_token(token)
        if payload:
            # Store the token or its unique jti (JWT ID) in a blacklist
            expiration = payload.get("exp")
            current_time = datetime.utcnow()
            if expiration:
                remaining_time = expiration - int(current_time.timestamp())
                # Store the token with its remaining time to live
                if remaining_time > 0:
                    crud.store_blacklisted_token(session=session, token=token, ttl=remaining_time)
            return ResponseModel(message="Token has been invalidated")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid token")
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid token")


