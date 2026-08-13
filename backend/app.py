import streamlit as st
import time
import random
from words_data import WORDS
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="SpeakUp", page_icon="🎤")
st.title("SpeakUp – 1 Minute Vocabulary Challenge")

if "stage" not in st.session_state:
    st.session_state.stage = "idle"
    st.session_state.current_word = random.choice(WORDS)

if st.session_state.stage == "idle":
    st.session_state.current_word = random.choice(WORDS)

word = st.session_state.current_word

st.header(word["word"])
st.write(f"*Pronunciation:* {word['pronunciation']}")
st.write(f"*Meaning:* {word['meaning']}")
st.badge(word["difficulty"])


def circular_timer(seconds_total, label):
    placeholder = st.empty()
    for i in range(seconds_total, -1, -1):
        elapsed = seconds_total - i
        percent = (elapsed / seconds_total) * 100
        mins, secs = divmod(i, 60)
        time_str = f"{mins:02d}:{secs:02d}"

        html = f"""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
          <div style="
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: conic-gradient(#6C63FF {percent}%, #E8E6FF {percent}% 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 20px rgba(108, 99, 255, 0.25);
          ">
            <div style="
              width: 180px;
              height: 180px;
              border-radius: 50%;
              background: white;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              font-family: sans-serif;
            ">
              <div style="font-size: 36px; font-weight: bold; color: #6C63FF;">{time_str}</div>
              <div style="font-size: 14px; color: #888;">{label}</div>
            </div>
          </div>
        </div>
        """
        placeholder.markdown(html, unsafe_allow_html=True)
        if i > 0:
            time.sleep(1)


if st.session_state.stage == "idle":
    if st.button("Start Preparation"):
        st.session_state.stage = "prep"
        st.rerun()

elif st.session_state.stage == "prep":
    st.info("Preparation time!")
    circular_timer(600, "Prep Time")
    st.session_state.stage = "thinking"
    st.rerun()

elif st.session_state.stage == "thinking":
    st.info("Think time!")
    circular_timer(15, "Think Time")
    st.session_state.stage = "speaking"
    st.rerun()

elif st.session_state.stage == "speaking":
    st.success("Speak now! 60 seconds")

    audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop Recording", key="speak_recorder")

    circular_timer(60, "Speak Time")

    if audio:
        st.session_state.recorded_audio = audio["bytes"]
        st.audio(audio["bytes"])

    if st.button("Finish"):
        st.session_state.stage = "done"
        st.rerun()

elif st.session_state.stage == "done":
    st.write("Time's up! (AI analysis coming next)")
    if "recorded_audio" in st.session_state:
        st.audio(st.session_state.recorded_audio)
    if st.button("Try Another Word"):
        st.session_state.stage = "idle"
        st.rerun()