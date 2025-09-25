from pydantic import BaseModel

class Scenario(BaseModel):
    text: str
    scenes: list = []
