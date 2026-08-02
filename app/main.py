from fastapi import FastAPI
from app.api.memory import router as memory_router
from app.models import memory_db
from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(memory_router)

@app.get("/")
def root():
    return {"message": "Adaptive Memory Engine is running!"}