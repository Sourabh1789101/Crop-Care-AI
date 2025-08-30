import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json

app = FastAPI(title="Crop-Care-AI Disease Detection Service")

# Global model and classes
model = None
disease_classes = []

@app.on_event("startup")
async def load_model():
    global model, disease_classes
    try:
        model_path = os.getenv("MODEL_PATH", "/app/models/disease_detection_model.h5")
        classes_path = os.getenv("CLASSES_PATH", "/app/models/disease_classes.json")
        
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print(f"Model loaded from {model_path}")
        else:
            print(f"Model not found at {model_path}, using dummy responses")
            
        if os.path.exists(classes_path):
            with open(classes_path, 'r') as f:
                disease_classes = json.load(f)
            print(f"Classes loaded: {len(disease_classes)} classes")
        else:
            disease_classes = ["Healthy", "Disease_1", "Disease_2"]  # Default
            print("Using default disease classes")
            
    except Exception as e:
        print(f"Error loading model: {e}")

def preprocess_image(image_data: bytes, target_size=(224, 224)):
    """Preprocess image for model inference"""
    try:
        image = Image.open(io.BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize(target_size)
        image_array = np.array(image) / 255.0
        return np.expand_dims(image_array, axis=0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image preprocessing failed: {e}")

@app.post("/analyze")
async def analyze_disease(file: UploadFile = File(...)):
    """Analyze uploaded image for crop disease detection"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and preprocess image
        image_data = await file.read()
        processed_image = preprocess_image(image_data)
        
        if model is not None:
            # Real prediction
            predictions = model.predict(processed_image)[0]
            predicted_idx = np.argmax(predictions)
            confidence = float(predictions[predicted_idx])
            
            disease = disease_classes[predicted_idx] if predicted_idx < len(disease_classes) else "Unknown"
            
            # Get top 3 predictions
            top_indices = np.argsort(predictions)[-3:][::-1]
            top_predictions = [
                {
                    "disease": disease_classes[i] if i < len(disease_classes) else f"Class_{i}",
                    "confidence": float(predictions[i])
                }
                for i in top_indices
            ]
        else:
            # Dummy response when model not available
            disease = "Rice Blast"
            confidence = 0.85
            top_predictions = [
                {"disease": "Rice Blast", "confidence": 0.85},
                {"disease": "Healthy", "confidence": 0.12},
                {"disease": "Leaf Spot", "confidence": 0.03}
            ]
        
        # Treatment recommendations (simplified)
        treatment_recommendations = get_treatment_recommendations(disease)
        
        return JSONResponse({
            "disease": disease,
            "confidence": confidence,
            "treatment_recommendations": treatment_recommendations,
            "top_predictions": top_predictions
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

def get_treatment_recommendations(disease: str) -> list:
    """Get treatment recommendations based on detected disease"""
    treatments = {
        "Rice Blast": [
            "Apply fungicide containing tricyclazole",
            "Improve field drainage",
            "Use resistant varieties",
            "Remove infected plant debris"
        ],
        "Leaf Spot": [
            "Apply copper-based fungicide",
            "Ensure proper plant spacing",
            "Avoid overhead irrigation",
            "Remove affected leaves"
        ],
        "Healthy": [
            "Continue current care practices",
            "Monitor regularly for early signs",
            "Maintain proper nutrition",
            "Ensure adequate water management"
        ]
    }
    return treatments.get(disease, ["Consult local agricultural extension officer"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
