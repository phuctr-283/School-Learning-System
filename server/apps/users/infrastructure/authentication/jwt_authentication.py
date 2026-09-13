import jwt

from django.conf import settings

from rest_framework.authentication import (
    BaseAuthentication,
)

from rest_framework.exceptions import (
    AuthenticationFailed,
)

from apps.users.application.dto.auth_dto import (
    AuthUserDTO,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header không hợp lệ")

        token = auth_header.split(
            " ",
            1,
        )[1].strip()

        if not token:
            raise AuthenticationFailed("Access token không được để trống")

        try:

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

        except jwt.ExpiredSignatureError:

            raise AuthenticationFailed("Access token đã hết hạn")

        except jwt.InvalidTokenError:

            raise AuthenticationFailed("Access token không hợp lệ")

        if payload.get("type") != "access":

            raise AuthenticationFailed("Token không phải access token")

        user_id = payload.get("user_id")

        username = payload.get("username")

        account_level = payload.get("account_level")

        university_id = payload.get("university_id")

        if not user_id or not username or account_level is None:
            raise AuthenticationFailed("Token thiếu thông tin người dùng")

        try:

            level = AccountLevel(account_level)

        except (
            ValueError,
            TypeError,
        ):

            raise AuthenticationFailed("Account level không hợp lệ")

        if level == AccountLevel.SUPER_ADMIN:

            if university_id is not None:
                raise AuthenticationFailed("Super Admin không thuộc trường")

        else:

            if not university_id:
                raise AuthenticationFailed("Tài khoản chưa được gắn với trường")

        user = AuthUserDTO(
            user_id=str(user_id),
            username=username,
            account_level=level,
            university_id=(str(university_id) if university_id else None),
        )

        return (
            user,
            token,
        )
