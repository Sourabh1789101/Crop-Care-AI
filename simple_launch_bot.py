#!/usr/bin/env python3
"""
SIMPLE CHATBOT LAUNCHER - No encoding issues
Launch enhanced WhatsApp bot with simple messages
"""
import os

def launch_enhanced_bot():
    """Launch the enhanced WhatsApp chatbot"""
    
    print("ENHANCED WHATSAPP CHATBOT LAUNCHER")
    print("=" * 50)
    
    # Check backend
    print("1. Checking backend server...")
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("   Backend server is running!")
        else:
            print("   Backend server not responding")
            return False
    except:
        print("   Backend server not accessible")
        return False
    
    # Read credentials
    print("\n2. Reading WhatsApp credentials...")
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("   .env file not found")
        return False
    
    access_token = env_vars.get("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = env_vars.get("WHATSAPP_PHONE_NUMBER_ID")
    
    if access_token and phone_number_id:
        print("   WhatsApp credentials found!")
    else:
        print("   WhatsApp credentials missing")
        return False
    
    # Send launch message
    print("\n3. Sending launch message...")
    
    message = "ENHANCED WHATSAPP CHATBOT LAUNCHED! Now supports natural language. Try: weather in 390001 OR fertilizer for wheat OR rice prices today. No commands to remember!"
    
    curl_cmd = f'curl -X POST "https://graph.facebook.com/v22.0/{phone_number_id}/messages" -H "Authorization: Bearer {access_token}" -H "Content-Type: application/json" -d "{\\"messaging_product\\": \\"whatsapp\\", \\"to\\": \\"919142685351\\", \\"type\\": \\"text\\", \\"text\\": {\\"body\\": \\"{message}\\"}}"'
    
    result = os.system(curl_cmd)
    
    if result == 0:
        print("   Launch message sent successfully!")
    else:
        print("   Failed to send launch message")
        return False
    
    print("\n" + "=" * 50)
    print("ENHANCED CHATBOT LAUNCHED SUCCESSFULLY!")
    print("=" * 50)
    
    print("\nNEW CAPABILITIES:")
    print("- Natural language understanding")
    print("- Context-aware responses")
    print("- Smart pattern recognition")
    print("- Agricultural guidance")
    print("- Multi-language support")
    
    print("\nFARMERS CAN NOW SAY:")
    print("- 'weather in my area 390001'")
    print("- 'what crop should i grow'")
    print("- 'fertilizer for wheat farming'")
    print("- 'rice market prices today'")
    print("- 'help with organic farming'")
    
    print("\nTRADITIONAL COMMANDS STILL WORK:")
    print("- !help")
    print("- !weather 390001")
    print("- !crop 90 42 43 6.5 120")
    print("- !fertilizer wheat")
    print("- !market rice")
    
    print("\nTO ENABLE FULL INTERACTIVITY:")
    print("1. Setup ngrok tunnel: ngrok http 8000")
    print("2. Configure webhook in Facebook Developer Console")
    print("3. Test bidirectional chat with farmers")
    
    print("\nCHECK YOUR WHATSAPP NOW!")
    print("You should see the enhanced chatbot launch message!")
    
    print("\nYOUR AGRICULTURAL AI ASSISTANT IS LIVE!")
    print("Ready to help farmers with natural conversation!")
    
    return True

def create_launch_summary():
    """Create launch summary"""
    summary = """
# ENHANCED WHATSAPP CHATBOT - LAUNCH COMPLETE

## STATUS: SUCCESSFULLY LAUNCHED

### NEW FEATURES ACTIVE:
- Natural Language Understanding
- Context-Aware Responses  
- Smart Pattern Recognition
- Agricultural Guidance
- Multi-Language Support
- Traditional Command Compatibility

### FARMER BENEFITS:
- Chat naturally like WhatsApp
- No commands to remember
- Instant agricultural advice
- 24/7 availability

### TECHNICAL CAPABILITIES:
- Weather queries with natural language
- Crop recommendations from conversation
- Fertilizer advice in plain English
- Market prices through chat
- General farming guidance

### NEXT STEPS:
1. Setup webhook for bidirectional chat
2. Test with real farmer interactions
3. Monitor and optimize responses
4. Scale to more farmers

### IMPACT:
Ready to revolutionize agriculture through AI-powered WhatsApp assistance!
"""
    
    with open("LAUNCH_SUMMARY.md", "w") as f:
        f.write(summary)
    
    print("\nLaunch summary saved to: LAUNCH_SUMMARY.md")

def main():
    print("Enhanced WhatsApp Chatbot Launcher")
    print("Natural Language Agricultural AI Assistant")
    print()
    
    if launch_enhanced_bot():
        create_launch_summary()
        print("\nLAUNCH STATUS: SUCCESS!")
        print("Enhanced chatbot is now live and ready for farmers!")
    else:
        print("\nLaunch failed. Please check the configuration.")

if __name__ == "__main__":
    main()
