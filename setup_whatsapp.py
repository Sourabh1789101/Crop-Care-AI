#!/usr/bin/env python3
"""
WhatsApp Business API Connection Test and Setup
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_whatsapp_connection():
    """Test WhatsApp Business API connection and get phone number ID"""
    
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    
    if not access_token or access_token.startswith('demo'):
        print("❌ No valid WhatsApp access token found in .env file")
        return False
    
    print("🔗 Testing WhatsApp Business API Connection...")
    print("="*60)
    
    # Test 1: Get WhatsApp Business Account Info
    try:
        print("1. Getting WhatsApp Business Account Info...")
        
        # First, let's get the WhatsApp Business Account ID
        url = f"https://graph.facebook.com/v18.0/me/accounts"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Connection successful!")
            print(f"   📱 Account data: {json.dumps(data, indent=2)}")
            
            # Try to get WhatsApp Business Account
            waba_url = f"https://graph.facebook.com/v18.0/me?fields=whatsapp_business_accounts"
            waba_response = requests.get(waba_url, headers=headers, timeout=10)
            
            if waba_response.status_code == 200:
                waba_data = waba_response.json()
                print(f"   📞 WhatsApp Business Accounts: {json.dumps(waba_data, indent=2)}")
                
                if 'whatsapp_business_accounts' in waba_data:
                    accounts = waba_data['whatsapp_business_accounts']['data']
                    if accounts:
                        waba_id = accounts[0]['id']
                        print(f"   🆔 WhatsApp Business Account ID: {waba_id}")
                        
                        # Get phone numbers for this WABA
                        phones_url = f"https://graph.facebook.com/v18.0/{waba_id}/phone_numbers"
                        phones_response = requests.get(phones_url, headers=headers, timeout=10)
                        
                        if phones_response.status_code == 200:
                            phones_data = phones_response.json()
                            print(f"   📱 Phone numbers: {json.dumps(phones_data, indent=2)}")
                            
                            if 'data' in phones_data and phones_data['data']:
                                phone_number_id = phones_data['data'][0]['id']
                                phone_number = phones_data['data'][0].get('display_phone_number', 'N/A')
                                print(f"\n🎉 SUCCESS! Found WhatsApp Phone Number:")
                                print(f"   📞 Phone Number: {phone_number}")
                                print(f"   🆔 Phone Number ID: {phone_number_id}")
                                
                                # Update .env file with phone number ID
                                update_env_with_phone_id(phone_number_id)
                                return True
                            else:
                                print("   ⚠️  No phone numbers found in the account")
                        else:
                            print(f"   ❌ Failed to get phone numbers: {phones_response.text}")
                    else:
                        print("   ⚠️  No WhatsApp Business Accounts found")
                else:
                    print("   ⚠️  No whatsapp_business_accounts field in response")
            else:
                print(f"   ❌ Failed to get WhatsApp Business Account: {waba_response.text}")
        else:
            print(f"   ❌ Connection failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return False

def update_env_with_phone_id(phone_number_id):
    """Update .env file with the phone number ID"""
    try:
        env_path = "d:\\Testing all inida\\SmartCropAdvisory\\.env"
        
        # Read current .env file
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace the phone number ID
        new_content = content.replace(
            'WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here',
            f'WHATSAPP_PHONE_NUMBER_ID={phone_number_id}'
        )
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            f.write(new_content)
        
        print(f"   ✅ Updated .env file with Phone Number ID: {phone_number_id}")
        
    except Exception as e:
        print(f"   ❌ Failed to update .env file: {e}")

def test_send_message():
    """Test sending a WhatsApp message"""
    
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    
    if not access_token or not phone_number_id or phone_number_id == 'your_phone_number_id_here':
        print("❌ WhatsApp credentials not properly configured")
        return False
    
    print("\n2. Testing WhatsApp Message Sending...")
    
    # Test phone number (replace with your WhatsApp number for testing)
    test_phone = input("   📱 Enter your WhatsApp number (with country code, e.g., +1234567890): ").strip()
    
    if not test_phone:
        print("   ⚠️  No phone number provided, skipping message test")
        return True
    
    try:
        url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Send a test message
        message_data = {
            "messaging_product": "whatsapp",
            "to": test_phone.replace('+', '').replace('-', '').replace(' ', ''),
            "type": "text",
            "text": {
                "body": "🌾 Hello! Your Smart Crop Advisory WhatsApp bot is now connected and working! Type !help to see available commands."
            }
        }
        
        response = requests.post(url, headers=headers, json=message_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Message sent successfully!")
            print(f"   📨 Message ID: {result.get('messages', [{}])[0].get('id', 'N/A')}")
            return True
        else:
            print(f"   ❌ Failed to send message: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error sending message: {e}")
        return False

if __name__ == "__main__":
    print("🤖 WhatsApp Business API Setup and Test")
    print("="*60)
    
    # Test connection and get phone number ID
    if test_whatsapp_connection():
        print("\n✅ WhatsApp Business API connection successful!")
        
        # Reload environment after update
        load_dotenv(override=True)
        
        # Test sending a message
        test_send_message()
        
        print("\n🎉 WhatsApp Setup Complete!")
        print("\n📋 Next Steps:")
        print("1. Restart your backend server to load new credentials")
        print("2. Set up webhook URL in Facebook Developer Console")
        print("3. Test WhatsApp commands: !help, !weather, !crop, etc.")
        
    else:
        print("\n❌ WhatsApp setup failed. Please check your access token and try again.")
        print("\n🔧 Troubleshooting:")
        print("1. Verify your access token is correct")
        print("2. Check that your WhatsApp Business Account is properly set up")
        print("3. Ensure you have the necessary permissions")
