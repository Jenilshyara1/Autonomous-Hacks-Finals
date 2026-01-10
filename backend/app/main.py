from fastapi import FastAPI
from .database import engine, Base
from .routes import processing

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Privilege Logging Pipeline")

app.include_router(processing.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Privilege Logging Pipeline API is running"}
