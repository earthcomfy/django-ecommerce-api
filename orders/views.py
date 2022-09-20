from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics

from orders.models import Order, OrderItem
from orders.permissions import IsOrderByBuyerOrAdmin, IsOrderItemByBuyerOrAdmin, IsOrderPending
from orders.serializers import OrderItemSerializer, OrderReadSerializer, OrderWriteSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.

    Only owner of the ordered items are permitted for CRUD operation.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsOrderItemByBuyerOrAdmin, )

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

    Only owner of the order are permitted for CRUD operation.
    """
    queryset = Order.objects.all()
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user_id = self.kwargs.get('user_id')
        return res.filter(buyer=user_id)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()
