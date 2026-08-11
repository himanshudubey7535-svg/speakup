import streamlit as st

st.set_page_config(page_title="SpeakUp", page_icon="🎤")

st.title("SpeakUp – 1 Minute Vocabulary Challenge")

# Sample word (later this will come from your word dataset / DB)
word = {
    "word": "Ephemeral",
    "pronunciation": "ih-FEM-er-ul",
    "meaning": "Lasting for a very short time",
    "difficulty": "Hard"
}

st.header(word["word"])
st.write(f"*Pronunciation:* {word['pronunciation']}")
st.write(f"*Meaning:* {word['meaning']}")
st.badge(word["difficulty"])

if st.button("New Word"):
    st.write("New word logic coming soon!")