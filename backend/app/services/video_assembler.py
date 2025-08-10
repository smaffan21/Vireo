import os
import subprocess
from typing import List, Optional

def assemble_final_video(
    clip_paths: List[str],
    voiceover_path: Optional[str],
    script: str,
    output_path: str
):
    """Assemble the final video by concatenating clips, adding voiceover and captions"""
    
    try:
        if not clip_paths:
            raise ValueError("No video clips provided")
        
        # Create a temporary file list for ffmpeg concatenation
        temp_dir = os.path.dirname(output_path)
        file_list_path = os.path.join(temp_dir, "file_list.txt")
        
        with open(file_list_path, "w") as f:
            for clip_path in clip_paths:
                if os.path.exists(clip_path):
                    f.write(f"file '{clip_path}'\n")
        
        # Step 1: Concatenate all video clips
        concatenated_path = os.path.join(temp_dir, "concatenated.mp4")
        concat_cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0", 
            "-i", file_list_path, "-c", "copy", concatenated_path
        ]
        
        subprocess.run(concat_cmd, check=True, capture_output=True)
        
        # Step 2: Add voiceover and captions
        if voiceover_path and os.path.exists(voiceover_path):
            # Add voiceover and captions
            final_cmd = [
                "ffmpeg", "-i", concatenated_path, "-i", voiceover_path,
                "-filter_complex", 
                f"drawtext=text='{script}':fontsize=40:fontcolor=white:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-th-20",
                "-c:v", "libx264", "-c:a", "aac", "-shortest", output_path
            ]
        else:
            # Add only captions
            final_cmd = [
                "ffmpeg", "-i", concatenated_path,
                "-vf", f"drawtext=text='{script}':fontsize=40:fontcolor=white:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-th-20",
                "-c:v", "libx264", "-c:a", "aac", output_path
            ]
        
        subprocess.run(final_cmd, check=True, capture_output=True)
        
        # Cleanup temporary files
        if os.path.exists(file_list_path):
            os.remove(file_list_path)
        if os.path.exists(concatenated_path):
            os.remove(concatenated_path)
            
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        # Fallback: create a simple video
        create_fallback_video(clip_paths, script, output_path)
    except Exception as e:
        print(f"Error assembling video: {e}")
        create_fallback_video(clip_paths, script, output_path)

def create_fallback_video(clip_paths: List[str], script: str, output_path: str):
    """Create a simple fallback video if assembly fails"""
    try:
        # Create a simple video with the script as text overlay
        script_words = script.split()[:10]  # Limit to first 10 words
        script_text = " ".join(script_words)
        
        cmd = [
            "ffmpeg", "-f", "lavfi", 
            "-i", "color=c=black:size=1920x1080:duration=10",
            "-vf", f"drawtext=text='{script_text}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-c:a", "aac", output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
    except Exception as e:
        print(f"Fallback video creation failed: {e}")
        # Create a minimal video
        cmd = [
            "ffmpeg", "-f", "lavfi", 
            "-i", "color=c=blue:size=1920x1080:duration=5",
            "-c:v", "libx264", output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
