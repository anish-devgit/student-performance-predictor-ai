from pydantic import BaseModel, Field
from typing import Literal

class StudentProfile(BaseModel):
    age: int = Field(..., ge=10, le=100, description="Age of the student")
    gender: Literal['male', 'female', 'other']
    course: Literal['diploma', 'undergraduate', 'postgraduate', 'phd', 'certificate', 'professional', 'vocational']
    study_hours: float = Field(..., ge=0, le=24, description="Daily study hours")
    class_attendance: float = Field(..., ge=0, le=100, description="Attendance percentage")
    internet_access: Literal['yes', 'no']
    sleep_hours: float = Field(..., ge=0, le=24, description="Daily sleep hours")
    sleep_quality: Literal['poor', 'average', 'good']
    study_method: Literal['coaching', 'self-study', 'group-study', 'online', 'tutoring']
    facility_rating: Literal['low', 'moderate', 'high']
    exam_difficulty: Literal['hard', 'moderate', 'easy']

class PredictionResponse(BaseModel):
    exam_score: float
    confidence_level: str = "High" # Placeholder for now, could be derived from probability if applicable
    pass_probability: float = 0.0 # Placeholder
