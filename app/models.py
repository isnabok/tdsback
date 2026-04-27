from sqlalchemy import Column, Integer, String
from app.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    target_url = Column(String)
    geo = Column(String, nullable=True)  # например: DE, PL
    device = Column(String, nullable=True)  # mobile / desktop