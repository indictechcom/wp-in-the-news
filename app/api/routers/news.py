from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import SessionLocal
from app.schemas.schemas import NewsSchema
from app.database.crud import add_news_to_db, get_news_by_date ,get_news_by_id
from app.core.utils import fetch_news_of_the_day
from datetime import datetime
import json
# Router instance
router = APIRouter(
    prefix="/api",
    tags=["News"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/news_of_the_day", response_model=List[NewsSchema])
async def get_news_of_the_day_route(db: Session = Depends(get_db)):
    """
    Fetch and store all news of the day.
    """
    news_data = fetch_news_of_the_day()
    # print(news_data)
    # Ensure news_data is a list
    if not isinstance(news_data, list) or len(news_data) == 0:
        raise HTTPException(status_code=404, detail="No news data found.")

    stored_news = []
    for news_item in news_data:
        # Ensure each news_item is a dictionary
        if not isinstance(news_item, dict):
            raise HTTPException(status_code=500, detail="Invalid news data format.")

        # News already exisits in the database
        if get_news_by_id(db, news_item['id']):
            stored_news.append(news_item)
            continue
   
        # Deserialize the links field from JSON string to Python list if necessary
        if isinstance(news_item["links"], str):
            news_item["links"] = json.loads(news_item["links"])

        stored_news.append(news_item)
        add_news_to_db(db, news_item)
    # print("Stored news items:")
    # print(stored_news)
    return stored_news


@router.get("/news/{date}", response_model=List[NewsSchema])
async def get_news_by_date_route(date: str, db: Session = Depends(get_db)):
    """
    Retrieve all news items by their featured date.
    """
    try:
        # Parse the date string into a datetime object
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    # Fetch the news items by date
    news_list = get_news_by_date(db, target_date)

    # Convert ORM objects to Pydantic models
    response = [NewsSchema.from_orm(news) for news in news_list]
    # print(response)  # Debug the response
    return response