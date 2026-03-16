from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users_app.controller.user_controller import (
    register_user,
    login_user,
    get_users,
    update_user,
    delete_user
)

urlpatterns = [

    path("register/", register_user, name="register_api"),

    path("login/", login_user, name="login_api"),

    path("users/", get_users, name="view_all_users"),

    path("users/<int:user_id>/update/", update_user, name="update_user"),

    path("users/<int:user_id>/delete/", delete_user, name="delete_user"),
]  