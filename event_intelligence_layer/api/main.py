import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from core.models import AskRequest, AskResponse, Source
from core.qa import seed_knowledge_base, answer_question
from data.events import get_all_events, get_event_by_id, get_all_knowledge_chunks

STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Event Intelligence Layer demo...")
    chunks = get_all_knowledge_chunks()
    seed_knowledge_base(chunks)
    print(f"Ready — {len(get_all_events())} events, {len(chunks)} knowledge chunks.")
    yield


app = FastAPI(
    title="Event Intelligence Layer",
    description="Per-event Q&A and enrichment demo for District.",
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
        "events": len(get_all_events()),
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
    }


@app.get("/events")
async def list_events():
    events = get_all_events()
    return [
        {k: v for k, v in e.items() if k != "knowledge_chunks"}
        for e in events
    ]


@app.get("/events/{event_id}")
async def get_event(event_id: str):
    event = get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {k: v for k, v in event.items() if k != "knowledge_chunks"}


@app.post("/events/{event_id}/ask", response_model=AskResponse)
async def ask(event_id: str, body: AskRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    event = get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    result = await answer_question(
        event_id=event_id,
        event_title=event["title"],
        event_date=event["date"],
        venue=event["venue"],
        question=body.question.strip(),
    )

    return AskResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        sources=[Source(**s) for s in result["sources"]],
        caveat=result.get("caveat"),
    )


# Serve frontend
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))
