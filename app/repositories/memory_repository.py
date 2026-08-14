from sqlalchemy.orm import Session
from app.models.memory_db import Memory
from datetime import datetime, timezone

def get_by_id(db: Session, memory_id: int) -> Memory | None:
    return db.query(Memory).filter(Memory.id == memory_id).first()

def get_all(db: Session) -> list[Memory]:
    return db.query(Memory).all()

def create(db: Session, memory: Memory) -> Memory:
    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory

def update(db: Session, memory: Memory) -> Memory:
    db.commit()
    db.refresh(memory)

    return memory

def delete(db: Session, memory: Memory) -> None:
    db.delete(memory)
    db.commit()

def record_access(db: Session, memory: Memory) -> Memory:

    memory.access_count += 1
    memory.last_accessed_at = datetime.now(timezone.utc)
    memory.importance_score = memory.access_count

    db.commit()
    db.refresh(memory)

    return memory