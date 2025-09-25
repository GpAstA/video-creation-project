from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.gemini_service import generate_scenario as gen_from_gemini

router = APIRouter(prefix="/api/scenario", tags=["scenario"])


class ScenarioRequest(BaseModel):
    text: str


class ScenarioResponse(BaseModel):
    scenario: str
    status: str = "success"


@router.post("/generate", response_model=ScenarioResponse)
async def generate_scenario(req: ScenarioRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="テキストが空です")

    scenario_text = gen_from_gemini(req.text)
    return ScenarioResponse(scenario=scenario_text)
