from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet, CartViewSet


app_name = 'cart'

router = DefaultRouter()
router.register(r'^(?P<cart_id>\d+)/cart-items', CartItemViewSet)
router.register(r'', CartViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
