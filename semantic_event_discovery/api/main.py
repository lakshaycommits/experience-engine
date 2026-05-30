import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from core.models import SearchQuery, SearchResponse
from core.search import semantic_search, seed_events, collection_count, ensure_collection


def _load_demo_events() -> list[dict]:
    from data.scrape_events import get_enriched_events
    return get_enriched_events()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up Semantic Event Discovery API...")
    ensure_collection()
    if collection_count() == 0:
        print("No events in Qdrant — seeding demo dataset...")
        events = _load_demo_events()
        seed_events(events)
        print(f"Seeded {collection_count()} events. Ready.")
    else:
        print(f"Qdrant has {collection_count()} events. Ready.")
    yield


app = FastAPI(
    title="Semantic Event Discovery",
    description=(
        "Intent-aware semantic search for Delhi events. "
        "Built to show what District's search could be — natural language, not keywords."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "events_indexed": collection_count(),
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
    }


@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
    """
    Semantic event search. Try these demo queries:

    - "something fun to do alone at night 2am"
    - "first date idea under 1500 rupees"
    - "like NH7 Weekender but in Delhi"
    - "chill Sunday morning activity"
    """
    if not query.text.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return await semantic_search(query)


@app.get("/events")
async def list_events(limit: int = 20, offset: int = 0):
    """Browse all indexed events."""
    from core.search import get_qdrant, COLLECTION_NAME

    client = get_qdrant()
    results, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=min(limit, 100),
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )
    return {
        "events": [r.payload for r in results],
        "total": collection_count(),
        "limit": limit,
        "offset": offset,
    }


@app.get("/")
async def root():
    return {
        "message": "Semantic Event Discovery API",
        "docs": "/docs",
        "search": "POST /search",
        "demo_queries": [
            "something fun to do alone at night 2am",
            "first date idea under 1500 rupees",
            "like NH7 Weekender but in Delhi",
            "chill Sunday morning activity",
        ],
    }
