from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from typing import List
from pydantic import BaseModel
import uuid
from datetime import datetime
from PIL import Image
import os

from app.utils import ensure_storage_paths, UPLOADS, GENERATED, add_file_metadata, list_files, get_file_metadata, delete_file_metadata

router = APIRouter(prefix="/api/media", tags=["media"])

ensure_storage_paths()


class UploadedFileInfo(BaseModel):
    file_id: str
    original_filename: str
    stored_filename: str
    file_path: str
    file_size: int
    mime_type: str
    width: int = None
    height: int = None
    thumbnail_url: str = None
    upload_date: datetime
    file_url: str


class UploadResponse(BaseModel):
    files: List[UploadedFileInfo]
    total_count: int
    status: str = "success"
    message: str = None


@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="最大10ファイルまでアップロード可能です")

    stored = []
    for f in files:
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(f.filename)[1] or ".jpg"
        stored_name = f"{file_id}{ext}"
        storage_path = UPLOADS / stored_name

        contents = await f.read()
        with open(storage_path, "wb") as fh:
            fh.write(contents)

        mime = f.content_type
        width = None
        height = None
        thumb_name = f"thumb_{stored_name}"
        thumb_path = GENERATED / thumb_name
        try:
            img = Image.open(storage_path)
            width, height = img.size
            img.thumbnail((320, 240))
            img.save(thumb_path)
            thumbnail_url = f"/storage/generated/{thumb_name}"
        except Exception:
            thumbnail_url = None

        info = {
            "file_id": file_id,
            "original_filename": f.filename,
            "stored_filename": stored_name,
            "file_path": str(storage_path),
            "file_size": len(contents),
            "mime_type": mime,
            "width": width,
            "height": height,
            "thumbnail_url": thumbnail_url,
            "upload_date": datetime.utcnow().isoformat(),
            "file_url": f"/storage/uploads/{stored_name}",
        }
        add_file_metadata(file_id, info)
        stored.append(UploadedFileInfo(**info))

    return UploadResponse(files=stored, total_count=len(stored), message=f"{len(stored)}個のファイルがアップロードされました")


@router.get("/files")
async def get_files(page: int = 1, limit: int = 20, file_type: str = None, sort: str = None):
    items, total = list_files(page=page, limit=limit, file_type=file_type, sort=sort)
    return {"files": items, "total_count": total, "page": page, "limit": limit, "total_pages": (total + limit - 1) // limit}


@router.get("/files/{file_id}")
async def file_info(file_id: str):
    info = get_file_metadata(file_id)
    if not info:
        raise HTTPException(status_code=404, detail="file not found")
    return info


@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    info = get_file_metadata(file_id)
    if not info:
        raise HTTPException(status_code=404, detail="file not found")

    # delete physical files
    try:
        p = info.get("file_path")
        if p and os.path.exists(p):
            os.remove(p)
        thumb = info.get("thumbnail_url")
        if thumb:
            # thumbnail_url is /storage/generated/<name>
            name = thumb.split('/')[-1]
            tpath = GENERATED / name
            if tpath.exists():
                tpath.unlink()
    except Exception:
        pass

    delete_file_metadata(file_id)
    return {"message": "ファイルが削除されました", "file_id": file_id}


@router.get("/download/{file_id}")
async def download_file(file_id: str):
    info = get_file_metadata(file_id)
    if not info:
        raise HTTPException(status_code=404, detail="file not found")
    path = info.get("file_path")
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="file not found")
    with open(path, "rb") as fh:
        data = fh.read()
    return Response(content=data, media_type=info.get("mime_type", "application/octet-stream"))
