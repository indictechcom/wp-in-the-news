from sqlalchemy import create_engine, Column, String, DateTime, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database Setup
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enables automatic reconnection
    pool_recycle=3600,   # Recycle connections after 1 hour
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# News Model
class News(Base):
    __tablename__ = "news"
    id = Column(String(32), primary_key=True, index=True)  # Unique ID for the news item
    text = Column(String(2000), nullable=False)  # The main text of the news item
    links = Column(String(5000), nullable=True)  # JSON string to store multiple links
    featured_date = Column(Date, nullable=False)  # The featured date of the news item

    def __repr__(self):
        return f"<News(id={self.id}, featured_date={self.featured_date}, text={self.text[:50]}...)>"