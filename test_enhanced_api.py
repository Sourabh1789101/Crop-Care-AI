import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test the Smart Crop Advisory API with new features
API_BASE = "http://localhost:8000"

print("🧪 Testing Enhanced Smart Crop Advisory API")
print("=" * 50)

def test_basic_endpoints():
    """Test basic API endpoints"""
    print("\n1. Testing Basic Endpoints...")
    
    # Health check
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            data = response.json()
            print(f"   Weather enabled: {data.get('weather', False)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_enhanced_weather():
    """Test enhanced weather API"""
    print("\n2. Testing Enhanced Weather API...")
    
    # Test with demo pincode
    pincode = "390001"  # Vadodara, Gujarat
    
    try:
        response = requests.get(f"{API_BASE}/weather", params={"pincode": pincode})
        if response.status_code == 200:
            print("✅ Enhanced weather API working")
            data = response.json()
            
            if "error" in data:
                print(f"   ⚠️  {data['error']}")
            else:
                print(f"   Location: {data.get('location', 'Unknown')}")
                current = data.get('current_weather', {})
                print(f"   Temperature: {current.get('temperature', 'N/A')}°C")
                print(f"   Alerts: {len(data.get('alerts', []))} found")
                print(f"   Recommendations: {len(data.get('agricultural_recommendations', []))} found")
                
        else:
            print(f"❌ Enhanced weather failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Enhanced weather error: {e}")

def test_whatsapp_endpoints():
    """Test WhatsApp integration endpoints"""
    print("\n3. Testing WhatsApp Integration...")
    
    # Test WhatsApp status
    try:
        response = requests.get(f"{API_BASE}/api/whatsapp/status")
        if response.status_code == 200:
            print("✅ WhatsApp status endpoint working")
            data = response.json()
            print(f"   WhatsApp configured: {data.get('whatsapp_configured', False)}")
            print(f"   Webhook token set: {data.get('webhook_token_set', False)}")
            print(f"   Status: {data.get('status', 'unknown')}")
        else:
            print(f"❌ WhatsApp status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ WhatsApp status error: {e}")

def test_crop_recommendation():
    """Test crop recommendation with enhanced response"""
    print("\n4. Testing Crop Recommendation...")
    
    crop_data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "ph": 6.5,
        "rainfall": 120
    }
    
    try:
        response = requests.post(f"{API_BASE}/recommend_crop", json=crop_data)
        if response.status_code == 200:
            print("✅ Crop recommendation working")
            data = response.json()
            print(f"   Recommended crop: {data.get('crop', 'Unknown')}")
            print(f"   Confidence: {data.get('confidence', 0)*100:.1f}%")
        else:
            print(f"❌ Crop recommendation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Crop recommendation error: {e}")

def test_fertilizer_recommendation():
    """Test fertilizer recommendation"""
    print("\n5. Testing Fertilizer Recommendation...")
    
    fert_data = {
        "crop": "wheat",
        "N": 90,
        "P": 42,
        "K": 43,
        "ph": 6.5
    }
    
    try:
        response = requests.post(f"{API_BASE}/recommend_fertilizer", json=fert_data)
        if response.status_code == 200:
            print("✅ Fertilizer recommendation working")
            data = response.json()
            adjusted = data.get('adjusted', {})
            print(f"   Urea: {adjusted.get('urea', 0)} kg/acre")
            print(f"   DAP: {adjusted.get('dap', 0)} kg/acre")
            print(f"   MOP: {adjusted.get('mop', 0)} kg/acre")
            print(f"   Soil notes: {len(data.get('notes', []))} found")
        else:
            print(f"❌ Fertilizer recommendation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Fertilizer recommendation error: {e}")

def test_market_prices():
    """Test market prices API"""
    print("\n6. Testing Market Prices...")
    
    try:
        response = requests.get(f"{API_BASE}/market")
        if response.status_code == 200:
            print("✅ Market prices working")
            data = response.json()
            results = data.get('results', [])
            print(f"   Found {len(results)} market entries")
            
            # Test specific crop
            response = requests.get(f"{API_BASE}/market", params={"crop": "wheat"})
            if response.status_code == 200:
                wheat_data = response.json()
                wheat_results = wheat_data.get('results', [])
                print(f"   Wheat prices: {len(wheat_results)} entries")
        else:
            print(f"❌ Market prices failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Market prices error: {e}")

def print_setup_instructions():
    """Print setup instructions for APIs"""
    print("\n" + "=" * 50)
    print("🔧 SETUP INSTRUCTIONS")
    print("=" * 50)
    
    print("\n📋 To enable full functionality:")
    
    print("\n1. Weather API Setup:")
    print("   • Go to: https://openweathermap.org/api")
    print("   • Sign up for free account")
    print("   • Get your API key")
    print("   • Add to .env: OPENWEATHER_API_KEY=your_key_here")
    
    print("\n2. WhatsApp API Setup (Choose one):")
    print("   Option A - Meta WhatsApp Business API (Free but complex):")
    print("   • Go to: https://developers.facebook.com/")
    print("   • Create app and get WhatsApp Business API")
    print("   • Add to .env:")
    print("     WHATSAPP_ACCESS_TOKEN=your_token")
    print("     WHATSAPP_PHONE_NUMBER_ID=your_phone_id")
    print("     WHATSAPP_VERIFY_TOKEN=your_verify_token")
    
    print("   Option B - Twilio WhatsApp API (Easy but paid):")
    print("   • Go to: https://twilio.com/whatsapp")
    print("   • Set up WhatsApp sandbox")
    print("   • Get credentials and adapt the code")
    
    print("\n3. Webhook Setup (for WhatsApp):")
    print("   • Your webhook URL: http://your-domain.com/api/whatsapp/webhook")
    print("   • Use ngrok for local testing: ngrok http 8000")
    
    print("\n🚀 Quick Start Commands:")
    print("   • Start backend: uvicorn app:app --reload")
    print("   • Start frontend: python -m http.server 3000")
    print("   • Test APIs: python test_enhanced_api.py")

def main():
    """Run all tests"""
    test_basic_endpoints()
    test_enhanced_weather()
    test_whatsapp_endpoints()
    test_crop_recommendation()
    test_fertilizer_recommendation()
    test_market_prices()
    
    print("\n🎉 API Testing Complete!")
    print(f"\n📱 Frontend: http://localhost:3000")
    print(f"🔧 Backend API: http://localhost:8000")
    print(f"📖 API Docs: http://localhost:8000/docs")
    print(f"🤖 WhatsApp Status: http://localhost:8000/api/whatsapp/status")
    
    # Check if API keys are configured
    openweather_key = os.getenv("OPENWEATHER_API_KEY")
    whatsapp_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    
    if not openweather_key or openweather_key == "demo_key_get_from_openweathermap":
        print("\n⚠️  Weather API not configured - get OpenWeatherMap API key")
    
    if not whatsapp_token or whatsapp_token == "demo_token_get_from_botfather":
        print("⚠️  WhatsApp API not configured - get WhatsApp Business API credentials")
    
    if not openweather_key and not whatsapp_token:
        print_setup_instructions()

if __name__ == "__main__":
    main()
