from fastapi import FastAPI
from app.api.memory import router as memory_router


app = FastAPI()
app.include_router(memory_router)

@app.get("/")
def root():
    return {"message": "Adaptive Memory Engine is running!"}