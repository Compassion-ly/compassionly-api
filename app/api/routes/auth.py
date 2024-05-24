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
from app.models import Message, NewPassword, Token, RequestToken, ResponseToken, User
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

@router.post("/access-token")
async def login_access_token(requestToken: RequestToken, session: SessionDep) -> ResponseToken:
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
        user = crud.create_user(session=session, user_create=user_data)
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

    return ResponseToken(access_token=access_token, user=user)

@router.post("/logout")
async def logout(token: str, session: SessionDep):
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
            return {"msg": "User logged out"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/me", response_model=User)
def me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Validate user and return user data
    """
    return current_user


# @router.post("/password-recovery/{email}")
# def recover_password(email: str, session: SessionDep) -> Message:
#     """
#     Password Recovery
#     """
#     user = crud.get_user_by_email(session=session, email=email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this email does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     email_data = generate_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )
#     send_email(
#         email_to=user.email,
#         subject=email_data.subject,
#         html_content=email_data.html_content,
#     )
#     return Message(message="Password recovery email sent")


# @router.post("/reset-password/")
# def reset_password(session: SessionDep, body: NewPassword) -> Message:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token=body.token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.get_user_by_email(session=session, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this email does not exist in the system.",
#         )
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(password=body.new_password)
#     user.hashed_password = hashed_password
#     session.add(user)
#     session.commit()
#     return Message(message="Password updated successfully")


# @router.post(
#     "/password-recovery-html-content/{email}",
#     dependencies=[Depends(get_current_active_superuser)],
#     response_class=HTMLResponse,
# )
# def recover_password_html_content(email: str, session: SessionDep) -> Any:
#     """
#     HTML Content for Password Recovery
#     """
#     user = crud.get_user_by_email(session=session, email=email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     email_data = generate_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )

#     return HTMLResponse(
#         content=email_data.html_content, headers={"subject:": email_data.subject}
#     )
