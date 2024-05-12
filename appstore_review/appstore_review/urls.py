"""
URL configuration for appstore_review project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from reviews.views import get_reviews, get_responses_for_review, save_selected_response, ReviewListView, analyze_reviews
from reviews.views import get_responses_for_review, save_selected_response, ReviewListView, analyze_reviews


urlpatterns = [
    path('admin/', admin.site.urls),    
    # path('reviews/', get_reviews, name='get_reviews'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('get_responses/<str:review_id>/', get_responses_for_review, name='get_responses'),
    path('save_response/', save_selected_response, name='save_response'),    
    path('reviews/analytics/', analyze_reviews, name='reviews-analytics'),
]
