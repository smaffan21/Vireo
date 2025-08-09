import os
import uuid
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from .trends import TRENDS, ensure_assets
from .services.openai_client import generate_script_lines
from .services.elevenlabs_client import synthesize_voiceover
from .services.video_renderer import render_video_fast_mode


load_dotenv()


class GenerateVideoRequest(BaseModel):
    trend_id: str
    prompt: str
    fast_mode: bool = True


class GenerateVideoResponse(BaseModel):
    video_url: str
    meta: Dict[str, Any] | None = None


app = FastAPI(title="Vireo API", version="0.1")


# CORS for hackathon/demo convenience
origins_env = os.getenv("ORIGINS", "*")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
VIDEOS_DIR = os.path.join(PUBLIC_DIR, "videos")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(VIDEOS_DIR, exist_ok=True)


@app.on_event("startup")
def startup():
    # Temporarily disabled asset generation to get server running
    # ensure_assets(base_assets_dir=os.path.join(ASSETS_DIR, "trends"))
    pass


# Serve static public files and assets
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.get("/trends")
def list_trends(request: Request):
    # Build absolute URLs for frontend convenience
    api_base = os.getenv("API_BASE_URL")  # optional override
    if not api_base:
        # e.g., http://localhost:8000
        api_base = str(request.base_url).rstrip("/")
    result = []
    for t in TRENDS:
        thumb = f"/assets/trends/{t['id']}/{t['thumbnail']}"
        audio = f"/assets/trends/{t['id']}/{t['music']}"
        result.append({
            "id": t["id"],
            "title": t["title"],
            "description": t.get("description", ""),
            "template": t.get("template", ""),
            "thumbnail_url": f"{api_base}{thumb}",
            "audio_sample_url": f"{api_base}{audio}",
        })
    return {"trends": result}


@app.post("/generate-video", response_model=GenerateVideoResponse)
def generate_video(payload: GenerateVideoRequest):
    trend = next((t for t in TRENDS if t["id"] == payload.trend_id), None)
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    # 1) Script lines (captions)
    captions = generate_script_lines(
        user_prompt=payload.prompt,
        trend_template=trend["template"],
        openai_api_key=openai_api_key,
    )

    # 2) Voiceover (optional if no API key)
    voiceover_path = None
    if elevenlabs_api_key:
        try:
            voiceover_path = synthesize_voiceover(
                text=" ".join([c["text"] for c in captions]),
                api_key=elevenlabs_api_key,
                voice_id=trend.get("voice_id", "21m00Tcm4TlvDq8ikWAM"),
                out_dir=VIDEOS_DIR,
            )
        except Exception:
            voiceover_path = None

    # 3) Render in fast mode (overlay captions + VO over base clip and music)
    output_name = f"{payload.trend_id}-{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(VIDEOS_DIR, output_name)

    render_video_fast_mode(
        base_assets_dir=os.path.join(ASSETS_DIR, "trends", payload.trend_id),
        base_video_filename=trend["base_video"],
        music_filename=trend["music"],
        captions=captions,
        output_path=output_path,
        voiceover_path=voiceover_path,
    )

    url_path = f"/public/videos/{output_name}"
    api_base = os.getenv("API_BASE_URL")
    video_url = url_path if not api_base else f"{api_base}{url_path}"
    return GenerateVideoResponse(video_url=video_url, meta={"trend_id": payload.trend_id})


@app.get("/")
def root():
    return {"ok": True, "service": "Vireo API"}


