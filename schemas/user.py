import uuid

from pydantic import BaseModel


class UserCreate(BaseModel):
    pass


class UserResponse(BaseModel):
    id: uuid.UUID
