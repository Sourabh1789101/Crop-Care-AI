from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import numpy as np

# Create FastAPI app
app = FastAPI(title="Smart Crop Advisory API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SoilInput(BaseModel):
    N: float
    P: float
    K: float
    ph: float
    rainfall: Optional[float] = 100
    soil_type: Optional[str] = "loam"
    location: Optional[str] = None

class CropRecoRequest(SoilInput):
    pass

class FertRequest(SoilInput):
    crop: str

# Routes
@app.get("/")
async def root():
    return {
        "message": "Smart Crop Advisory API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "crop_recommendation": "/recommend_crop",
            "fertilizer_recommendation": "/recommend_fertilizer",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "message": "API is running"}

@app.post("/recommend_crop")
async def recommend_crop(payload: CropRecoRequest):
    """Simple heuristic crop recommendation based on soil parameters"""
    ph = payload.ph
    
    # Simple rule-based recommendation
    if 6.0 <= ph <= 7.5:
        if payload.N > 80:
            crop = "wheat"
        elif payload.P > 40:
            crop = "corn"
        else:
            crop = "rice"
    elif ph < 6.0:
        crop = "rice"
    else:
        crop = "maize"
    
    return {
        "crop": crop,
        "confidence": 0.75,
        "note": "Basic recommendation - upgrade with ML models for better accuracy"
    }

@app.post("/recommend_fertilizer")
async def recommend_fertilizer(payload: FertRequest):
    """Basic fertilizer recommendation"""
    crop = payload.crop.lower()
    
    # Simple fertilizer recommendations
    fertilizer_map = {
        "wheat": {"N": "120-150 kg/ha", "P": "60-80 kg/ha", "K": "40-60 kg/ha"},
        "rice": {"N": "100-120 kg/ha", "P": "50-60 kg/ha", "K": "30-40 kg/ha"},
        "corn": {"N": "150-200 kg/ha", "P": "80-100 kg/ha", "K": "60-80 kg/ha"},
        "maize": {"N": "150-200 kg/ha", "P": "80-100 kg/ha", "K": "60-80 kg/ha"}
    }
    
    recommendation = fertilizer_map.get(crop, {
        "N": "100-120 kg/ha", 
        "P": "60-80 kg/ha", 
        "K": "40-60 kg/ha"
    })
    
    return {
        "crop": payload.crop,
        "fertilizer_recommendation": recommendation,
        "note": "Apply in split doses based on crop growth stage"
    }

@app.get("/market")
async def market(crop: Optional[str] = None, state: Optional[str] = None):
    """Mock market prices"""
    prices = {
        "wheat": {"price": "2500-2800 INR/quintal", "trend": "stable"},
        "rice": {"price": "2200-2600 INR/quintal", "trend": "increasing"},
        "corn": {"price": "2000-2400 INR/quintal", "trend": "stable"},
        "maize": {"price": "2000-2400 INR/quintal", "trend": "stable"}
    }
    
    if crop:
        return {
            "crop": crop,
            "market_data": prices.get(crop.lower(), {"price": "Contact local market", "trend": "unknown"})
        }
    
    return {"market_prices": prices, "note": "Mock data - integrate with real market APIs"}

@app.get("/weather")
async def weather(pincode: str):
    """Mock weather data"""
    return {
        "location": f"Pincode: {pincode}",
        "weather": {
            "temperature": "25-32°C",
            "humidity": "60-80%",
            "rainfall": "Expected in 2-3 days"
        },
        "agricultural_advisory": "Good conditions for sowing. Prepare for upcoming rain.",
        "note": "Mock data - set OPENWEATHER_API_KEY for real data"
    }

# Export for Vercel
handler = app
