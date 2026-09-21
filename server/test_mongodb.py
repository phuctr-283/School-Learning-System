import os

from pathlib import Path

from dotenv import load_dotenv

from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent


load_dotenv(
    BASE_DIR / ".env",
)


MONGO_URI = os.getenv(
    "MONGODB_URI",
)


if not MONGO_URI:

    raise RuntimeError("MONGODB_URI chưa được cấu hình.")


client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=10000,
    connectTimeoutMS=10000,
    socketTimeoutMS=20000,
)


try:

    print()
    print("========================================")
    print("TEST MONGODB ATLAS")
    print("========================================")

    result = client.admin.command("ping")

    print("MongoDB connection: OK")

    print(result)

except Exception as error:

    print()
    print("MongoDB connection: FAILED")

    print(type(error).__name__)

    print(error)

finally:

    client.close()
