from django.urls import path

from .api_views import CategoryListAPIView


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
]
