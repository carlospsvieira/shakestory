from fastapi import APIRouter, Depends, Form, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.base import User
from app.db.session import get_db
from app.dependencies.authentication import get_current_user
from app.services import story_service
from app.models.requests import StoryCreate, StoryResponse, UserResponse
from app.utils.helpers import validate_story_content

router = APIRouter()


@router.post("/story/new", response_model=StoryResponse)
async def new_story(
    story: StoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_story = story_service.get_story_by_title(db, story.title)
    if existing_story:
        raise HTTPException(status_code=400, detail="Title already registered")

    if not validate_story_content(story.content):
        raise HTTPException(status_code=400, detail="Invalid story content")

    created_story = story_service.create_story(db, story, current_user.id)

    story_response = StoryResponse(
        id=created_story.id,
        current_segment_id=0,
        user_id=current_user.id,
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Story created successfully",
            "story": story_response,
        },
    )


@router.put("/stories/{story_id}/title", response_model=dict)
async def update_title(
    story_id: int = Path(..., title="The ID of the title to update", ge=1),
    new_title: str = Form(..., title="The new title"),
    db: Session = Depends(get_db),
):
    if len(new_title) > 100:
        raise HTTPException(status_code=400, detail="Title has too many characters")

    updated_story = story_service.update_title(db, story_id, new_title)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"title": updated_story.title, "message": "Title updated!"},
    )


@router.delete("/stories/{story_id}", response_model=dict)
async def delete_story(
    story_id: int = Path(..., title="The ID of the story to delete", ge=1),
    db: Session = Depends(get_db),
):
    story_service.delete_story(db, story_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Story was deleted"}
    )
