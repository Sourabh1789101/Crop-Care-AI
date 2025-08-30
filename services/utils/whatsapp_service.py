import os
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class WhatsAppService:
    """WhatsApp Business API Service for sending messages"""
    
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
        self.api_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
        
        if not all([self.access_token, self.phone_number_id]):
            print("Warning: WhatsApp credentials not found. Set environment variables.")
    
    def send_text_message(self, to: str, message: str) -> Dict:
        """Send a text message to WhatsApp user"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            return {"success": True, "response": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_template_message(self, to: str, template_name: str, language: str = "en") -> Dict:
        """Send a template message"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language}
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            return {"success": True, "response": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_interactive_message(self, to: str, body_text: str, buttons: List[Dict]) -> Dict:
        """Send interactive message with buttons"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        interactive_buttons = []
        for i, button in enumerate(buttons[:3]):  # WhatsApp allows max 3 buttons
            interactive_buttons.append({
                "type": "reply",
                "reply": {
                    "id": button.get("id", f"btn_{i}"),
                    "title": button.get("title", f"Button {i+1}")
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": interactive_buttons}
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            return {"success": True, "response": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

class WhatsAppMessageProcessor:
    """Process incoming WhatsApp messages and generate responses"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base = api_base_url
        self.whatsapp_service = WhatsAppService()
    
    def process_message(self, message_data: Dict) -> Dict:
        """Process incoming WhatsApp message"""
        try:
            # Extract message details
            from_number = message_data.get("from", "")
            message_text = message_data.get("text", {}).get("body", "").strip()
            message_type = message_data.get("type", "text")
            
            response = self.generate_response(message_text, message_type, from_number)
            
            if response:
                # Send response back to user
                result = self.whatsapp_service.send_text_message(from_number, response)
                return {"status": "sent", "result": result}
            
            return {"status": "no_response"}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_response(self, message: str, message_type: str, from_number: str) -> str:
        """Generate appropriate response based on message content"""
        message_lower = message.lower()
        
        # Command processing
        if message_lower.startswith("!help") or message_lower == "help":
            return self.get_help_message()
        
        elif message_lower.startswith("!crop"):
            return self.handle_crop_command(message)
        
        elif message_lower.startswith("!weather"):
            return self.handle_weather_command(message)
        
        elif message_lower.startswith("!fertilizer"):
            return self.handle_fertilizer_command(message)
        
        elif message_lower.startswith("!market"):
            return self.handle_market_command(message)
        
        elif message_lower in ["hi", "hello", "start", "hey"]:
            return self.get_welcome_message()
        
        else:
            return self.get_default_response()
    
    def get_help_message(self) -> str:
        """Return help message with available commands"""
        return """🌾 *Smart Crop Advisory Bot Commands*

*Available Commands:*
• `!crop N P K pH rainfall` - Get crop recommendation
  Example: `!crop 90 42 43 6.5 120`

• `!weather [pincode]` - Get weather alerts
  Example: `!weather 390001`

• `!fertilizer crop N P K pH` - Get fertilizer guidance
  Example: `!fertilizer wheat 90 42 43 6.5`

• `!market [crop]` - Get market prices
  Example: `!market wheat`

• `!help` - Show this help message

*Quick Commands:*
• Type "hi" for welcome message
• Send plant image for disease detection (coming soon)

Need help? Just type your question in simple words!"""
    
    def get_welcome_message(self) -> str:
        """Return welcome message"""
        return """🌾 *Welcome to Smart Crop Advisory!*

I'm here to help you with:
• 🌱 Crop recommendations
• 🧪 Fertilizer guidance  
• 🌤️ Weather alerts
• 💰 Market prices
• 🦠 Disease detection

Type `!help` to see all commands or just ask me questions in simple words!

Example: "What crop should I grow?" or "Weather for 390001" """
    
    def get_default_response(self) -> str:
        """Return default response for unrecognized messages"""
        return """I didn't understand that command. 🤔

Try these:
• Type `!help` for all commands
• Ask "What crop should I grow?"
• Check "Weather for [your pincode]"
• Ask "Market prices for wheat"

I'm here to help with your farming needs! 🌾"""
    
    def handle_crop_command(self, message: str) -> str:
        """Handle crop recommendation command"""
        try:
            parts = message.split()
            if len(parts) < 6:
                return """🌱 *Crop Recommendation*

Please provide soil parameters:
`!crop N P K pH rainfall`

Example: `!crop 90 42 43 6.5 120`

Where:
• N = Nitrogen (kg/ha)
• P = Phosphorus (kg/ha)  
• K = Potassium (kg/ha)
• pH = Soil pH
• rainfall = Rainfall (mm)"""
            
            n, p, k, ph, rainfall = map(float, parts[1:6])
            
            # Call API
            payload = {"N": n, "P": p, "K": k, "ph": ph, "rainfall": rainfall}
            response = requests.post(f"{self.api_base}/recommend_crop", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                crop = data.get("crop", "Unknown")
                confidence = data.get("confidence", 0)
                
                return f"""🌱 *Crop Recommendation*

*Recommended Crop:* {crop.title()}
*Confidence:* {confidence*100:.1f}%

*Your Soil Parameters:*
• Nitrogen: {n} kg/ha
• Phosphorus: {p} kg/ha
• Potassium: {k} kg/ha
• pH: {ph}
• Rainfall: {rainfall} mm

Need fertilizer guidance? Try:
`!fertilizer {crop} {n} {p} {k} {ph}`"""
            else:
                return "❌ Unable to get crop recommendation. Please try again."
                
        except Exception as e:
            return f"❌ Error processing crop command: {str(e)}"
    
    def handle_weather_command(self, message: str) -> str:
        """Handle weather command"""
        try:
            parts = message.split()
            if len(parts) < 2:
                return """🌤️ *Weather Information*

Please provide your pincode:
`!weather [pincode]`

Example: `!weather 390001`

I'll provide current weather, alerts, and farming recommendations for your area."""
            
            pincode = parts[1]
            
            # Call API
            response = requests.get(f"{self.api_base}/weather", params={"pincode": pincode})
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    return f"❌ {data['error']}"
                
                # Format weather response
                location = data.get("location", "Unknown")
                current = data.get("current_weather", {})
                alerts = data.get("alerts", [])
                recommendations = data.get("agricultural_recommendations", [])
                conditions = data.get("farming_conditions", {})
                
                response_text = f"""🌤️ *Weather for {location}*

*Current Conditions:*
• Temperature: {current.get('temperature', 'N/A')}°C
• Humidity: {current.get('humidity', 'N/A')}%
• Wind: {current.get('wind_speed', 'N/A')} m/s
• Conditions: {current.get('description', 'N/A')}"""

                if alerts:
                    response_text += "\n\n*⚠️ Alerts:*\n"
                    for alert in alerts[:3]:  # Limit to 3 alerts
                        response_text += f"• {alert}\n"
                
                if recommendations:
                    response_text += "\n*📋 Farming Tips:*\n"
                    for rec in recommendations[:3]:  # Limit to 3 recommendations
                        response_text += f"• {rec}\n"
                
                # Farming conditions
                response_text += f"\n*🚜 Today's Farming Conditions:*\n"
                response_text += f"• Spraying: {conditions.get('spraying', 'Unknown').title()}\n"
                response_text += f"• Harvesting: {conditions.get('harvesting', 'Unknown').title()}\n"
                response_text += f"• Irrigation need: {conditions.get('irrigation', 'Unknown').title()}"
                
                return response_text
            else:
                return "❌ Unable to get weather information. Please check the pincode."
                
        except Exception as e:
            return f"❌ Error getting weather: {str(e)}"
    
    def handle_fertilizer_command(self, message: str) -> str:
        """Handle fertilizer recommendation command"""
        try:
            parts = message.split()
            if len(parts) < 6:
                return """🧪 *Fertilizer Guidance*

Please provide crop and soil parameters:
`!fertilizer crop N P K pH`

Example: `!fertilizer wheat 90 42 43 6.5`

Where:
• crop = Crop name (wheat, rice, maize)
• N = Nitrogen (kg/ha)
• P = Phosphorus (kg/ha)
• K = Potassium (kg/ha)
• pH = Soil pH"""
            
            crop = parts[1]
            n, p, k, ph = map(float, parts[2:6])
            
            # Call API
            payload = {"crop": crop, "N": n, "P": p, "K": k, "ph": ph}
            response = requests.post(f"{self.api_base}/recommend_fertilizer", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                base = data.get("base", {})
                adjusted = data.get("adjusted", {})
                notes = data.get("notes", [])
                
                response_text = f"""🧪 *Fertilizer Plan for {crop.title()}*

*Recommended Fertilizers (kg/acre):*
• Urea: {adjusted.get('urea', 0)} kg
• DAP: {adjusted.get('dap', 0)} kg  
• MOP: {adjusted.get('mop', 0)} kg

*Your Soil Status:*
• Nitrogen: {n} kg/ha
• Phosphorus: {p} kg/ha
• Potassium: {k} kg/ha
• pH: {ph}"""

                if notes:
                    response_text += "\n\n*⚠️ Soil Improvement Tips:*\n"
                    for note in notes[:3]:  # Limit to 3 notes
                        response_text += f"• {note}\n"
                
                return response_text
            else:
                return "❌ Unable to get fertilizer recommendation. Please try again."
                
        except Exception as e:
            return f"❌ Error processing fertilizer command: {str(e)}"
    
    def handle_market_command(self, message: str) -> str:
        """Handle market prices command"""
        try:
            parts = message.split()
            crop = parts[1] if len(parts) > 1 else None
            
            # Call API
            params = {"crop": crop} if crop else {}
            response = requests.get(f"{self.api_base}/market", params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                if not results:
                    return f"❌ No market data found for {crop if crop else 'any crop'}."
                
                response_text = "💰 *Current Market Prices*\n\n"
                
                for item in results[:5]:  # Limit to 5 results
                    crop_name = item.get("crop", "Unknown")
                    price = item.get("modal_price", 0)
                    unit = item.get("unit", "INR/qtl")
                    market = item.get("market", "Unknown")
                    
                    response_text += f"*{crop_name.title()}*\n"
                    response_text += f"• Price: ₹{price}/{unit}\n"
                    response_text += f"• Market: {market}\n\n"
                
                response_text += "_Prices are indicative and may vary._"
                return response_text
            else:
                return "❌ Unable to get market prices. Please try again."
                
        except Exception as e:
            return f"❌ Error getting market prices: {str(e)}"
