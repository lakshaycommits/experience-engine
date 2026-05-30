"""
Seeds enriched events into Qdrant.

Usage:
    python -m data.seed_qdrant

Reads enriched_events.json if present, otherwise uses the built-in demo events.
Requires Qdrant running (docker-compose up qdrant).
"""
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent


def main():
    enriched_path = DATA_DIR / "enriched_events.json"

    if enriched_path.exists():
        print(f"Loading from {enriched_path}")
        with open(enriched_path) as f:
            events = json.load(f)
    else:
        print("enriched_events.json not found — using built-in demo events")
        from data.scrape_events import get_enriched_events
        events = get_enriched_events()

    from core.search import seed_events, ensure_collection, collection_count

    ensure_collection()
    current = collection_count()
    if current > 0:
        print(f"Qdrant already has {current} events.")
        answer = input("Re-seed? This will add duplicates (y/N): ").strip().lower()
        if answer != "y":
            print("Skipping.")
            return

    seed_events(events)
    print(f"Done — {collection_count()} events now in Qdrant.")


if __name__ == "__main__":
    main()
