# transcribe_v02.py
# Before use: 1) add OpenAI API key to environment; 2) downsample audio to below 25 MB; 3) update PATH\FILEPATH\FILENAME; 4) select response_format

import openai
from datetime import datetime
import os

# Initialize the OpenAI client
client = openai.OpenAI()

# Read the audio file
audio_file = open(r"FILEPATH\FILENAME", "rb")

# Create the transcription
transcript = client.audio.translations.create(
    model="whisper-1",
    response_format="vtt",
    file=audio_file
)

# Close the audio file
audio_file.close()

# Print the transcript
print(transcript)

# Get current date and time for filename
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create 'transcripts' directory if it doesn't exist
transcripts_dir = "./transcripts"
os.makedirs(transcripts_dir, exist_ok=True)

# Filepath for the transcript file
transcript_file = os.path.join(transcripts_dir, f"transcript_{current_time}.txt")

# Write the transcript to a file
with open(transcript_file, "w") as file:
    file.write(str(transcript))

print(f"Transcript saved to {transcript_file}")
