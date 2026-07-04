from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import astrology
import os

app = FastAPI(title="Astrology API")

class NatalChartRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "UTC"

class CompatibilityRequest(BaseModel):
    chart1: dict
    chart2: dict

class NumerologyRequest(BaseModel):
    name: str
    birth_date: str

class TarotRequest(BaseModel):
    count: int = 3
    question: str = ""

class MuhuratRequest(BaseModel):
    date: str
    city: str = "Delhi"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Astrology API is running"}

@app.post("/api/astrology/natal-chart")
async def get_natal_chart(request: NatalChartRequest):
    try:
        chart = astrology.calculate_natal_chart(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return chart
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/astrology/horoscope/{sign}")
async def get_horoscope(sign: str, date: str = None):
    try:
        target_date = datetime.now().date() if not date else datetime.strptime(date, "%Y-%m-%d").date()
        horoscope = astrology.generate_daily_horoscope(sign, datetime.combine(target_date, datetime.min.time()))
        return horoscope
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/astrology/weekly-horoscope/{sign}")
async def get_weekly_horoscope(sign: str, week_start: str = None):
    try:
        if not week_start:
            week_start = datetime.now().strftime("%Y-%m-%d")
        result = astrology.generate_weekly_horoscope(sign, week_start)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/astrology/monthly-horoscope/{sign}")
async def get_monthly_horoscope(sign: str, year: int = None, month: int = None):
    try:
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        result = astrology.generate_monthly_horoscope(sign, year, month)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/astrology/transits")
async def get_transits(date: str, latitude: float, longitude: float):
    try:
        transits = astrology.calculate_transits(date, latitude, longitude)
        return transits
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/compatibility")
async def get_compatibility(request: CompatibilityRequest):
    try:
        result = astrology.calculate_compatibility(request.chart1, request.chart2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/kundli-matching")
async def get_kundli_matching(request: CompatibilityRequest):
    try:
        result = astrology.calculate_kundli_matching(request.chart1, request.chart2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/numerology")
async def get_numerology(request: NumerologyRequest):
    try:
        result = astrology.calculate_numerology(request.name, request.birth_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/detailed-analysis")
async def get_detailed_analysis(request: NatalChartRequest):
    try:
        chart = astrology.calculate_natal_chart(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        analysis = astrology.generate_detailed_analysis(chart)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/tarot")
async def get_tarot(request: TarotRequest):
    try:
        result = astrology.draw_tarot_cards(request.count, request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/muhurat")
async def get_muhurat(request: MuhuratRequest):
    try:
        result = astrology.calculate_muhurat(request.date, request.city)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# KP Astrology Endpoints

@app.post("/api/astrology/kp-chart")
async def get_kp_chart(request: NatalChartRequest):
    try:
        result = astrology.calculate_kp_chart(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/kp-dasha")
async def get_kp_dasha(request: NatalChartRequest):
    try:
        result = astrology.calculate_vimshottari_dasha(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class HoraryRequest(BaseModel):
    question: str
    question_date: str
    question_time: str
    latitude: float
    longitude: float

@app.post("/api/astrology/kp-horary")
async def get_kp_horary(request: HoraryRequest):
    try:
        result = astrology.calculate_horary_kp(request.question, request.question_date, request.question_time, request.latitude, request.longitude)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Fix numerology calculations

@app.post("/api/ai/chat")
async def ai_chat(request: Request):
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        
        import json
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError as je:
            return {"response": f"JSON parse error: {str(je)}"}
        
        msg = data.get("message", "") if data else ""
        
        if not msg:
            return {"response": "Please provide a message"}
        
        msg_lower = msg.lower()
        
        zodiac_info = {
            "aries": "Aries (March 21 - April 19) is a Fire sign ruled by Mars. They are courageous, energetic, and natural leaders. Lucky color: Red. Lucky day: Tuesday.",
            "taurus": "Taurus (April 20 - May 20) is an Earth sign ruled by Venus. They are patient, reliable, and appreciate luxury. Lucky color: Green. Lucky day: Friday.",
            "gemini": "Gemini (May 21 - June 20) is an Air sign ruled by Mercury. They are adaptable, curious, and excellent communicators. Lucky color: Yellow. Lucky day: Wednesday.",
            "cancer": "Cancer (June 21 - July 22) is a Water sign ruled by Moon. They are nurturing, intuitive, and deeply emotional. Lucky color: White. Lucky day: Monday.",
            "leo": "Leo (July 23 - August 22) is a Fire sign ruled by Sun. They are generous, confident, and born performers. Lucky color: Gold. Lucky day: Sunday.",
            "virgo": "Virgo (August 23 - September 22) is an Earth sign ruled by Mercury. They are analytical, practical, and detail-oriented. Lucky color: Navy blue. Lucky day: Wednesday.",
            "libra": "Libra (September 23 - October 22) is an Air sign ruled by Venus. They are diplomatic, charming, and seek balance. Lucky color: Pink. Lucky day: Friday.",
            "scorpio": "Scorpio (October 23 - November 21) is a Water sign ruled by Pluto. They are passionate, mysterious, and fiercely loyal. Lucky color: Maroon. Lucky day: Tuesday.",
            "sagittarius": "Sagittarius (November 22 - December 21) is a Fire sign ruled by Jupiter. They are adventurous, optimistic, and love freedom. Lucky color: Purple. Lucky day: Thursday.",
            "capricorn": "Capricorn (December 22 - January 19) is an Earth sign ruled by Saturn. They are disciplined, ambitious, and practical. Lucky color: Brown. Lucky day: Saturday.",
            "aquarius": "Aquarius (January 20 - February 18) is an Air sign ruled by Uranus. They are innovative, humanitarian, and independent. Lucky color: Electric blue. Lucky day: Saturday.",
            "pisces": "Pisces (February 19 - March 20) is a Water sign ruled by Neptune. They are compassionate, artistic, and intuitive. Lucky color: Sea green. Lucky day: Thursday."
        }
        
        greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening"]
        if any(g in msg_lower for g in greetings):
            return {"response": "Hello! I'm your astrology assistant. Ask me about zodiac signs, planets, numerology, or tarot cards. For example: 'Tell me about Aries' or 'What is my lucky number?'"}
        
        for sign_name, info in zodiac_info.items():
            if sign_name in msg_lower:
                return {"response": info}
        
        if "numerology" in msg_lower or "lucky number" in msg_lower:
            return {"response": "In Numerology, each number 1-9 has unique traits. Number 1 is leadership, 2 is cooperation, 3 is creativity, 4 is stability, 5 is freedom, 6 is harmony, 7 is spirituality, 8 is abundance, 9 is wisdom. Master numbers 11, 22, 33 carry higher spiritual vibrations."}
        
        if "tarot" in msg_lower:
            return {"response": "Tarot cards offer guidance through symbolism. Major Arcana cards (0-21) represent life's major lessons: The Fool (beginnings), The Magician (manifestation), The High Priestess (intuition), The Empress (abundance), The Emperor (authority). Minor Arcana covers daily matters through Wands, Cups, Swords, and Pentacles."}
        
        if "planet" in msg_lower or "sun" in msg_lower or "moon" in msg_lower or "mercury" in msg_lower or "venus" in msg_lower or "mars" in msg_lower or "jupiter" in msg_lower or "saturn" in msg_lower:
            return {"response": "Planets in astrology: Sun (identity), Moon (emotions), Mercury (communication), Venus (love), Mars (energy), Jupiter (expansion), Saturn (discipline), Uranus (innovation), Neptune (dreams), Pluto (transformation). Their positions in houses and signs shape your birth chart."}
        
        if "horoscope" in msg_lower or "today" in msg_lower:
            return {"response": "For daily horoscopes, use the Horoscope tab. Each sign has unique predictions based on planetary transits. Would you like to know about a particular sign?"}
        
        if "kp" in msg_lower or "sub lord" in msg_lower:
            return {"response": "KP (Krishnamurti Paddhati) astrology uses Nakshatra sub-lords for precise event prediction. Each Nakshatra divides into 9 unequal sub-divisions, ruled by different planets, enabling accurate timing of events. Great for horary (prashna) astrology."}
        
        return {"response": "I can help with astrology, numerology, tarot, and KP astrology! Ask about any zodiac sign, planets, or try the specialized tabs for detailed calculations. Examples: 'Tell me about Virgo', 'Explain numerology', 'How does KP work?'"}
        
    except Exception as e:
        import traceback
        return {"response": f"AI Error: {str(e)}", "trace": traceback.format_exc()}
