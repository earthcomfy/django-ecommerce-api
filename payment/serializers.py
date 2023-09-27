from rest_framework import serializers

from orders.models import Order
from payment.models import Payment
from users.models import Address
from users.serializers import BillingAddressSerializer, ShippingAddressSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer to CRUD payments for an order.
    """

    buyer = serializers.CharField(source="order.buyer.get_full_name", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "buyer",
            "status",
            "payment_option",
            "order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status",)


class PaymentOptionSerializer(serializers.ModelSerializer):
    """
    Payment serializer for checkout. Order will be automatically set during checkout.
    """

    buyer = serializers.CharField(source="order.buyer.get_full_name", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "buyer",
            "status",
            "payment_option",
            "order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "order")


class CheckoutSerializer(serializers.ModelSerializer):
    """
    Serializer class to set or update shipping address, billing address and payment of an order.
    """

    shipping_address = ShippingAddressSerializer()
    billing_address = BillingAddressSerializer()
    payment = PaymentOptionSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "payment",
            "shipping_address",
            "billing_address",
        )

    def update(self, instance, validated_data):
        order_shipping_address = None
        order_billing_address = None
        order_payment = None

        shipping_address = validated_data["shipping_address"]

        # Shipping address for an order is not set
        if not instance.shipping_address:
            order_shipping_address = Address(**shipping_address)
            order_shipping_address.save()
        else:
            # Shipping address for an order is already set so update its value
            address = Address.objects.filter(shipping_orders=instance.id)
            address.update(**shipping_address)

            order_shipping_address = address.first()

        billing_address = validated_data["billing_address"]

        # Billing address is not set for an order
        if not instance.billing_address:
            order_billing_address = Address(**billing_address)
            order_billing_address.save()

        else:
            # Billing address is set so update its value
            address = Address.objects.filter(billing_orders=instance.id)
            address.update(**billing_address)

            order_billing_address = address.first()

        payment = validated_data["payment"]

        # Payment option is not set for an order
        if not instance.payment:
            order_payment = Payment(**payment, order=instance)
            order_payment.save()

        else:
            # Payment option is set so update its value
            p = Payment.objects.filter(order=instance)
            p.update(**payment)

            order_payment = p.first()

        # Update order
        instance.shipping_address = order_shipping_address
        instance.billing_address = order_billing_address
        instance.payment = order_payment
        instance.save()

        return instance
