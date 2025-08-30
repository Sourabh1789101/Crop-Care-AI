# Bots Setup (WhatsApp + Telegram)

This guide helps you configure webhooks and tokens for bots.

Prereqs
- Public HTTPS URL for webhooks:
  - Dev: use ngrok (ngrok http 8080) and set PUBLIC_BASE_URL in .env
  - Prod: your Ingress public domain over TLS
- Docker Compose running (bots on ports 8011, 8012 behind gateway 8080)
- API_Gateway proxies:
  - /webhooks/whatsapp -> whatsapp-bot:/webhook
  - /webhooks/telegram -> telegram-bot:/webhook

WhatsApp (Meta WhatsApp Business Cloud API)
1. Create a Meta App and enable WhatsApp
2. Get:
   - WHATSAPP_ACCESS_TOKEN (long-lived)
   - WHATSAPP_PHONE_NUMBER_ID
   - WHATSAPP_VERIFY_TOKEN (choose your own secret)
3. Set environment in deployment/.env
4. Webhook:
   - In Meta App -> WhatsApp -> Configuration:
     - Callback URL: PUBLIC_BASE_URL/webhooks/whatsapp
     - Verify Token: WHATSAPP_VERIFY_TOKEN
   - Subscribe to message categories
5. Test:
   - Send "help" to your WhatsApp business number from a test user added in Meta.

Notes:
- For image detection you must:
  - Read media ID from webhook payload
  - GET media URL (needs app secret proof, or auth header)
  - Download image bytes
  - POST to /api/v1/diseases/detect
  - Reply with prediction
- Ensure your business is approved for “media” permissions in Meta.

Telegram Bot
1. Create bot with @BotFather
   - Get TELEGRAM_BOT_TOKEN
2. Optional: choose TELEGRAM_WEBHOOK_SECRET
3. Set environment in deployment/.env
4. Set webhook:
   - curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
     -H "Content-Type: application/json" \
     -d "{\"url\":\"$PUBLIC_BASE_URL/webhooks/telegram\",\"secret_token\":\"$TELEGRAM_WEBHOOK_SECRET\"}"
5. Test:
   - Open your bot chat, send "help" or "yield: {json}"

Security
- Restrict webhook exposure to HTTPS only
- Validate tokens/secrets
- Consider IP allowlists (Telegram IPs), or WAF for Meta calls

Next Steps
- Implement media handling for disease detection via both bots
- Centralize notification fanout via Redis queues
- Add i18n for farmer languages in responses
