from fastapi import APIRouter

router = APIRouter(prefix="/api/video", tags=["video"])

@router.post("/create")
async def create_video(payload: dict):
    # TODO: implement video creation pipeline
    return {"task_id": "task_123", "status": "processing"}

@router.get("/status/{task_id}")
async def status(task_id: str):
    return {"task_id": task_id, "status": "completed", "progress": 100}

@router.get("/list")
async def list_videos():
    return {"videos": [], "total_count": 0, "page": 1, "limit": 20, "total_pages": 0}
