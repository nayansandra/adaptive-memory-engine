from app.database.database import SessionLocal
from app.models.memory_db import Memory
from app.services.embedding_service import generate_embedding


db = SessionLocal()

memories = db.query(Memory).all()

updated_count = 0

for memory in memories:

    if memory.embedding:
        continue

    try:
        memory.embedding = generate_embedding(
            memory.content
        )
        updated_count += 1

    except ValueError:
        print(
            f"Skipping memory {memory.id}: empty content"
        )

db.commit()

print(
    f"Generated embeddings for {updated_count} memories."
)