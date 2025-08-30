#!/usr/bin/env python3
"""
Simple server startup script for Smart Crop Advisory
"""
import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    import uvicorn
    from app import app
    
    print("🌾 Starting Smart Crop Advisory Server...")
    print("📍 Backend directory:", backend_dir)
    print("🔗 Server will be available at: http://127.0.0.1:8000")
    print("📖 API documentation: http://127.0.0.1:8000/docs")
    print("🤖 WhatsApp status: http://127.0.0.1:8000/api/whatsapp/status")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
