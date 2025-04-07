import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from repositories.models.base import Base
from repositories.models.device import DeviceModel


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[str] = mapped_column(String, nullable=True)
    devices: Mapped[list["DeviceModel"]] = relationship(back_populates="user")
