from fastapi import HTTPException
from app.db.base import Story
from app.models.requests import StoryCreate
from sqlalchemy.orm import Session


def get_story_by_title(db: Session, title: str):
    story = db.query(Story).filter(Story.title == title).first()
    return story


def create_story(db: Session, story: StoryCreate, user_id: int):
    db_story = Story(
        title=story.title, genre=story.genre, content=story.content, user_id=user_id
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


def update_title(db: Session, story_id: int, title: str):
    story = db.query(Story).filter(Story.id == story_id).first()
    if story:
        story.title = title
        db.commit()
        db.refresh(story)
        return story
    return None


def update_story_content(db: Session, story_id: int, content: str):
    story = db.query(Story).filter(Story.id == story_id).first()
    if story:
        story.content = content
        db.commit()
        db.refresh(story)
        return story
    return None


def delete_story(db: Session, story_id: int):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    db.delete(story)
    db.commit()
