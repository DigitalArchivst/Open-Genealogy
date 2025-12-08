# transcribe-4o-chunk.py

"""
transcribe-4o-chunk.py

A user-friendly script for transcribing large audio files using OpenAI's
GPT-4o-transcribe model by chunking them into manageable pieces.

METADATA:
--------
TITLE: transcribe-4o-chunk.py
CREATOR: Steve Little; https://AIGenealogyInsights.com/
ADAPTED FOR GPT-4o & CHUNKING: Cascade AI (with user guidance)
DATE: Original Friday 15 December 2023, Adapted 2025-06-18
VERSION: 4o.2-chunk (2025-06-18)
LICENSE: This work is licensed under a Creative Commons BY-NC 4.0 License.

This script allows users to transcribe audio files, automatically handling
large files by splitting them into smaller chunks. It sends each chunk to
OpenAI's GPT-4o-transcribe model, retries failed chunks, and then
combines the transcriptions.

For license terms, visit: https://creativecommons.org/licenses/by-nc/4.0/
"""
# **Prerequisites**:
# 1. Install Python 3.8 or higher.
# 2. Install required Python libraries:
#    Run this command in your terminal or command prompt:
#    `pip install --upgrade openai pydub`
# 3. Install FFmpeg:
#    - Pydub requires FFmpeg for MP3 processing.
#    - Download from https://ffmpeg.org/download.html and install it.
#    - Ensure ffmpeg executable is in your system's PATH.
#      Test by typing `ffmpeg -version` in your terminal.
# 4. Obtain your OpenAI API key from https://platform.openai.com/.
# 5. Set your API key as an environment variable:
#    - On Windows: Run `set OPENAI_API_KEY=your_api_key` in your command prompt.
#    - On macOS/Linux: Run `export OPENAI_API_KEY=your_api_key` in your terminal.
#
# **Steps to Run the Script**:
# 1. Prepare your audio file (e.g., flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm).
# 2. Run the script. When prompted:
#    - Enter the full file path to your audio file.
#
# **Output**:
# - The transcription text will be printed to the console.
# - A copy will be saved as a .txt file in a folder named `transcripts`.

import openai
from datetime import datetime
import os
import math
import time
import shutil
import re
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

# --- Explicitly set FFmpeg and FFprobe paths for Pydub ---
# This is necessary if Pydub can't find them in the system's PATH.
# The paths below are based on a Chocolatey installation.
AudioSegment.converter = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ProgramData\chocolatey\bin\ffprobe.exe"

DEBUG = False  # set to True to see internal FFmpeg path diagnostics
if DEBUG:
    print("\n--- SCRIPT DEBUG INFO ---")
    print(f"Pydub converter path explicitly set to: {AudioSegment.converter}")
    print(f"Pydub ffprobe path explicitly set to: {AudioSegment.ffprobe}")
    print("-------------------------\n")

# --- Configuration ---
# Max duration for each chunk in seconds (OpenAI's gpt-4o-transcribe limit is ~1500s for some setups)
# We use a slightly lower value for safety.
# Robust chunk settings
MAX_MB = 24                    # keep each chunk < 24 MB to stay under 25 MB cap
CHUNK_LENGTH_S = 900           # 15-minute chunks -> ~11 MB @ 96 kb/s
CHUNK_LENGTH_MS = CHUNK_LENGTH_S * 1000
INITIAL_BITRATE = "96k"        # first export bitrate
FALLBACK_BITRATE = "64k"       # fallback if size still too large

# Overlap between consecutive chunks to avoid cutting mid-sentence
OVERLAP_S  = 10                  # seconds to overlap
OVERLAP_MS = OVERLAP_S * 1000
MAX_RETRIES = 3  # Number of retries for a failed chunk transcription
RETRY_DELAY_S = 5  # Seconds to wait before retrying a chunk
AUTO_DELETE_TEMP_CHUNKS = True

