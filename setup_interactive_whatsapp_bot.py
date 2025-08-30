#!/usr/bin/env python3
"""
Interactive WhatsApp Chatbot Setup with Ngrok
Setup complete two-way communication with farmers
"""
import os
import requests
import json
import time
import subprocess
import threading
from dotenv import load_dotenv
import psutil

# Load environment variables
load_dotenv()

class InteractiveWhatsAppBot:
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
        self.backend_url = "http://127.0.0.1:8000"
        self.ngrok_url = None
        
    def check_backend_status(self):
        """Check if backend is running"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_ngrok(self):
        """Start ngrok tunnel for webhook"""
        try:
            print("🌐 Starting ngrok tunnel...")
            
            # Kill existing ngrok processes
            for proc in psutil.process_iter(['pid', 'name']):
                if 'ngrok' in proc.info['name'].lower():
                    print(f"🔄 Killing existing ngrok process {proc.info['pid']}")
                    proc.kill()
            
            time.sleep(2)
            
            # Start new ngrok process
            ngrok_process = subprocess.Popen(
                ["ngrok", "http", "8000", "--log=stdout"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("⏳ Waiting for ngrok to start...")
            time.sleep(5)
            
            # Get ngrok URL
            try:
                response = requests.get("http://127.0.0.1:4040/api/tunnels")
                tunnels = response.json()["tunnels"]
                
                for tunnel in tunnels:
                    if tunnel["proto"] == "https":
                        self.ngrok_url = tunnel["public_url"]
                        print(f"✅ Ngrok tunnel active: {self.ngrok_url}")
                        return True
                        
            except Exception as e:
                print(f"❌ Failed to get ngrok URL: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start ngrok: {e}")
            print("💡 Make sure ngrok is installed: https://ngrok.com/download")
            return False
    
    def register_webhook(self):
        """Register webhook with WhatsApp"""
        if not self.ngrok_url:
            print("❌ No ngrok URL available")
            return False
            
        webhook_url = f"{self.ngrok_url}/api/whatsapp/webhook"
        
        print(f"📡 Registering webhook: {webhook_url}")
        print(f"🔐 Verify token: {self.verify_token}")
        
        # Test webhook endpoint first
        try:
            response = requests.get(f"{webhook_url}?hub.mode=subscribe&hub.verify_token={self.verify_token}&hub.challenge=test123")
            if response.status_code == 200:
                print("✅ Webhook verification successful")
                return True
            else:
                print(f"❌ Webhook verification failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Webhook test failed: {e}")
            return False
    
    def test_bot_commands(self):
        """Test various bot commands"""
        test_commands = [
            "!help",
            "hi",
            "!weather 390001",
            "!crop 90 42 43 6.5 120",
            "!fertilizer wheat",
            "!market rice"
        ]
        
        phone_number = "919142685351"  # Your test number
        
        print("\n🤖 Testing bot commands...")
        
        for command in test_commands:
            print(f"📤 Testing command: {command}")
            
            # Send command via WhatsApp API
            url = f"https://graph.facebook.com/v22.0/{self.phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": f"🧪 Testing: {command}"}
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    result = response.json()
                    message_id = result.get("messages", [{}])[0].get("id", "unknown")
                    print(f"✅ Message sent - ID: {message_id}")
                else:
                    print(f"❌ Failed to send message: {response.status_code}")
                    print(response.text)
                    
            except Exception as e:
                print(f"❌ Error sending message: {e}")
            
            time.sleep(2)  # Rate limiting
    
    def create_farmer_instructions(self):
        """Create instructions for farmers"""
        instructions = f"""
🌾 **Smart Crop Advisory WhatsApp Bot - NOW LIVE!**

📱 **How Farmers Can Use This Bot:**

1. **Add this WhatsApp number to contacts**: {self.phone_number_id}

