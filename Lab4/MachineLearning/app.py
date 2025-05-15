from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Load the trained model
model = joblib.load('music_recommender.joblib')

# Create FastAPI app
app = FastAPI(title="Music Recommender API")

# Define the input data model
class UserInput(BaseModel):
    age: int
    gender: int  # 1 for male, 0 for female

# Define prediction endpoint
@app.post("/predict")
def predict(user_input: UserInput):
    data = [[user_input.age, user_input.gender]]
    prediction = model.predict(data)
    return {"genre": prediction[0]}
