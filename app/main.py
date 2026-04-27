from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas

app = FastAPI()

# создаём таблицы
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "ok"}


#  создать ссылку
@app.post("/links", response_model=schemas.LinkResponse)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    db_link = models.Link(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


#  получить все ссылки
@app.get("/links", response_model=list[schemas.LinkResponse])
def get_links(db: Session = Depends(get_db)):
    return db.query(models.Link).all()