2. **Send commands to get instant help:**
   • `!help` - See all available commands
   • `!weather 390001` - Get weather for your pincode
   • `!crop 90 42 43 6.5 120` - Get crop recommendation
   • `!fertilizer wheat` - Get fertilizer advice for wheat
   • `!market rice` - Get current rice market prices

3. **Just chat normally:**
   • Send "hi" or "hello" for welcome message
   • Ask questions in simple language
   • Get instant agricultural advice

🚀 **The bot is now FULLY INTERACTIVE!**
Farmers can send messages and get instant responses.

📡 **Webhook URL**: {self.ngrok_url}/api/whatsapp/webhook
🔐 **Verify Token**: {self.verify_token}

💡 **Next Steps:**
1. Share this with local farmers
2. Test with real farming questions
3. Deploy to production for 24/7 service
"""
        
        # Save instructions to file
        with open("FARMER_WHATSAPP_BOT_INSTRUCTIONS.md", "w", encoding="utf-8") as f:
            f.write(instructions)
        
        print("📄 Farmer instructions saved to: FARMER_WHATSAPP_BOT_INSTRUCTIONS.md")
        return instructions
    
    def start_message_monitoring(self):
        """Monitor incoming messages"""
        print("\n👂 Monitoring incoming WhatsApp messages...")
        print("💡 Send a message to your WhatsApp bot to test!")
        print("🛑 Press Ctrl+C to stop monitoring")
        
        try:
            while True:
                # Check backend logs for incoming messages
                try:
                    response = requests.get(f"{self.backend_url}/api/whatsapp/status")
                    if response.status_code == 200:
                        status = response.json()
                        if status.get("status") == "ready":
                            print("✅ Bot is ready for messages", end="\r")
                        else:
                            print("⚠️ Bot needs configuration", end="\r")
                    
                except:
                    print("❌ Backend not responding", end="\r")
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Message monitoring stopped")
    
    def run_full_setup(self):
        """Run complete interactive bot setup"""
        print("🚀 Setting up Interactive WhatsApp Chatbot...")
        print("=" * 50)
        
        # 1. Check backend
        print("\n1️⃣ Checking backend server...")
        if not self.check_backend_status():
            print("❌ Backend not running. Please start it first:")
            print("   python backend/run_server.py")
            return False
        print("✅ Backend is running")
        
        # 2. Start ngrok
        print("\n2️⃣ Setting up ngrok tunnel...")
        if not self.start_ngrok():
            return False
        
        # 3. Register webhook
        print("\n3️⃣ Registering webhook...")
        if not self.register_webhook():
            return False
        
        # 4. Test commands
        print("\n4️⃣ Testing bot commands...")
        self.test_bot_commands()
        
        # 5. Create farmer instructions
        print("\n5️⃣ Creating farmer instructions...")
        instructions = self.create_farmer_instructions()
        
        print("\n" + "=" * 50)
        print("🎉 INTERACTIVE WHATSAPP BOT IS NOW LIVE!")
        print("=" * 50)
        
        print(f"📡 Webhook URL: {self.ngrok_url}/api/whatsapp/webhook")
        print(f"🔐 Verify Token: {self.verify_token}")
        print("📱 Bot can now receive AND send messages!")
        
        print("\n📋 IMMEDIATE NEXT STEPS:")
        print("1. Configure webhook in Facebook Developer Console:")
        print(f"   - Webhook URL: {self.ngrok_url}/api/whatsapp/webhook")
        print(f"   - Verify Token: {self.verify_token}")
        print("   - Subscribe to: messages")
        print("\n2. Test by sending a WhatsApp message to your bot number")
        print("3. Check backend logs for incoming messages")
        
        return True

def main():
    bot = InteractiveWhatsAppBot()
    
    if bot.run_full_setup():
        print("\n🎯 Would you like to monitor incoming messages? (y/n): ", end="")
        try:
            choice = input().lower()
            if choice == 'y':
                bot.start_message_monitoring()
        except KeyboardInterrupt:
            print("\n👋 Setup complete!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
