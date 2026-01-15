from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import StudentProfile, PredictionResponse
import sys
import os

# Add root to path to find src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.predict_pipeline import PredictPipeline

app = FastAPI(title="Exam Score Prediction API", version="1.0")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Pipeline
pipeline = None

@app.on_event("startup")
def load_model():
    global pipeline
    try:
        # Assuming running from root
        model_dir = "models"
        if not os.path.exists(model_dir):
            model_dir = os.path.join("..", "..", "models") # If running from app/backend (not likely with uvicorn root)
            
        pipeline = PredictPipeline(model_dir=model_dir)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        # Dont crash, just fail requests later
        
@app.get("/")
def home():
    return {"message": "Exam Score Prediction API is running. Use /predict to get scores."}

@app.post("/predict", response_model=PredictionResponse)
def predict_score(profile: StudentProfile):
    if not pipeline:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert Pydantic model to dict
        input_data = profile.dict()
        
        # Predict
        score = pipeline.predict(input_data)
        
        # Simple Logic for 'Pass Probability' (Mock logic since regression doesn't give prob implicitly without errors)
        # E.g. if score > 40 is pass
        pass_prob = min(1.0, max(0.0, (score - 20) / 80)) # Mock sigmoid-ish
        
        return {
            "exam_score": score, 
            "confidence_level": "High" if 0 <= score <= 100 else "Low (Outlier)",
            "pass_probability": round(pass_prob, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feature_importance")
def feature_importance():
    try:
        from src.explainability import get_feature_importance
        # Adjust paths based on where main.py is (app/backend) vs root
        # We need to point to root models/data
        data = get_feature_importance(model_dir="models", data_dir="data")
        return data
    except Exception as e:
        print(f"Error fetching importance: {e}")
        return []

