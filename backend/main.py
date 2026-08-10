from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
app=FastAPI()
@app.get("/health")
def health_check():
    return{"status":"ok"}
