from pydantic import BaseModel

class Video(BaseModel):
    task_id: str
    title: str = None
    status: str
    video_url: str = None
    created_at: str = None
    duration: float = None
    file_size: int = None
