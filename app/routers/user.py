from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import user_service
from app.models.requests import UserCreate

router = APIRouter()


@router.post("/register/", response_model=UserCreate)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = user_service.create_user(db, user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User registered successfully",
            "user": created_user.dict(),
        },
    )
