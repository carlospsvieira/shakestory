from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.enums.story_genre import StoryGenre
from .session import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(LargeBinary)

    class Config:
        orm_mode = True


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    genre = Column(SQLAlchemyEnum(StoryGenre))
    content = Column(String, nullable=True)
    current_segment_id = Column(Integer, ForeignKey("segments.id"))
    creation_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    segments = relationship(
        "Segment", back_populates="story", foreign_keys="Segment.story_id"
    )

    class Config:
        orm_mode = True


class Segment(Base):
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    story_id = Column(Integer, ForeignKey("stories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    contribution_date = Column(DateTime, default=datetime.utcnow)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)

    story = relationship(
        "Story", back_populates="segments", foreign_keys="Segment.story_id"
    )
    user = relationship("User")

    class Config:
        orm_mode = True
