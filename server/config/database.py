import mongoengine

from django.conf import settings


_CONNECTION_ALIAS = "default"


def connect_db():

    return mongoengine.connect(
        db=settings.MONGO_DB_NAME,
        host=settings.MONGO_HOST,
        alias=_CONNECTION_ALIAS,

        retryWrites=True,

        maxPoolSize=20,
        minPoolSize=0,

        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=20000,
    )


def disconnect_db():

    mongoengine.disconnect(
        alias=_CONNECTION_ALIAS,
    )