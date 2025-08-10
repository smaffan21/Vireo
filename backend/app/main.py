import os
import uuid
import tempfile
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from .services.openai_client import generate_script_and_scenes, extract_image_descriptions
from .services.elevenlabs_client import synthesize_voiceover
from .services.runway_client import generate_video_clips
from .services.video_assembler import assemble_final_video

load_dotenv()

class StoryGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "cinematic"
    image_files: List[str] = []  # Base64 encoded images

class StoryGenerationResponse(BaseModel):
    story_id: str
    script: str
    scenes: List[Dict[str, Any]]
    video_url: Optional[str] = None
    status: str

app = FastAPI(title="Image-to-Video Story Generator", version="1.0")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
VIDEOS_DIR = os.path.join(PUBLIC_DIR, "videos")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Serve static files
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.post("/generate-story", response_model=StoryGenerationResponse)
async def generate_story(
    prompt: str = Form(...),
    style: str = Form("cinematic"),
    images: List[UploadFile] = File(...)
):
    """Generate a complete story video from uploaded images and text prompt"""
    
    story_id = str(uuid.uuid4())
    story_dir = os.path.join(TEMP_DIR, story_id)
    os.makedirs(story_dir, exist_ok=True)
    
    try:
        # 1. Save uploaded images
        image_paths = []
        for i, image in enumerate(images):
            if image.content_type and image.content_type.startswith('image/'):
                image_path = os.path.join(story_dir, f"input_image_{i}.jpg")
                with open(image_path, "wb") as f:
                    shutil.copyfileobj(image.file, f)
                image_paths.append(image_path)
        
        if not image_paths:
            raise HTTPException(status_code=400, detail="No valid images uploaded")
        
        # 2. Extract image descriptions using OpenAI Vision
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        image_descriptions = extract_image_descriptions(image_paths, openai_api_key)
        
        # 3. Generate script and scene breakdown
        script, scenes = generate_script_and_scenes(
            prompt=prompt,
            style=style,
            image_descriptions=image_descriptions,
            api_key=openai_api_key
        )
        
        # 4. Generate video clips for each scene
        runway_api_key = os.getenv("RUNWAYML_API_KEY")
        if runway_api_key:
            try:
                clip_paths = generate_video_clips(
                    scenes=scenes,
                    reference_images=image_paths,
                    api_key=runway_api_key,
                    output_dir=story_dir
                )
            except Exception as e:
                print(f"RunwayML generation failed: {e}")
                # Use placeholder clips for demo
                clip_paths = create_placeholder_clips(scenes, story_dir)
        else:
            # Use placeholder clips for demo
            clip_paths = create_placeholder_clips(scenes, story_dir)
        
        # 5. Generate voiceover
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        voiceover_path = None
        if elevenlabs_api_key:
            try:
                voiceover_path = synthesize_voiceover(
                    text=script,
                    api_key=elevenlabs_api_key,
                    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                    out_dir=story_dir
                )
            except Exception as e:
                print(f"ElevenLabs synthesis failed: {e}")
        
        # 6. Assemble final video
        output_filename = f"story_{story_id}.mp4"
        output_path = os.path.join(VIDEOS_DIR, output_filename)
        
        assemble_final_video(
            clip_paths=clip_paths,
            voiceover_path=voiceover_path,
            script=script,
            output_path=output_path
        )
        
        video_url = f"/public/videos/{output_filename}"
        
        return StoryGenerationResponse(
            story_id=story_id,
            script=script,
            scenes=scenes,
            video_url=video_url,
            status="completed"
        )
        
    except Exception as e:
        # Cleanup on error
        if os.path.exists(story_dir):
            shutil.rmtree(story_dir)
        raise HTTPException(status_code=500, detail=str(e))

def create_placeholder_clips(scenes: List[Dict], output_dir: str) -> List[str]:
    """Create placeholder video clips for demo purposes"""
    clip_paths = []
    
    for i, scene in enumerate(scenes):
        # Create a simple colored video clip using ffmpeg
        clip_path = os.path.join(output_dir, f"scene_{i}.mp4")
        
        # Generate a simple colored video with text overlay
        color = ["red", "blue", "green", "yellow", "purple"][i % 5]
        duration = scene.get("duration", 3)
        
        scene_text = scene.get("description", "Scene").replace("'", "\\'")
        cmd = f'ffmpeg -f lavfi -i "color=c={color}:size=1920x1080:duration={duration}" -vf "drawtext=text=\'{scene_text}\':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" -c:a aac -shortest {clip_path}'
        
        os.system(cmd)
        clip_paths.append(clip_path)
    
    return clip_paths

@app.get("/story/{story_id}")
def get_story_status(story_id: str):
    """Get the status of a story generation"""
    story_dir = os.path.join(TEMP_DIR, story_id)
    if not os.path.exists(story_dir):
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Check if final video exists
    video_path = os.path.join(VIDEOS_DIR, f"story_{story_id}.mp4")
    if os.path.exists(video_path):
        return {
            "story_id": story_id,
            "status": "completed",
            "video_url": f"/public/videos/story_{story_id}.mp4"
        }
    else:
        return {
            "story_id": story_id,
            "status": "processing"
        }

@app.get("/styles")
def get_available_styles():
    """Get available video styles"""
    return {
        "styles": [
            {"id": "cinematic", "name": "Cinematic", "description": "Movie-like dramatic style"},
            {"id": "animation", "name": "Animation", "description": "Animated cartoon style"},
            {"id": "futuristic", "name": "Futuristic", "description": "Sci-fi futuristic style"},
            {"id": "documentary", "name": "Documentary", "description": "Realistic documentary style"},
            {"id": "artistic", "name": "Artistic", "description": "Creative artistic style"},
            {"id": "minimalist", "name": "Minimalist", "description": "Clean minimalist style"}
        ]
    }

@app.get("/")
def root():
    return {"ok": True, "service": "Image-to-Video Story Generator"}


