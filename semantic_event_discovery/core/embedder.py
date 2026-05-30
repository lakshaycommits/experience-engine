import os
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        print(f"Loading embedding model: {model_name}")
        _model = SentenceTransformer(model_name)
    return _model


def embed_text(text: str) -> list[float]:
    return get_model().encode(text, normalize_embeddings=True).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    return get_model().encode(texts, normalize_embeddings=True).tolist()


def build_semantic_string(event: dict) -> str:
    parts = []

    if event.get("semantic_description"):
        parts.append(event["semantic_description"])

    parts.append(f"Event: {event['title']}")
    parts.append(f"Type: {event['category']}")
    if event.get("subcategory"):
        parts.append(f"Subcategory: {event['subcategory']}")

    parts.append(f"Location: {event['venue']}, {event['area']}, Delhi")

    time_str = event.get("time", "")
    if event.get("end_time"):
        time_str += f" to {event['end_time']}"
    if time_str:
        parts.append(f"Time: {time_str}")

    parts.append(f"Date: {event.get('date', '')}")

    if event.get("vibe_tags"):
        parts.append(f"Vibe: {', '.join(event['vibe_tags'])}")

    if event.get("time_of_day"):
        parts.append(f"Time of day: {', '.join(event['time_of_day'])}")

    if event.get("energy_level"):
        parts.append(f"Energy: {event['energy_level']}")

    if event.get("social_context"):
        parts.append(f"Good for: {', '.join(event['social_context'])}")

    if event.get("indoor_outdoor"):
        parts.append(f"Setting: {event['indoor_outdoor']}")

    if event.get("price_tier"):
        parts.append(
            f"Price: {event['price_tier']} (₹{event.get('price_min', 0)}–{event.get('price_max', 0)})"
        )

    if event.get("tags"):
        parts.append(f"Tags: {', '.join(event['tags'])}")

    if event.get("description"):
        parts.append(event["description"])

    return " | ".join(p for p in parts if p)
