import requests
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
import jwt
import random

from django.http import JsonResponse
from django.views.decorators.http import require_GET


# 예시로 사용할 외부 API 엔드포인트
EXTERNAL_API_URL = f'https://api.appstoreconnect.apple.com/v1/apps/375239755/customerReviews?sort=-createdDate&exists[publishedResponse]=false'


# JWT 토큰 생성 함수 (FastAPI 코드에 맞춰서)
def create_jwt_token():
    auth_path = 'AppleConnect_AuthKey_G54BYZM5WR.p8'
    with open(auth_path, "rb") as authKey:
        signing_key = authKey.read()
        
    token = jwt.encode(
        {
            'iss': "69a6de70-6b36-47e3-e053-5b8c7c11a4d1",
            # 'exp': int(mktime((datetime.now()).timetuple())) + 1200,  # 20분 후 만료
            'exp': int(datetime.now().timestamp()) + 1200,  # 20분 후 만료
            'aud': 'appstoreconnect-v1'
        },
        signing_key,
        algorithm='ES256',
        headers={'kid': "G54BYZM5WR"}
    )
    return token


# 외부 API 호출 및 데이터 처리
# @require_GET
# def fetch_reviews(request):
def fetch_reviews():

    # JWT 토큰 생성
    token = create_jwt_token()

    # API 요청 헤더에 JWT 토큰 포함
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # 외부 API에 요청 보내기
    try:
        response = requests.get(EXTERNAL_API_URL, headers=headers)

        # 요청이 성공하면
        if response.status_code == 200:
            data = response.json()  # JSON 데이터로 변환
            # return JsonResponse(data, safe=False)  # 응답 데이터를 그대로 반환
            return data

        # 오류가 발생하면
        else:
            return JsonResponse({'error': 'Failed to fetch data from external API'}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        # 요청 중 오류 발생 시
        return JsonResponse({'error': str(e)}, status=500)

