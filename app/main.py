from fastapi import FastAPI
from app.db.session import engine
from app.db.session import Base
from app.routers.routers import router as main_router

app = FastAPI()


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()

app.include_router(main_router)
