from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
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

def product_list(request):
    products = Product.objects.filter(is_active=True, stock__gt=0)
    return render(request, 'products/products_list.html', {'products': products})