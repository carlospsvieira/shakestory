from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import story_service
from app.models.requests import StoryCreate, StoryResponse

router = APIRouter()


@router.post("/story/new", response_model=StoryCreate)
async def new_story(story: StoryCreate, db: Session = Depends(get_db)):
    existing_story = story_service.get_story_by_title(db, story.title)
    if existing_story:
        raise HTTPException(status_code=400, detail="Title already registered")

    created_story = story_service.create_story(db, story)

    story_response = StoryResponse(
        id=created_story.id,
        title=created_story.title,
        genre=created_story.genre,
        current_segment_id=created_story.current_segment_id,
        creation_date=created_story.creation_date,
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Story created successfully",
            "story": story_response,
        },
    )
