from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False, index=True)

    routes = relationship("Route", back_populates="project")
    destinations = relationship("Destination", back_populates="project")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    project = relationship("Project", back_populates="routes")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    weight = Column(Integer, default=100)
    status = Column(String, default="active")

    project = relationship("Project", back_populates="destinations")