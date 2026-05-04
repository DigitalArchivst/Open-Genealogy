# Scripts & Utilities

Python scripts for release packaging and audio transcription.

## Release Packaging

- **package_gra_skill.py**: Builds the installable GRA skill ZIP from
  runtime files only.
- **validate_gra_skill_zip.py**: Checks an extracted GRA runtime ZIP for
  required files, broken skill links, and excluded developer files.

Build the GRA runtime ZIP:

```powershell
python scripts/package_gra_skill.py
```

Validate an extracted GRA runtime ZIP:

```powershell
python scripts/validate_gra_skill_zip.py C:\tmp\gra-validate-v853\gra
```

## Transcription

- **transcribe-4o-chunk-v2.py**: Long-audio transcription with chunking,
  overlap trimming, and privacy defaults.
- **batch_transcribe_v2.py**: Batch wrapper that processes a folder of audio
  files sequentially.

## Requirements

- Python 3.9+
- `openai`: OpenAI Python SDK
- `pydub`: audio processing
- [FFmpeg](https://ffmpeg.org/): must be on PATH or installed via Chocolatey
  on Windows
- `OPENAI_API_KEY` environment variable set

Install Python dependencies:

```powershell
pip install openai pydub
```

## Previous Versions

- **transcribe-4.py**: Single-file transcription CLI; stable.
- **transcribe-4o-chunk.py**: Long-audio chunking v1; legacy. Use
  `transcribe-4o-chunk-v2.py`.
- **transcribe_v02.py**: Minimal reference implementation; stable.
