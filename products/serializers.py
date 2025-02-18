from rest_framework import serializers
from mptt.templatetags.mptt_tags import cache_tree_children
from .models import Category, Tag, Brand, Review, Product

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'children')

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
    category = CategorySerializer(read_only=True)
    category_hierarchy = serializers.SerializerMethodField()
    brand = serializers.StringRelatedField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    reviews = ReviewSerializer(many=True, read_only=True)
    related_products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'brand', 'tags', 'slug', 'description',
            'price', 'discount_price', 'stock', 'image', 'is_available', 'final_price',
            'created_at', 'updated_at', 'reviews', 'category_hierarchy', 'related_products'
        ]

    def get_category_hierarchy(self, obj):
        def get_parents(category):
            if category is None:
                return []
            return get_parents(category.parent) + [category]

        if obj.category:
            categories = get_parents(obj.category)
            return CategorySerializer(categories, many=True).data
        return []