from django.urls import path
# views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from authentication.api.views.index import (
    RegisterAV,
    LoginAV,
    ForgotPasswordAV,
    CheckPasswordTokenAV,
    ResetPasswordAV
)

urlpatterns = [
    path('register', RegisterAV.as_view(), name='register'),
    path('login', LoginAV.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('verify', TokenVerifyView.as_view(), name='verify'),
    path('reset-password', ForgotPasswordAV.as_view(), name='reset-password'),
    path('password-reset/<uidb64>/<token>',CheckPasswordTokenAV.as_view(), name='password-reset-confirm'),
    path('reset-password-complete', ResetPasswordAV.as_view(),name='password-reset-complete'),
]

