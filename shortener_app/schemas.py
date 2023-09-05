from pydantic import BaseModel


class URLBase(BaseModel):
    url: str


class URLShortened(BaseModel):
    shortened_url: str


class URLStats(URLBase):
    hits: int
    created_on: str

    class Config:
        orm_mode = True
