from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import astrology

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