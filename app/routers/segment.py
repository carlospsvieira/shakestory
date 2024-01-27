from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.base import User
from app.db.session import get_db
from app.dependencies.authentication import get_current_user
from app.services import segment_service
from app.models.requests import SegmentCreate, SegmentResponse
from app.utils.helpers import validate_content

router = APIRouter()


@router.post("/stories/{story_id}/segment/new", response_model=SegmentResponse)
async def new_segment(
    segment: SegmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    story_id: int = Path(..., title="The ID of the story to attach segment", ge=1),
):
    if not validate_content(segment.content):
        raise HTTPException(status_code=400, detail="Invalid segment content")

    created_segment = segment_service.create_segment(
        db, segment, story_id, current_user.id
    )

    segment_response = SegmentResponse(
        id=created_segment.id,
        content=created_segment.content,
        user_id=current_user.id,
        story_id=story_id,
        contribution_date=created_segment.contribution_date.strftime("%Y-%m-%d %H:%M:%S"),
        upvotes=created_segment.upvotes,
        downvotes=created_segment.downvotes,
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Segment created successfully",
            "story": segment_response,
        },
    )
