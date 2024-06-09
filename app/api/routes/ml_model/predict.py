import json
import os
from typing import List, Union, Dict

import numpy as np
import requests
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account
from pydantic import BaseModel, Field
from sklearn.preprocessing import normalize
from transformers import AutoTokenizer
from dotenv import load_dotenv

from app.api.deps import get_current_user
from app.core.config import settings
from app.models import User

# Setup environment variables and constants
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = FastAPI()
router = APIRouter()

# Load configuration from settings
service_account_file = settings.VERTEX_SERVICE_ACCOUNT
tokenizer_path = settings.VERTEX_QRECOM_TOKENIZER
instances_path = settings.VERTEX_QRECOM_INSTANCES
endpoint_url = settings.VERTEX_QRECOM_ENDPOINT_URL
vertex_model_numeric_url = settings.VERTEX_MODEL_NUMERIC_URL  # Use settings here
vertex_model_features_normalized = settings.VERTEX_MODEL_FEATURES_NORMALIZED
vertex_model_targets = settings.VERTEX_MODEL_TARGETS

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Load service account credentials from JSON key file
credentials = service_account.Credentials.from_service_account_file(service_account_file)
scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
scoped_credentials.refresh(GoogleRequest())

# Load other necessary data
features_normalized = np.load(vertex_model_features_normalized)
targets = np.load(vertex_model_targets, allow_pickle=True)


class PredictionResponse(BaseModel):
    message: str = Field(..., example="success")
    data: Dict[str, List[str]]


class ErrorResponse(BaseModel):
    detail: str


class UserPredictionRequest(BaseModel):
    pass


class InputText(BaseModel):
    text: str


def tokenize_texts(texts, tokenizer, max_len=128):
    return tokenizer(
        texts,
        max_length=max_len,
        truncation=True,
        padding='max_length',
        return_tensors='tf'
    )


def save_tokens_to_json(tokens, file_path):
    with open(file_path, 'w') as f:
        json.dump(tokens, f)


def predict_custom_trained_model_rest(
        endpoint_url: str,
        instances: Union[Dict, List[Dict]],
        access_token: str
):
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "instances": instances
        }

        response = requests.post(endpoint_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes

        predictions = response.json().get("predictions")
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction request: {str(e)}")


def get_embeddings(texts, tokenizer, max_len=128, access_token: str = None):
    try:
        tokens = tokenize_texts(texts, tokenizer, max_len)
        tokens = {key: value.numpy().tolist() for key, value in tokens.items()}
        instances = [{"input_ids": input_id, "attention_mask": attention_mask}
                     for input_id, attention_mask in zip(tokens['input_ids'], tokens['attention_mask'])]

        data_to_save = {"instances": instances}
        with open(instances_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

        result = predict_custom_trained_model_rest(
            endpoint_url=endpoint_url,
            instances=instances,
            access_token=scoped_credentials.token
        )

        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting embeddings: {str(e)}")


def recommend(input_data, features_normalized, targets, top_k=10):
    input_data_normalized = normalize([input_data], axis=1)
    pred = input_data_normalized
    similarities = np.dot(features_normalized, pred.T).flatten()
    top_k_indices = similarities.argsort()[-top_k:][::-1]
    recommended_courses = [targets[i] for i in top_k_indices]
    return recommended_courses


@router.post("/major-recommendation", response_model=PredictionResponse, responses={
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

    response = requests.post(vertex_model_numeric_url, headers=headers, json={"instances": [input_data]})

    if response.status_code == 200:
        prediction_result = response.json()
        predictions = prediction_result['predictions'][0]

        recommendations = recommend(predictions, features_normalized, targets)

        return {"message": "success", "data": {"prediction": recommendations}}  # Updated response format
    elif response.status_code == 400:
        raise HTTPException(status_code=400, detail="Bad request. Invalid input.")
    else:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/quick-recommendation", response_model=PredictionResponse, responses={
    200: {"model": PredictionResponse, "description": "Successful response with recommendations."},
    400: {"model": ErrorResponse, "description": "Bad request. Invalid input."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
async def root(input_text: InputText):
    try:
        input_embedding = get_embeddings([input_text.text], tokenizer, access_token=scoped_credentials.token)
        print(input_embedding)
        embedding_array = np.array(input_embedding)

        top_5_unique = np.argsort(embedding_array)[-5:][::-1]

        columns_to_consider = ['Matematika', 'Sains', 'Fisika', 'Sosiologi', 'Biologi', 'Kimia',
                               'Teknologi','Bisnis dan Ekonomi', 'Seni', 'Sastra dan Linguistik',
                               'Pendidikan', 'Hukum', 'Lingkungan', 'Kesehatan', 'Geografi',
                               'Komunikasi', 'Sejarah dan Filsafat']

        num_to_major = {i+1: columns_to_consider[i] for i in range(len(columns_to_consider))}

        top_5_majors_names = [num_to_major[num+1] for num in top_5_unique]

        response = {
            "message": "success",
            "data": {
                "prediction": top_5_majors_names
            }
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server Error: {str(e)}")


app.include_router(router)
