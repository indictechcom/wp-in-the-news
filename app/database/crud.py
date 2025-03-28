from datetime import datetime, date
from sqlalchemy.orm import Session
from app.database.models import News
from typing import Optional, List
import json

def add_news_to_db(db: Session, news_data: dict) -> News:
    """
    Add a news item to the database.
    """
    featured_date = datetime.strptime(news_data['featured_date'], "%Y-%m-%d").date()
    news = News(
        id=news_data['id'],
        text=news_data['text'],
        links=json.dumps(news_data['links']),  # Serialize links to JSON
        featured_date=featured_date
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    
    return news

def get_news_by_date(db: Session, target_date: str) -> List[News]:
    """
    Retrieve all news items by their featured date.
    """
    if isinstance(target_date, (datetime, date)):
        target_date = target_date.isoformat()
    
    target_date_obj = datetime.fromisoformat(target_date).date()
    news_list = db.query(News).filter(News.featured_date == target_date_obj).all()

    # Deserialize the links field from JSON string to Python list for each news item
    for news in news_list:
        if isinstance(news.links, str):
            news.links = json.loads(news.links)
    # print("News list:")
    # print(news_list)
    return news_list



def get_news_by_id(db: Session, news_id: str) -> Optional[News]:
    """
    Retrieve a news item by its unique ID.
    """
    return db.query(News).filter(News.id == news_id).first()