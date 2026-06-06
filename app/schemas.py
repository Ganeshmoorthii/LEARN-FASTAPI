from pydantic import BaseModel
from typing import Optional
import uuid


class PostCreate(BaseModel):
    caption: Optional[str] = None
    url: str
    file_type: str
    file_name: str


class PostUpdate(BaseModel):
    caption: Optional[str] = None
    url: Optional[str] = None
    file_type: Optional[str] = None
    file_name: Optional[str] = None


class PostResponse(BaseModel):
    id: uuid.UUID
    caption: Optional[str] = None
    url: str
    file_type: str
    file_name: str
