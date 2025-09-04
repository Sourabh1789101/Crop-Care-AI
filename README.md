# 🌾 Smart Crop Advisory System

[![Status](https://img.shields.io/badge/Status-Active-green)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.2-green)]()
[![PWA](https://img.shields.io/badge/PWA-Ready-purple)]()

A comprehensive, low-cost agricultural advisory system designed for small and marginal farmers. This system provides crop recommendations, fertilizer guidance, disease detection, weather alerts, and market price information through multiple interfaces.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for weather and market data)

### Option 1: Automated Setup (Recommended)
```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh && ./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Create environment file
cp .env.example .env
# Edit .env with your API keys

# 5. Start backend
cd backend
uvicorn app:app --reload

# 6. Start frontend (new terminal)
cd frontend
python -m http.server 3000
```

### Access the Application
- **Frontend (PWA)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 Features

### 🌱 Crop Recommendation
- Input soil parameters (N, P, K, pH, rainfall)
- Get crop recommendations with confidence scores
- Heuristic fallback when ML models aren't available

### 🧪 Fertilizer Advisory
- Personalized fertilizer recommendations
- Soil health analysis
- Corrective measures for nutrient deficiencies

### 🦠 Disease Detection
- Upload plant images for analysis
- Disease classification with remedies
- Placeholder for ML model integration

### 🌤️ Weather Alerts
- Real-time weather data by PIN code
- Agricultural alerts (rain, wind, temperature)
- Integration with OpenWeatherMap API

### 💰 Market Prices
- Current crop prices from APMC markets
- Filter by crop type
- Mock data with real API integration ready

### 🎙️ Voice Interface
- Voice commands for navigation
- Web Speech API integration
- Hands-free operation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (PWA)         │    │   (FastAPI)     │    │   Services      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • HTML/CSS/JS   │◄──►│ • REST API      │◄──►│ • OpenWeather   │
│ • Service Worker│    │ • ML Models     │    │ • Market APIs   │
│ • Voice Input   │    │ • Image Proc.   │    │ • Telegram      │
│ • Offline Cache │    │ • Data Logic    │    │ • (Future)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
SmartCropAdvisory/
├── 📂 backend/                 # FastAPI backend
│   ├── app.py                 # Main application
│   ├── requirements.txt       # Python dependencies
│   ├── 📂 utils/              # Helper modules
│   │   ├── soil_helper.py     # Soil analysis logic
│   │   ├── weather_api.py     # Weather integration
│   │   └── market_api.py      # Market data
│   ├── 📂 models/             # ML models (placeholder)
│   └── 📂 sample_data/        # Sample datasets
├── 📂 frontend/               # Progressive Web App
│   ├── index.html            # Main HTML file
│   ├── app.js                # Main JavaScript
│   ├── styles.css            # Styling
│   ├── service-worker.js     # Offline support
│   ├── manifest.json         # PWA manifest
│   └── 📂 components/        # Modular components
│       ├── CropAdvisor.js    # Crop recommendation UI
│       ├── FertilizerAdvisor.js # Fertilizer UI
│       ├── DiseaseDetector.js # Disease detection UI
│       ├── WeatherAlert.js   # Weather UI
│       └── MarketPrices.js   # Market prices UI
├── 📂 chatbot/               # Telegram bot
│   └── telegram_bot.py       # Bot implementation
├── 📂 deploy/                # Deployment configs
│   ├── Dockerfile           # Container config
│   └── serverless.yml       # Serverless config
├── 📂 docs/                  # Documentation
│   ├── README.md            # Main documentation
│   └── SIH_submission.md    # Hackathon details
├── .env.example             # Environment template
├── start.bat               # Windows start script
├── setup.bat               # Windows setup script
├── setup.sh               # Linux/Mac setup script
└── test_api.py            # API testing script
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/recommend_crop` | POST | Get crop recommendations |
| `/recommend_fertilizer` | POST | Get fertilizer guidance |
| `/detect_disease` | POST | Analyze plant images |
| `/weather` | GET | Weather data and alerts |
| `/market` | GET | Market price information |
| `/languages` | GET | Supported languages |

### Example API Usage

```javascript
// Crop Recommendation
const cropData = {
  "N": 90,
  "P": 42,
  "K": 43,
  "ph": 6.5,
  "rainfall": 120
};

fetch('http://localhost:8000/recommend_crop', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(cropData)
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔑 Environment Variables

```bash
# Required for weather features
OPENWEATHER_API_KEY=your_openweather_api_key

# Required for Telegram bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# API base URL
API_BASE=http://localhost:8000
```

## 🐳 Deployment

### Docker
```bash
# Build image
docker build -t smart-crop-advisory -f deploy/Dockerfile .

# Run container
docker run -p 8000:8000 -e OPENWEATHER_API_KEY=your_key smart-crop-advisory
```

### Serverless (AWS Lambda)
```bash
# Install serverless framework
npm install -g serverless

# Deploy
serverless deploy
```

## 🧪 Testing

Run the API test suite:
```bash
python test_api.py
```

Expected output:
```
🧪 Testing Smart Crop Advisory API
========================================
✅ Health check passed
✅ Crop recommendation passed
✅ Fertilizer recommendation passed
✅ Market prices passed
✅ Languages endpoint passed
🎉 API Testing Complete!
```

## 📱 Progressive Web App Features

- **Offline Support**: Works without internet connection
- **Responsive Design**: Adapts to all screen sizes
- **Voice Input**: Hands-free navigation
- **Camera Integration**: Direct image capture for disease detection
- **Fast Loading**: Optimized for slow networks

## 🤖 Telegram Bot

Start the bot:
```bash
cd chatbot
python telegram_bot.py
```

Bot commands:
- `/start` - Introduction and help
- `/crop N P K pH rainfall` - Crop recommendation
- `/fert crop N P K pH` - Fertilizer guidance
- `/weather pincode` - Weather alerts
- `/market [crop]` - Market prices

## 🔧 Development

### Adding New Features
1. **Backend**: Add endpoints in `backend/app.py`
2. **Frontend**: Create components in `frontend/components/`
3. **Models**: Add ML models to `backend/models/`

### Code Structure
- **Modular Design**: Easy to extend and maintain
- **API-First**: Clear separation of concerns
- **Responsive**: Mobile-first design approach

## 🌟 Future Enhancements

### Short Term
- [ ] Train ML models with real agricultural data
- [ ] Integrate actual market APIs (Agmarknet/eNAM)
- [ ] Add user authentication and profiles
- [ ] Implement data persistence

### Long Term
- [ ] IoT sensor integration
- [ ] Advanced disease detection models
- [ ] Multi-language support
- [ ] Farmer community features
- [ ] Analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check `/docs` folder
- **API Docs**: Visit http://localhost:8000/docs when running

## 🎯 Target Users

- Small and marginal farmers
- Agricultural extension workers
- Rural development organizations
- Agricultural students and researchers

---

**Built with ❤️ for farmers** | **Low-cost • Scalable • Open Source**
# Crop-Care-AI — Farmer-First Microservices

**Enhanced WhatsApp Agricultural AI Assistant with Microservices Architecture**

## 🌾 **Overview**

Crop-Care-AI provides practical decision support for farmers through:
- 📱 **WhatsApp & Telegram Bots** - Natural language agricultural assistance
- 🔍 **Disease Detection** - AI-powered crop disease identification from photos  
- 📊 **Yield Prediction** - Data-driven crop yield forecasting
- 💡 **Smart Recommendations** - Actionable farming advice
- 🌤️ **Weather Integration** - Agricultural weather alerts and insights

## 🏗️ **Architecture**

Microservices-based architecture with independent, scalable services:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WhatsApp Bot  │    │   Telegram Bot   │    │    Web App      │
└─────────┬───────┘    └─────────┬────────┘    └─────────┬───────┘
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      API Gateway        │
                    │        (8080)           │
                    └─────────────┬───────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────▼────────┐    ┌──────────▼───────┐    ┌───────────▼────┐
│ Disease Detect │    │ Yield Prediction │    │ Recommendation │
│     (8001)     │    │      (8002)      │    │     (8003)     │
└────────────────┘    └──────────────────┘    └────────────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                    ┌─────────────▼───────────┐
                    │   MongoDB + Redis       │
                    │   (Data & Cache)        │
                    └─────────────────────────┘
```

## 🚀 **Quick Start**

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for API Gateway)
- Python 3.11+ (for services)

### 1. Clone and Setup
```bash
git clone https://github.com/Sourabh1789101/Crop-Care-AI.git
cd Crop-Care-AI
cp deployment/.env.example deployment/.env
# Edit deployment/.env with your API keys and tokens
```

### 2. Start Services
```bash
cd deployment
docker compose up --build
```

### 3. Access Services
- **API Gateway**: http://localhost:8080
- **Web App**: http://localhost:3000  
- **Disease Detection**: http://localhost:8001
- **Yield Prediction**: http://localhost:8002
- **WhatsApp Bot**: http://localhost:8011
- **Telegram Bot**: http://localhost:8012

## 📱 **Bot Setup**

### WhatsApp Bot
1. Create Meta App with WhatsApp Business API
2. Set environment variables in `deployment/.env`:
   ```
   WHATSAPP_ACCESS_TOKEN=your_token
   WHATSAPP_PHONE_NUMBER_ID=your_id  
   WHATSAPP_VERIFY_TOKEN=your_secret
   ```
3. Configure webhook: `https://your-domain/webhooks/whatsapp`

### Telegram Bot  
1. Create bot with @BotFather
2. Set environment variables:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   ```
3. Set webhook: `https://your-domain/webhooks/telegram`

See [docs/bots/SETUP.md](docs/bots/SETUP.md) for detailed instructions.

## 💬 **Natural Language Examples**

Farmers can chat naturally with the bots:

```
🌤️ "weather in my area 390001"
🌱 "what crop should i grow"  
🌿 "fertilizer for wheat farming"
💰 "rice market prices today"
❓ "help me with organic farming"
```

## 🔧 **Services**

| Service | Port | Purpose |
|---------|------|---------|
| **api-gateway** | 8080 | Request routing & authentication |
| **disease-detection** | 8001 | AI crop disease identification |
| **yield-prediction** | 8002 | Data-driven yield forecasting |
| **recommendation** | 8003 | Actionable farming advice |
| **notification** | 8004 | Push, SMS, and alerts |
| **weather** | 8005 | Agricultural weather data |
| **user-management** | 8006 | Authentication & user profiles |
| **whatsapp-bot** | 8011 | WhatsApp Business API integration |
| **telegram-bot** | 8012 | Telegram Bot API integration |

## 📊 **API Examples**

### Disease Detection
```bash
curl -X POST http://localhost:8080/api/v1/diseases/detect \
  -F "file=@crop_image.jpg"
```

### Yield Prediction  
```bash
curl -X POST http://localhost:8080/api/v1/yields/predict \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "rice",
    "soil_data": {"nitrogen": 40, "phosphorus": 30, "potassium": 40, "ph": 6.5},
    "weather_data": {"average_temperature": 25, "total_rainfall": 1000, "average_humidity": 60}
  }'
```

## 🎯 **Key Features**

- ✅ **Natural Language Processing** - 15+ farming query patterns
- ✅ **Multi-Channel Support** - WhatsApp, Telegram, Web, Mobile
- ✅ **AI Disease Detection** - TensorFlow-based image classification
- ✅ **Smart Yield Prediction** - Scikit-learn models with soil/weather data
- ✅ **Real-time Weather** - Agricultural weather integration
- ✅ **Offline-First Mobile** - Works in low connectivity areas
- ✅ **Scalable Architecture** - Kubernetes-ready microservices
- ✅ **Production Ready** - Docker, CI/CD, monitoring

## 📚 **Documentation**

- [Architecture Overview](docs/architecture/)
- [Bot Setup Guide](docs/bots/SETUP.md)
- [API Documentation](docs/api/)
- [Development Guide](docs/development/)
- [Deployment Guide](docs/deployment/)

## 🌟 **Impact**

**Transforming agriculture through AI-powered assistance accessible via simple WhatsApp chat!**

- 🎯 **Immediate**: Farmers get instant advice
- 🎯 **Scalable**: Ready for thousands of farmers  
- 🎯 **Accessible**: No technical barriers
- 🎯 **Intelligent**: AI-powered recommendations

---

## 📞 **Support**

For issues and questions:
- Create an issue in this repository
- Check [docs/troubleshooting/](docs/troubleshooting/)
- Contact: [your-email@domain.com]

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.
