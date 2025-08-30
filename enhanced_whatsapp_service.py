import os
import requests
import json
import re
from typing import Dict, List, Optional
from datetime import datetime

class EnhancedWhatsAppMessageProcessor:
    """Enhanced WhatsApp message processor with natural language understanding"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base = api_base_url
        
        # Natural language patterns for commands
        self.patterns = {
            'weather': [
                r'weather\s+(\d{6})',
                r'weather\s+in\s+(\d{6})',
                r'weather\s+for\s+(\d{6})',
                r'what.*weather.*(\d{6})',
                r'how.*weather.*(\d{6})',
                r'weather\s+today\s+(\d{6})',
                r'(\d{6})\s+weather'
            ],
            'crop': [
                r'crop\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)',
                r'recommend\s+crop.*(\d+).*(\d+).*(\d+).*([\d.]+).*(\d+)',
                r'what\s+crop.*(\d+).*(\d+).*(\d+).*([\d.]+).*(\d+)',
                r'which\s+crop.*(\d+).*(\d+).*(\d+).*([\d.]+).*(\d+)'
            ],
            'fertilizer': [
                r'fertilizer\s+for\s+(\w+)',
                r'fertilizer\s+(\w+)',
                r'what\s+fertilizer.*(\w+)',
                r'which\s+fertilizer.*(\w+)',
                r'(\w+)\s+fertilizer'
            ],
            'market': [
                r'market\s+price\s+(\w+)',
                r'market\s+(\w+)',
                r'price\s+of\s+(\w+)',
                r'(\w+)\s+price',
                r'what.*price.*(\w+)',
                r'how\s+much.*(\w+)'
            ],
            'greeting': [
                r'hi|hello|hey|namaste|namaskar',
                r'good\s+morning|good\s+evening|good\s+afternoon',
                r'start|begin'
            ],
            'help': [
                r'help|commands|what\s+can\s+you\s+do',
                r'how\s+to\s+use|instructions',
                r'menu|options'
            ]
        }
        
        # Common farmer questions and their responses
        self.farmer_responses = {
            'soil': "🌱 For soil testing, I can help with crop recommendations if you have N-P-K values and pH. Use: !crop [N] [P] [K] [pH] [rainfall]",
            'disease': "🦠 For plant disease detection, take a clear photo of affected leaves/plant parts. Disease detection feature coming soon!",
            'irrigation': "💧 For irrigation advice, check weather conditions first with !weather [pincode]. I'll provide rainfall forecasts and watering recommendations.",
            'seeds': "🌰 For seed varieties, use !crop command with your soil parameters. I'll recommend the best crops for your conditions.",
            'pest': "🐛 For pest control, specific crop advice available via !fertilizer [crop] command. General pest management tips included.",
            'organic': "🌿 For organic farming methods, I provide eco-friendly fertilizer recommendations. Use !fertilizer [crop] for organic options.",
            'price': "💰 For current market prices, use !market [crop]. I provide real-time prices and market trends."
        }
    
    def process_message(self, message_data: Dict) -> Dict:
        """Process incoming WhatsApp message with enhanced understanding"""
        try:
            message_text = message_data.get("text", {}).get("body", "").strip()
            message_type = message_data.get("type", "text")
            from_number = message_data.get("from", "")
            
            # Clean message text
            message_text = message_text.lower().strip()
            
            print(f"📱 Processing message: '{message_text}' from {from_number}")
            
            # Generate response
            response = self.generate_enhanced_response(message_text, message_type, from_number)
            
            # Send response back via WhatsApp
            if response:
                result = self.send_whatsapp_response(from_number, response)
                return {
                    "status": "success",
                    "response_sent": True,
                    "message": "Response sent successfully"
                }
            
            return {
                "status": "success", 
                "response_sent": False,
                "message": "No response needed"
            }
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_enhanced_response(self, message: str, message_type: str, from_number: str) -> str:
        """Generate enhanced response with natural language understanding"""
        
        # Handle greetings
        if self.match_pattern(message, 'greeting'):
            return self.get_welcome_message()
        
        # Handle help requests
        if self.match_pattern(message, 'help'):
            return self.get_help_message()
        
        # Handle weather requests
        weather_match = self.extract_pattern_data(message, 'weather')
        if weather_match:
            pincode = weather_match[0]
            return self.handle_weather_command(f"!weather {pincode}")
        
        # Handle crop recommendations
        crop_match = self.extract_pattern_data(message, 'crop')
        if crop_match and len(crop_match) >= 5:
            n, p, k, ph, rainfall = crop_match[:5]
            return self.handle_crop_command(f"!crop {n} {p} {k} {ph} {rainfall}")
        
        # Handle fertilizer requests
        fertilizer_match = self.extract_pattern_data(message, 'fertilizer')
        if fertilizer_match:
            crop = fertilizer_match[0]
            return self.handle_fertilizer_command(f"!fertilizer {crop}")
        
        # Handle market price requests
        market_match = self.extract_pattern_data(message, 'market')
        if market_match:
            crop = market_match[0]
            return self.handle_market_command(f"!market {crop}")
        
        # Handle general farming questions
        farming_response = self.handle_farming_questions(message)
        if farming_response:
            return farming_response
        
        # Handle traditional commands (fallback)
        if message.startswith('!'):
            return self.handle_traditional_commands(message)
        
        # Default response for unrecognized messages
        return self.get_smart_default_response(message)
    
    def match_pattern(self, message: str, pattern_type: str) -> bool:
        """Check if message matches any pattern of given type"""
        patterns = self.patterns.get(pattern_type, [])
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False
    
    def extract_pattern_data(self, message: str, pattern_type: str) -> Optional[List[str]]:
        """Extract data from message using patterns"""
        patterns = self.patterns.get(pattern_type, [])
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return list(match.groups())
        return None
    
    def handle_farming_questions(self, message: str) -> Optional[str]:
        """Handle general farming questions"""
        for keyword, response in self.farmer_responses.items():
            if keyword in message:
                return response
        return None
    
    def get_smart_default_response(self, message: str) -> str:
        """Generate smart default response based on message content"""
        
        # Check for numbers (might be trying to use commands)
        if re.search(r'\d+', message):
            return """🤔 I see you mentioned some numbers. Are you trying to:

