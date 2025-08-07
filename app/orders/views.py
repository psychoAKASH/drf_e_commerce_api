from rest_framework import viewsets, status
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shop.models import Product
from rest_framework.exceptions import ValidationError
from django.db import transaction



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

