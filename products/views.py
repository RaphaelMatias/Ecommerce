from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_active=True, stock__gt=0)

    def get_related_categories(self, category):
        if not category:
            return []

        return Category.objects.filter(
            Q(tree_id=category.tree_id) &
            Q(lft__range=(category.lft, category.rght))
        )

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        product = self.get_object()
        main_category = product.category

        related_categories = self.get_related_categories(main_category)
        related_products = Product.objects.filter(
            Q(category__in=related_categories) | 
            Q(related_products=product)
        ).exclude(id=product.id).distinct().order_by('?')

        same_category = related_products.filter(category=main_category)[:4]
        other_related = related_products.exclude(category=main_category)[:4]

        final_products = list(same_category) + list(other_related)
        final_products = final_products[:8]

        serializer = self.get_serializer(final_products, many=True)
        return Response(serializer.data)