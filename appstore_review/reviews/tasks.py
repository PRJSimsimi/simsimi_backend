from .models import customer_reviews
from .api import fetch_reviews
from datetime import datetime
import logging

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def store_reviews_in_db():
    reviews = fetch_reviews()

    # Process the data
    processed_data = []

    for review in reviews["data"]:
      try:
        processed_data.append({
          "id": review["id"],
          "rating": review["attributes"]["rating"],
          "reviewer_nickname": review["attributes"]["reviewerNickname"],
          "title": review["attributes"]["title"],
          "body": review["attributes"]["body"],
          "created_date": review["attributes"]["createdDate"],
          "territory": review["attributes"]["territory"],
        })
      except KeyError as e:
        logging.error(f"Failed to process review: {review}. Error: {e}")

    # processed_data = [
    #   {
    #       "id": review["id"],
    #       "rating": review["attributes"]["rating"],
    #       "reviewer_nickname": review["attributes"]["reviewerNickname"],
    #       "title": review["attributes"]["title"],
    #       "body": review["attributes"]["body"],
    #       "created_date": review["attributes"]["createdDate"],
    #       "territory": review["attributes"]["territory"],
    #   }
    #   for review in reviews["data"]
    # ]


    for review in processed_data:
      # Check if the review already exists
      existing_review = customer_reviews.objects.filter(id=review["id"]).first()

      if existing_review:
          # Update the existing review
          existing_review.rating = review["rating"]
          existing_review.reviewer_nickname = review["reviewer_nickname"]
          existing_review.title = review["title"]
          existing_review.body = review["body"]
          # existing_review.created_at = datetime.strptime(review["created_date"], "%Y-%m-%dT%H:%M:%SZ")
          existing_review.created_date = datetime.fromisoformat(review["created_date"])
          existing_review.territory = review["territory"]
          existing_review.save()
      else:
          # Create a new review
          customer_reviews.objects.create(
              id=review["id"],
              rating=review["rating"],
              reviewer_nickname=review["reviewer_nickname"],
              title=review["title"],
              body=review["body"],
              # created_at=datetime.strptime(review["created_date"], "%Y-%m-%dT%H:%M:%SZ"),
              created_date=datetime.fromisoformat(review["created_date"]),
              territory=review["territory"],
          )