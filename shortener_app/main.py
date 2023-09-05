import validators
from fastapi import Depends, FastAPI, HTTPException, Request, status, Response
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .config import get_settings

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to my URL shortener API"


def format_shortened_url(shortened_url):
    return "/" + get_settings().urls_endpoint + "/" + shortened_url


@app.post(
    "/shorten",
    response_model=schemas.URLShortened,
    status_code=status.HTTP_201_CREATED,
    response_description="Created",
)
def create_url(url: schemas.URLBase, response: Response, db: Session = Depends(get_db)):
    if not validators.url(url.url):
        raise_bad_request(message="Your provided URL is not valid")

    if db_url := crud.get_db_url_by_target(db, target_url=url.url):
        response.status_code = status.HTTP_303_SEE_OTHER
        return schemas.URLShortened(
            shortened_url=format_shortened_url(db_url.shortened_url)
        )

    db_url = crud.create_db_url(db=db, url=url)

    return schemas.URLShortened(
        shortened_url=format_shortened_url(db_url.shortened_url)
    )


@app.get(
    "/" + get_settings().urls_endpoint + "/{shortened_url}/stats",
    name="Shortened URL info",
    response_model=schemas.URLStats,
    status_code=200,
)
def get_url_info(shortened_url: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_shortened(db, shortened_url=shortened_url):
        return schemas.URLStats(
            hits=db_url.hits,
            url=db_url.target_url,
            created_on=db_url.created_on.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
    else:
        raise_not_found(request)


@app.get("/" + get_settings().urls_endpoint + "/{shortened_url}")
def forward_to_target_url(
    shortened_url: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_shortened(db=db, shortened_url=shortened_url):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
