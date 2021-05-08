from django.urls import path

from .api_views import CategoryListCreateAPIView


urlpatterns = [
    path('categories/<str:id>', CategoryListCreateAPIView.as_view(), name='categories'),
]
