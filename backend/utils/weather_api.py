import os
import requests
from typing import Dict, List
from datetime import datetime, timedelta
import json

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"

class WeatherClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set OPENWEATHER_API_KEY env var")

    def current_by_pincode(self, pincode: str, country: str = "IN") -> Dict:
        params = {"zip": f"{pincode},{country}", "appid": self.api_key, "units": "metric"}
        r = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def forecast_by_pincode(self, pincode: str, country: str = "IN") -> Dict:
        params = {"zip": f"{pincode},{country}", "appid": self.api_key, "units": "metric"}
        r = requests.get(FORECAST_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    
    def get_coordinates_by_pincode(self, pincode: str, country: str = "IN") -> tuple:
        """Get latitude and longitude for a pincode"""
        try:
            current = self.current_by_pincode(pincode, country)
            lat = current["coord"]["lat"]
            lon = current["coord"]["lon"]
            return lat, lon
        except Exception:
            # Default coordinates for India (New Delhi)
            return 28.6139, 77.2090

    def get_detailed_forecast(self, pincode: str, country: str = "IN") -> Dict:
        """Get detailed 7-day weather forecast including agricultural data"""
        try:
            lat, lon = self.get_coordinates_by_pincode(pincode, country)
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "exclude": "minutely"
            }
            r = requests.get(ONECALL_URL, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            # Fallback to basic forecast
            return self.forecast_by_pincode(pincode, country)

    @staticmethod
    def simple_alerts(current: Dict) -> List[str]:
        alerts = []
        rain = 0.0
        if "rain" in current:
            rain = current.get("rain", {}).get("1h", 0.0)
        wind = current.get("wind", {}).get("speed", 0.0)
        temp = current.get("main", {}).get("temp", 25)
        humidity = current.get("main", {}).get("humidity", 50)
        
        if rain >= 2:
            alerts.append("🌧️ Heavy rain alert: Postpone spraying and field work.")
        elif rain >= 0.5:
            alerts.append("🌦️ Light rain expected: Plan indoor activities.")
            
        if wind >= 15:
            alerts.append("💨 High wind alert: Avoid pesticide spraying and tall crop work.")
        elif wind >= 10:
            alerts.append("🌬️ Moderate wind: Use caution with spray applications.")
            
        if temp >= 38:
            alerts.append("🔥 Heat alert: Irrigate during evening/early morning only.")
        elif temp >= 35:
            alerts.append("☀️ Hot weather: Increase irrigation frequency.")
        elif temp <= 5:
            alerts.append("🧊 Frost alert: Protect sensitive crops.")
            
        if humidity <= 30:
            alerts.append("🏜️ Low humidity: Increase irrigation, monitor for pest stress.")
        elif humidity >= 85:
            alerts.append("💧 High humidity: Monitor for fungal diseases.")
            
        return alerts

    @staticmethod
    def agricultural_recommendations(current: Dict, forecast: Dict = None) -> List[str]:
        """Generate crop-specific recommendations based on weather"""
        recommendations = []
        
        temp = current.get("main", {}).get("temp", 25)
        humidity = current.get("main", {}).get("humidity", 50)
        wind = current.get("wind", {}).get("speed", 0.0)
        
        # Temperature-based recommendations
        if temp > 35:
            recommendations.append("🌾 Wheat/Barley: Avoid harvesting during peak heat")
            recommendations.append("🌱 Vegetables: Provide shade during midday")
        elif temp < 10:
            recommendations.append("🌾 Protect winter crops from frost damage")
            recommendations.append("🌱 Cover sensitive seedlings")
            
        # Wind-based recommendations
        if wind > 12:
            recommendations.append("🚁 Avoid aerial spraying and drone operations")
            recommendations.append("🌾 Support tall crops to prevent lodging")
            
        # Humidity-based recommendations
        if humidity > 80:
            recommendations.append("🦠 High disease risk: Monitor for blight and fungus")
            recommendations.append("💨 Ensure good air circulation in crops")
        elif humidity < 40:
            recommendations.append("💧 Increase irrigation frequency")
            recommendations.append("🌿 Monitor for pest stress and wilting")
            
        return recommendations

    def get_agricultural_summary(self, pincode: str, country: str = "IN") -> Dict:
        """Get complete agricultural weather summary"""
        try:
            current = self.current_by_pincode(pincode, country)
            forecast = self.forecast_by_pincode(pincode, country)
            
            # Extract key data
            temp = current.get("main", {}).get("temp", 0)
            humidity = current.get("main", {}).get("humidity", 0)
            wind_speed = current.get("wind", {}).get("speed", 0)
            description = current.get("weather", [{}])[0].get("description", "")
            
            # Get rain forecast for next 24 hours
            next_24h_rain = 0
            if "list" in forecast:
                for item in forecast["list"][:8]:  # Next 24 hours (3-hour intervals)
                    if "rain" in item:
                        next_24h_rain += item["rain"].get("3h", 0)
            
            alerts = self.simple_alerts(current)
            recommendations = self.agricultural_recommendations(current, forecast)
            
            return {
                "location": current.get("name", "Unknown"),
                "current_weather": {
                    "temperature": temp,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "description": description,
                    "feels_like": current.get("main", {}).get("feels_like", temp)
                },
                "forecast": {
                    "rain_next_24h": round(next_24h_rain, 2),
                    "summary": f"Expected rainfall: {next_24h_rain:.1f}mm in next 24 hours"
                },
                "alerts": alerts,
                "agricultural_recommendations": recommendations,
                "farming_conditions": self.get_farming_conditions(current),
                "best_farming_hours": self.get_best_farming_hours(current)
            }
        except Exception as e:
            return {"error": f"Weather data unavailable: {str(e)}"}

    @staticmethod
    def get_farming_conditions(current: Dict) -> Dict:
        """Assess current farming conditions"""
        temp = current.get("main", {}).get("temp", 25)
        wind = current.get("wind", {}).get("speed", 0)
        humidity = current.get("main", {}).get("humidity", 50)
        
        conditions = {
            "spraying": "good",
            "harvesting": "good", 
            "planting": "good",
            "irrigation": "moderate"
        }
        
        # Spraying conditions
        if wind > 10 or temp > 35:
            conditions["spraying"] = "poor"
        elif wind > 6 or temp > 30:
            conditions["spraying"] = "moderate"
            
        # Harvesting conditions  
        if temp > 38 or wind > 15:
            conditions["harvesting"] = "poor"
        elif temp > 32:
            conditions["harvesting"] = "moderate"
            
        # Irrigation needs
        if temp > 35 or humidity < 40:
            conditions["irrigation"] = "high"
        elif temp < 20 and humidity > 70:
            conditions["irrigation"] = "low"
            
        return conditions

    @staticmethod
    def get_best_farming_hours(current: Dict) -> List[str]:
        """Recommend best hours for farming activities"""
        temp = current.get("main", {}).get("temp", 25)
        
        if temp > 35:
            return [
                "🌅 Early morning: 5:00 AM - 8:00 AM (irrigation, spraying)",
                "🌆 Evening: 6:00 PM - 8:00 PM (field work)",
                "🌙 Night: 8:00 PM onwards (irrigation)"
            ]
        elif temp > 30:
            return [
                "🌅 Morning: 6:00 AM - 10:00 AM (all activities)",
                "🌆 Evening: 4:00 PM - 7:00 PM (field work)"
            ]
        else:
            return [
                "🌅 Morning: 7:00 AM - 11:00 AM (all activities)",
                "🌞 Afternoon: 2:00 PM - 5:00 PM (field work)",
                "🌆 Evening: 5:00 PM - 7:00 PM (irrigation)"
            ]
