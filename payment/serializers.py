from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    buyer = serializers.CharField(
        source='order.buyer.get_full_name', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'buyer', 'status', 'payment_option',
                  'order', 'created_at', 'updated_at')
