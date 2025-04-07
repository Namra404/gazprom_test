from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from repositories.models.base import Base
from utils.utils import get_utc_now


class DeviceDataModel(Base):
    __tablename__ = 'devices_data'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    device: Mapped["DeviceModel"] = relationship(back_populates="data")
