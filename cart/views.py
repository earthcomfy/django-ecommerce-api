from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView

from cart.models import Cart, CartItem
from cart.permissions import IsCartItemByOwnerOrAdmin, IsUserCartOwner
from cart.serializers import CartItemSerializer, CartReadSerializer


class CartItemViewSet(ModelViewSet):
    """
    CRUD cart items that are associated with the current cart id.

    Only owner of the cart items are permitted for CRUD operation.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsCartItemByOwnerOrAdmin, )

    def get_queryset(self):
        res = super().get_queryset()
        cart = self.request.user.cart
        return res.filter(cart=cart)

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, id=self.kwargs.get('cart_id'))
        serializer.save(cart=cart)


class CartAPIView(RetrieveAPIView):
    """
    Read only view of a cart model and its items
    """
    queryset = Cart.objects.all()
    serializer_class = CartReadSerializer
    permission_classes = (IsUserCartOwner, )

    def get_object(self):
        return self.request.user.cart
