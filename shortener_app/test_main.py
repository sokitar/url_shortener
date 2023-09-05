from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from .database import Base
from .main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

SHORTENED_URL = ""
TEST_URL = "https://www.google.com/"


@pytest.mark.order(1)
def test_create_url_ok():
    global SHORTENED_URL, TEST_URL
    response = client.post(
        "/shorten",
        json={"url": TEST_URL},
    )
    SHORTENED_URL = response.json()["shortened_url"]
    assert response.status_code == 201


@pytest.mark.order(2)
def test_create_url_repeated():
    global SHORTENED_URL

    response = client.post(
        "/shorten",
        json={"url": TEST_URL},
    )
    assert response.status_code == 303
    assert SHORTENED_URL == response.json()["shortened_url"]


@pytest.mark.order(3)
def test_forward_to_target_url():
    global SHORTENED_URL, TEST_URL
    response = client.get(SHORTENED_URL, allow_redirects=False)
    assert response.status_code == 307

    response = client.get(SHORTENED_URL)
    assert response.url == TEST_URL


@pytest.mark.order(4)
def test_get_url_info():
    global SHORTENED_URL, TEST_URL
    response = client.get(SHORTENED_URL + "/stats")
    assert response.status_code == 200
    content = response.json()
    assert content["url"] == TEST_URL
    assert content["hits"] == 2  # One hit for every call in the previous test function
