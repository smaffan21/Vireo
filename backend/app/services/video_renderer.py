from __future__ import annotations

import os
from typing import List, Dict, Optional

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def _make_caption_clip(text: str, start: float, end: float, video_w: int, video_h: int) -> ImageClip:
    duration = max(0.3, end - start)
    # Render text with PIL to avoid ImageMagick dependency
    padding_x = int(video_w * 0.06)
    max_width = int(video_w * 0.85)
    target_y = int(video_h * 0.68)
    bg_color = (255, 255, 255, 242)
    text_color = (0, 0, 0, 255)

    # Choose a safe default font
    try:
        font = ImageFont.truetype("arialbd.ttf", size=80)
    except Exception:
        font = ImageFont.load_default()

    # Wrap text to fit max_width
    def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_w: int):
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            bbox = draw.textbbox((0, 0), trial, font=font)
            if bbox[2] - bbox[0] <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    # Create a canvas large enough for box; then position later via set_position
    canvas = Image.new("RGBA", (video_w, video_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    lines = wrap_text(draw, text, font, max_width - 2 * padding_x)
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])
    text_w = min(max_width - 2 * padding_x, max(line_widths) if line_widths else 0)
    text_h = sum(line_heights) + (len(lines) - 1) * 8
    box_w = text_w + 2 * padding_x
    box_h = text_h + 24

    box_x = (video_w - box_w) // 2
    box_y = target_y

    # Draw rounded rectangle background
    radius = 24
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=radius, fill=bg_color)

    # Draw text centered within box
    cur_y = box_y + 12
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        tx = box_x + (box_w - lw) // 2
        draw.text((tx, cur_y), line, font=font, fill=text_color)
        cur_y += lh + 8

    frame = np.array(canvas)
    clip = ImageClip(frame).set_start(start).set_duration(duration).set_position((0, 0))
    return clip


def render_video_fast_mode(
    base_assets_dir: str,
    base_video_filename: str,
    music_filename: str,
    captions: List[Dict],
    output_path: str,
    voiceover_path: Optional[str] = None,
) -> None:
    base_video_path = os.path.join(base_assets_dir, base_video_filename)
    music_path = os.path.join(base_assets_dir, music_filename)

    with VideoFileClip(base_video_path) as base:
        video_w, video_h = base.size

        # Build caption overlays
        caption_clips = [
            _make_caption_clip(c["text"], c["start"], c["end"], video_w, video_h)
            for c in captions
        ]
        overlay = CompositeVideoClip([base] + caption_clips, size=base.size)

        # Audio
        audio_tracks = []
        if os.path.exists(music_path):
            music = AudioFileClip(music_path).volumex(0.25)
            # Loop music to video duration
            music = music.set_duration(base.duration)
            audio_tracks.append(music)
        if voiceover_path and os.path.exists(voiceover_path):
            vo = AudioFileClip(voiceover_path).volumex(1.0)
            vo = vo.set_duration(min(vo.duration, base.duration))
            audio_tracks.append(vo)

        if audio_tracks:
            audio = CompositeAudioClip(audio_tracks).set_duration(base.duration)
            overlay = overlay.set_audio(audio)
        else:
            overlay = overlay.set_audio(base.audio)

        # Export
        out_dir = os.path.dirname(output_path)
        os.makedirs(out_dir, exist_ok=True)
        overlay.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=30,
            threads=2,
            preset="veryfast",
            verbose=False,
            logger=None,
        )


