import datetime
import jwt
from django.conf import settings


def generate_token(user, day, min):
    token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=day, minutes=min),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
    return token
