import streamlit as st
import whisper
from yt_dlp import YoutubeDL
import os

# Load Whisper model once
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")  # Use "base" or "small" if needed

# Download YouTube audio
def download_audio(url, filename="downloaded_audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename.replace(".mp3", ""),  # prevent double .mp3.mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

# Transcribe the audio using Whisper
def transcribe_audio(audio_path):
    model = load_model()
    result = model.transcribe(audio_path)
    return result["text"]

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Transcriber", layout="centered")

st.title("🎙️ YouTube Transcript Generator")
st.markdown("Paste a YouTube video URL below. This app will download the audio and transcribe it using Whisper.")

video_url = st.text_input("🔗 Enter YouTube URL")

if st.button("Generate Transcript"):
    if not video_url.strip():
        st.warning("Please enter a valid YouTube link.")
    else:
        with st.spinner("🔄 Downloading and transcribing..."):
            try:
                audio_file = download_audio(video_url)
                transcript = transcribe_audio(audio_file)

                st.success("✅ Transcript Ready!")
                st.text_area("📜 Transcript", transcript, height=300)

                # Save and offer download
                with open("transcript.txt", "w", encoding="utf-8") as f:
                    f.write(transcript)
                with open("transcript.txt", "rb") as f:
                    st.download_button("⬇️ Download Transcript", f, file_name="transcript.txt")

                # Optional cleanup
                if os.path.exists(audio_file):
                    os.remove(audio_file)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
