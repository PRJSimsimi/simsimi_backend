from rest_framework.generics import ListAPIView

from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from googletrans import Translator 

from .models import customer_reviews
from .tasks import fetch_and_store_reviews, fetch_and_store_reviews_async
from .llama3_utils import generate_responses
from .filters import ReviewFilter
from .serializers import ReviewSerializer
from .pagination import CustomPageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

import json
import logging
import pandas as pd

# 번역기 초기화
translator = Translator()
logger = logging.getLogger(__name__)

class ReviewListView(ListAPIView):
    queryset = customer_reviews.objects.all().order_by('-created_date')
    serializer_class = ReviewSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter


def analyze_reviews(request):
    """
    리뷰 데이터를 분석하여 통계를 반환하는 API
    """
    try:
        # DB에서 리뷰 데이터를 가져오기
        reviews = list(customer_reviews.objects.all().values())

        if not reviews:
            return JsonResponse({"message": "No reviews found."}, status=404)

        # Pandas DataFrame으로 변환
        df = pd.DataFrame(reviews)

        # 분석 데이터 생성
        analysis = {
            "average_rating": round(df["rating"].mean(), 2),
            "total_reviews": len(df),
            "reviews_per_territory": df["territory"].value_counts().to_dict(),
            "top_reviewers": df["reviewer_nickname"].value_counts().head(5).to_dict(),
            "rating_distribution": df["rating"].value_counts().to_dict(),
            "latest_review": df.loc[df["created_date"].idxmax()].to_dict()
        }

        return JsonResponse(analysis, safe=False)
    
    except Exception as e:
        logger.error(f"Error analyzing reviews: {e}")
        return JsonResponse({"error": str(e)}, status=500)


# 리뷰별 자동 답변 생성
def get_responses_for_review(request, review_id):
    """
    특정 리뷰에 대한 자동 답변 생성
    """
    try:
        # 리뷰 객체 가져오기
        review = customer_reviews.objects.get(id=review_id)

        # Llama3를 사용해 답변 생성
        response_options = generate_responses(review.body)

        # 본문 한글 번역
        try:
            translated_body = translator.translate(review.body, src='en', dest='ko').text
        except Exception as e:
            logger.error(f"Error translating review body: {e}")
            translated_body = "번역에 실패했습니다."

        return JsonResponse({
            "id": review.id,
            "rating": review.rating,
            "reviewer_nickname": review.reviewer_nickname,
            "title": review.title,
            "body": review.body,
            "translated_body": translated_body,  # 번역된 본문 
            "created_date": review.created_date,
            "territory": review.territory,

            "response_options": response_options, # 생성된 답변
        })
    except customer_reviews.DoesNotExist:
        return JsonResponse({"error": "Review not found"}, status=404)
    except Exception as e:
        logger.error(f"Error generating responses for review {review_id}: {e}")
        return JsonResponse({"error": str(e)}, status=500)


# 사용자 선택 답변 저장
@csrf_exempt
def save_selected_response(request):
    """
    선택된 자동 답변을 저장
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            review_id = body.get("review_id")
            selected_response = body.get("selected_response")

            # 필드 유효성 검사
            if not review_id or not selected_response:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # 리뷰 객체 가져오기
            review = customer_reviews.objects.get(id=review_id)
            review.selected_response = selected_response
            review.save()

            return JsonResponse({"message": "Response saved successfully!"})
        except customer_reviews.DoesNotExist:
            return JsonResponse({"error": "Review not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.error(f"Error saving selected response: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def trigger_review_sync(request):
    fetch_and_store_reviews_async.delay()
    return JsonResponse({"status": "Sync initiated"})