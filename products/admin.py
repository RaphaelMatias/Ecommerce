from django.contrib import admin
from .models import Category, Tag, Brand, Review, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent','description')
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('category', 'brand', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category__name', 'brand__name')
    prepopulated_fields = {'slug':('name',)}
    autocomplete_fields = ('category', 'brand', 'tags')
    readonly_fields = ('created_at', 'updated_at')