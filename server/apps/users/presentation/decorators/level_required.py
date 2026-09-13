from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


def level_required(
    minimum_level: AccountLevel,
):

    if not isinstance(
        minimum_level,
        AccountLevel,
    ):

        raise ValueError("minimum_level không hợp lệ")

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(
            request,
            *args,
            **kwargs,
        ):

            user = getattr(
                request,
                "user",
                None,
            )

            if not user or not getattr(
                user,
                "is_authenticated",
                False,
            ):

                return Response(
                    {
                        "success": False,
                        "message": "Chưa đăng nhập",
                    },
                    status=(status.HTTP_401_UNAUTHORIZED),
                )

            account_level = getattr(
                user,
                "account_level",
                None,
            )

            if account_level is None:

                return Response(
                    {
                        "success": False,
                        "message": "Tài khoản chưa được phân quyền",
                    },
                    status=(status.HTTP_403_FORBIDDEN),
                )

            if not isinstance(
                account_level,
                AccountLevel,
            ):

                try:

                    account_level = AccountLevel(account_level)

                except ValueError:

                    return Response(
                        {
                            "success": False,
                            "message": "Account level không hợp lệ",
                        },
                        status=(status.HTTP_403_FORBIDDEN),
                    )

            if account_level > minimum_level:

                return Response(
                    {
                        "success": False,
                        "message": "Bạn không có quyền truy cập",
                    },
                    status=(status.HTTP_403_FORBIDDEN),
                )

            return view_func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator
