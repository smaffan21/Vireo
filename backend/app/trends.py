import os
from typing import List, Dict

from moviepy.editor import VideoClip, AudioClip
import numpy as np


# Preloaded trend metadata
TRENDS: List[Dict] = [
    {
        "id": "im_x_of_course_i_y",
        "title": "I'm X, of course I Y",
        "description": "Fill the blanks for a classic self-referential meme format.",
        "template": "I'm {x}, of course I {y}.",
        "base_video": "base.mp4",
        "music": "music.mp3",
        "thumbnail": "thumb.png",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
    },
    {
        "id": "day_in_the_life",
        "title": "Day in the life of…",
        "description": "Mini-vlog format with snappy cuts.",
        "template": "A day in the life of {subject}: {steps}",
        "base_video": "base.mp4",
        "music": "music.mp3",
        "thumbnail": "thumb.png",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
    },
    {
        "id": "when_you_but",
        "title": "When you [situation] but [unexpected ending]",
        "description": "Setup and punchline with a twist.",
        "template": "When you {situation} but {twist}.",
        "base_video": "base.mp4",
        "music": "music.mp3",
        "thumbnail": "thumb.png",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
    },
]


def ensure_assets(base_assets_dir: str) -> None:
    """Generate simple synthetic assets for each trend if they don't exist.

    - base.mp4: 6s vertical 1080x1920 gradient color clip with gentle animation
    - music.mp3: short sine wave melody
    - thumb.png: basic thumbnail with gradient (text not embedded to avoid font deps)
    """
    os.makedirs(base_assets_dir, exist_ok=True)
    for trend in TRENDS:
        trend_dir = os.path.join(base_assets_dir, trend["id"])
        os.makedirs(trend_dir, exist_ok=True)
        base_video = os.path.join(trend_dir, trend["base_video"])
        music = os.path.join(trend_dir, trend["music"])
        thumb = os.path.join(trend_dir, trend["thumbnail"])

        if not os.path.exists(base_video):
            duration = 6
            w, h = 1080, 1920

            def make_frame(t):
                # Animated vertical gradient
                y = np.linspace(0, 1, h).reshape(h, 1)
                x = np.linspace(0, 1, w).reshape(1, w)
                # Create arrays with proper dimensions
                r = ((x + t * 0.1) % 1.0).T  # Transpose to get (h, w)
                g = ((y + t * 0.2) % 1.0)     # Already (h, 1), broadcast to (h, w)
                b = (((x + y) * 0.5 + t * 0.05) % 1.0).T  # Transpose to get (h, w)
                frame = np.stack([r, g, b], axis=2)
                return (frame * 255).astype(np.uint8)

            clip = VideoClip(make_frame=make_frame, duration=duration)
            clip = clip.set_fps(30)
            clip = clip.set_duration(duration)
            clip = clip.resize((w, h))
            clip.write_videofile(base_video, fps=30, codec="libx264", audio=False, verbose=False, logger=None)

        if not os.path.exists(music):
            sr = 44100
            duration = 6
            t = np.linspace(0, duration, int(sr * duration), False)
            # Simple two-tone melody
            tone1 = 0.2 * np.sin(2 * np.pi * 440 * t)
            tone2 = 0.2 * np.sin(2 * np.pi * 660 * t) * (t % 1.0 < 0.5)
            signal = (tone1 + tone2).astype(np.float32)

            def audio_make_frame(tt):
                idx = np.minimum((tt * sr).astype(int), len(signal) - 1)
                return signal[idx]

            audio = AudioClip(lambda tt: audio_make_frame(tt), duration=duration, fps=sr)
            audio.write_audiofile(music, fps=sr, nbytes=2, codec="mp3", verbose=False, logger=None)

        if not os.path.exists(thumb):
            # Generate a very simple thumbnail from the first frame of the base video
            try:
                from moviepy.editor import VideoFileClip

                with VideoFileClip(base_video) as v:
                    frame = v.get_frame(0.0)
                    from PIL import Image

                    img = Image.fromarray(frame)
                    # Resize to square-ish thumbnail for grid
                    img.thumbnail((600, 600))
                    img.save(thumb)
            except Exception:
                pass


