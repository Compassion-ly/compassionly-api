import os
from typing import List, Dict
import numpy as np
import requests
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account
from pydantic import BaseModel, Field
from sklearn.preprocessing import normalize
from sqlmodel import Session, select
from starlette import schemas

from app import crud, models
from app.api.deps import get_current_user, get_db
from app.core.config import settings  # Adjust this import as needed
from app.core.db import get_session
from app.models import Topic, UserTopicRating, User  # Adjust the import path as needed

app = FastAPI()
router = APIRouter()

# Load service account credentials from JSON key file
credentials = service_account.Credentials.from_service_account_file(settings.vertex_service_account)
scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
scoped_credentials.refresh(GoogleRequest())

features_normalized = np.load(settings.vertex_model_features_normalized)
targets = np.load(settings.vertex_model_targets, allow_pickle=True)


class PredictionResponse(BaseModel):
    message: str = Field(..., example="success")
    data: List[str]


class ErrorResponse(BaseModel):
    detail: str


class UserPredictionRequest(BaseModel):
    pass


def recommend(input_data, features_normalized, targets, top_k=10):
    input_data_normalized = normalize([input_data], axis=1)
    pred = input_data_normalized  # Replace with actual prediction if needed
    similarities = np.dot(features_normalized, pred.T).flatten()
    top_k_indices = similarities.argsort()[-top_k:][::-1]
    recommended_courses = [targets[i] for i in top_k_indices]
    return recommended_courses


@router.post("/numeric-model", response_model=PredictionResponse, responses={
    200: {"model": PredictionResponse, "description": "Successful response with recommendations."},
    400: {"model": ErrorResponse, "description": "Bad request. Invalid input."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
async def predict_for_user(
        request: UserPredictionRequest,
        current_user: User = Depends(get_current_user)
):
    user_topic_weight = current_user.user_topic_weight

    if not user_topic_weight:
        raise HTTPException(status_code=400, detail="User topic weights not found.")

    input_data = user_topic_weight

    headers = {
        'Authorization': f'Bearer {scoped_credentials.token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(settings.vertex_model_numeric_url, headers=headers, json={"instances": [input_data]})

    if response.status_code == 200:
        prediction_result = response.json()
        predictions = prediction_result['predictions'][0]

        recommendations = recommend(predictions, features_normalized, targets)

        return {"message": "success", "data": recommendations}
    elif response.status_code == 400:
        raise HTTPException(status_code=400, detail="Bad request. Invalid input.")
    else:
        raise HTTPException(status_code=500, detail="Internal server error.")


app.include_router(router)
