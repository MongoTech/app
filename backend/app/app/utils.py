import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails  # type: ignore
from app import crud, schemas
from app.core.config import settings
from emails.template import JinjaTemplate  # type: ignore
from jose import jwt  # type: ignore


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    if not settings.EMAILS_ENABLED:
        print("no provided configuration for email variables")
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


async def create_confirmation_token(db, user, email):  # type: ignore
    token = hashlib.md5(user["id"].encode()).hexdigest()  # nosec
    confirm = schemas.ConfirmCreate(
        user_id=user["id"],
        email=email,
        token=token,
        ttl=datetime.now() + timedelta(minutes=1),
    )
    token = await crud.confirm.create(db=db, obj_in=confirm)
    send_welcome_email(user["email"], user["full_name"], token=token["token"])


def send_welcome_email(email_to: str, full_name: str, token: str) -> None:
    subject = "Congratulation you register account on MongoTech"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "welcome.html") as f:
        template_str = f.read()

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "full_name": full_name,
            "link": settings.SERVER_HOST + "/api/users/activate?token=" + token,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
