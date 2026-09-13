import mongoengine
from django.conf import settings


def connect_db():
    return mongoengine.connect(
        db=settings.MONGO_DB_NAME,
        host=settings.MONGO_HOST,
        alias="default",

        retryWrites=True,

        maxPoolSize=50,
        minPoolSize=5,
    )