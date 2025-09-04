# Vercel Deployment Guide for Crop-Care-AI

## Prerequisites
1. Vercel account (https://vercel.com)
2. GitHub repository with your code
3. Environment variables (API keys)

## Deployment Steps

### 1. Connect to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel
```

### 2. Set Environment Variables
In your Vercel dashboard, add these environment variables:
- `OPENWEATHER_API_KEY`: Your OpenWeather API key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (optional)
- `WHATSAPP_ACCESS_TOKEN`: WhatsApp Business API token (optional)

### 3. Custom Domain (Optional)
Add your custom domain in the Vercel dashboard under Settings > Domains

## Troubleshooting Common Vercel Errors

### FUNCTION_INVOCATION_FAILED (500)
- Check your Python dependencies in requirements.txt
- Ensure all imports are available
- Check function timeout limits

### DEPLOYMENT_NOT_FOUND (404)
- Verify vercel.json routing configuration
- Check build output in deployment logs

### FUNCTION_PAYLOAD_TOO_LARGE (413)
- Reduce image upload size limits
- Implement image compression

### DNS_HOSTNAME_NOT_FOUND (502)
- Check domain configuration
- Verify DNS settings

## File Structure for Vercel
```
crop-care-ai/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── frontend/
│   ├── index.html        # Main frontend
│   ├── app.js           # Frontend logic
│   └── ...
├── services/
│   ├── app.py           # FastAPI application
│   ├── utils/           # Utility modules
│   └── ...
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── package.json         # Node.js package info
```

## Local Testing
```bash
# Test API locally
cd api
python index.py

# Test with Vercel dev server
vercel dev
```

## Production URLs
- Frontend: https://your-app.vercel.app
- API: https://your-app.vercel.app/api/
- Docs: https://your-app.vercel.app/api/docs
