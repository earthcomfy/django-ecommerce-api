from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from cart.models import Cart, CartItem
from cart.permissions import IsCartByOwnerOrAdmin, IsUserOwner
from cart.serializers import CartItemSerializer, CartReadSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    """
    CRUD cart items that are associated with the current cart id.

    Only owner of the cart items are permitted for CRUD operation.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsCartByOwnerOrAdmin, )

    def get_queryset(self):
        res = super().get_queryset()
        cart_id = self.kwargs.get('cart_id')
        return res.filter(cart__id=cart_id)

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, id=self.kwargs.get('cart_id'))
        serializer.save(cart=cart)


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only view of a cart model and its items
    """
    queryset = Cart.objects.all()
    serializer_class = CartReadSerializer
    permission_classes = (IsUserOwner, )
