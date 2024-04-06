from django.db import models

class customer_reviews(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # 리뷰 고유 ID
    rating = models.IntegerField()  # 별점 (1~5)
    reviewer_nickname = models.CharField(max_length=255)  # 작성자 닉네임
    title = models.CharField(max_length=255)  # 리뷰 제목
    body = models.TextField()  # 리뷰 본문
    created_date = models.DateTimeField()  # 리뷰 작성일
    territory = models.CharField(max_length=3)  # 지역 코드 (예: KOR, USA)

    class Meta:
        db_table = 'customer_reviews'  # 데이터베이스 테이블 이름

    # def __str__(self):
    #     return f"{self.reviewer_nickname} - {self.title[:20]}"