# --- Transcription Prompt ---
# A prompt to guide the model on context, style, and vocabulary.
TRANSCRIPTION_PROMPT = (
    "Transcribe this audio content accurately and naturally. Pay close attention to speaker changes.\n\n"
    "Instructions:\n"
    "- Preserve the original meaning and tone.\n"
    "- Use appropriate punctuation and capitalization.\n"
    "- Format text for readability.\n"
    "- Indicate unclear speech as [unclear].\n"
    "- **CRITICAL FOR SPEAKER IDENTIFICATION:**\n"
    "  - When a new person speaks, start their dialogue on a NEW LINE.\n"
    "  - Clearly label each speaker. Use 'Speaker 1:', 'Speaker 2:', etc., or 'Interviewee:', 'Interviewer:' if roles are clear. If names are mentioned, use them (e.g., 'John:', 'Dr. Smith:').\n"
    "  - Be consistent with speaker labels throughout the transcript.\n"
    "  - Example of speaker change:\n"
    "    Speaker 1: This is the first speaker's dialogue.\n"
    "    Speaker 2: And this is the second speaker starting.\n"
    "- Adapt to any content type (conversations, lectures, interviews, etc.).\n"
    "- Maintain technical terms and proper nouns when identifiable."
)

# Ensure the API key is set in the environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("Error: The OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI client
# The API key is automatically picked up from the OPENAI_API_KEY environment variable.
client = openai.OpenAI()

