from django.urls import path

from apps.users.presentation.views.login_view import (
    LoginView,
)

from apps.users.presentation.views.logout_view import (
    LogoutView,
)

from apps.users.presentation.views.refresh_token_view import (
    RefreshTokenView,
)

from apps.users.presentation.views.create_user_view import (
    CreateUserView,
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "refresh/",
        RefreshTokenView.as_view(),
        name="refresh-token",
    ),
    path(
        "create/",
        CreateUserView.as_view(),
        name="create-user",
    ),
]
