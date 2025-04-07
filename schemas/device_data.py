from datetime import datetime

from pydantic import BaseModel


class DeviceDataCreate(BaseModel):
    data: dict[str, float]


class DeviceDataAnalysis(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float


class DeviceDataResponse(BaseModel):
    id: int
    device_id: int
    name: str
    value: float
    created_at: datetime
    updated_at: datetime
