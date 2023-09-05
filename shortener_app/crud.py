from sqlalchemy.orm import Session

from . import keygen, models, schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    shortened_url = keygen.create_unique_random_key(db)
    db_url = models.URL(target_url=url.url, shortened_url=shortened_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_shortened(db: Session, shortened_url: str) -> models.URL:
    return (
        db.query(models.URL).filter(models.URL.shortened_url == shortened_url).first()
    )


def get_db_url_by_target(db: Session, target_url: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.target_url == target_url).first()


def update_db_clicks(db: Session, db_url: schemas.URLStats) -> models.URL:
    db_url.hits += 1
    db.commit()
    db.refresh(db_url)
    return db_url