• Get weather info? Try: `!weather [pincode]` 
• Get crop advice? Try: `!crop [N] [P] [K] [pH] [rainfall]`
• Check prices? Try: `!market [crop name]`

Type `!help` to see all commands."""
        
        # Check for crop names
        crops = ['wheat', 'rice', 'corn', 'tomato', 'potato', 'onion', 'cotton', 'sugarcane', 'soybean']
        mentioned_crops = [crop for crop in crops if crop in message]
        
        if mentioned_crops:
            crop = mentioned_crops[0]
            return f"""🌾 I see you mentioned {crop}. Here's what I can help with:

• `!fertilizer {crop}` - Get fertilizer recommendations
• `!market {crop}` - Check current market prices
• `!weather [your pincode]` - Weather conditions for {crop} farming

Type `!help` for all available commands."""
        
        return """🌾 I'm your Smart Crop Advisory Bot! 

I can help with:
• Weather forecasts and farming alerts
• Crop recommendations based on soil conditions
• Fertilizer guidance for specific crops
• Current market prices

Type `!help` to see all commands or just ask me naturally:
• "weather in 390001"
• "fertilizer for wheat"
• "rice market prices"

How can I assist you today?"""
    
    def handle_traditional_commands(self, message: str) -> str:
        """Handle traditional ! commands"""
        if message.startswith('!help'):
            return self.get_help_message()
        elif message.startswith('!weather'):
            return self.handle_weather_command(message)
        elif message.startswith('!crop'):
            return self.handle_crop_command(message)
        elif message.startswith('!fertilizer'):
            return self.handle_fertilizer_command(message)
        elif message.startswith('!market'):
            return self.handle_market_command(message)
        else:
            return "❓ Unknown command. Type `!help` to see available commands."
    
    def send_whatsapp_response(self, to_number: str, message: str) -> bool:
        """Send response via WhatsApp API"""
        try:
            access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
            phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
            
            if not access_token or not phone_number_id:
                print("❌ WhatsApp credentials not configured")
                return False
            
            url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {"body": message}
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get("messages", [{}])[0].get("id", "unknown")
                print(f"✅ Response sent successfully - Message ID: {message_id}")
                return True
            else:
                print(f"❌ Failed to send response: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Error sending WhatsApp response: {e}")
            return False
    
    def get_welcome_message(self) -> str:
        """Enhanced welcome message"""
        return """🌾 *नमस्ते! Welcome to Smart Crop Advisory Bot* 🌾

