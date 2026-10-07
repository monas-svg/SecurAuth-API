from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("auth/profile/update/", ProfileView.as_view(), name="profile-update"),
    path("auth/password/reset/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("auth/password/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
