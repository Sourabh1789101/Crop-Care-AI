#!/usr/bin/env python3
"""
Test WhatsApp Connection and Send Smart Crop Advisory Welcome Message
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_whatsapp_message():
    """Test sending WhatsApp message with Smart Crop Advisory bot"""
    
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    
    print("🤖 Testing Smart Crop Advisory WhatsApp Bot")
    print("="*60)
    print(f"📱 Phone Number ID: {phone_number_id}")
    print(f"🔑 Access Token: {access_token[:20] if access_token else 'None'}...")
    
    if not access_token or not phone_number_id:
        print("❌ WhatsApp credentials not found in .env file")
        return False
    
    # Test phone number (the one from your curl command)
    test_phone = "919142685351"  # Your number from the curl command
    
    try:
        url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Send Smart Crop Advisory welcome message
        message_data = {
            "messaging_product": "whatsapp",
            "to": test_phone,
            "type": "text",
            "text": {
                "body": "🌾 Hello! Your Smart Crop Advisory WhatsApp bot is now LIVE!\n\nAvailable commands:\n!help - Show all commands\n!weather 390001 - Get weather\n!crop 90 42 43 6.5 120 - Crop recommendation\n!fertilizer wheat - Fertilizer advice\n!market tomato - Market prices\n\nType any command to get started! 🚀"
            }
        }
        
        print("\n📤 Sending welcome message...")
        print(f"   URL: {url}")
        print(f"   To: {test_phone}")
        
        response = requests.post(url, headers=headers, json=message_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Message sent successfully!")
            print(f"   📨 Message ID: {result.get('messages', [{}])[0].get('id', 'N/A')}")
            print(f"   📱 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"   ❌ Failed to send message")
            print(f"   📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_template_message():
    """Test sending the hello_world template message"""
    
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    test_phone = "919142685351"
    
    try:
        url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Send template message (like your curl command)
        message_data = {
            "messaging_product": "whatsapp",
            "to": test_phone,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                }
            }
        }
        
        print("\n📤 Sending template message (hello_world)...")
        
        response = requests.post(url, headers=headers, json=message_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Template message sent successfully!")
            print(f"   📨 Message ID: {result.get('messages', [{}])[0].get('id', 'N/A')}")
            return True
        else:
            print(f"   ❌ Template message failed")
            print(f"   📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Test template message first (like your curl command)
    if test_template_message():
        print("\n🎉 Template message successful!")
    
    # Test custom Smart Crop Advisory message
    if test_whatsapp_message():
        print("\n🎉 Smart Crop Advisory bot message sent!")
        print("\n📋 Next Steps:")
        print("1. Check your WhatsApp for the message")
        print("2. Set up webhook URL for receiving messages")
        print("3. Test bot commands: !help, !weather, !crop")
        print("4. Your WhatsApp bot is ready for farmers! 🌾")
    else:
        print("\n❌ Message sending failed")
        print("\nTroubleshooting:")
        print("1. Check access token validity")
        print("2. Verify phone number ID")
        print("3. Ensure WhatsApp Business API is properly configured")
