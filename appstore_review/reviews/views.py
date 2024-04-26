from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from .models import customer_reviews
from .tasks import store_reviews_in_db 

def get_reviews(request):
  store_reviews_in_db()

  reviews = customer_reviews.objects.all()
  data = [
      {
          "id": review.id,  # 리뷰 고유 ID
          "rating": review.rating,  # 별점
          "reviewer_nickname": review.reviewer_nickname,  # 작성자 닉네임
          "title": review.title,  # 리뷰 제목
          "body": review.body,  # 리뷰 본문
          "created_date": review.created_date,  # 작성일
          "territory": review.territory,  # 지역 코드
      }
      for review in reviews
  ]
  return JsonResponse({"reviews": data}, safe=False)