from fastapi import APIRouter, HTTPException
from app.models.memory import MemoryItem, MemoryItemCreate, MemoryItemUpdate
from app.storage.memory_store import memory_store
from app.services import memory_service

router = APIRouter()

@router.get("/memory-items", response_model=list[MemoryItem])
def get_memories():
    return memory_store

@router.post("/memory-items", response_model=MemoryItem)
def create_memory(memory: MemoryItemCreate):
    return memory_service.create_memory(memory)

@router.get("/memory-items/{memory_id}", response_model=MemoryItem)
def get_memory(memory_id: int):
    memory = memory_service.find_memory(memory_id)

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with id {memory_id} not found."
        )

    return memory

@router.patch("/memory-items/{memory_id}", response_model=MemoryItem)
def update_memory(memory_id: int, update: MemoryItemUpdate):
    if update.title is None and update.content is None:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided."
        )

    memory = memory_service.update_memory(memory_id, update)

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with id {memory_id} not found."
        )

    return memory

@router.delete("/memory-items/{memory_id}", status_code=204)
def delete_memory(memory_id: int):
    deleted = memory_service.delete_memory(memory_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Memory with id {memory_id} not found."
        )

    return