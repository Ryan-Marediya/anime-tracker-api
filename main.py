from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anime Tracker API")

@app.get("/")
def root():
    return {"message": "Anime Tracker API is running"}

# Get all anime
@app.get("/anime")
def get_all_anime(db: Session = Depends(get_db)):
    return db.query(models.Anime).all()

# Get single anime by id
@app.get("/anime/{anime_id}")
def get_anime(anime_id: int, db: Session = Depends(get_db)):
    anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime

# Add new anime
@app.post("/anime")
def add_anime(anime: schemas.AnimeCreate, db: Session = Depends(get_db)):
    db_anime = models.Anime(**anime.dict())
    db.add(db_anime)
    db.commit()
    db.refresh(db_anime)
    return db_anime

# Update anime
@app.put("/anime/{anime_id}")
def update_anime(anime_id: int, updated: schemas.AnimeCreate, db: Session = Depends(get_db)):
    anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    for key, value in updated.dict().items():
        setattr(anime, key, value)
    db.commit()
    db.refresh(anime)
    return anime

# Delete anime
@app.delete("/anime/{anime_id}")
def delete_anime(anime_id: int, db: Session = Depends(get_db)):
    anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    db.delete(anime)
    db.commit()
    return {"message": f"{anime.title} deleted successfully"}

from sqlalchemy import func

# Analytics - summary stats
@app.get("/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(models.Anime).count()
    watched = db.query(models.Anime).filter(models.Anime.status == "watched").count()
    watching = db.query(models.Anime).filter(models.Anime.status == "watching").count()
    want_to_watch = db.query(models.Anime).filter(models.Anime.status == "want_to_watch").count()
    avg_rating = db.query(func.avg(models.Anime.rating)).filter(models.Anime.rating != None).scalar()

    return {
        "total_anime": total,
        "watched": watched,
        "currently_watching": watching,
        "want_to_watch": want_to_watch,
        "average_rating": round(avg_rating, 2) if avg_rating else None
    }

# Analytics - top rated
@app.get("/analytics/top_rated")
def get_top_rated(db: Session = Depends(get_db)):
    top = db.query(models.Anime).filter(models.Anime.rating != None).order_by(models.Anime.rating.desc()).limit(5).all()
    return top

# Analytics - by genre
@app.get("/analytics/by_genre")
def get_by_genre(db: Session = Depends(get_db)):
    results = db.query(models.Anime.genre, func.count(models.Anime.id), func.avg(models.Anime.rating)).group_by(models.Anime.genre).all()
    return [
        {
            "genre": r[0],
            "count": r[1],
            "average_rating": round(r[2], 2) if r[2] else None
        }
        for r in results
    ]
@app.get("/anime/filter/{status}")
def get_by_status(status: str, db: Session = Depends(get_db)):
    valid_statuses = ["watched", "watching", "want_to_watch"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from: {valid_statuses}")
    results = db.query(models.Anime).filter(models.Anime.status == status).all()
    return results