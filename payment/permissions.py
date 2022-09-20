from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from orders.models import Order


class IsPaymentByUser(BaseException):
    """
    Check if payment belongs to the appropriate buyer or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.order.buyer == request.user or request.user.is_staff


class IsPaymentPending(BasePermission):
    """
    Check if the status of payment is pending or completed before updating/deleting instance
    """
    message = _('Updating or deleting completed payment is not allowed.')

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve',):
            return True
        return obj.status == 'P'


class IsPaymentForOrderNotCompleted(BasePermission):
    message = _(
        'Creating a checkout session for completed payment is not allowed.')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            order_id = view.kwargs.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            return order.status != 'C'
        return False
