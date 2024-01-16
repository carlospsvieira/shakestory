from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.requests import UserCreate, UserLogin, UserResponse
from app.db.session import get_db
from app.services import user_service
from app.dependencies.authentication import authenticate_user

router = APIRouter()


@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = user_service.create_user(db, user)

    user_response = UserResponse(
        id=created_user.id, username=created_user.username, email=created_user.email
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User registered successfully",
            "user": user_response,
        },
    )


@router.post("/login", response_model=UserResponse)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, user_login)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = user_service.get_user_by_username(db, user_login.username)
    user_response = UserResponse(
        id=user.id, username=user.username, email=user.email
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User logged in successfully",
            "token": token["access_token"],
            "user": user_response,
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

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "User was deleted"}
    )
