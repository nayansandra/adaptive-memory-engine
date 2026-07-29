from datetime import datetime
from fastapi import FastAPI
from app.models.memory import MemoryItemCreate, MemoryItem

app = FastAPI()

memory_store = []
next_id=1

@app.get("/")
def root():
    return {
        "message": "Hello Nayan!",
        "project": "Adaptive Memory Engine",
        "status": "Learning FastAPI 🚀"
        }

@app.post("/memory-items", response_model=MemoryItem)
def create_memory(memory: MemoryItemCreate):
    global next_id

    memory_item = MemoryItem(
        id=next_id,
        title=memory.content[:30],
        content=memory.content,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        importance_score=0.0,
        access_count=0
    )

    memory_store.append(memory_item)
    next_id += 1
    
    return memory_item