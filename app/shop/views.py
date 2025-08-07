from rest_framework import viewsets, permissions,filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.query_params == {}:
            cached_categories = cache.get("category_list")
            if cached_categories:
                return cached_categories
            queryset = list(Category.objects.all())
            cache.set("category_list", queryset, timeout=3600)
            return queryset
        return Category.objects.all()

    def perform_create(self, serializer):
        cache.delete("category_list")
        serializer.save()

    def perform_update(self, serializer):
        cache.delete("category_list")
        serializer.save()

    def perform_destroy(self, instance):
        cache.delete("category_list")
        instance.delete()

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'stock', 'price','category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock', 'name']

    def get_queryset(self):
        if self.request.query_params == {}:
            cached_products = cache.get("product_list")
            if cached_products:
                return cached_products
            queryset = list(Product.objects.select_related('category').all())
            cache.set("product_list", queryset, timeout=3600)
            return queryset

        return Product.objects.select_related('category').all()

    def perform_update(self, serializer):
        cache.delete("product_list")
        serializer.save()

    def perform_destroy(self, instance):
        cache.delete("product_list")
        instance.delete()



