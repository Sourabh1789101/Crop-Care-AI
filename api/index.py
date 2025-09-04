import os
import sys
# Add the services directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services'))

from app import app

# Export the FastAPI app for Vercel
handler = app

# For testing locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
