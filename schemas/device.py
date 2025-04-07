import uuid

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    name: str


class DeviceResponse(BaseModel):
    id: int
    name: str
    user_id: uuid.UUID
