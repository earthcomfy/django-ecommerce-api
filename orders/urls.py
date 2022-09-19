from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import OrderItemViewSet, OrderViewSet, PaymentOptionAPIView, PaymentOptionCreateAPIView


app_name = 'orders'

router = DefaultRouter()
router.register(r'^(?P<order_id>\d+)/order-items', OrderItemViewSet)
router.register(r'', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<int:order_id>/create-payment-option/',
         PaymentOptionCreateAPIView.as_view(), name='create_payment_option'),
    path('<int:order_id>/payment-option/',
         PaymentOptionAPIView.as_view(), name='payment_option_detail'),

]
