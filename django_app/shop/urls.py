from django.urls import path
from shop.views import ProductListView, ProductDetailView, index

urlpatterns = [
    path('', index, name='index'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]