import requests
import json

# Test the Smart Crop Advisory API
API_BASE = "http://localhost:8000"

print("🧪 Testing Smart Crop Advisory API")
print("=" * 40)

# Test 1: Health check
print("\n1. Testing Health Endpoint...")
try:
    response = requests.get(f"{API_BASE}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Health check error: {e}")

# Test 2: Crop recommendation
print("\n2. Testing Crop Recommendation...")
try:
    crop_data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "ph": 6.5,
        "rainfall": 120
    }
    response = requests.post(f"{API_BASE}/recommend_crop", json=crop_data)
    if response.status_code == 200:
        print("✅ Crop recommendation passed")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Crop recommendation failed: {response.status_code}")
except Exception as e:
    print(f"❌ Crop recommendation error: {e}")

# Test 3: Fertilizer recommendation
print("\n3. Testing Fertilizer Recommendation...")
try:
    fert_data = {
        "crop": "wheat",
        "N": 90,
        "P": 42,
        "K": 43,
        "ph": 6.5
    }
    response = requests.post(f"{API_BASE}/recommend_fertilizer", json=fert_data)
    if response.status_code == 200:
        print("✅ Fertilizer recommendation passed")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Fertilizer recommendation failed: {response.status_code}")
except Exception as e:
    print(f"❌ Fertilizer recommendation error: {e}")

# Test 4: Market prices
print("\n4. Testing Market Prices...")
try:
    response = requests.get(f"{API_BASE}/market")
    if response.status_code == 200:
        print("✅ Market prices passed")
        data = response.json()
        print(f"   Found {len(data['results'])} market entries")
        for item in data['results'][:2]:  # Show first 2 items
            print(f"   - {item['crop']}: ₹{item['modal_price']}/{item['unit']} at {item['market']}")
    else:
        print(f"❌ Market prices failed: {response.status_code}")
except Exception as e:
    print(f"❌ Market prices error: {e}")

# Test 5: Languages
print("\n5. Testing Languages Endpoint...")
try:
    response = requests.get(f"{API_BASE}/languages")
    if response.status_code == 200:
        print("✅ Languages endpoint passed")
        data = response.json()
        print(f"   Supported languages: {', '.join(data['supported'])}")
    else:
        print(f"❌ Languages endpoint failed: {response.status_code}")
except Exception as e:
    print(f"❌ Languages endpoint error: {e}")

print("\n🎉 API Testing Complete!")
print("\n📱 Frontend: http://localhost:3000")
print("🔧 Backend API: http://localhost:8000")
print("📖 API Docs: http://localhost:8000/docs")
