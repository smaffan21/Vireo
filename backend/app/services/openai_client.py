from __future__ import annotations

import re
from typing import List, Dict


def _heuristic_captions(user_prompt: str, trend_template: str) -> List[Dict]:
    # Very simple fallback: split into ~3 caption lines
    text = user_prompt.strip()
    if not text:
        text = trend_template.replace("{", "").replace("}", "")
    # Split by punctuation or spaces to approximate chunks
    parts = re.split(r"[\.|,|;|!|\?|\n]", text)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) == 0:
        parts = [text]
    if len(parts) > 3:
        parts = parts[:3]
    total = max(4.0, 1.5 * len(parts))
    per = total / len(parts)
    captions = []
    for i, p in enumerate(parts):
        captions.append({"text": p, "start": round(i * per, 2), "end": round((i + 1) * per, 2)})
    return captions


def generate_script_lines(user_prompt: str, trend_template: str, openai_api_key: str | None) -> List[Dict]:
    """Return a list of caption dicts: [{text, start, end}] in seconds.

    If OPENAI_API_KEY is not set or API fails, use the heuristic fallback.
    """
    if not openai_api_key:
        return _heuristic_captions(user_prompt, trend_template)

    try:
        # Lazy import to avoid dependency if unused
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)
        system = (
            "You write short, punchy TikTok captions split across 2-4 timed lines. "
            "Return JSON array of objects with fields text, start, end (seconds). "
            "Keep total length under 6 seconds."
        )
        prompt = (
            f"Trend template: {trend_template}\n"
            f"User prompt: {user_prompt}\n"
            "Output only JSON array."
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = resp.choices[0].message.content
        import json

        # Extract JSON array
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            captions: List[Dict] = []
            for item in data:
                txt = str(item.get("text", "")).strip()
                start = float(item.get("start", 0))
                end = float(item.get("end", max(0.5, start + 1.5)))
                captions.append({"text": txt, "start": start, "end": end})
            if captions:
                return captions
    except Exception:
        pass

    return _heuristic_captions(user_prompt, trend_template)


