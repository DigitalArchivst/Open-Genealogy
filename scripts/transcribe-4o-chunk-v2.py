# transcribe-4o-chunk-v2.py

"""
transcribe-4o-chunk-v2.py

Privacy-first, non-breaking successor to transcribe-4o-chunk.py.

Key goals:
- Keep the interactive prompt order compatible with existing batch wrappers.
- Improve reliability and portability (FFmpeg resolution + clearer errors).
- Avoid printing full transcripts by default.
- Use run-scoped system temp storage for audio chunks and clean aggressively.

Environment controls (optional):
- TRANSCRIBE_V2_PRINT_FULL: 0/1 (default: 0)
- TRANSCRIBE_V2_PREVIEW_CHARS: integer (default: 500)
- TRANSCRIBE_V2_KEEP_TEMP: 0/1 (default: 0)

Additional tunables (optional):
- TRANSCRIBE_V2_MAX_MB (default: 24)
- TRANSCRIBE_V2_CHUNK_LENGTH_S (default: 900)
- TRANSCRIBE_V2_OVERLAP_S (default: 10)
- TRANSCRIBE_V2_INITIAL_BITRATE (default: 96k)
- TRANSCRIBE_V2_FALLBACK_BITRATE (default: 64k)
- TRANSCRIBE_V2_MAX_RETRIES (default: 3)
- TRANSCRIBE_V2_RETRY_DELAY_S (default: 5)
- TRANSCRIBE_V2_LANGUAGE (default: en; set to auto to let the model detect language)
"""

from __future__ import annotations

import math
import os
import re
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import openai
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

# Fix Windows console encoding issues without assuming reconfigure always exists.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


TRANSCRIPTION_PROMPT = (
    "Transcribe this audio content accurately and naturally. Pay close attention to speaker changes.\n\n"
    "Instructions:\n"
    "- Preserve the original meaning and tone.\n"
    "- Use appropriate punctuation and capitalization.\n"
    "- Format text for readability.\n"
    "- Indicate unclear speech as [unclear].\n"
    "- CRITICAL FOR SPEAKER IDENTIFICATION:\n"
    "  - When a new person speaks, start their dialogue on a NEW LINE.\n"
    "  - Clearly label each speaker. Use 'Speaker 1:', 'Speaker 2:', etc., or "
    "'Interviewee:', 'Interviewer:' if roles are clear. If names are mentioned, "
    "use them (e.g., 'John:', 'Dr. Smith:').\n"
    "  - Be consistent with speaker labels throughout the transcript.\n"
    "  - Example of speaker change:\n"
    "    Speaker 1: This is the first speaker's dialogue.\n"
    "    Speaker 2: And this is the second speaker starting.\n"
    "- Adapt to any content type (conversations, lectures, interviews, etc.).\n"
    "- Maintain technical terms and proper nouns when identifiable."
)


@dataclass(frozen=True)
class Config:
    max_mb: int
    chunk_length_s: int
    chunk_length_ms: int
    initial_bitrate: str
    fallback_bitrate: str
    language: Optional[str]
    overlap_s: int
    overlap_ms: int
    max_retries: int
    retry_delay_s: int
    print_full_transcript: bool
    preview_chars: int
    keep_temp_chunks: bool


def log_info(message: str) -> None:
    print(f"[INFO] {message}")


def log_warn(message: str) -> None:
    print(f"[WARN] {message}")


def log_error(message: str) -> None:
    print(f"[ERROR] {message}")


def parse_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False

    log_warn(f"{name} must be 0/1 (or true/false). Using default {int(default)}.")
    return default


def parse_int_env(name: str, default: int, minimum: int = 0) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default

    try:
        value = int(raw.strip())
    except ValueError:
        log_warn(f"{name} must be an integer. Using default {default}.")
        return default

    if value < minimum:
        log_warn(f"{name} must be >= {minimum}. Using default {default}.")
        return default

    return value


