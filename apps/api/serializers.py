from rest_framework import serializers
from .models import Order, OrderDetails
from apps.user.models import User
from apps.main.models import Product


class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = ["id", "product", "quantity", "product_name","detail_status"]

    def get_product_name(self, obj):
        return obj.product.name


class OrderSerializer(serializers.ModelSerializer):
    orderdetails_set = OrderDetailsSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ["table", "orderdetails_set"]

    def create(self, validated_data):
        orderdetails_data = validated_data.pop("orderdetails_set", [])
        validated_data["employee"] = User.objects.get(pk=2)
        order = Order.objects.create(**validated_data)

        for detail_data in orderdetails_data:
            product = detail_data.pop("product")
            quantity = detail_data.pop("quantity")
            total = product.sale_price * quantity
            OrderDetails.objects.create(
                order=order, product=product, quantity=quantity, total=total
            )

        return order
