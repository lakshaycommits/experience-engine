from pydantic import BaseModel
from typing import Optional, List


class RawEvent(BaseModel):
    id: str
    title: str
    venue: str
    area: str
    city: str = "delhi"
    date: str
    time: str
    end_time: Optional[str] = None
    category: str
    subcategory: str = ""
    price_min: int = 0
    price_max: int = 0
    description: str
    age_restriction: Optional[int] = None
    tags: List[str] = []
    organizer: str = ""


class EnrichedEvent(BaseModel):
    id: str
    title: str
    venue: str
    area: str
    city: str
    date: str
    time: str
    end_time: Optional[str]
    category: str
    subcategory: str
    price_min: int
    price_max: int
    description: str
    age_restriction: Optional[int]
    tags: List[str]
    organizer: str
    # LLM-enriched fields
    semantic_description: str
    vibe_tags: List[str]
    time_of_day: List[str]   # morning / afternoon / evening / late_night / all_day
    energy_level: str        # low / medium / high
    social_context: List[str]  # solo_ok / couples / groups / family
    indoor_outdoor: str      # indoor / outdoor / both
    price_tier: str          # free / budget / mid / premium
    semantic_string: str     # full text fed to the embedding model


class EventProfile(EnrichedEvent):
    embedding: List[float] = []


class SearchQuery(BaseModel):
    text: str
    city: str = "delhi"
    limit: int = 10


class TemporalContext(BaseModel):
    time_of_day: str = "any"        # morning/afternoon/evening/late_night/any
    specific_time: Optional[str] = None
    day_type: str = "any"           # weekday/weekend/any


class IntentResult(BaseModel):
    temporal_context: TemporalContext
    social_context: str = "any"     # solo/couple/group/family/any
    vibe: List[str] = []
    implicit_constraints: List[str] = []
    rewritten_query: str
    structured_filters: dict = {}
    raw_query: str


class SearchResultItem(BaseModel):
    id: str
    title: str
    venue: str
    area: str
    date: str
    time: str
    end_time: Optional[str]
    category: str
    price_min: int
    price_max: int
    price_tier: str
    description: str
    vibe_tags: List[str]
    social_context: List[str]
    energy_level: str
    indoor_outdoor: str
    score: float
    match_reason: str


class SearchResponse(BaseModel):
    results: List[SearchResultItem]
    intent_parsed: IntentResult
    total_candidates: int
    query: str
