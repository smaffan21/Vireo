# Vireo Backend

Setup:
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
- GET /trends
- POST /generate-video


