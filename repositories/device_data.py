import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, insert
from statistics import median
from typing import Dict, Any

from repositories.models.device import DeviceModel
from repositories.models.device_data import DeviceDataModel
from datetime import datetime, timedelta


class DeviceData:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, device_id: int, name: str, value: float):
        query_insert = (
            insert(DeviceDataModel)
            .values(
                device_id=device_id,
                name=name,
                value=value,
                created_at=datetime.utcnow(),  # Устанавливаем вручную, так как используем insert
                updated_at=datetime.utcnow()
            )
            .returning(DeviceDataModel)
        )
        # Выполняем запрос и получаем результат
        result = await self.db.execute(query_insert)
        obj = result.scalar_one()  # Получаем объект DeviceDataModel
        await self.db.commit()
        return obj
        # obj = DeviceDataModel(device_id=device_id, name=name, value=value)
        # self.db.add(obj)
        # await self.db.commit()
        # await self.db.refresh(obj)
        # return obj

    async def analyze(self, device_id: int, period: str = "all", name: str | None = None) -> Dict[str, Any]:

        device = await self.db.get(DeviceModel, device_id)
        if not device:
            raise ValueError(f"Device with id {device_id} not found")

        # Базовый запрос
        query = select(
            DeviceDataModel.name,
            func.min(DeviceDataModel.value).label("min"),
            func.max(DeviceDataModel.value).label("max"),
            func.count().label("count"),
            func.sum(DeviceDataModel.value).label("sum"),
            func.array_agg(DeviceDataModel.value).label("values")
        ).filter(DeviceDataModel.device_id == device_id)

        if period != "all":
            now = datetime.utcnow()
            if period == "day":
                time_filter = now - timedelta(days=1)
            elif period == "week":
                time_filter = now - timedelta(weeks=1)
            elif period == "month":
                time_filter = now - timedelta(days=30)
            else:
                raise ValueError(f"Unsupported period: {period}")
            query = query.filter(DeviceDataModel.created_at >= time_filter)

        if name is not None:
            query = query.filter(DeviceDataModel.name == name)

        query = query.group_by(DeviceDataModel.name)

        result = {}
        rows = await self.db.execute(query)
        for row in rows:
            values = row.values
            result[row.name] = {
                "min": row.min,
                "max": row.max,
                "count": row.count,
                "sum": row.sum,
                "median": median(values)
            }
        return result

    async def analyze_by_user(self, user_id: uuid.UUID, period: str = "all") -> Dict[str, Dict[str, Any]]:

        query = select(
            DeviceDataModel.name,
            func.min(DeviceDataModel.value).label("min"),
            func.max(DeviceDataModel.value).label("max"),
            func.count().label("count"),
            func.sum(DeviceDataModel.value).label("sum"),
            func.array_agg(DeviceDataModel.value).label("values")
        ).join(DeviceModel, DeviceDataModel.device_id == DeviceModel.id
               ).filter(DeviceModel.user_id == user_id)

        if period != "all":
            now = datetime.utcnow()
            if period == "day":
                time_filter = now - timedelta(days=1)
            elif period == "week":
                time_filter = now - timedelta(weeks=1)
            elif period == "month":
                time_filter = now - timedelta(days=30)
            else:
                raise ValueError(f"Unsupported period: {period}")
            query = query.filter(DeviceDataModel.created_at >= time_filter)

        query = query.group_by(DeviceDataModel.name)

        result = {}
        rows = await self.db.execute(query)
        for row in rows:
            values = row.values
            result[row.name] = {
                "min": row.min,
                "max": row.max,
                "count": row.count,
                "sum": row.sum,
                "median": median(values)
            }
        return result

    async def analyze_by_user_per_device(self, user_id: uuid.UUID, period: str = "all") -> Dict[int, Dict[str, Any]]:

        query = select(
            DeviceDataModel.device_id,
            DeviceDataModel.name,
            func.min(DeviceDataModel.value).label("min"),
            func.max(DeviceDataModel.value).label("max"),
            func.count().label("count"),
            func.sum(DeviceDataModel.value).label("sum"),
            func.array_agg(DeviceDataModel.value).label("values")
        ).join(DeviceModel, DeviceDataModel.device_id == DeviceModel.id
               ).filter(DeviceModel.user_id == user_id)

        if period != "all":
            now = datetime.now()
            if period == "day":
                time_filter = now - timedelta(days=1)
            elif period == "week":
                time_filter = now - timedelta(weeks=1)
            elif period == "month":
                time_filter = now - timedelta(days=30)
            else:
                raise ValueError(f"Unsupported period: {period}")
            query = query.filter(DeviceDataModel.created_at >= time_filter)

        query = query.group_by(DeviceDataModel.device_id, DeviceDataModel.name)

        result = {}
        rows = await self.db.execute(query)
        for row in rows:
            if row.device_id not in result:
                result[row.device_id] = {}
            values = row.values
            result[row.device_id][row.name] = {
                "min": row.min,
                "max": row.max,
                "count": row.count,
                "sum": row.sum,
                "median": median(values)
            }
        return result
