import os
import json
from typing import Any, Dict

import httpx
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Crop-Care-AI Telegram Bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")  # optional
API_GATEWAY_INTERNAL_URL = os.getenv("API_GATEWAY_INTERNAL_URL", "http://api-gateway:8080")
TG_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def t_send_text(chat_id: int, text: str) -> Dict[str, Any]:
    with httpx.Client(timeout=20) as client:
        r = client.post(f"{TG_BASE}/sendMessage", json={"chat_id": chat_id, "text": text})
        r.raise_for_status()
        return r.json()


async def handle_text(chat_id: int, text: str):
    t = text.strip().lower()
    if t == "help":
        t_send_text(chat_id, "Commands:\n- ping\n- yield: {json}\n- send a photo to detect disease (coming soon)")
        return
    if t == "ping":
        t_send_text(chat_id, "pong")
        return
    if t.startswith("yield:"):
        try:
            payload_str = text[text.index(":") + 1:].strip()
            data = json.loads(payload_str)
        except Exception as e:
            t_send_text(chat_id, f"Invalid JSON after 'yield:'. Error: {e}")
            return
        try:
            with httpx.Client(timeout=60) as client:
                resp = client.post(f"{API_GATEWAY_INTERNAL_URL}/api/v1/yields/predict", json=data)
                if resp.status_code >= 400:
                    t_send_text(chat_id, f"Prediction error: {resp.text}")
                    return
                pr = resp.json()
                py = pr.get("predicted_yield", {})
                value = py.get("value")
                unit = py.get("unit", "tonnes/ha")
                lb = py.get("lower_bound")
                ub = py.get("upper_bound")
                t_send_text(chat_id, f"Predicted yield: {value} {unit} (range {lb}-{ub}).")
        except Exception as e:
            t_send_text(chat_id, f"Service error: {e}")
        return
    t_send_text(chat_id, "Unrecognized command. Send 'help' for options.")


@app.post("/webhook")
async def webhook(request: Request, x_telegram_bot_api_secret_token: str | None = Header(default=None)):
    if TELEGRAM_WEBHOOK_SECRET:
        if x_telegram_bot_api_secret_token != TELEGRAM_WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Invalid webhook secret")
    update = await request.json()
    try:
        message = update.get("message") or update.get("edited_message") or {}
        if message:
            chat_id = message["chat"]["id"]
            if "text" in message:
                await handle_text(chat_id, message["text"])
            elif "photo" in message:
                t_send_text(chat_id, "Image detection coming soon. Please use the web app for now.")
        else:
            # Handle callbacks, etc., as needed
            pass
    except Exception as e:
        return JSONResponse({"status": "ignored", "error": str(e)}, status_code=200)
    return JSONResponse({"status": "ok"}, status_code=200)
