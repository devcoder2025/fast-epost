from fastapi import APIRouter, HTTPException
from .core import MessageQueue, QueuePriority

router = APIRouter()
message_queue = MessageQueue("amqp://localhost")

@router.post("/queue/{queue_name}")
async def publish_message(queue_name: str, message: dict, priority: str = "MEDIUM"):
    try:
        await message_queue.publish(
            queue_name,
            message,
            QueuePriority[priority]
        )
        return {"status": "success", "message": "Message published"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queue/metrics")
async def get_metrics():
    return message_queue.metrics.get_metrics()