# firebase configuration
from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

import firebase_admin
from firebase_admin import credentials

def initialize_firebase(settings):
    service_account_key_path = settings.FIREBASE_SERVICE_KEY
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully!")
