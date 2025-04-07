# src/routes/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.device import DeviceRepository
from schemas.device import DeviceResponse, DeviceCreate
from schemas.user import UserCreate, UserResponse
from tasks.tasks import analyze_by_user_task, analyze_by_user_per_device_task
import uuid

from repositories.factories import get_db
from repositories.user import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse)
async def create_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.create()
    return user


@router.post("/{user_id}/devices", response_model=DeviceResponse)
async def create_device(
        user_id: str,
        device: DeviceCreate,
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get(uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    device_repo = DeviceRepository(db)
    device = await device_repo.create(user_id=user.id, name=device.name)
    return device


@router.get("/{user_id}/analyze")
async def analyze_by_user(
        user_id: str,
        period: str = "all",
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get(uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = analyze_by_user_task.delay(user_id, period)
    return {"task_id": str(task.id)}


@router.get("/{user_id}/analyze-per-device")
async def analyze_by_user_per_device(
        user_id: str,
        period: str = "all",
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get(uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = analyze_by_user_per_device_task.delay(user_id, period)
    return {"task_id": str(task.id)}
