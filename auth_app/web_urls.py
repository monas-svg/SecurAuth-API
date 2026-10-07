from django.urls import path

from .views import (
    web_forgot_password,
    web_home,
    web_login,
    web_profile,
    web_register,
    web_reset_password,
)

urlpatterns = [
    path("", web_home, name="web-home"),
    path("login/", web_login, name="web-login"),
    path("register/", web_register, name="web-register"),
    path("forgot-password/", web_forgot_password, name="web-forgot-password"),
    path("reset-password/", web_reset_password, name="web-reset-password"),
    path("profile/", web_profile, name="web-profile"),
]
