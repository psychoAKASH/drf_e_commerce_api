from rest_framework import serializers
from .models import Order,CartItem
from shop.models import Product

class ProductQuantitySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
    items = ProductQuantitySerializer(many=True, write_only=True)  # Custom input field
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Response field
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'products', 'total_price', 'created_at']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request and not request.user.is_staff: # for admin only
            validated_data.pop('status', None)

        return super().update(instance, validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']