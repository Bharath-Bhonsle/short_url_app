from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl
    expires_in: Optional[int] = 24  # Default to 24 hours
    password: Optional[str] = None


class URLResponse(BaseModel):
    original_url: HttpUrl
    short_url: str
    expires_at: datetime


class AnalyticsResponse(BaseModel):
    short_url: str
    access_count: int
    logs: List[dict]  # List of access logs
