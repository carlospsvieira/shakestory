from sqlalchemy.orm import Session
from app.db.base import User
from app.models.requests import UserCreate


def create_user(db: Session, user: UserCreate):
    hashed_password = user.password
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
