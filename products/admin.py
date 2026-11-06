from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'category', 'created_at')
    search_fields = ('name', 'description', 'seller__shop_name')
    list_select_related = ('seller', 'category')
    readonly_fields = ('created_at', 'updated_at')