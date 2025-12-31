"""
transcribe-4.py

A user-friendly script for transcribing audio files using OpenAI's Whisper model.

METADATA:
--------
TITLE: transcribe-4.py
CREATOR: Steve Little; https://AIGenealogyInsights.com/
DATE: Friday 15 December 2023
VERSION: 4 (2025-03-13)
LICENSE: This work is licensed under a Creative Commons BY-NC 4.0 License.

This script allows users to easily transcribe audio files using OpenAI's Whisper
model. It handles the entire process from file input to saving the transcription,
with clear error handling and user guidance throughout.

For license terms, visit: https://creativecommons.org/licenses/by-nc/4.0/
"""
# **Prerequisites**:
# 1. Install Python 3.8 or higher.
# 2. Install the OpenAI Python library:
#    Run this command in your terminal or command prompt: `pip install openai`.
# 3. Obtain your OpenAI API key from https://platform.openai.com/.
# 4. Set your API key as an environment variable:
#    - On Windows: Run `set OPENAI_API_KEY=your_api_key` in your command prompt.
#    - On macOS/Linux: Run `export OPENAI_API_KEY=your_api_key` in your terminal.
#
# **Steps to Run the Script**:
# 1. Prepare your audio file:
#    - Ensure the file is in a supported format (e.g., MP3, WAV).
#    - Ensure the file is smaller than 25 MB.
# 2. Run the script. When prompted:
#    - Enter the full file path to your audio file (e.g., `C:\Users\YourName\Documents\example.mp3`).
#    - Optionally, specify the desired response format (default is "text").
#
# **Output**:
# - The transcription will be printed to the console.
# - A copy will be saved in a folder named `transcripts` created in the chosen directory.
#
# **Troubleshooting**:
# - If you encounter a "file not found" error:
#    - Double-check the file path and ensure it's correct.
#    - Make sure the file exists and is accessible.
# - If an API error occurs:
#    - Verify your OpenAI API key is set and valid.
#    - Check the OpenAI Python library version (`pip show openai`) and ensure compatibility with the script.
# - If permission issues occur, ensure the script has access to the directory or file you're using.

import openai
from datetime import datetime
import os

# Ensure the API key is set in the environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("Error: The OPENAI_API_KEY environment variable is not set.")

# Prompt user to enter the audio file path
audio_file_path = input("Enter the full path to your audio file: ").strip()

# Remove extra quotes if present
audio_file_path = audio_file_path.strip('"').strip("'")

# Ensure the file path is provided and exists
if not audio_file_path:
    raise ValueError("Error: No file path was provided.")
if not os.path.exists(audio_file_path):
    raise FileNotFoundError(f"Error: The file at {audio_file_path} was not found.")

# Let user select response format
response_format = input("Enter response format (text, srt, vtt, json, verbose_json) [default: text]: ").strip()
if not response_format:
    response_format = "text"

# Initialize the OpenAI client
client = openai.OpenAI()

try:
    # Open the audio file
    with open(audio_file_path, "rb") as audio_file:
        # Create the transcription
        transcript = client.audio.translations.create(
            model="whisper-1",
            response_format=response_format,
            file=audio_file
        )

    # Print the transcript to the console
    print("\nTranscription:\n")
    print(transcript)

    # Ask user for output location preference
    print("\nWhere would you like to save the transcript?")
    print("1. Same directory as the audio file")
    print("2. Same directory as this script")
    print("3. Custom location")
    output_location_choice = input("Enter your choice (1-3) [default: 1]: ").strip()
    if not output_location_choice or output_location_choice not in ["1", "2", "3"]:
        output_location_choice = "1"  # Default to audio file location

    # Determine transcript directory based on user choice
    if output_location_choice == "1":
        # Same directory as audio file
        base_dir = os.path.dirname(os.path.abspath(audio_file_path))
    elif output_location_choice == "2":
        # Same directory as script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        # Custom location
        custom_dir = input("Enter the full path to save the transcript: ").strip()
        custom_dir = custom_dir.strip('"').strip("'")  # Remove quotes if present
        if not custom_dir:
            print("No directory provided, using audio file location instead.")
            base_dir = os.path.dirname(os.path.abspath(audio_file_path))
        else:
            base_dir = custom_dir

    # Create transcripts subdirectory in the chosen location
    transcripts_dir = os.path.join(base_dir, "transcripts")

    # Verify write permissions
    try:
        # Test if we can create the directory
        os.makedirs(transcripts_dir, exist_ok=True)
        
        # Test if we can write a file
        test_file = os.path.join(transcripts_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)  # Clean up test file
    except (PermissionError, OSError) as e:
        print(f"Cannot write to {transcripts_dir}: {e}")
        print("Falling back to current working directory...")
        transcripts_dir = os.path.join(os.getcwd(), "transcripts")
        os.makedirs(transcripts_dir, exist_ok=True)

    # Save the transcript to a file
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    transcript_file = os.path.join(transcripts_dir, f"transcript_{current_time}.{response_format}")

    with open(transcript_file, "w") as file:
        file.write(str(transcript))

    print(f"\nTranscript saved to {os.path.abspath(transcript_file)}")

except openai.error.OpenAIError as e:
    print(f"An error occurred with the OpenAI API: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
