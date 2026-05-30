"""
Q&A system: in-memory Qdrant knowledge base + Groq for answer generation.
No external services needed — Qdrant runs in-memory, seeded at startup.
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from sentence_transformers import SentenceTransformer

COLLECTION = "event_knowledge"

_qdrant: QdrantClient | None = None
_embedder: SentenceTransformer | None = None
_seeded = False


def get_qdrant() -> QdrantClient:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantClient(":memory:")
    return _qdrant


def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        print("Loading sentence-transformer model...")
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded.")
    return _embedder


def seed_knowledge_base(chunks: list[dict]) -> None:
    global _seeded
    if _seeded:
        return

    client = get_qdrant()
    embedder = get_embedder()

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    points = []
    for i, chunk in enumerate(chunks):
        vector = embedder.encode(chunk["content"]).tolist()
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "event_id": chunk["event_id"],
                    "chunk_type": chunk["chunk_type"],
                    "source": chunk["source"],
                    "content": chunk["content"],
                },
            )
        )

    client.upsert(collection_name=COLLECTION, points=points)
    _seeded = True
    print(f"Knowledge base seeded with {len(points)} chunks.")


async def answer_question(
    event_id: str,
    event_title: str,
    event_date: str,
    venue: str,
    question: str,
) -> dict:
    from groq import Groq

    client = get_qdrant()
    embedder = get_embedder()

    query_vector = embedder.encode(question).tolist()

    response = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        query_filter=Filter(
            must=[FieldCondition(key="event_id", match=MatchValue(value=event_id))]
        ),
        limit=4,
        with_payload=True,
    )
    results = response.points

    if not results:
        return {
            "answer": "I don't have enough information to answer that. Contact the organiser directly for details.",
            "confidence": "low",
            "sources": [],
            "caveat": None,
        }

    context = "\n\n".join([r.payload["content"] for r in results])
    sources = [
        {"type": r.payload["chunk_type"], "label": r.payload["source"]}
        for r in results[:3]
    ]

    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

    response = groq_client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[
            {
                "role": "user",
                "content": f"""You are a helpful assistant for District, India's going-out app.

A user is considering attending this event and has a question.
Answer ONLY from the provided context. If the context doesn't clearly answer the question, say so honestly.

Event: {event_title}
Date: {event_date}
Venue: {venue}

Context (from venue reviews, event info, artist bios):
{context}

User question: {question}

Rules:
1. Be direct — answer the question, don't pad with filler
2. Be specific — use exact details from context (prices, times, dress codes, distances)
3. If you truly don't know, say "I don't have that information — contact the organiser directly"
4. If the answer might change, add a brief note to verify closer to the event
5. Maximum 3 sentences — be concise
6. Warm, helpful tone — you're helping someone decide whether to go

Answer:""",
            }
        ],
        temperature=0.1,
        max_tokens=200,
    )

    answer = response.choices[0].message.content.strip()
    max_score = max(r.score for r in results)
    confidence = "high" if max_score > 0.55 else "medium" if max_score > 0.35 else "low"

    caveat = None
    if confidence in ("high", "medium"):
        caveat = "Based on venue reviews and event information — verify time-sensitive details with the organiser."

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
        "caveat": caveat,
    }
