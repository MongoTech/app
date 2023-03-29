from sqlalchemy import Boolean, Column, String  # type: ignore

from app.db.base_class import Base


class Confirm(Base):
    __tablename__ = "confirm"
    _id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    token = Column(String)
    ttl = Column(String)
