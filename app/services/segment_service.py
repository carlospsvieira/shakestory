from sqlalchemy.orm import Session

from app.db.base import Segment
from app.models.requests import SegmentCreate


def get_segment_by_id(db: Session, segment_id: int):
    segment = db.query(Segment).filter(Segment.id == segment_id).first()
    return segment


def create_segment(db: Session, segment: SegmentCreate, story_id: int, user_id: int):
    db_segment = Segment(content=segment.content, story_id=story_id, user_id=user_id)
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment


def update_segment_content(db: Session, segment_id: int, content: str):
    segment = db.query(Segment).filter(Segment.id == segment_id).first()
    if segment:
        segment.content = content
        db.commit()
        db.refresh(segment)
        return segment
    return None
