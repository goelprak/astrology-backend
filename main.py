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
        hf_token = os.environ.get("HF_TOKEN", "")
        
        body = await request.body()
        body_str = body.decode('utf-8')
        
        import json
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError as je:
            try:
                data = json.loads(body_str.encode('ascii', 'replace').decode('utf-8', 'ignore'))
            except:
                body_preview = repr(body_str[:100])
                return {"response": f"JSON parse error: {str(je)}, body was: {body_preview}"}
        
        msg = data.get("message", "") if data else ""
        
        if not msg:
            return {"response": "Please provide a message"}
        
        from huggingface_hub import InferenceClient
        
        context = "You are a knowledgeable astrologer specializing in Vedic astrology, KP astrology, Numerology, and Tarot."
        prompt = f"{context}\nUser: {msg}\nAssistant:"
        
        client = InferenceClient(token=hf_token if hf_token else None, timeout=60)
        result = client.text_generation(
            prompt,
            model="google/flan-t5-large",
            max_new_tokens=400,
            temperature=0.7,
            do_sample=True
        )
        
        if result:
            text = str(result).strip()
            answer = text[len(prompt):].strip() if text.startswith(prompt) else text
            return {"response": answer or text}
        return {"response": "AI did not return a response"}
        
    except Exception as e:
        import traceback
        return {"response": f"AI Error: {str(e)}", "trace": traceback.format_exc()}
