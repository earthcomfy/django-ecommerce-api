from django.urls import path

from .views import (
    AddressAPIView,
    ProfileAPIView,
    SendOrResendSMSAPIView,
    UserAPIView,
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

    path('profile/', ProfileAPIView.as_view(), name='profile_detail'),
    path('', UserAPIView.as_view(), name='user_detail'),
    path('profile/address/', AddressAPIView.as_view(), name='address_detail'),

]
