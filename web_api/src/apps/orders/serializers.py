from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from products.models import Product
from .models import Order, OrderProductMembership


class OrderProductMembershipListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderProductMembership
        fields = ('id', 'name', 'price', 'quantity')


class OrderProductMembershipCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')

    class Meta:
        model = OrderProductMembership
        fields = ('id', 'quantity')


class OrderListSerializer(serializers.ModelSerializer):
    products = OrderProductMembershipListSerializer(source='orderproductmembership_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('status', 'total_price', 'products', 'shipping_details', 'created_date', 'shipment_date',
                  'close_date')
        depth = 1


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    products = OrderProductMembershipCreateUpdateSerializer(source='orderproductmembership_set',
                                                            many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('products', 'shipping_details')
        depth = 1

    def create(self, validated_data):
        products = self.initial_data.get('products')
        if not products:
            raise serializers.ValidationError('Products must be set.')

        order_instance = super().create(validated_data)
        for product in products:
            product_instance = get_object_or_404(Product, pk=product.get('id'))
            OrderProductMembership.objects.get_or_create(
                product=product_instance,
                order=order_instance,
                quantity=product.get('quantity'))
        return order_instance

    def update(self, instance, validated_data):
        products = self.initial_data.get('products')
        if not products:
            raise serializers.ValidationError('Products must be set.')

        # update or create products for order
        for product in products:
            product_instance = get_object_or_404(Product, pk=product.get('id'))
            OrderProductMembership.objects.update_or_create(
                product=product_instance,
                order=instance,
                defaults={
                    'quantity': product.get('quantity'),
                }
            )

        # remove old memberships if products not set
        OrderProductMembership.objects\
            .select_related('product')\
            .filter(order=instance)\
            .exclude(product__pk__in=[product['id'] for product in products])\
            .delete()

        return super().update(instance, validated_data)
