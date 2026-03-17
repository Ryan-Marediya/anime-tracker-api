# Anime Tracker API

A REST API built with Python and FastAPI to track anime you've watched, are currently watching, or want to watch — with built-in analytics.

## Tech Stack
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite

## Features
- Full CRUD — add, update, delete, and retrieve anime
- Track status: watched, watching, or want to watch
- Rate anime on a 1-10 scale
- Filter anime by status
- Analytics endpoints — average rating, top rated, genre breakdown
- Jikan/MyAnimeList API integration — search and auto-populate anime data

## Getting Started

1. Clone the repo
   git clone https://github.com/Ryan-Marediya/anime-tracker-api.git

2. Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install fastapi uvicorn sqlalchemy requests

4. Run the server
   uvicorn main:app --reload

5. Open docs
   http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /anime | Get all anime |
| GET | /anime/{id} | Get anime by ID |
| POST | /anime | Add new anime |
| PUT | /anime/{id} | Update anime |
| DELETE | /anime/{id} | Delete anime |
| GET | /anime/filter/{status} | Filter by status |
| GET | /analytics/summary | Overall stats |
| GET | /analytics/top_rated | Top 5 rated anime |
| GET | /analytics/by_genre | Stats grouped by genre |
| GET | /search/{title} | Search anime via Jikan API |
| POST | /anime/add_from_search/{mal_id} | Auto-add anime from search |