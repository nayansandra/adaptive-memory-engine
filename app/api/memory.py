from fastapi import APIRouter, Depends, HTTPException
from app.models.memory import MemoryItem, MemoryItemCreate, MemoryItemUpdate
from app.services import memory_service
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter()

@router.get("/memory-items", response_model=list[MemoryItem])
def get_memories(db: Session = Depends(get_db)):
    
    return memory_service.get_memories(db)

@router.post("/memory-items", response_model=MemoryItem)
def create_memory(memory: MemoryItemCreate, db: Session = Depends(get_db)):

    return memory_service.create_memory(memory, db)

@router.get("/memory-items/ranked", response_model=list[MemoryItem])
def get_ranked_memories(db: Session = Depends(get_db)):
    return memory_service.get_ranked_memories(db)

@router.get("/memory-items/search", response_model=list[MemoryItem])
def search_memories(query: str, db: Session = Depends(get_db)):
    try:
        return memory_service.search_memories(query, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/memory-items/semantic-search", response_model=list[MemoryItem])
def semantic_search_memories(query: str, db: Session = Depends(get_db)):
    try:
        return memory_service.semantic_search(query, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/memory-items/{memory_id}", response_model=MemoryItem)
def get_memory(memory_id: int, db: Session = Depends(get_db)):
    memory = memory_service.get_memory_and_track_access(memory_id, db)

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with id {memory_id} not found."
        )

    return memory

@router.patch("/memory-items/{memory_id}", response_model=MemoryItem)
def update_memory(memory_id: int, update: MemoryItemUpdate, db: Session = Depends(get_db)):
    if update.title is None and update.content is None:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided."
        )

    memory = memory_service.update_memory(memory_id, update, db)

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with id {memory_id} not found."
        )

    return memory

@router.delete("/memory-items/{memory_id}", status_code=204)
def delete_memory(memory_id: int, db: Session = Depends(get_db)):

    deleted = memory_service.delete_memory(memory_id, db)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with id {memory_id} not found."
        )

    return