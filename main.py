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
            "aries": (
                "Aries (March 21 - April 19) is the first Fire sign, ruled by Mars, and is a Cardinal sign initiating the zodiac. "
                "Aries natives are natural-born leaders with immense courage, pioneering spirit, and boundless energy. They are impulsive, competitive, and thrive on challenges. "
                "Strengths include bravery, confidence, optimism, and enthusiasm. Weaknesses include impatience, short temper, aggressiveness, and a tendency to be self-centered. "
                "In career, Aries excels in leadership roles, entrepreneurship, sports, military, police, firefighting, surgery, and any field requiring quick decisions and action. "
                "Health-wise, they are prone to headaches, migraines, sinus issues, injuries from accidents, and high blood pressure. They must guard against burnout. "
                "In love and relationships, Aries is passionate, direct, and highly romantic. They enjoy the chase and need a partner who can match their energy and independence. "
                "They are most compatible with Leo, Sagittarius, Gemini, and Aquarius. Challenging matches include Cancer and Capricorn. "
                "Lucky Color: Red. Lucky Day: Tuesday. Lucky Numbers: 1, 9. Lucky Stone: Red Coral. "
                "Famous Aries: Leonardo da Vinci, Thomas Jefferson, Charlie Chaplin, Mariah Carey, Robert Downey Jr."
            ),
            "taurus": (
                "Taurus (April 20 - May 20) is the first Earth sign, ruled by Venus, a Fixed sign known for stability and determination. "
                "Taurus natives are patient, reliable, practical, and deeply grounded. They love luxury, comfort, and sensual pleasures. Once they commit, they are loyal for life. "
                "Strengths include dependability, persistence, artistic talent, practicality, and a strong work ethic. Weaknesses include stubbornness, possessiveness, laziness when comfortable, and resistance to change. "
                "In career, Taurus thrives in finance, banking, accounting, real estate, art, music, culinary arts, fashion, and agriculture. They excel where patience and consistency matter. "
                "Health-wise, they are prone to throat issues, thyroid problems, neck tension, and weight gain. They benefit from regular exercise and portion control. "
                "In love, Taurus is deeply loyal, sensual, and values stability above all. They express love through physical affection, quality time, and providing material comfort. They need a partner who appreciates their steady nature. "
                "They are most compatible with Virgo, Capricorn, Cancer, and Pisces. Challenging matches include Leo and Aquarius. "
                "Lucky Color: Green. Lucky Day: Friday. Lucky Numbers: 2, 6. Lucky Stone: Diamond or Emerald. "
                "Famous Taurus: William Shakespeare, Sigmund Freud, Audrey Hepburn, Adele, Dwayne Johnson."
            ),
            "gemini": (
                "Gemini (May 21 - June 20) is the first Air sign, ruled by Mercury, a Mutable sign known for adaptability and intellect. "
                "Gemini natives are curious, witty, versatile, and excellent communicators. They have a youthful energy and love learning new things constantly. "
                "Strengths include intelligence, adaptability, quick wit, sociability, and eloquence. Weaknesses include inconsistency, indecisiveness, restlessness, nervousness, and a tendency to be superficial or gossipy. "
                "In career, Gemini excels in writing, journalism, teaching, sales, marketing, technology, programming, public relations, and any field requiring communication and mental agility. "
                "Health-wise, they are prone to lung issues, respiratory problems, anxiety, nervous disorders, and carpal tunnel syndrome. They need mental stimulation and fresh air. "
                "In love, Gemini needs intellectual stimulation and variety. They are flirtatious and charming but can be commitment-phobic until they find someone who keeps their mind engaged. Communication is the key to their heart. "
                "They are most compatible with Libra, Aquarius, Aries, and Leo. Challenging matches include Virgo and Pisces. "
                "Lucky Color: Yellow. Lucky Day: Wednesday. Lucky Numbers: 3, 5. Lucky Stone: Emerald. "
                "Famous Gemini: John F. Kennedy, Bob Dylan, Angelina Jolie, Kanye West, Marilyn Monroe."
            ),
            "cancer": (
                "Cancer (June 21 - July 22) is the first Water sign, ruled by the Moon, a Cardinal sign known for nurturing and emotional depth. "
                "Cancer natives are deeply intuitive, emotional, nurturing, and protective of their loved ones. They have a strong connection to home, family, and the past. "
                "Strengths include tenacity, imagination, loyalty, empathy, and psychic sensitivity. Weaknesses include moodiness, pessimism, clinginess, over-sensitivity, and difficulty letting go of the past. "
                "In career, Cancer excels in nursing, counseling, social work, real estate, culinary arts, hospitality, childcare, history, and marine sciences. They thrive in environments where they can care for others. "
                "Health-wise, they are prone to digestive issues, stomach ulcers, water retention, mood swings, and depression. Emotional health directly affects their physical well-being. "
                "In love, Cancer is deeply emotional, romantic, and seeks security. They are devoted partners who nurture their relationships intensely. They need a partner who provides emotional safety and appreciates their caring nature. "
                "They are most compatible with Scorpio, Pisces, Taurus, and Virgo. Challenging matches include Aries and Libra. "
                "Lucky Color: Silver or White. Lucky Day: Monday. Lucky Numbers: 2, 7. Lucky Stone: Pearl. "
                "Famous Cancer: Princess Diana, Nelson Mandela, Tom Cruise, Meryl Streep, Elon Musk."
            ),
            "leo": (
                "Leo (July 23 - August 22) is a Fire sign ruled by the Sun, a Fixed sign known for confidence and leadership. "
                "Leo natives are confident, generous, dramatic, and natural performers who love to be in the spotlight. They have a warm heart and a regal presence. "
                "Strengths include creativity, passion, generosity, warm-heartedness, loyalty, and natural leadership. Weaknesses include arrogance, stubbornness, self-centeredness, laziness when not appreciated, and a need for constant admiration. "
                "In career, Leo excels in entertainment, acting, management, politics, design, fashion, luxury goods, event planning, and any role where they can shine and inspire others. "
                "Health-wise, they are prone to heart issues, back pain, spinal problems, and circulation issues. They thrive with regular cardiovascular exercise and need to manage stress on their heart. "
                "In love, Leo is romantic, passionate, and extremely generous. They love grand gestures and need a partner who admires them and gives them attention. They are fiercely loyal and protective of their loved ones. "
                "They are most compatible with Aries, Sagittarius, Gemini, and Libra. Challenging matches include Taurus and Scorpio. "
                "Lucky Color: Gold or Orange. Lucky Day: Sunday. Lucky Numbers: 1, 4. Lucky Stone: Ruby. "
                "Famous Leo: Napoleon Bonaparte, Barack Obama, Madonna, Jennifer Lopez, Chris Hemsworth."
            ),
            "virgo": (
                "Virgo (August 23 - September 22) is an Earth sign ruled by Mercury, a Mutable sign known for analysis and service. "
                "Virgo natives are analytical, practical, meticulous, and have an eye for detail that is unmatched. They are perfectionists who strive for excellence in everything. "
                "Strengths include modesty, reliability, hard work, intelligence, analytical thinking, and a helpful nature. Weaknesses include being overly critical (of self and others), perfectionism that leads to paralysis, worry, shyness, and difficulty relaxing. "
                "In career, Virgo excels in healthcare (doctor, nurse, researcher), science, accounting, editing, data analysis, nutrition, fitness, teaching, and any role requiring precision and organization. "
                "Health-wise, they are prone to digestive issues, food sensitivities, anxiety, stress-related disorders, and hypochondria. They benefit from structured routines and clean eating. "
                "In love, Virgo shows love through acts of service and practical help. They are devoted partners who notice every detail. They need a partner who appreciates their thoughtfulness and doesn't mistake their critical nature for lack of love. "
                "They are most compatible with Taurus, Capricorn, Cancer, and Scorpio. Challenging matches include Gemini and Sagittarius. "
                "Lucky Color: Navy Blue or Green. Lucky Day: Wednesday. Lucky Numbers: 5, 8. Lucky Stone: Sapphire. "
                "Famous Virgo: Mother Teresa, Beyonce, Freddie Mercury, Keanu Reeves, Zendaya."
            ),
            "libra": (
                "Libra (September 23 - October 22) is an Air sign ruled by Venus, a Cardinal sign known for balance and harmony. "
                "Libra natives are diplomatic, charming, sociable, and have a natural sense of justice and fairness. They are the peacemakers of the zodiac. "
                "Strengths include cooperation, graciousness, fair-mindedness, artistic taste, diplomacy, and social grace. Weaknesses include indecisiveness, avoidance of confrontation, self-pity, a tendency to be superficial, and people-pleasing. "
                "In career, Libra excels in law, diplomacy, counseling, design, fashion, beauty, art, music, public relations, and any role requiring negotiation and social skills. "
                "Health-wise, they are prone to kidney issues, skin problems, lower back pain, and hormonal imbalances. Stress affects their physical health significantly. "
                "In love, Libra is the ultimate romantic. They seek balanced, harmonious partnerships and thrive when in a relationship. They are charming, affectionate partners who value intellectual connection and aesthetic beauty. They hate conflict and need a partner who can communicate calmly. "
                "They are most compatible with Gemini, Aquarius, Leo, and Sagittarius. Challenging matches include Cancer and Capricorn. "
                "Lucky Color: Pink or Light Blue. Lucky Day: Friday. Lucky Numbers: 6, 9. Lucky Stone: Opal. "
                "Famous Libra: Mahatma Gandhi, John Lennon, Serena Williams, Kim Kardashian, Will Smith."
            ),
            "scorpio": (
                "Scorpio (October 23 - November 21) is a Water sign ruled by Pluto (and traditionally Mars), a Fixed sign known for intensity and transformation. "
                "Scorpio natives are passionate, mysterious, determined, and possess incredible emotional depth. They are the most intense and transformative sign of the zodiac. "
                "Strengths include bravery, loyalty, resourcefulness, passion, determination, and psychic intuition. Weaknesses include jealousy, secretiveness, manipulative tendencies, possessiveness, and a tendency toward vengeance. "
                "In career, Scorpio excels in investigation, detective work, psychology, therapy, research, science, surgery, finance, and any role requiring depth and strategic thinking. "
                "Health-wise, they are prone to reproductive issues, bladder problems, toxins accumulation, and stress-related disorders. They have powerful regenerative abilities. "
                "In love, Scorpio loves with total intensity. They seek deep, transformative, soul-level connections. They are fiercely loyal but require complete trust and honesty. They are passionate and sexually powerful partners. Betrayal is unforgivable to them. "
                "They are most compatible with Cancer, Pisces, Virgo, and Capricorn. Challenging matches include Leo and Aquarius. "
                "Lucky Color: Maroon or Black. Lucky Day: Tuesday. Lucky Numbers: 8, 11. Lucky Stone: Topaz. "
                "Famous Scorpio: Marie Curie, Pablo Picasso, Julia Roberts, Leonardo DiCaprio, Bill Gates."
            ),
            "sagittarius": (
                "Sagittarius (November 22 - December 21) is a Fire sign ruled by Jupiter, a Mutable sign known for adventure and philosophy. "
                "Sagittarius natives are adventurous, optimistic, honest, and love freedom above all. They are the explorers and philosophers of the zodiac, always seeking higher meaning. "
                "Strengths include generosity, idealism, humor, open-mindedness, honesty, and a great sense of adventure. Weaknesses include impatience, tactlessness, restlessness, over-promising, and commitment issues. "
                "In career, Sagittarius excels in travel, tourism, education, publishing, sports, law, philosophy, international business, and any field allowing freedom and exploration. "
                "Health-wise, they are prone to hip issues, sciatica, over-exertion injuries, liver problems, and weight gain from overindulgence. They need regular outdoor exercise. "
                "In love, Sagittarius needs a partner who shares their love for adventure, travel, and intellectual exploration. They are honest to a fault and value freedom in relationships. They need space and get bored with routine. "
                "They are most compatible with Aries, Leo, Gemini, and Aquarius. Challenging matches include Virgo and Pisces. "
                "Lucky Color: Purple or Royal Blue. Lucky Day: Thursday. Lucky Numbers: 3, 7. Lucky Stone: Turquoise. "
                "Famous Sagittarius: Winston Churchill, Walt Disney, Taylor Swift, Brad Pitt, Mark Twain."
            ),
            "capricorn": (
                "Capricorn (December 22 - January 19) is an Earth sign ruled by Saturn, a Cardinal sign known for discipline and ambition. "
                "Capricorn natives are disciplined, ambitious, practical, and responsible. They are the builders and achievers of the zodiac, climbing steadily toward their goals. "
                "Strengths include patience, hard work, self-control, wisdom, responsibility, and strategic thinking. Weaknesses include pessimism, rigidity, unforgiving nature, workaholism, and emotional reserve. "
                "In career, Capricorn excels in business, finance, banking, engineering, management, law, politics, real estate, and any field requiring long-term planning and discipline. "
                "Health-wise, they are prone to knee issues, bone problems, joint pain, dental issues, and stress-related conditions. They need to balance work with rest. "
                "In love, Capricorn is serious and cautious about relationships. They take time to open up but are deeply loyal once committed. They show love through providing security and stability. They need a partner who respects their ambitions and is equally driven. "
                "They are most compatible with Taurus, Virgo, Cancer, and Scorpio. Challenging matches include Aries and Libra. "
                "Lucky Color: Brown or Dark Green. Lucky Day: Saturday. Lucky Numbers: 4, 8. Lucky Stone: Garnet. "
                "Famous Capricorn: Isaac Newton, Martin Luther King Jr., Michelle Obama, Denzel Washington, Kate Middleton."
            ),
            "aquarius": (
                "Aquarius (January 20 - February 18) is an Air sign ruled by Uranus, a Fixed sign known for innovation and humanitarianism. "
                "Aquarius natives are innovative, independent, humanitarian, and eccentric. They think outside the box and are often ahead of their time. "
                "Strengths include progressiveness, originality, friendliness, idealism, intellectual brilliance, and strong social conscience. Weaknesses include emotional detachment, unpredictability, rebelliousness, stubbornness, and difficulty with intimacy. "
                "In career, Aquarius excels in technology, science, engineering, aviation, social work, activism, astrology, inventing, and any field that allows them to innovate and help humanity. "
                "Health-wise, they are prone to circulation issues, ankle problems, varicose veins, and nerve disorders. They benefit from group exercise and outdoor activities. "
                "In love, Aquarius needs intellectual connection and unconventional relationships. They value friendship as the foundation of love. They need a partner who respects their independence and shares their vision for the future. They are loyal but need space. "
                "They are most compatible with Gemini, Libra, Aries, and Sagittarius. Challenging matches include Taurus and Scorpio. "
                "Lucky Color: Electric Blue or Silver. Lucky Day: Saturday. Lucky Numbers: 4, 11. Lucky Stone: Amethyst. "
                "Famous Aquarius: Thomas Edison, Abraham Lincoln, Oprah Winfrey, Cristiano Ronaldo, Bob Marley."
            ),
            "pisces": (
                "Pisces (February 19 - March 20) is a Water sign ruled by Neptune, a Mutable sign known for compassion and creativity. "
                "Pisces natives are compassionate, artistic, intuitive, and deeply spiritual. They are the dreamers and mystics of the zodiac, with a profound connection to the unseen. "
                "Strengths include imagination, compassion, selflessness, musical talent, intuition, and adaptability. Weaknesses include escapist tendencies, being overly trusting, melancholia, addictive tendencies, and difficulty with boundaries. "
                "In career, Pisces excels in art, music, dance, film, photography, healing, spirituality, social work, nursing, marine biology, and any field requiring creativity and empathy. "
                "Health-wise, they are prone to foot issues, sleep disorders, allergies, addictions, and psychosomatic conditions. They need regular alone time and creative outlets. "
                "In love, Pisces is the ultimate romantic dreamer. They seek soulmate connections and unconditional love. They are incredibly giving and intuitive partners who can sense their partner's needs. They need a partner who provides stability and appreciates their sensitive nature. "
                "They are most compatible with Cancer, Scorpio, Taurus, and Capricorn. Challenging matches include Gemini and Sagittarius. "
                "Lucky Color: Sea Green or Mauve. Lucky Day: Thursday. Lucky Numbers: 3, 7. Lucky Stone: Jade or Moonstone. "
                "Famous Pisces: Albert Einstein, Steve Jobs, Rihanna, Kurt Cobain, Elizabeth Taylor."
            )
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
        
        greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening", "good afternoon"]
        if any(g in msg_lower for g in greetings):
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
        
        if "house" in msg_lower and ("birth" in msg_lower or "chart" in msg_lower or "kundli" in msg_lower):
            return {"response": "In astrology, the 12 houses represent different areas of life: 1st House (Self, personality, physical appearance - Aries). 2nd House (Wealth, family, speech, values - Taurus). 3rd House (Communication, siblings, courage, short journeys - Gemini). 4th House (Home, mother, emotions, property - Cancer). 5th House (Creativity, children, romance, speculation - Leo). 6th House (Health, service, enemies, daily work - Virgo). 7th House (Marriage, partnerships, contracts, open enemies - Libra). 8th House (Transformation, death, inheritance, occult - Scorpio). 9th House (Higher learning, philosophy, luck, long journeys - Sagittarius). 10th House (Career, reputation, authority, father - Capricorn). 11th House (Gains, friendships, aspirations, social networks - Aquarius). 12th House (Loss, spirituality, isolation, foreign lands - Pisces). Planets placed in each house modify how that life area operates for you."}
        
        if "aspect" in msg_lower:
            return {"response": "Astrological aspects are angles between planets that create specific energetic relationships. Major aspects: Conjunction (0°, planets merge energies). Sextile (60°, harmonious opportunity). Square (90°, tension and growth). Trine (120°, natural flow and talent). Opposition (180°, polarity and balance). Minor aspects: Semi-sextile (30°), Quincunx/Inconjunct (150°), Semi-square (45°), Sesquiquadrate (135°). In KP astrology, aspect rules differ: all planets aspect the 7th house from themselves, plus Mars aspects 4th and 8th, Jupiter aspects 5th and 9th, Saturn aspects 3rd and 10th. Rahu and Ketu also aspect 5th and 9th."}
        
        return {"response": "I have detailed knowledge about all 12 zodiac signs including personality traits, strengths, weaknesses, career paths, health tendencies, love and relationship patterns, lucky attributes, and famous personalities. You can also ask about numerology (including Life Path Numbers), tarot cards (Major and Minor Arcana meanings), planets and their significations, horoscopes, KP astrology (sub-lord theory, significators), Vedic astrology (Nakshatras, Dasha systems, Yogas), birth chart houses, or astrological aspects. Try asking specific questions like: 'Tell me about Pisces in detail', 'What career suits a Gemini?', 'Who is Scorpio compatible with?', 'Explain planetary aspects', or 'What are Nakshatras?'"}
        
    except Exception as e:
        import traceback
        return {"response": f"AI Error: {str(e)}", "trace": traceback.format_exc()}
