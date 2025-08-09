from __future__ import annotations

import os
import uuid
import requests


def synthesize_voiceover(text: str, api_key: str, voice_id: str, out_dir: str) -> str:
    """Synthesize voiceover with ElevenLabs. Returns MP3 file path.

    Raises on error. Caller may catch and fallback.
    """
    os.makedirs(out_dir, exist_ok=True)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": api_key,
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    out_path = os.path.join(out_dir, f"vo-{uuid.uuid4().hex[:8]}.mp3")
    with open(out_path, "wb") as f:
        f.write(r.content)
    return out_path


