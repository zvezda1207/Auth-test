import jwt
from django.conf import settings
from datetime import datetime, timezone, timedelta

def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + settings.JWT_ACCESS_TOKEN_LIFETIME
    payload = {
        'user_id': user_id,
        'exp': exp,
        'iat': now,
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_access_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])