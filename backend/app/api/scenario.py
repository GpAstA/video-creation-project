from fastapi import APIRouter

router = APIRouter(prefix="/api/scenario", tags=["scenario"])

@router.post("/generate")
async def generate_scenario(payload: dict):
    # TODO: implement scenario generation
    return {"scenario": "シーン1: サンプル\nシーン2: サンプル", "status": "success"}
