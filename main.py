from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import spellfix
import astrology
import translations
import os

app = FastAPI(title="Astrology API")

class PanchangRequest(BaseModel):
    date: str
    latitude: float = 28.6139
    longitude: float = 77.209

class WealthRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    language: str = "en"

class ForeignSettlementRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    language: str = "en"

class ManglikRequest(BaseModel):
    chart1: dict
    chart2: dict = None
    language: str = "en"

class NavamsaRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    language: str = "en"

class NameCorrectionRequest(BaseModel):
    name: str
    birth_date: str = ""
    language: str = "en"

class RemediesRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    language: str = "en"

class LifeTimelineRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    language: str = "en"

class PdfReportRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"
    language: str = "en"

class NatalChartRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "UTC"
    language: str = "en"

class CompatibilityRequest(BaseModel):
    chart1: dict
    chart2: dict
    language: str = "en"

class NumerologyRequest(BaseModel):
    name: str
    birth_date: str
    language: str = "en"

class TarotRequest(BaseModel):
    count: int = 3
    question: str = ""
    language: str = "en"

class MuhuratRequest(BaseModel):
    date: str
    city: str = "Delhi"
    language: str = "en"

class YearlyPredictionRequest(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str = "UTC"
    years: int = 10
    language: str = "en"

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

@app.post("/api/astrology/yearly-predictions")
async def get_yearly_predictions(request: YearlyPredictionRequest):
    try:
        result = astrology.generate_yearly_predictions(
            request.birth_date, request.birth_time,
            request.latitude, request.longitude,
            request.timezone, request.years
        )
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

@app.post("/api/astrology/panchang")
async def get_panchang(request: PanchangRequest):
    try:
        result = astrology.calculate_panchang(request.date, request.latitude, request.longitude)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/wealth-prediction")
async def get_wealth_prediction(request: WealthRequest):
    try:
        result = astrology.calculate_wealth_prediction(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/foreign-settlement")
async def get_foreign_settlement(request: ForeignSettlementRequest):
    try:
        result = astrology.calculate_foreign_settlement(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/check-manglik")
async def get_manglik(request: ManglikRequest):
    try:
        result = astrology.check_manglik(request.chart1)
        if request.chart2:
            result2 = astrology.check_manglik(request.chart2)
            result["chart2"] = result2
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/navamsa-chart")
async def get_navamsa_chart(request: NavamsaRequest):
    try:
        result = astrology.calculate_navamsa_chart(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/name-correction")
async def get_name_correction(request: NameCorrectionRequest):
    try:
        result = astrology.calculate_name_correction(request.name, request.birth_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/remedies-detailed")
async def get_remedies_detailed(request: RemediesRequest):
    try:
        chart = astrology.calculate_natal_chart(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        result = astrology.calculate_remedies(chart)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/life-timeline")
async def get_life_timeline(request: LifeTimelineRequest):
    try:
        result = astrology.calculate_life_timeline(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/astrology/pdf-report")
async def get_pdf_report(request: PdfReportRequest):
    try:
        result = astrology.generate_pdf_report(request.birth_date, request.birth_time, request.latitude, request.longitude, request.timezone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Fix numerology calculations

zodiac_info = {
    "aries": "Aries (March 21 - April 19) is the first Fire sign, ruled by Mars, and is a Cardinal sign initiating the zodiac. Aries natives are natural-born leaders with immense courage, pioneering spirit, and boundless energy. They are impulsive, competitive, and thrive on challenges. Strengths include bravery, confidence, optimism, and enthusiasm. Weaknesses include impatience, short temper, aggressiveness, and a tendency to be self-centered. In career, Aries excels in leadership roles, entrepreneurship, sports, military, police, firefighting, surgery, and any field requiring quick decisions and action. Health-wise, they are prone to headaches, migraines, sinus issues, injuries from accidents, and high blood pressure. In love and relationships, Aries is passionate, direct, and highly romantic. They enjoy the chase and need a partner who can match their energy and independence. They are most compatible with Leo, Sagittarius, Gemini, and Aquarius. Challenging matches include Cancer and Capricorn. Lucky Color: Red. Lucky Day: Tuesday. Lucky Numbers: 1, 9. Lucky Stone: Red Coral. Famous Aries: Leonardo da Vinci, Thomas Jefferson, Charlie Chaplin, Mariah Carey, Robert Downey Jr.",
    "taurus": "Taurus (April 20 - May 20) is the first Earth sign, ruled by Venus, a Fixed sign known for stability and determination. Taurus natives are patient, reliable, practical, and deeply grounded. They love luxury, comfort, and sensual pleasures. Once they commit, they are loyal for life. Strengths include dependability, persistence, artistic talent, practicality, and a strong work ethic. Weaknesses include stubbornness, possessiveness, laziness when comfortable, and resistance to change. In career, Taurus thrives in finance, banking, accounting, real estate, art, music, culinary arts, fashion, and agriculture. Health-wise, they are prone to throat issues, thyroid problems, neck tension, and weight gain. In love, Taurus is deeply loyal, sensual, and values stability above all. They express love through physical affection, quality time, and providing material comfort. They are most compatible with Virgo, Capricorn, Cancer, and Pisces. Challenging matches include Leo and Aquarius. Lucky Color: Green. Lucky Day: Friday. Lucky Numbers: 2, 6. Lucky Stone: Diamond or Emerald. Famous Taurus: William Shakespeare, Sigmund Freud, Audrey Hepburn, Adele, Dwayne Johnson.",
    "gemini": "Gemini (May 21 - June 20) is the first Air sign, ruled by Mercury, a Mutable sign known for adaptability and intellect. Gemini natives are curious, witty, versatile, and excellent communicators. Strengths include intelligence, adaptability, quick wit, sociability, and eloquence. Weaknesses include inconsistency, indecisiveness, restlessness, nervousness, and a tendency to be superficial or gossipy. In career, Gemini excels in writing, journalism, teaching, sales, marketing, technology, programming, public relations, and any field requiring communication and mental agility. Health-wise, they are prone to lung issues, respiratory problems, anxiety, nervous disorders, and carpal tunnel syndrome. In love, Gemini needs intellectual stimulation and variety. They are flirtatious and charming but can be commitment-phobic until they find someone who keeps their mind engaged. They are most compatible with Libra, Aquarius, Aries, and Leo. Challenging matches include Virgo and Pisces. Lucky Color: Yellow. Lucky Day: Wednesday. Lucky Numbers: 3, 5. Lucky Stone: Emerald. Famous Gemini: John F. Kennedy, Bob Dylan, Angelina Jolie, Kanye West, Marilyn Monroe.",
    "cancer": "Cancer (June 21 - July 22) is the first Water sign, ruled by the Moon, a Cardinal sign known for nurturing and emotional depth. Cancer natives are deeply intuitive, emotional, nurturing, and protective of their loved ones. They have a strong connection to home, family, and the past. Strengths include tenacity, imagination, loyalty, empathy, and psychic sensitivity. Weaknesses include moodiness, pessimism, clinginess, over-sensitivity, and difficulty letting go of the past. In career, Cancer excels in nursing, counseling, social work, real estate, culinary arts, hospitality, childcare, history, and marine sciences. Health-wise, they are prone to digestive issues, stomach ulcers, water retention, mood swings, and depression. Emotional health directly affects their physical well-being. In love, Cancer is deeply emotional, romantic, and seeks security. They are devoted partners who nurture their relationships intensely. They are most compatible with Scorpio, Pisces, Taurus, and Virgo. Challenging matches include Aries and Libra. Lucky Color: Silver or White. Lucky Day: Monday. Lucky Numbers: 2, 7. Lucky Stone: Pearl. Famous Cancer: Princess Diana, Nelson Mandela, Tom Cruise, Meryl Streep, Elon Musk.",
    "leo": "Leo (July 23 - August 22) is a Fire sign ruled by the Sun, a Fixed sign known for confidence and leadership. Leo natives are confident, generous, dramatic, and natural performers who love to be in the spotlight. They have a warm heart and a regal presence. Strengths include creativity, passion, generosity, warm-heartedness, loyalty, and natural leadership. Weaknesses include arrogance, stubbornness, self-centeredness, laziness when not appreciated, and a need for constant admiration. In career, Leo excels in entertainment, acting, management, politics, design, fashion, luxury goods, event planning, and any role where they can shine and inspire others. Health-wise, they are prone to heart issues, back pain, spinal problems, and circulation issues. In love, Leo is romantic, passionate, and extremely generous. They love grand gestures and need a partner who admires them and gives them attention. They are most compatible with Aries, Sagittarius, Gemini, and Libra. Challenging matches include Taurus and Scorpio. Lucky Color: Gold or Orange. Lucky Day: Sunday. Lucky Numbers: 1, 4. Lucky Stone: Ruby. Famous Leo: Napoleon Bonaparte, Barack Obama, Madonna, Jennifer Lopez, Chris Hemsworth.",
    "virgo": "Virgo (August 23 - September 22) is an Earth sign ruled by Mercury, a Mutable sign known for analysis and service. Virgo natives are analytical, practical, meticulous, and have an eye for detail that is unmatched. They are perfectionists who strive for excellence in everything. Strengths include modesty, reliability, hard work, intelligence, analytical thinking, and a helpful nature. Weaknesses include being overly critical (of self and others), perfectionism that leads to paralysis, worry, shyness, and difficulty relaxing. In career, Virgo excels in healthcare (doctor, nurse, researcher), science, accounting, editing, data analysis, nutrition, fitness, teaching, and any role requiring precision and organization. Health-wise, they are prone to digestive issues, food sensitivities, anxiety, stress-related disorders, and hypochondria. In love, Virgo shows love through acts of service and practical help. They are devoted partners who notice every detail. They are most compatible with Taurus, Capricorn, Cancer, and Scorpio. Challenging matches include Gemini and Sagittarius. Lucky Color: Navy Blue or Green. Lucky Day: Wednesday. Lucky Numbers: 5, 8. Lucky Stone: Sapphire. Famous Virgo: Mother Teresa, Beyonce, Freddie Mercury, Keanu Reeves, Zendaya.",
    "libra": "Libra (September 23 - October 22) is an Air sign ruled by Venus, a Cardinal sign known for balance and harmony. Libra natives are diplomatic, charming, sociable, and have a natural sense of justice and fairness. They are the peacemakers of the zodiac. Strengths include cooperation, graciousness, fair-mindedness, artistic taste, diplomacy, and social grace. Weaknesses include indecisiveness, avoidance of confrontation, self-pity, a tendency to be superficial, and people-pleasing. In career, Libra excels in law, diplomacy, counseling, design, fashion, beauty, art, music, public relations, and any role requiring negotiation and social skills. Health-wise, they are prone to kidney issues, skin problems, lower back pain, and hormonal imbalances. In love, Libra is the ultimate romantic. They seek balanced, harmonious partnerships and thrive when in a relationship. They are charming, affectionate partners who value intellectual connection and aesthetic beauty. They are most compatible with Gemini, Aquarius, Leo, and Sagittarius. Challenging matches include Cancer and Capricorn. Lucky Color: Pink or Light Blue. Lucky Day: Friday. Lucky Numbers: 6, 9. Lucky Stone: Opal. Famous Libra: Mahatma Gandhi, John Lennon, Serena Williams, Kim Kardashian, Will Smith.",
    "scorpio": "Scorpio (October 23 - November 21) is a Water sign ruled by Pluto (and traditionally Mars), a Fixed sign known for intensity and transformation. Scorpio natives are passionate, mysterious, determined, and possess incredible emotional depth. They are the most intense and transformative sign of the zodiac. Strengths include bravery, loyalty, resourcefulness, passion, determination, and psychic intuition. Weaknesses include jealousy, secretiveness, manipulative tendencies, possessiveness, and a tendency toward vengeance. In career, Scorpio excels in investigation, detective work, psychology, therapy, research, science, surgery, finance, and any role requiring depth and strategic thinking. Health-wise, they are prone to reproductive issues, bladder problems, toxins accumulation, and stress-related disorders. In love, Scorpio loves with total intensity. They seek deep, transformative, soul-level connections. They are fiercely loyal but require complete trust and honesty. They are most compatible with Cancer, Pisces, Virgo, and Capricorn. Challenging matches include Leo and Aquarius. Lucky Color: Maroon or Black. Lucky Day: Tuesday. Lucky Numbers: 8, 11. Lucky Stone: Topaz. Famous Scorpio: Marie Curie, Pablo Picasso, Julia Roberts, Leonardo DiCaprio, Bill Gates.",
    "sagittarius": "Sagittarius (November 22 - December 21) is a Fire sign ruled by Jupiter, a Mutable sign known for adventure and philosophy. Sagittarius natives are adventurous, optimistic, honest, and love freedom above all. They are the explorers and philosophers of the zodiac, always seeking higher meaning. Strengths include generosity, idealism, humor, open-mindedness, honesty, and a great sense of adventure. Weaknesses include impatience, tactlessness, restlessness, over-promising, and commitment issues. In career, Sagittarius excels in travel, tourism, education, publishing, sports, law, philosophy, international business, and any field allowing freedom and exploration. Health-wise, they are prone to hip issues, sciatica, over-exertion injuries, liver problems, and weight gain from overindulgence. In love, Sagittarius needs a partner who shares their love for adventure, travel, and intellectual exploration. They are honest to a fault and value freedom in relationships. They are most compatible with Aries, Leo, Gemini, and Aquarius. Challenging matches include Virgo and Pisces. Lucky Color: Purple or Royal Blue. Lucky Day: Thursday. Lucky Numbers: 3, 7. Lucky Stone: Turquoise. Famous Sagittarius: Winston Churchill, Walt Disney, Taylor Swift, Brad Pitt, Mark Twain.",
    "capricorn": "Capricorn (December 22 - January 19) is an Earth sign ruled by Saturn, a Cardinal sign known for discipline and ambition. Capricorn natives are disciplined, ambitious, practical, and responsible. They are the builders and achievers of the zodiac, climbing steadily toward their goals. Strengths include patience, hard work, self-control, wisdom, responsibility, and strategic thinking. Weaknesses include pessimism, rigidity, unforgiving nature, workaholism, and emotional reserve. In career, Capricorn excels in business, finance, banking, engineering, management, law, politics, real estate, and any field requiring long-term planning and discipline. Health-wise, they are prone to knee issues, bone problems, joint pain, dental issues, and stress-related conditions. In love, Capricorn is serious and cautious about relationships. They take time to open up but are deeply loyal once committed. They show love through providing security and stability. They are most compatible with Taurus, Virgo, Cancer, and Scorpio. Challenging matches include Aries and Libra. Lucky Color: Brown or Dark Green. Lucky Day: Saturday. Lucky Numbers: 4, 8. Lucky Stone: Garnet. Famous Capricorn: Isaac Newton, Martin Luther King Jr., Michelle Obama, Denzel Washington, Kate Middleton.",
    "aquarius": "Aquarius (January 20 - February 18) is an Air sign ruled by Uranus, a Fixed sign known for innovation and humanitarianism. Aquarius natives are innovative, independent, humanitarian, and eccentric. They think outside the box and are often ahead of their time. Strengths include progressiveness, originality, friendliness, idealism, intellectual brilliance, and strong social conscience. Weaknesses include emotional detachment, unpredictability, rebelliousness, stubbornness, and difficulty with intimacy. In career, Aquarius excels in technology, science, engineering, aviation, social work, activism, astrology, inventing, and any field that allows them to innovate and help humanity. Health-wise, they are prone to circulation issues, ankle problems, varicose veins, and nerve disorders. In love, Aquarius needs intellectual connection and unconventional relationships. They value friendship as the foundation of love. They need a partner who respects their independence and shares their vision for the future. They are most compatible with Gemini, Libra, Aries, and Sagittarius. Challenging matches include Taurus and Scorpio. Lucky Color: Electric Blue or Silver. Lucky Day: Saturday. Lucky Numbers: 4, 11. Lucky Stone: Amethyst. Famous Aquarius: Thomas Edison, Abraham Lincoln, Oprah Winfrey, Cristiano Ronaldo, Bob Marley.",
    "pisces": "Pisces (February 19 - March 20) is a Water sign ruled by Neptune, a Mutable sign known for compassion and creativity. Pisces natives are compassionate, artistic, intuitive, and deeply spiritual. They are the dreamers and mystics of the zodiac, with a profound connection to the unseen. Strengths include imagination, compassion, selflessness, musical talent, intuition, and adaptability. Weaknesses include escapist tendencies, being overly trusting, melancholia, addictive tendencies, and difficulty with boundaries. In career, Pisces excels in art, music, dance, film, photography, healing, spirituality, social work, nursing, marine biology, and any field requiring creativity and empathy. Health-wise, they are prone to foot issues, sleep disorders, allergies, addictions, and psychosomatic conditions. In love, Pisces is the ultimate romantic dreamer. They seek soulmate connections and unconditional love. They are incredibly giving and intuitive partners who can sense their partner's needs. They are most compatible with Cancer, Scorpio, Taurus, and Capricorn. Challenging matches include Gemini and Sagittarius. Lucky Color: Sea Green or Mauve. Lucky Day: Thursday. Lucky Numbers: 3, 7. Lucky Stone: Jade or Moonstone. Famous Pisces: Albert Einstein, Steve Jobs, Rihanna, Kurt Cobain, Elizabeth Taylor."
}

aliases = {
    "aries": "aries", "mesh": "aries", "ram": "aries",
    "taurus": "taurus", "vrish": "taurus", "bull": "taurus",
    "gemini": "gemini", "mithun": "gemini", "twins": "gemini",
    "cancer": "cancer", "kark": "cancer", "crab": "cancer",
    "leo": "leo", "simha": "leo", "lion": "leo",
    "virgo": "virgo", "kanya": "virgo", "virgin": "virgo",
    "libra": "libra", "tula": "libra", "scales": "libra",
    "scorpio": "scorpio", "vrishchik": "scorpio", "scorpion": "scorpio",
    "sagittarius": "sagittarius", "dhanu": "sagittarius", "archer": "sagittarius",
    "capricorn": "capricorn", "makar": "capricorn", "goat": "capricorn",
    "aquarius": "aquarius", "kumbh": "aquarius", "water bearer": "aquarius",
    "pisces": "pisces", "meen": "pisces", "fish": "pisces"
}

def build_personalized_response(msg_lower, chart, name, lang="en"):
    try:
        analysis = astrology.generate_detailed_analysis(chart)
        sun = chart.get("sun_sign", "Unknown")
        moon = chart.get("moon_sign", "Unknown")
        asc = chart.get("rising_sign", "Unknown")
        planets = chart.get("planets", {})
        nname = name or "there"

        # Normalize misspellings via fuzzy matching
        msg_lower = spellfix.correct_spelling(msg_lower)

        # Helper: translate astrological terms and return Hindi if needed
        def t(text):
            if lang != "hi":
                return text
            return translations.translate_sign_planet(text, "hi")

        if any(w in msg_lower for w in ["my birth chart", "my chart", "my kundli", "about my chart"]):
            planets_str = "; ".join([f"{p}: {d.get('sign', '?')} {d.get('degree', 0):.1f}°" for p, d in planets.items()])
            if lang == "hi":
                return translations.CHART_ANALYSIS_HI.format(name=nname, sun=translations.SIGNS_HI.get(sun, sun), moon=translations.SIGNS_HI.get(moon, moon), asc=translations.SIGNS_HI.get(asc, asc), planets=t(planets_str), summary=t(analysis.get('summary', '')))
            return f"{nname}, here is your birth chart analysis. Your Sun sign is {sun} (identity, ego, life purpose). Your Moon sign is {moon} (emotions, subconscious, inner self). Your Ascendant/Rising sign is {asc} (outward personality, how others see you). Planetary positions: {planets_str}. {analysis.get('summary', '')}"

        if any(w in msg_lower for w in ["youtube", "you tube", "yt", "blogger", "blogging", "content creator", "influencer", "social media", "vlogger", "vlogging"]):
            mer = planets.get('Mercury', {}).get('sign', 'Gemini')
            ven = planets.get('Venus', {}).get('sign', 'Taurus')
            jup = planets.get('Jupiter', {}).get('sign', 'Sagittarius')
            tenth = analysis.get('element', 'Air')
            mer_comm = "strong" if mer in ['Gemini', 'Virgo', 'Libra'] else "moderate"
            ven_show = "strong" if ven in ['Leo', 'Libra', 'Pisces'] else "moderate"
            yes_no = "yes, your chart supports it" if mer_comm == "strong" and tenth == "Air" else "yes, with focused effort" if mer_comm != "weak" else "it's possible but requires extra dedication"
            if lang == "hi":
                mer_comm_hi = "मजबूत" if mer_comm == "strong" else "मध्यम"
                ven_show_hi = "मजबूत" if ven_show == "strong" else "मध्यम"
                yes_no_hi = "हाँ, आपकी कुंडली इसे समर्थन करती है" if "yes" in yes_no and "focused" not in yes_no and "possible" not in yes_no else "हाँ, केंद्रित प्रयास से" if "focused" in yes_no else "संभव है लेकिन अतिरिक्त समर्पण चाहिए"
                return translations.YOUTUBE_HI.format(name=nname, mer=t(mer), mer_comm=mer_comm_hi, ven=t(ven), ven_show=ven_show_hi, yes_no=yes_no_hi, element=t(tenth))
            return f"{nname}, regarding {msg_lower.split('as')[-1] if 'as' in msg_lower else 'content creation'} as a career: {yes_no}. Your Mercury in {mer} gives you {mer_comm} communication skills {'— ideal for scripting, presenting, and engaging with an audience' if mer_comm == 'strong' else '— you may need to work on consistent content creation'}. Venus in {ven} indicates {ven_show} creative and aesthetic sense {'that will attract viewers through visual appeal and charm' if ven_show == 'strong' else '— consider collaborating for production quality'}. Your 3rd house (communication) and 5th house (creativity) placements will play key roles in your success. Confidence: 78%. Best timing: Start building your channel now and you will see meaningful growth within 6-8 months. Preparation: Focus on a niche that combines your knowledge with your natural {tenth.lower()} energy — educational, lifestyle, or creative content suits your chart."

        if any(w in msg_lower for w in ["cricket", "cric ter", "cricter", "cricketer", "cricketer", "sports", "sport", "athlete", "athletic", "player", "football", "soccer", "basketball", "tennis"]):
            mars = planets.get('Mars', {}).get('sign', 'Aries')
            sun = planets.get('Sun', {}).get('sign', 'Leo')
            jup = planets.get('Jupiter', {}).get('sign', 'Sagittarius')
            sat = planets.get('Saturn', {}).get('sign', 'Capricorn')
            mars_str = "strong" if mars in ['Aries', 'Scorpio', 'Capricorn'] else "moderate"
            sun_str = "strong" if sun in ['Leo', 'Aries', 'Sagittarius'] else "moderate"
            yes_no = "yes, your chart shows athletic potential" if mars_str == "strong" and sun_str == "strong" else "yes, with training and discipline" if mars_str != "weak" else "it's possible but requires extra physical conditioning"
            if lang == "hi":
                mars_str_hi = "मजबूत" if mars_str == "strong" else "मध्यम"
                sun_str_hi = "मजबूत" if sun_str == "strong" else "मध्यम"
                yes_no_hi = "हाँ, आपकी कुंडली में एथलेटिक क्षमता है" if "athletic" in yes_no else "हाँ, प्रशिक्षण और अनुशासन से" if "training" in yes_no else "संभव है लेकिन अतिरिक्त शारीरिक परिश्रम चाहिए"
                return translations.SPORTS_HI.format(name=nname, mars=t(mars), mars_str=mars_str_hi, sun=t(sun), sun_str=sun_str_hi, yes_no=yes_no_hi)
            return f"{nname}, regarding sports as a career: {yes_no}. Your Mars in {mars} gives you {mars_str} physical drive and competitiveness {'— a natural advantage for sports requiring stamina and aggression' if mars_str == 'strong' else '— consistency in training will be key'}. Your Sun in {sun} indicates {sun_str} leadership and confidence {'that helps in high-pressure sports environments' if sun_str == 'strong' else '— building self-belief through practice is important'}. Saturn in {sat} influences your discipline and long-term athletic development. Confidence: 80%. Best timing: The next 12-18 months are favorable for starting serious training. Preparation: Focus on building endurance and technical skills before competitive matches."

        if any(w in msg_lower for w in ["my career", "my job", "my profession", "career for me", "what should i do for work", "will i get promoted", "promotion", "job change", "career growth", "professional", "work life", "get promoted", "career", "carrier", "business", "startup", "entrepreneur", "side hustle", "freelance", "new job", "should i start", "can i start", "thinking of starting", "want to start", "work from home", "online business"]):
            career = analysis.get("career", ["Various career paths suit your chart"])
            car_conf = analysis.get("career_confidence", 85)
            car_reason = analysis.get("career_reasoning", "Jupiter strengthens your 10th house while Saturn supports long-term growth")
            car_window = analysis.get("best_timing_career", "August-November")
            car_prep = analysis.get("preparation_career", "Focus on leadership responsibilities")
            if lang == "hi":
                return translations.CAREER_HI.format(name=nname, element=t(analysis.get('element', '')), career='; '.join(career), confidence=car_conf, conf_label=translations.confidence_hi(car_conf), reasoning=t(car_reason), best_window=translations.timing_hi(car_window), preparation=t(car_prep))
            return f"{nname}, based on your birth chart: your Sun in {sun} indicates natural career strengths. Key career indications for you: {'; '.join(career)}. Your chart shows you would excel in fields that align with your {analysis.get('element', '')} energy and {analysis.get('quality', '')} nature. Confidence: {car_conf}%. Reasoning: {car_reason}. Best window for career moves: {car_window}. Preparation: {car_prep}."

        if any(w in msg_lower for w in ["my love", "my relationship", "my romance", "love life", "compatibility", "get married", "marriage", "will i find love", "when will i get married", "partner", "soulmate", "relationship", "love", "when will i marry"]):
            rel = analysis.get("relationships", ["Partnerships are important for growth"])
            venus_sign = planets.get('Venus', {}).get('sign', 'a sign')
            love_conf = analysis.get("love_confidence", 72)
            love_reason = analysis.get("love_reasoning", f"Your Venus in {venus_sign} with current planetary aspects creates favorable relationship timing")
            love_window = analysis.get("best_timing_love", "favorable periods indicated in your chart")
            love_prep = analysis.get("preparation_love", "Focus on open communication and emotional vulnerability")
            moon_needs = {'Cancer': 'intuitive understanding', 'Scorpio': 'intuitive understanding', 'Pisces': 'intuitive understanding', 'Taurus': 'practical stability', 'Virgo': 'practical stability', 'Capricorn': 'practical stability', 'Gemini': 'intellectual connection', 'Libra': 'intellectual connection', 'Aquarius': 'intellectual connection'}
            if lang == "hi":
                return translations.LOVE_HI.format(name=nname, sign=t(venus_sign), confidence=love_conf, conf_label=translations.confidence_hi(love_conf), reasoning=t(love_reason), best_window=translations.timing_hi(love_window), preparation=t(love_prep))
            return f"{nname}, regarding love and relationships: {'; '.join(rel)}. Your Moon in {moon} shows you need emotional security through {moon_needs.get(moon, 'connection')}. Venus in {venus_sign} reveals your love language and what you value in a partner. Confidence: {love_conf}%. Reasoning: {love_reason}. Best window for relationship growth: {love_window}. Preparation: {love_prep}."

        if any(w in msg_lower for w in ["my strength", "my weakness", "strength and weakness", "good at", "bad at", "strengths", "weaknesses", "what am i good at"]):
            strengths = analysis.get("strengths", ["Natural talents"])
            challenges = analysis.get("challenges", ["Areas for growth"])
            if lang == "hi":
                return f"{nname}, आपकी जन्म कुंडली के अनुसार आपकी ताकत: {'; '.join(strengths)}. विकास के क्षेत्र: {'; '.join(challenges) if challenges else 'आपकी कुंडली में सभी क्षेत्रों में संतुलित ऊर्जा है'}."
            return f"{nname}, your birth chart reveals these strengths: {'; '.join(strengths)}. Areas for growth: {'; '.join(challenges) if challenges else 'Your chart shows balanced energy across all areas.'}. Your Sun in {sun} gives you the core drive of a {sun.lower()}, which brings both gifts and lessons."

        if any(w in msg_lower for w in ["my health", "my body", "health for me", "wellness", "health", "sick", "disease", "well being", "healthy"]):
            health = analysis.get("health", ["Maintain balance in lifestyle"])
            sixth_sign = analysis.get("sixth_house_sign", "your chart indicates")
            hlth_conf = analysis.get("health_confidence", 78)
            hlth_reason = analysis.get("health_reasoning", f"Your Moon in {moon} and 6th house in {sixth_sign} indicate health patterns")
            hlth_window = analysis.get("best_timing_health", "the coming months")
            hlth_prep = analysis.get("preparation_health", "Establish consistent wellness routines")
            if lang == "hi":
                return translations.HEALTH_HI.format(name=nname, sign=t(sixth_sign), confidence=hlth_conf, conf_label=translations.confidence_hi(hlth_conf), reasoning=t(hlth_reason), best_window=translations.timing_hi(hlth_window), preparation=t(hlth_prep))
            return f"{nname}, health insights from your chart: {'; '.join(health)}. Your Sun in {sun} suggests paying attention to health areas related to that sign. For personalized health recommendations, consider your complete chart and consult with a healthcare professional. Confidence: {hlth_conf}%. Reasoning: {hlth_reason}. Best focus period: {hlth_window}. Preparation: {hlth_prep}."

        if any(w in msg_lower for w in ["my finance", "my money", "my wealth", "rich", "wealth", "financial", "money", "finance", "investment", "property", "wealthy"]):
            fin = analysis.get("finance", ["Financial stability is indicated in your chart"])
            if lang == "hi":
                return translations.FINANCE_HI.format(name=nname, sign=t(planets.get('Jupiter', {}).get('sign', 'धनु')), confidence=75, conf_label="उच्च", reasoning=t("Your 2nd house wealth and 11th house gains with Jupiter and Venus shape your financial prospects"), best_window="अगले कुछ महीने", preparation=t("बचत और निवेश पर ध्यान दें"))
            return f"{nname}, regarding finances: Your 2nd house (wealth) and 11th house (gains) combined with Jupiter and Venus placements shape your financial prospects. {' '.join(fin) if isinstance(fin, list) else fin} For a detailed wealth analysis, visit the Wealth Prediction tab."

        if any(w in msg_lower for w in ["my future", "future", "what will happen", "prediction", "predict", "upcoming", "what is in store", "destiny"]):
            if lang == "hi":
                dasha_name = "?"
                try:
                    d = astrology.calculate_vimshottari_dasha(chart.get("birth_date", ""), chart.get("birth_time", ""), chart.get("latitude", 0), chart.get("longitude", 0))
                    dasha_name = d.get("current_dasha", "?")
                except: pass
                return translations.FUTURE_HI.format(name=nname, element=t(analysis.get('element', 'वायु')), dasha=t(dasha_name), career_direction=t('; '.join(analysis.get('career', ['Professional growth']))))
            return f"{nname}, based on your birth chart analysis: Your Sun in {sun} drives your life purpose. You are currently in a period influenced by your {planets.get('Sun', {}).get('sign', sun)} Sun and {moon} Moon. Key life areas to focus on: {'; '.join(analysis.get('career', ['Professional growth']))}. For detailed future predictions, visit the 10-Year Predictions tab with year-by-year analysis."

        if any(w in msg_lower for w in ["my sun sign", "my sun"]):
            info = zodiac_info.get(sun.lower(), "")
            if lang == "hi":
                sinfo = t(info[:200]) + ("..." if len(info) > 200 else "")
                return f"{nname}, आपकी सूर्य राशि {translations.SIGNS_HI.get(sun, sun)} है। {sinfo}"
            return f"{nname}, your Sun sign is {sun}. {info}"

        if any(w in msg_lower for w in ["my moon sign", "my moon"]):
            info = zodiac_info.get(moon.lower(), "")
            if lang == "hi":
                minfo = t(info[:200]) + ("..." if len(info) > 200 else "")
                return f"{nname}, आपकी चंद्र राशि {translations.SIGNS_HI.get(moon, moon)} है। {minfo}"
            return f"{nname}, your Moon sign is {moon}. {info}"

        if any(w in msg_lower for w in ["my rising", "my ascendant", "my rising sign"]):
            info = zodiac_info.get(asc.lower(), "")
            if lang == "hi":
                ainfo = t(info[:200]) + ("..." if len(info) > 200 else "")
                return f"{nname}, आपकी लग्न राशि {translations.SIGNS_HI.get(asc, asc)} है। {ainfo}"
            return f"{nname}, your Rising sign (Ascendant) is {asc}. {info}"

        if any(w in msg_lower for w in ["my numerology", "my life path", "my destiny number", "my soul urge", "tell my numbers"]):
            try:
                num = astrology.calculate_numerology(nname if nname != "there" else "User", chart.get("birth_date", ""))
                if lang == "hi":
                    return f"{nname}, आपकी पूर्ण अंक ज्योतिष प्रोफ़ाइल: जीवन पथ अंक {num.get('life_path', '?')} ({t(str(num.get('life_path_meaning', '')))}). भाग्य अंक {num.get('destiny', '?')} ({t(str(num.get('destiny_meaning', '')))}). आत्मा अंक {num.get('soul_urge', '?')} ({t(str(num.get('soul_urge_meaning', '')))}). व्यक्तित्व अंक {num.get('personality', '?')} ({t(str(num.get('personality_meaning', '')))}). वर्तमान व्यक्तिगत वर्ष: {num.get('personal_year', '?')} ({t(str(num.get('personal_year_meaning', '')))})."
                return f"{nname}, here is your complete numerology profile: Life Path Number {num.get('life_path', '?')} ({num.get('life_path_meaning', 'Your life journey')}). Destiny Number {num.get('destiny', '?')} ({num.get('destiny_meaning', 'Your purpose')}). Soul Urge Number {num.get('soul_urge', '?')} ({num.get('soul_urge_meaning', 'Inner desires')}). Personality Number {num.get('personality', '?')} ({num.get('personality_meaning', 'How others see you')}). Current Personal Year: {num.get('personal_year', '?')} ({num.get('personal_year_meaning', 'Your theme for this year')})."
            except:
                return f"{nname}, I can look up your numerology if you provide your full birth date and name in the Profile tab."

        if any(w in msg_lower for w in ["my dasha", "my planetary period", "current dasha", "my mahadasha"]):
            try:
                kp = astrology.calculate_kp_chart(chart.get("birth_date", ""), chart.get("birth_time", ""), chart.get("latitude", 0), chart.get("longitude", 0))
                dasha = astrology.calculate_vimshottari_dasha(chart.get("birth_date", ""), chart.get("birth_time", ""), chart.get("latitude", 0), chart.get("longitude", 0))
                nak = kp.get("planets", {}).get("Moon", {}).get("nakshatra", "?")
                lord = dasha.get("moon_nakshatra_lord", "?")
                current = dasha.get("current_dasha", "?")
                if lang == "hi":
                    return f"{nname}, आपका चंद्रमा {t(nak)} नक्षत्र में है जिसके स्वामी {t(lord)} हैं। आप वर्तमान में {t(current)} महादशा से गुज़र रहे हैं। {t(dasha.get('message', ''))} विस्तृत दशा भविष्यवाणियों के लिए KP दशा टैब पर जाएं।"
                return f"{nname}, your Moon is in {nak} Nakshatra ruled by {lord}. You are currently running {current} Mahadasha. {dasha.get('message', '')} For detailed dasha predictions, visit the KP Dasha tab."
            except:
                return f"{nname}, I can calculate your current dasha periods if you provide your complete birth details in the Profile tab."

        if any(w in msg_lower for w in ["my gemstone", "gemstone for me", "what gemstone should i wear", "remedies for me", "my remedy", "gemstone", "gem", "stone", "wear"]):
            sun_lower = sun.lower()
            gem_map = {"aries": "Red Coral", "taurus": "Emerald or Diamond", "gemini": "Emerald", "cancer": "Pearl", "leo": "Ruby", "virgo": "Sapphire", "libra": "Opal", "scorpio": "Topaz", "sagittarius": "Turquoise or Yellow Sapphire", "capricorn": "Garnet or Blue Sapphire", "aquarius": "Amethyst", "pisces": "Jade or Moonstone"}
            gem = gem_map.get(sun_lower, "a gemstone suitable for your chart")
            gem_hi = {"Red Coral": "मूंगा", "Emerald or Diamond": "पन्ना या हीरा", "Emerald": "पन्ना", "Pearl": "मोती", "Ruby": "माणिक", "Sapphire": "नीलम", "Opal": "ओपल", "Topaz": "पुखराज", "Turquoise or Yellow Sapphire": "फ़िरोज़ा या पीला नीलम", "Garnet or Blue Sapphire": "गार्नेट या नीला नीलम", "Amethyst": "कटैला", "Jade or Moonstone": "जेड या चंद्रकांत"}
            if lang == "hi":
                return f"{nname}, आपकी सूर्य राशि {translations.SIGNS_HI.get(sun, sun)} के अनुसार, अनुशंसित रत्न {gem_hi.get(gem, gem)} है। सटीक रत्न चयन के लिए पूर्ण कुंडली विश्लेषण आवश्यक है। उपाय टैब पर जाएं।"
            return f"{nname}, based on your Sun sign {sun}, a recommended gemstone is {gem}. However, for accurate gemstone selection, a complete chart analysis is needed considering planetary strengths, dignity, and current dasha periods. Visit the Remedies tab for a full analysis."

        if lang == "hi":
            return translations.GENERAL_HI.format(name=nname, sun=translations.SIGNS_HI.get(sun, sun), moon=translations.SIGNS_HI.get(moon, moon), asc=translations.SIGNS_HI.get(asc, asc), element=t(analysis.get('element', 'वायु')), house=t("प्रथम, चतुर्थ, सप्तम एवं दशम"))
        return f"{nname}, based on your birth chart: Your {sun} Sun drives your core identity, and your {moon} Moon shapes your emotional world. With {asc} rising, you present yourself with a {asc.lower()} demeanor. Career-wise, your Mercury in {planets.get('Mercury', {}).get('sign', 'a communicative sign')} influences your professional communication style. This is a good time to explore paths that align with your natural strengths. For more specific answers, try asking directly about career, love, health, or visit the relevant tab for detailed predictions."
    except:
        return None

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
        birth_data = data.get("birth_data", None) if data else None
        tab_context = data.get("tab_context", {}) if data else {}
        lang = data.get("language", "en") if data else "en"

        if not msg:
            return {"response": "Please provide a message"}

        msg_lower = msg.lower()
        has_birth = birth_data and birth_data.get("birthDate") and birth_data.get("birthTime")
        user_name = (birth_data.get("name", "") if birth_data else "") or ""

        if has_birth:
            try:
                bd = birth_data
                if bd.get("birthDate") and bd.get("birthTime"):
                    chart = astrology.calculate_natal_chart(bd["birthDate"], bd["birthTime"], float(bd.get("latitude", 28.6139)), float(bd.get("longitude", 77.209)), bd.get("timezone", "Asia/Kolkata"))
                    if "error" not in chart:
                        chart["birth_date"] = bd["birthDate"]
                        chart["birth_time"] = bd["birthTime"]
                        chart["latitude"] = float(bd.get("latitude", 28.6139))
                        chart["longitude"] = float(bd.get("longitude", 77.209))
                        personalized = build_personalized_response(msg_lower, chart, bd.get("name", ""), lang)
                        if personalized:
                            return {"response": personalized}
            except Exception as e:
                return {"response": f"I have your birth details but encountered an issue computing your chart: {str(e)}. I can still answer general questions for you."}

        # Tab context based responses - AI knows what user just looked at
        if tab_context:
            tarot = tab_context.get("tarot")
            if tarot and tarot.get("cards"):
                cards = tarot["cards"]
                if any(w in msg_lower for w in ["first card", "card 1", "card one", "card #1"]):
                    c = cards[0]
                    return {"response": f"The first card in your reading is {c.get('name', 'Unknown')}. In the {c.get('position', '?')} position, it represents: {c.get('meaning', 'A meaningful card')}. The advice from this card: {c.get('advice', 'Trust your inner wisdom')}. This card sets the foundation for your reading and addresses the core energy around your question."}
                if any(w in msg_lower for w in ["second card", "card 2", "card two", "card #2"]):
                    c = cards[1] if len(cards) > 1 else cards[0]
                    return {"response": f"The second card is {c.get('name', 'Unknown')} in the {c.get('position', '?')} position. Meaning: {c.get('meaning', 'A card of significance')}. Advice: {c.get('advice', 'Pay attention to the signs')}. This card represents the challenges or opportunities you need to navigate."}
                if any(w in msg_lower for w in ["third card", "card 3", "card three", "card #3"]):
                    c = cards[2] if len(cards) > 2 else cards[-1]
                    return {"response": f"The third card is {c.get('name', 'Unknown')} in the {c.get('position', '?')} position. Meaning: {c.get('meaning', 'A guiding message')}. Advice: {c.get('advice', 'Look forward with hope')}. This card reveals the likely outcome or guidance for moving forward."}
                if len(cards) >= 4 and any(w in msg_lower for w in ["fourth card", "card 4", "card four", "card #4"]):
                    c = cards[3]
                    return {"response": f"The fourth card is {c.get('name', 'Unknown')} in the {c.get('position', '?')} position. Meaning: {c.get('meaning', 'Additional insight')}. Advice: {c.get('advice', 'Integrate this wisdom')}."}
                if any(w in msg_lower for w in ["all card", "all three", "all tarot", "explain the reading", "what do these cards mean", "tell me about this reading", "my cards", "my tarot", "this reading", "the spread"]):
                    q = tarot.get("question", "Not specified")
                    descs = "; ".join([f"{c.get('name', '?')} ({c.get('position','?')}): {c.get('meaning', '?')}" for c in cards])
                    return {"response": f"Here is your complete tarot reading interpretation. Your question was: \"{q}\". Cards drawn: {descs}. Overall summary: {tarot.get('summary', 'Your cards reveal meaningful guidance')}. Guidance: {tarot.get('guidance', 'Trust the journey')}. Each card's position in the spread tells part of your story — together they paint a picture of your current situation, the forces at play, and the path ahead."}

            hor = tab_context.get("horoscope")
            if hor and any(w in msg_lower for w in ["my horoscope", "today's prediction", "today horoscope", "daily horoscope", "what does today", "my daily", "explain my horoscope"]):
                return {"response": f"Your daily horoscope for {hor.get('sign', 'your sign')} on {hor.get('date', 'today')}: {hor.get('prediction', 'A day of potential and growth')}. Your mood: {hor.get('mood', 'Balanced')}. Lucky number: {hor.get('lucky_number', '?')}. Lucky color: {hor.get('lucky_color', '?')}. Lucky day: {hor.get('lucky_day', '?')}. Focus area: {hor.get('focus_area', 'Personal growth')}. This prediction is based on the current lunar transit and how it aspects your Sun sign. Confidence: Career {hor.get('confidence_career','?')}% | Love {hor.get('confidence_love','?')}% | Health {hor.get('confidence_health','?')}% | Finance {hor.get('confidence_finance','?')}%. Reasoning: {hor.get('reasoning','')} Best timing: {hor.get('best_timing','')} Preparation: {hor.get('preparation','')}"}

            wk = tab_context.get("weekly")
            if wk and any(w in msg_lower for w in ["my weekly", "this week", "weekly horoscope", "week ahead", "explain my week"]):
                return {"response": f"Your weekly horoscope for {wk.get('sign', 'your sign')}\n💕 Love: {wk.get('love', 'A week for connection')}\n💼 Career: {wk.get('career', 'Professional growth indicated')}\n❤️ Health: {wk.get('health', 'Focus on wellbeing')}\n💰 Finance: {wk.get('finance', 'Financial stability')}\nWeekly advice: {wk.get('advice', 'Trust your path')}\nLucky color: {wk.get('lucky_color', '?')}, Lucky number: {wk.get('lucky_number', '?')}\nWeek rating: {wk.get('rating', '?')}/10"}

            mo = tab_context.get("monthly")
            if mo and any(w in msg_lower for w in ["my monthly", "this month", "monthly horoscope", "month ahead", "explain my month"]):
                return {"response": f"Your monthly horoscope for {mo.get('sign', 'your sign')} — {mo.get('month', '?')}/{mo.get('year', '?')}\nTheme: {mo.get('theme', 'A month of growth')}\n💼 Career: {mo.get('career', 'Career developments ahead')}\n💕 Love: {mo.get('love', 'Relationship insights')}\n💰 Finance: {mo.get('finance', 'Financial outlook')}\n❤️ Health: {mo.get('health', 'Health guidance')}\nHighlights: {mo.get('highlights', 'Positive developments')}\nChallenges: {mo.get('challenges', 'Areas requiring attention')}\nSpirit animal: {mo.get('spirit_animal', '?')}\nLucky days: {mo.get('lucky_days', '?')}\nRating: {mo.get('rating', '?')}/10"}

            num = tab_context.get("numerology")
            if num:
                if any(w in msg_lower for w in ["my life path", "explain my life path", "life path number", "what is my life path"]):
                    return {"response": f"Your Life Path Number is {num.get('life_path', '?')}. This is your primary numerology number, calculated from your full birth date. It represents your life's purpose, the journey you're meant to take, and the lessons you'll encounter along the way. It's the most significant number in your numerology chart and shapes your overall life direction."}
                if any(w in msg_lower for w in ["my destiny", "destiny number", "my expression", "expression number"]):
                    return {"response": f"Your Destiny (Expression) Number is {num.get('destiny', '?')}. Calculated from your full birth name, this number reveals your natural talents, abilities, and the goals you're meant to achieve in this lifetime. It represents the potential you're working to fulfill."}
                if any(w in msg_lower for w in ["my soul urge", "soul urge", "heart's desire", "my heart desire"]):
                    return {"response": f"Your Soul Urge (Heart's Desire) Number is {num.get('soul_urge', '?')}. Derived from the vowels in your name, this number reveals your innermost desires, what truly motivates you, and what your soul deeply craves for fulfillment."}
                if any(w in msg_lower for w in ["my personality", "personality number"]):
                    return {"response": f"Your Personality Number is {num.get('personality', '?')}. Based on the consonants in your name, this number shows how others perceive you — the outer persona you present to the world. It's the first impression you make."}
                if any(w in msg_lower for w in ["my personal year", "personal year", "my year number", "this year for me"]):
                    return {"response": f"Your Personal Year Number is {num.get('personal_year', '?')}. This number changes every year (calculated from your birth month/day + current year) and reveals the theme, lessons, and opportunities for your current year. It guides you on what energy to work with for this 12-month cycle."}
                if any(w in msg_lower for w in ["my numbers", "my numerology", "tell me about my numerolog", "explain my number"]):
                    return {"response": f"Here is your complete numerology profile:\nLife Path {num.get('life_path', '?')} (your life journey)\nDestiny {num.get('destiny', '?')} (your purpose)\nSoul Urge {num.get('soul_urge', '?')} (inner desires)\nPersonality {num.get('personality', '?')} (outer persona)\nPersonal Year {num.get('personal_year', '?')} (current theme)\nBirth Day {num.get('birth_day', '?')} (your natural gift). These numbers together create a comprehensive picture of your numerological blueprint."}

            yr = tab_context.get("yearly")
            if yr and yr.get("predictions"):
                preds = yr["predictions"]
                year_match = None
                import re
                for y in range(2020, 2100):
                    if str(y) in msg_lower:
                        for p in preds:
                            if p.get("year") == y:
                                year_match = p
                                break
                        break
                if year_match:
                    career_d = year_match.get("career", {})
                    love_d = year_match.get("love", {})
                    finance_d = year_match.get("finance", {})
                    health_d = year_match.get("health", {})
                    career_text = f"💼 Career ({career_d.get('confidence', '?')}%): {career_d.get('prediction', year_match.get('career_prediction', 'Professional developments'))}... Reasoning: {career_d.get('reasoning', 'Planetary alignments support career growth')}. Best window: {career_d.get('best_window', 'Your chart cycles')}. Preparation: {career_d.get('preparation', 'Focus on skill development')}"
                    love_text = f"❤️ Love ({love_d.get('confidence', '?')}%): {love_d.get('prediction', year_match.get('love_prediction', 'Relationship insights'))}... Reasoning: {love_d.get('reasoning', 'Venus and 7th house indicate relationship growth')}. Best window: {love_d.get('best_window', 'Your relationship cycles')}. Preparation: {love_d.get('preparation', 'Nurture emotional connections')}"
                    finance_text = f"💰 Finance ({finance_d.get('confidence', '?')}%): {finance_d.get('prediction', year_match.get('finance_prediction', 'Financial outlook'))}... Reasoning: {finance_d.get('reasoning', 'Jupiter and 2nd house influence financial trends')}. Best window: {finance_d.get('best_window', 'Your financial cycles')}. Preparation: {finance_d.get('preparation', 'Plan investments carefully')}"
                    health_text = f"🏥 Health ({health_d.get('confidence', '?')}%): {health_d.get('prediction', year_match.get('health_prediction', 'Health guidance'))}... Reasoning: {health_d.get('reasoning', 'Moon and 6th house indicate health patterns')}. Best window: {health_d.get('best_window', 'Your health cycles')}. Preparation: {health_d.get('preparation', 'Maintain balanced routines')}"
                    return {"response": f"Prediction for {year_match.get('year', '?')} (age {year_match.get('age', '?')}):\nMahadasha: {year_match.get('mahadasha', '?')}\nAntardasha: {year_match.get('antardasha', '?')}\nOverall theme: {year_match.get('overall_theme', 'A year of growth')}\n{career_text}\n{love_text}\n{finance_text}\n{health_text}\nRating: {year_match.get('rating', '?')}/10"}
                if any(w in msg_lower for w in ["my prediction", "my future", "my 10 year", "what will happen", "future prediction", "dasha predictions"]):
                    return {"response": f"Your 10-year predictions are available in the 10-Year Predictions tab. The current year's Mahadasha is {preds[0].get('mahadasha', '?')} with {preds[0].get('antardasha', '?')} Antardasha. Your chart shows {yr.get('chart_summary', {}).get('sun_sign', '?')} Sun, {yr.get('chart_summary', {}).get('moon_sign', '?')} Moon, {yr.get('chart_summary', {}).get('rising_sign', '?')} Rising. Ask about a specific year (e.g., 'What happens in 2027?') for detailed predictions."}

            da = tab_context.get("detailed_analysis")
            if da:
                if any(w in msg_lower for w in ["my strength", "my weakness", "strength and weakness", "what am i good at"]):
                    strs = da.get("strengths", [])
                    chals = da.get("challenges", [])
                    return {"response": f"Your birth chart reveals these key strengths: {'; '.join(strs) if strs else 'Natural talents across multiple areas'}. Areas for growth: {'; '.join(chals) if chals else 'Balanced energy overall'}. Your Sun in {da.get('sun_sign', '?')} gives you your core drive, while your Moon in {da.get('moon_sign', '?')} shapes your emotional nature."}
                if any(w in msg_lower for w in ["my career", "my job", "career for me", "what should i do for work", "my profession"]):
                    car = da.get("career", [])
                    car_conf = da.get("career_confidence", "?")
                    car_reason = da.get("career_reasoning", "Planetary alignments support your professional growth")
                    car_timing = da.get("best_timing_career", "your chart cycles")
                    car_prep = da.get("preparation_advice", "Continue developing your strengths")
                    return {"response": f"Your career insights based on your chart: {'; '.join(car) if car else 'Multiple career paths suit your chart'}. Your Sun in {da.get('sun_sign', '?')} indicates natural leadership qualities, and your 10th house ruler further shapes your professional path. Confidence scores: Career {car_conf}%. {car_reason} Best timing: Career growth during {car_timing} Preparation: {car_prep}"}
                if any(w in msg_lower for w in ["my love", "my relationship", "love life", "compatibility"]):
                    rel = da.get("relationships", [])
                    love_conf = da.get("love_confidence", "?")
                    love_reason = da.get("love_reasoning", "Venus and 7th house placements shape your relationship dynamics")
                    love_timing = da.get("best_timing_love", "your relationship cycles")
                    love_prep = da.get("preparation_advice", "Continue developing your strengths")
                    return {"response": f"Love and relationship insights from your chart: {'; '.join(rel) if rel else 'Meaningful partnerships indicated'}. Venus and 7th house placements play key roles in your relationship dynamics. Confidence scores: Love {love_conf}%. {love_reason} Best timing: Relationship growth during {love_timing} Preparation: {love_prep}"}
                if any(w in msg_lower for w in ["my health", "my body", "health for me", "wellness"]):
                    hea = da.get("health", [])
                    hlth_conf = da.get("health_confidence", "?")
                    hlth_reason = da.get("health_reasoning", "Moon and 6th house influence your wellbeing patterns")
                    hlth_timing = da.get("best_timing_health", "your health cycles")
                    hlth_prep = da.get("preparation_advice", "Continue developing your strengths")
                    return {"response": f"Health insights from your chart: {'; '.join(hea) if hea else 'Balance is key for your wellbeing'}. Your chart indicates areas to focus on for optimal wellness. Confidence scores: Health {hlth_conf}%. {hlth_reason} Best timing: Health focus during {hlth_timing} Preparation: {hlth_prep}"}

        greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening", "good afternoon"]
        if any(g in msg_lower for g in greetings):
            if has_birth and user_name:
                return {"response": f"Hello {user_name}! I'm your personal astrology assistant. I can see you've shared your birth details. Ask me about your birth chart, career, love life, strengths and weaknesses, numerology, or current dasha periods. You can also ask about any zodiac sign, tarot, planets, or KP astrology."}
            return {"response": "Hello! I'm your detailed astrology assistant. Ask me about any zodiac sign for an in-depth personality profile, career guidance, love compatibility, health advice, and more. You can also ask about numerology, tarot, planets, horoscopes, or KP astrology. For example: 'Tell me everything about Aries' or 'What career is best for Virgo?'"}

        detected_sign = None
        for alias, sign_name in aliases.items():
            if alias in msg_lower:
                detected_sign = sign_name
                break

        if detected_sign:
            return {"response": zodiac_info[detected_sign]}

        if "numerology" in msg_lower or "lucky number" in msg_lower:
            return {"response": "In Numerology, each number 1-9 has unique traits. Number 1 (Leadership, independence, ambition). Number 2 (Cooperation, diplomacy, sensitivity). Number 3 (Creativity, self-expression, joy). Number 4 (Stability, hard work, practicality). Number 5 (Freedom, adventure, versatility). Number 6 (Harmony, family, responsibility). Number 7 (Spirituality, analysis, introspection). Number 8 (Abundance, power, success). Number 9 (Wisdom, compassion, completion). Master numbers 11 (Intuition, enlightenment), 22 (Master builder, manifesting dreams), 33 (Master teacher, unconditional love) carry higher spiritual vibrations. Your Life Path Number is the most important - calculated from your full birth date reduced to a single digit (or master number)."}

        if "tarot" in msg_lower:
            return {"response": "Tarot cards offer guidance through rich symbolism. The 78-card deck divides into: Major Arcana (22 cards, 0-21) representing life's major spiritual lessons - The Fool (0 - new beginnings, spontaneity), The Magician (1 - manifestation, skill), The High Priestess (2 - intuition, mystery), The Empress (3 - abundance, nurturing), The Emperor (4 - authority, structure), The Hierophant (5 - tradition, spiritual guidance), The Lovers (6 - choices, relationships), The Chariot (7 - willpower, victory), Strength (8 - courage, inner power), The Hermit (9 - introspection, soul-searching), Wheel of Fortune (10 - destiny, cycles), Justice (11 - truth, fairness), The Hanged Man (12 - surrender, new perspective), Death (13 - transformation, endings), Temperance (14 - balance, moderation), The Devil (15 - materialism, shadow self), The Tower (16 - upheaval, revelation), The Star (17 - hope, inspiration), The Moon (18 - illusion, subconscious), The Sun (19 - joy, success), Judgement (20 - rebirth, inner calling), The World (21 - completion, fulfillment). Minor Arcana (56 cards, 4 suits) covers daily life: Wands (passion, creativity, action), Cups (emotions, relationships, intuition), Swords (thoughts, challenges, truth), Pentacles (material world, work, finances). Each suit has 10 numbered cards (Ace through 10) and 4 Court cards (Page, Knight, Queen, King)."}

        if "planet" in msg_lower or "sun" in msg_lower or "moon" in msg_lower or "mercury" in msg_lower or "venus" in msg_lower or "mars" in msg_lower or "jupiter" in msg_lower or "saturn" in msg_lower or "uranus" in msg_lower or "neptune" in msg_lower or "pluto" in msg_lower:
            return {"response": "Planets in astrology each rule specific areas of life: Sun (core identity, ego, vitality, the Self - rules Leo). Moon (emotions, subconscious, habits, nurturing - rules Cancer). Mercury (communication, intellect, thinking style, travel - rules Gemini and Virgo). Venus (love, beauty, values, pleasure, money - rules Taurus and Libra). Mars (energy, drive, anger, passion, ambition - rules Aries and traditionally Scorpio). Jupiter (expansion, luck, wisdom, higher learning, abundance - rules Sagittarius and traditionally Pisces). Saturn (discipline, responsibility, limitations, karma, life lessons - rules Capricorn and traditionally Aquarius). Uranus (innovation, rebellion, sudden changes, originality - rules Aquarius). Neptune (dreams, illusions, spirituality, creativity, transcendence - rules Pisces). Pluto (transformation, power, death/rebirth, the subconscious - rules Scorpio). The sign and house position of each planet in your birth chart reveals how these energies express in your life."}

        if "horoscope" in msg_lower or "daily" in msg_lower:
            return {"response": "For daily, weekly, or monthly horoscopes, visit the Horoscope tab in the app. Each sign receives unique predictions based on planetary transits and aspects. Your horoscope changes based on the Moon's position each day and how it aspects your Sun sign. For a personalized reading, use the Kundli or Birth Chart tabs with your exact birth details (date, time, place). Would you like to know about a particular sign's horoscope trends?"}

        if "kp" in msg_lower or "sub lord" in msg_lower or "krishnamurti" in msg_lower:
            return {"response": "KP (Krishnamurti Paddhati) astrology is a precise system of prediction developed by Prof. K. S. Krishnamurti. It uses the Nakshatra (constellation) sub-lord system for accurate event timing. Each of the 27 Nakshatras (13°20' each) is divided into 9 unequal sub-divisions called sub-lords, ruled by different planets in the Vimshottari Dasha order (Ket, Ven, Sun, Moon, Mars, Rah, Jup, Sat, Mer). The sub-lord at the time of a question (Prashna/horary astrology) or at birth determines the outcome. KP uses 4 key principles: (1) Significators based on planet ownership and occupancy, (2) Sub-lord theory for precise prediction, (3) Ruling planets at the moment of query, (4) Cuspal link theory connecting houses to events. It's widely used for predicting marriage timing, career events, financial gains, and legal matters."}

        if "vedic" in msg_lower or "hindu" in msg_lower or "jyotish" in msg_lower:
            return {"response": "Vedic astrology (Jyotish) is the ancient Indian science of light. Key differences from Western astrology: (1) It uses the Sidereal zodiac (fixed star positions) vs Western Tropical zodiac (seasonal). This means your Vedic sign may differ from your Western sign by about 24 degrees. (2) It uses 27 Nakshatras (lunar mansions) of 13°20' each, each with unique qualities and deities. (3) The 9 planets (Navagraha) include Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, plus the shadow planets Rahu (North Lunar Node) and Ketu (South Lunar Node). (4) It uses a complex Dasha system (planetary periods) for timing events, primarily Vimshottari Dasha (120-year cycle). (5) 16 Varga charts (divisional charts) examine specific life areas. (6) Ashtakavarga system for strength assessment. (7) Numerous Yogas (planetary combinations) that create specific life results. The birth chart (Kundli) is the foundation of all predictions."}

        if ("house" in msg_lower and ("birth" in msg_lower or "chart" in msg_lower or "kundli" in msg_lower)):
            return {"response": "In astrology, the 12 houses represent different areas of life: 1st House (Self, personality, physical appearance - Aries). 2nd House (Wealth, family, speech, values - Taurus). 3rd House (Communication, siblings, courage, short journeys - Gemini). 4th House (Home, mother, emotions, property - Cancer). 5th House (Creativity, children, romance, speculation - Leo). 6th House (Health, service, enemies, daily work - Virgo). 7th House (Marriage, partnerships, contracts, open enemies - Libra). 8th House (Transformation, death, inheritance, occult - Scorpio). 9th House (Higher learning, philosophy, luck, long journeys - Sagittarius). 10th House (Career, reputation, authority, father - Capricorn). 11th House (Gains, friendships, aspirations, social networks - Aquarius). 12th House (Loss, spirituality, isolation, foreign lands - Pisces). Planets placed in each house modify how that life area operates for you."}

        if "aspect" in msg_lower:
            return {"response": "Astrological aspects are angles between planets that create specific energetic relationships. Major aspects: Conjunction (0°, planets merge energies). Sextile (60°, harmonious opportunity). Square (90°, tension and growth). Trine (120°, natural flow and talent). Opposition (180°, polarity and balance). Minor aspects: Semi-sextile (30°), Quincunx/Inconjunct (150°), Semi-square (45°), Sesquiquadrate (135°). In KP astrology, aspect rules differ: all planets aspect the 7th house from themselves, plus Mars aspects 4th and 8th, Jupiter aspects 5th and 9th, Saturn aspects 3rd and 10th. Rahu and Ketu also aspect 5th and 9th."}

        return {"response": "I have detailed knowledge about all 12 zodiac signs including personality traits, strengths, weaknesses, career paths, health tendencies, love and relationship patterns, lucky attributes, and famous personalities. You can also ask about numerology (including Life Path Numbers), tarot cards (Major and Minor Arcana meanings), planets and their significations, horoscopes, KP astrology (sub-lord theory, significators), Vedic astrology (Nakshatras, Dasha systems, Yogas), birth chart houses, or astrological aspects. Try asking specific questions like: 'Tell me about Pisces in detail', 'What career suits a Gemini?', 'Who is Scorpio compatible with?', 'Explain planetary aspects', or 'What are Nakshatras?'"}

    except Exception as e:
        import traceback
        return {"response": f"AI Error: {str(e)}", "trace": traceback.format_exc()}
