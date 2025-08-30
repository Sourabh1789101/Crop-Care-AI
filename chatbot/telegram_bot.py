import os
import requests
from functools import partial
from typing import Final

# pip install python-telegram-bot==13.15
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_BASE: Final[str] = os.getenv("API_BASE", "http://localhost:8000")
TOKEN: Final[str] = os.getenv("TELEGRAM_BOT_TOKEN", "")

HELP = (
    "Commands:\n"
    "/start - intro\n"
    "/crop N P K pH rainfall - recommend crop (e.g., /crop 90 42 43 6.5 120)\n"
    "/fert crop N P K pH - fertilizer plan (e.g., /fert wheat 90 42 43 6.5)\n"
    "/weather pincode - get weather alerts (e.g., /weather 390001)\n"
    "/market [crop] - mandi prices (e.g., /market wheat)\n"
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Smart Crop Advisory Bot\n" + HELP)

def crop_cmd(update: Update, context: CallbackContext):
    try:
        N, P, K, ph, rainfall = map(float, context.args)
        payload = {"N":N,"P":P,"K":K,"ph":ph,"rainfall":rainfall}
        r = requests.post(f"{API_BASE}/recommend_crop", json=payload, timeout=10)
        update.message.reply_text(r.text)
    except Exception as e:
        update.message.reply_text(f"Usage: /crop N P K pH rainfall\nError: {e}")

def fert_cmd(update: Update, context: CallbackContext):
    try:
        crop = context.args[0]
        N, P, K, ph = map(float, context.args[1:])
        payload = {"crop":crop, "N":N,"P":P,"K":K,"ph":ph}
        r = requests.post(f"{API_BASE}/recommend_fertilizer", json=payload, timeout=10)
        update.message.reply_text(r.text)
    except Exception as e:
        update.message.reply_text(f"Usage: /fert crop N P K pH\nError: {e}")

def weather_cmd(update: Update, context: CallbackContext):
    try:
        pin = context.args[0]
        r = requests.get(f"{API_BASE}/weather", params={"pincode": pin}, timeout=10)
        update.message.reply_text(r.text)
    except Exception as e:
        update.message.reply_text(f"Usage: /weather pincode\nError: {e}")

def market_cmd(update: Update, context: CallbackContext):
    crop = context.args[0] if context.args else None
    r = requests.get(f"{API_BASE}/market", params={"crop": crop} if crop else None, timeout=10)
    update.message.reply_text(r.text)

def main():
    if not TOKEN:
        print("Set TELEGRAM_BOT_TOKEN env var")
        return
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('crop', crop_cmd))
    dp.add_handler(CommandHandler('fert', fert_cmd))
    dp.add_handler(CommandHandler('weather', weather_cmd))
    dp.add_handler(CommandHandler('market', market_cmd))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda u,c: u.message.reply_text(HELP)))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
