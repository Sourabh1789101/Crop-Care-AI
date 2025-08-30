import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

app = FastAPI(title="Crop-Care-AI Yield Prediction Service")

# Global model and scaler
model = None
scaler = None

class YieldPredictionRequest(BaseModel):
    crop_type: str
    soil_data: Dict[str, float]  # nitrogen, phosphorus, potassium, ph
    weather_data: Dict[str, float]  # temperature, rainfall, humidity
    farm_area_hectares: Optional[float] = 1.0
    region: Optional[str] = "default"

@app.on_event("startup")
async def load_model():
    global model, scaler
    try:
        model_path = os.getenv("MODEL_PATH", "/app/models/yield_prediction_model.pkl")
        scaler_path = os.getenv("SCALER_PATH", "/app/models/yield_scaler.pkl")
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print(f"Model loaded from {model_path}")
        else:
            print(f"Model not found at {model_path}, using dummy predictions")
            
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            print(f"Scaler loaded from {scaler_path}")
        else:
            print("Scaler not found, using dummy scaling")
            
    except Exception as e:
        print(f"Error loading model: {e}")

def extract_features(request: YieldPredictionRequest) -> np.ndarray:
    """Extract features from request for model prediction"""
    features = [
        request.soil_data.get('nitrogen', 0),
        request.soil_data.get('phosphorus', 0),
        request.soil_data.get('potassium', 0),
        request.soil_data.get('ph', 7.0),
        request.weather_data.get('average_temperature', 25),
        request.weather_data.get('total_rainfall', 1000),
        request.weather_data.get('average_humidity', 60),
        # Add crop type encoding (simplified)
        1 if request.crop_type.lower() == 'rice' else 0,
        1 if request.crop_type.lower() == 'wheat' else 0,
        1 if request.crop_type.lower() == 'corn' else 0,
    ]
    return np.array(features).reshape(1, -1)

@app.post("/predict")
async def predict_yield(request: YieldPredictionRequest):
    """Predict crop yield based on soil and weather data"""
    try:
        features = extract_features(request)
        
        if model is not None and scaler is not None:
            # Real prediction
            features_scaled = scaler.transform(features)
            yield_prediction = model.predict(features_scaled)[0]
            
            # Calculate bounds (simplified)
            lower_bound = max(0, yield_prediction * 0.8)
            upper_bound = yield_prediction * 1.2
        else:
            # Dummy prediction when model not available
            base_yield = {
                'rice': 4.5,
                'wheat': 3.2,
                'corn': 6.8
            }.get(request.crop_type.lower(), 4.0)
            
            # Adjust based on soil quality
            soil_quality = (
                request.soil_data.get('nitrogen', 40) / 100 +
                request.soil_data.get('phosphorus', 30) / 100 +
                request.soil_data.get('potassium', 40) / 100 +
                min(request.soil_data.get('ph', 6.5) / 7.0, 1.0)
            ) / 4.0
            
            # Adjust based on weather
            temp = request.weather_data.get('average_temperature', 25)
            rainfall = request.weather_data.get('total_rainfall', 1000)
            weather_factor = min(temp / 30.0, 1.0) * min(rainfall / 1200.0, 1.0)
            
            yield_prediction = base_yield * soil_quality * weather_factor
            lower_bound = max(0, yield_prediction * 0.8)
            upper_bound = yield_prediction * 1.2
        
        # Calculate total production and market value
        total_production = yield_prediction * request.farm_area_hectares
        market_price_per_tonne = get_market_price(request.crop_type)
        estimated_value = total_production * market_price_per_tonne
        
        # Generate recommendations
        recommendations = generate_recommendations(request, yield_prediction)
        
        return {
            "predicted_yield": {
                "value": round(yield_prediction, 2),
                "unit": "tonnes/hectare",
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2)
            },
            "total_production": {
                "value": round(total_production, 2),
                "unit": "tonnes"
            },
            "market_value_estimation": {
                "price_per_tonne": market_price_per_tonne,
                "total_value": round(estimated_value, 2),
                "currency": "USD"
            },
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

def get_market_price(crop_type: str) -> float:
    """Get current market price per tonne (simplified)"""
    prices = {
        'rice': 400,
        'wheat': 250,
        'corn': 200,
        'soybean': 500,
        'cotton': 1500
    }
    return prices.get(crop_type.lower(), 300)

def generate_recommendations(request: YieldPredictionRequest, predicted_yield: float) -> list:
    """Generate recommendations to improve yield"""
    recommendations = []
    
    # Soil-based recommendations
    nitrogen = request.soil_data.get('nitrogen', 0)
    phosphorus = request.soil_data.get('phosphorus', 0)
    potassium = request.soil_data.get('potassium', 0)
    ph = request.soil_data.get('ph', 7.0)
    
    if nitrogen < 40:
        recommendations.append("Consider nitrogen fertilizer application to improve soil nitrogen levels")
    if phosphorus < 30:
        recommendations.append("Apply phosphorus fertilizer to enhance root development")
    if potassium < 40:
        recommendations.append("Increase potassium levels for better plant disease resistance")
    if ph < 6.0 or ph > 8.0:
        recommendations.append("Adjust soil pH to optimal range (6.0-7.5) using lime or sulfur")
    
    # Weather-based recommendations
    rainfall = request.weather_data.get('total_rainfall', 1000)
    temperature = request.weather_data.get('average_temperature', 25)
    
    if rainfall < 800:
        recommendations.append("Consider irrigation planning due to low rainfall prediction")
    if temperature > 35:
        recommendations.append("Monitor for heat stress; consider shade management")
    
    # Yield-based recommendations
    if predicted_yield < 3.0:
        recommendations.append("Consider high-yielding varieties and improved farming practices")
    
    if not recommendations:
        recommendations.append("Current conditions are favorable for good yield")
    
    return recommendations

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
