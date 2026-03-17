from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    status = Column(String, nullable=False)  # "watched", "watching", "want_to_watch"
    rating = Column(Float, nullable=True)    # 1.0 - 10.0, only if watched
    episodes_watched = Column(Integer, default=0)
    total_episodes = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)    # personal notes on the anime
    date_added = Column(DateTime, default=func.now())