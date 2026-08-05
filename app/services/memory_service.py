from datetime import datetime
from app.models.memory import MemoryItem, MemoryItemCreate, MemoryItemUpdate
from app.storage.memory_store import memory_store
from sqlalchemy.orm import Session
from app.models.memory_db import Memory


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

    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)

    return db_memory

def get_memories(db: Session) -> list[Memory]:
    return db.query(Memory).all()

def find_memory(memory_id: int, db: Session) -> Memory | None:
    return db.query(Memory).filter(Memory.id == memory_id).first()

def update_memory(memory_id: int, update: MemoryItemUpdate) -> MemoryItem | None:

    memory = find_memory(memory_id)

    if memory is None:
        return None

    if update.title is not None:
        memory.title = update.title

    if update.content is not None:
        memory.content = update.content

    memory.updated_at = datetime.now()

    return memory

def delete_memory(memory_id: int) -> bool:
    memory = find_memory(memory_id)

    if memory is None:
        return False

    memory_store.remove(memory)
    return True