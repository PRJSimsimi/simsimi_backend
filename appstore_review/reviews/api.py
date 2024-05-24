import requests
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
import jwt
import random

from django.http import JsonResponse
from django.views.decorators.http import require_GET


# 외부 API 엔드포인트
EXTERNAL_API_URL = f'https://api.appstoreconnect.apple.com/v1/apps/375239755/customerReviews?sort=-createdDate&exists[publishedResponse]=false'


# JWT 토큰 생성 함수 (FastAPI 코드에 맞춰서)
def create_jwt_token():
    auth_path = os.getenv("APPLE_AUTH_KEY_PATH")
    
    with open(auth_path, "rb") as authKey:
        signing_key = authKey.read()
        
    token = jwt.encode(
        {
            'iss': os.getenv("APPLE_ISS"),
            # 'exp': int(mktime((datetime.now()).timetuple())) + 1200,  # 20분 후 만료
            'exp': int(datetime.now().timestamp()) + 1200,  # 20분 후 만료
            'aud': 'appstoreconnect-v1'
        },
        signing_key,
        algorithm='ES256',
        headers={'kid': os.getenv("APPLE_KID")}
    )
    return token



def fetch_reviews(rating=None, start_date=None, end_date=None):
    token = create_jwt_token()
    headers = {'Authorization': f'Bearer {token}'}

    params = {
        'sort': '-createdDate',
        'filter[rating]': rating if rating else None,
        'filter[date]': f"{start_date},{end_date}" if start_date and end_date else None
    }

    response = requests.get(EXTERNAL_API_URL, headers=headers, params={k: v for k, v in params.items() if v})

    if response.status_code == 200:
        return response.json()
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)

