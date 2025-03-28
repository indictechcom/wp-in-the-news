from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# News Schema for Response
class NewsSchema(BaseModel):
    id: str
    text: str
    links: Optional[List[dict]]  # List of links (each link is a dictionary with "url" and "text")
    featured_date: date
    
    class Config:
        orm_mode = True
        from_attributes = True
