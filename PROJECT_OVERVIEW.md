# Smart Crop Advisory - Complete Project Overview

## 🎯 Project Description
SmartCropAdvisory is a comprehensive agricultural advisory system designed for small and marginal farmers. It provides:
- **Crop Recommendation** based on soil parameters
- **Fertilizer Guidance** with soil-specific adjustments
- **Disease Detection** through image analysis (basic implementation)
- **Weather Alerts** for farming decisions
- **Market Price Information** for better crop planning

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11
- **Features**: 
  - RESTful API endpoints
  - Optional ML model integration
  - Weather API integration (OpenWeather)
  - Mock market price data
  - Image processing for disease detection

### Frontend (PWA)
- **Technology**: Vanilla JavaScript, Progressive Web App
- **Features**:
  - Offline support with Service Worker
  - Voice input capability
  - Responsive design
  - Dark theme optimized for mobile

### Chatbot (Telegram)
- **Platform**: Telegram Bot API
- **Features**: Text-based interaction with all backend services

## 📁 Project Structure
```
SmartCropAdvisory/
├── backend/
│   ├── app.py                    # Main FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── models/                   # ML models (to be added)
│   ├── utils/
│   │   ├── soil_helper.py        # Soil analysis utilities
│   │   ├── weather_api.py        # Weather service integration
│   │   └── market_api.py         # Market price utilities
│   └── sample_data/
│       └── crop_reco_sample.csv  # Sample training data
├── frontend/
│   ├── index.html                # Main HTML file
│   ├── app.js                    # Main application logic
│   ├── styles.css                # Styling
│   ├── service-worker.js         # PWA service worker
│   ├── manifest.json             # PWA manifest
│   └── components/               # UI components
│       ├── CropAdvisor.js
│       ├── FertilizerAdvisor.js
│       ├── DiseaseDetector.js
│       ├── WeatherAlert.js
│       └── MarketPrices.js
├── chatbot/
│   └── telegram_bot.py           # Telegram bot implementation
├── deploy/
│   ├── Dockerfile                # Container deployment
│   └── serverless.yml            # Serverless deployment
├── docs/
│   ├── README.md                 # Main documentation
│   └── SIH_submission.md         # Hackathon submission details
├── .env.example                  # Environment variables template
├── setup.sh                     # Unix setup script
└── setup.bat                    # Windows setup script
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js (for frontend serving)
- OpenWeather API key (optional)
- Telegram Bot Token (optional)

### Setup Steps

1. **Clone and Setup**
   ```bash
   # Windows
   setup.bat
   
   # Linux/Mac
   chmod +x setup.sh && ./setup.sh
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your API keys (optional for basic functionality)

3. **Start Backend**
   ```bash
   uvicorn backend.app:app --reload
   ```

4. **Start Frontend**
   ```bash
   npx serve frontend
   ```

5. **Start Telegram Bot (Optional)**
   ```bash
   python chatbot/telegram_bot.py
   ```

## 🔧 Configuration

### Environment Variables
- `OPENWEATHER_API_KEY`: Weather service integration
- `TELEGRAM_BOT_TOKEN`: Telegram bot functionality
- `API_BASE`: Backend URL for chatbot

### ML Models (Optional)
Place trained models in `backend/models/`:
- `crop_model.pkl`: Crop recommendation model
- `fertilizer_model.pkl`: Fertilizer recommendation model

## 📱 Features Overview

### 1. Crop Recommendation
- Input: N, P, K, pH, rainfall
- Output: Recommended crop with confidence score
- Fallback: Heuristic-based recommendation

### 2. Fertilizer Advisory
- Input: Crop type + soil parameters
- Output: Customized fertilizer plan
- Features: Base recommendations + soil-specific adjustments

### 3. Disease Detection
- Input: Plant image upload
- Output: Disease classification + treatment recommendation
- Current: Basic heuristic (placeholder for ML model)

### 4. Weather Alerts
- Input: PIN code
- Output: Current weather + farming alerts
- Alerts: Rain, wind, temperature warnings

### 5. Market Prices
- Input: Crop name (optional)
- Output: Current market prices
- Current: Mock data (placeholder for real API)

## 🌐 API Endpoints

### Core Endpoints
- `POST /recommend_crop` - Crop recommendation
- `POST /recommend_fertilizer` - Fertilizer guidance
- `POST /detect_disease` - Disease detection
- `GET /weather?pincode={code}` - Weather information
- `GET /market?crop={name}` - Market prices
- `GET /health` - System health check
- `GET /languages` - Supported languages

## 🚀 Deployment Options

### 1. Docker Container
```bash
docker build -t sca-backend -f deploy/Dockerfile .
docker run -p 8000:8000 sca-backend
```

### 2. Serverless (AWS Lambda)
```bash
serverless deploy
```

### 3. Traditional Hosting
- Deploy backend on any Python hosting platform
- Serve frontend as static files

## 🎯 Target Users
- Small and marginal farmers
- Agricultural extension workers
- Agricultural cooperatives
- Rural development organizations

## 💡 Key Benefits
1. **Low Cost**: Minimal infrastructure requirements
2. **Offline Capable**: PWA works without constant internet
3. **Multi-Platform**: Web, mobile, and chat interfaces
4. **Extensible**: Easy to add new features and models
5. **Scalable**: From local deployment to cloud scale

## 🔮 Future Enhancements
1. **ML Model Integration**: Replace heuristics with trained models
2. **Real Market Data**: Integrate with official market APIs
3. **Multilingual Support**: Add regional language support
4. **IoT Integration**: Connect with soil sensors
5. **Farmer Network**: Social features and knowledge sharing

## 📞 Support
For technical support or questions about implementation, refer to the documentation in the `docs/` folder or check the inline code comments.

---
**Note**: This is a prototype implementation suitable for hackathons and demonstration purposes. For production use, implement proper security, authentication, and error handling mechanisms.
