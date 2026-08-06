from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register_phone, name="register"),
    path("verify/", views.verify_code, name="verify_code"),
    path( "complete-register/", views.complete_register, name="complete_register"),
    path(
        "logout/",
    views.logout_view,
    name="logout"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "phone-login/",
        views.phone_login,
        name="phone_login"
    ),

    path(
        "phone-verify/",
        views.phone_verify,
        name="phone_verify",
    ),

    path("profile/", views.profile, name="profile"),

    path("profile/orders/", views.orders, name="orders"),
    path("profile/account/", views.account_info, name="account_info"),
    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),
]