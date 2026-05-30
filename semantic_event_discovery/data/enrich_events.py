"""
LLM enrichment pipeline using Groq.
Reads raw_events.json, enriches each event, saves to enriched_events.json.

For the demo, this step is OPTIONAL — scrape_events.py already provides
pre-enriched events. Run this only if you want to re-enrich with Groq.
"""
import os
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent



ENRICH_PROMPT = """You are enriching a Delhi events listing for a semantic search system.

Given this event, extract structured metadata. Return ONLY valid JSON.

Event:
{event_json}

Return JSON with exactly these fields:
{{
  "semantic_description": "2-3 sentences capturing the vibe, ideal audience, and experience. Be specific and evocative.",
  "vibe_tags": ["8-12 single words: party/chill/romantic/indie/jazz/underground/family/solo/etc"],
  "time_of_day": ["array of applicable: morning/afternoon/evening/late_night/all_day"],
  "energy_level": "low or medium or high",
  "social_context": ["array of applicable: solo_ok/couples/groups/family"],
  "indoor_outdoor": "indoor or outdoor or both",
  "price_tier": "free or budget or mid or premium"
}}"""


async def enrich_event(client, event: dict) -> dict:
    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {
                    "role": "user",
                    "content": ENRICH_PROMPT.format(event_json=json.dumps(event, indent=2)),
                }
            ],
            temperature=0.2,
            max_tokens=500,
            response_format={"type": "json_object"},
        )
        enrichment = json.loads(response.choices[0].message.content)
        return {**event, **enrichment}
    except Exception as e:
        print(f"  Failed to enrich '{event.get('title', '?')}': {e}")
        return event


async def main():
    from groq import Groq

    raw_path = DATA_DIR / "raw_events.json"
    enriched_path = DATA_DIR / "enriched_events.json"

    if not raw_path.exists():
        print("raw_events.json not found. Run: python -m data.scrape_events")
        return

    with open(raw_path) as f:
        events = json.load(f)

    print(f"Enriching {len(events)} events via Groq...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

    enriched = []
    for i, event in enumerate(events):
        print(f"  [{i + 1}/{len(events)}] {event['title']}")
        enriched_event = await enrich_event(client, event)
        enriched.append(enriched_event)
        await asyncio.sleep(0.15)  # stay within rate limits

    with open(enriched_path, "w") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(enriched)} enriched events → {enriched_path}")


if __name__ == "__main__":
    asyncio.run(main())
