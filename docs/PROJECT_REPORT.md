# 📊 Crop Care AI - Project Report

## Project Information

| Field | Details |
|-------|---------|
| **Project Name** | Crop Care AI - Smart Agricultural Advisory System |
| **Version** | 1.0.0 |
| **Date** | December 2025 |
| **Author** | Sourabh |
| **Repository** | https://github.com/Sourabh1789101/Crop-Care-AI |

---

## 1. Executive Summary

Crop Care AI is a comprehensive, low-cost agricultural advisory system designed specifically for small and marginal farmers in India. The system provides intelligent recommendations for crop selection, fertilizer management, plant disease detection, weather alerts, and market price information through an easy-to-use Progressive Web App (PWA).

### Key Highlights
- **5 Core Features:** Crop Advisory, Fertilizer Guidance, Disease Detection, Weather Alerts, Market Prices
- **Offline Capable:** Works without internet using PWA technology
- **Voice Enabled:** Hands-free operation using Web Speech API
- **Mobile First:** Responsive design optimized for smartphones
- **Low Cost:** No subscription fees, minimal data usage

---

## 2. Problem Statement

### Challenges Faced by Indian Farmers

1. **Lack of Scientific Knowledge**
   - Farmers often rely on traditional methods
   - No access to soil testing recommendations
   - Improper crop selection leading to low yields

2. **Fertilizer Mismanagement**
   - Over-application of chemical fertilizers
   - Nutrient imbalance in soil
   - Environmental degradation

3. **Crop Disease Management**
   - Late detection of plant diseases
   - Incorrect identification of pests
   - Inappropriate pesticide usage

4. **Weather Unpredictability**
   - Inability to plan farming activities
   - Crop damage due to unexpected weather
   - No access to localized weather forecasts

5. **Market Information Gap**
   - Exploitation by middlemen
   - Poor understanding of market prices
   - Inability to time crop sales

---

## 3. Solution Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                         │
│                   (Progressive Web App)                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │  Crop   │ │Fertilizer│ │ Disease │ │ Weather │ │ Market ││
│  │ Advisor │ │ Advisor  │ │Detector │ │ Alerts  │ │ Prices ││
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └───┬────┘│
└───────┼──────────┼─────────┼─────────┼─────────┼───────────┘
        │          │         │         │         │
        └──────────┴────┬────┴─────────┴─────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend API                             │
│                     (FastAPI)                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Crop Logic   │ │ Soil Helper  │ │ Image Processing     │ │
│  │ (Heuristic)  │ │ (Analysis)   │ │ (Disease Detection)  │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                         │
│  ┌──────────────┐ ┌──────────────┐                         │
│  │ OpenWeather  │ │ Market APIs  │                         │
│  │    API       │ │ (Mock Data)  │                         │
│  └──────────────┘ └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Features Description

### 4.1 Crop Recommendation System

**Purpose:** Suggest optimal crops based on soil conditions

**Input Parameters:**
| Parameter | Unit | Description |
|-----------|------|-------------|
| Nitrogen (N) | kg/ha | Soil nitrogen content |
| Phosphorus (P) | kg/ha | Soil phosphorus content |
| Potassium (K) | kg/ha | Soil potassium content |
| pH | - | Soil acidity/alkalinity |
| Rainfall | mm | Average rainfall |

**Algorithm:** Rule-based heuristic system (can be upgraded to ML)

**Output:** Recommended crop with confidence score

---

### 4.2 Fertilizer Advisory System

**Purpose:** Provide personalized fertilizer recommendations

**Features:**
- Crop-specific fertilizer plans
- Soil health analysis
- Nutrient deficiency detection
- Dosage calculations (Urea, DAP, MOP)
- Application timing guidance

**Supported Crops:** Wheat, Rice, Maize, Corn, and more

---

### 4.3 Disease Detection

**Purpose:** Identify plant diseases from leaf images

**Process:**
1. User uploads plant leaf image
2. Image is analyzed for disease indicators
3. Disease classification is returned
4. Remedies and treatment suggestions provided

**Current Implementation:** Basic heuristic (placeholder for ML model)

---

### 4.4 Weather Alerts

**Purpose:** Provide agricultural weather advisories

**Features:**
- Temperature monitoring
- Humidity tracking
- Rainfall predictions
- Agricultural activity recommendations
- Extreme weather alerts

**Data Source:** OpenWeatherMap API (optional)

---

### 4.5 Market Prices

**Purpose:** Display current crop market prices

**Features:**
- APMC market prices
- Price trends (stable/increasing/decreasing)
- Crop-wise filtering
- State-wise data (future enhancement)

**Data Source:** Mock data (ready for Agmarknet/eNAM integration)

---

