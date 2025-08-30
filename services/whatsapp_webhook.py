import os
import sys
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
import json
import hashlib
import hmac

# Add parent directory to path to import enhanced service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from enhanced_whatsapp_service import EnhancedWhatsAppMessageProcessor

router = APIRouter()
message_processor = EnhancedWhatsAppMessageProcessor()

@router.get("/whatsapp/webhook")
async def verify_webhook(request: Request):
    """Verify WhatsApp webhook (required by Meta)"""
    try:
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")
        
        verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
        
        if mode == "subscribe" and token == verify_token:
            print("✅ WhatsApp webhook verified successfully")
            return PlainTextResponse(challenge)
        else:
            print("❌ WhatsApp webhook verification failed")
            raise HTTPException(status_code=403, detail="Verification failed")
            
    except Exception as e:
        print(f"❌ Webhook verification error: {e}")
        raise HTTPException(status_code=400, detail="Bad request")

@router.post("/whatsapp/webhook")
async def handle_webhook(request: Request):
    """Handle incoming WhatsApp messages"""
    try:
        # Get request body
        body = await request.body()
        
        # Verify signature (optional but recommended for production)
        signature = request.headers.get("x-hub-signature-256", "")
        if signature and not verify_signature(body, signature):
            raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Parse the message
        data = json.loads(body)
        
        # Process webhook data
        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        if change.get("field") == "messages":
                            process_message_change(change.get("value", {}))
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Webhook handling error: {e}")
        return {"status": "error", "message": str(e)}

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature for security"""
    try:
        app_secret = os.getenv("WHATSAPP_APP_SECRET")
        if not app_secret:
            return True  # Skip verification if no secret set
            
        expected_signature = hmac.new(
            app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    except Exception:
        return False

def process_message_change(value: dict):
    """Process incoming message changes"""
    try:
        messages = value.get("messages", [])
        
        for message in messages:
            message_id = message.get("id")
            from_number = message.get("from")
            timestamp = message.get("timestamp")
            
            print(f"📱 Received message from {from_number}: {message_id}")
            
            # Process the message
            result = message_processor.process_message(message)
            print(f"📤 Response status: {result.get('status')}")
            
    except Exception as e:
        print(f"❌ Message processing error: {e}")

# Additional utility endpoints
@router.get("/whatsapp/status")
async def whatsapp_status():
    """Check WhatsApp integration status"""
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    
    return {
        "whatsapp_configured": bool(access_token and phone_number_id),
        "webhook_token_set": bool(verify_token),
        "status": "ready" if (access_token and phone_number_id and verify_token) else "needs_configuration"
    }

@router.post("/whatsapp/send")
async def send_test_message(phone_number: str, message: str):
    """Send a test message (for debugging)"""
    try:
        from utils.whatsapp_service import WhatsAppService
        service = WhatsAppService()
        result = service.send_text_message(phone_number, message)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
