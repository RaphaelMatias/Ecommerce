from rest_framework import serializers
from .models import Category, Tag, Brand, Review, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'brand', 'tags', 'slug', 'description',
            'price', 'discount_price', 'stock', 'image', 'is_available', 'final_price',
            'created_at', 'updated_at', 'reviews'
        ]