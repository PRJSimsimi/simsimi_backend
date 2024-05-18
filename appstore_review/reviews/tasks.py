from .models import customer_reviews
from .api import fetch_reviews
from datetime import datetime
from .llama3_utils import generate_responses
import logging
from celery import shared_task

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# 데이터 유효성 검사
def validate_review_data(review):
    if not review.get("id"):
        raise ValueError("Review ID is missing.")
    if not review.get("attributes"):
        raise ValueError("Attributes are missing.")
    if not 1 <= review["attributes"]["rating"] <= 5:
        raise ValueError("Invalid rating value.")
    return True


def fetch_and_store_reviews():
    try:
        reviews = fetch_reviews()  # 외부 API 호출
        logging.info(f"Fetched {len(reviews['data'])} reviews.")
        print(f"Fetched {len(reviews['data'])} reviews.")

        for review in reviews["data"]:
            try:
                # 유효성 검사
                validate_review_data(review)

                # 리뷰 본문에서 답변 생성
                # response_options = generate_responses(review["attributes"]["body"])  # 3개의 답변 생성      

                # 데이터 저장 또는 업데이트
                customer_reviews.objects.update_or_create(
                    id=review["id"],
                    defaults={
                        "rating": review["attributes"]["rating"],
                        "reviewer_nickname": review["attributes"]["reviewerNickname"],
                        "title": review["attributes"]["title"],
                        "body": review["attributes"]["body"],
                        # "created_date": review["attributes"]["createdDate"],
                        "created_date": datetime.fromisoformat(review["attributes"]["createdDate"]),
                        "territory": review["attributes"]["territory"],
                        # "response_options": response_options,  # 생성된 답변 저장
                    },
                )
                logging.info(f"Review {review['id']} processed successfully.")
            except ValueError as e:
                logging.error(f"Validation error for review {review['id']}: {e}")
            
    except Exception as e:
        logging.error(f"Failed to fetch reviews: {e}")


@shared_task
def fetch_and_store_reviews_async():
    fetch_and_store_reviews()