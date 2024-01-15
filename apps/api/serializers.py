from rest_framework import serializers
from .models import Order, OrderDetails
from apps.user.models import User
from apps.main.models import Product


class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = ["id", "product", "quantity", "product_name", "detail_status"]

    def get_product_name(self, obj):
        return obj.product.name


class OrderSerializer(serializers.ModelSerializer):
    orderdetails_set = OrderDetailsSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ["id", "table", "order_status", "orderdetails_set"]

    def create(self, validated_data):
        orderdetails_data = validated_data.pop("orderdetails_set", [])
        
        validated_data["employee"] = User.objects.get(pk=5)
        order = Order.objects.create(**validated_data)
        total_order = 0

        for detail_data in orderdetails_data:
            product = detail_data.pop("product")
            quantity = detail_data.pop("quantity")
            total = product.sale_price * quantity
            total_order += total

            OrderDetails.objects.create(
                order=order, product=product, quantity=quantity, total=total
            )

        order.total = total_order
        order.save()

        return order
    def update(self, instance, validated_data):
        orderdetails_data = validated_data.pop('orderdetails_set', [])
        instance.table = validated_data.get('table', instance.table)

        for detail_data in orderdetails_data:
            detail_id = detail_data.get('id', None)
            if detail_id:
                detail = OrderDetails.objects.get(id=detail_id, order=instance)
                detail.product = detail_data.get('product', detail.product)
                detail.quantity = detail_data.get('quantity', detail.quantity)
                detail.total = detail.product.sale_price * detail.quantity
                
                detail.save()
            else:
                product = detail_data.get('product')
                quantity = detail_data.get('quantity')
                total = product.sale_price * quantity
                
                # Busca un OrderDetail existente con el mismo producto
                existing_detail = OrderDetails.objects.filter(order=instance, product=product, detail_status='P').first()
                if existing_detail:
                    
                    # Si existe, actualiza su cantidad y total
                    existing_detail.quantity = quantity  # Establece la cantidad a la nueva cantidad
                    existing_detail.total = total  
                    existing_detail.save()
                   
                else:
                    # Si no existe, crea uno nuevo
                    if quantity > 0:
                        OrderDetails.objects.create(order=instance, product=product, quantity=quantity, total=total)
    
        # Calcula el total de todos los detalles de la orden
        total_order = sum(detail.total for detail in OrderDetails.objects.filter(order=instance))
        instance.total = total_order  # Actualiza el total de la orden con total_order
        instance.save()
        return instance
