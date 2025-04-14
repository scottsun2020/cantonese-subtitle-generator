import streamlit as st
import whisper
import os
import tempfile
from datetime import timedelta

# Helper: Format time for SRT
def format_srt_time(seconds):
    td = timedelta(seconds=seconds)
    return str(td)[:10].replace('.', ',').zfill(12)

# Upload section
st.title("🎧 Cantonese Audio → Subtitle Generator")
uploaded_file = st.file_uploader("Upload Cantonese Audio File", type=["mp3", "m4a", "wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.write("🔁 Transcribing with Whisper...")
    model = whisper.load_model("medium")
    result = model.transcribe(tmp_path, language="zh")

    # Show editable text
    segments = result['segments']
    srt_blocks = []
    for i, seg in enumerate(segments):
        start = format_srt_time(seg['start'])
        end = format_srt_time(seg['end'])
        text = seg['text']
        srt_blocks.append(f"{i+1}\n{start} --> {end}\n{text.strip()}\n")

    editable_srt = st.text_area("📝 Edit Subtitles (SRT format)", value="".join(srt_blocks), height=400)

    # Download final SRT
    st.download_button("📥 Download SRT File", data=editable_srt, file_name="subtitles.srt", mime="text/plain")
