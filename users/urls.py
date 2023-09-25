from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    change_password_view,
    refresh_token_view,
)

app_name = "users"

urlpatterns: list = [
    path("register", register_view, name="register"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("change-password", change_password_view, name="changepassword"),
    path("token-refresh/", refresh_token_view, name="token_refresh"),
]
