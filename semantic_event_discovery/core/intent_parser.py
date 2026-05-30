import os
import json
import re

from core.models import IntentResult, TemporalContext

SYSTEM_PROMPT = """You are an intent parser for a Delhi events and nightlife discovery app.

Given a natural language query, extract structured intent. Return ONLY valid JSON.

Schema:
{
  "temporal_context": {
    "time_of_day": "morning|afternoon|evening|late_night|any",
    "specific_time": "HH:MM or null",
    "day_type": "weekday|weekend|any"
  },
  "social_context": "solo|couple|group|family|any",
  "vibe": ["array of vibe keywords"],
  "implicit_constraints": ["inferred requirements"],
  "rewritten_query": "semantically rich search string capturing full intent",
  "structured_filters": {}
}

Rules:
- "2am", "3am", "after midnight", "late night", "all night" → time_of_day: late_night
- "alone", "by myself", "solo" → social_context: solo
- "date", "romantic", "partner", "girlfriend", "boyfriend" → social_context: couple
- "friends", "group", "crew", "gang" → social_context: group
- "family", "kids", "children" → social_context: family
- "NH7", "Sunburn", "festival", "multi-artist", "live bands" → vibe: [indie, music, festival, live, outdoor]
- "chill", "relax", "slow", "easy", "peaceful" → vibe: [chill, relaxed, laid-back, slow-paced]
- "fun", "party", "dance" → vibe: [fun, energetic, lively]
- For price constraints like "under 1500", add to structured_filters: {"max_price_per_person": 1500}
- rewritten_query must be a rich semantic description of what the user wants (not just the original query)
"""


def _get_groq():
    from groq import Groq
    return Groq(api_key=os.getenv("GROQ_API_KEY", ""))


async def parse_intent(query: str) -> IntentResult:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return _fallback_parse(query)

    try:
        client = _get_groq()
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Parse this query: {query}"},
            ],
            temperature=0.1,
            max_tokens=600,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)

        tc = data.get("temporal_context", {})
        return IntentResult(
            temporal_context=TemporalContext(
                time_of_day=tc.get("time_of_day", "any"),
                specific_time=tc.get("specific_time"),
                day_type=tc.get("day_type", "any"),
            ),
            social_context=data.get("social_context", "any"),
            vibe=data.get("vibe", []),
            implicit_constraints=data.get("implicit_constraints", []),
            rewritten_query=data.get("rewritten_query", query),
            structured_filters=data.get("structured_filters", {}),
            raw_query=query,
        )
    except Exception as e:
        print(f"Intent parsing failed ({e}), using fallback.")
        return _fallback_parse(query)


def _fallback_parse(query: str) -> IntentResult:
    q = query.lower()

    time_of_day = "any"
    specific_time = None
    if any(x in q for x in ["2am", "3am", "4am", "midnight", "late night", "after midnight", "all night"]):
        time_of_day = "late_night"
        if "2am" in q:
            specific_time = "02:00"
        elif "3am" in q:
            specific_time = "03:00"
    elif any(x in q for x in ["night", "evening", "dinner", "tonight", "after 8", "after 9", "after 10"]):
        time_of_day = "evening"
    elif any(x in q for x in ["morning", "sunrise", "breakfast", "brunch", "early"]):
        time_of_day = "morning"
    elif any(x in q for x in ["afternoon", "lunch", "noon"]):
        time_of_day = "afternoon"

    day_type = "any"
    if any(x in q for x in ["sunday", "saturday", "weekend"]):
        day_type = "weekend"
    elif any(x in q for x in ["weekday", "monday", "tuesday", "wednesday", "thursday", "friday"]):
        day_type = "weekday"

    social = "any"
    if any(x in q for x in ["alone", "solo", "by myself", "myself", "single"]):
        social = "solo"
    elif any(x in q for x in ["date", "partner", "couple", "romantic", "girlfriend", "boyfriend"]):
        social = "couple"
    elif any(x in q for x in ["family", "kids", "children", "child"]):
        social = "family"
    elif any(x in q for x in ["friends", "group", "gang", "crew"]):
        social = "group"

    vibe: list[str] = []
    if any(x in q for x in ["fun", "party", "dance"]):
        vibe += ["fun", "energetic"]
    if any(x in q for x in ["chill", "relax", "calm", "peaceful", "slow", "easy"]):
        vibe += ["chill", "relaxed", "laid-back"]
    if any(x in q for x in ["nh7", "indie", "live music", "concert", "festival", "band"]):
        vibe += ["indie", "music", "live", "festival"]
    if any(x in q for x in ["comedy", "laugh", "funny", "standup"]):
        vibe += ["comedy", "humor"]
    if any(x in q for x in ["art", "culture", "museum"]):
        vibe += ["art", "culture"]
    if any(x in q for x in ["food", "eat", "dining", "restaurant"]):
        vibe += ["food", "dining"]

    structured_filters: dict = {}
    price_match = re.search(r"under\s*(?:rs\.?|₹)?\s*(\d+)", q)
    if price_match:
        structured_filters["max_price_per_person"] = int(price_match.group(1))

    # Build a richer rewritten query
    parts = [query]
    if time_of_day != "any":
        parts.append(time_of_day.replace("_", " "))
    if social != "any":
        parts.append(social)
    if vibe:
        parts.extend(vibe[:3])
    parts.append("Delhi")
    rewritten = " ".join(parts)

    return IntentResult(
        temporal_context=TemporalContext(
            time_of_day=time_of_day,
            specific_time=specific_time,
            day_type=day_type,
        ),
        social_context=social,
        vibe=vibe,
        implicit_constraints=[],
        rewritten_query=rewritten,
        structured_filters=structured_filters,
        raw_query=query,
    )
