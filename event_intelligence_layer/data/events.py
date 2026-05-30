"""
5 demo events for the Event Intelligence Layer.
Each event has:
  - structured attributes (vibe_tags, dress_code, crowd, accessibility, etc.)
  - knowledge_chunks: text chunks that feed the Q&A knowledge base
"""

DEMO_EVENTS: list[dict] = [
    {
        "id": "eil_001",
        "title": "Prateek Kuhad Acoustic Session",
        "venue": "Siri Fort Auditorium",
        "area": "Siri Fort",
        "date": "Sat, 13 Jun 2026",
        "time": "8:00 PM",
        "end_time": "10:30 PM",
        "price": "₹800 – ₹2,000",
        "category": "Live Music",
        "description": "India's most beloved indie singer-songwriter performs in an intimate acoustic setting. If you haven't cried to 'Cold/Mess' at least once, this will be the night.",
        "image_emoji": "🎸",
        "image_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        # Structured attributes
        "vibe_tags": ["intimate", "acoustic", "romantic", "emotional", "indie"],
        "suitable_for": ["couples", "date night", "first date", "indie fans", "solo"],
        "dress_code": "smart casual",
        "crowd_type": "couples and young professionals (22–35)",
        "arrive_early_mins": 25,
        "metro_accessible": True,
        "metro_info": "Green Park station (15 min walk) or Hauz Khas (10 min auto)",
        "parking": True,
        "parking_info": "Parking available inside Siri Fort complex, Gate 2",
        "age_restriction": "All ages",
        "seated": True,
        "indoor_outdoor": "indoor",
        "duration_hours": 2.5,
        "food_available": True,
        "alcohol_available": False,
        "one_line_pitch": "An intimate acoustic evening that will make you cry — in the best way",
        "suggested_questions": [
            "Is this good for a first date?",
            "What should I wear?",
            "How do I get there by metro?",
            "Is it too loud to talk?",
        ],
        "knowledge_chunks": [
            {
                "chunk_type": "venue_review",
                "source": "Venue reviews",
                "content": "Siri Fort Auditorium is one of Delhi's finest indoor performance venues. The acoustics are exceptional — every seat feels close to the stage. Seating capacity is around 2000 with comfortable cushioned seats, climate control, and excellent sightlines from all rows. The hall is well-maintained and staffed. Toilets are clean and plentiful. There is a small food stall area outside the main hall.",
            },
            {
                "chunk_type": "artist_bio",
                "source": "Artist information",
                "content": "Prateek Kuhad is India's most celebrated indie singer-songwriter, known for introspective, melodic songs in Hindi and English. His hit 'Cold/Mess' has over 100 million streams and has been featured in Barack Obama's annual music playlist. His acoustic shows are deeply intimate — he typically performs with just a guitar, talking between songs, telling stories. His setlist draws from Cold/Mess, Kasoor, Favorite Mistakes, and his album 'The Way That Lovers Do'.",
            },
            {
                "chunk_type": "artist_review",
                "source": "Concert reviews",
                "content": "Prateek Kuhad live is everything the recordings promise. The acoustic format makes every song feel personal. He talks between songs, tells stories, and the 2-2.5 hour set flies by. Audience is predominantly couples and young professionals. The crowd listens quietly and sings along softly — this is not a loud rock show. People in the audience are often visibly emotional during certain songs. It's a beautifully intimate experience.",
            },
            {
                "chunk_type": "practical_info",
                "source": "Event logistics",
                "content": "Doors open 30 minutes before show time (7:30 PM). Arrive 20-25 minutes early to find your seats comfortably. It's a fully seated concert — no standing zone. Photography with phones is allowed but no professional cameras. Metro access: Green Park station is a 15 minute walk or take an auto from Hauz Khas village (10 mins). Parking is available inside the Siri Fort complex at Gate 2 — enter from Khel Gaon Marg. No outside food or beverages allowed inside the auditorium.",
            },
            {
                "chunk_type": "vibe_description",
                "source": "Event profile",
                "content": "This is a concert where the audience often cries. The vibe is intimate, quiet, and emotional. Most attendees are couples treating this as a date night. The acoustic format means the music never overwhelms conversation — during the intervals you can absolutely talk. Dress: smart casual is the norm — most people wear shirts and dresses. The venue is elegant enough for a nice outfit but not so formal that jeans feel wrong.",
            },
            {
                "chunk_type": "faq",
                "source": "FAQ",
                "content": "Is this good for a first date? Yes — it's one of Delhi's best first date options. The music is emotional and beautiful, the seating means you're side by side (not across a table), and the shared experience creates a natural intimacy. Plus the show gives you plenty to talk about after. Is it too loud to talk? No — this is an acoustic set. The music is at a conversational level. You can absolutely lean over and whisper during songs. Is parking available? Yes — Siri Fort Auditorium has parking inside the complex at Gate 2. Age restriction? None — all ages welcome.",
            },
        ],
    },

    {
        "id": "eil_002",
        "title": "Jazz Dinner at Plum by Bent Chair",
        "venue": "Plum by Bent Chair",
        "area": "Janpath",
        "date": "Every Friday & Saturday",
        "time": "8:00 PM",
        "end_time": "11:00 PM",
        "price": "₹1,200 – ₹2,000 per person",
        "category": "Dining Experience",
        "description": "Live jazz trio while you dine on modern Indian cuisine. Candlelit, softly lit room, excellent cocktail list. An elegant dining experience that doesn't require a two-month reservation.",
        "image_emoji": "🎷",
        "image_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "vibe_tags": ["candlelit", "romantic", "jazz", "elegant", "date-night"],
        "suitable_for": ["couples", "first date", "special occasions", "date night"],
        "dress_code": "smart casual to semi-formal (no shorts or slippers)",
        "crowd_type": "mostly couples, professionals on date nights",
        "arrive_early_mins": 10,
        "metro_accessible": False,
        "metro_info": "Rajiv Chowk metro is 20 min walk. Best to take an auto or cab from CP.",
        "parking": True,
        "parking_info": "Street parking on Janpath and nearby Connaught Place parking lots (5 min walk)",
        "age_restriction": "All ages (bar open to 21+)",
        "seated": True,
        "indoor_outdoor": "indoor",
        "duration_hours": 3.0,
        "food_available": True,
        "alcohol_available": True,
        "one_line_pitch": "The closest thing to a jazz club dinner in Paris — in the middle of Delhi",
        "suggested_questions": [
            "What should I wear?",
            "Is this good for a first date?",
            "Do I need a reservation?",
            "How much will it cost for two?",
        ],
        "knowledge_chunks": [
            {
                "chunk_type": "venue_review",
                "source": "Venue reviews",
                "content": "Plum by Bent Chair on Janpath is a mid-century modern restaurant with warm amber lighting and about 60 seats. Tables are intimate without being cramped. The lighting dims noticeably after 9:30 PM creating a genuinely romantic atmosphere. The décor is warm — leather seats, brass fixtures, soft music. The room is air-conditioned and comfortable even in summer.",
            },
            {
                "chunk_type": "artist_bio",
                "source": "Artist information",
                "content": "The house jazz trio at Plum features musicians from Delhi's conservatory circuit. They play standards (Miles Davis, Coltrane, Bill Evans), Brazilian bossa nova, and original compositions. The violinist has performed at Jazz India Circuit multiple times. The music starts at 9 PM and runs until 11 PM with a short break. Volume is low enough for easy conversation across the table.",
            },
            {
                "chunk_type": "practical_info",
                "source": "Event logistics",
                "content": "Reservations are strongly recommended on weekends — walk-ins are accepted but you may wait 20-30 minutes. The venue is not metro-accessible easily (Rajiv Chowk is a 20 minute walk). Best to take an auto or cab. Uber/Ola drops at the door. Street parking is available on Janpath and Connaught Place lots are a 5 minute walk. Dress code: smart casual minimum — no shorts, no slippers. Most guests wear shirts/kurtas and dresses. The dinner is designed as a 2.5-3 hour experience — not a quick meal.",
            },
            {
                "chunk_type": "vibe_description",
                "source": "Event profile",
                "content": "Most tables at Plum on Friday and Saturday evenings are couples on date nights. The atmosphere is romantic but not over-the-top — this is elegant dining, not a Valentine's Day gimmick. The jazz is live and beautiful but at a volume where you barely notice it's live until you look up. Average spend is ₹1,500-2,000 per person including one or two cocktails. Vegetarian options are excellent on the menu.",
            },
            {
                "chunk_type": "faq",
                "source": "FAQ",
                "content": "Is this good for a first date? It's one of the best first date options in Delhi. A candlelit jazz dinner gives you something to talk about (the music, the food) and creates a naturally romantic setting without being cheesy. How much does it cost for two? Budget ₹3,000-4,000 for two people including two drinks each. What should I wear? Smart casual at minimum — most guests wear shirts and dresses. No shorts. Do I need a reservation? Yes, especially on weekends. Call ahead or book on Dineout. Is there live music every night? Only Friday and Saturday evenings. The jazz trio starts at 9 PM.",
            },
            {
                "chunk_type": "menu_info",
                "source": "Restaurant information",
                "content": "Plum by Bent Chair serves modern Indian cuisine with a European technique. The menu rotates seasonally. Signature dishes include the burrata chaat and the lamb rogan josh ravioli. Cocktail list is extensive and well-curated — the Delhi Mule and the Gulab Martini are popular. Mocktails available. Full vegetarian menu available.",
            },
        ],
    },

    {
        "id": "eil_003",
        "title": "When Chai Met Toast — Live in Delhi",
        "venue": "Jawaharlal Nehru Stadium",
        "area": "Pragati Vihar",
        "date": "Sat, 7 Jun 2026",
        "time": "7:00 PM",
        "end_time": "10:30 PM",
        "price": "₹999 – ₹2,500",
        "category": "Indie Concert",
        "description": "South India's biggest indie folk act brings their joyful, layered sound to Delhi. Expect singalongs, feel-good energy, and the kind of communal concert experience NH7 is famous for.",
        "image_emoji": "🎵",
        "image_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "vibe_tags": ["festival-vibe", "joyful", "singalong", "high-energy", "feel-good"],
        "suitable_for": ["groups of friends", "couples", "solo concert-goers", "first-time concert"],
        "dress_code": "casual (comfortable shoes essential — standing venue)",
        "crowd_type": "indie music crowd, 18–35, groups and couples",
        "arrive_early_mins": 45,
        "metro_accessible": True,
        "metro_info": "JLN Stadium metro station (Violet Line) — 10 min walk to venue",
        "parking": False,
        "parking_info": "No dedicated parking. Use metro or cab drop-off on Bhishma Pitamah Marg.",
        "age_restriction": "All ages",
        "seated": False,
        "indoor_outdoor": "outdoor",
        "duration_hours": 3.5,
        "food_available": True,
        "alcohol_available": True,
        "one_line_pitch": "Every song becomes a singalong — this is what joy sounds like live",
        "suggested_questions": [
            "How early should I arrive for a good spot?",
            "Is the artist actually good live?",
            "What should I wear?",
            "Is there parking available?",
        ],
        "knowledge_chunks": [
            {
                "chunk_type": "venue_review",
                "source": "Venue reviews",
                "content": "JN Stadium outdoor grounds can hold up to 15,000 people for music events. The outdoor plaza area is used for concerts — flat ground with a raised stage. No seating for most ticket tiers (GA standing). Sound quality is consistently good at this venue with a proper PA system. Multiple food stalls are set up inside — expect biryani, pizza, beer counters. Basic but clean toilets. Security check at entry takes about 10-15 minutes if you arrive close to show time.",
            },
            {
                "chunk_type": "artist_bio",
                "source": "Artist information",
                "content": "When Chai Met Toast is a Bangalore-based indie folk quartet known for layered harmonies and joyful, communal music. Their songs are in English and Malayalam. Known for 'Firefly', 'Moana', 'Almost Home', and 'Khidki'. They've headlined NH7 Weekender four times. The band's energy live is famously infectious — they're known for making audiences feel like they've known each other for years.",
            },
            {
                "chunk_type": "artist_review",
                "source": "Concert reviews",
                "content": "When Chai Met Toast live is the closest thing to a communal celebration you'll find at a concert. The entire crowd sings along from the first song. Strangers talk to each other between songs. The band jokes with the audience, takes requests, and plays encore after encore. Expect to be on your feet for all 2.5 hours. They typically start with Khidki or Firefly and save Moana for the encore. The energy doesn't drop for a single song.",
            },
            {
                "chunk_type": "practical_info",
                "source": "Event logistics",
                "content": "Arrive 45 minutes early to clear security and get a good standing position near the stage. Security checks can cause long queues if you arrive at 7 PM sharp. It's an outdoor standing venue — wear comfortable shoes, not heels. Metro: JLN Stadium station (Violet Line) is a 10 minute walk. No dedicated parking at the venue — use metro or cab drop on Bhishma Pitamah Marg. Security does not allow outside food or drinks — cans, bottles, and outside alcohol are confiscated. There are food and beer counters inside.",
            },
            {
                "chunk_type": "vibe_description",
                "source": "Event profile",
                "content": "This concert has the energy of NH7 Weekender's main stage — joyful, communal, and high-energy. The crowd is 18-35, mostly groups of friends and couples. Solo attendees are completely comfortable here — you'll be singing with strangers within the first song. Not suitable for those with hearing sensitivity — it's loud. Wear layers if you're attending in June as Delhi evenings can be warm early and cooler later.",
            },
            {
                "chunk_type": "faq",
                "source": "FAQ",
                "content": "How early should I arrive? 45 minutes before doors open. The queues at security are long closer to show time and good spots near the stage fill up fast. Is it good for a first date? Yes but only if your date loves live music — it's loud and standing, not intimate. Great for groups. Is parking available? No dedicated parking. Take the metro (JLN Stadium station) or drop by cab. What to wear? Casual and comfortable — this is an outdoor standing venue. No heels. Light jacket recommended for later in the evening.",
            },
        ],
    },

    {
        "id": "eil_004",
        "title": "Peter Cat Recording Co. at Summer House",
        "venue": "Summer House Café",
        "area": "Anand Lok",
        "date": "Fri, 30 May 2026",
        "time": "9:00 PM",
        "end_time": "12:00 AM",
        "price": "₹800 – ₹1,200",
        "category": "Indie / Art Rock",
        "description": "Delhi's most artistically interesting band plays their intimate home venue. Peter Cat's music is psychedelic, layered, and unlike anything you've heard. Underground Delhi indie at its finest.",
        "image_emoji": "🌀",
        "image_gradient": "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
        "vibe_tags": ["underground", "psychedelic", "intimate", "art-rock", "late-night"],
        "suitable_for": ["indie music enthusiasts", "music heads", "curious first-timers"],
        "dress_code": "casual to artsy — anything goes",
        "crowd_type": "Delhi indie music community, 21–35, music enthusiasts",
        "arrive_early_mins": 30,
        "metro_accessible": True,
        "metro_info": "Panchsheel Park station (Yellow Line) — 5 min auto to venue",
        "parking": False,
        "parking_info": "Limited street parking on Aurobindo Marg. Most people take metro.",
        "age_restriction": "21+ (strictly enforced at Summer House)",
        "seated": False,
        "indoor_outdoor": "indoor",
        "duration_hours": 3.0,
        "food_available": True,
        "alcohol_available": True,
        "one_line_pitch": "The most interesting band in Delhi, in the room they built their sound",
        "suggested_questions": [
            "Is the artist actually good live?",
            "What kind of music is it — will I enjoy it as a first-timer?",
            "How crowded does it get?",
            "What's the age restriction?",
        ],
        "knowledge_chunks": [
            {
                "chunk_type": "venue_review",
                "source": "Venue reviews",
                "content": "Summer House Café in Anand Lok is Delhi's best small music venue. Capacity is 200 people. The venue splits between an indoor stage area and an outdoor terrace. Standing only for concerts. The sound system is exceptional for the size — every instrument is distinct and clear. The bar is well-stocked and service is fast. The indoor area can get warm when full, the terrace provides relief. Age 21+ strictly enforced — carry ID.",
            },
            {
                "chunk_type": "artist_bio",
                "source": "Artist information",
                "content": "Peter Cat Recording Co. (PCRC) is Delhi's most critically acclaimed band, led by Suryakant Sawhney. Their sound blends psychedelic rock, jazz, art-pop, and Hindi-Urdu poetry — something completely original. Their album 'Bismillah' is considered a landmark of Indian indie music. They've performed at SXSW, toured Europe, and been reviewed in Pitchfork. Summer House is their home venue — they've played here over 50 times.",
            },
            {
                "chunk_type": "artist_review",
                "source": "Concert reviews",
                "content": "Peter Cat Recording Co. live at Summer House is a transcendent experience for those who get their music. The sound is layered, textured, and unhurried — they don't play to the cheap seats. The crowd knows every word of every song, which creates a special atmosphere. They typically play 2-2.5 hours with no support act. The lighting is minimal and moody. First-timers often describe it as 'not what I expected but I couldn't stop listening'. They are genuinely exceptional live — better than the recordings.",
            },
            {
                "chunk_type": "practical_info",
                "source": "Event logistics",
                "content": "Age 21+ strictly enforced at Summer House — no exceptions. Carry government ID. Doors open at 9 PM, set starts around 9:30-10 PM. Sold-out shows are common for PCRC — book tickets in advance. Metro: Panchsheel Park station (Yellow Line) then 5 minute auto to Anand Lok. Limited parking on Aurobindo Marg. The venue is indoors and can get warm — dress accordingly. Bar is inside and well-stocked.",
            },
            {
                "chunk_type": "vibe_description",
                "source": "Event profile",
                "content": "The crowd at PCRC shows is Delhi's indie music community — the people who know every show, every album, every b-side. First-timers are absolutely welcome and often become converts. The vibe is art-focused and music-first — this is not a night where people talk through the set. It's the kind of show you remember for years. The psychedelic, slow-build nature of their music means it rewards attention.",
            },
            {
                "chunk_type": "faq",
                "source": "FAQ",
                "content": "Will I enjoy it as a first-timer? If you're open to music that takes time to reveal itself — absolutely. PCRC is not instant-gratification pop. Give it 20 minutes and you'll either be hooked or not. Is it too underground for a casual listener? Their music has wide appeal if you're patient. Think Radiohead meets Urdu poetry meets jazz. How crowded does it get? Very — 200-person capacity and usually sold out. What's the age restriction? 21+ strictly enforced. Bring government ID or you won't get in. Is it good for a first date? Yes, for the right kind of date — someone open to interesting music experiences.",
            },
        ],
    },

    {
        "id": "eil_005",
        "title": "Delhi Midnight Cycling Tour",
        "venue": "India Gate Lawns",
        "area": "India Gate",
        "date": "Every Saturday Night",
        "time": "11:30 PM",
        "end_time": "3:00 AM",
        "price": "₹500 (cycle included)",
        "category": "Outdoor Experience",
        "description": "Cycle through Delhi's monuments at midnight — India Gate, Rashtrapati Bhawan, Connaught Place. The city looks completely different at 2 AM. Bikes and helmets provided.",
        "image_emoji": "🚲",
        "image_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "vibe_tags": ["midnight", "outdoor", "adventure", "monuments", "unique", "peaceful"],
        "suitable_for": ["solo riders", "couples", "groups", "anyone curious about Delhi at night"],
        "dress_code": "casual and comfortable — light jacket recommended",
        "crowd_type": "curious solo riders (60%), small groups and couples",
        "arrive_early_mins": 15,
        "metro_accessible": True,
        "metro_info": "Central Secretariat station (Yellow/Violet Line) — 10 min walk to India Gate Gate 3",
        "parking": True,
        "parking_info": "India Gate lawns have designated parking. Easy and free after 10 PM.",
        "age_restriction": "No age restriction (16+ recommended)",
        "seated": False,
        "indoor_outdoor": "outdoor",
        "duration_hours": 3.5,
        "food_available": False,
        "alcohol_available": False,
        "one_line_pitch": "Delhi after midnight on a cycle — you'll never see your city the same way again",
        "suggested_questions": [
            "Is parking available near India Gate?",
            "Do I need to know how to cycle well?",
            "Is it safe at midnight?",
            "What should I bring?",
        ],
        "knowledge_chunks": [
            {
                "chunk_type": "venue_review",
                "source": "Route information",
                "content": "The midnight cycling tour route covers approximately 15km on flat roads: India Gate → Rajpath (now Kartavya Path) → Rashtrapati Bhawan → Parliament House → Connaught Place inner circle → back to India Gate. The roads are completely empty after midnight — no traffic, no auto-rickshaws. All roads on the route are well-lit, smooth, and have police presence (Rajpath especially). The monuments are lit up with floodlights and look extraordinary at night.",
            },
            {
                "chunk_type": "practical_info",
                "source": "Event logistics",
                "content": "Meet at India Gate Lawns, Gate 3 (Kartavya Path side) at 11:15 PM. Cycles are provided — hybrid city bikes, well-maintained with working lights and gears. Helmets are mandatory and provided. Group size is 15-20 people with 2 guides. Metro: Central Secretariat station is a 10 minute walk to India Gate. Parking is available at India Gate lawns — free and easy after 10 PM. No outside food inside but you can bring a water bottle. The tour operates rain or shine unless there's heavy rain — check the organiser's WhatsApp group (link sent after booking) for weather updates.",
            },
            {
                "chunk_type": "safety_info",
                "source": "Safety information",
                "content": "The route is safe — India Gate to Connaught Place is one of the most secure and well-patrolled areas in Delhi. Police is consistently present on Kartavya Path. The tour operates in a group with guides. Female solo riders regularly attend and find it completely safe. Delhi's monuments area has CCTV and is regularly patrolled by Central and Delhi Police. The roads are empty of traffic after midnight which is actually what makes it peaceful and safe to cycle.",
            },
            {
                "chunk_type": "fitness_info",
                "source": "Participant information",
                "content": "Fitness level required: moderate. The route is 15km on completely flat roads with no hills. Most adults who can cycle comfortably can complete it. You don't need to be a regular cyclist — the pace is leisurely with multiple stops for photography and explanation. Ages 16 to 60+ regularly attend. The tour takes about 3 hours with stops. Bring water (at least 500ml), a light jacket (Delhi nights can be cool even in summer), and your phone for photos.",
            },
            {
                "chunk_type": "vibe_description",
                "source": "Event profile",
                "content": "Delhi at midnight is a completely different city. The chaos, traffic, and noise of the day is gone — you're left with wide, empty boulevards, lit-up monuments, and silence. Solo riders make up about 60% of participants. The group is always friendly and conversations happen naturally during stops. This is the kind of experience you tell people about for years.",
            },
            {
                "chunk_type": "faq",
                "source": "FAQ",
                "content": "Is parking available near India Gate? Yes — India Gate lawns have designated parking areas that are free and easy to use after 10 PM. Is it safe at midnight? Yes — the route covers some of Delhi's most patrolled roads (Kartavya Path, around Parliament). Police presence is high in this area. Female solo riders regularly attend. Do I need to cycle well? You need to be able to ride a bicycle — no special skill beyond that. The pace is leisurely. What should I bring? Water bottle, light jacket, phone for photos, comfortable closed shoes. Cycles and helmets are provided.",
            },
        ],
    },
]


def get_all_events() -> list[dict]:
    return DEMO_EVENTS


def get_event_by_id(event_id: str) -> dict | None:
    return next((e for e in DEMO_EVENTS if e["id"] == event_id), None)


def get_all_knowledge_chunks() -> list[dict]:
    chunks = []
    for event in DEMO_EVENTS:
        for chunk in event.get("knowledge_chunks", []):
            chunks.append({**chunk, "event_id": event["id"]})
    return chunks
