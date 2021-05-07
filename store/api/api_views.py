from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from .serializers import CategorySerializer, SmartphoneSerializer
from ..models import Category, Smartphone


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SmartphoneListAPIView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'price']

