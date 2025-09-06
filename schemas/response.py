from pydantic import BaseModel
from typing import Any, Optional

class ResponseSchema(BaseModel):
    status: str
    message: str
    body: Optional[Any] = None
