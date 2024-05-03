from django.shortcuts import render

from django.core.paginator import Paginator

from django.http import JsonResponse
from .models import customer_reviews
from .tasks import store_reviews_in_db 

def get_reviews(request):
  store_reviews_in_db()

  rating = request.GET.get('rating')
  start_date = request.GET.get('start_date')
  end_date = request.GET.get('end_date')

  reviews = customer_reviews.objects.all()

  # 필터링
  if rating:
      reviews = reviews.filter(rating=rating)
  if start_date and end_date:
      reviews = reviews.filter(created_date__range=[start_date, end_date])

  # 페이징 처리
  page = request.GET.get('page', 1)
  paginator = Paginator(reviews, 10)  # 페이지당 10개
  current_page = paginator.get_page(page)

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
      for review in current_page
  ]
  return JsonResponse({"reviews": data, "total_pages": paginator.num_pages}, safe=False)