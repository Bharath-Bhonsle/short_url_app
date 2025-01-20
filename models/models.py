from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy import event

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    password_hash = Column(String, nullable=True)  # Optional for password protection


# Event listener to ensure `expires_at` is timezone-aware before inserting or updating
@event.listens_for(URL, 'before_insert')
@event.listens_for(URL, 'before_update')
def ensure_timezone_awareness(mapper, connection, target):
    if target.expires_at.tzinfo is None:
        target.expires_at = target.expires_at.replace(tzinfo=timezone.utc)


class AccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(Integer, primary_key=True, index=True)
    short_url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    accessed_at = Column(DateTime, default=datetime.now(timezone.utc))
    ip_address = Column(String, nullable=False)
