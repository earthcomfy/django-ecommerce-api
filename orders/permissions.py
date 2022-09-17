from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.translation import gettext_lazy as _

from orders.models import Order


class IsBuyerOrAdmin(BasePermission):
    """
    Check if authenticated user is buyer of the product or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.buyer == request.user or request.user.is_staff


class IsOrderPending(BasePermission):
    """
    Check the status of order is pending or completed before updating/deleting instance
    """
    message = _('Updating or deleting closed order is not allowed.')

    def has_object_permission(self, request, view, obj):
        return obj.status == 'P'


class IsOrderByBuyerOrAdmin(BasePermission):
    """
    Check if order item is owned by appropriate buyer or admin
    """

    def has_permission(self, request, view):
        order_id = view.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return order.buyer == request.user or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.order.buyer == request.user or request.user.is_staff
