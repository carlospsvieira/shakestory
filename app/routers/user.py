from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import user_service
from app.models.requests import UserCreate

router = APIRouter()


@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = user_service.create_user(db, user)

    user_dict = {
        "id": created_user.id,
        "username": created_user.username,
        "email": created_user.email,
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User registered successfully",
            "user": user_dict,
        },
    )


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int = Path(..., title="The ID of the user to delete", ge=1),
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_service.delete_user(db, user_id)

    return {"message": "User deleted successfully"}
