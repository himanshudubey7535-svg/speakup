# SpeakUp – 1 Minute Vocabulary Challenge

A speech practice app that gives you a random difficult word, records you speaking about it for 1 minute, and uses AI to analyze fluency, grammar, pronunciation, confidence, vocabulary, and filler words — plus non-verbal engagement cues from your camera (eye contact, stillness, expression).

## Features
- Random difficult-word prompts with pronunciation, meaning, and difficulty level
- 10-minute preparation timer, 15-second think timer, 60-second speak timer — each with an animated circular countdown
- In-browser microphone recording during the speak window
- AI-powered speech analysis: fluency, grammar, vocabulary, pronunciation, filler-word detection
- Non-verbal engagement analysis via webcam: eye contact, stillness, expression cues (not personality detection)
- Combined soft-skills score (weighted audio + camera signals)
- Session history and progress tracking (planned)
- Dark mode toggle (planned)

## Tech Stack
- **App**: Streamlit (Python) — unified frontend + backend logic
- **Speech-to-text**: OpenAI Whisper
- **AI analysis**: LLM-based grammar/vocabulary/confidence scoring
- **Camera analysis**: OpenCV / MediaPipe for face detection and engagement tracking
- **Database**: PostgreSQL with SQLAlchemy
- **Storage**: AWS S3 (audio files)
- **CI/CD**: GitHub Actions
- **Deployment**: Streamlit Community Cloud / Render (planned)

## Status
🚧 In active development — 60-day build plan, currently mid-build.

## Roadmap
See `ROADMAP.md` for the full day-by-day build plan.

## Local Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
streamlit run app.py
```