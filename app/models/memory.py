from datetime import datetime

from pydantic import BaseModel, Field, field_validator

class MemoryItemCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Content cannot be empty or whitespace.")
        return value

class MemoryItem(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    importance_score: float
    access_count: int

class MemoryItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    content: str | None = Field(default=None, min_length=1)

    @field_validator("title", "content")
    @classmethod
    def validate_strings(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty or whitespace.")

        return value