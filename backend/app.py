
import streamlit as st
import time
import os
import random
import random as rnd
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

if st.session_state.stage != "done":
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


def generate_mock_scores():
    return {
        "fluency": rnd.randint(60, 95),
        "grammar": rnd.randint(60, 95),
        "vocabulary": rnd.randint(60, 95),
        "pronunciation": rnd.randint(60, 95),
        "confidence": rnd.randint(60, 95),
        "filler_words": rnd.randint(0, 8),
    }


def render_score_bar(label, value, max_value=100):
    percent = (value / max_value) * 100
    html = f"""
    <div style="margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; font-family: sans-serif; margin-bottom: 4px;">
        <span style="font-weight: 600;">{label}</span>
        <span style="color: #6C63FF; font-weight: 600;">{value}/100</span>
      </div>
      <div style="background: #E8E6FF; border-radius: 8px; height: 12px; width: 100%;">
        <div style="background: #6C63FF; border-radius: 8px; height: 12px; width: {percent}%;"></div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


if st.session_state.stage == "idle":
    if st.button("Start Preparation"):
        st.session_state.stage = "prep"
        for key in ["prep_placeholder", "recorded_audio", "scores", "speak_timer_start"]:
            if key in st.session_state:
                del st.session_state[key]
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

    if "recorded_audio" not in st.session_state:
        audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop Recording", key="speak_recorder")
        if audio:
            st.session_state.recorded_audio = audio["bytes"]
            os.makedirs("recordings", exist_ok=True)
            filename = f"recordings/{word['word']}_{int(time.time())}.wav"
            with open(filename, "wb") as f:
                f.write(audio["bytes"])
            st.session_state.audio_filepath = filename
            st.rerun()
    else:
        st.audio(st.session_state.recorded_audio)
        st.success("Recording captured!")

    if "speak_timer_start" not in st.session_state:
        st.session_state.speak_timer_start = time.time()

    elapsed = int(time.time() - st.session_state.speak_timer_start)
    remaining = max(60 - elapsed, 0)
    percent = min((elapsed / 60) * 100, 100)
    mins, secs = divmod(remaining, 60)
    render_ring(percent, f"{mins:02d}:{secs:02d}", "Speak Time")

    col1, col2 = st.columns(2)
    with col1:
        finish_early = st.button("✅ Finish Early", key="finish_early_btn")
    with col2:
        finish_normal = st.button("Finish", key="finish_btn")

    if finish_early or finish_normal or remaining <= 0:
        if "speak_timer_start" in st.session_state:
            del st.session_state.speak_timer_start
        st.session_state.stage = "done"
        st.rerun()

elif st.session_state.stage == "done":
    st.balloons()
    st.subheader("Your Results")

    if "recorded_audio" in st.session_state:
        st.audio(st.session_state.recorded_audio)

    if "scores" not in st.session_state:
        st.session_state.scores = generate_mock_scores()

    scores = st.session_state.scores
    overall = round(sum([scores["fluency"], scores["grammar"], scores["vocabulary"],
                          scores["pronunciation"], scores["confidence"]]) / 5)

    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
      <div style="font-size: 48px; font-weight: bold; color: #6C63FF;">{overall}</div>
      <div style="color: #888;">Overall Score</div>
    </div>
    """, unsafe_allow_html=True)

    render_score_bar("Fluency", scores["fluency"])
    render_score_bar("Grammar", scores["grammar"])
    render_score_bar("Vocabulary", scores["vocabulary"])
    render_score_bar("Pronunciation", scores["pronunciation"])
    render_score_bar("Confidence", scores["confidence"])

    st.info(f"🗣️ Filler words detected: {scores['filler_words']}")

    st.divider()
    if st.button("Try Another Word"):
        st.session_state.stage = "idle"
        st.rerun()