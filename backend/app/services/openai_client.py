from __future__ import annotations

import os
import base64
from typing import List, Dict, Any, Tuple
import openai

def extract_image_descriptions(image_paths: List[str], api_key: str) -> List[str]:
    """Extract descriptions from uploaded images using OpenAI Vision"""
    client = openai.OpenAI(api_key=api_key)
    descriptions = []
    
    for image_path in image_paths:
        try:
            with open(image_path, "rb") as image_file:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Describe this image in detail, focusing on visual elements, style, mood, and any objects or scenes that could be used for video generation. Be specific about colors, lighting, composition, and atmosphere."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=300
                )
                descriptions.append(response.choices[0].message.content)
        except Exception as e:
            print(f"Error extracting description from {image_path}: {e}")
            descriptions.append("A generic image with visual elements")
    
    return descriptions

def generate_script_and_scenes(
    prompt: str, 
    style: str, 
    image_descriptions: List[str], 
    api_key: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """Generate a script and scene breakdown based on user prompt and image descriptions"""
    
    client = openai.OpenAI(api_key=api_key)
    
    # Combine image descriptions
    image_context = "\n".join([f"Image {i+1}: {desc}" for i, desc in enumerate(image_descriptions)])
    
    system_prompt = f"""You are a professional video script writer and storyboard artist. Create a compelling short story video based on the user's prompt and reference images.

Style: {style}

Your task:
1. Write a short, engaging script (3-5 sentences) that tells a complete story
2. Break down the script into 3-5 scenes, each 3-5 seconds long
3. For each scene, provide a detailed visual prompt for AI video generation

Guidelines:
- Keep the total video length under 20 seconds
- Make each scene visually distinct and engaging
- Use the reference images to inform the visual style and content
- Create prompts that are specific enough for AI video generation
- Ensure the story flows naturally from scene to scene

Output format:
SCRIPT: [Your script here]

SCENES:
1. [Scene description] | Duration: [X] seconds | Prompt: [Detailed visual prompt for AI]
2. [Scene description] | Duration: [X] seconds | Prompt: [Detailed visual prompt for AI]
..."""

    user_prompt = f"""User Request: {prompt}

Reference Images:
{image_context}

Please create a compelling story video based on this prompt and the visual style of the reference images."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Parse the response
        script, scenes = parse_script_response(content)
        
        return script, scenes
        
    except Exception as e:
        print(f"Error generating script: {e}")
        # Fallback response
        script = "A beautiful story unfolds before our eyes. Each moment captures the essence of wonder and discovery. The journey takes us through breathtaking landscapes and intimate moments."
        scenes = [
            {
                "description": "Opening scene with dramatic lighting",
                "duration": 4,
                "prompt": "Cinematic opening shot with dramatic lighting, inspired by the reference images"
            },
            {
                "description": "Middle scene with dynamic movement",
                "duration": 4,
                "prompt": "Dynamic middle scene with flowing movement and vibrant colors"
            },
            {
                "description": "Closing scene with emotional impact",
                "duration": 4,
                "prompt": "Emotional closing scene with powerful visual impact and resolution"
            }
        ]
        return script, scenes

def parse_script_response(content: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Parse the AI response to extract script and scenes"""
    
    lines = content.split('\n')
    script = ""
    scenes = []
    
    in_script = False
    in_scenes = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("SCRIPT:"):
            in_script = True
            in_scenes = False
            script = line.replace("SCRIPT:", "").strip()
            continue
            
        if line.startswith("SCENES:"):
            in_script = False
            in_scenes = True
            continue
            
        if in_script and line:
            script += " " + line
            
        if in_scenes and line and line[0].isdigit():
            # Parse scene line: "1. [description] | Duration: [X] seconds | Prompt: [prompt]"
            try:
                parts = line.split("|")
                if len(parts) >= 3:
                    description = parts[0].split(".", 1)[1].strip()
                    duration_part = parts[1].strip()
                    prompt_part = parts[2].strip()
                    
                    duration = int(duration_part.replace("Duration:", "").replace("seconds", "").strip())
                    prompt = prompt_part.replace("Prompt:", "").strip()
                    
                    scenes.append({
                        "description": description,
                        "duration": duration,
                        "prompt": prompt
                    })
            except Exception as e:
                print(f"Error parsing scene line '{line}': {e}")
                # Add fallback scene
                scenes.append({
                    "description": "Scene",
                    "duration": 3,
                    "prompt": "Generic scene with visual elements"
                })
    
    # Ensure we have at least one scene
    if not scenes:
        scenes = [{
            "description": "Opening scene",
            "duration": 3,
            "prompt": "Beautiful opening scene with dramatic lighting"
        }]
    
    return script, scenes


