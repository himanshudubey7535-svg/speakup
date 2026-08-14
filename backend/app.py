import streamlit as st
import time
import os
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


def render_ring(percent, time_str, label):
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
    st.markdown(html, unsafe_allow_html=True)


def circular_timer(seconds_total, label):
    placeholder = st.empty()
    for i in range(seconds_total, -1, -1):
        elapsed = seconds_total - i
        percent = (elapsed / seconds_total) * 100
        mins, secs = divmod(i, 60)
        time_str = f"{mins:02d}:{secs:02d}"

        placeholder.empty()
        with placeholder.container():
            render_ring(percent, time_str, label)

        if i > 0:
            time.sleep(1)


@st.fragment(run_every=1)
def skippable_timer(seconds_total, label, next_stage, placeholder):
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = time.time()

    elapsed = int(time.time() - st.session_state.timer_start)
    remaining = max(seconds_total - elapsed, 0)
    percent = min((elapsed / seconds_total) * 100, 100)
    mins, secs = divmod(remaining, 60)
    time_str = f"{mins:02d}:{secs:02d}"

    placeholder.empty()
    with placeholder.container():
        render_ring(percent, time_str, label)
        if st.button("Skip →", key=f"skip_{label}"):
            del st.session_state.timer_start
            del st.session_state.prep_placeholder
            st.session_state.stage = next_stage
            st.rerun()

    if remaining <= 0:
        del st.session_state.timer_start
        del st.session_state.prep_placeholder
        st.session_state.stage = next_stage
        st.rerun()


if st.session_state.stage == "idle":
    if st.button("Start Preparation"):
        st.session_state.stage = "prep"
        if "prep_placeholder" in st.session_state:
            del st.session_state.prep_placeholder
        st.rerun()

elif st.session_state.stage == "prep":
    st.info("Preparation time! Click Skip anytime to move ahead.")
    if "prep_placeholder" not in st.session_state:
        st.session_state.prep_placeholder = st.empty()
    skippable_timer(600, "Prep Time", "thinking", st.session_state.prep_placeholder)

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

        os.makedirs("recordings", exist_ok=True)
        filename = f"recordings/{word['word']}_{int(time.time())}.wav"
        with open(filename, "wb") as f:
            f.write(audio["bytes"])
        st.session_state.audio_filepath = filename

    if st.button("Finish"):
        st.session_state.stage = "done"
        st.rerun()

elif st.session_state.stage == "done":
    st.write("Time's up! (AI analysis coming next)")
    if "recorded_audio" in st.session_state:
        st.audio(st.session_state.recorded_audio)
        st.caption(f"Saved to: {st.session_state.get('audio_filepath', 'N/A')}")
    if st.button("Try Another Word"):
        st.session_state.stage = "idle"
        st.rerun()