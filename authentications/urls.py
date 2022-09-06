from django.urls import path
from .views import RegisterView, LoginApiView, AuthUserApiView, GenLoginOTPApiView


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/verify', LoginApiView.as_view(), name='verify_otp'),
    path('auth/login', GenLoginOTPApiView.as_view(), name='login'),
    path('user', AuthUserApiView.as_view(), name='auth_user'),
]