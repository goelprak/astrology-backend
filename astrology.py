from datetime import datetime
from typing import Optional, Dict, List, Any
import pytz
import math

def sin_rad(degrees):
    return math.sin(degrees)

def cos_rad(degrees):
    return math.cos(degrees)

def tan(degrees):
    return math.tan(degrees)

def atan_rad(x):
    return math.atan(x)

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
    "Uranus", "Neptune", "Pluto", "North Node", "Chiron"
]

ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
}

QUALITIES = {
    "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
    "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
    "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable"
}

PLANET_RULERS = {
    "Sun": "Leo", "Moon": "Cancer", "Mercury": ["Gemini", "Virgo"],
    "Venus": ["Taurus", "Libra"], "Mars": ["Aries", "Scorpio"],
    "Jupiter": ["Sagittarius", "Pisces"], "Saturn": ["Capricorn", "Aquarius"],
    "Uranus": "Aquarius", "Neptune": "Pisces", "Pluto": "Scorpio"
}

def get_zodiac_sign(degree: float) -> str:
    index = int(degree // 30) % 12
    return ZODIAC_SIGNS[index]

def get_sign_degree(degree: float) -> tuple:
    sign_index = int(degree // 30) % 12
    sign_degree = degree % 30
    return ZODIAC_SIGNS[sign_index], int(sign_degree), int((sign_degree % 1) * 60)

def calculate_aspects(planets1: Dict[str, float], planets2: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
    aspects = []
    orb = 8 if planets2 else 6
    
    target_planets = planets2 if planets2 else planets1
    
    for p1, deg1 in planets1.items():
        for p2, deg2 in target_planets.items():
            if p1 == p2:
                continue
            
            diff = abs(deg1 - deg2)
            if diff > 180:
                diff = 360 - diff
            
            aspect_types = [
                (0, "Conjunction", 0),
                (60, "Sextile", 6),
                (90, "Square", 8),
                (120, "Trine", 8),
                (180, "Opposition", 8)
            ]
            
            for asp_deg, asp_name, asp_orb in aspect_types:
                if abs(diff - asp_deg) <= orb:
                    aspects.append({
                        "planet1": p1,
                        "planet2": p2,
                        "aspect": asp_name,
                        "degree": round(diff, 2),
                        "angle": asp_deg
                    })
                    break
    
    return aspects

def calculate_compatibility(chart1: Dict, chart2: Dict) -> Dict[str, Any]:
    score = 0
    max_score = 100
    
    sun1 = chart1.get("Sun", {}).get("degree", 0)
    sun2 = chart2.get("Sun", {}).get("degree", 0)
    
    sun_diff = abs(sun1 - sun2)
    if sun_diff > 180:
        sun_diff = 360 - sun_diff
    
    if sun_diff <= 30:
        score += 25
    elif sun_diff <= 60:
        score += 15
    elif sun_diff <= 90:
        score += 5
    
    moon1 = chart1.get("Moon", {}).get("degree", 0)
    moon2 = chart2.get("Moon", {}).get("degree", 0)
    
    moon_diff = abs(moon1 - moon2)
    if moon_diff > 180:
        moon_diff = 360 - moon_diff
    
    if moon_diff <= 30:
        score += 25
    elif moon_diff <= 60:
        score += 15
    elif moon_diff <= 90:
        score += 5
    
    aspects = calculate_aspects(
        {k: v["degree"] for k, v in chart1.items()},
        {k: v["degree"] for k, v in chart2.items()}
    )
    
    trine_count = sum(1 for a in aspects if a["aspect"] == "Trine")
    conjunction_count = sum(1 for a in aspects if a["aspect"] == "Conjunction")
    square_count = sum(1 for a in aspects if a["aspect"] == "Square")
    
    score += min(trine_count * 5, 20)
    score += min(conjunction_count * 3, 15)
    score -= min(square_count * 2, 10)
    
    sign1 = get_zodiac_sign(sun1)
    sign2 = get_zodiac_sign(sun2)
    
    if ELEMENTS.get(sign1) == ELEMENTS.get(sign2):
        score += 10
    
    if QUALITIES.get(sign1) == QUALITIES.get(sign2):
        score += 5
    
    score = max(0, min(score, 100))
    
    descriptions = {
        (0, 30): "Challenging - requires work but can grow together",
        (30, 50): "Moderate - some natural harmony with areas to develop",
        (50, 70): "Good - solid foundation for a lasting connection",
        (70, 100): "Excellent - strong natural compatibility"
    }
    
    description = "Challenging connection"
    for (low, high), desc in descriptions.items():
        if low <= score < high:
            description = desc
            break
    
    return {
        "score": score,
        "description": description,
        "sun_aspect": "Compatible" if sun_diff <= 90 else "Challenging",
        "moon_aspect": "Compatible" if moon_diff <= 90 else "Challenging",
        "element_match": ELEMENTS.get(sign1) == ELEMENTS.get(sign2),
        "aspect_summary": {
            "trines": trine_count,
            "conjunctions": conjunction_count,
            "squares": square_count
        }
    }

def generate_daily_horoscope(sign: str, date: datetime) -> Dict[str, Any]:
    import hashlib
    
    sign_index = ZODIAC_SIGNS.index(sign) if sign in ZODIAC_SIGNS else 0
    
    seed = f"{sign}{date.year}{date.month}{date.day}"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    horoscopes = {
        "Aries": [
            "A powerful new idea emerges today. Trust your instincts and take that first step.",
            "Your energy is magnetic today. Others are drawn to your confidence.",
            "Focus on personal goals. The cosmos supports your ambitions.",
            "A creative breakthrough awaits. Let your imagination guide you.",
            "Adventure calls! Something exciting is just around the corner."
        ],
        "Taurus": [
            "Financial matters come into focus. Smart decisions lead to gains.",
            "Your patience pays off. Good things come to those who wait.",
            "Focus on stability and security. Build lasting foundations.",
            "Indulge in life's pleasures, but maintain balance.",
            "Connect with nature to find inner peace and clarity."
        ],
        "Gemini": [
            "Communication flows easily. Share your brilliant ideas.",
            "Curiosity leads to discovery. Explore something new today.",
            "Social connections bring opportunities. Reach out to others.",
            "Mental sharpness peaks. Tackle complex problems with ease.",
            "Express yourself through writing or conversation."
        ],
        "Cancer": [
            "Home and family take priority. Nurture those you love.",
            "Your intuition is especially strong. Trust your gut feelings.",
            "Emotional connections deepen. Vulnerability is strength.",
            "Create a peaceful sanctuary. Your space reflects your soul.",
            "Trust in the process. Things are falling into place."
        ],
        "Leo": [
            "Your radiance shines bright. Others notice your leadership.",
            "Creativity flourishes. Let your inner star shine.",
            "Romance and fun are highlighted. Enjoy life's pleasures.",
            "Self-expression is key. Share your unique gifts with world.",
            "Generosity returns multiplied. Give freely and receive gladly."
        ],
        "Virgo": [
            "Health and wellness take focus. Small improvements add up.",
            "Service to others brings fulfillment. Help where you can.",
            "Detail work pays off. Your precision is your superpower.",
            "Organization brings peace. Tidy your space, tidy your mind.",
            "Practical wisdom guides your path. Trust the process."
        ],
        "Libra": [
            "Relationships need attention. Balance give and take.",
            "Beauty and harmony call to you. Create something lovely.",
            "Partnerships flourish. Collaboration brings success.",
            "Justice is on your side. Stand up for what's right.",
            "Peace and equilibrium are your superpowers today."
        ],
        "Scorpio": [
            "Transformation calls. Let go of what no longer serves you.",
            "Intensity deepens connections. Vulnerability builds trust.",
            "Your determination is unstoppable. Keep pushing forward.",
            "Secrets revealed. Truth sets you free.",
            "Emotional depth is your gift. Embrace it fully."
        ],
        "Sagittarius": [
            "Adventure awaits! Expand your horizons today.",
            "Philosophy and truth call to you. Seek wisdom.",
            "Optimism attracts opportunities. Believe in possibilities.",
            "Travel and exploration call. Answer the call of wanderlust.",
            "Share your knowledge. Teaching illuminates your path."
        ],
        "Capricorn": [
            "Career ambitions advance. Your hard work is noticed.",
            "Responsibility calls, but you handle it gracefully.",
            "Long-term planning pays off. Think strategically.",
            "Authority respects your dedication. Build your legacy.",
            "Structure brings freedom. Discipline creates possibility."
        ],
        "Aquarius": [
            "Innovation sparks interest. Your unique ideas shine.",
            "Community connections expand. Find your tribe.",
            "Humanitarian impulses rise. Make a difference.",
            "Originality is your gift. Don't follow - lead.",
            "Future visions inspire. Dream big and act boldly."
        ],
        "Pisces": [
            "Intuition flows strong. Trust your inner wisdom.",
            "Creativity and dreams merge. Art awaits expression.",
            "Compassion connects you to others. Spread kindness.",
            "Spiritual insights arise. Meditate and reflect.",
            "Let go and flow. Release to find peace."
        ]
    }
    
    index = (hash_val % 5 + date.weekday()) % len(horoscopes.get(sign, horoscopes["Aries"]))
    prediction = horoscopes.get(sign, horoscopes["Aries"])[index]
    
    luck_factors = {
        "lucky_number": (hash_val % 99) + 1,
        "lucky_color": ["Red", "Blue", "Green", "Gold", "Purple", "Silver"][hash_val % 6],
        "lucky_day": ["Monday", "Thursday", "Saturday"][hash_val % 3]
    }
    
    categories = ["Career", "Love", "Health", "Finance", "Social"]
    category_index = (hash_val % 5 + date.weekday()) % 5
    
    return {
        "sign": sign,
        "date": date.strftime("%Y-%m-%d"),
        "prediction": prediction,
        "mood": ["Happy", "Energetic", "Calm", "Reflective", "Creative"][hash_val % 5],
        "lucky_number": luck_factors["lucky_number"],
        "lucky_color": luck_factors["lucky_color"],
        "lucky_day": luck_factors["lucky_day"],
        "focus_area": categories[category_index]
    }

def calculate_natal_chart(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(f"{birth_date}T{birth_time}")
    except:
        return {"error": "Invalid date/time format. Use ISO format: YYYY-MM-DD HH:MM"}
    
    try:
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt) if dt.tzinfo is None else dt
    except:
        dt = pytz.utc.localize(dt)
    
    jd = datetime_to_julian_day(dt)
    
    planets = calculate_planet_positions(jd, latitude, longitude)
    
    asc_degree = calculate_ascendant(jd, latitude, longitude)
    mc_degree = calculate_midheaven(jd, longitude)
    
    sun_sign = get_zodiac_sign(planets.get("Sun", 0))
    moon_sign = get_zodiac_sign(planets.get("Moon", 0))
    asc_sign = get_zodiac_sign(asc_degree)
    
    chart = {
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "rising_sign": asc_sign,
        "ascendant_degree": round(asc_degree, 2),
        "midheaven_degree": round(mc_degree, 2),
        "planets": {k: {"degree": round(v, 2), "sign": get_zodiac_sign(v)} for k, v in planets.items()},
        "houses": calculate_houses(asc_degree, mc_degree, latitude)
    }
    
    return chart

def datetime_to_julian_day(dt: datetime) -> float:
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return jd

def calculate_ascendant(jd: float, latitude: float, longitude: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    L0 = L0 % 360
    
    omega = 125.0445479 - 1934.1362891 * T + 0.0020754 * T * T
    epsilon = 23.439291 - 0.0130042 * T - 0.00000016 * T * T + 0.000000504 * T * T * T
    epsilon_rad = epsilon * 3.14159265358979 / 180
    
    obliquity_correction = epsilon + 0.00256 * cos_rad(omega * 3.14159265358979 / 180)
    obliquity_rad = obliquity_correction * 3.14159265358979 / 180
    
    GMST = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T * T * T / 38710000.0
    GMST = GMST % 360
    
    LST = (GMST + longitude) % 360
    LST_rad = LST * 3.14159265358979 / 180
    
    tan_A = -cos_rad(LST_rad) / (sin_rad(LST_rad) * sin_rad(obliquity_rad) + tan(latitude * 3.14159265358979 / 180) * cos_rad(obliquity_rad))
    A = atan_rad(tan_A)
    
    asc = (A * 180 / 3.14159265358979 + 180) % 360
    return asc

def calculate_midheaven(jd: float, longitude: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    L0 = L0 % 360
    
    omega = 125.0445479 - 1934.1362891 * T + 0.0020754 * T * T
    epsilon = 23.439291 - 0.0130042 * T - 0.00000016 * T * T + 0.000000504 * T * T * T
    
    obliquity_correction = epsilon + 0.00256 * cos_rad(omega * 3.14159265358979 / 180)
    obliquity_rad = obliquity_correction * 3.14159265358979 / 180
    
    GMST = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T * T * T / 38710000.0
    GMST = (GMST + longitude) % 360
    
    MC = (GMST - L0) % 360
    if MC < 0:
        MC += 360
    
    return MC

def calculate_planet_positions(jd: float, latitude: float, longitude: float) -> Dict[str, float]:
    T = (jd - 2451545.0) / 36525.0
    
    planets = {}
    
    sun_mean_anomaly = 357.52911 + 35999.05029 * T - 0.0001536 * T * T
    sun_mean_longitude = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    earth_orbit_eccentricity = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T
    
    sun_true_anomaly = sun_mean_anomaly + 1.914602 - 0.004817 * T - 0.000014 * T * T
    sun_equation_of_center = (1.914602 - 0.004817 * T - 0.000014 * T * T) * sin_rad(sun_mean_anomaly * 3.14159265358979 / 180) + \
                              (0.019993 - 0.000101 * T) * sin_rad(2 * sun_mean_anomaly * 3.14159265358979 / 180) + \
                              0.000289 * sin_rad(3 * sun_mean_anomaly * 3.14159265358979 / 180)
    
    sun_true_longitude = (sun_mean_longitude + sun_equation_of_center) % 360
    sun_distance = 1.000001017 * (1 - earth_orbit_eccentricity * earth_orbit_eccentricity) / (1 + earth_orbit_eccentricity * cos_rad(sun_true_anomaly * 3.14159265358979 / 180))
    
    planets["Sun"] = sun_true_longitude
    
    moon_mean_longitude = 218.3164477 + 481267.88123421 * T - 0.0015786 * T * T
    moon_mean_elongation = 297.8501921 + 445267.1114034 * T - 0.0018819 * T * T
    moon_mean_anomaly = 134.9633964 + 477198.8675055 * T + 0.0087414 * T * T
    moon_argument_of_latitude = 93.272095 + 483202.0175233 * T - 0.0036539 * T * T
    
    moon_longitude = moon_mean_longitude + 6.289 * sin_rad(moon_mean_anomaly * 3.14159265358979 / 180)
    moon_latitude = 5.128 * sin_rad(moon_argument_of_latitude * 3.14159265358979 / 180)
    moon_distance = 385000.566
    
    planets["Moon"] = moon_longitude % 360
    
    mercury_mean_longitude = 252.250905 + 149472.67411175 * T + 0.000160 * T * T - 0.000001 * T * T * T
    mercury_mean_anomaly = 174.794864 + 4.0923349 * T
    
    venus_mean_longitude = 181.979801 + 58517.8156760 * T + 0.000001 * T * T
    venus_mean_anomaly = 50.115444 + 1.3921973 * T
    
    mars_mean_longitude = 355.433275 + 19140.2993313 * T + 0.000001 * T * T
    mars_mean_anomaly = 19.412419 + 0.5240211 * T
    
    jupiter_mean_longitude = 34.351519 + 3034.9061279 * T + 0.000004 * T * T
    jupiter_mean_anomaly = 20.020187 + 0.0830853 * T + 0.000033 * T * T
    
    saturn_mean_longitude = 49.954248 + 1222.1138488 * T + 0.000004 * T * T
    saturn_mean_anomaly = 317.020509 + 0.9924440 * T + 0.000002 * T * T
    
    planets["Mercury"] = (mercury_mean_longitude + 0.083 * sin_rad(mercury_mean_anomaly * 3.14159265358979 / 180)) % 360
    planets["Venus"] = (venus_mean_longitude + 0.723 * sin_rad(venus_mean_anomaly * 3.14159265358979 / 180)) % 360
    planets["Mars"] = (mars_mean_longitude + 0.631 * sin_rad(mars_mean_anomaly * 3.14159265358979 / 180)) % 360
    planets["Jupiter"] = (jupiter_mean_longitude + 5.555 * sin_rad(jupiter_mean_anomaly * 3.14159265358979 / 180)) % 360
    planets["Saturn"] = (saturn_mean_longitude + 5.102 * sin_rad(saturn_mean_anomaly * 3.14159265358979 / 180)) % 360
    
    for name, mean_long in [
        ("Uranus", 96.661867 + 1919.2858945 * T),
        ("Neptune", 173.005615 + 841.3301066 * T),
        ("Pluto", 238.956785 + 144.96 * T)
    ]:
        planets[name] = mean_long % 360
    
    north_node_mean = 125.0445479 - 1934.1362891 * T
    planets["North Node"] = north_node_mean % 360
    
    chiron_mean = 209.0 + 7.0 * T
    planets["Chiron"] = chiron_mean % 360
    
    return planets

def calculate_houses(asc_degree: float, mc_degree: float, latitude: float) -> Dict[str, Dict]:
    house_cusp_1 = asc_degree
    house_cusp_10 = mc_degree
    
    house_cusp_7 = (house_cusp_1 + 180) % 360
    house_cusp_4 = (house_cusp_10 + 180) % 360
    
    diff = (house_cusp_10 - house_cusp_1) % 360
    if diff > 180:
        diff -= 360
    
    house_cusp_11 = (house_cusp_1 + diff * 0.75) % 360
    house_cusp_12 = (house_cusp_1 + diff * 0.5) % 360
    house_cusp_2 = (house_cusp_1 + diff * 0.25) % 360
    house_cusp_3 = (house_cusp_1 + diff * 0.1) % 360
    house_cusp_5 = (house_cusp_10 + diff * 0.1 + 180) % 360
    house_cusp_6 = (house_cusp_10 + diff * 0.25 + 180) % 360
    house_cusp_8 = (house_cusp_10 + diff * 0.5 + 180) % 360
    house_cusp_9 = (house_cusp_10 + diff * 0.75 + 180) % 360
    
    return {
        "1": {"cusp": round(house_cusp_1, 2), "sign": get_zodiac_sign(house_cusp_1)},
        "2": {"cusp": round(house_cusp_2, 2), "sign": get_zodiac_sign(house_cusp_2)},
        "3": {"cusp": round(house_cusp_3, 2), "sign": get_zodiac_sign(house_cusp_3)},
        "4": {"cusp": round(house_cusp_4, 2), "sign": get_zodiac_sign(house_cusp_4)},
        "5": {"cusp": round(house_cusp_5, 2), "sign": get_zodiac_sign(house_cusp_5)},
        "6": {"cusp": round(house_cusp_6, 2), "sign": get_zodiac_sign(house_cusp_6)},
        "7": {"cusp": round(house_cusp_7, 2), "sign": get_zodiac_sign(house_cusp_7)},
        "8": {"cusp": round(house_cusp_8, 2), "sign": get_zodiac_sign(house_cusp_8)},
        "9": {"cusp": round(house_cusp_9, 2), "sign": get_zodiac_sign(house_cusp_9)},
        "10": {"cusp": round(house_cusp_10, 2), "sign": get_zodiac_sign(house_cusp_10)},
        "11": {"cusp": round(house_cusp_11, 2), "sign": get_zodiac_sign(house_cusp_11)},
        "12": {"cusp": round(house_cusp_12, 2), "sign": get_zodiac_sign(house_cusp_12)}
    }

def calculate_transits(current_date: str, latitude: float, longitude: float) -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(current_date)
    except:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    jd = datetime_to_julian_day(dt)
    
    transits = calculate_planet_positions(jd, latitude, longitude)
    
    result = {}
    for planet, degree in transits.items():
        sign = get_zodiac_sign(degree)
        sign_degree, minutes = divmod(degree % 30, 1)
        result[planet] = {
            "degree": round(degree, 2),
            "sign": sign,
            "sign_degree": int(sign_degree),
            "sign_minute": int(minutes * 60),
            "element": ELEMENTS.get(sign, "Unknown"),
            "quality": QUALITIES.get(sign, "Unknown")
        }
    
    return result

def calculate_numerology(name: str, birth_date: str) -> Dict[str, Any]:
    def reduce_to_single(num):
        while num > 9 and num not in [11, 22, 33]:
            num = sum(int(d) for d in str(num))
        return num
    
    name_digits = ''.join(c for c in name.upper() if c.isalpha())
    name_values = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 
                   'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
                   'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 
                   'Y': 7, 'Z': 8}
    
    vowels = 'AEIOU'
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    
    birth_digits = ''.join(c for c in birth_date if c.isdigit())
    birth_parts = birth_date.split('-')
    day = int(birth_parts[2]) if len(birth_parts) > 2 else 1
    month = int(birth_parts[1]) if len(birth_parts) > 1 else 1
    year = int(birth_parts[0]) if len(birth_parts) > 0 else 2000
    
    life_path = reduce_to_single(sum(int(c) for c in birth_digits))
    destiny = reduce_to_single(sum(name_values.get(c, 0) for c in name_digits))
    soul_urge = reduce_to_single(sum(name_values.get(c, 0) for c in name_digits if c in vowels))
    personality = reduce_to_single(sum(name_values.get(c, 0) for c in name_digits if c in consonants))
    birth_day = reduce_to_single(day)
    
    maturity = reduce_to_single(life_path + destiny)
    
    personal_year = reduce_to_single(sum(int(c) for c in str(year)) + month + day)
    personal_month = reduce_to_single(personal_year + (datetime.now().month))
    personal_day = reduce_to_single(personal_year + (datetime.now().day))
    
    name_sum = sum(name_values.get(c, 0) for c in name_digits)
    name_number = reduce_to_single(name_sum)
    
    first_letter = name.upper().strip()[0] if name.strip() else 'A'
    cornerstone = reduce_to_single(name_values.get(first_letter, 1))
    
    last_letter = name.upper().strip()[-1] if name.strip() else 'A'
    capstone = reduce_to_single(name_values.get(last_letter, 1))
    
    balance = reduce_to_single(name_values.get(name.upper().split()[0][0] if name.split() else 'A', 1))
    
    challenge_1 = reduce_to_single(abs(day - month))
    challenge_2 = reduce_to_single(abs(day - year % 100))
    challenge_3 = reduce_to_single(abs(month - year % 100))
    challenge_4 = reduce_to_single(challenge_1 + challenge_3)
    
    name_parts = name.upper().split()
    if len(name_parts) >= 2:
        soul_urge_1 = reduce_to_single(sum(name_values.get(c, 0) for c in name_parts[0] if c in vowels))
        soul_urge_2 = reduce_to_single(sum(name_values.get(c, 0) for c in name_parts[-1] if c in vowels))
    else:
        soul_urge_1 = soul_urge
        soul_urge_2 = 0
    
    life_path_meanings = {
        1: "Leader, independent, innovative, pioneering - You are meant to lead and create new paths.",
        2: "Diplomat, cooperative, harmonious, sensitive - You bring peace and balance to situations.",
        3: "Creative, expressive, joyful, optimistic - You are here to spread joy and creativity.",
        4: "Builder, practical, stable, disciplined - You create lasting foundations through hard work.",
        5: "Explorer, freedom-loving, dynamic, versatile - You are meant to experience and teach freedom.",
        6: "Nurturer, responsible, protective, domestic - You find purpose in caring for others.",
        7: "Seeker, introspective, analytical, spiritual - You are here to find inner wisdom.",
        8: "Achiever, ambitious, materialistic, powerful - You are meant to achieve material success.",
        9: "Humanitarian, compassionate, generous, wise - You are here to serve humanity.",
        11: "Visionary, intuitive, inspirational, master number - You are an old soul with special gifts.",
        22: "Master builder, practical dreamer, great potential - You can create great things on earth.",
        33: "Master teacher, healing, compassion, enlightened - You are here to uplift humanity."
    }

    destiny_meanings = {
        1: "Your destiny is to lead and pioneer. You will inspire others through your independence.",
        2: "Your destiny involves partnerships and diplomacy. You bring harmony to relationships.",
        3: "Your destiny is creative expression. You will bring joy and inspiration to others.",
        4: "Your destiny is to build lasting structures. You create stability and order.",
        5: "Your destiny is freedom and adventure. You will inspire others to embrace change.",
        6: "Your destiny is nurturing and responsibility. You find fulfillment in family and service.",
        7: "Your destiny is spiritual wisdom. You are meant to seek and share inner truths.",
        8: "Your destiny is power and achievement. You will attain material and financial success.",
        9: "Your destiny is humanitarian service. You are meant to help and heal others."
    }

    soul_urge_meanings = {
        1: "Your soul craves independence and self-expression. You need to be your own person.",
        2: "Your soul desires harmony and partnership. You need meaningful relationships.",
        3: "Your soul seeks joy and creativity. You need to express yourself freely.",
        4: "Your soul wants security and stability. You need a solid foundation in life.",
        5: "Your soul demands freedom and adventure. You need to experience life fully.",
        6: "Your soul yearns for love and family. You need to care for and be cared for.",
        7: "Your soul seeks truth and understanding. You need time for introspection.",
        8: "Your soul desires success and recognition. You need to achieve and accomplish.",
        9: "Your soul wants to serve humanity. You need to give and receive compassion."
    }

    personality_meanings = {
        1: "Others see you as a confident, independent leader.",
        2: "Others see you as a cooperative, diplomatic mediator.",
        3: "Others see you as a creative, joyful communicator.",
        4: "Others see you as a reliable, practical organizer.",
        5: "Others see you as an adventurous, versatile explorer.",
        6: "Others see you as a caring, responsible nurturer.",
        7: "Others see you as a wise, mysterious thinker.",
        8: "Others see you as a powerful, ambitious achiever.",
        9: "Others see you as a generous, compassionate humanitarian."
    }

    personal_year_meanings = {
        1: "This is a year of new beginnings and independence.",
        2: "This is a year of partnerships and cooperation.",
        3: "This is a year of creativity and self-expression.",
        4: "This is a year of hard work and building foundations.",
        5: "This is a year of change and freedom.",
        6: "This is a year of family and responsibilities.",
        7: "This is a year of introspection and spiritual growth.",
        8: "This is a year of achievement and recognition.",
        9: "This is a year of completion and humanitarian service."
    }

    return {
        "life_path": life_path,
        "life_path_meaning": life_path_meanings.get(life_path, "Your path is unique"),
        "destiny": destiny,
        "destiny_meaning": destiny_meanings.get(destiny, "Your destiny is unique"),
        "soul_urge": soul_urge,
        "soul_urge_meaning": soul_urge_meanings.get(soul_urge, "Your soul's desire is unique"),
        "personality": personality,
        "personality_meaning": personality_meanings.get(personality, "Your personality is unique"),
        "birth_day": birth_day,
        "birth_day_meaning": f"Birth Day {birth_day} gives you natural talent and practical abilities.",
        
        "maturity": maturity,
        "maturity_meaning": f"Your maturity number is {maturity}. This represents your later life purpose.",
        
        "personal_year": personal_year,
        "personal_year_meaning": personal_year_meanings.get(personal_year, "This is your personal year."),
        
        "personal_month": personal_month,
        "personal_day": personal_day,
        
        "name_number": name_number,
        "name_number_meaning": f"Your name adds up to {name_number}, influencing how you present yourself.",
        
        "cornerstone": cornerstone,
        "cornerstone_meaning": f"The first letter '{name.strip()[0].upper() if name.strip() else 'A'}' gives you {['strong leadership', 'diplomatic nature', 'creative expression', 'practical stability', 'adventurous spirit', 'nurturing heart', 'deep wisdom', 'powerful drive', 'compassionate soul'][cornerstone-1]} qualities.",
        
        "capstone": capstone,
        "capstone_meaning": f"Your last letter indicates how you finish things - you are {['determined', 'harmonious', 'optimistic', 'reliable', 'flexible', 'caring', 'thoughtful', 'ambitious', 'generous'][capstone-1]} in your approach.",
        
        "balance": balance,
        "balance_meaning": f"Your balance number is {balance}, representing your inner harmony.",
        
        "challenges": {
            "first": challenge_1,
            "second": challenge_2,
            "third": challenge_3,
            "fourth": challenge_4
        },
        
        "soul_urge_doubles": {
            "first_name": soul_urge_1,
            "last_name": soul_urge_2
        },
        
        "power_number": reduce_to_single(life_path + destiny),
        "yearly_theme": f"{personal_year} - {personal_year_meanings.get(personal_year, 'Growth year')}"
    }

def get_planet_ruler(sign: str) -> str:
    rulers = {
        "Aries": "Mars", "Scorpio": "Pluto", "Leo": "Sun", "Cancer": "Moon",
        "Taurus": "Venus", "Libra": "Venus", "Virgo": "Mercury", "Gemini": "Mercury",
        "Capricorn": "Saturn", "Aquarius": "Uranus", "Sagittarius": "Jupiter", "Pisces": "Neptune"
    }
    return rulers.get(sign, "Unknown")

def generate_detailed_analysis(chart: Dict) -> Dict[str, Any]:
    sun_sign = chart.get("sun_sign", "")
    moon_sign = chart.get("moon_sign", "")
    rising_sign = chart.get("rising_sign", "")
    planets = chart.get("planets", {})
    
    strengths = []
    challenges = []
    career_indications = []
    relationship_indications = []
    health_indications = []
    
    if sun_sign in ["Aries", "Leo", "Sagittarius"]:
        strengths.append("Natural leadership abilities and creative energy")
    if moon_sign in ["Cancer", "Scorpio", "Pisces"]:
        strengths.append("Deep emotional intuition and sensitivity")
    if rising_sign in ["Capricorn", "Virgo", "Taurus"]:
        strengths.append("Strong practical approach and determination")
    
    if planets.get("Sun", {}).get("sign") in ["Leo"]:
        career_indications.append("Creative fields, performing arts, management roles")
    if planets.get("Jupiter", {}).get("sign") in ["Sagittarius", "Pisces"]:
        career_indications.append("Teaching, travel, higher education, philosophy")
    if planets.get("Saturn", {}).get("sign") in ["Capricorn", "Aquarius"]:
        career_indications.append("Business, engineering, structured professions")
    
    if "Venus" in planets:
        venus_sign = planets["Venus"].get("sign", "")
        relationship_indications.append(f"Venus in {venus_sign} indicates romantic nature and values in partnerships")
    if "Moon" in planets:
        moon_sign = planets["Moon"].get("sign", "")
        relationship_indications.append(f"Moon in {moon_sign} shows emotional needs in relationships")
    
    if planets.get("Mars", {}).get("sign") in ["Aries", "Scorpio"]:
        health_indications.append("Watch for head and facial injuries, maintain energy balance")
    if planets.get("Venus", {}).get("sign") in ["Taurus", "Libra"]:
        health_indications.append("Focus on throat and kidney health")
    
    sun_ruler = get_planet_ruler(sun_sign)
    moon_ruler = get_planet_ruler(moon_sign) if moon_sign else ""
    
    return {
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "rising_sign": rising_sign,
        "sun_ruler": sun_ruler,
        "moon_ruler": moon_ruler,
        "element": ELEMENTS.get(sun_sign, "Unknown"),
        "quality": QUALITIES.get(sun_sign, "Unknown"),
        "modalities": {
            "fire": {"signs": ["Aries", "Leo", "Sagittarius"], "traits": "Creative, passionate, spontaneous"},
            "earth": {"signs": ["Taurus", "Virgo", "Capricorn"], "traits": "Practical, stable, materialistic"},
            "air": {"signs": ["Gemini", "Libra", "Aquarius"], "traits": "Intellectual, social, communicative"},
            "water": {"signs": ["Cancer", "Scorpio", "Pisces"], "traits": "Emotional, intuitive, spiritual"}
        },
        "strengths": strengths,
        "challenges": challenges,
        "career": career_indications if career_indications else ["Various career paths suit your chart"],
        "relationships": relationship_indications if relationship_indications else ["Partnerships are important for growth"],
        "health": health_indications if health_indications else ["Maintain balance in lifestyle"],
        "summary": f"You are a {ELEMENTS.get(sun_sign, '')} sign ({sun_sign}) with {moon_sign} Moon and {rising_sign} Rising. Your ruling planet is {sun_ruler}."
    }

def calculate_kundli_matching(chart1: Dict, chart2: Dict) -> Dict[str, Any]:
    gunas = {
        "Varna": {"max": 1, "score": 0},
        "Vashya": {"max": 2, "score": 0},
        "Tara": {"max": 3, "score": 0},
        "Yoni": {"max": 4, "score": 0},
        "Graha Maitri": {"max": 5, "score": 0},
        "Gana": {"max": 6, "score": 0},
        "Kuta": {"max": 7, "score": 0},
        "Nadi": {"max": 8, "score": 0}
    }
    
    element_map = {"Fire": "Aries,Leo,Sagittarius", "Earth": "Taurus,Virgo,Capricorn", 
                   "Air": "Gemini,Libra,Aquarius", "Water": "Cancer,Scorpio,Pisces"}
    
    sign1 = chart1.get("sun_sign", "")
    sign2 = chart2.get("sun_sign", "")
    
    if ELEMENTS.get(sign1) == ELEMENTS.get(sign2):
        gunas["Varna"]["score"] = 1
    else:
        gunas["Varna"]["score"] = 0
    
    vashya_pairs = {
        "Aries": ["Aries", "Leo", "Sagittarius"], "Taurus": ["Taurus", "Virgo", "Capricorn"],
        "Gemini": ["Gemini", "Libra", "Aquarius"], "Cancer": ["Cancer", "Scorpio", "Pisces"]
    }
    for sign, pool in vashya_pairs.items():
        if sign1 in pool and sign2 in pool:
            gunas["Vashya"]["score"] = 2
            break
    else:
        gunas["Vashya"]["score"] = 1
    
    moon1 = chart1.get("moon_sign", "")
    moon2 = chart2.get("moon_sign", "")
    tara_scores = {0: 3, 1: 2, 2: 1, 3: 1, 4: 2, 5: 3, 6: 1, 7: 2, 8: 0, 9: 1, 10: 2, 11: 3}
    gunas["Tara"]["score"] = tara_scores.get((ZODIAC_SIGNS.index(moon1) - ZODIAC_SIGNS.index(moon2)) % 12, 1)
    
    compatibility_elements = {
        ("Aries", "Leo"): 4, ("Aries", "Sagittarius"): 4, ("Aries", "Gemini"): 2,
        ("Taurus", "Virgo"): 4, ("Taurus", "Capricorn"): 4, ("Taurus", "Cancer"): 2,
        ("Gemini", "Libra"): 4, ("Gemini", "Aquarius"): 4, ("Cancer", "Scorpio"): 4,
        ("Cancer", "Pisces"): 4, ("Leo", "Sagittarius"): 4, ("Virgo", "Capricorn"): 4,
        ("Scorpio", "Pisces"): 4, ("Libra", "Aquarius"): 4, ("Capricorn", "Aquarius"): 2
    }
    gunas["Graha Maitri"]["score"] = compatibility_elements.get((sign1, sign2), compatibility_elements.get((sign2, sign1), 1))
    
    gana_map = {"Aries": "Deva", "Taurus": "Manusha", "Gemini": "Rakshasa", 
                "Cancer": "Deva", "Leo": "Deva", "Virgo": "Manusha",
                "Libra": "Rakshasa", "Scorpio": "Rakshasa", "Sagittarius": "Deva",
                "Capricorn": "Manusha", "Aquarius": "Rakshasa", "Pisces": "Manusha"}
    
    if gana_map.get(sign1) == gana_map.get(sign2):
        gunas["Gana"]["score"] = 6
    elif (gana_map.get(sign1), gana_map.get(sign2)) in [("Deva", "Manusha"), ("Manusha", "Deva")]:
        gunas["Gana"]["score"] = 3
    else:
        gunas["Gana"]["score"] = 1
    
    kuta_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio"]
    gunas["Kuta"]["score"] = 7 if sign1 in kuta_signs and sign2 in kuta_signs else 0
    
    gunas["Nadi"]["score"] = 8
    
    total_score = sum(g["score"] for g in gunas.values())
    max_score = sum(g["max"] for g in gunas.values())
    percentage = round((total_score / max_score) * 100, 1)
    
    if percentage >= 70:
        result = "Excellent - Very harmonious match"
    elif percentage >= 50:
        result = "Good - Can work with understanding"
    elif percentage >= 30:
        result = "Average - Needs adjustments"
    else:
        result = "Low compatibility - Difficult match"
    
    return {
        "total_gunas": 36,
        "obtained_gunas": total_score,
        "percentage": percentage,
        "result": result,
        "details": gunas,
        "advice": "For best results, consult with a Vedic astrologer for personalized remedies and guidance."
    }

def generate_weekly_horoscope(sign: str, week_start_date: str) -> Dict[str, Any]:
    import hashlib
    
    sign_index = ZODIAC_SIGNS.index(sign) if sign in ZODIAC_SIGNS else 0
    seed = f"{sign}{week_start_date}weekly"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    predictions = {
        "Aries": {
            "love": "Passionate week ahead. Your energy attracts new connections.",
            "career": "Great time to start new projects. Your leadership shines.",
            "health": "High energy levels. Channel into physical activities.",
            "finance": "Unexpected gains possible. Trust your instincts."
        },
        "Taurus": {
            "love": "Stable relationships flourish. Express feelings openly.",
            "career": "Patience pays off. Focus on long-term goals.",
            "health": "Mind-body balance is key. Practice meditation.",
            "finance": "Financial planning beneficial. Avoid impulse buys."
        },
        "Gemini": {
            "love": "Communication is key. Share your thoughts clearly.",
            "career": "Networking brings opportunities. Stay curious.",
            "health": "Mental stimulation needed. Try something new.",
            "finance": "Multiple income streams possible. Diversify."
        },
        "Cancer": {
            "love": "Family matters dominate. Nurture existing bonds.",
            "career": "Intuition guides decisions. Trust your gut.",
            "health": "Emotional wellbeing important. Self-care essential.",
            "finance": "Home investments favorable. Secure your foundation."
        },
        "Leo": {
            "love": "Romance lights up your week. Be generous with love.",
            "career": "Creative projects succeed. Your confidence inspires.",
            "health": "Heart health needs attention. Stay active.",
            "finance": "Generosity brings returns. Invest in yourself."
        },
        "Virgo": {
            "love": "Practical expressions of love appreciated.",
            "career": "Details matter. Quality work gets recognized.",
            "health": "Focus on routine. Healthy habits pay off.",
            "finance": "Smart budgeting helps. Track expenses carefully."
        },
        "Libra": {
            "love": "Partnerships bloom. Balance give and take.",
            "career": "Diplomatic skills help. Avoid office politics.",
            "health": "Seek harmony in routine. Peaceful environments help.",
            "finance": "Joint finances beneficial. Discuss openly."
        },
        "Scorpio": {
            "love": "Deep transformations in love. Intensity increases.",
            "career": "Research pays off. Dive deep into problems.",
            "health": "Stress management crucial. Release tension.",
            "finance": "Hidden resources revealed. Trust your research."
        },
        "Sagittarius": {
            "love": "Adventure calls. Try something new together.",
            "career": "Travel and learning bring growth. Expand horizons.",
            "health": "Outdoor activities beneficial. Nature heals.",
            "finance": "Educational investments pay. Learn new skills."
        },
        "Capricorn": {
            "love": "Responsibility in relationships. Show commitment.",
            "career": "Career advancements possible. Hard work pays.",
            "health": "Build strength gradually. Consistency is key.",
            "finance": "Long-term investments wise. Plan for future."
        },
        "Aquarius": {
            "love": "Unique connections form. Embrace individuality.",
            "career": "Innovation rewarded. Think outside the box.",
            "health": "Mental exercises help. Challenge your mind.",
            "finance": "Tech investments favorable. Future-focused."
        },
        "Pisces": {
            "love": "Dreams become reality. Trust your intuition.",
            "career": "Creative inspiration flows. Follow your imagination.",
            "health": "Spiritual practices help. Connect with inner self.",
            "finance": "Intuitive investments work. Trust your gut."
        }
    }
    
    sign_pred = predictions.get(sign, predictions["Aries"])
    
    rating = ((hash_val % 5) + 6)
    
    return {
        "sign": sign,
        "week_start": week_start_date,
        "rating": f"{rating}/10",
        "love": sign_pred["love"],
        "career": sign_pred["career"],
        "health": sign_pred["health"],
        "finance": sign_pred["finance"],
        "lucky_color": ["Red", "Blue", "Green", "Gold", "Purple", "Silver", "White", "Black"][hash_val % 8],
        "lucky_number": (hash_val % 99) + 1,
        "advice": "Trust the journey. Every challenge is an opportunity for growth."
    }

def generate_monthly_horoscope(sign: str, year: int, month: int) -> Dict[str, Any]:
    import hashlib
    
    seed = f"{sign}{year}{month}monthly"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    themes = [
        "Transformation and new beginnings",
        "Relationships take center stage",
        "Career and ambition focus",
        "Personal growth and learning",
        "Family and home matters",
        "Creative expression and joy",
        "Financial planning and stability",
        "Spiritual awakening and healing"
    ]
    
    rating = ((hash_val % 5) + 6)
    
    predictions = {
        "Aries": {
            "theme": "Leadership and initiative",
            "highlights": "Your pioneering spirit leads to success",
            "challenges": "Patience needed in relationships",
            "spirit_animal": "Ram - Bold and determined"
        },
        "Taurus": {
            "theme": "Stability and abundance",
            "highlights": "Material and emotional security grows",
            "challenges": "Resistance to change",
            "spirit_animal": "Bull - Persistent and reliable"
        }
    }
    
    default_pred = {
        "theme": themes[month % len(themes)],
        "highlights": "Positive developments in multiple areas",
        "challenges": "Balance between work and life",
        "spirit_animal": f"Signs - Guide your path"
    }
    
    pred = predictions.get(sign, default_pred)
    
    return {
        "sign": sign,
        "month": f"{year}-{month:02d}",
        "rating": f"{rating}/10",
        "theme": pred["theme"],
        "highlights": pred["highlights"],
        "challenges": pred["challenges"],
        "spirit_animal": pred["spirit_animal"],
        "lucky_days": ["Monday", "Wednesday", "Friday"][hash_val % 3],
        "career": "Professional growth likely. New opportunities emerge.",
        "love": "Romance Flourishes. Deepen existing bonds.",
        "finance": "Financial gains possible. Smart investments work.",
        "health": "Maintain balance. Listen to your body."
    }

def draw_tarot_cards(count: int = 3, question: str = "") -> Dict[str, Any]:
    import random
    
    tarot_cards = [
        {"name": "The Fool", "meaning": "New beginnings, innocence, spontaneity, free spirit", "advice": "Take a leap of faith. New adventures await!"},
        {"name": "The Magician", "meaning": "Manifestation, power, skill, creativity", "advice": "You have all the tools. Use them wisely."},
        {"name": "The High Priestess", "meaning": "Intuition, mystery, subconscious, inner voice", "advice": "Trust your inner wisdom. Listen to your gut."},
        {"name": "The Empress", "meaning": "Femininity, nature, nurturing, abundance", "advice": "Nurture your creative side. Embrace growth."},
        {"name": "The Emperor", "meaning": "Authority, structure, stability, father figure", "advice": "Establish boundaries. Lead with confidence."},
        {"name": "The Hierophant", "meaning": "Tradition, teaching, guidance, beliefs", "advice": "Seek knowledge from experienced mentors."},
        {"name": "The Lovers", "meaning": "Love, harmony, relationships, choices", "advice": "Follow your heart. Balance is key."},
        {"name": "The Chariot", "meaning": "Victory, determination, will power", "advice": "Stay focused on your goals. Victory is near!"},
        {"name": "Strength", "meaning": "Courage, patience, inner strength, compassion", "advice": "Inner peace conquers all. Be patient."},
        {"name": "The Hermit", "meaning": "Soul searching, introspection, solitude", "advice": "Take time for yourself. Reflect internally."},
        {"name": "Wheel of Fortune", "meaning": "Destiny, change, cycles, fate", "advice": "Embrace the cycles. Good fortune is coming."},
        {"name": "Justice", "meaning": "Truth, fairness, cause and effect", "advice": "Seek truth. Balance will be restored."},
        {"name": "The Hanged Man", "meaning": "Pause, surrender, new perspective", "advice": "Stop and see differently. Let go to move forward."},
        {"name": "Death", "meaning": "Transformation, endings, new beginnings", "advice": "Release what no longer serves you. Make space for new."},
        {"name": "Temperance", "meaning": "Balance, patience, moderation", "advice": "Find balance in all things. Patience pays off."},
        {"name": "The Devil", "meaning": "Temptation, shadow self, materialism", "advice": "Break free from limitations. You are stronger."},
        {"name": "The Tower", "meaning": "Sudden change, revelation, awakening", "advice": "Sometimes destruction leads to liberation. Embrace change."},
        {"name": "The Star", "meaning": "Hope, inspiration, guidance, faith", "advice": "Stay hopeful. Better days are coming."},
        {"name": "The Moon", "meaning": "Illusion, intuition, dreams, fear", "advice": "Trust your dreams. Face your fears with courage."},
        {"name": "The Sun", "meaning": "Success, joy, vitality, positivity", "advice": "Success is coming! Embrace the joy."},
        {"name": "Judgement", "meaning": "Rebirth, inner calling, absolution", "answer": "It's time for rebirth. Answer your calling."},
        {"name": "The World", "meaning": "Completion, accomplishment, travel", "advice": "You've completed a cycle. Celebrate your journey!"},
        {"name": "Ace of Wands", "meaning": "Inspiration, new opportunities, growth", "advice": "A new creative spark awaits. Embrace it!"},
        {"name": "Ace of Cups", "meaning": "New love, compassion, emotional joy", "advice": "Love is in the air. Open your heart."},
        {"name": "Ace of Swords", "meaning": "Clarity, truth, new ideas", "advice": "Truth will set you free. Speak your mind."},
        {"name": "Ace of Pentacles", "meaning": "New job, financial gain, opportunity", "advice": "A promising opportunity is coming. Prepare!"}
    ]
    
    selected = random.sample(tarot_cards, min(count, len(tarot_cards)))
    
    return {
        "question": question if question else "General Reading",
        "cards": [{"position": i+1, **card} for i, card in enumerate(selected)],
        "summary": f"You drew {count} cards. The {selected[0]['name']} appears as your primary message.",
        "guidance": "Remember: Tarot is a tool for reflection. Trust your intuition in interpreting these messages."
    }

def calculate_muhurat(date: str, city: str = "Delhi") -> Dict[str, Any]:
    from datetime import datetime, timedelta
    
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    city_lat_lng = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Bangalore": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567)
    }
    
    lat, lng = city_lat_lng.get(city, (28.6139, 77.2090))
    
    jd = datetime_to_julian_day(dt)
    
    sunrise_jd, sunset_jd = 0, 0
    for hour in range(5, 18):
        test_dt = dt.replace(hour=hour)
        jd_test = datetime_to_julian_day(test_dt)
        positions = calculate_planet_positions(jd_test, lat, lng)
        if 90 <= positions.get("Sun", 0) <= 120:
            sunrise_jd = jd_test
            break
    
    day_length = (sunset_jd - sunrise_jd) if sunrise_jd > 0 else 0.5
    
    muhurats = [
        {"name": "Shubh Muhurat (Auspicious)", "time": "6:00 AM - 7:00 AM", "activities": ["New ventures", "Starting business", "Marriage"]},
        {"name": "Labh Muhurat (Profit)", "time": "10:00 AM - 11:00 AM", "activities": ["Financial deals", "Profitable work"]},
        {"name": "Amrit Muhurat (Nectar)", "time": "4:00 AM - 5:00 AM", "activities": ["Spiritual practices", "Meditation"]},
        {"name": "CharMuhurat (Four Ghadis)", "time": "8:00-10:00 AM, 2:00-4:00 PM", "activities": ["All good works"]},
        {"name": "Vijay Muhurat (Victory)", "time": "2:00 PM - 3:00 PM", "activities": ["Starting wars", "Legal matters"]},
        {"name": "Godhuli Muhurat", "time": "5:30 PM - 6:30 PM", "activities": ["Starting new home", "Gifts"]}
    ]
    
    rahu_kalam_start = (sunrise_jd + 2.625) % 1
    yamaganda_start = (sunrise_jd + 0.875) % 1
    
    return {
        "date": date,
        "city": city,
        "sunrise": f"{int((sunrise_jd % 1) * 24)}:00",
        "sunset": f"{int(((sunrise_jd + day_length) % 1) * 24)}:00",
        "muhurats": muhurats,
        "avoid": {
            "rahu_kalam": "10:30 AM - 12:00 PM",
            "yamaganda": "12:00 PM - 1:30 PM",
            "gulikai_kalam": "2:00 PM - 3:30 PM"
        },
        "advice": "For best results, start important work during Shubh or Amrit Muhurat."
    }