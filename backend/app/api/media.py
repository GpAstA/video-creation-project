from fastapi import APIRouter

router = APIRouter(prefix="/api/media", tags=["media"])

@router.post("/upload")
async def upload_media():
    # TODO: implement media upload handling
    return {"files": [], "total_count": 0, "status": "success"}
