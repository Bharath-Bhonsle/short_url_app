import hashlib
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from models import models, schemas
from database import database
from utils import utils
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(data: schemas.URLCreate, db: Session = Depends(database.get_db)):
    short_url = utils.generate_short_url(str(data.original_url))
    expiration_time = utils.get_expiration_time(data.expires_in)

    db_url = models.URL(
        original_url=str(data.original_url),
        short_url=short_url,
        created_at=utils.get_expiration_time(0),
        expires_at=expiration_time,
    )

    if data.password:
        db_url.password_hash = hashlib.sha256(data.password.encode()).hexdigest()

    try:
        db.add(db_url)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="URL already shortened")

    return {
        "original_url": data.original_url,
        "short_url": f"https://short.ly/{short_url}",
        "expires_at": expiration_time,
    }


@app.get("/{short_url}")
def redirect_to_url(short_url: str, request: Request, db: Session = Depends(database.get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if db_url.expires_at and db_url.expires_at.tzinfo is None:
        db_url.expires_at = db_url.expires_at.replace(tzinfo=timezone.utc)

    if db_url.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="URL has expired")

    db_log = models.AccessLog(
        short_url_id=db_url.id,
        ip_address=request.client.host,
    )
    db.add(db_log)
    db.commit()

    return RedirectResponse(url=db_url.original_url)


@app.get("/analytics/{short_url}", response_model=schemas.AnalyticsResponse)
def get_analytics(short_url: str, db: Session = Depends(database.get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    logs = db.query(models.AccessLog).filter(models.AccessLog.short_url_id == db_url.id).all()

    return {
        "short_url": short_url,
        "access_count": len(logs),
        "logs": [{"accessed_at": log.accessed_at, "ip_address": log.ip_address} for log in logs],
    }
