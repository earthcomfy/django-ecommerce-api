from rest_framework import viewsets

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user_id = self.kwargs.get('user_id')
        return res.filter(order__buyer=user_id)
