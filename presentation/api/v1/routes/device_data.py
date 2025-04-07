from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from celery.result import AsyncResult

from repositories.device import DeviceRepository
from repositories.device_data import DeviceData
from repositories.factories import get_db
from schemas.device_data import DeviceDataCreate, DeviceDataResponse
from tasks.tasks import analyze_device_data_task

router = APIRouter(prefix="/devices", tags=["Device Data"])


@router.post("/{device_id}/data", response_model=list[DeviceDataResponse])
async def collect_data(
        device_id: int,
        device_data: DeviceDataCreate,
        db: AsyncSession = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device = await device_repo.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    repo = DeviceData(db)
    result = []
    for name, value in device_data.data.items():
        data = await repo.create(device_id=device_id, name=name, value=value)
        result.append(data)
    return result


@router.get("/{device_id}/analyze")
async def analyze_device_data(
        device_id: int,
        period: str = "all",
        name: str | None = None,
        db: AsyncSession = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device = await device_repo.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    task = analyze_device_data_task.delay(device_id, period, name)
    # repo = DeviceData(db)
    # result = await repo.analyze(device_id, period, name)
    return {"task_id": task}


@router.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return {"task_id": task_id, "status": "pending"}
    elif task.state == "SUCCESS":
        return {"task_id": task_id, "status": "success", "result": task.result}
    else:
        return {"task_id": task_id, "status": task.state}
