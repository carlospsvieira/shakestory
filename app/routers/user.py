from fastapi import APIRouter, Depends, Form, HTTPException, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.requests import UserCreate, UserLogin, UserResponse
from app.db.session import get_db
from app.services import user_service
from app.dependencies.authentication import authenticate_user
from app.utils.helpers import validate_password_format

router = APIRouter()


@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not validate_password_format(user.password):
        raise HTTPException(status_code=400, detail="Password format isn't valid")

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


@router.post("/login", response_model=dict)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, user_login)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User logged in successfully",
            "token": token["access_token"],
        },
    )


@router.put("/users/{user_id}/password", response_model=dict)
async def update_password(
    user_id: int = Path(..., title="The ID of the user to update", ge=1),
    new_password: str = Form(..., title="The new password"),
    db: Session = Depends(get_db),
):
    if not validate_password_format(new_password):
        raise HTTPException(status_code=400, detail="Password format isn't valid")

    updated_user = user_service.update_password(db, user_id, new_password)
    if updated_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Password updated!"},
        )
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int = Path(..., title="The ID of the user to delete", ge=1),
    db: Session = Depends(get_db),
):
    user_service.delete_user(db, user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "User was deleted"}
    )