I'm here to help farmers with:

🌤️ *Weather & Alerts*
• Real-time weather updates
• Farming condition alerts
• Rain forecasts

🌱 *Crop Guidance*
• Crop recommendations
• Fertilizer advice
• Best planting times

💰 *Market Intelligence*
• Current crop prices
• Market trends
• Price alerts

*Quick Start:*
• Type "weather 390001" for weather
• Type "fertilizer wheat" for advice
• Type "rice prices" for market info
• Type "help" for all commands

*Natural Language Supported!*
Just ask me normally - "How's the weather?" or "What fertilizer for tomatoes?"

How can I help your farming today? 🚜"""
    
    def get_help_message(self) -> str:
        """Enhanced help message"""
        return """🌾 *Smart Crop Advisory Bot - Help Guide*

*🔥 NATURAL LANGUAGE COMMANDS:*
Just talk to me naturally! I understand:
• "Weather in 390001" 
• "Fertilizer for wheat"
• "Rice market prices"
• "Best crop for my soil"

*⚡ QUICK COMMANDS:*
• `!weather [pincode]` - Weather alerts & farming conditions
• `!crop [N] [P] [K] [pH] [rainfall]` - Crop recommendations  
• `!fertilizer [crop]` - Fertilizer guidance
• `!market [crop]` - Current market prices

*📍 EXAMPLES:*
• `!weather 390001` - Weather for pincode 390001
• `!crop 90 42 43 6.5 120` - Crop suggestion for soil values
• `!fertilizer wheat` - Fertilizer advice for wheat
• `!market tomato` - Current tomato prices

*🎯 SMART FEATURES:*
• Weather-based farming recommendations
• Soil condition analysis
• Market price tracking
• Agricultural alerts
• Multilingual support (Hindi/English)

*💡 TIP:* I understand farming questions in simple language. Just ask naturally!

Type any command or question to get started! 🚀"""
    
    # Include all the existing command handlers from the original file
    def handle_weather_command(self, message: str) -> str:
        """Handle weather command - keeping existing implementation"""
        try:
            parts = message.split()
            if len(parts) < 2:
                return """🌤️ *Weather Information*

Please provide your pincode:
`!weather [pincode]` or just "weather [pincode]"

