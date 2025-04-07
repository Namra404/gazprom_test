import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.models import UserModel


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self) -> UserModel:
        user = UserModel()
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get(self, user_id: uuid.UUID):
        user = await self.db.get(UserModel, user_id)
        return user

