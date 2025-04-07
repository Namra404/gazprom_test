import os
from uuid import UUID

from celery import Celery

from repositories.device import DeviceRepository
from repositories.device_data import DeviceData
from repositories.factories import PostgresSessionFactory
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

session_factory = PostgresSessionFactory()


@celery_app.task
async def analyze_device_data_task(device_id: int, period: str = "all", name: str | None = None):
    async with session_factory.get_session() as db:
        repo = DeviceData(db)
        result = await repo.analyze(device_id, period, name)
        return result


@celery_app.task
async def analyze_by_user_task(user_id: UUID, period: str = "all"):
    async with session_factory.get_session() as db:
        repo = DeviceData(db)
        result = await repo.analyze_by_user(user_id, period)
        return result


@celery_app.task
async def analyze_by_user_per_device_task(user_id: UUID, period: str = "all"):
    async with session_factory.get_session() as db:
        repo = DeviceData(db)
        result = await repo.analyze_by_user_per_device(user_id, period)
        return result


@celery_app.task
async def analyze_user_device(user_id: str, device_id: int, period: str = "all"):
    async with session_factory.get_session() as db:
        device_repo = DeviceRepository(db)
        device = await device_repo.get(device_id)
        if not device or str(device.user_id) != user_id:
            raise ValueError(f"Device {device_id} does not belong to user {user_id}")

        repo = DeviceData(db)
        result = await repo.analyze(device_id, period)
        return result
