#!/usr/bin/env python3
"""
Batch wrapper for transcribe-4o-chunk-v2.py (Windows-friendly)

- Discovers media files in a folder (optionally recursive)
- Calls transcribe-4o-chunk-v2.py for each file, auto-answering its prompts
  (file path, output location, and custom dir if needed)
- Can skip processing when a transcript already exists for a given file

Usage:
  # If run without an input folder arg, you'll be prompted for it
  python batch_transcribe_v2.py

  # With explicit folder
  python batch_transcribe_v2.py "C:\\path\\to\\folder"

  # Recursive, multiple patterns, and skip existing
  python batch_transcribe_v2.py "C:\\path\\to\\folder" -r -s

  # Save transcripts next to transcriber (choice 2)
  python batch_transcribe_v2.py "C:\\path\\to\\folder" -o 2

  # Save to custom directory (choice 3)
  python batch_transcribe_v2.py "C:\\path\\to\\folder" -o 3 -d "C:\\path\\to\\output"

  # Opt in to retaining a full MP3 with each transcript
  python batch_transcribe_v2.py "C:\\path\\to\\folder" --retain-audio

Notes:
- OPENAI_API_KEY and FFmpeg must be set up as required by transcribe-4o-chunk-v2.py.
- The output choice (-o) applies to the whole batch. If -o 3 is used, -d is required.
- Full-audio MP3 copies are not retained by default. --retain-audio stores a copy in
  the selected transcripts directory for local review or recovery; retained copies
  are not deleted automatically and must be removed manually when no longer needed.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Set

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None


def _split_patterns(args: Optional[List[str]]) -> List[str]:
    pats: List[str] = []
    for a in (args or []):
        pats.extend([p.strip() for p in a.split(',') if p.strip()])
    return pats or ['*.mp3', '*.mp4', '*.m4a', '*.wav', '*.flac', '*.ogg', '*.webm']


def _sanitize_filename_component(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name).strip()
    cleaned = cleaned.rstrip(' .')
    return cleaned or 'audio'


def _find_files(root: Path, patterns: List[str], recursive: bool) -> List[Path]:
    found: Set[Path] = set()
    for pat in patterns:
        it = root.rglob(pat) if recursive else root.glob(pat)
        for p in it:
            if p.is_file():
                found.add(p)
    return sorted(found)


def _transcripts_dir_for(audio: Path, choice: str, custom_dir: Optional[Path], transcriber: Path) -> Path:
    if choice == '1':
        base = audio.parent
    elif choice == '2':
        base = transcriber.parent
    else:
        base = custom_dir if custom_dir else audio.parent
    return (base / 'transcripts').resolve()


def _has_transcript(audio: Path, choice: str, custom_dir: Optional[Path], transcriber: Path) -> bool:
    tdir = _transcripts_dir_for(audio, choice, custom_dir, transcriber)
    if not tdir.exists():
        return False
    prefix = f'transcript_{_sanitize_filename_component(audio.stem)}_'
    try:
        for child in tdir.iterdir():
            if child.is_file() and child.suffix.lower() == '.txt' and child.name.startswith(prefix):
                return True
    except Exception:
        return False
    return False


def _ensure_ffmpeg_paths() -> bool:
    """Resolve ffmpeg for Pydub (PATH first, then Chocolatey fallback)."""
    if AudioSegment is None:
        print('      (audio) ERROR: pydub is required for --retain-audio. Install it with: pip install pydub')
        return False

    ffmpeg_in_path = shutil.which('ffmpeg')
    ffprobe_in_path = shutil.which('ffprobe')
    if ffmpeg_in_path and ffprobe_in_path:
        AudioSegment.converter = ffmpeg_in_path
        AudioSegment.ffprobe = ffprobe_in_path
        return True

    fallback_ffmpeg = Path(r"C:\ProgramData\chocolatey\bin\ffmpeg.exe")
    fallback_ffprobe = Path(r"C:\ProgramData\chocolatey\bin\ffprobe.exe")
    if fallback_ffmpeg.exists() and fallback_ffprobe.exists():
        AudioSegment.converter = str(fallback_ffmpeg)
        AudioSegment.ffprobe = str(fallback_ffprobe)
        return True

    print('      (audio) WARNING: ffmpeg/ffprobe not found. Full MP3 extraction may fail.')
    return False


def _extract_full_audio(audio: Path, dest_dir: Path, bitrate: str = '96k') -> Optional[Path]:
    """Extract and save one full MP3 for the input file into dest_dir.

    Skips only a prior export with its completion marker. Export through a
    temporary file so an interrupted conversion cannot look successful later.
    """
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        out_path = dest_dir / f"audio_{_sanitize_filename_component(audio.stem)}.mp3"
        marker_path = out_path.with_name(out_path.name + ".ok")
        if out_path.is_file() and marker_path.is_file():
            print(f"      (audio) Exists: {out_path.name}")
            return out_path
        temp_path = out_path.with_name(out_path.name + ".tmp")
        temp_path.unlink(missing_ok=True)
        seg = AudioSegment.from_file(str(audio))
        seg.export(str(temp_path), format='mp3', bitrate=bitrate)
        if not temp_path.is_file() or temp_path.stat().st_size == 0:
            raise RuntimeError("export produced no audio bytes")
        temp_path.replace(out_path)
        marker_path.write_text("complete\n", encoding="ascii")
        print(f"      (audio) Saved: {out_path.name}")
        return out_path
    except KeyboardInterrupt:
        raise
    except Exception as e:
        if 'temp_path' in locals():
            temp_path.unlink(missing_ok=True)
        print(f"      (audio) Failed to save full MP3: {e}")
        return None


def _run_one(transcriber: Path, audio: Path, choice: str, custom_dir: Optional[Path]) -> int:
    # Build input payload that the transcriber expects across prompts
    lines = [str(audio), choice]
    if choice == '3':
        lines.append(str(custom_dir if custom_dir else audio.parent))
    payload = '\n'.join(lines) + '\n'

    cmd = [sys.executable, '-u', str(transcriber)]  # -u for unbuffered output
    try:
        # Use Popen to stream output in real-time instead of buffering
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=None,  # Inherit stdout - shows progress in real-time
            stderr=None,  # Inherit stderr
            text=True,
            cwd=str(transcriber.parent)
        )
        proc.communicate(input=payload)
        return proc.returncode
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[ERROR] Failed for {audio}: {e}")
        return 1


def _process_batch(
    files: List[Path],
    *,
    transcriber: Path,
    output_choice: str,
    custom_output_dir: Optional[Path],
    skip_existing: bool,
    retain_audio: bool,
    run_one=_run_one,
) -> tuple[int, int, int]:
    """Run one batch and return successful, skipped, and failed file counts."""
    ok = skipped = failed = 0
    total = len(files)
    for i, audio in enumerate(files, 1):
        if skip_existing and _has_transcript(audio, output_choice, custom_output_dir, transcriber):
            print(f'[{i}/{total}] SKIP: {audio.name} (already has transcript)')
            skipped += 1
            continue

        print(f'[{i}/{total}] START: {audio}')
        if retain_audio:
            retained_audio_dir = _transcripts_dir_for(
                audio,
                output_choice,
                custom_output_dir,
                transcriber,
            )
            retained = _extract_full_audio(audio, retained_audio_dir)
            if retained is None:
                print(
                    f'[{i}/{total}] FAIL: {audio.name} '
                    '(required retained-audio extraction failed)\n'
                )
                failed += 1
                continue

        rc = run_one(transcriber, audio, output_choice, custom_output_dir)
        if rc == 0:
            print(f'[{i}/{total}] OK: {audio.name}\n')
            ok += 1
        else:
            print(f'[{i}/{total}] FAIL ({rc}): {audio.name}\n')
            failed += 1

    return ok, skipped, failed


def main() -> None:
    ap = argparse.ArgumentParser(description='Batch wrapper for transcribe-4o-chunk-v2.py')
    ap.add_argument('input_dir', type=Path, nargs='?', help='Folder with media files (prompted if omitted)')
    ap.add_argument('-p', '--pattern', action='append', default=None,
                    help='Glob pattern(s) (repeat or comma-separated). Default: mp3,mp4,m4a,wav,flac,ogg,webm')
    ap.add_argument('-r', '--recursive', action='store_true', help='Recurse into subfolders')
    ap.add_argument('-o', '--output-choice', choices=['1', '2', '3'], default='1',
                    help='1=next to audio, 2=next to transcriber, 3=custom dir')
    ap.add_argument('-d', '--custom-output-dir', type=Path, default=None,
                    help='Required if -o 3 (custom)')
    ap.add_argument('-s', '--skip-existing', action='store_true', help='Skip if transcript already exists')
    ap.add_argument(
        '--retain-audio',
        action='store_true',
        help=(
            'Opt in to full MP3 copies in the selected transcripts directory for '
            'local review or recovery; copies are not deleted automatically.'
        ),
    )
    ap.add_argument('--transcriber', type=Path, default=None,
                    help='Path to transcribe-4o-chunk-v2.py (defaults to sibling)')
    args = ap.parse_args()

    # Interactive prompt for folder if not provided
    if not args.input_dir:
        user_in = input('Enter the full path to the folder of media files: ').strip().strip('"').strip("'")
        if not user_in:
            ap.error('No folder provided.')
        args.input_dir = Path(user_in)

    root = args.input_dir.expanduser().resolve()
    if not root.is_dir():
        ap.error(f'Not a directory: {root}')

    patterns = _split_patterns(args.pattern)

    transcriber = args.transcriber or Path(__file__).with_name('transcribe-4o-chunk-v2.py')
    if not transcriber.exists():
        ap.error(f'Transcriber not found: {transcriber}')

    if args.output_choice == '3' and not args.custom_output_dir:
        ap.error('Custom output dir (-d) is required when -o 3')

    files = _find_files(root, patterns, args.recursive)
    if not files:
        print('No files found.')
        return

    if args.retain_audio and not _ensure_ffmpeg_paths():
        ap.error('--retain-audio requires pydub plus ffmpeg and ffprobe.')

    total = len(files)
    print(f'Discovered {total} file(s). Running sequentially...\n')
    if args.retain_audio:
        print(
            'Full-audio retention enabled: MP3 copies will be kept in the selected '
            'transcripts directory until you remove them.\n'
        )

    ok, skipped, failed = _process_batch(
        files,
        transcriber=transcriber,
        output_choice=args.output_choice,
        custom_output_dir=args.custom_output_dir,
        skip_existing=args.skip_existing,
        retain_audio=args.retain_audio,
    )

    print(f'Finished. ok={ok}, skipped={skipped}, failed={failed}, total={total}')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main() or 0)
