import mongoengine
from django.conf import settings


def test_mongodb():

    print("=" * 60)
    print("MONGODB TEST")

    print(
        "DB:",
        settings.MONGO_DB_NAME,
    )

    connection = mongoengine.get_connection(
        alias="default",
    )

    print(
        "HOST:",
        connection.address,
    )

    print(
        "REPLICA SET:",
        connection.replica_set,
    )

    print(
        "NODES:",
        connection.nodes,
    )

    print("-" * 60)
    print("PING:")

    try:
        result = connection.admin.command("ping")
        print(result)
    except Exception as error:
        print(
            "PING ERROR:",
            repr(error),
        )

    print("-" * 60)
    print("HELLO:")

    try:
        result = connection.admin.command("hello")

        print(
            "IS WRITABLE PRIMARY:",
            result.get("isWritablePrimary"),
        )

        print(
            "PRIMARY:",
            result.get("primary"),
        )

        print(
            "SET NAME:",
            result.get("setName"),
        )

        print(
            "ME:",
            result.get("me"),
        )

    except Exception as error:
        print(
            "HELLO ERROR:",
            repr(error),
        )

    print("=" * 60)