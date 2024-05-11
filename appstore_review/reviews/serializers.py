from rest_framework import serializers
from .models import customer_reviews

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer_reviews
        fields = '__all__'  # 모든 필드 직렬화
