from fastapi import FastAPI
from app.db.session import engine
from app.db.session import Base
from app.routes.routes import routes

app = FastAPI()

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()

routes(app)
