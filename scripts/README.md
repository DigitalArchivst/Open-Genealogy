# Scripts & Utilities

Python scripts for audio transcription using OpenAI's transcription API.

## Recommended

| Script | Description |
|--------|-------------|
| **transcribe-4o-chunk-v2.py** | Long-audio transcription with chunking, overlap trimming, and privacy defaults |
| **batch_transcribe_v2.py** | Batch wrapper — process a folder of audio files sequentially |

## Requirements

- Python 3.9+
- `openai` — OpenAI Python SDK
- `pydub` — audio processing
- [FFmpeg](https://ffmpeg.org/) — must be on PATH or installed via Chocolatey (Windows)
- `OPENAI_API_KEY` environment variable set

Install Python dependencies:

```
pip install openai pydub
```

## Previous Versions

| Script | Description | Status |
|--------|-------------|--------|
| transcribe-4.py | Single-file transcription CLI | stable |
| transcribe-4o-chunk.py | Long-audio chunking (v1) | legacy — use transcribe-4o-chunk-v2.py |
| transcribe_v02.py | Minimal reference implementation | stable |
