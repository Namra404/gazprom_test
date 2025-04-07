import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from repositories.models.base import Base
from repositories.models.device_data import DeviceDataModel


class DeviceModel(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  # Добавляем внешний ключ

    user: Mapped["UserModel"] = relationship(back_populates="devices")
    data: Mapped[list["DeviceDataModel"]] = relationship(back_populates="device", cascade="all, delete-orphan")