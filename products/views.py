from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Product
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

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        product = self.get_object()
        related_products = product.related_products.all()[:4]
        if not related_products.exists():
            related_products = Product.objects.filter(
                category=product.category
            ).exclude(id=product.id).order_by('?')[:4]
        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)