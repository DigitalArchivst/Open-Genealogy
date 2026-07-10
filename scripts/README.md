# Scripts & Utilities

Python scripts for release packaging and audio transcription.

## Release Packaging

- **generate_chat_edition.py**: Generates the v9.2.0
  [Chat Edition](../research/research-assistant-v9.2.0-chat.md) from the
  [Agent Edition](../skills/gra/SKILL.md) and records immutable hashes for
  both generation inputs. The provenance field `input_commit` names the latest
  clean commit containing both generator inputs; the two LF-normalized hashes
  identify their exact contents.
- **measure_gra_compact.py**: Reports LF-normalized Agent and Chat Edition
  sizes and the 8,000-character chat gate.
- **package_gra_skill.py**: Builds the installable GRA skill ZIP from
  runtime files only.
- **validate_gra_skill_zip.py**: Checks an extracted GRA runtime ZIP for
  required files, broken runtime links, and excluded developer files.

Check the generated v9.2.0 Chat Edition and size gates:

```powershell
python scripts/generate_chat_edition.py --check
python scripts/measure_gra_compact.py
```

Build the v9.2.0 runtime ZIP locally:

```powershell
python scripts/package_gra_skill.py --output dist/gra-skill-v9.2.0.zip
```

The `dist/` directory is ignored by Git; do not commit the ZIP. Extract it to
a temporary directory and validate the runtime package:

```powershell
$stage = Join-Path $env:TEMP "gra-validate-v9.2.0-$PID"
Expand-Archive -LiteralPath dist\gra-skill-v9.2.0.zip -DestinationPath $stage
python scripts/validate_gra_skill_zip.py "$stage\gra"
```

These are offline packaging checks. The API-backed Agent and Chat Edition
fixture gates documented in [skills/gra/tests/README.md](../skills/gra/tests/README.md)
remain separate release requirements.

## Transcription

- **transcribe-4o-chunk-v2.py**: Long-audio transcription with chunking,
  overlap trimming, and privacy defaults. It uploads audio chunks derived from
  the selected media to the OpenAI API for transcription. OpenAI API processing
  incurs charges billed to the account associated with `OPENAI_API_KEY`.
- **batch_transcribe_v2.py**: Batch wrapper that processes a folder of audio
  files sequentially. It does not retain full-audio copies by default. Pass
  `--retain-audio` only when a persistent local MP3 is needed for review or
  recovery: each copy is stored in the selected `transcripts` directory and is
  not deleted automatically. Remove retained copies manually when they are no
  longer needed.

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
