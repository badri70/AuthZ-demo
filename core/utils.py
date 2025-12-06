# users/utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET = settings.SECRET_KEY
ALGORITHM = "HS256"

def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=12),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token

def decode_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
