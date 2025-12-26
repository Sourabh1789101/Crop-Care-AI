# 🌾 Crop Care AI - Smart Agricultural Advisory System

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.2-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![PWA](https://img.shields.io/badge/PWA-Ready-purple)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A comprehensive, low-cost agricultural advisory system designed for small and marginal farmers. This system provides **crop recommendations**, **fertilizer guidance**, **disease detection**, **weather alerts**, and **market price information** through an intuitive Progressive Web App (PWA).

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌱 **Crop Recommendation** | Get optimal crop suggestions based on soil parameters (N, P, K, pH, rainfall) |
| 🧪 **Fertilizer Advisory** | Personalized fertilizer plans with dosage recommendations |
| 🦠 **Disease Detection** | Upload plant images for disease analysis and remedies |
| 🌤️ **Weather Alerts** | Real-time weather data with agricultural advisories |
| 💰 **Market Prices** | Current crop prices from APMC markets |
| 🎙️ **Voice Interface** | Hands-free navigation using voice commands |
| 📱 **Offline Support** | Works offline as a Progressive Web App |

---

## 📁 Project Structure

```
Crop-Care-AI/
├── 📂 api/                      # Vercel Serverless API
│   ├── index.py                 # Main API endpoints
│   └── requirements.txt         # API dependencies
│
├── 📂 frontend/                 # Progressive Web App
│   ├── index.html               # Main HTML entry
│   ├── app.js                   # Application logic
│   ├── styles.css               # Styling
│   ├── manifest.json            # PWA manifest
│   ├── service-worker.js        # Offline caching
│   └── 📂 components/           # UI Components
│       ├── CropAdvisor.js       # Crop recommendation UI
│       ├── FertilizerAdvisor.js # Fertilizer guidance UI
│       ├── DiseaseDetector.js   # Disease detection UI
│       ├── WeatherAlert.js      # Weather alerts UI
│       └── MarketPrices.js      # Market prices UI
│
├── 📂 services/                 # Backend Services (Development)
│   ├── app.py                   # Full-featured FastAPI app
│   ├── run_server.py            # Server startup script
│   ├── requirements.txt         # Backend dependencies
│   ├── 📂 utils/                # Utility modules
│   │   ├── soil_helper.py       # Soil analysis logic
│   │   ├── weather_api.py       # Weather API integration
│   │   └── market_api.py        # Market data utilities
│   └── 📂 sample_data/          # Sample datasets
│       └── crop_reco_sample.csv # Training data sample
│
├── 📂 docs/                     # Documentation
│   └── README.md                # Additional docs
│
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── index.html                   # Root redirect
├── package.json                 # Project metadata
├── requirements.txt             # Python dependencies
├── setup.bat                    # Windows setup script
├── setup.sh                     # Linux/Mac setup script
├── test_api.py                  # API test suite
└── vercel.json                  # Vercel deployment config
```

---

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn ASGI
- **Validation:** Pydantic
- **Image Processing:** Pillow
- **Numerical Computing:** NumPy

### Frontend
- **Type:** Progressive Web App (PWA)
- **Languages:** HTML5, CSS3, JavaScript (ES6+)
- **Features:** Service Workers, Web Speech API
- **Design:** Responsive, Mobile-first, Dark Theme

### External APIs
- **Weather:** OpenWeatherMap API
- **Market Data:** Mock data (ready for Agmarknet/eNAM integration)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Setup

**Windows:**
```bash
git clone https://github.com/Sourabh1789101/Crop-Care-AI.git
cd Crop-Care-AI
setup.bat
```

**Linux/Mac:**
```bash
git clone https://github.com/Sourabh1789101/Crop-Care-AI.git
cd Crop-Care-AI
chmod +x setup.sh && ./setup.sh
```

### Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/Sourabh1789101/Crop-Care-AI.git
cd Crop-Care-AI

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env and add your API keys (optional)

# 6. Start the backend server
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# 7. Start the frontend (new terminal)
cd frontend
python -m http.server 3000
```

---

## 💻 Usage

### Access Points
| Service | URL |
|---------|-----|
| Frontend (PWA) | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |

### Using the Features

1. **Crop Recommendation**
   - Enter soil parameters: N, P, K (kg/ha), pH, Rainfall (mm)
   - Click "Recommend Crop" to get suggestions

2. **Fertilizer Advisory**
   - Select crop type
   - Enter soil parameters
   - Get personalized fertilizer plan

3. **Disease Detection**
   - Upload a plant leaf image
   - Receive disease diagnosis and remedies

4. **Weather Alerts**
   - Enter PIN code
   - View weather data and agricultural advisories

5. **Market Prices**
   - Enter crop name (optional)
   - View current market prices

---

## 📖 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/recommend_crop` | POST | Crop recommendation |
| `/recommend_fertilizer` | POST | Fertilizer guidance |
| `/detect_disease` | POST | Disease detection |
| `/weather` | GET | Weather data |
| `/market` | GET | Market prices |
| `/docs` | GET | Interactive API docs |

### Example Requests

**Crop Recommendation:**
```bash
curl -X POST http://localhost:8000/recommend_crop \
  -H "Content-Type: application/json" \
  -d '{"N": 90, "P": 42, "K": 43, "ph": 6.5, "rainfall": 120}'
```

**Fertilizer Advisory:**
```bash
curl -X POST http://localhost:8000/recommend_fertilizer \
  -H "Content-Type: application/json" \
  -d '{"N": 90, "P": 42, "K": 43, "ph": 6.5, "crop": "wheat"}'
```

**Weather Data:**
```bash
curl "http://localhost:8000/weather?pincode=390001"
```

**Market Prices:**
```bash
curl "http://localhost:8000/market?crop=wheat"
```

---

## 🌐 Deployment

### Vercel (Recommended)

1. Fork this repository
2. Connect to Vercel
3. Deploy with default settings
4. Add environment variables in Vercel dashboard

### Manual Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Optional |
| `API_BASE` | Backend API URL | Optional |

Get your free API key from [OpenWeatherMap](https://openweathermap.org/api).

---

## 🧪 Testing

```bash
# Run API tests
python test_api.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Sourabh** - *Initial Development* - [GitHub](https://github.com/Sourabh1789101)

---

## 🙏 Acknowledgments

- OpenWeatherMap for weather API
- FastAPI for the excellent framework
- All contributors and supporters

---

<p align="center">
  Made with ❤️ for Indian Farmers
</p>
