# Vireo: Image-to-Video Story Generator

Developed for Hack-Nation's 2nd ever Global AI Hackathon. 


Transform your images into captivating video stories with AI-powered generation. Upload 1-2 images, describe your story, and watch as AI creates a complete video narrative with script, scenes, voiceover, and final assembly.

## Features

- **Image Upload**: Drag & drop 1-2 images for style reference
- **AI Script Generation**: GPT-4o-mini creates compelling story scripts
- **Scene Breakdown**: Automatic scene planning with detailed prompts
- **Video Generation**: RunwayML Gen-2 creates individual scene clips
- **Voice Synthesis**: ElevenLabs generates high-quality narration
- **Video Assembly**: FFmpeg concatenates clips with audio and captions
- **Style Customization**: Choose from 6 different video styles
- **Real-time Preview**: See generated script and scene breakdown
- **Download Ready**: Get your final video in MP4 format

## Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: Next.js, React, Framer Motion, Tailwind CSS
- **AI Services**: OpenAI GPT-4o-mini, RunwayML Gen-2, ElevenLabs
- **Video Processing**: FFmpeg
- **Styling**: Tailwind CSS 

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- FFmpeg installed on your system
- API keys for OpenAI, RunwayML, and ElevenLabs

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Vireo
   ```

2. **Install FFmpeg**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

3. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

5. **Start the Services**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

6. **Open the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## API Keys Setup

1. **OpenAI API Key**
   - Visit https://platform.openai.com/api-keys
   - Create a new API key
   - Add to `.env`: `OPENAI_API_KEY=your_key_here`

2. **RunwayML API Key**
   - Visit https://runwayml.com/
   - Sign up and get your API key
   - Add to `.env`: `RUNWAYML_API_KEY=your_key_here`

3. **ElevenLabs API Key**
   - Visit https://elevenlabs.io/
   - Create an account and get your API key
   - Add to `.env`: `ELEVENLABS_API_KEY=your_key_here`

## Usage

1. **Upload Images**: Drag & drop 1-2 images for style reference
2. **Write Prompt**: Describe what your video should be about
3. **Choose Style**: Select from 6 different video styles
4. **Generate**: Click "Generate Story Video" and wait for processing
5. **Review**: See the generated script and scene breakdown
6. **Download**: Get your final video in MP4 format

## Video Styles

- **Cinematic**: Movie-like dramatic style
- **Animation**: Animated cartoon style
- **Futuristic**: Sci-fi futuristic style
- **Documentary**: Realistic documentary style
- **Artistic**: Creative artistic style
- **Minimalist**: Clean minimalist style

## Project Structure

```
Vireo/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   └── services/
│   │       ├── openai_client.py    # Script & scene generation
│   │       ├── runway_client.py    # Video generation
│   │       ├── elevenlabs_client.py # Voice synthesis
│   │       └── video_assembler.py  # Video assembly
│   ├── public/videos/              # Generated videos
│   ├── temp/                       # Temporary files
│   └── requirements.txt
├── frontend/
│   ├── components/
│   │   ├── ImageUpload.jsx         # Image upload component
│   │   ├── StyleSelector.jsx       # Style selection
│   │   └── StoryGenerator.jsx      # Results display
│   ├── pages/
│   │   └── index.js                # Main application page
│   └── package.json
└── README.md
```

## API Endpoints

- `POST /generate-story`: Generate a complete story video
- `GET /story/{story_id}`: Get story generation status
- `GET /styles`: Get available video styles
- `GET /public/videos/{filename}`: Download generated videos

## Development

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Testing
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

### A few common issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your PATH
   - Test with: `ffmpeg -version`

2. **API Key Errors**
   - Verify all API keys are correctly set in `.env`
   - Check API key permissions and quotas

3. **Video Generation Fails**
   - The system will use placeholder clips if RunwayML fails
   - Check API quotas and network connectivity

4. **Voice Synthesis Fails**
   - ElevenLabs API key may be invalid or quota exceeded
   - Videos will be generated without voiceover

### Performance Tips

- Use smaller images (max 2MB each) for faster processing
- Keep prompts concise but descriptive
- Monitor API usage to avoid rate limits