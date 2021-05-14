from django.urls import path
from .views import BaseSpecView, NewCategoryView

urlpatterns = [
    path('', BaseSpecView.as_view(), name='base_spec'),
    path('new_category/', NewCategoryView.as_view(), name='new_category')
]