import jwt

from uuid import uuid4

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from django.conf import settings


class JWTService:

    # =========================================
    # ACCESS TOKEN
    # =========================================

    @staticmethod
    def generate_access_token(user):

        now = datetime.now(timezone.utc)

        payload = {
            "jti": str(uuid4()),
            "user_id": str(user.user_id),
            "username": user.username,
            "account_level": (user.account_level.value),
            "university_id": (str(user.university_id) if user.university_id else None),
            "type": "access",
            "iat": now,
            "exp": (
                now + timedelta(minutes=(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
            ),
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    # =========================================
    # REFRESH TOKEN
    # =========================================

    @staticmethod
    def generate_refresh_token(user):

        now = datetime.now(timezone.utc)

        payload = {
            "jti": str(uuid4()),
            "user_id": str(user.user_id),
            "username": user.username,
            "account_level": (user.account_level.value),
            "university_id": (str(user.university_id) if user.university_id else None),
            "type": "refresh",
            "iat": now,
            "exp": (now + timedelta(days=(settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))),
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    # =========================================
    # GENERATE BOTH TOKENS
    # =========================================

    @staticmethod
    def generate_tokens(user):

        return {
            "access_token": (JWTService.generate_access_token(user)),
            "refresh_token": (JWTService.generate_refresh_token(user)),
        }

    # =========================================
    # DECODE TOKEN
    # =========================================

    @staticmethod
    def decode_token(token):

        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )

    # =========================================
    # DECODE REFRESH TOKEN
    # =========================================

    @staticmethod
    def decode_refresh_token(token):

        payload = JWTService.decode_token(token)

        if payload.get("type") != "refresh":
            raise ValueError("Token không phải refresh token")

        return payload