Example: `!weather 390001` or "weather in 390001"

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
                
                if conditions:
                    response_text += f"\n*🌾 Farming Conditions:*\n"
                    response_text += f"• Overall: {conditions.get('overall', 'N/A')}\n"
                    response_text += f"• Best Hours: {conditions.get('best_farming_hours', 'N/A')}"
                
                response_text += f"\n\n📅 *Updated:* {datetime.now().strftime('%I:%M %p')}"
                return response_text
                
            else:
                return f"❌ Weather service error. Please try again later."
                
        except Exception as e:
            return f"❌ Error getting weather data: {str(e)}"
    
    def handle_crop_command(self, message: str) -> str:
        """Handle crop recommendation command"""
        try:
            parts = message.split()
            if len(parts) < 6:
                return """🌱 *Crop Recommendation*

Please provide soil parameters:
`!crop [N] [P] [K] [pH] [rainfall]`

Example: `!crop 90 42 43 6.5 120`
• N = Nitrogen level
• P = Phosphorus level  
• K = Potassium level
• pH = Soil pH value
• Rainfall = Annual rainfall (mm)

I'll recommend the best crops for your soil conditions."""
            
            try:
                n = float(parts[1])
                p = float(parts[2])
                k = float(parts[3])
                ph = float(parts[4])
                rainfall = float(parts[5])
            except ValueError:
                return "❌ Please provide valid numeric values for soil parameters."
            
            # Call API
            response = requests.post(f"{self.api_base}/api/crop/recommend", json={
                "nitrogen": n,
                "phosphorus": p,
                "potassium": k,
                "ph": ph,
                "rainfall": rainfall
            })
            
            if response.status_code == 200:
                data = response.json()
                crop = data.get("recommended_crop", "Unknown")
                confidence = data.get("confidence", 0)
                
                response_text = f"""🌱 *Crop Recommendation*

*🎯 Recommended Crop:* *{crop.title()}*
*📊 Confidence:* {confidence:.1%}

*📋 Your Soil Analysis:*
• Nitrogen (N): {n}
• Phosphorus (P): {p}  
• Potassium (K): {k}
• pH Level: {ph}
• Rainfall: {rainfall}mm

*💡 Why {crop}?*
Based on your soil conditions, {crop} is most suitable for optimal yield and growth.

*📞 Next Steps:*
• `!fertilizer {crop}` - Get fertilizer advice
• `!weather [pincode]` - Check farming conditions
• `!market {crop}` - Check current prices"""
                
                return response_text
            else:
                return "❌ Unable to get crop recommendation. Please try again."
                
        except Exception as e:
            return f"❌ Error processing crop recommendation: {str(e)}"
    
    def handle_fertilizer_command(self, message: str) -> str:
        """Handle fertilizer recommendation command"""
        try:
            parts = message.split()
            if len(parts) < 2:
                return """🌿 *Fertilizer Guidance*

Please specify the crop:
`!fertilizer [crop]` or "fertilizer for [crop]"

Example: `!fertilizer wheat`

Popular crops: wheat, rice, corn, tomato, potato, cotton, sugarcane"""
            
            crop = parts[1].lower()
            
            # Call API
            response = requests.get(f"{self.api_base}/fertilizer", params={"crop": crop})
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    return f"❌ {data['error']}"
                
                response_text = f"""🌿 *Fertilizer Guide for {crop.title()}*

*🧪 Recommended Fertilizers:*
"""
                
                fertilizers = data.get("fertilizers", [])
                for fert in fertilizers[:3]:  # Limit to 3
                    response_text += f"• {fert}\n"
                
                if data.get("organic_options"):
                    response_text += f"\n*🌱 Organic Options:*\n"
                    for organic in data.get("organic_options", [])[:2]:
                        response_text += f"• {organic}\n"
                
                if data.get("application_timing"):
                    response_text += f"\n*📅 Best Application Time:*\n{data['application_timing']}"
                
                if data.get("dosage"):
                    response_text += f"\n*⚖️ Recommended Dosage:*\n{data['dosage']}"
                
                response_text += f"\n\n*💡 Tip:* Always test soil before applying fertilizers for best results."
                
                return response_text
            else:
                return f"❌ Fertilizer information not available for {crop}. Try common crops like wheat, rice, tomato."
                
        except Exception as e:
            return f"❌ Error getting fertilizer information: {str(e)}"
    
    def handle_market_command(self, message: str) -> str:
        """Handle market prices command"""
        try:
            parts = message.split()
            if len(parts) < 2:
                return """💰 *Market Prices*

Please specify the crop:
`!market [crop]` or "[crop] prices"

Example: `!market tomato`

Popular crops: wheat, rice, tomato, onion, potato, cotton, sugarcane"""
            
            crop = parts[1].lower()
            
            # Call API
            response = requests.get(f"{self.api_base}/market", params={"crop": crop})
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    return f"❌ {data['error']}"
                
                response_text = f"""💰 *Market Prices for {crop.title()}*

*📊 Current Prices:*
• Minimum: ₹{data.get('min_price', 'N/A')} per quintal
• Maximum: ₹{data.get('max_price', 'N/A')} per quintal  
• Average: ₹{data.get('avg_price', 'N/A')} per quintal

*📈 Market Trend:* {data.get('trend', 'Stable')}

*📍 Major Markets:*
"""
                
                markets = data.get("markets", [])
                for market in markets[:3]:  # Limit to 3
                    response_text += f"• {market.get('name', 'Unknown')}: ₹{market.get('price', 'N/A')}/quintal\n"
                
                if data.get("recommendation"):
                    response_text += f"\n*💡 Recommendation:*\n{data['recommendation']}"
                
                response_text += f"\n\n📅 *Last Updated:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
                
                return response_text
            else:
                return f"❌ Market price information not available for {crop}. Try common crops like wheat, rice, tomato."
                
        except Exception as e:
            return f"❌ Error getting market information: {str(e)}"

# Create backward compatibility alias
WhatsAppMessageProcessor = EnhancedWhatsAppMessageProcessor
