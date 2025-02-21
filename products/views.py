from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q, Case, When, IntegerField, Subquery, OuterRef
from django.db.models.functions import Coalesce
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
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, stock__gt=0)
        return queryset.select_related('category', 'brand')

    @action(detail=True, methods=['get'], url_path='related')
    def related_products(self, request, pk=None):
        product = self.get_object()
        related_products = self._get_related_products(product)
        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)

    def _get_related_products(self, product):
        base_qs = Product.objects.filter(is_active=True).exclude(id=product.id)
        parent_category = product.category.parent if product.category else None

        return base_qs.annotate(
            manual_relation=Case(
                When(related_products=product, then=0),
                default=1,
                output_field=IntegerField()
            ),
            hierarchy_group=Case(
                When(category=product.category, then=0),
                When(
                    Q(category=parent_category) | 
                    Q(category__parent=parent_category) if parent_category 
                    else Q(pk__isnull=False),
                    then=1
                ),
                default=2,
                output_field=IntegerField()
            ),
            category_depth=Coalesce(
                Subquery(
                    Category.objects.filter(pk=OuterRef('category'))
                    .values('level')[:1]
                ), 
                0
            )
        ).filter(
            hierarchy_group__in=[0, 1]  # Remove totalmente o fallback
        ).order_by(
            'manual_relation',
            'hierarchy_group',
            '-category_depth'
        )[:8]  # Pode retornar menos de 8 se não houver produtos suficientes