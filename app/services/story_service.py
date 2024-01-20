from app.db.base import Story
from app.models.requests import StoryCreate
from sqlalchemy.orm import Session


def get_story_by_title(db: Session, title: str):
    story = db.query(Story).filter(Story.title == title).first()
    return story


def create_story(db: Session, story: StoryCreate, user_id: int):
    db_story = Story(title=story.title, genre=story.genre, user_id=user_id)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story
