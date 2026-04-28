from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas

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