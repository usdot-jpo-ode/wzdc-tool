from pydantic import BaseModel
from typing import List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    token_expires: str
