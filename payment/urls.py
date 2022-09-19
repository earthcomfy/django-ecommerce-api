from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import PaymentViewSet


app_name = 'payment'

router = DefaultRouter()
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
