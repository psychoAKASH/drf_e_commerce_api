from rest_framework import serializers
from .models import Order
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