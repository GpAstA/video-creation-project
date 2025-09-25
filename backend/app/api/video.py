from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
import threading
import time

from app.utils import add_task, get_task, list_tasks, update_task

router = APIRouter(prefix="/api/video", tags=["video"])


class VideoCreateRequest(BaseModel):
    scenario: str
    settings: dict


class VideoCreateResponse(BaseModel):
    task_id: str
    video_url: Optional[str]
    audio_url: Optional[str]
    subtitle_url: Optional[str]
    status: str
    processing_time: Optional[float]
    metadata: Optional[dict]


def _process_task(task_id: str):
    # simulate processing steps
    add_task(task_id, {"task_id": task_id, "status": "processing", "progress": 0, "steps": {}})
    for i, step in enumerate(["video_generation", "audio_extraction", "subtitle_generation", "final_composition"]):
        time.sleep(1)
        update_task(task_id, {"progress": int((i + 1) / 4 * 100), "current_step": step})
    update_task(task_id, {"status": "completed", "progress": 100, "video_url": f"/storage/generated/video_{task_id}.mp4"})


@router.post("/create", response_model=VideoCreateResponse)
async def create_video(req: VideoCreateRequest):
    if not req.scenario or not req.scenario.strip():
        raise HTTPException(status_code=400, detail="scenario is required")

    task_id = f"task_{uuid.uuid4().hex[:12]}"
    # start background thread
    t = threading.Thread(target=_process_task, args=(task_id,), daemon=True)
    t.start()
    return VideoCreateResponse(task_id=task_id, status="processing")


@router.get("/status/{task_id}")
async def get_status(task_id: str):
    t = get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="task not found")
    return t


@router.get("/list")
async def list_videos(page: int = 1, limit: int = 20, status: Optional[str] = None):
    items, total = list_tasks(page=page, limit=limit, status=status)
    return {"videos": items, "total_count": total, "page": page, "limit": limit, "total_pages": (total + limit - 1) // limit}
