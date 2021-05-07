from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter

from .serializers import CategorySerializer, SmartphoneSerializer
from ..models import Category, Smartphone


class CategoryListCreateAPIView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'


class SmartphoneListAPIView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'price']


class SmartphoneRetrieveAPIView(RetrieveAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    lookup_field = 'id'
