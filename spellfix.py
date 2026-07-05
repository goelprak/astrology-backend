import difflib

KNOWN_WORDS = [
    # Career / profession
    "career", "job", "business", "entrepreneur", "startup", "freelance",
    "youtube", "blogger", "vlogger", "influencer", "content",
    "cricket", "cricketer", "sports", "athlete", "football", "tennis",
    "doctor", "engineer", "artist", "teacher", "writer", "actor",
    "lawyer", "pilot", "scientist", "politician", "chef",
    # Life areas
    "love", "marriage", "relationship", "family", "children",
    "health", "wealth", "finance", "money", "education", "study",
    "travel", "foreign", "settlement", "abroad", "immigration",
    "house", "property", "vehicle",
    # Astrology
    "remedy", "remedies", "gemstone", "mantra", "puja", "donation",
    "numerology", "panchang", "manglik",
    "kundli", "matching", "dasha", "mahadasha", "antardasha",
    "prediction", "horoscope", "natal", "chart",
    "karma", "dharma", "spiritual", "meditation", "yoga",
    # General
    "future", "luck", "success", "obstacle", "problem", "solution",
    "timing", "date", "period", "phase", "transition",
]

# Multi-word phrases that should be collapsed into a single keyword
PHRASE_MAP = {
    "you tube": "youtube", "u tube": "youtube",
    "content creator": "content", "content creating": "content",
    "side hustle": "freelance",
    "name correction": "numerology",
    "birth chart": "natal",
    "love marriage": "marriage",
    "foreign settlement": "settlement",
    "foreign travel": "travel",
}


def correct_spelling(text: str, cutoff: float = 0.6) -> str:
    # Apply phrase replacements first
    for phrase, replacement in PHRASE_MAP.items():
        if phrase in text:
            text = text.replace(phrase, replacement)

    words = text.split()
    corrected = []
    for w in words:
        if len(w) <= 2:
            corrected.append(w)
            continue
        matches = difflib.get_close_matches(w, KNOWN_WORDS, n=1, cutoff=cutoff)
        if matches:
            corrected.append(matches[0])
        else:
            corrected.append(w)
    return " ".join(corrected)
