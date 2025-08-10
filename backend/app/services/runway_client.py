import os
import time
import requests
from typing import List, Dict, Any
import base64

def generate_video_clips(
    scenes: List[Dict[str, Any]], 
    reference_images: List[str], 
    api_key: str, 
    output_dir: str
) -> List[str]:
    """Generate video clips for each scene using RunwayML Gen-2 API"""
    
    clip_paths = []
    
    for i, scene in enumerate(scenes):
        try:
            # Prepare the prompt for this scene
            prompt = scene.get("prompt", "Beautiful cinematic scene")
            duration = scene.get("duration", 3)
            
            # Use the first reference image for style consistency
            reference_image_path = reference_images[0] if reference_images else None
            
            # Generate video clip
            clip_path = os.path.join(output_dir, f"scene_{i}.mp4")
            
            success = generate_single_clip(
                prompt=prompt,
                duration=duration,
                reference_image_path=reference_image_path,
                output_path=clip_path,
                api_key=api_key
            )
            
            if success:
                clip_paths.append(clip_path)
            else:
                # Create a placeholder clip if generation fails
                create_placeholder_clip(scene, clip_path)
                clip_paths.append(clip_path)
                
        except Exception as e:
            print(f"Error generating clip for scene {i}: {e}")
            # Create placeholder clip
            clip_path = os.path.join(output_dir, f"scene_{i}.mp4")
            create_placeholder_clip(scene, clip_path)
            clip_paths.append(clip_path)
    
    return clip_paths

def generate_single_clip(
    prompt: str, 
    duration: int, 
    reference_image_path: str, 
    output_path: str, 
    api_key: str
) -> bool:
    """Generate a single video clip using RunwayML Gen-2 API"""
    
    try:
        # RunwayML Gen-2 API endpoint
        url = "https://api.runwayml.com/v1/inference"
        
        # Prepare the request payload
        payload = {
            "model": "gen-2",
            "input": {
                "prompt": prompt,
                "duration": duration,
                "width": 1920,
                "height": 1080,
                "fps": 24
            }
        }
        
        # Add reference image if available
        if reference_image_path and os.path.exists(reference_image_path):
            with open(reference_image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
                payload["input"]["reference_image"] = f"data:image/jpeg;base64,{image_data}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make the API request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Download the generated video
            video_data = response.json()
            video_url = video_data.get("output", {}).get("video_url")
            
            if video_url:
                video_response = requests.get(video_url)
                if video_response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(video_response.content)
                    return True
        
        print(f"RunwayML API error: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        print(f"Error in RunwayML generation: {e}")
        return False

def create_placeholder_clip(scene: Dict[str, Any], output_path: str):
    """Create a placeholder video clip using ffmpeg"""
    try:
        description = scene.get("description", "Scene")
        duration = scene.get("duration", 3)
        
        # Create a simple colored video with text overlay
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
        color = colors[len(description) % len(colors)]
        
        # Escape special characters in description
        safe_description = description.replace("'", "\\'").replace('"', '\\"')
        
        cmd = f'ffmpeg -f lavfi -i "color=c={color}:size=1920x1080:duration={duration}" -vf "drawtext=text=\'{safe_description}\':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" -c:a aac -shortest {output_path}'
        
        os.system(cmd)
        
    except Exception as e:
        print(f"Error creating placeholder clip: {e}")
        # Create a simple black video as last resort
        cmd = f'ffmpeg -f lavfi -i "color=c=black:size=1920x1080:duration=3" -c:a aac -shortest {output_path}'
        os.system(cmd)
