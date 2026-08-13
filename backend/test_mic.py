import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title("Mic Test")

audio = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", key="recorder")

if audio:
    st.audio(audio["bytes"])