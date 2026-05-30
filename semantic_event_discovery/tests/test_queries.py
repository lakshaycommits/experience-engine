"""
Demo test suite for Semantic Event Discovery.
Tests the 4 key queries from the implementation spec against live Qdrant.

Run: python -m tests.test_queries
Requires: API stack running (docker-compose up + seeded data)
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from core.models import SearchQuery
from core.search import semantic_search

DEMO_QUERIES = [
    {
        "query": "something fun to do alone at night 2am",
        "description": "Late-night solo plan",
        "expect_time": "late_night",
        "expect_social": "solo",
        "good_result_keywords": ["karaoke", "comedy", "jazz", "gaming", "cycling", "speakeasy", "bar", "night"],
    },
    {
        "query": "first date idea under 1500 rupees",
        "description": "Romantic date on a budget",
        "expect_social": "couple",
        "good_result_keywords": ["pottery", "art", "wine", "cinema", "boat", "candle", "rooftop", "jazz"],
    },
    {
        "query": "like NH7 Weekender but in Delhi",
        "description": "Indie music festival vibe",
        "good_result_keywords": ["indie", "festival", "live", "music", "band", "chai", "ritviz", "train"],
    },
    {
        "query": "chill Sunday morning activity",
        "description": "Relaxed weekend morning plan",
        "expect_time": "morning",
        "good_result_keywords": ["yoga", "market", "bird", "pottery", "brunch", "heritage", "meditation", "sketch"],
    },
]

DIVIDER = "=" * 65


def _check_result(result_title: str, keywords: list[str]) -> bool:
    t = result_title.lower()
    return any(k in t for k in keywords)


async def run_query(q: dict) -> dict:
    print(f"\n{DIVIDER}")
    print(f"Query : {q['query']}")
    print(f"Expect: {q['description']}")
    print(DIVIDER)

    response = await semantic_search(SearchQuery(text=q["query"], limit=5))
    intent = response.intent_parsed

    print(f"\nParsed Intent:")
    print(f"  time_of_day   : {intent.temporal_context.time_of_day}")
    print(f"  social_context: {intent.social_context}")
    print(f"  vibe          : {intent.vibe}")
    print(f"  rewritten     : {intent.rewritten_query}")

    print(f"\nTop {len(response.results)} results (from {response.total_candidates} candidates):\n")

    hits = 0
    for i, r in enumerate(response.results, 1):
        is_good = _check_result(r.title, q.get("good_result_keywords", []))
        marker = "✓" if is_good else "·"
        hits += int(is_good)

        print(f"  {marker} {i}. {r.title}")
        print(f"       📍 {r.venue}, {r.area}")
        print(f"       🕐 {r.time}  |  💰 ₹{r.price_min}–{r.price_max} ({r.price_tier})  |  ⚡ {r.energy_level}")
        print(f"       🏷  {', '.join(r.vibe_tags[:5])}")
        print(f"       ✦  {r.match_reason}")
        print(f"       score: {r.score:.4f}")
        print()

    # Basic assertions
    time_ok = True
    social_ok = True
    if "expect_time" in q:
        time_ok = intent.temporal_context.time_of_day == q["expect_time"]
    if "expect_social" in q:
        social_ok = intent.social_context == q["expect_social"]

    print(f"  Intent time   : {'✓' if time_ok else '✗'} ({intent.temporal_context.time_of_day})")
    print(f"  Intent social : {'✓' if social_ok else '✗'} ({intent.social_context})")
    print(f"  Relevant hits : {hits}/{len(response.results)}")

    return {
        "query": q["query"],
        "time_ok": time_ok,
        "social_ok": social_ok,
        "relevant_hits": hits,
        "total_results": len(response.results),
    }


async def main():
    print("\nSemantic Event Discovery — Demo Test Suite")
    print(DIVIDER)

    results = []
    for q in DEMO_QUERIES:
        r = await run_query(q)
        results.append(r)

    print(f"\n{DIVIDER}")
    print("SUMMARY")
    print(DIVIDER)
    total_hits = sum(r["relevant_hits"] for r in results)
    total_slots = sum(r["total_results"] for r in results)
    intent_ok = sum(int(r["time_ok"] and r["social_ok"]) for r in results)

    for r in results:
        status = "✓" if (r["time_ok"] and r["social_ok"] and r["relevant_hits"] >= 2) else "✗"
        print(f"  {status} {r['query'][:55]:<55}  hits: {r['relevant_hits']}/{r['total_results']}")

    print(f"\n  Intent accuracy : {intent_ok}/{len(results)} queries")
    print(f"  Relevant results: {total_hits}/{total_slots} total slots")
    print()


if __name__ == "__main__":
    asyncio.run(main())
