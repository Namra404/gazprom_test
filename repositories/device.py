import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.models import UserModel
from repositories.models.device import DeviceModel


class DeviceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID, name: str) -> DeviceModel:
        # Проверяем, существует ли пользователь
        user = await self.db.get(UserModel, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        device = DeviceModel(user_id=user_id, name=name)
        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)
        return device

    async def get(self, device_id: int) -> DeviceModel:
        device = await self.db.get(DeviceModel, device_id)
        return device

    async def get_by_user(self, user_id: uuid.UUID) -> list[DeviceModel]:
        # Джойн не нужен, так как user_id уже есть в DeviceModel
        query = select(DeviceModel).filter(DeviceModel.user_id == user_id)
        result = await self.db.execute(query)
        devices = result.scalars().all()
        return devices
