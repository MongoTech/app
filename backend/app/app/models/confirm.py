from app.db.base_class import Base
from sqlalchemy import Column, String  # type: ignore


class Confirm(Base):
    __tablename__ = "confirm"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    token = Column(String)
    ttl = Column(String)
