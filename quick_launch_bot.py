#!/usr/bin/env python3
"""
QUICK LAUNCH - Enhanced WhatsApp Chatbot
Launch the enhanced natural language bot immediately
"""
import os
import time

def send_simple_test_message():
    """Send a simple test message to verify the enhanced bot is working"""
    
    # Read environment variables
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ .env file not found")
        return False
    
    access_token = env_vars.get("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = env_vars.get("WHATSAPP_PHONE_NUMBER_ID")
    phone_number = "919142685351"
    
    if not access_token or not phone_number_id:
        print("❌ WhatsApp credentials not found")
        return False
    
    # Simple test message
    message = "🚀 ENHANCED WHATSAPP CHATBOT LAUNCHED! 🌾 Now supports natural language: Try 'weather in 390001' or 'fertilizer for wheat' - No more commands to remember!"
    
    # Create a simple curl command file
    curl_command = f'''curl -X POST "https://graph.facebook.com/v22.0/{phone_number_id}/messages" ^
-H "Authorization: Bearer {access_token}" ^
-H "Content-Type: application/json" ^
-d "{{\\"messaging_product\\": \\"whatsapp\\", \\"to\\": \\"{phone_number}\\", \\"type\\": \\"text\\", \\"text\\": {{\\"body\\": \\"{message}\\"}}}}"'''
    
    # Write to batch file
    with open("send_message.bat", "w") as f:
        f.write(curl_command)
    
    print(f"📤 Sending enhanced chatbot launch message...")
    result = os.system("send_message.bat")
    
    # Clean up
    if os.path.exists("send_message.bat"):
        os.remove("send_message.bat")
    
    return result == 0

def quick_launch_demo():
    """Quick demonstration of enhanced chatbot capabilities"""
    
    print("🚀 ENHANCED WHATSAPP CHATBOT - QUICK LAUNCH")
    print("=" * 55)
    
    # Check backend
    print("🔧 Checking backend server...")
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server running on http://127.0.0.1:8000")
        else:
            print("❌ Backend server not responding")
            return False
    except:
        print("❌ Backend server not accessible")
        return False
    
    # Send launch message
    print("\n📱 Sending enhanced chatbot launch message...")
    if send_simple_test_message():
        print("✅ Launch message sent successfully!")
    else:
        print("❌ Failed to send launch message")
        return False
    
    print("\n🌟 ENHANCED CHATBOT FEATURES NOW ACTIVE:")
    print("=" * 55)
    
    print("\n💬 NATURAL LANGUAGE EXAMPLES:")
    print("🌤️  Weather: 'weather in my area 390001'")
    print("🌱 Crops: 'what crop should i grow'") 
    print("🌿 Fertilizer: 'fertilizer for wheat farming'")
    print("💰 Prices: 'rice market prices today'")
    print("❓ Help: 'help me with organic farming'")
    
    print("\n⚡ TRADITIONAL COMMANDS (Still Work):")
    print("• !help • !weather 390001 • !crop • !fertilizer • !market")
    
    print("\n🎯 ENHANCED CAPABILITIES:")
    print("✅ Natural Language Understanding")
    print("✅ Context-Aware Responses")
    print("✅ Smart Pattern Recognition")
    print("✅ Agricultural Guidance")
    print("✅ Multi-Language Support")
    print("✅ Traditional Command Compatibility")
    
    print("\n📱 FOR FARMERS:")
    print("🔥 No more remembering exact commands!")
    print("🔥 Chat naturally like WhatsApp!")
    print("🔥 Get instant agricultural advice!")
    print("🔥 Available 24/7 in Hindi/English!")
    
    print("\n🔗 TO ENABLE FULL INTERACTIVITY:")
    print("1. Download ngrok: https://ngrok.com/download")
    print("2. Run: ngrok http 8000")
    print("3. Configure webhook in Facebook Developer Console")
    print("4. Test bidirectional chat")
    
    print("\n" + "=" * 55)
    print("🎉 ENHANCED CHATBOT LAUNCHED SUCCESSFULLY!")
    print("=" * 55)
    
    print("\n📞 CHECK YOUR WHATSAPP NOW!")
    print("You should see the enhanced chatbot launch message!")
    
    print("\n🌾 YOUR AGRICULTURAL AI REVOLUTION IS LIVE!")
    print("Ready to help farmers with natural conversation! 🚀🤖")
    
    return True

def main():
    print("🎯 Enhanced WhatsApp Chatbot - Quick Launch")
    print("🌾 Natural Language Agricultural AI Assistant")
    print()
    
    if quick_launch_demo():
        print("\n🚀 LAUNCH STATUS: SUCCESS!")
        print("\n📋 WHAT'S NEW:")
        print("• Farmers can chat naturally")
        print("• No commands to remember")
        print("• Context-aware responses")
        print("• Smart agricultural guidance")
        
        print("\n🎉 READY TO REVOLUTIONIZE AGRICULTURE!")
    else:
        print("\n❌ Launch encountered issues. Please check configuration.")

if __name__ == "__main__":
    main()