def parse_bitrate_env(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default

    value = raw.strip().lower()
    if re.fullmatch(r"\d+k", value):
        return value

    log_warn(f"{name} must look like '96k'. Using default {default}.")
    return default


def parse_language_env(name: str, default: str = "en") -> Optional[str]:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default

    value = raw.strip().lower()
    if value in {"auto", "detect", "none", "null"}:
        return None

    # Basic BCP-47 style validation (e.g., en, en-us, pt-br).
    if re.fullmatch(r"[a-z]{2,3}(?:-[a-z0-9]{2,8})*", value):
        return value

    log_warn(f"{name} must be a language tag (e.g., 'en', 'es', 'pt-br') or 'auto'. Using default {default}.")
    return default


def load_config() -> Config:
    max_mb = parse_int_env("TRANSCRIBE_V2_MAX_MB", default=24, minimum=1)
    chunk_length_s = parse_int_env("TRANSCRIBE_V2_CHUNK_LENGTH_S", default=900, minimum=1)
    overlap_s = parse_int_env("TRANSCRIBE_V2_OVERLAP_S", default=10, minimum=0)

    if overlap_s >= chunk_length_s:
        adjusted = max(0, chunk_length_s - 1)
        log_warn(
            "TRANSCRIBE_V2_OVERLAP_S must be less than TRANSCRIBE_V2_CHUNK_LENGTH_S. "
            f"Using {adjusted} instead."
        )
        overlap_s = adjusted

    max_retries = parse_int_env("TRANSCRIBE_V2_MAX_RETRIES", default=3, minimum=1)
    retry_delay_s = parse_int_env("TRANSCRIBE_V2_RETRY_DELAY_S", default=5, minimum=0)

    initial_bitrate = parse_bitrate_env("TRANSCRIBE_V2_INITIAL_BITRATE", default="96k")
    fallback_bitrate = parse_bitrate_env("TRANSCRIBE_V2_FALLBACK_BITRATE", default="64k")
    language = parse_language_env("TRANSCRIBE_V2_LANGUAGE", default="en")

    print_full_transcript = parse_bool_env("TRANSCRIBE_V2_PRINT_FULL", default=False)
    preview_chars = parse_int_env("TRANSCRIBE_V2_PREVIEW_CHARS", default=500, minimum=0)
    keep_temp_chunks = parse_bool_env("TRANSCRIBE_V2_KEEP_TEMP", default=False)

    return Config(
        max_mb=max_mb,
        chunk_length_s=chunk_length_s,
        chunk_length_ms=chunk_length_s * 1000,
        initial_bitrate=initial_bitrate,
        fallback_bitrate=fallback_bitrate,
        language=language,
        overlap_s=overlap_s,
        overlap_ms=overlap_s * 1000,
        max_retries=max_retries,
        retry_delay_s=retry_delay_s,
        print_full_transcript=print_full_transcript,
        preview_chars=preview_chars,
        keep_temp_chunks=keep_temp_chunks,
    )


def resolve_ffmpeg_paths() -> None:
    # Prefer PATH first for portability, then known Chocolatey fallback.
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffprobe = ffprobe_path
        log_info(f"Using FFmpeg from PATH: {ffmpeg_path}")
        return

    fallback_ffmpeg = Path(r"C:\ProgramData\chocolatey\bin\ffmpeg.exe")
    fallback_ffprobe = Path(r"C:\ProgramData\chocolatey\bin\ffprobe.exe")
    if fallback_ffmpeg.exists() and fallback_ffprobe.exists():
        AudioSegment.converter = str(fallback_ffmpeg)
        AudioSegment.ffprobe = str(fallback_ffprobe)
        log_info(f"Using FFmpeg fallback path: {fallback_ffmpeg}")
        return

    raise EnvironmentError(
        "FFmpeg/ffprobe not found. Install FFmpeg and add it to PATH, "
        "or install via Chocolatey so these files exist: "
        "C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe and ffprobe.exe"
    )


def sanitize_filename_component(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name).strip()
    cleaned = cleaned.rstrip(" .")
    return cleaned or "audio"


def normalize_for_overlap(text: str) -> str:
    return re.sub(r"[^\w]+", "", text.lower())


def is_failure_placeholder(text: str) -> bool:
    return text.startswith("===== CHUNK") and "FAILED" in text


def trim_overlap(prev_text: str, current_text: str, max_trim_ratio: float = 0.60) -> Tuple[str, int]:
    """Trim duplicated overlap from current_text based on end of prev_text.

    The max_trim_ratio guard avoids trimming an excessive portion of the new chunk.
    """
    if not prev_text or not current_text:
        return current_text, 0

    prev_tail_orig = prev_text[-400:]
    normalized_prev_tail = normalize_for_overlap(prev_tail_orig)
    current_head_max_len_orig = min(250, len(current_text))

    for k in range(current_head_max_len_orig, 19, -1):
        if k / len(current_text) > max_trim_ratio:
            continue

        current_prefix_orig = current_text[:k]
        normalized_prefix = normalize_for_overlap(current_prefix_orig)
        if len(normalized_prefix) < 10:
            continue

        if normalized_prev_tail.endswith(normalized_prefix):
            return current_text[k:], k

    return current_text, 0


def transcribe_single_audio_chunk(
    chunk_file_path: Path,
    client_instance: openai.OpenAI,
    chunk_num: int,
    total_chunks: int,
    config: Config,
) -> Tuple[Optional[str], int, Optional[str]]:
    """Transcribe one chunk with retries and deterministic logging."""
    last_error: Optional[str] = None

    for attempt in range(1, config.max_retries + 1):
        try:
            with chunk_file_path.open("rb") as audio_file_chunk:
                request_payload = {
                    "model": "gpt-4o-transcribe",
                    "response_format": "json",
                    "file": audio_file_chunk,
                    "prompt": TRANSCRIPTION_PROMPT,
                }
                if config.language:
                    request_payload["language"] = config.language

                transcript_response = client_instance.audio.transcriptions.create(**request_payload)

            log_info(
                f"Chunk {chunk_num}/{total_chunks}: transcription succeeded "
                f"(attempt {attempt}/{config.max_retries})."
            )
            return transcript_response.text, attempt, None

        except openai.APIError as exc:
            last_error = f"APIError: {exc}"
        except Exception as exc:
            last_error = f"{exc.__class__.__name__}: {exc}"

        log_error(
            f"Chunk {chunk_num}/{total_chunks}: transcription failed "
            f"(attempt {attempt}/{config.max_retries}): {last_error}"
        )

        if attempt < config.max_retries and config.retry_delay_s > 0:
            log_info(f"Chunk {chunk_num}/{total_chunks}: retrying in {config.retry_delay_s}s...")
            time.sleep(config.retry_delay_s)

    log_error(f"Chunk {chunk_num}/{total_chunks}: failed after {config.max_retries} attempts.")
    return None, config.max_retries, last_error


def choose_output_base_dir(audio_file_path: Path) -> Path:
    """Preserve prompt order/flow for batch wrapper compatibility."""
    print("\nWhere would you like to save the transcript?")
    print("1. Same directory as the audio file")
    print("2. Same directory as this script")
    print("3. Custom location")
    output_location_choice = input("Enter your choice (1-3) [default: 1]: ").strip()

    if not output_location_choice or output_location_choice not in {"1", "2", "3"}:
        output_location_choice = "1"

    if output_location_choice == "1":
        return audio_file_path.resolve().parent

    if output_location_choice == "2":
        return Path(__file__).resolve().parent

    custom_dir_input = input("Enter the full path to save the transcript: ").strip().strip('"').strip("'")
    if not custom_dir_input:
        log_warn("No directory provided. Using audio file location instead.")
        return audio_file_path.resolve().parent

    try:
        return Path(custom_dir_input).expanduser()
    except Exception as exc:
        log_warn(f"Custom path is invalid ({exc}). Using audio file location instead.")
        return audio_file_path.resolve().parent


def ensure_writable_transcripts_dir(base_dir: Path) -> Path:
    transcripts_dir = base_dir / "transcripts"

    try:
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        test_file = transcripts_dir / ".write_test"
        test_file.write_text("test", encoding="utf-8")
        if test_file.exists():
            test_file.unlink()
        return transcripts_dir
    except (PermissionError, OSError) as exc:
        log_warn(
            f"Cannot write to {transcripts_dir}: {exc}. "
            "Falling back to current working directory."
        )

    fallback_dir = Path.cwd() / "transcripts"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_dir


def show_transcript_summary(final_transcript: str, config: Config) -> None:
    total_chars = len(final_transcript)
    log_info(f"Final transcript length: {total_chars} characters.")

    if config.print_full_transcript:
        print("\n--- Full Transcription ---\n")
        print(final_transcript)
        return

    if config.preview_chars > 0 and total_chars > 0:
        preview = final_transcript[: config.preview_chars]
        if total_chars > config.preview_chars:
            preview += "..."
        print("\n--- Transcript Preview ---\n")
        print(preview)

    log_info("Full transcript printing is disabled by default (set TRANSCRIBE_V2_PRINT_FULL=1 to enable).")


def cleanup_temp_assets(temp_dir: Path, temp_chunk_files: List[Path], keep_temp_chunks: bool) -> None:
    if keep_temp_chunks:
        log_info(f"Keeping temporary chunk files at: {temp_dir}")
        return

    for temp_file in temp_chunk_files:
        if temp_file.exists():
            try:
                temp_file.unlink()
            except Exception as exc:
                log_warn(f"Could not remove temp file {temp_file}: {exc}")

    try:
        shutil.rmtree(temp_dir)
        log_info("Temporary chunk files cleaned up.")
    except Exception as exc:
        log_warn(f"Could not remove temp directory {temp_dir}: {exc}")
        if temp_dir.exists():
            log_warn(f"Temporary files retained at: {temp_dir}")


def main() -> None:
    config = load_config()
    if config.language:
        log_info(f"Transcription language hint: {config.language}")
    else:
        log_info("Transcription language hint disabled (auto-detect mode).")

    temp_dir: Optional[Path] = None
    temp_chunk_files: List[Path] = []

    all_transcripts: List[str] = []
    failed_chunks: List[int] = []
    export_failed_chunks: List[int] = []
    transcribe_failed_chunks: List[int] = []
    successful_chunks = 0
    total_transcribe_attempts = 0

    audio_file_path: Optional[Path] = None

    try:
        audio_file_path_input = input("Enter the full path to your audio file: ").strip()
        audio_file_path_clean = audio_file_path_input.strip('"').strip("'")

        if not audio_file_path_clean:
            raise ValueError("Error: No file path was provided.")

        audio_file_path = Path(audio_file_path_clean).expanduser()
        if not audio_file_path.exists():
            raise FileNotFoundError(f"Error: The file at {audio_file_path} was not found.")

        resolve_ffmpeg_paths()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("Error: The OPENAI_API_KEY environment variable is not set.")

        client = openai.OpenAI(api_key=api_key)

        base_audio_filename = audio_file_path.stem
        safe_base_audio_filename = sanitize_filename_component(base_audio_filename)

        log_info(f"Loading audio: {audio_file_path.name}")
        try:
            full_audio = AudioSegment.from_file(str(audio_file_path))
            log_info("Adding a 0.5s silent leader to stabilize transcription start.")
            full_audio = AudioSegment.silent(duration=500) + full_audio
        except CouldntDecodeError:
            log_error(f"Could not decode audio file: {audio_file_path}")
            log_error("Ensure FFmpeg is installed correctly and the file format is valid.")
            return
        except Exception as exc:
            log_error(f"Error loading audio file with Pydub: {exc}")
            return

        total_duration_s = full_audio.duration_seconds
        total_duration_ms = len(full_audio)
        log_info(f"Audio duration: {total_duration_s:.2f} seconds.")

        if total_duration_ms == 0:
            log_warn("Audio file is empty. Nothing to transcribe.")
            return

        num_chunks = math.ceil(total_duration_ms / config.chunk_length_ms)
        log_info(f"Splitting into {num_chunks} chunk(s) of up to {config.chunk_length_s} seconds each.")

        temp_dir = Path(tempfile.mkdtemp(prefix="transcribe_v2_chunks_"))
        log_info(f"Using temporary chunk directory: {temp_dir}")

        for i in range(num_chunks):
            start_ms = 0 if i == 0 else i * config.chunk_length_ms - config.overlap_ms
            end_ms = min((i + 1) * config.chunk_length_ms, total_duration_ms)
            chunk_audio = full_audio[start_ms:end_ms]

            log_info(
                f"Chunk {i + 1}/{num_chunks}: preparing {((end_ms - start_ms) / 1000):.2f}s segment."
            )

            final_chunk_path: Optional[Path] = None
            try:
                primary_chunk_path = temp_dir / f"temp_{safe_base_audio_filename}_chunk_{i + 1}.mp3"
                chunk_audio.export(str(primary_chunk_path), format="mp3", bitrate=config.initial_bitrate)
                final_chunk_path = primary_chunk_path
                size_mb = final_chunk_path.stat().st_size / (1024 * 1024)
                log_info(
                    f"Chunk {i + 1}/{num_chunks}: export {size_mb:.2f} MB @ {config.initial_bitrate}."
                )

                if size_mb > config.max_mb:
                    log_warn(
                        f"Chunk {i + 1}/{num_chunks}: size exceeds {config.max_mb} MB. "
                        f"Re-encoding @ {config.fallback_bitrate}."
                    )
                    fallback_chunk_path = temp_dir / (
                        f"temp_{safe_base_audio_filename}_chunk_{i + 1}_low.mp3"
                    )
                    chunk_audio.export(
                        str(fallback_chunk_path),
                        format="mp3",
                        bitrate=config.fallback_bitrate,
                    )

                    if primary_chunk_path.exists():
                        try:
                            primary_chunk_path.unlink()
                        except OSError:
                            pass

                    final_chunk_path = fallback_chunk_path
                    size_mb = final_chunk_path.stat().st_size / (1024 * 1024)
                    log_info(
                        f"Chunk {i + 1}/{num_chunks}: export {size_mb:.2f} MB @ {config.fallback_bitrate}."
                    )

                    if size_mb > config.max_mb:
                        log_warn(
                            f"Chunk {i + 1}/{num_chunks}: still above {config.max_mb} MB "
                            f"({size_mb:.2f} MB). Consider reducing TRANSCRIBE_V2_CHUNK_LENGTH_S."
                        )

                temp_chunk_files.append(final_chunk_path)

            except Exception as exc:
                log_error(f"Chunk {i + 1}/{num_chunks}: export failed: {exc}")
                all_transcripts.append(f"===== CHUNK {i + 1}/{num_chunks} FAILED: EXPORT ERROR =====")
                failed_chunks.append(i + 1)
                export_failed_chunks.append(i + 1)
                continue

            if final_chunk_path is None:
                log_error(f"Chunk {i + 1}/{num_chunks}: no chunk file was produced.")
                all_transcripts.append(f"===== CHUNK {i + 1}/{num_chunks} FAILED: NO OUTPUT FILE =====")
                failed_chunks.append(i + 1)
                export_failed_chunks.append(i + 1)
                continue

            transcript_text_of_chunk, attempts_used, failure_reason = transcribe_single_audio_chunk(
                final_chunk_path,
                client,
                i + 1,
                num_chunks,
                config,
            )
            total_transcribe_attempts += attempts_used

            if transcript_text_of_chunk:
                trim_len = 0
                if all_transcripts:
                    prev_transcript_text = all_transcripts[-1]
                    if not is_failure_placeholder(prev_transcript_text):
                        transcript_text_of_chunk, trim_len = trim_overlap(
                            prev_transcript_text,
                            transcript_text_of_chunk,
                        )

                combined = transcript_text_of_chunk.strip()
                all_transcripts.append(combined)
                successful_chunks += 1
                log_info(
                    f"Chunk {i + 1}/{num_chunks}: text {len(combined)} chars "
                    f"(overlap trim: {trim_len} chars)."
                )
            else:
                placeholder = f"===== CHUNK {i + 1}/{num_chunks} FAILED ====="
                all_transcripts.append(placeholder)
                failed_chunks.append(i + 1)
                transcribe_failed_chunks.append(i + 1)
                if failure_reason:
                    log_error(
                        f"Chunk {i + 1}/{num_chunks}: final failure reason: {failure_reason}"
                    )

        final_transcript = "\n\n".join(all_transcripts)

        log_info(
            "Chunk summary: "
            f"total={num_chunks}, "
            f"succeeded={successful_chunks}, "
            f"failed={len(failed_chunks)} "
            f"(export={len(export_failed_chunks)}, transcribe={len(transcribe_failed_chunks)}), "
            f"transcribe_attempts={total_transcribe_attempts}."
        )

        if failed_chunks:
            failed_list = ", ".join(str(chunk_num) for chunk_num in failed_chunks)
            log_warn(f"Failed chunk indices: {failed_list}")

        show_transcript_summary(final_transcript, config)

        base_dir = choose_output_base_dir(audio_file_path)
        transcripts_dir = ensure_writable_transcripts_dir(base_dir)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        transcript_filename = f"transcript_{safe_base_audio_filename}_{current_time}.txt"
        transcript_file_path = transcripts_dir / transcript_filename

        transcript_file_path.write_text(final_transcript, encoding="utf-8")
        log_info(f"Transcript saved to {transcript_file_path.resolve()}")

    except openai.APIError as exc:
        log_error(f"An OpenAI API error occurred: {exc}")
    except openai.OpenAIError as exc:
        log_error(f"An OpenAI client error occurred: {exc}")
    except FileNotFoundError as exc:
        log_error(str(exc))
    except ValueError as exc:
        log_error(str(exc))
    except EnvironmentError as exc:
        log_error(str(exc))
    except Exception as exc:
        log_error(f"An unexpected error occurred in the main process: {exc}")
    finally:
        if temp_dir is not None:
            cleanup_temp_assets(temp_dir, temp_chunk_files, config.keep_temp_chunks)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log_error(f"A critical error occurred: {exc}")
        log_error("The script will now exit.")
