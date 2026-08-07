from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    pronunciation = Column(String)
    meaning = Column(Text)
    difficulty_level = Column(String)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    audio_url = Column(String)
    transcript = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    fluency_score = Column(Float)
    grammar_score = Column(Float)
    pronunciation_score = Column(Float)
    confidence_score = Column(Float)
    vocabulary_score = Column(Float)
    filler_word_count = Column(Integer)
    suggestions = Column(Text)