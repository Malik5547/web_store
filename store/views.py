from django.shortcuts import render, HttpResponse
from django.views.generic.detail import DetailView

from .models import Notebook, Smartphone, Category


def index(request):
    categories = Category.objects.get_categories_for_left_sidebar()
    return render(request, 'base.html', {'categories': categories})


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

