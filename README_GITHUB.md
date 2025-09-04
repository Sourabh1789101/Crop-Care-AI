# 🌾 Smart Crop Advisory System

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/YOUR_USERNAME/crop-care-ai-system)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2Fcrop-care-ai-system)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.2-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![PWA](https://img.shields.io/badge/PWA-Ready-purple)](https://web.dev/progressive-web-apps/)

**AI-powered agricultural assistance system for farmers** - Providing crop recommendations, disease detection, weather alerts, and market prices through a modern web interface.

## ✨ Features

- 🌱 **Crop Recommendation** - AI-based suggestions based on soil parameters
- 🦠 **Disease Detection** - Image-based plant disease identification
- 🌦️ **Weather Alerts** - Agricultural weather information and alerts
- 💰 **Market Prices** - Real-time crop market pricing data
- 📱 **Progressive Web App** - Works offline and can be installed on mobile
- 🤖 **Multi-platform Bots** - WhatsApp and Telegram integration
- 🎤 **Voice Interface** - Speech recognition for hands-free operation

## 🚀 Quick Deploy

### Deploy to Vercel (1-click)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2Fcrop-care-ai-system)

### Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/crop-care-ai-system.git
cd crop-care-ai-system

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start the server
cd services
python run_server.py
```

## 📁 Project Structure

```
crop-care-ai-system/
├── 🖥️ frontend/           # Progressive Web App
│   ├── index.html         # Main interface
│   ├── app.js            # Frontend logic
│   └── components/       # Modular components
├── 🔧 api/               # Vercel serverless functions
│   └── index.py          # API entry point
├── 🚀 services/          # Backend services
│   ├── app.py           # FastAPI application
│   ├── utils/           # Utility modules
│   └── *-bot/           # Bot integrations
├── 📋 vercel.json        # Vercel deployment config
└── 📦 requirements.txt   # Python dependencies
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/recommend_crop` | POST | Get crop recommendations |
| `/recommend_fertilizer` | POST | Get fertilizer advice |
| `/detect_disease` | POST | Detect plant diseases |
| `/weather` | GET | Weather information |
| `/market` | GET | Market prices |
| `/docs` | GET | Interactive API documentation |

## 🔧 Environment Variables

For full functionality, set these environment variables:

```bash
OPENWEATHER_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token_here
```

## 🎯 Usage Examples

### Crop Recommendation
```python
import requests

data = {
    "N": 90,      # Nitrogen
    "P": 42,      # Phosphorus  
    "K": 43,      # Potassium
    "ph": 6.5,    # Soil pH
    "rainfall": 120  # Rainfall in mm
}

response = requests.post("https://your-app.vercel.app/api/recommend_crop", json=data)
print(response.json())  # {"crop": "wheat", "confidence": 0.85}
```

### Disease Detection
```python
import requests

files = {"file": open("plant_image.jpg", "rb")}
response = requests.post("https://your-app.vercel.app/api/detect_disease", files=files)
print(response.json())
```

## 📱 Bot Integration

### WhatsApp Bot
Send messages to your WhatsApp Business number:
- "recommend crop for pH 6.5"
- "weather for 560001"
- "market prices for rice"

### Telegram Bot
Use @YourBotName on Telegram with commands:
- `/crop` - Get crop recommendations
- `/weather <pincode>` - Weather information
- `/market <crop>` - Market prices

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- Built for farmers and agricultural communities
- Powered by FastAPI and modern web technologies
- Deployed on Vercel for global accessibility
- AI models for crop and disease prediction

## 📞 Support

- 📧 Email: support@crop-care-ai.com
- 📝 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/crop-care-ai-system/issues)
- 📖 Documentation: [Wiki](https://github.com/YOUR_USERNAME/crop-care-ai-system/wiki)

---

⭐ **Star this repository if it helped you!** ⭐
