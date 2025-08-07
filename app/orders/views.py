from rest_framework import viewsets, status
from .models import Order,CartItem
from rest_framework.decorators import action
from .serializers import OrderSerializer,CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shop.models import Product
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.core.cache import cache




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        items_data = serializer.validated_data.pop('items')

        total_price = 0
        products_to_add = []

        with transaction.atomic():
            for item in items_data:
                product_id = item['product_id']
                quantity = item['quantity']

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError(f"Product with id {product_id} not found.")

                if product.stock < quantity:
                    raise ValidationError(f"Only {product.stock} of '{product.name}' left in stock.")

                product.stock -= quantity
                product.save()

                total_price += product.price * quantity
                products_to_add.extend([product] * quantity)  # Add same product multiple times

            order = serializer.save(user=user, total_price=total_price)
            order.products.set(products_to_add)
        cache.delete("product_list")

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff:
            return Response({'detail': 'Only admin can update order status.'},
                            status=status.HTTP_403_FORBIDDEN)

        status_to_set = request.data.get('status')
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]

        if status_to_set not in valid_statuses:
            return Response({'detail': 'Invalid status value.'},
                            status=status.HTTP_400_BAD_REQUEST)

        instance.status = status_to_set
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def from_cart(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        items = [{"product_id": item.product.id, "quantity": item.quantity} for item in cart_items]
        serializer = self.get_serializer(data={"items": items})
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)