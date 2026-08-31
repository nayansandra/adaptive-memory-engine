import math

def cosine_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))

    magnitude_a = math.sqrt(sum(a * a for a in embedding_a))

    magnitude_b = math.sqrt(sum(b * b for b in embedding_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)