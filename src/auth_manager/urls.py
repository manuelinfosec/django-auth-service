from django.urls import path

from auth_manager.views import ManageUserView, CreateUserView, TestSecuredView
from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    refresh_jwt_token,
)

MANAGE_USER = ManageUserView.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    # User Registration
    path("register/", CreateUserView.as_view({"post": "create"}), name="register"),
    # API View that receives a POST with a user's username and password.
    path("login/", obtain_jwt_token, name="login_user"),
    # CRUD operations for user management
    path("user/", MANAGE_USER, name="manage_user"),
    # Check that authentication worked
    path("protected/", TestSecuredView.as_view(), name="protected_endpoint"),
    # checks the validity of a token, returning the token if it is valid.
    path("token_verify/", verify_jwt_token, name="verify_token"),
    # API View that returns a refreshed token (with new expiration) based on existing token
    path("token_refresh/", refresh_jwt_token, name="refresh_token"),
]
