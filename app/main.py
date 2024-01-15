from fastapi import FastAPI
from app.db.session import engine
from app.db.session import Base

app = FastAPI()

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()

@app.get("/")
def read_root():
    return {"message": "hello Shakestory, now running with db"}
