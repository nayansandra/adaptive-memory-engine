from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list[float]:

    if not text.strip():
        raise ValueError(
            "Cannot generate embedding for empty text."
        )

    return model.encode(text).tolist()