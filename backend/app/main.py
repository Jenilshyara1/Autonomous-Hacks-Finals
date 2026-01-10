from fastapi import FastAPI
from .database import engine, Base
from .routes import processing

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Privilege Logging Pipeline", lifespan=lifespan)

app.include_router(processing.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Privilege Logging Pipeline API is running"}
