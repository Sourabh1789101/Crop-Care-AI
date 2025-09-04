import os
import json
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse

app = FastAPI(title="Crop-Care-AI WhatsApp Bot")

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
API_GATEWAY_INTERNAL_URL = os.getenv("API_GATEWAY_INTERNAL_URL", "http://api-gateway:8080")

GRAPH_BASE = "https://graph.facebook.com/v17.0"


def w_send_text(to: str, text: str) -> Dict[str, Any]:
    url = f"{GRAPH_BASE}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": text}
    }
    with httpx.Client(timeout=20) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()


async def handle_text_message(from_number: str, text: str) -> None:
    t = text.strip().lower()
    if t == "help":
        msg = (
            "Crop-Care-AI Help:\n"
            "- Send 'ping' -> pong\n"
            "- Send 'yield: {json}' to get yield prediction.\n"
            "  Example:\n"
            "  yield: {\"crop_type\":\"rice\",\"soil_data\":{\"nitrogen\":40,\"phosphorus\":30,\"potassium\":40,\"ph\":6.5},\"weather_data\":{\"average_temperature\":25,\"total_rainfall\":1000,\"average_humidity\":60}}\n"
            "- Send an image (coming soon) to detect disease."
        )
        w_send_text(from_number, msg)
        return
    if t == "ping":
        w_send_text(from_number, "pong")
        return
    if t.startswith("yield:"):
        try:
            payload_str = text[text.index(":") + 1:].strip()
            data = json.loads(payload_str)
        except Exception as e:
            w_send_text(from_number, f"Invalid JSON after 'yield:'. Error: {e}")
            return
        # Call gateway
        try:
            with httpx.Client(timeout=60) as client:
                resp = client.post(f"{API_GATEWAY_INTERNAL_URL}/api/v1/yields/predict", json=data)
                if resp.status_code >= 400:
                    w_send_text(from_number, f"Prediction error: {resp.text}")
                    return
                pr = resp.json()
                py = pr.get("predicted_yield", {})
                value = py.get("value")
                unit = py.get("unit", "tonnes/ha")
                lb = py.get("lower_bound")
                ub = py.get("upper_bound")
                w_send_text(from_number, f"Predicted yield: {value} {unit} (range {lb}-{ub}).")
        except Exception as e:
            w_send_text(from_number, f"Service error: {e}")
        return

    # default
    w_send_text(from_number, "Unrecognized command. Send 'help' for options.")


@app.get("/webhook", response_class=PlainTextResponse)
async def verify(request: Request):
    # Meta verification
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN and challenge:
        return PlainTextResponse(content=challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    # Expect standard WhatsApp webhook payload
    try:
        entry = body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        for m in messages:
            from_number = m.get("from")
            mtype = m.get("type")
            if mtype == "text":
                text = m.get("text", {}).get("body", "")
                await handle_text_message(from_number, text)
            elif mtype in {"image", "document"}:
                # TODO: Implement media download using Media API, then forward to disease detection
                w_send_text(from_number, "Image detection coming soon. Please use the web app for now.")
            else:
                w_send_text(from_number, "Unsupported message type.")
    except Exception as e:
        # Do not fail webhook; log in real system
        return JSONResponse({"status": "ignored", "error": str(e)}, status_code=200)
    return JSONResponse({"status": "ok"}, status_code=200)
