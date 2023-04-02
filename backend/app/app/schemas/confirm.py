from datetime import datetime

from app.schemas.base import Base
from pydantic import EmailStr


# Shared properties
class ConfirmBase(Base):
    user_id: str
    email: EmailStr
    token: str
    ttl: datetime


# Properties to receive via API on creation
class ConfirmCreate(ConfirmBase):
    pass


# Properties to receive via API on update
class ConfirmUpdate(ConfirmBase):
    pass


class ConfirmInDBBase(ConfirmBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Confirm(ConfirmInDBBase):
    pass


# Additional properties stored in DB
class ConfirmInDB(ConfirmInDBBase):
    hashed_password: str
