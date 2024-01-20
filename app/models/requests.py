from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class StoryCreate(BaseModel):
    title: str
    genre: str
    content: str = Field(..., max_length=500)


class StoryResponse(BaseModel):
    id: int
    current_segment_id: int
    user_id: int

    class Config:
        orm_mode = True


class SegmentCreate(BaseModel):
    content: str


class SegmentResponse(BaseModel):
    id: int
    content: str
    story_id: int
    user: UserResponse
    contribution_date: str
    upvotes: int
    downvotes: int
