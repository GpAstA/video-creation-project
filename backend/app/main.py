from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import scenario, media, video

app = FastAPI(title="Video Creation Project API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scenario.router)
app.include_router(media.router)
app.include_router(video.router)

# Serve storage for local dev
app.mount("/storage/uploads", StaticFiles(directory="../storage/uploads"), name="uploads")
app.mount("/storage/generated", StaticFiles(directory="../storage/generated"), name="generated")

@app.get("/")
async def root():
    return {"message": "Backend skeleton running"}
