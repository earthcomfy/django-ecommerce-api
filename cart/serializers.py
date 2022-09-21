from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions

from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing cart items
    """
    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity',
                  'price', 'cost', 'created_at', 'updated_at', )
        read_only_fields = ('cart', )

    def validate(self, validated_data):
        order_quantity = validated_data['quantity']
        product_quantity = validated_data['product'].quantity

        cart = self.context['view'].kwargs.get('cart_id')
        product = validated_data['product']
        current_item = CartItem.objects.filter(cart__id=cart, product=product)

        if order_quantity > product_quantity:
            error = {'quantity': _('Ordered quantity is more than the stock.')}
            raise serializers.ValidationError(error)

        if not self.instance and current_item.count() > 0:
            error = {'product': _('Product already exists in your cart.')}
            raise serializers.ValidationError(error)

        if self.context['request'].user == product.seller:
            error = _('Adding your own product to your cart is not allowed')
            raise exceptions.PermissionDenied(error)

        return validated_data

    def get_price(self, obj):
        return obj.product.price

    def get_cost(self, obj):
        return obj.cost


class CartReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading cart and its items
    """
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    cart_items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items', 'created_at', 'updated_at')
