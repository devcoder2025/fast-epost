from fastapi import APIRouter, HTTPException
from .monitor import HealthMonitor

router = APIRouter()
health_monitor = HealthMonitor()

@router.get("/health")
async def health_check():
    status = health_monitor.get_status()
    if status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=status)
    return status

@router.get("/health/detailed")
async def detailed_health():
    return health_monitor.get_status()
