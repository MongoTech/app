from datetime import timedelta
from typing import Any
from google_auth_oauthlib.flow import InstalledAppFlow
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Response, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_302_FOUND
import requests
from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
import time

router = APIRouter()


@router.get('/social')
def social(response: Response):
    REDIRECT_URI = "http://localhost/api/response"
    client_config = {
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
        }
    flow = InstalledAppFlow.from_client_config({
        "web": client_config},
        redirect_uri=REDIRECT_URI,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]
    )

    # Redirect the user to Google's authorization page
    authorization_url, state = flow.authorization_url(
        access_type='offline',  # to get a refresh token
        prompt='consent'  # to force the user to grant consent again
    )

    return authorization_url + '&timestamp=' + str(time.time())

@router.get('/response')
async def response(resp: Response, state: str, code: str, db: Session = Depends(deps.get_db)):
    redirect_uri = "http://localhost/api/response"
    token_url = 'https://accounts.google.com/o/oauth2/token'
    token_payload = {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': 'authorization_code'
    }
    data = requests.post(token_url, data=token_payload).json()

    response = requests.get('https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses',
                            headers={'Authorization': 'Bearer ' + data["access_token"]})
    profile_data = response.json()
    name = profile_data["names"][0]["displayName"]
    email = profile_data["emailAddresses"][0]["value"].lower()
    user = await crud.user.get_by_email(db=db, email=email)
    if not user:
        user = await crud.user.create(db=db, obj_in={"full_name": name,
                                                     "email": email,
                                                     "is_superuser": False,
                                                     "is_active": True,
                                                     "access_token": data["access_token"],
                                                     "refresh_token": data["refresh_token"]
                                                     })
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(str(user["_id"]), expires_delta=access_token_expires)
    resp = RedirectResponse("/dashboard")
    resp.set_cookie(key="token", value=token, expires=access_token_expires)
    return resp


@router.post("/login/access-token", response_model=Any)
async def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=403, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(key="token", value=security.create_access_token(
            user["_id"], expires_delta=access_token_expires  # type: ignore
        ), expires=access_token_expires)
    response.status_code = 200

    return response

@router.post("/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user["email"], email=email, token=password_reset_token  # type: ignore
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.User)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> schemas.User:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):  # type: ignore
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user = await crud.user.update(
        db=db, db_obj=user, obj_in={"hashed_password": hashed_password}
    )
    return user
