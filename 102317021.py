import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# ---------- Helper function ----------
def error(msg):
    print("Error:", msg)
    print('Usage: python 102317022.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFile>')
    sys.exit(1)

# ---------- Argument Check ----------
# sys.argv = [script, singer, videos, duration, output]
if len(sys.argv) != 5:
    error("Incorrect number of arguments")

singer_name = sys.argv[1]

try:
    number_of_videos = int(sys.argv[2])
    audio_duration = int(sys.argv[3])
except ValueError:
    error("NumberOfVideos and AudioDuration must be integers")

output_file = sys.argv[4]

if number_of_videos <= 10:
    error("NumberOfVideos must be greater than 10")

if audio_duration <= 20:
    error("AudioDuration must be greater than 20 seconds")

# ---------- Create folders ----------
os.makedirs("downloads", exist_ok=True)

# ---------- Download videos ----------
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "quiet": True,
    "noplaylist": True
}

print("Downloading videos from YouTube...")

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([f"ytsearch{number_of_videos}:{singer_name} songs"])

# ---------- Convert + Trim audio ----------
print("Converting videos to audio and trimming...")

audio_clips = []

for file in os.listdir("downloads"):
    file_path = os.path.join("downloads", file)
    audio = AudioSegment.from_file(file_path)
    trimmed_audio = audio[:audio_duration * 1000]
    audio_clips.append(trimmed_audio)

# ---------- Merge audios ----------
final_audio = audio_clips[0]
for clip in audio_clips[1:]:
    final_audio += clip

# ---------- Export ----------
final_audio.export(output_file, format="mp3")

print("Mashup created successfully:", output_file)
