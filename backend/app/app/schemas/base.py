from datetime import datetime
from pydantic import BaseModel


# Shared properties
class Base(BaseModel):
    created: datetime = datetime.now()

