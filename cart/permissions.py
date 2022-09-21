from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _


class IsUserCartOwner(BasePermission):
    """
    Check if authenticated user is owner of the cart or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsCartItemByOwnerOrAdmin(BasePermission):
    """
    Check if cart item is owned by appropriate user or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user or request.user.is_staff
