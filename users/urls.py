from django.urls import path

from .views import (
    SendOrResendSMSAPIView,
    UserLoginAPIView,
    UserRegisterationAPIView,
    VerifyPhoneNumberAPIView,
)

app_name = 'users'

urlpatterns = [

    path('register/', UserRegisterationAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),

    path(
        'send-sms/',
        SendOrResendSMSAPIView.as_view(),
        name='send_resend_sms'
    ),
    path(
        'verify-phone/',
        VerifyPhoneNumberAPIView.as_view(),
        name='verify_phone_number'
    ),
]
