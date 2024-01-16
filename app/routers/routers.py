from fastapi import APIRouter
from .user import router as user_router
from .story import router as story_router
from .segment import router as segment_router

router = APIRouter()

router.include_router(user_router)
router.include_router(story_router)
router.include_router(segment_router)
