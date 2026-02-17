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

Notes:
- OPENAI_API_KEY and FFmpeg must be set up as required by transcribe-4o-chunk-v2.py.
- The output choice (-o) applies to the whole batch. If -o 3 is used, -d is required.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Set
from pydub import AudioSegment


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


def _ensure_ffmpeg_paths() -> None:
    """Resolve ffmpeg for Pydub (PATH first, then Chocolatey fallback)."""
    ffmpeg_in_path = shutil.which('ffmpeg')
    ffprobe_in_path = shutil.which('ffprobe')
    if ffmpeg_in_path and ffprobe_in_path:
        AudioSegment.converter = ffmpeg_in_path
        AudioSegment.ffprobe = ffprobe_in_path
        return

    fallback_ffmpeg = Path(r"C:\ProgramData\chocolatey\bin\ffmpeg.exe")
    fallback_ffprobe = Path(r"C:\ProgramData\chocolatey\bin\ffprobe.exe")
    if fallback_ffmpeg.exists() and fallback_ffprobe.exists():
        AudioSegment.converter = str(fallback_ffmpeg)
        AudioSegment.ffprobe = str(fallback_ffprobe)
        return

    print('      (audio) WARNING: ffmpeg/ffprobe not found. Full MP3 extraction may fail.')


def _extract_full_audio(audio: Path, dest_dir: Path, bitrate: str = '96k') -> Optional[Path]:
    """Extract and save one full MP3 for the input file into dest_dir.

    Skips if the output already exists.
    """
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        out_path = dest_dir / f"audio_{_sanitize_filename_component(audio.stem)}.mp3"
        if out_path.exists():
            print(f"      (audio) Exists: {out_path.name}")
            return out_path
        seg = AudioSegment.from_file(str(audio))
        seg.export(str(out_path), format='mp3', bitrate=bitrate)
        print(f"      (audio) Saved: {out_path.name}")
        return out_path
    except KeyboardInterrupt:
        raise
    except Exception as e:
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

    # Ensure Pydub can find ffmpeg like the transcriber
    _ensure_ffmpeg_paths()

    total = len(files)
    print(f'Discovered {total} file(s). Running sequentially...\n')

    ok = skipped = failed = 0
    for i, f in enumerate(files, 1):
        if args.skip_existing and _has_transcript(f, args.output_choice, args.custom_output_dir, transcriber):
            print(f'[{i}/{total}] SKIP: {f.name} (already has transcript)')
            skipped += 1
            continue
        print(f'[{i}/{total}] START: {f}')
        # Pre-create transcripts directory and save one full MP3 per file
        tdir = _transcripts_dir_for(f, args.output_choice, args.custom_output_dir, transcriber)
        _extract_full_audio(f, tdir)
        rc = _run_one(transcriber, f, args.output_choice, args.custom_output_dir)
        if rc == 0:
            print(f'[{i}/{total}] OK: {f.name}\n')
            ok += 1
        else:
            print(f'[{i}/{total}] FAIL ({rc}): {f.name}\n')
            failed += 1

    print(f'Finished. ok={ok}, skipped={skipped}, failed={failed}, total={total}')


if __name__ == '__main__':
    main()
