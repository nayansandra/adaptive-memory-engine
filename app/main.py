from typing import List
from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.models.memory import MemoryItemCreate, MemoryItem, MemoryItemUpdate

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

    now=datetime.now()

    memory_item = MemoryItem(
        id=next_id,
        title=memory.content[:30],
        content=memory.content,
        created_at=now,
        updated_at=now,
        importance_score=0.0,
        access_count=0
    )

    memory_store.append(memory_item)
    next_id += 1

    return memory_item

@app.get("/memory-items", response_model=List[MemoryItem])
def get_memories():
    return memory_store

@app.get("/memory-items/{memory_id}", response_model=MemoryItem)
def get_memory(memory_id: int):
    for memory in memory_store:
        if memory.id == memory_id:
            return memory
        
    raise HTTPException(
        status_code=404, 
        detail=f"Memory with id {memory_id} not found."
        )

@app.patch("/memory-items/{memory_id}", response_model=MemoryItem)
def update_memory(memory_id: int, update: MemoryItemUpdate):
    if update.title is None and update.content is None:
        raise HTTPException(
            status_code=400, 
            detail="At least one field must be provided."
        )
    for memory in memory_store:
        if memory.id == memory_id:
            if update.title is not None:
                memory.title = update.title
            if update.content is not None:
                memory.content = update.content
            memory.updated_at = datetime.now()
            return memory
        
    raise HTTPException(
        status_code=404, 
        detail=f"Memory with id {memory_id} not found."
        )