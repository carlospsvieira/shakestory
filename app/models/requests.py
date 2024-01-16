from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class StoryCreate(BaseModel):
    title: str
    genre: str


class StoryResponse(BaseModel):
    id: int
    title: str
    genre: str
    current_segment_id: int
    creation_date: str
    user: UserResponse


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
