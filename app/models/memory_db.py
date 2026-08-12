from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.database.database import Base

class Memory(Base):
    __tablename__ = "memory_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    importance_score = Column(Float, nullable=False, default=0.0)
    access_count = Column(Integer, nullable=False, default=0)
    last_accessed_at = Column(DateTime, nullable=True)