## 5. Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Programming Language |
| FastAPI | 0.110.2 | Web Framework |
| Uvicorn | 0.29.0 | ASGI Server |
| Pydantic | 2.7.1 | Data Validation |
| Pillow | 10.3.0 | Image Processing |
| NumPy | 1.26.4 | Numerical Computing |
| Requests | 2.31.0 | HTTP Client |

### Frontend

| Technology | Purpose |
|------------|---------|
| HTML5 | Structure |
| CSS3 | Styling |
| JavaScript (ES6+) | Logic |
| Service Workers | Offline Support |
| Web Speech API | Voice Commands |

### Deployment

| Platform | Purpose |
|----------|---------|
| Vercel | Serverless Deployment |
| GitHub | Version Control |

---

## 6. API Specification

### Base URL
- Development: `http://localhost:8000`
- Production: `https://your-app.vercel.app`

### Endpoints

#### GET /health
```json
Response: {
  "status": "ok",
  "message": "API is running"
}
```

#### POST /recommend_crop
```json
Request: {
  "N": 90,
  "P": 42,
  "K": 43,
  "ph": 6.5,
  "rainfall": 120
}

Response: {
  "crop": "wheat",
  "confidence": 0.75,
  "note": "Basic recommendation"
}
```

#### POST /recommend_fertilizer
```json
Request: {
  "N": 90,
  "P": 42,
  "K": 43,
  "ph": 6.5,
  "crop": "wheat"
}

Response: {
  "crop": "wheat",
  "fertilizer_recommendation": {
    "N": "120-150 kg/ha",
    "P": "60-80 kg/ha",
    "K": "40-60 kg/ha"
  }
}
```

#### POST /detect_disease
```json
Request: FormData with image file

Response: {
  "label": "healthy",
  "confidence": 0.72,
  "remedy": "No action needed"
}
```

#### GET /weather?pincode={pincode}
```json
Response: {
  "location": "Pincode: 390001",
  "weather": {
    "temperature": "25-32°C",
    "humidity": "60-80%"
  },
  "agricultural_advisory": "Good conditions for sowing"
}
```

#### GET /market?crop={crop}
```json
Response: {
  "crop": "wheat",
  "market_data": {
    "price": "2500-2800 INR/quintal",
    "trend": "stable"
  }
}
```

---

## 7. Installation Guide

### System Requirements
- Operating System: Windows 10+, macOS 10.14+, Linux
- Python: 3.8 or higher
- RAM: 2GB minimum
- Storage: 500MB free space
- Internet: Required for initial setup

### Step-by-Step Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/Sourabh1789101/Crop-Care-AI.git
   cd Crop-Care-AI
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate Environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your OPENWEATHER_API_KEY (optional)
   ```

6. **Start Backend**
   ```bash
   uvicorn api.index:app --host 0.0.0.0 --port 8000
   ```

7. **Start Frontend**
   ```bash
   cd frontend
   python -m http.server 3000
   ```

---

## 8. Testing

### API Test Results

| Test | Status | Description |
|------|--------|-------------|
| Health Check | ✅ Pass | API responds with status OK |
| Crop Recommendation | ✅ Pass | Returns valid crop suggestion |
| Fertilizer Advisory | ✅ Pass | Returns fertilizer plan |
| Disease Detection | ✅ Pass | Analyzes uploaded images |
| Weather Alerts | ✅ Pass | Returns weather data |
| Market Prices | ✅ Pass | Returns price information |

### Running Tests
```bash
python test_api.py
```

---

## 9. Future Enhancements

### Phase 2 (Planned)

1. **Machine Learning Integration**
   - Train crop recommendation model on real data
   - Deep learning for disease detection
   - Yield prediction models

2. **Real API Integration**
   - Agmarknet for live market prices
   - eNAM marketplace integration
   - Multiple weather providers

3. **Multi-language Support**
   - Hindi, Gujarati, Marathi
   - Tamil, Telugu, Kannada
   - Bengali, Punjabi

4. **Additional Features**
   - Soil testing lab locator
   - Government scheme information
   - Expert consultation booking
   - Community forum

---

## 10. Conclusion

Crop Care AI successfully addresses the key challenges faced by small and marginal farmers in India. The system provides:

- **Accessible Technology:** Works on basic smartphones
- **Offline Capability:** Functions without constant internet
- **Voice Interface:** Usable by farmers with limited literacy
- **Comprehensive Features:** One-stop solution for farming needs
- **Scalable Architecture:** Ready for ML model integration

The project demonstrates the potential of technology to empower farmers and improve agricultural productivity in India.

---

## 11. References

1. FastAPI Documentation - https://fastapi.tiangolo.com/
2. OpenWeatherMap API - https://openweathermap.org/api
3. Progressive Web Apps - https://web.dev/progressive-web-apps/
4. Indian Agriculture Statistics - Ministry of Agriculture

---

**Report Generated:** December 2025

**Project Repository:** https://github.com/Sourabh1789101/Crop-Care-AI
