from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MovieDBModel(Base):
    __tablename__ = 'movies'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String)
    location = Column(String, nullable=False)
    published = Column(Boolean, nullable=False)
    rating = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
