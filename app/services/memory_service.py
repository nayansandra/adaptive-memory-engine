from datetime import datetime

from app.models.memory import MemoryItem, MemoryItemCreate, MemoryItemUpdate
from app.storage.memory_store import memory_store


next_id = 1

def create_memory(memory: MemoryItemCreate) -> MemoryItem:
    global next_id

    now = datetime.now()

    memory_item = MemoryItem(
        id=next_id,
        title=memory.content[:30],
        content=memory.content,
        created_at=now,
        updated_at=now,
        importance_score=0.0,
        access_count=0,
    )

    memory_store.append(memory_item)
    next_id += 1

    return memory_item

def find_memory(memory_id: int) -> MemoryItem|None:
    for memory in memory_store:
        if memory.id == memory_id:
            return memory
    return None

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