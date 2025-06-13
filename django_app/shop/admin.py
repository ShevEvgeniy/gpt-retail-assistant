from django.contrib import admin
from shop.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ['id', 'name', 'price', 'on_sale']
    list_editable = ['name', 'price', 'on_sale',]