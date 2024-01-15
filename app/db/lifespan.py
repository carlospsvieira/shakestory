from contextlib import asynccontextmanager
from fastapi import FastAPI

# Create a dictionary to store shared resources or states
shared_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Initialize resources, database connections, etc.
    shared_state["database"] = "Initialized Database"
    yield
    # Shutdown logic: Cleanup resources, close database connections, etc.
    shared_state.clear()

app = FastAPI(lifespan=lifespan)
