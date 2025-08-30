#!/usr/bin/env python3
"""
Simple API test to verify the server is running
"""
import requests
import time
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Smart Crop Advisory API")
    print("="*50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    try:
        # Test health endpoint
        print("1. Testing Health Check...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running at http://127.0.0.1:8000")
        print("   Please start the server with: python backend/run_server.py")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
        
    try:
        # Test crop recommendation
        print("\n2. Testing Crop Recommendation...")
        crop_data = {
            "nitrogen": 90,
            "phosphorus": 42,
            "potassium": 43,
            "ph": 6.5,
            "rainfall": 120
        }
        response = requests.post(f"{base_url}/recommend_crop", json=crop_data, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Recommended Crop: {result.get('recommendation', 'N/A')}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        
    try:
        # Test WhatsApp status
        print("\n3. Testing WhatsApp Status...")
        response = requests.get(f"{base_url}/api/whatsapp/status", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   WhatsApp Status: {result.get('status', 'N/A')}")
        else:
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        
    try:
        # Test weather API (will show demo mode)
        print("\n4. Testing Weather API...")
        response = requests.get(f"{base_url}/weather?pincode=390001", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Weather Location: {result.get('location', 'N/A')}")
            print(f"   Temperature: {result.get('temperature', 'N/A')}")
        else:
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 API Testing Complete!")
    print(f"\n📱 View in browser:")
    print(f"   API Docs: {base_url}/docs")
    print(f"   Health: {base_url}/health")
    print(f"   WhatsApp Status: {base_url}/api/whatsapp/status")

if __name__ == "__main__":
    test_api()
