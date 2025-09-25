from pathlib import Path
import json
import threading
from typing import Optional, Dict, Any


ROOT = Path(__file__).resolve().parents[1]
STORAGE = ROOT / "storage"
UPLOADS = STORAGE / "uploads"
GENERATED = STORAGE / "generated"
TEMP = STORAGE / "temp"
METADATA_FILE = STORAGE / "media_metadata.json"
TASKS_FILE = STORAGE / "video_tasks.json"


def ensure_storage_paths() -> Dict[str, str]:
    for p in [UPLOADS, GENERATED, TEMP]:
        p.mkdir(parents=True, exist_ok=True)
    # ensure metadata files exist
    if not METADATA_FILE.exists():
        METADATA_FILE.write_text(json.dumps({}))
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text(json.dumps({}))
    return {"uploads": str(UPLOADS), "generated": str(GENERATED), "temp": str(TEMP)}


_meta_lock = threading.Lock()


def _load_metadata() -> Dict[str, Any]:
    try:
        return json.loads(METADATA_FILE.read_text())
    except Exception:
        return {}


def _save_metadata(data: Dict[str, Any]):
    with _meta_lock:
        METADATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def add_file_metadata(file_id: str, info: Dict[str, Any]):
    data = _load_metadata()
    data[file_id] = info
    _save_metadata(data)


def get_file_metadata(file_id: str) -> Optional[Dict[str, Any]]:
    data = _load_metadata()
    return data.get(file_id)


def delete_file_metadata(file_id: str) -> bool:
    data = _load_metadata()
    if file_id in data:
        del data[file_id]
        _save_metadata(data)
        return True
    return False


def list_files(page: int = 1, limit: int = 20, file_type: Optional[str] = None, sort: Optional[str] = None):
    data = _load_metadata()
    items = list(data.values())
    # filter by file_type
    if file_type:
        items = [i for i in items if i.get("mime_type", "").startswith(file_type)]
    # sort
    if sort == "date_desc":
        items.sort(key=lambda x: x.get("upload_date", ""), reverse=True)
    elif sort == "date_asc":
        items.sort(key=lambda x: x.get("upload_date", ""))
    elif sort == "name_asc":
        items.sort(key=lambda x: x.get("original_filename", ""))
    elif sort == "size_desc":
        items.sort(key=lambda x: x.get("file_size", 0), reverse=True)

    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    return items[start:end], total


# Video tasks store
_tasks_lock = threading.Lock()


def _load_tasks() -> Dict[str, Any]:
    try:
        return json.loads(TASKS_FILE.read_text())
    except Exception:
        return {}


def _save_tasks(data: Dict[str, Any]):
    with _tasks_lock:
        TASKS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def add_task(task_id: str, info: Dict[str, Any]):
    data = _load_tasks()
    data[task_id] = info
    _save_tasks(data)


def update_task(task_id: str, patch: Dict[str, Any]):
    data = _load_tasks()
    if task_id in data:
        data[task_id].update(patch)
        _save_tasks(data)


def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    data = _load_tasks()
    return data.get(task_id)


def list_tasks(page: int = 1, limit: int = 20, status: Optional[str] = None):
    data = _load_tasks()
    items = list(data.values())
    if status:
        items = [i for i in items if i.get("status") == status]
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    return items[start:end], total
