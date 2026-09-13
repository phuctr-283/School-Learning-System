from django.urls import path

from apps.administrators.presentation.views.school_admin.get_school_admins_view import (
    GetSchoolAdminsView,
)
from apps.administrators.presentation.views.school_admin.register_school_admin_view import (
    RegisterSchoolAdminView,
)

from apps.administrators.presentation.views.super_admin.register_super_admin_view import (
    RegisterSuperAdminView,
)

urlpatterns = [

    path(
        "school-admins/list/",
        GetSchoolAdminsView.as_view(),
        name="get-school-admins",
    ),
    path(
        "school-admins/register/",
        RegisterSchoolAdminView.as_view(),
        name="register-school-admin",
    ),

    path(
        "super-admins/register/",
        RegisterSuperAdminView.as_view(),
        name="register-super-admin",
    ),
]