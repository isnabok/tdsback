from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas

import random
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@app.post("/routes", response_model=schemas.RouteResponse)
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = models.Route(**route.model_dump())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


@app.get("/routes", response_model=list[schemas.RouteResponse])
def get_routes(db: Session = Depends(get_db)):
    return db.query(models.Route).all()


@app.get("/routes/{slug}", response_model=schemas.RouteResponse)
def get_route_by_slug(slug: str, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.slug == slug).first()

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    return route


@app.get("/projects/{project_id}/routes", response_model=list[schemas.RouteResponse])
def get_project_routes(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Route).filter(models.Route.project_id == project_id).all()


@app.post("/projects/{project_id}/routes", response_model=schemas.RouteResponse)
def create_project_route(
    project_id: int,
    route: schemas.RouteCreate,
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_route = models.Route(
        project_id=project_id,
        name=route.name,
        slug=route.slug,
    )

    db.add(db_route)
    db.commit()
    db.refresh(db_route)

    return db_route


@app.get("/r/{slug}")
def traffic_entry(slug: str, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.slug == slug).first()

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    project = db.query(models.Project).filter(models.Project.id == route.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    destinations = db.query(models.Destination).filter(
        models.Destination.project_id == project.id,
        models.Destination.status == "active",
        models.Destination.weight > 0,
    ).all()

    if not destinations:
        raise HTTPException(status_code=404, detail="No active destinations")

    destination = random.choices(
        destinations,
        weights=[d.weight for d in destinations],
        k=1,
    )[0]

    return RedirectResponse(url=destination.url, status_code=302)


@app.get("/projects/{project_id}/destinations", response_model=list[schemas.DestinationResponse])
def get_project_destinations(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Destination).filter(
        models.Destination.project_id == project_id
    ).all()


@app.post("/projects/{project_id}/destinations", response_model=schemas.DestinationResponse)
def create_project_destination(
    project_id: int,
    destination: schemas.DestinationCreate,
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_destination = models.Destination(
        project_id=project_id,
        name=destination.name,
        url=str(destination.url),
        weight=destination.weight,
        status=destination.status,
    )

    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)

    return db_destination