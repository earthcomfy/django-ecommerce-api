from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.views import CartAPIView, CartItemViewSet


app_name = 'cart'

router = DefaultRouter()
router.register(r'', CartItemViewSet)


urlpatterns = [
    path('', CartAPIView.as_view(), name='user_cart'),
    path('cart-items/', include(router.urls)),
]
