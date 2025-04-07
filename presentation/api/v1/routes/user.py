from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.device import DeviceRepository
from repositories.device_data import DeviceData
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
        user_id: uuid.UUID,
        device: DeviceCreate,
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    device_repo = DeviceRepository(db)
    device = await device_repo.create(user_id=user.id, name=device.name)
    return device


@router.get("/{user_id}/analyze")
async def analyze_by_user(
        user_id: uuid.UUID,
        period: str = "all",
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # task = analyze_by_user_task.delay(user_id, period)
    repo = DeviceData(db)
    result = await repo.analyze_by_user(user_id, period)
    return {"res": result}


@router.get("/{user_id}/analyze-per-device")
async def analyze_by_user_per_device(
        user_id: uuid.UUID,
        period: str = "all",
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # task = analyze_by_user_per_device_task.delay(user_id, period)
    repo = DeviceData(db)
    result = await repo.analyze_by_user_per_device(user_id, period)
    return {"res": result}
