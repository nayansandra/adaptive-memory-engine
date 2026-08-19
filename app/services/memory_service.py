from datetime import datetime
from app.models.memory import MemoryItemCreate, MemoryItemUpdate
from sqlalchemy.orm import Session
from app.models.memory_db import Memory
from app.repositories import memory_repository

def calculate_recency_factor(last_accessed_at):

    if last_accessed_at is None:
        return 1.0

    age = datetime.now() - last_accessed_at

    days = age.days

    if days <= 1:
        return 1.0

    if days <= 7:
        return 0.8

    if days <= 30:
        return 0.5

    return 0.2

def calculate_effective_score(importance_score: float, last_accessed_at) -> float:

    factor = calculate_recency_factor(last_accessed_at)

    return importance_score * factor

def create_memory(memory: MemoryItemCreate, db: Session) -> Memory:
    now = datetime.now()

    db_memory = Memory(
        title=memory.content[:30],
        content=memory.content,
        created_at=now,
        updated_at=now,
        importance_score=0.0,
        access_count=0,
    )

    return memory_repository.create(db,db_memory)

def get_memories(db: Session) -> list[Memory]:
    return memory_repository.get_all(db)

def find_memory(memory_id: int, db: Session) -> Memory | None:
    return memory_repository.get_by_id(db,memory_id)

def update_memory(memory_id: int, update: MemoryItemUpdate, db: Session) -> Memory | None:

    memory = find_memory(memory_id, db)

    if memory is None:
        return None

    if update.title is not None:
        memory.title = update.title

    if update.content is not None:
        memory.content = update.content

    memory.updated_at = datetime.now()

    return memory_repository.update(db,memory)

def delete_memory(memory_id: int, db: Session) -> bool:
    memory = find_memory(memory_id, db)

    if memory is None:
        return False

    memory_repository.delete(db,memory)
    
    return True

def get_memory_and_track_access(memory_id: int, db: Session) -> Memory | None:

    memory = memory_repository.get_by_id(db, memory_id)

    if memory is None:
        return None

    return memory_repository.record_access(db, memory)