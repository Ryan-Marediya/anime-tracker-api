from pydantic import BaseModel
from typing import Optional

class AnimeCreate(BaseModel):
    title: str
    genre: Optional[str] = None
    status: str
    rating: Optional[float] = None
    episodes_watched: Optional[int] = 0
    total_episodes: Optional[int] = None
    notes: Optional[str] = None