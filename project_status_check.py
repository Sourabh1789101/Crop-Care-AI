#!/usr/bin/env python3
"""
Quick Project Status Check
"""
import requests
import time

print("🚀 Smart Crop Advisory Project Status Check")
print("="*60)

# Test Backend
print("1. Testing Backend Server...")
try:
    response = requests.get("http://127.0.0.1:8000/health", timeout=5)
    if response.status_code == 200:
        print("   ✅ Backend: RUNNING on http://127.0.0.1:8000")
        data = response.json()
        print(f"   📊 Status: {data}")
    else:
        print("   ❌ Backend: Not responding properly")
except:
    print("   ❌ Backend: NOT RUNNING")

# Test Frontend
print("\n2. Testing Frontend Server...")
try:
    response = requests.get("http://127.0.0.1:3000", timeout=5)
    if response.status_code == 200:
        print("   ✅ Frontend: RUNNING on http://127.0.0.1:3000")
    else:
        print(f"   ⚠️  Frontend: Status {response.status_code}")
except:
    print("   ❌ Frontend: NOT RUNNING")

# Test WhatsApp Status
print("\n3. Testing WhatsApp Integration...")
try:
    response = requests.get("http://127.0.0.1:8000/api/whatsapp/status", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   📱 WhatsApp Status: {data.get('status', 'unknown')}")
    else:
        print(f"   ❌ WhatsApp: Error {response.status_code}")
except:
    print("   ❌ WhatsApp: Cannot connect")

# Test Key APIs
print("\n4. Testing Agricultural APIs...")
apis = [
    ("/api/crop/recommend", "POST", {"N": 90, "P": 42, "K": 43, "ph": 6.5, "rainfall": 120}),
    ("/weather?pincode=390001", "GET", None),
    ("/fertilizer?crop=wheat", "GET", None),
    ("/market?crop=tomato", "GET", None)
]

for endpoint, method, data in apis:
    try:
        if method == "GET":
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", timeout=5)
        else:
            response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=data, timeout=5)
        
        if response.status_code == 200:
            print(f"   ✅ {endpoint}: Working")
        else:
            print(f"   ⚠️  {endpoint}: Status {response.status_code}")
    except:
        print(f"   ❌ {endpoint}: Failed")

print("\n🎉 PROJECT STATUS SUMMARY:")
print("📱 Frontend: http://127.0.0.1:3000")
print("🔧 Backend API: http://127.0.0.1:8000")
print("📖 API Docs: http://127.0.0.1:8000/docs")
print("🤖 WhatsApp Status: http://127.0.0.1:8000/api/whatsapp/status")

print("\n🌾 Your Smart Crop Advisory system is ready for farmers!")
