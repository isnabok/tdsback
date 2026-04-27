from pydantic import BaseModel


class LinkCreate(BaseModel):
    slug: str
    target_url: str
    geo: str | None = None
    device: str | None = None


class LinkResponse(BaseModel):
    id: int
    slug: str
    target_url: str
    geo: str | None
    device: str | None

    class Config:
        from_attributes = True