def transcribe_single_audio_chunk(chunk_file_path, client_instance, chunk_num, total_chunks):
    """
    Transcribes a single audio chunk using the OpenAI API with retry logic.
    """
    
    for attempt in range(MAX_RETRIES):
        try:
            with open(chunk_file_path, "rb") as audio_file_chunk:
                transcript_response = client_instance.audio.transcriptions.create(
                    model="gpt-4o-transcribe",
                    response_format="json",  # gpt-4o-transcribe only supports json
                    file=audio_file_chunk,
                    prompt=TRANSCRIPTION_PROMPT,
                    language="en"
                )
            print(f"  🎤 Transcribe: ✔️ (attempt {attempt + 1})")
            return transcript_response.text
        except openai.APIError as e:
            print(f"  🎤 Transcribe: ❌ API Error (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"      Retrying in {RETRY_DELAY_S}s...")
                time.sleep(RETRY_DELAY_S)
            else:
                print(f"  🎤 Transcribe: 💀 Failed after {MAX_RETRIES} attempts (API Error).")
                return None # Failed after all retries
        except Exception as e:
            print(f"  🎤 Transcribe: ❌ Unexpected Error (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"      Retrying in {RETRY_DELAY_S}s...")
                time.sleep(RETRY_DELAY_S)
            else:
                print(f"  🎤 Transcribe: 💀 Failed after {MAX_RETRIES} attempts (Unexpected Error).")
                return None # Failed after all retries
    return None


def main():
    # Prompt user to enter the audio file path
    audio_file_path_input = input("Enter the full path to your audio file: ").strip()

    # Remove extra quotes if present
    audio_file_path = audio_file_path_input.strip('"').strip("'")

    # Ensure the file path is provided and exists
    if not audio_file_path:
        raise ValueError("Error: No file path was provided.")
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Error: The file at {audio_file_path} was not found.")

    base_audio_filename = os.path.splitext(os.path.basename(audio_file_path))[0]
    all_transcripts = []
    temp_chunk_files = []

    try:
        print(f"\n⏳ Loading audio: {os.path.basename(audio_file_path)}...")
        if DEBUG:
            print(f"--- DEBUG: Pydub is about to use converter: {AudioSegment.converter} ---")
        try:
            full_audio = AudioSegment.from_file(audio_file_path)  # from_file handles various formats

            print("Adding a 0.5s silent leader to stabilize transcription start...")
            silent_leader = AudioSegment.silent(duration=500)  # 500 milliseconds of silence
            full_audio = silent_leader + full_audio
        except CouldntDecodeError:
            print(f"Error: Could not decode audio file: {audio_file_path}.")
            print("Please ensure FFmpeg is installed correctly and the file is a valid audio format.")
            return
        except Exception as e:
            print(f"Error loading audio file with Pydub: {e}")
            return
            
        total_duration_s = full_audio.duration_seconds
        total_duration_ms = len(full_audio)
        print(f"Audio duration: {total_duration_s:.2f} seconds.")

        num_chunks = math.ceil(total_duration_ms / CHUNK_LENGTH_MS)
        if num_chunks == 0 and total_duration_ms > 0 : # handle very short files
            num_chunks = 1
        
        print(f"Splitting into {num_chunks} chunk(s) of up to {CHUNK_LENGTH_S} seconds each.")

        if num_chunks == 0 and total_duration_ms == 0:
            print("Audio file is empty. Nothing to transcribe.")
            return

        for i in range(num_chunks):
            if i == 0:
                start_ms = 0
            else:
                start_ms = i * CHUNK_LENGTH_MS - OVERLAP_MS
            end_ms = min((i + 1) * CHUNK_LENGTH_MS, total_duration_ms)
            chunk_audio = full_audio[start_ms:end_ms]

            # Create a temporary directory for chunks if it doesn't exist
            temp_dir = os.path.join(os.path.dirname(audio_file_path), "temp_audio_chunks")
            os.makedirs(temp_dir, exist_ok=True)
            
            temp_chunk_path = os.path.join(temp_dir, f"temp_{base_audio_filename}_chunk_{i+1}.mp3")
            temp_chunk_files.append(temp_chunk_path)

            print(f"\n--- 🧩 Chunk {i+1}/{num_chunks} ({((end_ms - start_ms)/1000):.2f}s) ---")
            try:
                # first export at INITIAL_BITRATE
                chunk_audio.export(temp_chunk_path, format="mp3", bitrate=INITIAL_BITRATE)
                size_mb = os.path.getsize(temp_chunk_path) / (1024*1024)
                print(f"  💿 Export: {size_mb:.2f} MB @ {INITIAL_BITRATE}")
                if size_mb > MAX_MB:
                    print(f"  ⚠️ Size > {MAX_MB}MB, re-encoding @ {FALLBACK_BITRATE}...")
                    smaller_path = temp_chunk_path.replace('.mp3', '_low.mp3')
                    chunk_audio.export(smaller_path, format='mp3', bitrate=FALLBACK_BITRATE)
                    os.remove(temp_chunk_path)
                    temp_chunk_path = smaller_path
                    size_mb = os.path.getsize(temp_chunk_path) / (1024*1024)
                    print(f"  💿 Export (fallback): {size_mb:.2f} MB @ {FALLBACK_BITRATE}")
                    if size_mb > MAX_MB:
                        print(f"  🔥 Warning: Still > {MAX_MB}MB ({size_mb:.2f}MB). Consider reducing CHUNK_LENGTH_S.")
            except Exception as e:
                print(f"  ❌ Export Error: {e}")
                all_transcripts.append(f"[Error exporting chunk {i+1}: {e}]") # Add error to transcript
                continue # Skip to next chunk

            transcript_text_of_chunk = transcribe_single_audio_chunk(
                temp_chunk_path, client, i + 1, num_chunks
            )

            if transcript_text_of_chunk:
                # Trim leading overlap duplication
                trim_len = 0  # default
                if all_transcripts: # Check if there's a previous transcript to compare with
                    prev_transcript_text = all_transcripts[-1]
                    # Max length of the suffix of previous transcript to consider for matching (original characters)
                    prev_tail_max_len_orig = 400
                    prev_tail_orig = prev_transcript_text[-prev_tail_max_len_orig:]
                    
                    # Normalize the tail of the previous transcript
                    normalized_prev_tail = prev_tail_orig.lower()
                    normalized_prev_tail = re.sub(r'[^\w]+', '', normalized_prev_tail)

                    # Max length of the prefix of current transcript to consider for matching (original characters)
                    current_head_max_len_orig = min(250, len(transcript_text_of_chunk))

                    # Iterate from longer potential overlaps to shorter ones
                    # k is the length of the ORIGINAL prefix of the current chunk
                    for k in range(current_head_max_len_orig, 19, -1): # Min original check length 20 chars
                        current_chunk_original_prefix = transcript_text_of_chunk[:k]
                        
                        # Normalize this prefix
                        normalized_current_prefix = current_chunk_original_prefix.lower()
                        normalized_current_prefix = re.sub(r'[^\w]+', '', normalized_current_prefix)

                        # If normalized prefix is too short (e.g., less than 2-3 words), skip
                        if len(normalized_current_prefix) < 10: 
                            continue

                        if normalized_prev_tail.endswith(normalized_current_prefix):
                            trim_len = k # k is the length of the ORIGINAL prefix to be trimmed
                            break
                    
                    if trim_len:
                        transcript_text_of_chunk = transcript_text_of_chunk[trim_len:]

                combined = transcript_text_of_chunk.strip()
                print(f"  📝 Text obtained: {len(transcript_text_of_chunk)} chars (overlap trim: {trim_len} chars)")
                all_transcripts.append(combined)
            else:
                # Placeholder so the gap is obvious in the final text
                placeholder = f"===== CHUNK {i+1}/{num_chunks} FAILED ====="
                all_transcripts.append(placeholder)

        # Combine transcripts
        final_transcript = "\n\n".join(all_transcripts) # Use double newline to separate chunk texts

        # Print the final transcript to the console
        print("\n--- Full Transcription ---:\n")
        print(final_transcript)

        # --- Save the transcript ---
        # Ask user for output location preference
        print("\nWhere would you like to save the transcript?")
        print("1. Same directory as the audio file")
        print("2. Same directory as this script")
        print("3. Custom location")
        output_location_choice = input("Enter your choice (1-3) [default: 1]: ").strip()
        if not output_location_choice or output_location_choice not in ["1", "2", "3"]:
            output_location_choice = "1"

        if output_location_choice == "1":
            base_dir = os.path.dirname(os.path.abspath(audio_file_path))
        elif output_location_choice == "2":
            base_dir = os.path.dirname(os.path.abspath(__file__))
        else: # Custom location
            custom_dir_input = input("Enter the full path to save the transcript: ").strip().strip('"').strip("'")
            if not custom_dir_input:
                print("No directory provided, using audio file location instead.")
                base_dir = os.path.dirname(os.path.abspath(audio_file_path))
            else:
                base_dir = custom_dir_input
        
        transcripts_dir = os.path.join(base_dir, "transcripts")

        try:
            os.makedirs(transcripts_dir, exist_ok=True)
            test_file = os.path.join(transcripts_dir, ".write_test")
            with open(test_file, "w") as f: f.write("test")
            os.remove(test_file)
        except (PermissionError, OSError) as e:
            print(f"Cannot write to {transcripts_dir}: {e}. Falling back to current working directory...")
            transcripts_dir = os.path.join(os.getcwd(), "transcripts")
            os.makedirs(transcripts_dir, exist_ok=True)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        transcript_filename = f"transcript_{base_audio_filename}_{current_time}.txt"
        transcript_file_path = os.path.join(transcripts_dir, transcript_filename)

        with open(transcript_file_path, "w", encoding='utf-8') as file:
            file.write(final_transcript)
        print(f"\nTranscript saved to {os.path.abspath(transcript_file_path)}")

    except openai.APIError as e:
        print(f"An API error occurred: {e}")
        if hasattr(e, 'code') and e.code: print(f"Error code: {e.code}")
        if hasattr(e, 'message') and e.message: print(f"Error message: {e.message}")
    except openai.OpenAIError as e:
        print(f"An error occurred with the OpenAI API: {e}")
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except EnvironmentError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred in the main process: {e}")
    finally:
        if AUTO_DELETE_TEMP_CHUNKS:
            print("\nCleaning up temporary chunk files...")
            for temp_file in temp_chunk_files:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)

                    except Exception as e:
                        print(f"  Error deleting {temp_file}: {e}")
            # Attempt to remove the temporary directory (handles hidden OneDrive files)
            temp_chunk_dir = os.path.join(os.path.dirname(audio_file_path), "temp_audio_chunks")
            if os.path.exists(temp_chunk_dir):
                try:
                    shutil.rmtree(temp_chunk_dir, ignore_errors=True)

                except Exception as e:
                    print(f"  Error deleting temporary directory {temp_chunk_dir}: {e}")

            print("Done.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e: # Catch-all for any unhandled exception in main to prevent abrupt exit
        print(f"A critical error occurred: {e}")
        print("The script will now exit.")
