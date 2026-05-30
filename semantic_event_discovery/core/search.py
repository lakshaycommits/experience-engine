import os
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchAny,
    PayloadSchemaType,
)

from core.models import SearchQuery, SearchResponse, SearchResultItem, IntentResult
from core.embedder import embed_text, embed_batch, build_semantic_string
from core.intent_parser import parse_intent
from core.reranker import rerank

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "district_events")
VECTOR_SIZE = 384  # all-MiniLM-L6-v2

_qdrant: Optional[QdrantClient] = None


def get_qdrant() -> QdrantClient:
    global _qdrant
    if _qdrant is None:
        host = os.getenv("QDRANT_HOST", "localhost")
        if host in (":memory:", "memory"):
            _qdrant = QdrantClient(location=":memory:")
        else:
            _qdrant = QdrantClient(host=host, port=int(os.getenv("QDRANT_PORT", "6333")))
    return _qdrant


def ensure_collection():
    client = get_qdrant()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        for field in ("time_of_day", "social_context", "price_tier", "city"):
            client.create_payload_index(COLLECTION_NAME, field, PayloadSchemaType.KEYWORD)
        print(f"Created Qdrant collection: {COLLECTION_NAME}")


def collection_count() -> int:
    try:
        return get_qdrant().get_collection(COLLECTION_NAME).points_count or 0
    except Exception:
        return 0


def seed_events(events: list[dict]):
    ensure_collection()
    client = get_qdrant()

    for e in events:
        if not e.get("semantic_string"):
            e["semantic_string"] = build_semantic_string(e)

    texts = [e["semantic_string"] for e in events]
    print(f"Embedding {len(events)} events...")
    vectors = embed_batch(texts)

    points = [
        PointStruct(id=i, vector=vec, payload=event)
        for i, (event, vec) in enumerate(zip(events, vectors))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Seeded {len(points)} events into Qdrant.")


def _build_filter(intent: IntentResult) -> Optional[Filter]:
    conditions = []

    tod = intent.temporal_context.time_of_day
    if tod != "any":
        # Cast a wide net — include adjacent time slots
        tod_values = {
            "late_night": ["late_night", "evening"],
            "evening": ["evening", "late_night", "afternoon"],
            "morning": ["morning", "afternoon", "all_day"],
            "afternoon": ["afternoon", "morning", "evening", "all_day"],
        }.get(tod, [tod, "all_day"])
        conditions.append(FieldCondition(key="time_of_day", match=MatchAny(any=tod_values)))

    social = intent.social_context
    if social != "any":
        social_map = {
            "solo": "solo_ok",
            "couple": "couples",
            "group": "groups",
            "family": "family",
        }
        social_val = social_map.get(social, social)
        conditions.append(FieldCondition(key="social_context", match=MatchAny(any=[social_val])))

    return Filter(must=conditions) if conditions else None


def _match_reason(query: str, event: dict, intent: IntentResult) -> str:
    reasons = []

    tod = intent.temporal_context.time_of_day
    event_tod = event.get("time_of_day", [])
    if tod == "late_night" and "late_night" in event_tod:
        end = event.get("end_time", "")
        reasons.append(f"Open until {end}" if end else "Late-night event")
    elif tod == "morning" and "morning" in event_tod:
        reasons.append(f"Morning slot — starts at {event.get('time', '')}")
    elif tod == "evening" and "evening" in event_tod:
        reasons.append("Evening event")

    social = intent.social_context
    sc = event.get("social_context", [])
    if social == "solo" and "solo_ok" in sc:
        reasons.append("Solo-friendly atmosphere")
    elif social == "couple" and "couples" in sc:
        reasons.append("Great for couples")
    elif social == "group" and "groups" in sc:
        reasons.append("Perfect for groups")

    vibe_overlap = set(intent.vibe) & set(event.get("vibe_tags", []))
    if vibe_overlap:
        reasons.append(f"Matches vibe: {', '.join(sorted(vibe_overlap)[:3])}")

    max_price = intent.structured_filters.get("max_price_per_person")
    if max_price and event.get("price_max", 9999) <= max_price:
        reasons.append(f"Within budget (₹{event['price_min']}–{event['price_max']})")


    q = query.lower()
    if not reasons:
        cat = event.get("category", "")
        area = event.get("area", "Delhi")
        reasons.append(f"Semantic match — {cat} in {area}")

    return " · ".join(reasons)


async def semantic_search(query: SearchQuery) -> SearchResponse:
    # 1. Parse intent
    intent = await parse_intent(query.text)

    # 2. Embed the rewritten query
    query_vec = embed_text(intent.rewritten_query or query.text)

    # 3. Vector search (top-50 candidates with optional filter)
    client = get_qdrant()
    search_filter = _build_filter(intent)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vec,
        query_filter=search_filter,
        limit=50,
        with_payload=True,
    )
    results = response.points

    # Retry without filters if too few results
    if len(results) < 5 and search_filter is not None:
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vec,
            limit=50,
            with_payload=True,
        )
        results = response.points

    candidates = []
    for r in results:
        payload = dict(r.payload or {})
        payload["vector_score"] = r.score
        candidates.append(payload)

    # 4. Post-filter on price if requested
    max_price = intent.structured_filters.get("max_price_per_person")
    if max_price:
        filtered = [c for c in candidates if c.get("price_max", 9999) <= max_price * 1.25]
        if len(filtered) >= 3:
            candidates = filtered

    total_candidates = len(candidates)

    # 5. Re-rank
    reranked = rerank(query.text, candidates)

    # 6. Build response items
    items = []
    for event in reranked[: query.limit]:
        items.append(
            SearchResultItem(
                id=event.get("id", ""),
                title=event.get("title", ""),
                venue=event.get("venue", ""),
                area=event.get("area", ""),
                date=event.get("date", ""),
                time=event.get("time", ""),
                end_time=event.get("end_time"),
                category=event.get("category", ""),
                price_min=event.get("price_min", 0),
                price_max=event.get("price_max", 0),
                price_tier=event.get("price_tier", ""),
                description=event.get("description", ""),
                vibe_tags=event.get("vibe_tags", []),
                social_context=event.get("social_context", []),
                energy_level=event.get("energy_level", ""),
                indoor_outdoor=event.get("indoor_outdoor", ""),
                score=round(event.get("vector_score", 0.0), 4),
                match_reason=_match_reason(query.text, event, intent),
            )
        )

    return SearchResponse(
        results=items,
        intent_parsed=intent,
        total_candidates=total_candidates,
        query=query.text,
    )
