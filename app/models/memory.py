from datetime import datetime

from pydantic import BaseModel

class MemoryItemCreate(BaseModel):
    content: str

class MemoryItem(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    importance_score: float
    access_count: int

class MemoryItemUpdate(BaseModel):
    title: str|None= None
    content: str|None= None