from pydantic import BaseModel
from typing import Literal


ProjectType = Literal["redirect", "direct", "protection"]


class ProjectCreate(BaseModel):
    name: str
    type: ProjectType


class ProjectResponse(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True


class RouteCreate(BaseModel):
    project_id: int
    name: str
    slug: str


class RouteResponse(BaseModel):
    id: int
    project_id: int
    name: str
    slug: str

    class Config:
        from_attributes = True