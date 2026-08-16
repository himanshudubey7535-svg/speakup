import streamlit as st
import time
import os
import random
import random as rnd
from words_data import WORDS
from streamlit_mic_recorder import mic_recorder
from auth import signup, login, get_profile, update_profile

st.set_page_config(page_title="SpeakUp", page_icon="🎤")

# ---------------- AUTH GATE (front page) ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center; margin-top:40px; margin-bottom:20px;">
      <div style="font-size:48px;">🎤</div>
      <div style="font-size:32px; font-weight:bold; color:#6C63FF; font-family:sans-serif;">SpeakUp</div>
      <div style="color:#888; font-family:sans-serif;">1 Minute Vocabulary Challenge</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            success, msg = login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error(msg)

    with tab2:
        new_username = st.text_input("Choose a username", key="signup_user")
        new_password = st.text_input("Choose a password", type="password", key="signup_pass")

        st.markdown("**Profile Details**")
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"], key="signup_gender")
        dob = st.date_input("Date of Birth", key="signup_dob")
        locality = st.text_input("Locality / City", key="signup_locality")
        email = st.text_input("Email Address", key="signup_email")
        phone = st.text_input("Phone Number", key="signup_phone")

        if st.button("Sign Up", key="signup_btn"):
            profile = {
                "gender": gender,
                "dob": str(dob),
                "locality": locality,
                "email": email,
                "phone": phone
            }
            success, msg = signup(new_username, new_password, profile)
            if success:
                st.success(msg + " — you can log in now")
            else:
                st.error(msg)

    st.stop()

# ---------------- MAIN APP (only reachable after login) ----------------

col_title, col_logout = st.columns([4, 1])
with col_title:
    st.title("SpeakUp – 1 Minute Vocabulary Challenge")
with col_logout:
    if st.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()

with st.expander("👤 My Profile"):
    profile = get_profile(st.session_state.username)
    st.write(f"**Username:** {st.session_state.username}")

    edit_gender = st.selectbox(
        "Gender",
        ["Prefer not to say", "Male", "Female", "Other"],
        index=["Prefer not to say", "Male", "Female", "Other"].index(profile.get("gender", "Prefer not to say")),
        key="edit_gender"
    )
    edit_locality = st.text_input("Locality / City", value=profile.get("locality", ""), key="edit_locality")
    edit_email = st.text_input("Email Address", value=profile.get("email", ""), key="edit_email")
    edit_phone = st.text_input("Phone Number", value=profile.get("phone", ""), key="edit_phone")
    st.caption(f"Date of Birth: {profile.get('dob', 'Not set')}")

    if st.button("Save Profile", key="save_profile_btn"):
        updated_profile = {
            "gender": edit_gender,
            "dob": profile.get("dob", ""),
            "locality": edit_locality,
            "email": edit_email,
            "phone": edit_phone
        }
        update_profile(st.session_state.username, updated_profile)
        st.success("Profile updated!")

if "stage" not in st.session_state:
    st.session_state.stage = "idle"
    st.session_state.current_word = random.choice(WORDS)
    st.session_state.streak = 0

if st.session_state.stage == "idle":
    st.session_state.current_word = random.choice(WORDS)

word = st.session_state.current_word

st.markdown(f"""
<div style="text-align: right; font-family: sans-serif; color: #6C63FF; font-weight: 600; margin-bottom: 10px;">
  Welcome, {st.session_state.username} · 🔥 Streak: {st.session_state.streak}
</div>
""", unsafe_allow_html=True)

if st.session_state.stage != "done":
    st.markdown(f"""
    <style>
    @keyframes flipIn {{
      0% {{ transform: rotateY(90deg); opacity: 0; }}
      100% {{ transform: rotateY(0deg); opacity: 1; }}
    }}
    .word-card {{
      animation: flipIn 0.6s ease-out;
      background: linear-gradient(135deg, #6C63FF 0%, #9B8CFF 100%);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      color: white;
      font-family: sans-serif;
      box-shadow: 0 8px 24px rgba(108, 99, 255, 0.3);
      margin-bottom: 20px;
    }}
    </style>
    <div class="word-card">
      <div style="font-size: 32px; font-weight: bold;">{word['word']}</div>
      <div style="font-size: 16px; opacity: 0.9; margin-top: 4px;">{word['pronunciation']}</div>
      <div style="font-size: 15px; margin-top: 10px;">{word['meaning']}</div>
      <div style="display: inline-block; margin-top: 10px; padding: 4px 14px; background: rgba(255,255,255,0.25); border-radius: 20px; font-size: 13px;">{word['difficulty']}</div>
    </div>
    """, unsafe_allow_html=True)


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


def score_to_grade(overall):
    if overall >= 90:
        return "A+", "#22C55E"
    elif overall >= 80:
        return "A", "#4ADE80"
    elif overall >= 70:
        return "B", "#FACC15"
    elif overall >= 60:
        return "C", "#FB923C"
    else:
        return "D", "#F87171"


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
        st.markdown("""
        <style>
        @keyframes pulseBar {
          0%, 100% { height: 12px; }
          50% { height: 40px; }
        }
        .wave-bar {
          display: inline-block;
          width: 6px;
          margin: 0 3px;
          background: #6C63FF;
          border-radius: 3px;
          animation: pulseBar 0.8s ease-in-out infinite;
        }
        </style>
        <div style="display:flex; justify-content:center; align-items:center; height:50px; margin: 10px 0;">
          <div class="wave-bar" style="animation-delay: 0s;"></div>
          <div class="wave-bar" style="animation-delay: 0.1s;"></div>
          <div class="wave-bar" style="animation-delay: 0.2s;"></div>
          <div class="wave-bar" style="animation-delay: 0.3s;"></div>
          <div class="wave-bar" style="animation-delay: 0.4s;"></div>
          <div class="wave-bar" style="animation-delay: 0.3s;"></div>
          <div class="wave-bar" style="animation-delay: 0.2s;"></div>
          <div class="wave-bar" style="animation-delay: 0.1s;"></div>
        </div>
        """, unsafe_allow_html=True)

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
        st.session_state.streak += 1
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
    grade, grade_color = score_to_grade(overall)

    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
      <div style="
        display: inline-block;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: {grade_color};
        color: white;
        font-size: 42px;
        font-weight: bold;
        line-height: 100px;
        box-shadow: 0 6px 20px {grade_color}66;
        margin-bottom: 10px;
      ">{grade}</div>
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
    st.success(f"🔥 Current streak: {st.session_state.streak}")

    st.divider()
    if st.button("Try Another Word"):
        st.session_state.stage = "idle"
        st.rerun()