from django.shortcuts import render

from django.views.generic import ListView, DetailView
from shop.models import Product

def index(request):
    context = {
        'title': 'Доставка суши SusiShop',
        'products_on_sale': Product.objects.filter(on_sale=True)
    }
    return render(request, 'index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_option = self.request.GET.get('sort')
        if sort_option == 'asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'desc':
            queryset = queryset.order_by('-price')
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'