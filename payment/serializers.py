from rest_framework import serializers

from payment.models import Payment


class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'payment_option', 'order')
        read_only_fields = ('order', )
