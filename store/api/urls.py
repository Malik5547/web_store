from django.urls import path

from .api_views import CategoryListAPIView, SmartphoneListAPIView, SmartphoneRetrieveAPIView


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphones'),
    path('smartphones/<str:id>', SmartphoneRetrieveAPIView.as_view(), name='smartphone_retrieve')
]
