from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, generics

from orders.models import Order, OrderItem
from orders.permissions import IsBuyerOrAdmin, IsOrderByBuyerOrAdmin, IsOrderPending
from orders.serializers import OrderItemSerializer, OrderReadSerializer, OrderWriteSerializer
from payment.models import Payment
from payment.serializers import PaymentOptionSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.

    Only owner of the ordered items are permitted for CRUD operation.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsOrderByBuyerOrAdmin, )

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD orders of a user
    """
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsBuyerOrAdmin, IsOrderPending, )
        else:
            self.permission_classes = (permissions.IsAuthenticated, )

        return super().get_permissions()


class PaymentOptionCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentOptionSerializer

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)


class PaymentOptionAPIView(generics.RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentOptionSerializer

    def get_object(self):
        order_id = self.kwargs.get('order_id')
        return Payment.objects.filter(order=order_id).first()
