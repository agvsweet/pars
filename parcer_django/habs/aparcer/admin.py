from django.contrib import admin
from .forms import ProductForm
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user_name', 'user_link', 'r_date')
    form = ProductForm