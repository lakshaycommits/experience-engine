# District AI — Mood & Deets

**By Lakshay** · Backend & AI Engineer

> Two working demos that show what District's discovery experience could be — grounded in real product gaps, not slides.

---

## The Problem

These queries were tested live on District (May 2026):

| Query | District returns | What the user wants |
|---|---|---|
| `something fun to do alone at night 2am` | Fun n Food Water Park, Raymond clothing | Late-night solo events |
| `something that is new` | NEWME brand, New Balance shoes | New events, recently opened places |
| `first date idea under 1500 rupees` | Irrelevant keyword hits | Romantic spots under budget |

District's search does substring matching. It has no understanding of intent — time, social context, vibe, or budget. Every query that returns noise is a user who doesn't book.

The second problem: event pages are ads. Title, date, price, and whatever the organiser wrote. No answer to the questions that actually drive decisions — "is this good for a first date?", "what should I wear?", "how do I get there by metro?"

Both problems are solvable. These demos show how.

---

## The Two Features

### [Mood](./semantic_event_discovery/README.md)

Intent-aware search. Natural language queries return relevant results because the system understands *what the user means*, not just what words they typed.

```
"something fun to do alone at night 2am"
  → time: late_night  ·  social: solo  ·  vibe: fun, casual
  → results: midnight cycling tour, gaming café, karaoke bar
```

**Stack:** FastAPI · Qdrant · sentence-transformers · Groq (Llama 3.1 8B) · cross-encoder re-ranking

---

### [Deets](./event_intelligence_layer/README.md)

Per-event Q&A. Every event gets a knowledge base built from venue reviews, artist bios, and event info. Users can ask anything before they book — and get grounded answers, not hallucinations.

```
"Is this good for a first date?"
  → "Yes — Siri Fort Auditorium has intimate seating and the acoustic
     format keeps the music at a conversational volume. Most attendees
     are couples. Dress smart casual."
     Confidence: high  ·  Source: Concert reviews, Event profile
```

**Stack:** FastAPI · Qdrant (in-memory) · sentence-transformers · Groq (Llama 3.1 8B)

---

## Running the Demos

Both features need a Groq API key (free tier at [console.groq.com](https://console.groq.com)).

**Semantic Event Discovery** — requires Docker for Qdrant:

```bash
cd semantic_event_discovery
cp .env.example .env        # add GROQ_API_KEY
docker-compose up -d qdrant
pip install -r requirements.txt
uvicorn api.main:app --reload
# Open ui/index.html in browser — points to localhost:8000
```

**Event Intelligence Layer** — no Docker needed, Qdrant runs in-memory:

```bash
cd event_intelligence_layer
cp .env.example .env        # add GROQ_API_KEY
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8001
# Open http://localhost:8001
```

---

## How They Connect

Event Intelligence builds structured event profiles — vibe tags, social context, energy level, semantic descriptions. Semantic Search uses those exact profiles to match intent queries against meaning, not keywords.

They're the same pipeline: enrich events → search them intelligently → answer questions about them.

---

*Lakshay — Backend & AI Engineer*
*FastAPI · Qdrant · Kafka · LangGraph · sentence-transformers · Groq*
