import os
from sqlalchemy.orm import Session
from app.models.requests import UserLogin
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from app.services.user_service import get_user_by_username

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": data.get("username"),
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def authenticate_user(db: Session, user_login: UserLogin):
    user = get_user_by_username(db, user_login.username)

    if user and bcrypt.checkpw(
        user_login.password.encode("utf-8"), user.password
    ):
        access_token = create_access_token({"username": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    return None
