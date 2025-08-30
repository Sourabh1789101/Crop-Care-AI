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
