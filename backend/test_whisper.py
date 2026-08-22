import whisper

model = whisper.load_model("base")
result = model.transcribe("recordings/Fickle_1786814822.wav")
print(result["text"])